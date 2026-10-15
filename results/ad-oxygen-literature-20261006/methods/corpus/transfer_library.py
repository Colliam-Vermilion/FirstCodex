"""Prepare/verify private hybrid corpus and reviewed Windows returns, without cloud credentials.

Published originals remain in the existing Git original_files tree. Private packages
contain the missing private originals plus extraction files, not another public copy.
Every package is checked by actual SHA256 reads before hydration or ID-based merge.
"""
from pathlib import Path,PurePosixPath
import argparse,csv,hashlib,json,re,shutil,zipfile,subprocess
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
from audit_library import dump,sha,read_csv,write_csv


def safe_member(name):
    p=PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name and not re.match(r'^[A-Za-z]:',name)


def redact_url(url):
    u=urlsplit(url);host=u.hostname or ''
    if u.port:host+=':'+str(u.port)
    values=parse_qsl(u.query,keep_blank_values=True)
    query=[(k,'REDACTED' if re.search(r'token|secret|signatur|credential|authorization|api.?key|x-amz-',k,re.I) else v) for k,v in values]
    return urlunsplit((u.scheme,host,u.path,urlencode(query),''))


def verify_package(path,expected=None):
    path=Path(path)
    if expected and sha(path)!=expected:raise ValueError('Package SHA mismatch')
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)>200000 or sum(i.file_size for i in z.infolist())>20*1024**3:raise ValueError('Package exceeds safety review limit')
        if len(names)!=len(set(names)) or any(not safe_member(n) for n in names):raise ValueError('Unsafe/duplicate archive path')
        manifest=json.loads(z.read('transfer_manifest.json'));expected_files=manifest['files']
        if set(names)!={r['path'] for r in expected_files}|{'transfer_manifest.json'}:raise ValueError('Unmanifested or missing package members')
        for row in expected_files:
            info=z.getinfo(row['path'])
            if info.file_size!=row['size_bytes']:raise ValueError('Member size mismatch')
            h=hashlib.sha256()
            with z.open(info) as f:
                for data in iter(lambda:f.read(1048576),b''):h.update(data)
            if h.hexdigest()!=row['sha256']:raise ValueError('Member SHA mismatch: '+row['path'])
    return {'package_sha256':sha(path),'size_bytes':path.stat().st_size,'files_verified':len(expected_files),'kind':manifest['kind'],'all_member_sha_verified':True,'manifest':manifest}


