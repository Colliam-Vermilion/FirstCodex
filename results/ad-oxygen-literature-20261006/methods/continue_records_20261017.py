"""Continue only existing included records and their explicitly declared SI.

No keyword searches or classification. Preserve every acquired candidate; an
automated metadata heuristic cannot register a new PDF as verified. Originals
are backed up every five processed records or ten minutes, whichever is first.
"""
import argparse, collections, csv, hashlib, io, json, re, time, unicodedata, zipfile, signal, mimetypes
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup
import recovery_20261017 as r
from continue_known_fulltexts import Retriever, Links, normalized

class BoundedRetriever(Retriever):
    def event(self,event):
        clean={k:r.safe_url(v) if k in ['url','redirect','final_url'] and isinstance(v,str) else re.sub(r';(?:jsessionid|phpsessid)=[^/?#;\s"\'<>]*','',v,flags=re.I) if isinstance(v,str) else v for k,v in event.items()}
        return super().event(clean)
    def get(self,id,url):
        def deadline(signum,frame):raise TimeoutError('Per-request wall time exceeded')
        previous=signal.signal(signal.SIGALRM,deadline);signal.alarm(60)
        try:
            response=super().get(id,url)
            return (response[0],r.safe_url(response[1]),response[2]) if response else None
        finally:signal.alarm(0);signal.signal(signal.SIGALRM,previous)

def rows(name):return r.readcsv(r.ROOT/name)
def paused_doi_host(doi,blocked):
    routes={'10.1016':['www.sciencedirect.com','sciencedirect.com','linkinghub.elsevier.com','www.linkinghub.elsevier.com'],
        '10.1007':['link.springer.com','www.springer.com'],'10.1186':['link.springer.com','bmcmicrobiol.biomedcentral.com'],
        '10.2166':['iwaponline.com'],'10.1021':['pubs.acs.org'],'10.1002':['onlinelibrary.wiley.com'],
        '10.1111':['onlinelibrary.wiley.com'],'10.3390':['www.mdpi.com'],'10.1080':['www.tandfonline.com']}
    return next((h for h in routes.get(doi.split('/')[0],[]) if h in blocked),None)
def ready():
    gate=r.load(r.RUN/'pilot_gate.json',{})
    assert gate.get('all_original_bytes_readback_verified') and gate.get('body_samples',0)>=3,'Independent three-body readback is required'
    apply_approved_pdfs()
def store(id,role,name,data,url,version='',extra=None):
    assets=r.load(r.ASSETS,[]);digest=r.sha(data)
    old=next((a for a in assets if a['record_id']==id and a['sha256']==digest),None)
    if old and r.present(old):return old
    name=re.sub(r'[^\w. ()-]','_',Path(name).name)[:180]
    folder='fulltext' if role=='main' else 'supplementary/'+id if role=='supplementary' else 'source_evidence/'+id
    path=r.ROOT/'original_files'/folder/name;path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and r.sha(path.read_bytes())!=digest:path=path.with_name(path.stem+'_'+digest[:12]+path.suffix)
    path.write_bytes(data)
    a=old or {'record_id':id,'asset_id':id+'.'+role+'.'+digest[:16],'role':role,'official_attachment':role=='supplementary',
        'original_filename':name,'canonical_path':'','source_local_path':'','historical_sha256':'','archive_parent_asset_id':'','parsing_status':'pending'}
    a.update(preferred_for_record=role=='main',source_repo_path=str(path.relative_to(r.ROOT)),resolved_source_path=str(path),
        format=path.suffix.lstrip('.').lower(),size_bytes=len(data),sha256=digest,availability='present_sha_verified',
        storage_status='local_acquired_pending_remote_readback',source_url=r.safe_url(url),version=version,
        license_evidence=a.get('license_evidence','Private authorized research backup; source license not inferred'))
    if extra:a.update(extra)
    if role=='main':
        for existing in assets:
            if existing['record_id']==id and existing['role']=='main' and existing['sha256']!=digest:existing['preferred_for_record']=False
    if not old:assets.append(a)
    r.save(r.ASSETS,assets);return a

