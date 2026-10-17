"""Reconcile actual extraction files, protect prior decisions, and report delivery."""
import collections, json, sqlite3
from pathlib import Path
import recovery_20261017 as r

def finalize():
    baseline=r.load(r.RUN/'baseline.json');old=r.load(r.RUN/'baseline_library_rows.json')
    current=r.readcsv(r.ROOT/'final_results/ad_oxygen_download_review_utf8.csv')
    assert len(current)==len(old)==554
    byid={x['稳定记录ID']:x for x in current}
    for row in old:
        # All original bibliographic/scope/manual/acquisition-history fields stay.
        for key in list(row)[:110]:
            assert byid[row['稳定记录ID']][key]==row[key],(row['稳定记录ID'],key)
    for path,digest in baseline['protected_files_sha256'].items():assert r.sha((r.ROOT/path).read_bytes())==digest,path
    assets=r.load(r.ASSETS,[]);assetmap={a['asset_id']:a for a in assets}
    before=r.ROOT/'inventory/extracted_files.json'
    if not (r.RUN/'historical_extracted_manifest.json').exists():r.save(r.RUN/'historical_extracted_manifest.json',r.load(before,[]))
    historical=r.load(r.RUN/'historical_extracted_manifest.json',[])
    rows=[];paths=set();remote={x['relative_path']:x for x in r.load(r.RUN/'remote_readback.json',{}).get('checks',[])}
    for path in sorted((r.ROOT/'papers').glob('*/extracted/**/*')):
        if not path.is_file():continue
        rel=str(path.relative_to(r.ROOT));parts=path.relative_to(r.ROOT).parts;id=parts[1];aid=parts[3]
        a=assetmap.get(aid,{});digest=r.sha(path.read_bytes());prior=remote.get(rel,{})
        rows.append({'record_id':id,'asset_id':aid,'relative_path':rel,'source_sha256':a.get('sha256',''),
            'size_bytes':path.stat().st_size,'sha256':digest,'artifact_kind':'extracted','current_local_path':str(path),
            'availability':'present_sha_verified','storage_status':'git_remote_verified' if prior.get('backed_up') and prior.get('sha256')==digest else 'pending_remote_readback',
            'github_path':str(r.ROOT.relative_to(r.REPO)/rel)})
        paths.add(rel)
    for item in historical:
        if item['relative_path'] not in paths:
            rows.append({**item,'availability':'historical_processed_file_not_restored','storage_status':'historical_only_not_current_backup'})
    r.save(before,rows);r.writecsv(r.ROOT/'inventory/extracted_files_utf8.csv',rows)
    for a in assets:
        report=r.load(r.ROOT/'papers'/a['record_id']/'extracted'/a['asset_id']/'report.json',{})
        if r.present(a) and report.get('source_sha256')==a['sha256']:
            a['parsing_status']=report['status']
            a['extraction_20261017']={k:report.get(k) for k in ['status','search_chunks','table_count','ocr_pages','ocr_pending_pages','limitations','errors']}
    r.save(r.ASSETS,assets)
    index=r.ROOT/'search.sqlite';index_report={'exists':index.is_file(),'new_search_of_external_literature':False}
    if index.is_file():
        db=sqlite3.connect('file:'+str(index)+'?mode=ro',uri=True)
        index_report.update(quick_check=db.execute('PRAGMA quick_check').fetchone()[0],
            chunks=db.execute('SELECT count(*) FROM chunks').fetchone()[0],
            record_ids=db.execute('SELECT count(distinct record_id) FROM chunks').fetchone()[0],
            microaeration_query_results=db.execute("SELECT count(*) FROM chunks WHERE chunks MATCH 'microaeration'").fetchone()[0],
            sample_locator=db.execute("SELECT record_id,source_sha256,location FROM chunks WHERE chunks MATCH 'microaeration' LIMIT 1").fetchone())
        db.close();assert index_report['quick_check']=='ok' and index_report['chunks']>0 and index_report['microaeration_query_results']>0
        index_report.update(size_bytes=index.stat().st_size,sha256=r.sha(index.read_bytes()))
    baseline_assets=r.load(r.RUN/'baseline_assets.json');held0={(a['record_id'],a['role'],a['sha256']) for a in baseline_assets if a.get('source_repo_path')}
    present=[a for a in assets if r.present(a)];mains=[a for a in present if a['role']=='main'];si=[a for a in present if a['role']=='supplementary']
    new=[a for a in present if (a['record_id'],a['role'],a['sha256']) not in held0]
    historical_ids={x['原记录ID'] for x in r.readcsv(r.ROOT/'methods/audit/scansci_verified_pdf_manifest_utf8.csv')}|{a['record_id'] for a in baseline_assets if a['role']=='main'}
    official_missing=[{'record_id':a['record_id'],'filename':a['original_filename'],'sha256':a['sha256'],'source_url':a.get('source_url','')} for a in assets if a['role']=='supplementary' and not r.present(a)]
    si_status=r.load(r.RUN/'supplementary_check.json',{})
    uncovered=[x for x in r.readcsv(r.ROOT/'inventory/papers_utf8.csv') if x['included_for_download'] in ['True',True] and x['record_id'] not in si_status]
    report={'time_utc':r.now(),'restored_remote_baseline':baseline,
        'current_main_ids':len({a['record_id'] for a in mains}),'current_main_files':len(mains),'current_main_bytes':sum(int(a['size_bytes']) for a in mains),
        'current_official_supplementary_files':len(si),'current_official_supplementary_bytes':sum(int(a['size_bytes']) for a in si),
        'newly_acquired_roles':dict(collections.Counter(a['role'] for a in new)),
        'first_obtained_main_ids_this_round':sorted({a['record_id'] for a in mains if a['record_id'] not in historical_ids}),
        'remaining_main_ids':426-len({a['record_id'] for a in mains}),'known_missing_official_attachments':official_missing,
        'supplementary_record_statuses':dict(collections.Counter(x.get('status','not_checked') for x in si_status.values())),
        'supplementary_unchecked_record_count':len(uncovered),
        'present_extraction_files':sum(x['availability']=='present_sha_verified' for x in rows),
        'historical_extraction_outputs_not_restored':sum(x['availability']!='present_sha_verified' for x in rows),
        'index_validation':index_report,'original_110_fields_554_records_preserved':True,'manual_original_files_sha_preserved':True,
        'new_topic_search_or_classification':False,'unbacked_counts_require_final_remote_readback':True,
        'latest_completed_readback_commit':r.load(r.RUN/'remote_readback.json',{}).get('remote_commit')}
    r.save(r.RUN/'delivery_summary.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ['restored_remote_baseline','index_validation']},ensure_ascii=False))

if __name__=='__main__':finalize()
