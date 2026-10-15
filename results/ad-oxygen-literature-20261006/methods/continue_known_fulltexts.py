"""Resume retrieval of existing included IDs from recorded, identity-bound sources.

No keyword searches or scope decisions. Files remain outside Git until their
identity, version and redistribution permission are reviewed separately.
"""
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlsplit, urljoin, unquote
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError
from email.utils import parsedate_to_datetime
import argparse, csv, hashlib, json, re, threading, time, unicodedata, zipfile, io
import fitz


def normalized(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', text)


class Links(HTMLParser):
    def __init__(self, base):
        super().__init__(); self.base=base; self.pdf=[]; self.si=[]; self.a=None; self.text=[]; self.metadata={}; self.page_title=''; self.in_title=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='meta':self.metadata[a.get('name',a.get('property','')).lower()]=a.get('content','')
        if tag=='title':self.in_title=True
        if tag=='meta' and a.get('name','').lower()=='citation_pdf_url':
            self.pdf.append(urljoin(self.base,a.get('content','')))
        if tag=='a': self.a=(a.get('href',''),a.get('title','')); self.text=[]
    def handle_data(self,text):
        if self.a: self.text.append(text)
        if self.in_title:self.page_title+=text
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag!='a' or not self.a:return
        href,title=self.a; label=' '.join(self.text); value=(href+' '+title+' '+label).lower()
        u=urljoin(self.base,href); path=urlsplit(u).path.lower()
        is_si=any(s in value for s in ['supplement','supporting information','additional file','suppl_file','/esm','-s001','_s1.','_s001.'])
        file_link=bool(re.search(r'\.(pdf|docx?|xlsx?|csv|tsv|zip|gz|txt|rar|pptx?|r|py|fasta|xml)$',path))
        if is_si and (file_link or '/bin/' in path):self.si.append(u)
        elif path.endswith('.pdf') or ('/pdf' in path and 'download' in label.lower()):self.pdf.append(u)
        self.a=None


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None


class Retriever:
    def __init__(self, root, out, group, workers=2, retry_failed=False):
        self.root=root; self.out=out; self.group=group; self.out.mkdir(parents=True,exist_ok=True)
        self.log_path=out/(group+'_access.jsonl'); self.state_path=out/(group+'_results.json')
        self.lock=threading.RLock(); self.host_locks={}; self.last={}; self.blocked={}; self.cooldown={}
        self.opener=build_opener(NoRedirect()); self.results={}
        self.retry_failed=retry_failed
        if self.state_path.exists(): self.results=json.loads(self.state_path.read_text())
    def event(self,event):
        event['time_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
        with self.lock:
            with self.log_path.open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')
    def get(self,id,url):
        for hop in range(6):
            host=urlsplit(url).hostname
            if not host or urlsplit(url).scheme not in ('https','http'):return None
            with self.lock: host_lock=self.host_locks.setdefault(host,threading.Lock())
            with host_lock:
                if host in self.blocked or self.cooldown.get(host,0)>time.time():
                    self.event({'id':id,'url':url,'host':host,'skipped':self.blocked.get(host,'Retry-After cooldown')}); return None
                time.sleep(max(0,3-(time.monotonic()-self.last.get(host,0))))
                event={'id':id,'url':url,'host':host}
                try:
                    response=self.opener.open(Request(url,headers={'User-Agent':'AD literature existing-record retrieval/20261015'}),timeout=30)
                    with response:
                        data=response.read(60*1024*1024+1)
                        if len(data)>60*1024*1024:raise ValueError('file exceeds 60 MiB review limit')
                        event.update(http=response.status,bytes=len(data),content_type=response.headers.get('Content-Type',''))
                    self.last[host]=time.monotonic(); self.event(event)
                    return data,url,event.get('content_type','')
                except HTTPError as ex:
                    event['http']=ex.code
                    if ex.code in (301,302,303,307,308):
                        target=urljoin(url,ex.headers.get('Location',''));event['redirect']=target;self.event(event)
                        self.last[host]=time.monotonic();url=target;continue
                    if ex.code==429:
                        retry=ex.headers.get('Retry-After',''); delay=300
                        try:delay=float(retry)
                        except ValueError:
                            try:delay=parsedate_to_datetime(retry).timestamp()-time.time()
                            except Exception:pass
                        self.cooldown[host]=time.time()+max(60,delay);event['cooldown_seconds']=max(60,delay)
                    snippet=ex.read(500).decode('utf-8','replace');event['response_excerpt']=snippet
                    if ex.code in (401,403):self.blocked[host]='HTTP'+str(ex.code)+'; source paused this run'
                except Exception as ex:
                    # Error text must not contain proxy credentials or runtime proxy addresses.
                    error=str(ex)
                    event['error_type']=type(ex).__name__
                    event['error']='CONNECT403' if 'Tunnel connection failed: 403' in error else type(ex).__name__
                    if 'Tunnel connection failed: 403' in error:self.blocked[host]='CONNECT403'
                self.last[host]=time.monotonic();self.event(event);return None
        return None
    def pdf_check(self,data,row,historical=None):
        result={'verified':False,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
        if not data.lstrip().startswith(b'%PDF'):return result
        try:
            doc=fitz.open(stream=data,filetype='pdf');texts=[p.get_text() for p in doc];result['pages']=len(texts)
            alltext='\n'.join(texts);front='\n'.join(texts[:4]);norm=normalized(front)
            result['all_pages_parsed']=True
            if historical and result['sha256']==historical['SHA256']:
                result.update(verified=True,historical_sha_match=True,version=historical['PDF版本'],verification='historical byte identity + all-page PDF parsing');return result
            words=set(re.findall(r'[a-z]{3,}',unicodedata.normalize('NFKD',row['完整题名']).encode('ascii','ignore').decode().lower()))
            frontwords=set(re.findall(r'[a-z]{3,}',unicodedata.normalize('NFKD',front).encode('ascii','ignore').decode().lower()))
            coverage=len(words&frontwords)/max(1,len(words));doi=row['DOI（原库不改）'].lower()
            first_author=row['作者（原库不改）'].split(';')[0].strip()
            surname=first_author.split(',')[0] if ',' in first_author else first_author.split()[-1] if first_author else ''
            result.update(title_token_coverage=coverage,first_author_present=bool(surname and normalized(surname) in norm),doi_in_front=bool(doi and normalized(doi) in norm),body_chars=len(alltext))
            lower=alltext.lower()
            sections=sum(bool(re.search(pattern,lower)) for pattern in [r'\bintroduction\b',r'\bmaterials? and methods\b|\bmethodology\b|\bexperimental\b',r'\bresults\b',r'\bconclusions?\b',r'\breferences\b|\bbibliography\b'])
            result['body_section_types']=sections
            if 'accepted manuscript' in front.lower() or 'accepted version' in front.lower():version='accepted manuscript'
            elif 'journal pre-proof' in front.lower() or 'uncorrected proof' in front.lower():version='publisher proof; not final version'
            elif result['doi_in_front'] and any(x in front.lower() for x in ['journal','elsevier','springer','published','copyright','volume']):version='publisher formatted version; see file evidence'
            else:version='version requires manual verification'
            result['version']=version
            result['automated_checks_passed']=bool(result['pages']>=2 and len(alltext)>6000 and coverage>=0.78 and result['first_author_present'] and result['doi_in_front'] and sections>=3 and 'version requires' not in version)
            # A review can cite all target metadata; heuristic matches never prove
            # the identity of the PDF's own title/author block or its version.
            result['verified']=False
            result['manual_review_required']=True
            result['verification_status']='automated_candidate_pending_manual_identity_version'
            result['cc_by_evidence']=bool(re.search(r'creativecommons\.org/licenses/by/4\.0|creative commons attribution\s*\(cc by\)',alltext,re.I))
            if result['cc_by_evidence']:result['license']='CC BY (check exact version before sharing)'
        except Exception as ex:result['parse_error']=type(ex).__name__
        return result
    def process(self,task):
        id=task['id']; row=task['row'];old=self.results.get(id)
        reused_body=None
        if old and old.get('body',{}).get('verified') and Path(old['body']['path']).is_file():
            if hashlib.sha256(Path(old['body']['path']).read_bytes()).hexdigest()==old['body']['sha256']:
                reused_body=old['body']
                # A completed SI attempt is not a claim of complete SI coverage.
                # Explicit --retry-failed resumes SI after a source/config change,
                # while the verified body bytes are reused independently.
                if not self.retry_failed:return old
        if old and old.get('status') and not old.get('body',{}).get('verified') and not self.retry_failed:
            return old
        result={'id':id,'doi':row['DOI（原库不改）'],'scope_changed':False,'group':self.group,'urls_considered':task['urls'],'body':reused_body or {'verified':False},'si':[],'attempted':True}
        todo=list(task['urls']);visited=set();pages=0
        while todo and len(visited)<10:
            url=todo.pop(0)
            if url in visited:continue
            if reused_body and url==reused_body.get('source_url'):continue
            mapped_host={'10.1016':'www.sciencedirect.com','10.1007':'link.springer.com','10.2166':'iwaponline.com','10.1021':'pubs.acs.org'}.get(row['DOI（原库不改）'].split('/')[0])
            if urlsplit(url).hostname in ('doi.org','dx.doi.org') and mapped_host in self.blocked:
                self.event({'id':id,'url':url,'skipped':'known publisher host paused: '+mapped_host});continue
            if result['body']['verified'] and re.search(r'/pdf|\.pdf',urlsplit(url).path,re.I):continue
            visited.add(url); response=self.get(id,url)
            if not response:continue
            data,actual,content_type=response
            if data.lstrip().startswith(b'%PDF'):
                check=self.pdf_check(data,row,task.get('historical'))
                name=(task.get('historical') or {}).get('PDF文件名') or id+'_'+(row['正式年份（原库不改）'] or row['索引年份'] or 'year_unknown')+'_'+re.sub(r'[^A-Za-z0-9]+','_',row['完整题名'])[:100]+'.pdf'
                directory=self.out/('fulltexts' if check['verified'] else 'candidates');directory.mkdir(exist_ok=True)
                if not check['verified']:name=Path(name).stem+'_'+check['sha256'][:12]+'.pdf'
                path=directory/name;path.write_bytes(data);check.update(path=str(path),source_url=actual)
                if check['verified']:result['body']=check;continue
                result.setdefault('unverified_candidates',[]).append(check);continue
            html=data.decode('utf-8','replace')
            if any(x in html[:15000].lower() for x in ['just a moment','checking your browser','verify you are human','access denied','making sure you']):
                self.blocked[urlsplit(actual).hostname]='HTML challenge';continue
            if pages>=4:continue
            pages+=1; parser=Links(actual)
            try:parser.feed(html)
            except Exception:continue
            # Metadata-bound landing pages only; never walk citation/organization links.
            pdf_links=[u for u in dict.fromkeys(parser.pdf) if not re.search(r'catalog|mediapack|media.pack|price.list|brochure|leaflet|flyer|author.guidelines',u,re.I)]
            todo=pdf_links+todo
            page_title=parser.metadata.get('citation_title') or parser.metadata.get('dc.title') or parser.page_title
            page_identity=bool(normalized(row['完整题名']) and normalized(row['完整题名']) in normalized(page_title))
            for attachment in dict.fromkeys(parser.si):
                si_response=self.get(id,attachment)
                if not si_response:continue
                si,si_actual,mime=si_response
                if 'text/html' in mime or si.lstrip().startswith((b'<!DOCTYPE',b'<html',b'<!doctype')):continue
                name=Path(unquote(urlsplit(si_actual).path)).name or 'attachment.bin'
                name=re.sub(r'[^\w. -]','_',name)[:160]
                digest=hashlib.sha256(si).hexdigest()
                if any(x['sha256']==digest for x in result['si']):continue
                name=digest[:12]+'_'+name
                directory=self.out/'supplementary'/id;directory.mkdir(parents=True,exist_ok=True)
                dest=directory/name;dest.write_bytes(si)
                structure=False
                try:
                    if zipfile.is_zipfile(io.BytesIO(si)):
                        with zipfile.ZipFile(io.BytesIO(si)) as archive:structure=archive.testzip() is None
                    elif si.lstrip().startswith(b'%PDF'):
                        document=fitz.open(stream=si,filetype='pdf');structure=len(document)>0
                except Exception:pass
                result['si'].append({'path':str(dest),'source_url':si_actual,'bytes':len(si),'sha256':digest,'association':'supplementary link; title metadata matched' if page_identity else 'unverified landing-page association','landing_page_identity_matched':page_identity,'archive_or_pdf_structure_checked':structure,'verified':False,'manual_review_required':True,'content_type':mime})
        result['visited_urls']=list(visited)
        result['status']='verified body' if result['body']['verified'] else 'no newly verified body; see actual source events'
        with self.lock:
            self.results[id]=result
            temp=self.state_path.with_suffix('.tmp');temp.write_text(json.dumps(self.results,ensure_ascii=False,indent=2));temp.replace(self.state_path)
        print(json.dumps({'id':id,'verified':result['body']['verified'],'si_files':len(result['si'])}),flush=True)
        return result


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parent.parent)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--group',choices=['remaining335','historical91'],required=True)
    ap.add_argument('--gate',type=Path,required=True);ap.add_argument('--workers',type=int,default=2)
    ap.add_argument('--retry-failed',action='store_true',help='Only after a meaningful network/source change; otherwise completed failures are resumed without new requests')
    args=ap.parse_args()
    gate=json.loads(args.gate.read_text());assert gate.get('all_original_bytes_readback_verified') and gate.get('body_samples',0)>=3,'Remote original-byte readback gate is required'
    def read(rel):
        with (args.project/rel).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
    current={r['原记录ID']:r for r in read('manual_review/scansci_download_status_utf8.csv')}
    hist={r['原记录ID']:r for r in read('methods/audit/scansci_verified_pdf_manifest_utf8.csv')}
    old=json.loads((args.project/'methods/audit/scansci_sourcewise_results.json').read_text());tasks=[]
    ids=[r['原记录ID'] for r in read('manual_review/scansci_need_fulltext_utf8.csv')] if args.group=='remaining335' else list(hist)
    for id in ids:
        row=current[id];urls=[]; previous=old.get(id,{})
        existing=Path(row.get('当前原件路径',''))
        if not existing.is_absolute():existing=args.project/existing
        if args.group=='historical91' and row.get('当前原件SHA256') and existing.is_file():
            if hashlib.sha256(existing.read_bytes()).hexdigest()==row['当前原件SHA256']:continue
        if row['实际PDF来源URL（下载或历史记录明确）']:urls.append(row['实际PDF来源URL（下载或历史记录明确）'])
        urls+=json.loads(row['公开PDF候选URL（非下载URL绑定实录）'] or '[]')
        for location in previous.get('Unpaywall',{}).get('locations',[]):
            urls += [location.get(k) for k in ['url_for_pdf','url_for_landing_page','url'] if location.get(k)]
        urls+=previous.get('OpenAlex_additional_locations',[])
        for page in previous.get('HTML_entry_audits',[]):
            title=page.get('page_title','')
            if normalized(row['完整题名']) in normalized(title):urls+=page.get('matched_document_links',[])
        urls+=[row['官方文章/仓储入口']]
        clean=[]
        for u in urls:
            if not isinstance(u,str) or not u.startswith(('http://','https://')):continue
            host=urlsplit(u).hostname or ''
            if host in ['pubmed.ncbi.nlm.nih.gov','www.ncbi.nlm.nih.gov','doaj.org']:continue
            if host in ['api.elsevier.com']:continue # optional API credentials absent; use bound public routes
            if host in ['www.uva.es','www.ufc.br','www.wur.nl']:continue # known old OpenAIRE organizational-link pollution
            if u.startswith('http://'):
                # A new HTTPS variant, not a claim about the historical URL.
                # Never downgrade an HTTPS certificate failure to HTTP.
                secure='https://'+u[len('http://'):]
                if secure not in clean:clean.append(secure)
            elif u not in clean:clean.append(u)
        tasks.append({'id':id,'row':row,'urls':clean,'historical':hist.get(id) if args.group=='historical91' else None})
    retriever=Retriever(args.project,args.out,args.group,retry_failed=args.retry_failed)
    with ThreadPoolExecutor(max_workers=min(args.workers,2)) as pool:
        futures=[pool.submit(retriever.process,t) for t in tasks]
        for f in as_completed(futures):f.result()
    print(json.dumps({'group':args.group,'records':len(retriever.results),'verified':sum(r['body']['verified'] for r in retriever.results.values()),'paused_hosts':retriever.blocked,'cooldown_hosts':list(retriever.cooldown)}))


if __name__=='__main__':main()