def checkpt(message):
    apply_approved_pdfs()
    # Full library refresh after acquired assets change. Failure-only checkpoints
    # persist the source ledger without rewriting every workbook and PDF parse.
    si_state=r.RUN/'supplementary_check.json'
    def signature():return r.sha(r.ASSETS.read_bytes()+(si_state.read_bytes() if si_state.exists() else b''))
    current_signature=signature()
    old=r.load(r.RUN/'last_full_refresh.json',{})
    if old.get('asset_signature')!=current_signature:
        r.audit();r.parse_files()
    r.sync(message)
    r.save(r.RUN/'last_full_refresh.json',{'asset_signature':signature(),'time_utc':r.now()})

def apply_approved_pdfs():
    path=r.RUN/'manual_approvals_20261017.json'
    approvals=r.load(path,{})
    changed=False
    for id,decision in approvals.items():
        if decision.get('applied_asset_id'):continue
        source=r.ROOT/decision['candidate_relative_path']
        if not source.exists():continue
        data=source.read_bytes();assert r.sha(data)==decision['sha256']
        doc=r.fitz.open(stream=data,filetype='pdf');texts=[p.get_text() for p in doc]
        assert len(texts)==decision['pages'] and sum(map(len,texts))>6000
        a=store(id,'main',decision.get('output_filename') or source.name,data,decision['source_url'],decision['version'],{'identity_review_20261017':decision})
        source.unlink()
        decision.update(applied_asset_id=a['asset_id'],canonical_path=a['source_repo_path'],applied_at_utc=r.now())
        changed=True
    if changed:r.save(path,approvals)

def known():
    ready();out=r.ROOT/'original_files/continuation_20261017';out.mkdir(parents=True,exist_ok=True)
    worker=BoundedRetriever(r.ROOT,out,'existing_included',workers=1)
    prior_pause=r.load(r.RUN/'batch_downloads.json',{}).get('paused_hosts',{})
    worker.blocked.update({h:'Paused after earlier source failure in this recovery pass: '+v for h,v in prior_pause.items()})
    if worker.log_path.exists():
        for line in worker.log_path.read_text().splitlines():
            event=json.loads(line);host=event.get('host') or urlsplit(event.get('url','')).hostname
            if host and (event.get('http') in [401,403,429] or event.get('error')=='CONNECT403'):
                worker.blocked[host]='Earlier observed access failure in the same continuation pass; no unchanged retry'
    previous=r.load(r.ROOT/'methods/audit/scansci_sourcewise_results.json',{})
    current={x['原记录ID']:x for x in rows('manual_review/scansci_download_status_utf8.csv')}
    hist={x['原记录ID']:x for x in rows('methods/audit/scansci_verified_pdf_manifest_utf8.csv')}
    finalmeta={m.get('record_id') or m.get('id'):m for m in r.load(r.ROOT/'methods/audit/final_record_metadata.json',[])}
    tasks=[]
    for row in rows('manual_review/current_environment_need_fulltext_utf8.csv'):
        id=row['原记录ID'];old=current[id];p=previous.get(id,{});urls=[]
        if old.get('实际PDF来源URL（下载或历史记录明确）'):urls.append(old['实际PDF来源URL（下载或历史记录明确）'])
        pmc=finalmeta.get(id,{}).get('pmc','')
        if re.fullmatch(r'PMC\d+',pmc):urls.append('https://europepmc.org/api/getPdf?pmcid='+pmc)
        urls+=json.loads(old.get('公开PDF候选URL（非下载URL绑定实录）') or '[]')
        for loc in p.get('Unpaywall',{}).get('locations',[]):
            urls += [loc[k] for k in ['url_for_pdf','url_for_landing_page','url'] if loc.get(k)]
        urls+=p.get('OpenAlex_additional_locations',[])
        for page in p.get('HTML_entry_audits',[]):
            if normalized(old['完整题名']) in normalized(page.get('page_title','')):urls+=page.get('matched_document_links',[])
        urls+=[old.get('官方文章/仓储入口','')]
        clean=[]
        for u in urls:
            if not isinstance(u,str) or not u.startswith(('http://','https://')):continue
            if urlsplit(u).hostname in ['api.elsevier.com','www.uva.es','www.ufc.br','www.wur.nl','pubmed.ncbi.nlm.nih.gov']:continue
            if u.startswith('http://'):u='https://'+u[7:]
            if u not in clean:clean.append(u)
        tasks.append({'id':id,'row':old,'urls':clean,'historical':hist.get(id)})
    r.save(r.RUN/'continuation_tasks.json',[{'record_id':t['id'],'known_urls':t['urls']} for t in tasks])
    checkpoint=time.monotonic();count=0
    for task in tasks:
        if worker.results.get(task['id'],{}).get('status'):continue
        paused=paused_doi_host(task['row']['DOI（原库不改）'],worker.blocked)
        if paused:
            task['urls']=[u for u in task['urls'] if urlsplit(u).hostname not in ['doi.org','dx.doi.org']]
        result=worker.process(task);id=task['id'];body=result.get('body',{})
        if body.get('verified'):
            path=Path(body['path']);store(id,'main',path.name,path.read_bytes(),body['source_url'],body.get('version',''))
            # Source canonicalization must not keep duplicate original bytes.
            path.unlink()
        count+=1
        if count%5==0 or time.monotonic()-checkpoint>=600:
            checkpt('Continue existing literature records and persist all acquired candidates');checkpoint=time.monotonic()
    checkpt('Complete known-source continuation pass')
    r.save(r.RUN/'continuation_summary.json',{'records_processed':len(worker.results),'new_records_processed_this_invocation':count,'paused_hosts':worker.blocked,'cooldown_hosts':list(worker.cooldown),'new_searches':False})

