"""Reconcile actual extraction files, protect prior decisions, and report delivery."""
import collections, json, sqlite3
from urllib.parse import urlsplit
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
    events=[]
    for log in [r.RUN/'access_events.jsonl',r.ROOT/'original_files/continuation_20261017/existing_included_access.jsonl',r.ROOT/'original_files/publisher_checks_20261017/publisher_SI_access.jsonl',r.ROOT/'original_files/repository_followups_20261017/exact_item_followup_access.jsonl']:
        if log.exists():events += [json.loads(line) for line in log.read_text().splitlines() if line.strip()]
    eventmap=collections.defaultdict(list)
    for event in events:
        id=event.get('record_id') or event.get('id')
        if id:eventmap[id].append(event)
    continuation=r.load(r.ROOT/'original_files/continuation_20261017/existing_included_results.json',{})
    rejected={x['sha256'] for x in r.load(r.RUN/'rejected_non_target_files.json',[])}
    labels={'pending_identity':'已取得PDF候选，身份/版本待核验','wrong_PDF':'实际返回出版商目录/宣传资料，不是目标正文',
        'proxy_CONNECT_403':'代理CONNECT403，未到达出版商；不据此判订阅','rate_limited':'HTTP429；本来源暂停自动重试',
        'HTTP403_or_challenge':'来源HTTP403/挑战；未推定学校订阅权限','authentication_required':'HTTP401/登录要求，未完成本人官方浏览器认证',
        'upstream_server_error':'来源5xx/仓储服务错误','timeout':'请求/读取超时','broken_or_expired_link':'现有链接404/410或过期',
        'HTML_no_verified_PDF':'可访问HTML/元数据，但未取得核验PDF','no_current_file_link':'现有记录未提供当前可取得的正文文件'}
    failures=[]
    for row in r.readcsv(r.ROOT/'manual_review/current_environment_need_fulltext_utf8.csv'):
        id=row['原记录ID'];ev=eventmap[id];categories=set()
        candidates=continuation.get(id,{}).get('unverified_candidates',[])
        if any(c['sha256'] not in rejected and not any(a['record_id']==id and a['sha256']==c['sha256'] and r.present(a) for a in assets) for c in candidates):categories.add('pending_identity')
        if any(c['sha256'] in rejected for c in candidates):categories.add('wrong_PDF')
        for event in ev:
            code=event.get('http',event.get('http_status'));error=event.get('error','');skip=event.get('skipped','')
            if 'CONNECT403' in str(error) or 'CONNECT_403' in str(error) or 'CONNECT403' in skip:categories.add('proxy_CONNECT_403')
            if code==429 or 'Retry-After' in skip:categories.add('rate_limited')
            if code==403:categories.add('HTTP403_or_challenge')
            if code==401 or '/login' in urlsplit(event.get('url','')).path.lower() or '/login' in urlsplit(event.get('redirect','')).path.lower():categories.add('authentication_required')
            if isinstance(code,int) and code>=500:categories.add('upstream_server_error')
            if code in [404,410]:categories.add('broken_or_expired_link')
            if 'Timeout' in str(error) or event.get('error_type')=='TimeoutError':categories.add('timeout')
            if code==200:categories.add('HTML_no_verified_PDF')
        if not categories:categories.add('no_current_file_link')
        ordered=[k for k in labels if k in categories]
        failures.append({'record_id':id,'title':row['完整题名'],'doi':row['DOI（原库不改）'],'main_original_status':row['当前原件状态'],
            'primary_observation_not_unique_cause':ordered[0],'observed_reasons':'；'.join(labels[k] for k in ordered),
            'actual_request_events':sum(not e.get('skipped') for e in ev),
            'source_hosts':'; '.join(sorted({urlsplit(e.get('url','')).hostname or '' for e in ev if e.get('url')})),
            'source_urls_json':json.dumps(list(dict.fromkeys(e['url'] for e in ev if e.get('url'))),ensure_ascii=False),
            'public_fulltext_absence_not_inferred':True})
    r.writecsv(r.RUN/'remaining_main_failure_matrix_utf8.csv',failures)
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
    prior_receipt=r.load(r.RUN/'remote_readback.json',{})
    original_proofs={x['relative_path']:x for x in prior_receipt.get('checks',[])}
    verified_originals=[a for a in mains+si if original_proofs.get(a['source_repo_path'],{}).get('backed_up') and original_proofs[a['source_repo_path']]['sha256']==a['sha256']]
    unbacked_originals=[a['source_repo_path'] for a in mains+si if a not in verified_originals]
    report={'time_utc':r.now(),'restored_remote_baseline':baseline,
        'current_main_ids':len({a['record_id'] for a in mains}),'current_main_files':len(mains),'current_main_bytes':sum(int(a['size_bytes']) for a in mains),
        'current_official_supplementary_files':len(si),'current_official_supplementary_bytes':sum(int(a['size_bytes']) for a in si),
        'newly_acquired_roles':dict(collections.Counter(a['role'] for a in new)),
        'newly_acquired_main_ids':len({a['record_id'] for a in new if a['role']=='main'}),
        'newly_acquired_main_files':sum(a['role']=='main' for a in new),
        'reacquired_historical_main_ids':sorted({a['record_id'] for a in new if a['role']=='main' and a['record_id'] in historical_ids}),
        'reacquired_historical_main_files':sum(a['role']=='main' and a['record_id'] in historical_ids for a in new),
        'first_obtained_main_ids_this_round':sorted({a['record_id'] for a in mains if a['record_id'] not in historical_ids}),
        'remaining_main_ids':426-len({a['record_id'] for a in mains}),'known_missing_official_attachments':official_missing,
        'remaining_main_primary_observation_counts':dict(collections.Counter(x['primary_observation_not_unique_cause'] for x in failures)),
        'supplementary_record_statuses':dict(collections.Counter(x.get('status','not_checked') for x in si_status.values())),
        'supplementary_unchecked_record_count':len(uncovered)+sum(x.get('status')=='not_checked' for x in si_status.values()),
        'supplementary_missing_check_records_without_attempt':len(uncovered),
        'present_extraction_files':sum(x['availability']=='present_sha_verified' for x in rows),
        'historical_extraction_outputs_not_restored':sum(x['availability']!='present_sha_verified' for x in rows),
        'index_validation':index_report,'original_110_fields_554_records_preserved':True,'manual_original_files_sha_preserved':True,
        'new_topic_search_or_classification':False,'unbacked_counts_require_final_remote_readback':True,
        'verified_main_and_supplementary_files':len(verified_originals),
        'verified_main_and_supplementary_bytes':sum(int(a['size_bytes']) for a in verified_originals),
        'unbacked_acquired_main_and_supplementary_files':unbacked_originals,
        'original_file_proof_commit':prior_receipt.get('remote_commit'),
        'latest_completed_readback_commit':r.load(r.RUN/'remote_readback.json',{}).get('remote_commit')}
    r.save(r.RUN/'delivery_summary.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ['restored_remote_baseline','index_validation']},ensure_ascii=False))

if __name__=='__main__':finalize()