def write_package(output,sources,kind,extra):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);temporary=output.with_suffix(output.suffix+'.partial')
    rows=[];seen={}
    with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for rel,source,role in sources:
            if not safe_member(rel):raise ValueError('Unsafe output path')
            source=Path(source);digest=sha(source)
            if rel in seen:
                if seen[rel]!=digest:raise ValueError('Conflicting output path')
                continue
            seen[rel]=digest;z.write(source,rel);rows.append({'path':rel,'sha256':digest,'size_bytes':source.stat().st_size,'role':role})
        manifest={'schema_version':1,'kind':kind,'files':rows,**extra};z.writestr('transfer_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    if output.exists():
        if sha(output)!=sha(temporary):temporary.unlink();raise FileExistsError('Different package already exists; use a versioned output filename')
        temporary.unlink()
    else:temporary.replace(output)
    result=verify_package(output);receipt={k:v for k,v in result.items() if k!='manifest'};dump(output.with_suffix(output.suffix+'.sha256.json'),receipt);return receipt


def prepare(args):
    p=args.project.resolve();root=args.root.resolve();assets=json.loads((p/'inventory/assets.json').read_text());sources=[];mapping=[]
    for a in assets:
        if a['storage_status']=='git_remote_verified':
            if not a.get('source_repo_path') or sha(p/a['source_repo_path'])!=a['sha256']:raise ValueError('Git original missing/mismatched')
            mapping.append({'asset_id':a['asset_id'],'canonical_path':a['canonical_path'],'storage':'github_existing_original','source_repo_path':a['source_repo_path'],'source_commit':json.loads((p/'inventory/current_file_audit.json').read_text())['baseline_commit'],'sha256':a['sha256']});continue
        source=next((f for f in [root/a['canonical_path'],Path(a['resolved_source_path'])] if f.is_file() and sha(f)==a['sha256']),None)
        if source is None:raise ValueError('Private original absent: '+a['asset_id'])
        sources.append((a['canonical_path'],source,'private_original'));mapping.append({'asset_id':a['asset_id'],'canonical_path':a['canonical_path'],'storage':'private_package','sha256':a['sha256']})
    for f in sorted((root/'papers').rglob('*')):
        if f.is_file() and 'extracted' in f.parts:sources.append((f.relative_to(root).as_posix(),f,'extracted'))
    for f in sorted((p/'papers').glob('*/metadata.json')):sources.append((f.relative_to(p).as_posix(),f,'metadata'))
    for name in ['assets.json','papers_utf8.csv','current_file_audit.json','external_data_links.json','extraction_summary.json','source_media_map.json','extracted_files.json','parser_run_receipt.json','external_data_link_check.json']:
        if not (p/'inventory'/name).exists():continue
        sources.append(('inventory/'+name,p/'inventory'/name,'inventory'))
    if (root/'search.sqlite').is_file():sources.append(('search.sqlite',root/'search.sqlite','search_index'))
    # An explicit storage map preserves existing Git copies as durable originals.
    tmp=args.out.with_suffix('.storage_map.json');dump(tmp,mapping);sources.append(('inventory/storage_map.json',tmp,'storage_map'))
    receipt=write_package(args.out,sources,'hybrid_private_corpus',{'original_assets':len(assets),'github_original_assets_reused':sum(x['storage']=='github_existing_original' for x in mapping),'private_original_assets':sum(x['storage']=='private_package' for x in mapping),'external_cloud_uploaded':False})
    dump(p/'inventory/private_package_preparation.json',{**receipt,'local_package_path_not_download_link':str(args.out.resolve()),'external_cloud_uploaded':False,'storage_status':'prepared_and_locally_verified_only','private_originals':sum(x['storage']=='private_package' for x in mapping),'published_originals_reused':sum(x['storage']=='github_existing_original' for x in mapping)})
    print(json.dumps(receipt))


def prepare_return(args):
    root=args.root.resolve();intake_manifest=root/'intake/assets.json';assets=json.loads(intake_manifest.read_text()) if intake_manifest.exists() else [];sources=[];validated=[]
    acknowledged=set()
    if getattr(args,'exclude_ack',None):
        ack=json.loads(args.exclude_ack.read_text());acknowledged=set(ack.get('new_assets',[])+ack.get('duplicate_assets_skipped',[]))
    assets=[a for a in assets if a['asset_id'] not in acknowledged and (not getattr(args,'ids',None) or a['record_id'] in args.ids.split(','))]
    for a in assets:
        if not a.get('review',{}).get('identity_or_association_explicitly_reviewed'):raise ValueError('Unreviewed source in return')
        source=root/a['canonical_path']
        if not source.is_file() or sha(source)!=a['sha256'] or source.stat().st_size!=a['size_bytes']:raise ValueError('Returned file bytes changed')
        a['source_url']=redact_url(a.get('source_url',''));validated.append(a);sources.append((a['canonical_path'],source,'reviewed_original'))
        folder=root/'papers'/a['record_id']/'extracted'/a['asset_id']
        if folder.exists():
            for f in folder.rglob('*'):
                if f.is_file():sources.append((f.relative_to(root).as_posix(),f,'extracted'))
    sanitized=root/'intake/return_assets.json';dump(sanitized,validated);sources.append(('inventory/returned_assets.json',sanitized,'returned_inventory'))
    for f in (root/'intake').glob('*/supplementary_review.json'):
        if getattr(args,'ids',None) and f.parent.name not in args.ids.split(','):continue
        sources.append((f.relative_to(root).as_posix(),f,'SI_review'))
    result=write_package(args.out,sources,'reviewed_windows_return',{'reviewed_asset_count':len(validated),'raw_credentials_included':False});print(json.dumps(result))


def hydrate(args):
    result=verify_package(args.package,args.expected_sha256);dest=args.root.resolve();dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.package) as z:
        for row in result['manifest']['files']:
            target=dest/row['path'];target=target.resolve()
            if dest not in target.parents:raise ValueError('Archive target escapes root')
            if target.exists():
                if sha(target)!=row['sha256']:raise ValueError('Existing different bytes; hydrate into a new directory')
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            with z.open(row['path']) as src,target.open('wb') as out:shutil.copyfileobj(src,out)
    dump(dest/'transfer_receipt.json',{k:v for k,v in result.items() if k!='manifest'});print(json.dumps({k:v for k,v in result.items() if k!='manifest'}))