def text(e):return ''.join(e.itertext()).strip() if e is not None else ''
def localtag(e):return e.tag.rsplit('}',1)[-1] if isinstance(e.tag,str) else ''
def supplementary():
    ready();allmeta=r.load(r.ROOT/'methods/audit/final_record_metadata.json',[])
    metadata={m.get('record_id') or m.get('id'):m for m in allmeta}
    report=r.load(r.RUN/'supplementary_check.json',{})
    paused={};last={};events=[];count=0;checkpoint=time.monotonic()
    for id,m in metadata.items():
        paper=r.load(r.ROOT/'papers'/str(id)/'metadata.json',{})
        if not paper.get('included_for_download'):continue
        if id in report:continue
        pmc=m.get('pmc','')
        if not re.fullmatch(r'PMC\d+',pmc):continue
        xmlurl='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/fullTextXML'
        data=r.fetch_bytes(xmlurl,paused,last,events,id)
        record={'record_id':id,'checked_at_utc':r.now(),'article_url':xmlurl,'official_files':[],'external_data_links':[]}
        if not data:
            record.update(status='access_failed',reason=paused.get('www.ebi.ac.uk','request_failed'));report[id]=record;r.save(r.RUN/'supplementary_check.json',report);count+=1
            if count%5==0 or time.monotonic()-checkpoint>=600:
                checkpt('Persist supplementary access failures without claiming no attachments');checkpoint=time.monotonic()
            continue
        try:xml=ET.fromstring(data,parser=ET.XMLParser(target=ET.TreeBuilder(insert_pis=True)))
        except ET.ParseError:
            record['status']='invalid_XML_response';report[id]=record;r.save(r.RUN/'supplementary_check.json',report);continue
        title=text(xml.find('./front/article-meta/title-group/article-title'))
        doi=next((text(e) for e in xml.findall('./front/article-meta/article-id') if e.attrib.get('pub-id-type')=='doi'),'')
        if normalized(title)!=normalized(m['title']) or normalized(doi)!=normalized(m.get('doi','')):
            record.update(status='identity_review_required',actual_title=title,actual_doi=doi);report[id]=record;r.save(r.RUN/'supplementary_check.json',report);continue
        store(id,'evidence_xml',pmc+'_fullText.xml',data,xmlurl,'JATS full text')
        declarations=[]
        for element in xml.iter():
            if localtag(element) not in ['supplementary-material','inline-supplementary-material']:continue
            for e in element.iter():
                href=e.attrib.get('{http://www.w3.org/1999/xlink}href') or e.attrib.get('href')
                if not href:continue
                serial=ET.tostring(e,encoding='unicode')
                pis=dict(re.findall(r'<\?suppdata-(name|size|md5)\s+([^?]+)\?>',serial))
                name=pis.get('name',Path(urlsplit(href).path).name).strip()
                if not urlsplit(href).scheme and re.search(r'\.[A-Za-z0-9]{1,8}$',name):
                    declarations.append({'filename':name,'href':href,'expected_size':pis.get('size','').strip(),'expected_md5':pis.get('md5','').strip()})
                elif urlsplit(href).scheme in ['http','https']:
                    if re.search(r'\.(pdf|docx?|xlsx?|csv|tsv|png|jpe?g|tiff?|mp4|avi|mov|webm|zip|r|py|txt)$',urlsplit(href).path,re.I):
                        declarations.append({'filename':name,'href':href,'direct_url':href,'expected_size':pis.get('size','').strip(),'expected_md5':pis.get('md5','').strip()})
                    else:record['external_data_links'].append({'url':href,'size_bytes':None,'size_status':'not supplied; no bulk database download','downloaded':False})
        unique={x['filename']:x for x in declarations};record['declared_attachments']=list(unique.values())
        if unique:
            existing=[a for a in r.load(r.ASSETS,[]) if a['record_id']==id and a['role']=='supplementary' and r.present(a)]
            needed=[x for name,x in unique.items() if not any(a['original_filename']==name and (not x['expected_size'].isdigit() or int(x['expected_size'])==int(a['size_bytes'])) for a in existing)]
            bundleurl='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/supplementaryFiles'
            direct=[x for x in needed if x.get('direct_url')]
            for x in direct:
                content=r.fetch_bytes(x['direct_url'],paused,last,events,id)
                if content and not content.lstrip().lower().startswith((b'<html',b'<!doctype')):
                    a=store(id,'supplementary',x['filename'],content,x['direct_url'],'Official supplementary-material link in verified JATS',{'source_xml_url':xmlurl})
                    record['official_files'].append({'asset_id':a['asset_id'],'sha256':a['sha256'],'size_bytes':a['size_bytes'],'path':a['source_repo_path']})
            bundle=r.fetch_bytes(bundleurl,paused,last,events,id) if any(not x.get('direct_url') for x in needed) else None
            if bundle:
                try:
                    with zipfile.ZipFile(io.BytesIO(bundle)) as archive:
                        if sum(i.file_size for i in archive.infolist())>100*1024*1024:raise ValueError('Large bundle needs size review')
                        names={Path(n).name:n for n in archive.namelist()}
                        for x in needed:
                            if x['filename'] not in names:continue
                            content=archive.read(names[x['filename']])
                            if x['expected_size'].isdigit() and len(content)!=int(x['expected_size']):continue
                            if x['expected_md5'] and hashlib.md5(content).hexdigest()!=x['expected_md5']:continue
                            a=store(id,'supplementary',x['filename'],content,bundleurl,'Official publisher supplementary material',{'source_xml_url':xmlurl})
                            record['official_files'].append({'asset_id':a['asset_id'],'sha256':a['sha256'],'size_bytes':a['size_bytes'],'path':a['source_repo_path']})
                except (zipfile.BadZipFile,ValueError):record['bundle_error']='invalid_or_oversize_bundle'
            record['status']='downloaded' if len(existing)+len(record['official_files'])>=len(unique) else 'partial_or_access_failed'
        else:record['status']='external_data_links_only' if record['external_data_links'] else 'explicit_no_attachments_in_complete_JATS'
        report[id]=record;r.save(r.RUN/'supplementary_check.json',report);count+=1
        print(id,record['status'],len(record['official_files']),flush=True)
        if count%5==0 or time.monotonic()-checkpoint>=600:
            checkpt('Persist checked official supplementary materials and full-text evidence');checkpoint=time.monotonic()
    checkpt('Complete existing PMC supplementary review with original-format files')

