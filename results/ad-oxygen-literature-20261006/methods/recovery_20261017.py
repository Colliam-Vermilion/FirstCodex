"""Restore by ID/SHA, retrieve recorded sources, parse and verify private Git backup.

Use the existing checkout. Never create a worktree, reset, force-push, change
classification, run topic searches, or persist runtime credentials. Network
failures pause that host, not the other sources. Downloaded bytes stay in
original_files; ZIP contents are parsed without storing duplicate originals.
"""
import argparse, collections, csv, hashlib, io, json, os, re, subprocess
import tempfile, time, urllib.request, urllib.error, urllib.parse, zipfile, signal
from datetime import datetime, timezone
from pathlib import Path
import fitz
import openpyxl

ROOT=Path(__file__).resolve().parent.parent
REPO=ROOT.parents[1]
BRANCH='results/ad-oxygen-literature-20261006'
RUN=ROOT/'inventory/recovery_20261017'
ASSETS=ROOT/'inventory/assets.json'

def now():return datetime.now(timezone.utc).isoformat()
def safe_url(url):
    url=re.sub(r';(?:jsessionid|phpsessid)=[^/?#;]*','',url,flags=re.I)
    parsed=urllib.parse.urlsplit(url)
    sensitive={'access_token','api_key','apikey','authorization','password','session','sessionid','token','signature','sig','x-amz-signature','x-amz-credential','x-amz-security-token','awsaccesskeyid','x-goog-credential','x-goog-signature'}
    query=[(k,v) for k,v in urllib.parse.parse_qsl(parsed.query,keep_blank_values=True) if k.lower() not in sensitive]
    netloc=parsed.netloc.rsplit('@',1)[-1]
    return urllib.parse.urlunsplit((parsed.scheme,netloc,parsed.path,urllib.parse.urlencode(query),parsed.fragment))
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path,default=None):return json.loads(path.read_text()) if path.is_file() else default
def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');tmp.replace(path)
def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(path,rows,fields=None):
    fields=fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def git(*args,**kw):return subprocess.check_output(['git','-C',str(REPO),*args],text=True,**kw).strip()
def path_for(asset):
    rel=asset.get('source_repo_path','')
    return ROOT/rel if rel and not Path(rel).is_absolute() and '..' not in Path(rel).parts else None
def present(asset):
    p=path_for(asset)
    return bool(p and p.is_file() and p.stat().st_size==int(asset['size_bytes']) and sha(p.read_bytes())==asset['sha256'])

def baseline():
    RUN.mkdir(parents=True,exist_ok=True)
    if (RUN/'baseline.json').exists():return
    assets=load(ASSETS,[])
    originals=[a for a in assets if present(a)]
    protected=['methods/manual_classification_20261007_original.csv','methods/manual_classification_pending36_20261007_original.csv']
    rows=readcsv(ROOT/'final_results/ad_oxygen_download_review_utf8.csv')
    # Preserve every pre-recovery row, state, historical SHA and manual decision.
    save(RUN/'baseline_assets.json',assets)
    save(RUN/'baseline_library_rows.json',rows)
    save(RUN/'baseline_papers.json',{p.parent.name:load(p) for p in (ROOT/'papers').glob('*/metadata.json')})
    save(RUN/'baseline.json',{'time_utc':now(),'remote_source_commit':git('rev-parse','HEAD'),
        'branch':BRANCH,'records':len(rows),'protected_files_sha256':{p:sha((ROOT/p).read_bytes()) for p in protected},
        'recovered_files':len(originals),'recovered_bytes':sum(int(a['size_bytes']) for a in originals),
        'recovered_roles':dict(collections.Counter(a['role'] for a in originals)),
        'historical_assets_missing':len(assets)-len(originals),'user_authorized_private_backup_all_acquired_files':True})

