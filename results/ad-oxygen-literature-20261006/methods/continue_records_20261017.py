"""Continue only existing included records and their explicitly declared SI.

No keyword searches or classification. Preserve every acquired candidate; an
automated metadata heuristic cannot register a new PDF as verified. Originals
are backed up every five processed records or ten minutes, whichever is first.
"""
import argparse, collections, csv, hashlib, io, json, re, time, unicodedata, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit, urljoin
import recovery_20261017 as r
from continue_known_fulltexts import Retriever, Links, normalized

def rows(name):return r.readcsv(r.ROOT/name)
def ready():
    gate=r.load(r.RUN/'pilot_gate.json',{})
    assert gate.get('all_original_bytes_readback_verified') and gate.get('body_samples',0)>=3,'Independent three-body readback is required'
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
        storage_status='local_acquired_pending_remote_readback',source_url=url,version=version,
        license_evidence=a.get('license_evidence','Private authorized research backup; source license not inferred'))
    if extra:a.update(extra)
    if not old:assets.append(a)
    r.save(r.ASSETS,assets);return a

def checkpt(message):
    r.audit();r.parse_files();r.sync(message)

def known():
    ready();out=r.ROOT/'original_files/continuation_20261017';out.mkdir(parents=True,exist_ok=True)
    worker=Retriever(r.ROOT,out,'existing_included',workers=1)
    prior_pause=r.load(r.RUN/'batch_downloads.json',{}).get('paused_hosts',{})
    worker.blocked.update({h:'Paused after earlier source failure in this recovery pass: '+v for h,v in prior_pause.items()})
    previous=r.load(r.ROOT/'methods/audit/scansci_sourcewise_results.json',{})
    current={x['原记录ID']:x for x in rows('manual_review/scansci_download_status_utf8.csv')}
    hist={x['原记录ID']:x for x in rows('methods/audit/scansci_verified_pdf_manifest_utf8.csv')}
    tasks=[]
    for row in rows('manual_review/current_environment_need_fulltext_utf8.csv'):
        id=row['原记录ID'];old=current[id];p=previous.get(id,{});urls=[]
        if old.get('实际PDF来源URL（下载或历史记录明确）'):urls.append(old['实际PDF来源URL（下载或历史记录明确）'])
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
        result=worker.process(task);id=task['id'];body=result.get('body',{})
        if body.get('verified'):
            path=Path(body['path']);store(id,'main',path.name,path.read_bytes(),body['source_url'],body.get('version',''))
            # Source canonicalization must not keep duplicate original bytes.
            path.unlink()
        count+=1
        if count%5==0 or time.monotonic()-checkpoint>=600:
            checkpt('Continue existing literature records and persist all acquired candidates');checkpoint=time.monotonic()
    checkpt('Complete known-source continuation pass')
    r.save(r.RUN/'continuation_summary.json',{'records_processed':count,'paused_hosts':worker.blocked,'cooldown_hosts':list(worker.cooldown),'new_searches':False})

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
            record.update(status='access_failed',reason=paused.get('www.ebi.ac.uk','request_failed'));report[id]=record;r.save(r.RUN/'supplementary_check.json',report);continue
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
                elif urlsplit(href).scheme in ['http','https']:record['external_data_links'].append({'url':href,'size_bytes':None,'size_status':'not supplied; no bulk database download','downloaded':False})
        unique={x['filename']:x for x in declarations};record['declared_attachments']=list(unique.values())
        if unique:
            existing=[a for a in r.load(r.ASSETS,[]) if a['record_id']==id and a['role']=='supplementary' and r.present(a)]
            needed=[x for name,x in unique.items() if not any(a['original_filename']==name and (not x['expected_size'].isdigit() or int(x['expected_size'])==int(a['size_bytes'])) for a in existing)]
            bundleurl='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/supplementaryFiles'
            bundle=r.fetch_bytes(bundleurl,paused,last,events,id) if needed else None
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

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['known','supplementary']);args=parser.parse_args()
    known() if args.action=='known' else supplementary()