def publisher_supplements():
    ready();report=r.load(r.RUN/'supplementary_check.json',{})
    out=r.ROOT/'original_files/publisher_checks_20261017';out.mkdir(parents=True,exist_ok=True)
    worker=BoundedRetriever(r.ROOT,out,'publisher_SI',workers=1)
    for h,v in r.load(r.RUN/'batch_downloads.json',{}).get('paused_hosts',{}).items():worker.blocked[h]='Earlier source failure: '+v
    count=0;checkpoint=time.monotonic()
    suffixes=r'\.(pdf|docx?|xlsx?|csv|tsv|zip|gz|txt|png|jpe?g|tiff?|gif|svg|mp4|avi|mov|mpe?g|webm|r|py|m|c|cpp|fasta|xml|pptx?)$'
    for row in rows('manual_review/scansci_download_status_utf8.csv'):
        id=row['原记录ID'];meta=r.load(r.ROOT/'papers'/id/'metadata.json',{})
        if not meta.get('included_for_download'):continue
        if report.get(id,{}).get('status') in ['downloaded','explicit_no_attachments_in_complete_JATS','external_data_links_only']:continue
        if report.get(id,{}).get('publisher_checked_this_run'):continue
        url=row.get('官方文章/仓储入口','')
        record=report.get(id,{'record_id':id,'official_files':[],'external_data_links':[]})
        record.update(publisher_checked_this_run=True,publisher_url=url,checked_at_utc=r.now())
        mapped=paused_doi_host(meta.get('doi',''),worker.blocked)
        paused_destination=mapped and urlsplit(url).hostname in ['doi.org','dx.doi.org']
        response=worker.get(id,url) if url.startswith(('http://','https://')) and not paused_destination else None
        if response:
            data,actual,mime=response
            if data.lstrip().startswith(b'%PDF'):
                record.update(status='not_checked',reason='Provided entry is a PDF, not an article/attachment page')
            else:
                html=data.decode('utf-8','replace');parser=Links(actual);parser.feed(html)
                title=parser.metadata.get('citation_title') or parser.metadata.get('dc.title') or parser.metadata.get('og:title') or parser.page_title
                identity=normalized(row['完整题名']) in normalized(title)
                record['publisher_title_identity_match']=identity
                if identity:
                    # Retain the checked article page as source evidence.
                    safe_html=re.sub(r';(?:jsessionid|phpsessid)=[^/?#;\s"\'<>]*','',html,flags=re.I).encode('utf-8')
                    store(id,'evidence_html','publisher_article_page_20261017.html',safe_html,actual,'Article HTML with anonymous server session identifiers removed')
                    soup=BeautifulSoup(html,'html.parser');links=[];landings=[]
                    for anchor in soup.find_all('a',href=True):
                        href=urljoin(actual,anchor['href']);label=(anchor.get_text(' ',strip=True)+' '+anchor.get('title','')+' '+href).lower()
                        parent=anchor.find_parent(['section','div'],class_=re.compile('supplement|support|additional',re.I))
                        if not (parent or re.search(r'supplement|supporting information|additional file|suppl_file|mmc\d|moesm|_s00\d',label)):continue
                        if re.search(suffixes,urlsplit(href).path,re.I) or '/bin/' in urlsplit(href).path:
                            if href not in links:links.append(href)
                        elif urlsplit(href).hostname==urlsplit(actual).hostname and urlsplit(href).path!=urlsplit(actual).path:
                            if href not in landings:landings.append(href)
                        elif urlsplit(href).hostname not in [urlsplit(actual).hostname,'doi.org']:
                            record.setdefault('external_data_links',[]).append({'url':href,'size_bytes':None,'size_status':'not supplied; linked external data, no bulk download','downloaded':False})
                    for landing in landings[:3]:
                        sub=worker.get(id,landing)
                        if not sub or sub[0].lstrip().startswith(b'%PDF'):continue
                        page=BeautifulSoup(sub[0],'html.parser')
                        for anchor in page.find_all('a',href=True):
                            href=urljoin(sub[1],anchor['href'])
                            label=(href+' '+anchor.get_text(' ',strip=True)).lower()
                            if re.search(r'author.?guideline|catalog|brochure|price.?list',label):continue
                            if not re.search(r'supplement|support|additional|attachment|moesm|mmc\d|_s00\d|data.sheet|table[_ -]?\d|video|movie|appendi|source.code',label):continue
                            if re.search(suffixes,urlsplit(href).path,re.I) and href not in links:links.append(href)
                    record['publisher_supplement_landing_pages']=landings[:3]
                    record['publisher_declared_file_links']=links
                    current=[a for a in r.load(r.ASSETS,[]) if a['record_id']==id and a['role']=='supplementary' and r.present(a)]
                    failed=[]
                    for link in links:
                        if any(a.get('source_url')==link for a in current):continue
                        result=worker.get(id,link)
                        if not result:failed.append(link);continue
                        content,actualfile,contenttype=result
                        if content.lstrip().lower().startswith((b'<html',b'<!doctype')) or 'text/html' in contenttype:failed.append(link);continue
                        name=Path(urlsplit(actualfile).path).name or ('attachment_'+r.sha(content)[:12])
                        if not Path(name).suffix:name+=(mimetypes.guess_extension(contenttype.split(';')[0].strip()) or '.bin')
                        a=store(id,'supplementary',name,content,actualfile,'Official supplementary link from identity-matched article',{'source_xml_url':actual})
                        record.setdefault('official_files',[]).append({'asset_id':a['asset_id'],'sha256':a['sha256'],'size_bytes':a['size_bytes'],'path':a['source_repo_path']})
                    record['publisher_failed_file_links']=failed
                    if links:record['status']='partial_or_access_failed' if failed else 'downloaded'
                    elif re.search(r'(no supplementary (?:material|information)|no supporting information|supplementary (?:material|information)\s*[:：]\s*(?:none|not applicable))',soup.get_text(' ',strip=True),re.I):record['status']='explicit_no_attachments_on_article_page'
                    else:record['status']='checked_no_file_links_found_coverage_unconfirmed'
                else:record.update(status='access_failed' if re.search('just a moment|access denied|verify you are human',html[:15000],re.I) else 'identity_review_required',reason='Page did not expose verified target article metadata')
        else:record.update(status='access_failed',reason=worker.blocked.get(mapped if paused_destination else urlsplit(url).hostname,'Entry unavailable or source cooldown'),source_request_skipped_due_to_known_publisher_pause=bool(paused_destination))
        report[id]=record;r.save(r.RUN/'supplementary_check.json',report);count+=1
        print(id,record['status'],len(record.get('official_files',[])),flush=True)
        if count%5==0 or time.monotonic()-checkpoint>=600:
            checkpt('Persist publisher supplementary checks and acquired original attachments');checkpoint=time.monotonic()
    checkpt('Complete supplementary source pass for existing included records')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['known','supplementary','publisher-supplements']);args=parser.parse_args()
    {'known':known,'supplementary':supplementary,'publisher-supplements':publisher_supplements}[args.action]()