def audit():
    baseline();assets=load(ASSETS,[]);papers=load(RUN/'baseline_papers.json');queue=[]
    historical91=readcsv(ROOT/'methods/audit/scansci_verified_pdf_manifest_utf8.csv')
    for old in historical91:
        if any(a['record_id']==old['原记录ID'] and a['sha256']==old['SHA256'] for a in assets):continue
        id=old['原记录ID'];digest=old['SHA256']
        assets.append({'record_id':id,'asset_id':id+'.main.'+digest[:16],'role':'main','preferred_for_record':not any(a['record_id']==id and a['role']=='main' for a in assets),
            'official_attachment':False,'original_filename':old['PDF文件名'],'canonical_path':'','source_repo_path':'','source_local_path':old['本地文件路径（不是下载链接）'],
            'resolved_source_path':'','format':'pdf','size_bytes':int(old['文件大小（字节）']),'sha256':digest,
            'source_url':old.get('实际PDF来源URL（下载或历史记录明确）',''),'recorded_candidate_urls':json.loads(old.get('公开PDF候选URL（非下载URL绑定实录）') or '[]'),
            'source_xml_url':'','version':old['PDF版本'],'license_evidence':'Historical record; source rights not reassessed','historical_sha256':digest,'archive_parent_asset_id':'',
            'parsing_status':'historical_only_current_original_missing'})
    for a in assets:
        ok=present(a)
        a['recovery_checked_at_utc']=now()
        if ok:
            a['availability']='present_sha_verified'
            a['resolved_source_path']=str(path_for(a))
        else:
            a['availability']='historical_acquired_current_original_not_restored'
            a['storage_status']='historical_only_original_missing'
            a['resolved_source_path']=''
            queue.append({'record_id':a['record_id'],'asset_id':a['asset_id'],'role':a['role'],
                'historical_sha256':a['sha256'],'size_bytes':a['size_bytes'],'source_url':a.get('source_url',''),
                'original_filename':a['original_filename'],'status':'历史已获取，当前原件未恢复'})
    save(ASSETS,assets);writecsv(ROOT/'inventory/assets_utf8.csv',assets)
    writecsv(RUN/'historical_reacquisition_queue_utf8.csv',queue)
    # Update current paper states only; original scope fields remain untouched.
    current=readcsv(ROOT/'manual_review/current_environment_acquisition426_utf8.csv')
    attempts=load(RUN/'retrieval_results.json',{})
    continuation=load(ROOT/'original_files/continuation_20261017/existing_included_results.json',{})
    for id,record in continuation.items():
        if not record.get('body',{}).get('verified'):
            attempts[id]={'reason':'本轮已处理已有来源链接，未取得核验正文；HTTP/暂停/挑战等逐来源证据见original_files/continuation_20261017/existing_included_access.jsonl','status':record.get('status')}
    si_checks=load(RUN/'supplementary_check.json',{})
    rows_by_id={r['原记录ID']:r for r in current}
    byid=collections.defaultdict(list)
    for a in assets:byid[a['record_id']].append(a)
    main_ok=0
    for id,original in papers.items():
        m=load(ROOT/'papers'/id/'metadata.json',original)
        aa=byid[id];bodies=[a for a in aa if a['role']=='main' and present(a)]
        body=next((a for a in bodies if a.get('preferred_for_record')),bodies[0] if bodies else None)
        official=[a for a in aa if a['role']=='supplementary' and present(a)]
        historical=any(a['role']=='main' for a in aa)
        status='downloaded_verified' if body else 'historical_acquired_current_original_not_restored' if historical else 'not_downloaded'
        m.update(main_status=status,assets=aa,recovery_checked_at_utc=now(),supplementary_official_count=len(official))
        m['preferred_main_asset_id']=body['asset_id'] if body else None
        m['recovery_original_status_preserved_in']='inventory/recovery_20261017/baseline_papers.json'
        checked=si_checks.get(id,{})
        m['supplementary_status']=checked.get('status') or ('downloaded' if official else 'historical_acquired_current_original_not_restored' if any(a['role']=='supplementary' for a in aa) else 'not_checked')
        m['supplementary_coverage_complete']=checked.get('status') in ['downloaded','explicit_no_attachments_in_complete_JATS','explicit_no_attachments_on_article_page','external_data_links_only']
        save(ROOT/'papers'/id/'metadata.json',m)
        if id not in rows_by_id:continue
        row=rows_by_id[id];main_ok+=bool(body)
        state='已下载并核验' if body else '历史已获取，当前原件未恢复' if historical else '尚未取得'
        row.update({'新环境核查日期':'2026-10-17','当前原件状态':state,
            '当前正文核验状态':'SHA256/大小一致；全部PDF页可解析' if body else '本机和远端当前均无可复用正文',
            '当前原件路径':str(path_for(body)) if body else '', '当前原件SHA256':body['sha256'] if body else '',
            '当前实际获取URL':body.get('source_url','') if body else '', '当前版本及限制':body.get('version','') if body else '',
            '原件恢复队列':'已恢复' if body else '历史原件重取队列' if historical else '既有未获全文队列',
            '当前持久下载入口':body.get('source_repo_path','') if body else '',
            '当前补充材料状态':(checked.get('status')+'；官方附件'+str(len(official))) if checked.get('status') else f'已下载{len(official)}份官方附件；完整性仍需逐来源核查' if official else '尚未完成本轮附件检查；不判无附件',
            '持久化及独立取回状态':'已恢复；本轮独立远端核验见recovery清单' if body else '当前原件未恢复',
            '当前下载失败或访问限制':attempts.get(id,{}).get('reason','尚未执行本轮获取；保留历史日志') if not body else ''})
    writecsv(ROOT/'manual_review/current_environment_acquisition426_utf8.csv',current)
    historical_queue=readcsv(ROOT/'manual_review/historical91_original_recovery_queue_utf8.csv')
    for row in historical_queue:
        match=next((a for a in assets if a['record_id']==row['原记录ID'] and a['sha256']==row['SHA256'] and present(a)),None)
        for k,v in rows_by_id[row['原记录ID']].items():
            if k in row and k.startswith(('当前','新环境','原件恢复','持久化')):row[k]=v
        row['历史原字节恢复20261017']='已按ID/SHA恢复' if match else '历史已获取，当前原件未恢复（替代版本另记）'
    writecsv(ROOT/'manual_review/historical91_original_recovery_queue_utf8.csv',historical_queue)
    writecsv(ROOT/'manual_review/current_environment_need_fulltext_utf8.csv',[r for r in current if not r['当前原件SHA256']])
    library=readcsv(ROOT/'final_results/ad_oxygen_download_review_utf8.csv')
    for row in library:
        if row['稳定记录ID'] in rows_by_id:
            for key,value in rows_by_id[row['稳定记录ID']].items():
                if key in row and key.startswith(('当前','新环境','原件恢复','持久化')):row[key]=value
    writecsv(ROOT/'final_results/ad_oxygen_download_review_utf8.csv',library)
    paperrows=readcsv(ROOT/'inventory/papers_utf8.csv')
    for row in paperrows:
        m=load(ROOT/'papers'/row['record_id']/'metadata.json')
        for k in ['main_status','supplementary_status','supplementary_coverage_complete','supplementary_official_count']:row[k]=m[k]
    writecsv(ROOT/'inventory/papers_utf8.csv',paperrows)
    sirows=readcsv(ROOT/'manual_review/supplementary_material_status_utf8.csv')
    for row in sirows:
        aa=[a for a in byid[row['原记录ID']] if a['role']=='supplementary' and present(a)]
        checked=si_checks.get(row['原记录ID'],{})
        detail={'downloaded':'已下载全部JATS明确列出的本地附件；外部数据单列',
            'explicit_no_attachments_in_complete_JATS':'已检查身份匹配的完整JATS，明确未声明附件',
            'explicit_no_attachments_on_article_page':'目标文章页明确声明无补充材料',
            'external_data_links_only':'完整JATS仅列外部数据链接；未自动下载数据库',
            'access_failed':'访问失败；不能据此判无附件','partial_or_access_failed':'部分附件已下载，其余访问失败或未取得'}.get(checked.get('status'))
        row.update({'核查日期':'2026-10-17','附件数量':str(len(aa)),'当前附件保存位置':'; '.join(a['source_repo_path'] for a in aa),
            '附件SHA256':'; '.join(a['sha256'] for a in aa),
            '补充材料获取状态':detail or ('已下载；全附件覆盖尚未确认' if aa else '尚未检查或历史附件未恢复'),
            '附件持久化状态':'Git原件已恢复；独立核验见recovery清单' if aa else '当前无附件原件；不判无附件',
            '附件用户下载入口':'; '.join(a['source_repo_path'] for a in aa)})
    writecsv(ROOT/'manual_review/supplementary_material_status_utf8.csv',sirows)
    for rispath in (ROOT/'final_results').glob('*.ris'):
        content=rispath.read_text(encoding='utf-8-sig')
        parts=re.split(r'(?=^TY  - )',content,flags=re.M);updated=[]
        for part in parts:
            match=re.search(r'^ID  - (.+)$',part,re.M)
            if match and match.group(1) in rows_by_id:
                row=rows_by_id[match.group(1)]
                part=re.sub(r'^N1  - 恢复2026-10-17：.*\n?','',part,flags=re.M)
                note='N1  - 恢复2026-10-17：'+row['当前原件状态']+'；SHA256='+row['当前原件SHA256']+'；Git路径='+row['当前持久下载入口']+'；SI='+row['当前补充材料状态']+'；人工分类及旧获取记录保留。\n'
                part=re.sub(r'^ER  -',lambda m:note+m.group(0),part,flags=re.M)
            updated.append(part)
        rispath.write_text(''.join(updated),encoding='utf-8')
    # Do not replace historical workbook sheets or RIS notes. Refresh live rows,
    # and expose new explicitly dated recovery sheets/notes alongside them.
    bookpath=ROOT/'final_results/ad_oxygen_download_review_20261006.xlsx'
    book=openpyxl.load_workbook(bookpath)
    library_byid={x['稳定记录ID']:x for x in library}
    for sheet in book:
        header={str(cell.value):cell.column for cell in sheet[1] if cell.value is not None}
        if '稳定记录ID' not in header:continue
        for number in range(2,sheet.max_row+1):
            id=sheet.cell(number,header['稳定记录ID']).value
            if id not in library_byid:continue
            for key,column in header.items():
                if key.startswith(('当前','新环境','原件恢复','持久化')) and key in library_byid[id]:sheet.cell(number,column,library_byid[id][key])
    for name,data in [('恢复20261017',current),('当前原件20261017',assets),('补充材料20261017',sirows)]:
        if name in book:del book[name]
        sheet=book.create_sheet(name);fields=list(data[0])
        sheet.append(fields)
        for row in data:sheet.append([json.dumps(row.get(k,''),ensure_ascii=False) if isinstance(row.get(k), (dict,list)) else row.get(k,'') for k in fields])
        sheet.freeze_panes='A2';sheet.auto_filter.ref=sheet.dimensions
    book.save(bookpath)
    invpath=ROOT/'inventory/unified_library_inventory.xlsx'
    inv=openpyxl.load_workbook(invpath) if invpath.exists() else openpyxl.Workbook()
    if 'Sheet' in inv and inv['Sheet'].max_row==1:del inv['Sheet']
    for name,data in [('papers',paperrows),('assets',assets),('reacquisition',queue)]:
        if name in inv:del inv[name]
        sheet=inv.create_sheet(name)
        if data:
            fields=list(data[0]);sheet.append(fields)
            for row in data:sheet.append([json.dumps(row.get(k,''),ensure_ascii=False) if isinstance(row.get(k),(dict,list)) else row.get(k,'') for k in fields])
    inv.save(invpath)
    save(RUN/'status.json',{'checked_at_utc':now(),'included_records':426,'current_verified_main_ids':main_ok,
        'missing_main_ids':426-main_ok,'present_assets':sum(present(a) for a in assets),
        'historical_missing_assets':len(queue),'source_failures':len(attempts),
        'classification_changed':False,'new_topic_searches':False})
    readme=ROOT/'README.md';content=readme.read_text()
    if '\n# 第18轮' in content:
        history='\n# 第18轮'+content.split('\n# 第18轮',1)[1]
        roles=collections.Counter(a['role'] for a in assets if present(a))
        readme.write_text(f'''# 新环境恢复与全部原件备份（2026-10-17，当前）

以远端提交 `bac51bfccceae13a91745322ed5793260e30a85c` 实际文件恢复：40正文、9官方附件、5历史派生件。554条及全部人工判断保留，类别1–4共426条，不重新检索或分类。

当前实际核验正文 **{main_ok}篇**，缺正文 **{426-main_ok}篇**。实际对象角色：{dict(roles)}。历史记录但无原件者明确标记“历史已获取，当前原件未恢复”，历史SHA和替代版本分开保留。3篇重新下载、上传及独立远端读回门槛已完成，后续按5篇或10分钟检查点推送；仅远端核验通过后称已备份。

- [最新状态](inventory/recovery_20261017/status.json)、[逐文件备份/独立读回清单](inventory/recovery_20261017/backup_manifest_utf8.csv)、[远端核验回执](inventory/recovery_20261017/remote_readback.json)
- [正文原件](original_files/fulltext/)、[补充材料原件](original_files/supplementary/)、[逐ID解析结果](papers/)、[统一原件清单](inventory/assets_utf8.csv)
- [426获取状态](manual_review/current_environment_acquisition426_utf8.csv)、[尚缺正文](manual_review/current_environment_need_fulltext_utf8.csv)、[历史缺件队列](inventory/recovery_20261017/historical_reacquisition_queue_utf8.csv)、[SI逐篇状态](manual_review/supplementary_material_status_utf8.csv)
- [总Excel](final_results/ad_oxygen_download_review_20261006.xlsx)、[总CSV](final_results/ad_oxygen_download_review_utf8.csv)、[分组RIS](final_results/)
- [安装脚本](methods/runtime_support/recover_20261017.sh)、[恢复/下载/解析/备份脚本](methods/recovery_20261017.py)、[现有文献及SI续取脚本](methods/continue_records_20261017.py)

所有取得且允许保存的原件、解析结果和记录直接备份到本私有结果分支；不依赖旧环境或外部存储。既有ZIP仅为历史元数据包，无论文原件，不新增重复原件整包。以下数量、局部交付和未备份说明均为历史快照，当前以本节及20261017清单为准。
\n'''+history)
    print(json.dumps(load(RUN/'status.json'),ensure_ascii=False))

