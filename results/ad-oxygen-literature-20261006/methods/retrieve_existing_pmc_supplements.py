"""Fetch supplements only for already catalogued, included PMCID records."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.parse import unquote, urlsplit
from email.utils import parsedate_to_datetime
import csv, hashlib, io, json, os, re, time, unicodedata, zipfile
import xml.etree.ElementTree as ET
import fitz

ROOT=Path('/workspace/FirstCodex/results/ad-oxygen-literature-20261006')
OUT=Path('/workspace/library-files/ad-oxygen-supplements')
REPORT=Path('/workspace/pmc_supplementary_current_pass.json')
XLINK='{http://www.w3.org/1999/xlink}href'
BASE='https://www.ebi.ac.uk/europepmc/webservices/rest/'
CONTACT=os.environ.get('SCANSCI_CONTACT_EMAIL','').strip()
last_request=0.0
blocked=None

def sha(data): return hashlib.sha256(data).hexdigest()
def norm(text):
    text=unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode().lower()
    return re.sub('[^a-z0-9]','',text)
def tag(e): return e.tag.rsplit('}',1)[-1] if isinstance(e.tag,str) else ''
def text(e): return ''.join(e.itertext()).strip() if e is not None else ''
def save(report):
    report['last_update_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    tmp=REPORT.with_suffix('.tmp');tmp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');tmp.replace(REPORT)
def request(url,record):
    global last_request,blocked
    if blocked: return None,{'url':url,'status':'skipped_host_paused','reason':blocked}
    assert url.startswith(BASE)
    time.sleep(max(0,3.2-(time.monotonic()-last_request)))
    event={'url':url,'requested_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    try:
        agent='FirstCodex-existing-PMC-supplement-recovery/1.0'+(' (mailto:'+CONTACT+')' if CONTACT else '')
        with urlopen(Request(url,headers={'User-Agent':agent}),timeout=35) as response:
            data=response.read(60*1024*1024+1)
            event.update(http_status=response.status,content_type=response.headers.get('Content-Type'),bytes=len(data),sha256=sha(data))
            if len(data)>60*1024*1024:raise ValueError('response exceeds 60 MiB review limit')
            if response.url!=url:event['final_url']=response.url
            return data,event
    except HTTPError as exc:
        event.update(http_status=exc.code,response_excerpt=exc.read(250).decode('utf-8','replace'))
        if exc.code==429:
            value=exc.headers.get('Retry-After','');delay=300
            try:delay=float(value)
            except ValueError:
                try:delay=parsedate_to_datetime(value).timestamp()-time.time()
                except Exception:pass
            event['retry_after_seconds']=max(60,delay);blocked='HTTP429; resume only after Retry-After cooldown; no immediate retry'
        if exc.code in (401,403):blocked='HTTP'+str(exc.code)+'; source paused, no challenge retry'
    except Exception as exc:
        event['error_type']=type(exc).__name__
        if 'Tunnel connection failed: 403' in str(exc):
            event['error']='CONNECT403';blocked='CONNECT403; source paused'
        else:event['error']=type(exc).__name__
    finally:last_request=time.monotonic()
    return None,event

def identity(root,row):
    meta=root.find('./front/article-meta')
    if meta is None: return {'verified':False,'failure':'article-meta missing'}
    title=text(meta.find('./title-group/article-title'))
    identifiers={e.attrib.get('pub-id-type'):text(e) for e in meta.findall('article-id')}
    doi=identifiers.get('doi','');pmc=identifiers.get('pmc') or identifiers.get('pmcid')
    # JATS defaults omitted contrib-type to author; ElementTree does not load DTD defaults.
    contributors=[e for e in meta.findall('./contrib-group/contrib') if e.attrib.get('contrib-type','author').lower()=='author']
    surnames=[text(e.find('.//name/surname')) or text(e.find('.//string-name/surname')) for e in contributors]
    surname_norms=[norm(s) for s in surnames if s]
    expected_surnames=[a.split(',')[0] if ',' in a else a.split()[-1] for a in row.get('authors',[]) if a.strip()]
    matched=[a for a in expected_surnames if norm(a) in surname_norms]
    first=bool(expected_surnames and norm(expected_surnames[0]) in surname_norms)
    title_match=norm(title)==norm(row['title'])
    doi_match=norm(doi)==norm(row['doi'])
    pmc_match=not pmc or pmc.replace('PMC','')==row['pmc'].replace('PMC','')
    author_match=bool(expected_surnames and len(matched)>=len(expected_surnames)*0.8 and first)
    return {'verified':bool(title_match and doi_match and pmc_match and author_match),'xml_title':title,'xml_doi':doi,'xml_pmc':pmc,'xml_author_surnames':surnames,'expected_author_surnames':expected_surnames,'matched_author_surnames':matched,'title_match':title_match,'doi_match':doi_match,'pmc_match':pmc_match,'authors_match':author_match,'first_author_match':first}

def licence(root):
    permissions=root.find('./front/article-meta/permissions')
    if permissions is None:return {'status':'not stated in XML','redistribution_permission_verified':False}
    serialized=ET.tostring(permissions,encoding='unicode');statement=text(permissions)
    urls=list(dict.fromkeys(re.findall(r'https?://creativecommons\.org/(?:licenses|publicdomain)/[^\s<"\)]+',serialized)))
    # Only explicit author/article permissions count, not a cited reference's licence.
    allowed=any(re.search(r'/licenses/(?:by|by-sa)/[0-9.]*/?$',u) or '/publicdomain/' in u for u in urls)
    return {'status':'explicit XML article permissions','statement':statement,'license_urls':urls,'redistribution_permission_verified':allowed,'publish_original_to_git':allowed,'note':'Restricted or unknown licence requires separate review; a public endpoint alone is not permission.'}

def declared_assets(root):
    found=[]; external=[]
    for element in root.iter():
        if tag(element) not in ('supplementary-material','inline-supplementary-material'):continue
        candidates=[element]+[e for e in element.iter() if e is not element and tag(e) in ('media','ext-link','graphic')]
        for asset in candidates:
            href=asset.attrib.get(XLINK) or asset.attrib.get('href')
            if not href:continue
            serialized=ET.tostring(asset,encoding='unicode')
            pis={k:v.strip() for k,v in re.findall(r'<\?suppdata-(name|size|md5)\s+([^?]+)\?>',serialized)}
            filename=pis.get('name') or Path(unquote(urlsplit(href).path)).name
            is_file=bool(re.search(r'\.[A-Za-z0-9]{1,7}$',filename))
            entry={'xml_id':element.attrib.get('id'),'declared_href':href,'filename':filename,'caption':text(element.find('./caption')) or text(asset.find('./caption')),'expected_size_bytes':int(pis['size']) if pis.get('size','').isdigit() else None,'expected_md5':pis.get('md5')}
            if (not urlsplit(href).scheme and is_file) or pis.get('name'):found.append(entry)
            else:external.append(entry)
    unique={e['filename']:e for e in found}
    return list(unique.values()),external

def inspect_bytes(data,name):
    suffix=Path(name).suffix.lower();r={'format':suffix or 'no suffix','size_bytes':len(data),'sha256':sha(data)}
    try:
        if suffix=='.pdf':
            doc=fitz.open(stream=data,filetype='pdf');r.update(format='PDF',pages=len(doc),all_pages_parse=all(p.get_text() is not None for p in doc),format_valid=True)
        elif suffix in ('.zip','.xlsx','.docx','.pptx') or data.startswith(b'PK'):
            z=zipfile.ZipFile(io.BytesIO(data));bad=z.testzip();r.update(zip_crc_error=bad,format_valid=bad is None,archive_members=[i.filename for i in z.infolist()])
            if suffix=='.xlsx':
                wb=ET.fromstring(z.read('xl/workbook.xml'));ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};r['worksheets']=[e.attrib.get('name') for e in wb.findall('./s:sheets/s:sheet',ns)];r['format']='XLSX'
            elif suffix=='.docx':r.update(format='DOCX',document_xml_present='word/document.xml' in z.namelist())
            elif suffix=='.pptx':r.update(format='PPTX',presentation_xml_present='ppt/presentation.xml' in z.namelist())
            else:r['format']='ZIP'
        elif suffix in ('.csv','.tsv','.txt','.r','.py','.fasta','.xml'):
            decoded=data.decode('utf-8-sig');r.update(format_valid=True,text_decoding='UTF-8',text_characters=len(decoded))
            if suffix in ('.csv','.tsv'):
                rr=list(csv.reader(io.StringIO(decoded),delimiter='\t' if suffix=='.tsv' else ','));r.update(rows=len(rr),first_row_columns=len(rr[0]) if rr else 0)
        elif suffix in ('.doc','.xls'):
            r.update(format_valid=data.startswith(bytes.fromhex('d0cf11e0a1b11ae1')),validation='OLE compound-file signature only; full application-level parsing unavailable')
        else:r.update(format_valid=None,validation='Original byte integrity checked; format-specific parser not applied')
    except Exception as exc:r.update(format_valid=False,format_error=type(exc).__name__)
    return r

def store_file(directory,name,data):
    safe=Path(unquote(name)).name
    safe=re.sub(r'[^\w. ()-]','_',safe)[:180] or 'attachment.bin'
    directory.mkdir(parents=True,exist_ok=True);dest=directory/safe
    if dest.exists() and sha(dest.read_bytes())!=sha(data):dest=directory/(dest.stem+'_'+sha(data)[:12]+dest.suffix)
    if not dest.exists():dest.write_bytes(data)
    return dest

def extract_derivatives(data,name,directory,depth=0):
    if depth>2 or not data.startswith(b'PK') or Path(name).suffix.lower() in ('.xlsx','.docx','.pptx'):return []
    output=[];z=zipfile.ZipFile(io.BytesIO(data))
    if z.testzip():return []
    if sum(i.file_size for i in z.infolist())>250*1024*1024:return [{'status':'unpacked size exceeds 250 MiB review limit'}]
    for item in z.infolist():
        if item.is_dir():continue
        parts=Path(item.filename)
        if parts.is_absolute() or '..' in parts.parts:output.append({'name':item.filename,'status':'unsafe archive path not extracted'});continue
        content=z.read(item);dest=store_file(directory,parts.name,content);entry=inspect_bytes(content,parts.name);entry.update(name=item.filename,path=str(dest),role='extracted_derivative_for_inspection',count_as_additional_official_attachment=False)
        output.append(entry);output+=extract_derivatives(content,parts.name,directory/(parts.stem+'_contents'),depth+1)
    return output

def run():
    rows=json.loads((ROOT/'methods/audit/final_record_metadata.json').read_text())
    queue=[r for r in rows if str(r.get('final_category_code')) in ('1','2','3','4') and re.fullmatch('PMC[0-9]+',r.get('pmc',''))]
    report={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'canonical_source':str(ROOT/'methods/audit/final_record_metadata.json'),'queue_count':len(queue),'excluded_category_5_records_not_requested':sum(str(r.get('final_category_code'))=='5' for r in rows),'scope':'Existing included PMCID records only; no searches or classification changes. Original declared assets count once; transport bundle/derived contents do not increase official attachment count.','queue':[{'id':r['id'],'pmc':r['pmc'],'doi':r['doi'],'category':r['final_category_code']} for r in queue],'records':{},'events':[]}
    if REPORT.exists():
        prior=json.loads(REPORT.read_text())
        if prior.get('queue')==report['queue']:
            report=prior;report.setdefault('resume_notes',[]).append('Resume after correcting JATS default author parsing; preserve completed records and all access evidence.')
    save(report)
    for row in queue:
        rid=row['id'];directory=OUT/rid;previous=report['records'].get(rid,{})
        if previous.get('status') and previous['status'] not in ('started','identity_pending_manual_review_no_bundle_requested'):
            continue
        record={'id':rid,'pmc':row['pmc'],'doi':row['doi'],'expected_title':row['title'],'category':row['final_category_code'],'official_attachments':[],'official_attachment_count':0,'status':'started','scope_changed':False}
        if previous:record['previous_check']={'status':previous.get('status'),'identity':previous.get('identity')}
        report['records'][rid]=record
        cached=Path('/workspace/R09236_xml.txt') if rid=='R09236' else None
        previous_xml=Path(previous.get('xml_path','/nonexistent'))
        if previous_xml.is_file():xml=previous_xml.read_bytes();record['xml_reused_from_previous_attempt']=str(previous_xml)
        elif cached and cached.exists():xml=cached.read_bytes();record['xml_reused_from_prior_validated_pilot']=str(cached)
        else:
            xml,event=request(BASE+row['pmc']+'/fullTextXML',record);report['events'].append({'id':rid,**event})
        if xml is None:record['status']='XML_unavailable';save(report);print(json.dumps({'id':rid,'status':record['status']}),flush=True);continue
        try:root=ET.fromstring(xml,parser=ET.XMLParser(target=ET.TreeBuilder(insert_pis=True)))
        except Exception as exc:record.update(status='XML_parse_failed',error_type=type(exc).__name__);save(report);continue
        record['identity']=identity(root,row);record['xml_sha256']=sha(xml)
        directory.mkdir(parents=True,exist_ok=True);xmlpath=store_file(directory/'evidence',row['pmc']+'_fullText.xml',xml);record['xml_path']=str(xmlpath)
        if not record['identity']['verified']:record['status']='identity_pending_manual_review_no_bundle_requested';save(report);print(json.dumps({'id':rid,'status':record['status'],'identity':record['identity']}),flush=True);continue
        record['license']=licence(root);declared,external=declared_assets(root);record['declared_local_attachments']=declared;record['external_supplement_links']=external;record['official_attachment_count']=len(declared)
        if not declared:
            record['status']='XML_checked_no_local_supplementary_assets_declared' if not external else 'XML_checked_external_supplement_links_only';save(report);print(json.dumps({'id':rid,'status':record['status'],'declared':0}),flush=True);continue
        # Existing pilot asset is byte-checked and reused; no repeated request.
        if rid=='R09236':
            asset=directory/'microorganisms-11-02349-s001.zip'
            if asset.exists() and sha(asset.read_bytes())=='17102352b095b0fc97e7455ed7edc91ce96d20181b5c1194d69fc2336d7ad5fa':
                data=asset.read_bytes();detail=inspect_bytes(data,asset.name);detail.update(path=str(asset),role='official_original_supplementary_attachment',declared=declared[0],reused_from_prior_pilot=True,expected_size_matches=len(data)==declared[0]['expected_size_bytes'],expected_md5_matches=hashlib.md5(data).hexdigest()==declared[0]['expected_md5']);detail['derivatives']=extract_derivatives(data,asset.name,directory/'extracted');record['official_attachments'].append(detail);record['status']='all_declared_local_attachments_verified_reused';save(report);print(json.dumps({'id':rid,'status':record['status'],'declared':1}),flush=True);continue
        bundle,event=request(BASE+row['pmc']+'/supplementaryFiles',record);report['events'].append({'id':rid,**event})
        if bundle is None:record['status']='supplement_bundle_unavailable';save(report);print(json.dumps({'id':rid,'status':record['status']}),flush=True);continue
        try:
            archive=zipfile.ZipFile(io.BytesIO(bundle));bad=archive.testzip()
            if bad:raise ValueError('transport ZIP CRC failed')
            if sum(i.file_size for i in archive.infolist())>250*1024*1024:raise ValueError('transport ZIP expanded contents exceed 250 MiB review limit')
            bundle_path=store_file(directory/'transport',row['pmc']+'_supplementaryFiles.zip',bundle);record['transport_bundle']={'path':str(bundle_path),'bytes':len(bundle),'sha256':sha(bundle),'zip_crc_error':bad,'role':'repository_generated_transport_bundle','count_as_official_attachment':False,'member_count':len(archive.infolist())}
            names=archive.namelist();bybase={Path(n).name:n for n in names}
            for entry in declared:
                member=entry['filename'] if entry['filename'] in names else bybase.get(entry['filename'])
                if not member:record['official_attachments'].append({'declared':entry,'status':'declared_attachment_missing_from_transport_bundle'});continue
                data=archive.read(member);size_ok=entry['expected_size_bytes'] is None or len(data)==entry['expected_size_bytes'];md5_ok=entry['expected_md5'] is None or hashlib.md5(data).hexdigest()==entry['expected_md5']
                sub='official' if size_ok and md5_ok else 'quarantine';path=store_file(directory/sub,entry['filename'],data);detail=inspect_bytes(data,entry['filename']);detail.update(path=str(path),declared=entry,role='official_original_supplementary_attachment',actual_md5=hashlib.md5(data).hexdigest(),expected_size_matches=size_ok,expected_md5_matches=md5_ok,status='byte_integrity_verified' if size_ok and md5_ok and detail.get('format_valid') is not False else 'integrity_or_format_check_failed')
                if size_ok and md5_ok:detail['derivatives']=extract_derivatives(data,entry['filename'],directory/'extracted'/Path(entry['filename']).stem)
                record['official_attachments'].append(detail)
            good=[a for a in record['official_attachments'] if a.get('status')=='byte_integrity_verified'];record['verified_official_attachment_count']=len(good);record['status']='all_declared_local_attachments_verified' if len(good)==len(declared) else 'some_declared_attachments_pending_verification'
        except Exception as exc:record.update(status='bundle_integrity_or_parse_failed',error_type=type(exc).__name__)
        save(report);print(json.dumps({'id':rid,'status':record['status'],'declared':len(declared),'verified':record.get('verified_official_attachment_count',0)}),flush=True)
    report['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());report['paused_host_reason']=blocked
    report['summary']={'records':len(report['records']),'identity_verified':sum(bool(r.get('identity',{}).get('verified')) for r in report['records'].values()),'official_attachments_declared':sum(r.get('official_attachment_count',0) for r in report['records'].values()),'official_attachments_integrity_verified':sum(sum(1 for a in r['official_attachments'] if a.get('status')=='byte_integrity_verified' or a.get('reused_from_prior_pilot')) for r in report['records'].values())};save(report);print(json.dumps({'summary':report['summary']}),flush=True)

if __name__=='__main__':run()
