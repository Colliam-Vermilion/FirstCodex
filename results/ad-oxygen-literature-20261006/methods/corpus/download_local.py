"""Cross-platform, known-source downloads and explicit local identity/attachment review.

No theme searches, credential handling or login bypass. Files first enter intake;
only explicit identity/version or attachment-association review can accept new bytes.
Run --help for commands. All state and originals stay outside the cloned repository.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from urllib.parse import urlsplit,urljoin,unquote
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from collections import defaultdict
import argparse,csv,json,hashlib,io,os,re,shutil,time,zipfile
from audit_library import dump,sha,read_csv,write_csv,safe_name
BODY_VERSIONS=['publisher_version','accepted_manuscript','preprint','author_manuscript_unconfirmed','thesis','other_complete_body']
SI_STATES=['not_checked','downloaded_partial','explicit_none','access_failed','external_data_link']
EXTERNAL=re.compile(r'(?:^|\.)(?:ncbi\.nlm\.nih\.gov|ebi\.ac\.uk|sra\.ebi\.ac\.uk|zenodo\.org|figshare\.com|figshare\.s3[^.]*\.amazonaws\.com|datadryad\.org|osf\.io|github\.com|gitlab\.com)$',re.I)
TYPES=re.compile(r'\.(?:pdf|docx?|xlsx?|xlsm|csv|tsv|txt|zip|7z|rar|tar|gz|bz2|png|jpe?g|tiff?|bmp|gif|svg|mp4|mov|avi|mkv|wmv|webm|r|py|m|ipynb|fasta|fastq|fa|fq|skp)(?:$|[?#])',re.I)


def validate_file(path,role):
    path=Path(path);head=path.read_bytes()[:8192];low=head.lstrip().lower()
    if low.startswith((b'<!doctype html',b'<html')) or b'<title>just a moment' in low or b'<title>sign in' in low:raise ValueError('HTML/login/challenge is not an attachment')
    ext=path.suffix.lower();fmt=ext.lstrip('.')
    if role=='evidence_xml':
        import xml.etree.ElementTree as ET
        tree=ET.parse(path).getroot()
        if tree.tag!='article' or tree.find('body') is None:raise ValueError('Expected a complete JATS article source, not an XML error document')
        return {'format':'xml','validation':'JATS article/body present; metadata identity requires explicit review'}
    if role=='transport_archive' and not zipfile.is_zipfile(path):raise ValueError('Expected a repository transport ZIP')
    if role=='main' or ext=='.pdf' or head.startswith(b'%PDF'):
        if not head.lstrip().startswith(b'%PDF'):raise ValueError('Main must be an actual PDF, not HTML/error text')
        import fitz
        doc=fitz.open(path)
        if not len(doc) or doc.needs_pass:raise ValueError('Empty/encrypted PDF')
        for page in doc:page.get_text()
        return {'format':'pdf','pages':len(doc),'pdf_repaired':bool(doc.is_repaired),'validation':'all PDF pages parse; identity/version require explicit review'}
    if ext in ['.docx','.xlsx','.xlsm','.pptx','.zip']:
        with zipfile.ZipFile(path) as z:
            if sum(m.file_size for m in z.infolist())>500*1024*1024:raise ValueError('Archive expansion exceeds 500 MiB review limit')
            if z.testzip() is not None:raise ValueError('Archive CRC mismatch')
            required={'.docx':'word/document.xml','.xlsx':'xl/workbook.xml','.xlsm':'xl/workbook.xml','.pptx':'ppt/presentation.xml'}.get(ext)
            if required and required not in z.namelist():raise ValueError('Wrong OOXML structure')
        return {'format':fmt,'validation':'ZIP/OOXML CRC and expected document member verified'}
    if ext in ['.doc','.xls'] and not head.startswith(bytes.fromhex('d0cf11e0a1b11ae1')):raise ValueError('Wrong legacy Office OLE signature')
    if ext in ['.csv','.tsv','.txt','.json','.xml','.py','.r','.md']:
        raw=path.read_bytes()
        try:raw.decode('utf-8-sig');encoding='utf-8-sig'
        except UnicodeDecodeError:raw.decode('gb18030');encoding='gb18030'
        return {'format':fmt,'encoding':encoding,'validation':'text decoded; table/contents pending parser/review'}
    if ext in ['.png','.jpg','.jpeg','.gif','.tif','.tiff','.bmp']:
        from PIL import Image
        with Image.open(path) as im:im.verify()
        return {'format':fmt,'validation':'image decoded; image content not indexed'}
    return {'format':fmt or 'unknown','validation':'byte integrity only; format-specific parser unavailable','content_indexed':False}


def permitted_record(project,id):
    meta=json.loads((project/'papers'/id/'metadata.json').read_text())
    if not meta['included_for_download']:raise ValueError('Excluded record: '+id)
    return meta


def append_event(root,event):
    folder=root/'intake';folder.mkdir(parents=True,exist_ok=True)
    with (folder/'events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')


def register(args):
    project=args.project.resolve();root=args.root.resolve();meta=permitted_record(project,args.id)
    if not args.reviewed or not args.evidence:raise ValueError('Explicit --reviewed and --evidence required; download alone is not verification')
    if args.role=='main' and args.version not in BODY_VERSIONS:raise ValueError('Explicit complete-body version required')
    if args.role!='main' and not args.association_reviewed:raise ValueError('Confirm this is the target paper’s attachment with --association-reviewed')
    source=args.file.resolve();check=validate_file(source,args.role);digest=sha(source);filename=source.name
    # A stable digest suffix prevents two versions or same-named attachments overwriting.
    folder='main' if args.role=='main' else 'supplementary' if args.role=='supplementary' else 'evidence'
    canonical=f'papers/{args.id}/{folder}/{digest[:12]}_{safe_name(filename)}'
    dest=root/canonical;dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():
        if sha(dest)!=digest:raise ValueError('Existing object changed; refusing overwrite')
    elif source!=dest:shutil.copy2(source,dest)
    manifest=root/'intake/assets.json';assets=json.loads(manifest.read_text()) if manifest.exists() else []
    aid=args.id+'.'+args.role+'.'+digest[:16]
    a={'record_id':args.id,'asset_id':aid,'role':args.role,'official_attachment':args.role=='supplementary','original_filename':filename,'canonical_path':canonical,'source_repo_path':'','source_local_path':str(dest),'resolved_source_path':str(dest),'format':check['format'],'size_bytes':dest.stat().st_size,'sha256':digest,'availability':'present_sha_verified','storage_status':'local_only_not_backed_up','source_url':args.url or '', 'source_xml_url':'','version':args.version if args.role=='main' else 'original_supplementary_attachment' if args.role=='supplementary' else 'repository_source_representation_not_PDF','license_evidence':'not assessed for redistribution; private by default','historical_sha256':'','archive_parent_asset_id':'','parsing_status':'not_started','review':{'identity_or_association_explicitly_reviewed':True,'evidence':args.evidence,'format_checks':check}}
    same=[x for x in assets if x['asset_id']==aid]
    if not same:assets.append(a)
    if args.role=='supplementary' and source.suffix.lower()=='.zip':
        with zipfile.ZipFile(source) as z:
            if len(z.infolist())>10000:raise ValueError('Archive member count exceeds review limit')
            for item in z.infolist():
                if item.is_dir():continue
                if '..' in Path(item.filename).parts or item.filename.startswith(('/',chr(92))) or chr(92) in item.filename or re.match(r'^[A-Za-z]:',item.filename):raise ValueError('Unsafe archive member')
                if (item.external_attr>>16)&0o170000==0o120000:continue
                if item.file_size>100*1024*1024:continue
                data=z.read(item);childsha=hashlib.sha256(data).hexdigest();childname=Path(item.filename).name
                childpath=f'papers/{args.id}/supplementary/derived/{childsha[:12]}_{safe_name(childname)}';childdest=root/childpath;childdest.parent.mkdir(parents=True,exist_ok=True)
                if not childdest.exists():childdest.write_bytes(data)
                elif sha(childdest)!=childsha:raise ValueError('Archive derivative conflict')
                child=dict(a);child.update(asset_id=args.id+'.derived.'+childsha[:16],role='derived',official_attachment=False,original_filename=childname,canonical_path=childpath,source_local_path=str(childdest),resolved_source_path=str(childdest),format=childdest.suffix.lower().lstrip('.'),size_bytes=len(data),sha256=childsha,version='extracted_archive_member',archive_parent_asset_id=aid,archive_member_path=item.filename)
                child['review']={'identity_or_association_explicitly_reviewed':True,'evidence':'SHA/CRC-bound member of reviewed parent '+aid,'parent_attachment_review':args.evidence}
                if not any(x['asset_id']==child['asset_id'] for x in assets):assets.append(child)
    dump(manifest,assets);append_event(root,{'action':'register_verified','record_id':args.id,'asset_id':aid,'sha256':digest,'version':a['version'],'evidence':args.evidence})
    print(json.dumps(a,ensure_ascii=False))


def download(args):
    root=args.root.resolve();project=args.project.resolve();root.mkdir(parents=True,exist_ok=True)
    rows=read_csv(args.queue);statefile=root/'intake/download_state.json';state=json.loads(statefile.read_text()) if statefile.exists() else {};last={};paused={}
    for previous_event in state.values():
        if previous_event.get('retry_not_before_utc_epoch',0)>time.time():paused[urlsplit(previous_event.get('url','')).hostname]='Retry-After still active'
    accepted_path=root/'intake/assets.json';accepted=json.loads(accepted_path.read_text()) if accepted_path.is_file() else []
    pending_ids={e['record_id'] for e in state.values() if e.get('role')=='main' and e.get('status')=='downloaded_pending_review' and Path(e.get('path','')).is_file() and sha(e['path'])==e.get('sha256')}
    for row in rows:
        id=row['record_id'];permitted_record(project,id);url=row.get('url') or row.get('source_url')
        if not url or not url.startswith(('http://','https://')):continue
        role=row.get('role','main');key=hashlib.sha256((id+'|'+role+'|'+url).encode()).hexdigest();old=state.get(key,{})
        # Reuse actually available Git/local originals before network, not historical status.
        meta=json.loads((project/'papers'/id/'metadata.json').read_text())
        if role=='main':
            reusable=[str(root/a['canonical_path']) for a in accepted if a['record_id']==id and a['role']=='main' and (root/a['canonical_path']).is_file() and sha(root/a['canonical_path'])==a['sha256']]
            for a in meta['assets']:
                if a['role']!='main':continue
                candidates=[root/a['canonical_path']]
                if a.get('source_repo_path'):candidates.append(project/a['source_repo_path'])
                for path in candidates:
                    if path.is_file() and sha(path)==a['sha256']:reusable.append(str(path))
            if reusable:
                state[key]={'record_id':id,'role':role,'status':'reused_actual_sha_verified','paths':reusable};dump(statefile,state);continue
        if old.get('status')=='rejected_candidate':continue
        if role=='main' and id in pending_ids:continue
        if old.get('status')=='downloaded_pending_review' and Path(old.get('path','')).is_file() and sha(old['path'])==old.get('sha256'):continue
        if old.get('status') and not args.retry_failed:continue
        if row.get('external_data','').lower() in ('true','1','yes'):
            state[key]={'record_id':id,'url':url,'status':'external_data_link_not_downloaded'};dump(statefile,state);continue
        if role!='main' and row.get('association_verified','').lower() not in ('true','1','yes'):
            state[key]={'record_id':id,'url':url,'status':'pending_attachment_association_review'};dump(statefile,state);continue
        host=urlsplit(url).hostname
        if host in paused:
            state[key]={'record_id':id,'url':url,'role':role,'status':'source_paused','reason':paused[host]};dump(statefile,state);continue
        remaining=max(0,args.delay-(time.monotonic()-last.get(host,0)))
        if remaining:time.sleep(remaining)
        destdir=root/'intake'/id/role;destdir.mkdir(parents=True,exist_ok=True)
        suggested=row.get('filename') or Path(unquote(urlsplit(url).path)).name or ('main.pdf' if role=='main' else 'attachment.bin')
        suggested=safe_name(suggested)
        if role=='main' and not suggested.lower().endswith('.pdf'):suggested+='.pdf'
        partial=destdir/(key[:12]+'_'+suggested+'.part');validator=partial.with_suffix('.resume.json')
        previous=json.loads(validator.read_text()) if validator.exists() else {};headers={'User-Agent':'FirstCodex-known-source-local-acquisition/1.0'}
        start=partial.stat().st_size if partial.exists() and previous.get('validator') else 0
        if start:headers.update({'Range':f'bytes={start}-','If-Range':previous['validator']})
        event={'record_id':id,'role':role,'url':url,'status':'failed'}
        try:
            with urlopen(Request(url,headers=headers),timeout=60) as response:
                ctype=response.headers.get('Content-Type','').lower();length=int(response.headers.get('Content-Length') or 0);event.update(http_status=response.status,final_url=response.url,content_type=ctype)
                if 'text/html' in ctype:raise ValueError('HTML response is not original bytes; use official browser if authentication required')
                if length>args.max_mib*1024*1024:raise ValueError('Large attachment recorded, not auto-downloaded: '+str(length))
                append=response.status==206 and start>0
                range_info=re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)',response.headers.get('Content-Range','')) if response.status==206 else None
                if response.status==206 and (not range_info or int(range_info[1])!=start):raise ValueError('Unexpected Content-Range; refusing corrupt append')
                token=response.headers.get('ETag','')
                if token.startswith('W/'):token=''
                token=token or response.headers.get('Last-Modified','');dump(validator,{'url':url,'validator':token})
                mode='ab' if append else 'wb';received=start if append else 0
                with partial.open(mode) as f:
                    while True:
                        data=response.read(1024*1024)
                        if not data:break
                        received+=len(data)
                        if received>args.max_mib*1024*1024:raise ValueError('Transfer exceeds configured attachment limit')
                        f.write(data)
                if length and partial.stat().st_size!=(start if append else 0)+length:raise ValueError('Truncated Content-Length')
                if range_info and partial.stat().st_size!=int(range_info[3]):raise ValueError('Partial range does not complete the object; resume required')
            digest=sha(partial);final=destdir/(digest[:12]+'_'+suggested)
            if final.exists() and sha(final)!=digest:raise ValueError('Refuse overwrite')
            partial.replace(final);check=validate_file(final,role)
            expected=row.get('expected_sha256','')
            if expected and digest!=expected:check['historical_sha_mismatch']=True
            pending_ids.add(id) if role=='main' else None
            event.update(status='downloaded_pending_review',path=str(final),sha256=digest,size_bytes=final.stat().st_size,format_checks=check,identity_verified=False,version_verified=False)
        except HTTPError as exc:
            event.update(http_status=exc.code,status='access_failed')
            if exc.code in [401,403,429]:
                paused[host]=str(exc.code);event['source_paused']=True
                if exc.code==429:
                    retry=exc.headers.get('Retry-After','60')
                    try:seconds=float(retry)
                    except ValueError:
                        try:seconds=parsedate_to_datetime(retry).timestamp()-time.time()
                        except Exception:seconds=60
                    event['retry_not_before_utc_epoch']=time.time()+max(60,seconds)
        except Exception as exc:event.update(error_type=type(exc).__name__,error=str(exc)[:250])
        finally:last[host]=time.monotonic()
        state[key]=event;dump(statefile,state);append_event(root,event);print(json.dumps(event,ensure_ascii=False),flush=True)


class SupplementLinks(HTMLParser):
    def __init__(self,base):super().__init__();self.base=base;self.active=None;self.links=[];self.title=False;self.page_title=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='title':self.title=True
        if tag=='a' and d.get('href'):self.active={'url':urljoin(self.base,d['href']),'text':'','attributes':str(d)}
    def handle_data(self,data):
        if self.title:self.page_title.append(data)
        if self.active:self.active['text']+=data+' '
    def handle_endtag(self,tag):
        if tag=='title':self.title=False
        if tag=='a' and self.active:self.links.append(self.active);self.active=None


def discover(args):
    permitted_record(args.project,args.id);url=args.url;event={'record_id':args.id,'landing_url':url,'status':'not_checked','candidates':[]}
    try:
        with urlopen(Request(url,headers={'User-Agent':'FirstCodex-associated-attachment-review/1.0'}),timeout=45) as r:
            raw=r.read(8*1024*1024+1)
            if len(raw)>8*1024*1024:raise ValueError('Article page exceeds 8MiB')
            html=raw.decode('utf-8','replace');event['http_status']=r.status;event['final_url']=r.url
        if re.search(r'just a moment|checking your browser|verify you are human',html[:16000],re.I):raise ValueError('HTML challenge, page not checked')
        parser=SupplementLinks(event['final_url']);parser.feed(html);event['page_title']=' '.join(parser.page_title);seen=set()
        for link in parser.links:
            text=link['text']+' '+link['attributes']+' '+link['url']
            if not re.search(r'supplement|supporting|additional.file|suppl_file|/esm|data.availability|dataset|source.code|code.availability',text,re.I):continue
            u=link['url']
            if u in seen or not u.startswith(('http://','https://')):continue
            seen.add(u);host=urlsplit(u).hostname or ''
            external=(bool(EXTERNAL.search(host)) and not TYPES.search(u)) or bool(re.search(r'ncbi\.nlm\.nih\.gov|ebi\.ac\.uk',host,re.I))
            if re.search(r'/europepmc/.*(?:supplementaryFiles|fullTextXML)',u,re.I):external=False
            event['candidates'].append({'record_id':args.id,'role':'supplementary','url':u,'link_text':link['text'].strip(),'filename':Path(unquote(urlsplit(u).path)).name,'external_data':external,'size_bytes':None,'association_verified':False,'status':'external_data_link' if external else 'candidate_pending_association_and_format_review'})
        event['status']='page_checked_candidates_found' if event['candidates'] else 'page_checked_no_detected_links_not_explicit_none'
    except Exception as exc:event.update(status='access_failed',error_type=type(exc).__name__,error=str(exc)[:250])
    folder=args.root/'intake'/args.id;folder.mkdir(parents=True,exist_ok=True);dump(folder/'supplementary_discovery.json',event)
    if event['candidates']:write_csv(folder/'supplementary_candidates_utf8.csv',event['candidates'])
    append_event(args.root,event);print(json.dumps(event,ensure_ascii=False))


def reject(args):
    permitted_record(args.project,args.id);statefile=args.root/'intake/download_state.json';state=json.loads(statefile.read_text());found=False
    for row in state.values():
        if row.get('record_id')==args.id and row.get('path') and Path(row['path']).resolve()==args.file.resolve():row['status']='rejected_candidate';row['rejection_evidence']=args.evidence;found=True
    if not found:raise ValueError('Candidate not found in download state')
    dump(statefile,state);append_event(args.root,{'action':'reject_candidate','record_id':args.id,'path':str(args.file),'evidence':args.evidence})


def si_review(args):
    meta=permitted_record(args.project,args.id)
    if not args.evidence.strip():raise ValueError('Review evidence required')
    if args.status=='explicit_none' and meta.get('supplementary_official_count',0):raise ValueError('Existing verified official attachments contradict global explicit-none')
    if args.status=='explicit_none' and not (args.publisher_checked and args.repository_checked and args.evidence):raise ValueError('explicit_none requires both source scopes checked and concrete evidence; no detected links is not enough')
    event={'record_id':args.id,'supplementary_status':args.status,'publisher_checked':args.publisher_checked,'repository_checked':args.repository_checked,'evidence':args.evidence,'related_urls':args.url or [],'scope':'explicit user review, not automatically inferred'}
    dump(args.root/'intake'/args.id/'supplementary_review.json',event);append_event(args.root,event);print(json.dumps(event,ensure_ascii=False))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--root',type=Path,required=True);sub=ap.add_subparsers(dest='action',required=True)
    d=sub.add_parser('download');d.add_argument('--queue',type=Path,required=True);d.add_argument('--delay',type=float,default=6);d.add_argument('--max-mib',type=int,default=100);d.add_argument('--retry-failed',action='store_true')
    r=sub.add_parser('register');r.add_argument('--id',required=True);r.add_argument('--role',choices=['main','supplementary','evidence_xml','transport_archive'],required=True);r.add_argument('--file',type=Path,required=True);r.add_argument('--version',choices=BODY_VERSIONS);r.add_argument('--url');r.add_argument('--reviewed',action='store_true');r.add_argument('--association-reviewed',action='store_true');r.add_argument('--evidence',required=True)
    rej=sub.add_parser('reject');rej.add_argument('--id',required=True);rej.add_argument('--file',type=Path,required=True);rej.add_argument('--evidence',required=True)
    s=sub.add_parser('discover-si');s.add_argument('--id',required=True);s.add_argument('--url',required=True)
    st=sub.add_parser('si-status');st.add_argument('--id',required=True);st.add_argument('--status',choices=SI_STATES,required=True);st.add_argument('--publisher-checked',action='store_true');st.add_argument('--repository-checked',action='store_true');st.add_argument('--evidence',required=True);st.add_argument('--url',action='append')
    args=ap.parse_args()
    if getattr(args,'delay',6)<3:raise ValueError('Same-source delay must be at least3 seconds')
    {'download':download,'register':register,'discover-si':discover,'si-status':si_review,'reject':reject}[args.action](args)


if __name__=='__main__':main()