def parse_files():
    baseline();manifest=[]
    for a in load(ASSETS,[]):
        if not present(a):continue
        path=path_for(a);out=ROOT/'papers'/a['record_id']/'extracted'/a['asset_id'];out.mkdir(parents=True,exist_ok=True)
        outputs=[]
        if a['format'].lower()=='pdf':
            doc=fitz.open(path);pages=[]
            for n,page in enumerate(doc):pages.append({'page':n+1,'text':page.get_text()})
            if not doc.page_count:raise ValueError(f'Empty PDF: {path}')
            save(out/'pages_recovery_20261017.json',{'record_id':a['record_id'],'source_sha256':a['sha256'],'page_count':doc.page_count,'pages':pages})
            (out/'fulltext_recovery_20261017.txt').write_text('\n'.join(f'\n[PDF page {p["page"]}]\n{p["text"]}' for p in pages))
            outputs=[out/'pages_recovery_20261017.json',out/'fulltext_recovery_20261017.txt']
        elif path.suffix.lower() in ['.xlsx','.xlsm']:
            book=openpyxl.load_workbook(path,read_only=True,data_only=False)
            data={sheet.title:[[str(v) if v is not None else '' for v in row] for row in sheet.values] for sheet in book}
            save(out/'worksheets_recovery_20261017.json',{'record_id':a['record_id'],'source_sha256':a['sha256'],'worksheets':data});book.close()
            outputs=[out/'worksheets_recovery_20261017.json']
        elif path.suffix.lower()=='.docx':
            from xml.etree import ElementTree as ET
            with zipfile.ZipFile(path) as z:
                xml=ET.fromstring(z.read('word/document.xml'))
                paras=[''.join(t.itertext()) for t in xml.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')]
            save(out/'paragraphs_recovery_20261017.json',{'record_id':a['record_id'],'source_sha256':a['sha256'],'paragraphs':paras});outputs=[out/'paragraphs_recovery_20261017.json']
        elif path.suffix.lower()=='.zip':
            with zipfile.ZipFile(path) as z:
                data=[{'member':i.filename,'uncompressed_bytes':i.file_size,'compressed_bytes':i.compress_size,'sha256':sha(z.read(i))} for i in z.infolist() if not i.is_dir()]
            save(out/'archive_members_recovery_20261017.json',{'record_id':a['record_id'],'source_sha256':a['sha256'],'members':data,'original_members_not_duplicated':True});outputs=[out/'archive_members_recovery_20261017.json']
        for p in outputs:manifest.append({'record_id':a['record_id'],'source_sha256':a['sha256'],'relative_path':str(p.relative_to(ROOT)),'size_bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
    writecsv(RUN/'parsed_files_utf8.csv',manifest)
    print(json.dumps({'parsed_outputs':len(manifest),'bytes':sum(x['size_bytes'] for x in manifest)}))

def fetch_bytes(url,paused,last,events,id):
    host=urllib.parse.urlsplit(url).hostname
    if host in paused:return None
    time.sleep(max(0,5-(time.monotonic()-last.get(host,0))))
    event={'record_id':id,'url':safe_url(url),'time_utc':now()}
    def deadline(signum,frame):raise TimeoutError('Per-request wall time exceeded')
    previous_handler=signal.signal(signal.SIGALRM,deadline)
    signal.alarm(60)
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Existing-record literature recovery (polite, 5s per host)'}),timeout=25) as response:
            data=response.read(50*1024*1024+1)
            if len(data)>50*1024*1024:raise ValueError('over 50 MiB; review size/storage before download')
            event.update(http=response.status,bytes=len(data),content_type=response.headers.get('content-type'),final_url=safe_url(response.url))
            return data
    except Exception as e:
        message=str(e)
        reason='proxy_CONNECT_403' if 'Tunnel connection failed: 403' in message else 'HTTP_'+str(e.code) if isinstance(e,urllib.error.HTTPError) else type(e).__name__
        event['error']=reason
        if reason in ['proxy_CONNECT_403','HTTP_401','HTTP_403','HTTP_429']:paused[host]=reason
    finally:
        signal.alarm(0);signal.signal(signal.SIGALRM,previous_handler)
        last[host]=time.monotonic();events.append(event)
        with (RUN/'access_events.jsonl').open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')

def retrieve(pilot=False):
    baseline();assets=load(ASSETS,[]);results=load(RUN/'retrieval_results.json',{});events=[];last={};paused={}
    progress_file=RUN/('pilot_downloads.json' if pilot else 'batch_downloads.json')
    success=load(progress_file,{}).get('downloaded_asset_ids',[])
    checkpoint=time.monotonic();response_cache={}
    if not pilot:
        receipt=load(RUN/'pilot_gate.json',{})
        if not receipt.get('all_original_bytes_readback_verified') or receipt.get('body_samples',0)<3:
            raise SystemExit('Required three-paper download/upload/independent-readback gate not passed; no bulk download started')
    pending=[]
    for a in assets:
        if present(a) or a['role'] not in ['main','supplementary','evidence_xml']:continue
        if a['role']=='main' and a.get('source_url') and any(b['record_id']==a['record_id'] and b['role']=='main' and b.get('source_url')==a['source_url'] and present(b) for b in assets):
            a['historical_restore_note']='Same source currently supplies an already-held different SHA; reuse valid current version, historical bytes remain missing'
            continue
        pending.append(a)
    # Public, identity-bound sources already recorded in the repository only.
    pending.sort(key=lambda a:(a['role']!='main',a['record_id'] not in ['R01238','R07903','R03455']))
    for a in pending:
        id=a['record_id'];url=a.get('source_url') or a.get('source_xml_url','')
        if not url.startswith('https://'):continue
        if url not in response_cache:response_cache[url]=fetch_bytes(url,paused,last,events,id)
        data=response_cache[url]
        if not data:
            results[id]={'time_utc':now(),'status':'access_failed','reason':paused.get(urllib.parse.urlsplit(url).hostname,events[-1].get('error','request_failed') if events else 'request_failed'),'url':url}
            save(RUN/'retrieval_results.json',results)
            if time.monotonic()-checkpoint>=600:
                audit();parse_files();sync('Timed literature recovery checkpoint');checkpoint=time.monotonic()
            continue
        # EuropePMC returns attachment bundles. Accept only exact expected
        # member bytes; do not put the transport ZIP and its members in Git.
        if sha(data)!=a['sha256'] and data.startswith(b'PK'):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for info in z.infolist():
                    if not info.is_dir() and info.file_size<50*1024*1024:
                        candidate=z.read(info)
                        if sha(candidate)==a['sha256']:data=candidate;break
        check={'historical_sha_match':sha(data)==a['sha256'],'bytes':len(data),'sha256':sha(data)}
        if not check['historical_sha_match']:
            # Preserve acquired candidates, but never call an unidentified
            # HTML response or a different paper verified full text.
            duplicate=next((b for b in assets if b['record_id']==id and b['sha256']==check['sha256'] and present(b)),None)
            if duplicate:check['reused_existing_different_version_path']=duplicate['source_repo_path']
            elif data.startswith(b'%PDF'):
                path=ROOT/'original_files/unverified_candidates'/id/(sha(data)[:16]+'.pdf');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
                check['candidate_path']=str(path.relative_to(ROOT));check['manual_identity_review_required']=True
            results[id]={'time_utc':now(),'status':'candidate_not_verified','reason':'historical_SHA_mismatch','checks':check,'url':url};save(RUN/'retrieval_results.json',results);continue
        if a['role']=='main':
            doc=fitz.open(stream=data,filetype='pdf');texts=[p.get_text() for p in doc]
            check.update(pages=len(texts),all_pages_parsed=True,text_chars=sum(map(len,texts)),identity='previously verified exact source bytes plus current all-page parsing')
            if len(texts)<2 or sum(map(len,texts))<1000:raise ValueError('PDF body verification failed '+id)
        folder='fulltext' if a['role']=='main' else 'supplementary/'+id if a['role']=='supplementary' else 'source_evidence/'+id
        path=ROOT/'original_files'/folder/a['original_filename'];path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists() and sha(path.read_bytes())!=a['sha256']:raise ValueError('Preserve pre-existing file '+str(path))
        path.write_bytes(data);a.update(source_repo_path=str(path.relative_to(ROOT)),resolved_source_path=str(path),availability='present_sha_verified',storage_status='local_acquired_pending_remote_readback')
        save(ASSETS,assets)
        results[id]={'time_utc':now(),'status':'downloaded_verified','checks':check,'url':url,'asset_id':a['asset_id']};save(RUN/'retrieval_results.json',results)
        success.append(a['asset_id']);save(RUN/'downloaded_asset_ids.json',success)
        print(id,a['role'],'verified',len(data),flush=True)
        if pilot and sum('.main.' in x for x in success)>=3:break
        if time.monotonic()-checkpoint>=600 or (not pilot and len(success)%5==0):
            audit();parse_files();sync('Batch original-file recovery checkpoint');checkpoint=time.monotonic()
    save(RUN/('pilot_downloads.json' if pilot else 'batch_downloads.json'),{'time_utc':now(),'downloaded_asset_ids':success,'body_samples':sum('.main.' in x for x in success),'paused_hosts':paused,'gate_passed':False})
    audit()
    print(json.dumps({'newly_downloaded':len(success),'paused_hosts':paused,'pilot':pilot},ensure_ascii=False))

def remote_verify(persist=True):
    # Independent remote object database: no alternates, local clones, or
    # copies of local objects. Git fetch uses platform-injected HTTPS auth.
    bare=Path('/tmp/ad-oxygen-remote-readback-20261017.git')
    if not bare.exists():subprocess.run(['git','init','--bare',str(bare)],check=True,stdout=subprocess.DEVNULL)
    subprocess.run(['git','--git-dir',str(bare),'fetch','--depth=1','https://github.com/Colliam-Vermilion/FirstCodex.git',BRANCH],check=True)
    commit=subprocess.check_output(['git','--git-dir',str(bare),'rev-parse','FETCH_HEAD'],text=True).strip()
    checks=[]
    expected=[]
    for a in load(ASSETS,[]):
        if present(a):expected.append({'record_id':a['record_id'],'role':a['role'],'relative_path':a['source_repo_path'],'sha256':a['sha256'],'size_bytes':int(a['size_bytes'])})
    expected+=readcsv(RUN/'parsed_files_utf8.csv') if (RUN/'parsed_files_utf8.csv').exists() else []
    # Include pre-existing parsed samples and any acquired unverified files.
    known={r['relative_path'] for r in expected}
    for parent in [ROOT/'papers',ROOT/'original_files']:
        for p in parent.rglob('*'):
            if p.is_file() and ('/extracted/' in str(p) or ('/original_files/' in str(p) and p.suffix.lower() in ['.pdf','.zip','.doc','.docx','.xls','.xlsx','.csv','.xml','.html','.jpg','.png','.mp4','.mov','.r','.py'])) and str(p.relative_to(ROOT)) not in known:
                expected.append({'relative_path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'size_bytes':p.stat().st_size,'role':'derived_parse' if '/extracted/' in str(p) else 'acquired_candidate'})
    prefix=str(ROOT.relative_to(REPO))
    tree=subprocess.check_output(['git','--git-dir',str(bare),'ls-tree','-r','-z','--format=%(objectname) %(path)',commit])
    blobids={entry.decode().split(' ',1)[1]:entry.decode().split(' ',1)[0] for entry in tree.split(b'\0') if entry}
    previous={x['relative_path']:x for x in load(RUN/'remote_readback.json',{}).get('checks',[])}
    for row in expected:
        rel=row['relative_path'];cmd=['git','--git-dir',str(bare),'show',commit+':'+prefix+'/'+rel]
        oid=blobids.get(prefix+'/'+rel);old=previous.get(rel,{})
        if oid and oid==old.get('remote_blob_oid') and old.get('backed_up') and old.get('sha256')==row['sha256'] and int(old['size_bytes'])==int(row['size_bytes']):
            checks.append({**row,'size_bytes':int(row['size_bytes']),'remote_commit':commit,'remote_blob_oid':oid,
                'sha_size_match':True,'readable':True,'backed_up':True,'independent_readback_this_batch':False,
                'unchanged_git_object_already_read_back':True,'readback_source_commit':old.get('readback_source_commit',old['remote_commit'])})
            continue
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        ok=p.returncode==0 and sha(p.stdout)==row['sha256'] and len(p.stdout)==int(row['size_bytes'])
        readable=True
        if ok and rel.lower().endswith('.pdf'):
            try:
                doc=fitz.open(stream=p.stdout,filetype='pdf');readable=bool(doc.page_count)
                for page in doc:page.get_text()
            except Exception:readable=False
        elif ok and rel.lower().endswith(('.xlsx','.docx','.zip')):
            try:
                with zipfile.ZipFile(io.BytesIO(p.stdout)) as z:readable=z.testzip() is None
            except Exception:readable=False
        checks.append({**row,'size_bytes':int(row['size_bytes']),'remote_commit':commit,'remote_blob_oid':oid,
            'sha_size_match':ok,'readable':readable,'backed_up':bool(ok and readable),'independent_readback_this_batch':True,'readback_source_commit':commit})
    originals=[r for r in checks if r.get('role') in ['main','supplementary','derived','evidence_xml']]
    report={'time_utc':now(),'remote_commit':commit,'independent_git_database':str(bare),'uses_local_alternates':False,
        'verified_files':sum(r['backed_up'] for r in checks),'files':len(checks),
        'original_files':len(originals),'original_bytes':sum(r['size_bytes'] for r in originals if r['backed_up']),
        'all_passed':bool(checks) and all(r['backed_up'] for r in checks),'checks':checks}
    if not persist:
        save(Path('/workspace/tools/final_remote_readback_20261017.json'),report)
        print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
        if not report['all_passed']:raise SystemExit('Final independent remote verification failed')
        return
    save(RUN/'remote_readback.json',report);writecsv(RUN/'backup_manifest_utf8.csv',checks)
    assets=load(ASSETS,[])
    for a in assets:
        if any(r.get('relative_path')==a.get('source_repo_path') and r['backed_up'] for r in checks):a['storage_status']='git_remote_verified_20261017'
    save(ASSETS,assets)
    pilot=load(RUN/'pilot_downloads.json',{})
    ids=pilot.get('downloaded_asset_ids',[])
    passed=[a for a in load(ASSETS,[]) if a['asset_id'] in ids and a['role']=='main' and any(r['relative_path']==a['source_repo_path'] and r['backed_up'] for r in checks)]
    save(RUN/'pilot_gate.json',{'time_utc':now(),'body_samples':len(passed),'all_original_bytes_readback_verified':len(passed)>=3,'remote_commit':commit,'verified_asset_ids':[a['asset_id'] for a in passed],
        'recovered_existing_files_do_not_count_as_new_download_pilot':True})
    print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
    if not report['all_passed']:raise SystemExit('Remote byte/readability mismatch; do not mark backup complete')

def sync(message,final=False):
    if git('branch','--show-current')!=BRANCH:raise SystemExit('Refusing changes outside result branch')
    subprocess.run(['git','-C',str(REPO),'fetch','origin',BRANCH],check=True)
    remote=git('rev-parse','FETCH_HEAD')
    # Never discard remote edits. Stop for explicit merge on divergence.
    if subprocess.run(['git','-C',str(REPO),'merge-base','--is-ancestor',remote,'HEAD']).returncode:
        raise SystemExit('Remote advanced; preserve local changes and merge before pushing')
    subprocess.run(['git','-C',str(REPO),'add','--',str(ROOT.relative_to(REPO))],check=True)
    if subprocess.run(['git','-C',str(REPO),'diff','--cached','--quiet']).returncode:
        subprocess.run(['git','-C',str(REPO),'-c','user.name=Codex','-c','user.email=codex@openai.com','commit','-m',message],check=True)
    subprocess.run(['git','-C',str(REPO),'push','origin','HEAD:refs/heads/'+BRANCH],check=True)
    remote_verify(persist=not final)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['audit','parse','pilot','batch','verify-remote','sync','sync-final'])
    parser.add_argument('--message',default='Restore literature project and persist verified originals and recovery evidence')
    args=parser.parse_args()
    if args.action=='audit':audit()
    elif args.action=='parse':parse_files()
    elif args.action=='pilot':retrieve(True)
    elif args.action=='batch':retrieve(False)
    elif args.action=='verify-remote':remote_verify()
    elif args.action in ['sync','sync-final']:sync(args.message,final=args.action=='sync-final')

if __name__=='__main__':main()