def verify_view(args):
    p=args.project.resolve();root=args.root.resolve();assets=json.loads((root/'inventory/assets.json').read_text());checks=[]
    for a in assets:
        choices=[root/a['canonical_path']]
        if a.get('source_repo_path'):choices.append(p/a['source_repo_path'])
        found=next((f for f in choices if f.is_file() and sha(f)==a['sha256'] and f.stat().st_size==a['size_bytes']),None)
        checks.append({'record_id':a['record_id'],'asset_id':a['asset_id'],'verified':found is not None,'physical_path':str(found) if found else None})
    report={'assets':len(checks),'verified':sum(x['verified'] for x in checks),'all_originals_actually_readable':all(x['verified'] for x in checks),'checks':checks,'external_cloud_readback_claimed':False}
    dump(root/'hybrid_view_verification.json',report);print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
    if not report['all_originals_actually_readable']:raise SystemExit(1)


def merge(args):
    p=args.project.resolve();root=args.root.resolve();incoming=json.loads((root/'inventory/returned_assets.json').read_text());existing=json.loads((p/'inventory/assets.json').read_text());index={a['asset_id']:a for a in existing};accepted=[];duplicates=[];version_conflicts=[]
    for f in (root/'intake').glob('*/supplementary_review.json'):
        review=json.loads(f.read_text());meta=json.loads((p/'papers'/review['record_id']/'metadata.json').read_text())
        if not re.fullmatch(r'R[0-9]+',review['record_id']) or not meta['included_for_download']:raise ValueError('Excluded/invalid record in SI review')
        if review['supplementary_status']=='explicit_none' and (not (review.get('publisher_checked') and review.get('repository_checked') and review.get('evidence')) or meta.get('supplementary_official_count',0)):raise ValueError('Invalid explicit-none review')
    # Validate the complete batch before any metadata mutation.
    for a in incoming:
        if a['role'] not in ['main','supplementary','derived','evidence_xml','transport_archive']:raise ValueError('Unknown asset role')
        if not re.fullmatch(r'R[0-9]+',a['record_id']) or not safe_member(a['canonical_path']) or not a['canonical_path'].startswith('papers/'+a['record_id']+'/'):raise ValueError('Invalid incoming ID/path')
        if a['asset_id']!=a['record_id']+'.'+a['role']+'.'+a['sha256'][:16]:raise ValueError('Invalid incoming asset identity')
        source=(root/a['canonical_path']).resolve()
        if root not in source.parents or not source.is_file() or sha(source)!=a['sha256'] or source.stat().st_size!=a['size_bytes']:raise ValueError('Preflight SHA/path failure')
        meta=json.loads((p/'papers'/a['record_id']/'metadata.json').read_text())
        if not meta['included_for_download'] or not a.get('review',{}).get('identity_or_association_explicitly_reviewed'):raise ValueError('Excluded/unreviewed incoming file')
    for a in incoming:
        meta=json.loads((p/'papers'/a['record_id']/'metadata.json').read_text())
        if not meta['included_for_download']:raise ValueError('Excluded ID in return')
        if not a.get('review',{}).get('identity_or_association_explicitly_reviewed'):raise ValueError('Missing explicit review')
        source=root/a['canonical_path']
        if not source.is_file() or sha(source)!=a['sha256'] or source.stat().st_size!=a['size_bytes']:raise ValueError('Returned SHA/size mismatch')
        if a['asset_id'] in index:
            old=index[a['asset_id']]
            if old['sha256']!=a['sha256']:raise ValueError('Asset prefix collision; full SHA differs')
            if not old.get('source_repo_path'):
                old['resolved_source_path']=str(source);old['source_local_path']=str(source)
                for item in meta['assets']:
                    if item['asset_id']==a['asset_id']:item['resolved_source_path']=str(source);item['source_local_path']=str(source)
                dump(p/'papers'/a['record_id']/'metadata.json',meta)
            duplicates.append(a['asset_id']);continue
        if any(x['record_id']==a['record_id'] and x['role']=='main' and x['sha256']!=a['sha256'] for x in existing) and a['role']=='main':
            version_conflicts.append({'record_id':a['record_id'],'new_asset_id':a['asset_id'],'decision':'both versions preserved; preferred current original unchanged'})
        a['preferred_for_record']=a['role']=='main' and not any(x['record_id']==a['record_id'] and x['role']=='main' for x in existing)
        a['resolved_source_path']=str(source);a['source_local_path']=str(source);a['source_repo_path']='';a['storage_status']='private_return_readable_local_cloud_persistence_requires_remote_receipt';a['source_url']=redact_url(a.get('source_url',''))
        reportfile=root/'papers'/a['record_id']/'extracted'/a['asset_id']/'report.json'
        if reportfile.is_file():
            parser=json.loads(reportfile.read_text())
            if parser.get('source_sha256')==a['sha256']:a['parsing_status']=parser['status'];a['extraction']={'relative_directory':f'papers/{a["record_id"]}/extracted/{a["asset_id"]}'}
        existing.append(a);index[a['asset_id']]=a;accepted.append(a['asset_id'])
        meta['assets']=[x for x in meta['assets'] if x['asset_id']!=a['asset_id']]+[a];meta.setdefault('version_history',[]).append({'sha256':a['sha256'],'version':a['version'],'status':'returned_verified_version_preserved_not_automatic_replacement'})
        if a['role']=='main':
            meta['main_status']='downloaded_verified'
            if a['preferred_for_record']:meta['preferred_main_asset_id']=a['asset_id']
        elif a['role']=='supplementary':meta['supplementary_status']='downloaded_partial';meta['supplementary_official_count']=sum(x['official_attachment'] for x in meta['assets'])
        dump(p/'papers'/a['record_id']/'metadata.json',meta)
    # Preserve supplementary reviews even when no files were downloaded.
    for f in (root/'intake').glob('*/supplementary_review.json'):
        review=json.loads(f.read_text());mp=p/'papers'/review['record_id']/'metadata.json';meta=json.loads(mp.read_text())
        if not meta['included_for_download']:raise ValueError('Excluded ID in SI review')
        if review['supplementary_status']=='explicit_none' and not (review.get('publisher_checked') and review.get('repository_checked') and review.get('evidence')):raise ValueError('Unsubstantiated explicit-none')
        meta['supplementary_status']=review['supplementary_status'];meta['supplementary_coverage_complete']=review['supplementary_status']=='explicit_none';meta.setdefault('supplementary_evidence',[]).append(review);dump(mp,meta)
    dump(p/'inventory/assets.json',existing);write_csv(p/'inventory/assets_utf8.csv',existing,fields=list(existing[0]) if existing else ['record_id','asset_id','role','canonical_path','sha256','size_bytes'])
    papers=[]
    for f in sorted((p/'papers').glob('*/metadata.json')):
        m=json.loads(f.read_text());papers.append({k:m[k] for k in ['record_id','title','doi','category_unchanged','included_for_download','main_status','supplementary_status','supplementary_coverage_complete','supplementary_official_count']})
    write_csv(p/'inventory/papers_utf8.csv',papers)
    report={'new_assets':accepted,'duplicate_assets_skipped':duplicates,'version_conflicts':version_conflicts,'merged_SI_reviews':[f.parent.name for f in (root/'intake').glob('*/supplementary_review.json')],'record_id_merge_not_row_order':True,'legacy_master_and_manual_classification_not_modified':True,'remaining_included_body_ids':sum(x['included_for_download'] and x['main_status']!='downloaded_verified' for x in papers)}
    dump(p/'inventory/last_return_merge.json',report)
    from refresh_queues import refresh
    refresh(p)
    print(json.dumps(report,ensure_ascii=False))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);sub=ap.add_subparsers(dest='action',required=True)
    prep=sub.add_parser('prepare-private');prep.add_argument('--root',type=Path,required=True);prep.add_argument('--out',type=Path,required=True)
    ret=sub.add_parser('prepare-return');ret.add_argument('--root',type=Path,required=True);ret.add_argument('--out',type=Path,required=True);ret.add_argument('--ids',help='Comma-separated original IDs for smaller return batches');ret.add_argument('--exclude-ack',type=Path,help='Previous last_return_merge.json; skip already accepted asset IDs')
    ver=sub.add_parser('verify');ver.add_argument('--package',type=Path,required=True);ver.add_argument('--expected-sha256')
    hyd=sub.add_parser('hydrate');hyd.add_argument('--package',type=Path,required=True);hyd.add_argument('--root',type=Path,required=True);hyd.add_argument('--expected-sha256')
    view=sub.add_parser('verify-view');view.add_argument('--root',type=Path,required=True)
    mer=sub.add_parser('merge-return');mer.add_argument('--root',type=Path,required=True)
    args=ap.parse_args()
    if args.action=='verify':print(json.dumps({k:v for k,v in verify_package(args.package,args.expected_sha256).items() if k!='manifest'}))
    else:{'prepare-private':prepare,'prepare-return':prepare_return,'hydrate':hydrate,'verify-view':verify_view,'merge-return':merge}[args.action](args)


if __name__=='__main__':main()
