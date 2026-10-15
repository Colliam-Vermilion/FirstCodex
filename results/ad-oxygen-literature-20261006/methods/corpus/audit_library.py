"""Audit real bytes and map the existing original_files tree without moving originals."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, subprocess, re, argparse


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()


def read_csv(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def write_csv(path,rows,fields=None):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rows)


def dump(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.tmp');temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(path)


def safe_name(s):
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',s).rstrip('. ')[:180] or 'file'


def audit(project):
    p=Path(project).resolve();out=p/'inventory';out.mkdir(exist_ok=True)
    merged=out/'last_return_merge.json'
    if merged.exists() and (json.loads(merged.read_text()).get('new_assets') or json.loads(merged.read_text()).get('merged_SI_reviews')):raise RuntimeError('Imported current assets exist; use verify_inventory.py, do not rebuild from old snapshot tables')
    master=read_csv(p/'final_results/ad_oxygen_download_review_utf8.csv')
    body=read_csv(p/'methods/audit/current_local_verified_body_files_utf8.csv')
    si=read_csv(p/'methods/audit/current_supplementary_files_manifest_utf8.csv')
    history=read_csv(p/'methods/audit/scansci_verified_pdf_manifest_utf8.csv')
    durable=read_csv(p/'methods/audit/current_original_files_manifest_utf8.csv')
    assets=[];by_id={r['稳定记录ID']:r for r in master}
    def add(r,role,pathkey):
        id=r['原记录ID'];digest=r['SHA256'];repo=r['Git持久原件路径'];local=Path(r[pathkey]);candidates=[p/repo] if repo else []
        candidates.append(local);existing=[x for x in candidates if x.is_file()]
        for f in existing:
            if sha(f)!=digest or f.stat().st_size!=int(r['字节数']):raise ValueError('Actual bytes disagree: '+id+' '+str(f))
        source=existing[0] if existing else None;official=role=='supplementary';filename=Path(r[pathkey]).name
        logical_folder={'main':'main','supplementary':'supplementary','derived':'supplementary/derived'}[role]
        # Keep the original name in metadata; logical names carry SHA to avoid Windows collisions.
        canonical=f'papers/{id}/{logical_folder}/{digest[:12]}_{safe_name(filename)}'
        a={'preferred_for_record':role=='main','record_id':id,'asset_id':id+'.'+role+'.'+digest[:16],'role':role,'official_attachment':official,
           'original_filename':filename,'canonical_path':canonical,'source_repo_path':repo,'source_local_path':str(local),
           'resolved_source_path':str(source) if source else '', 'format':Path(filename).suffix.lower().lstrip('.'),
           'size_bytes':int(r['字节数']),'sha256':digest,'availability':'present_sha_verified' if source else 'missing_current_bytes',
           'storage_status':'git_remote_verified' if repo and source else 'local_only_not_backed_up' if source else 'missing',
           'source_url':r.get('实际来源') or r.get('实际附件下载URL',''),'source_xml_url':r.get('归属XML',''),
           'version':r.get('版本','original_supplementary_attachment' if official else 'extracted_archive_member'),
           'license_evidence':r.get('共享许可状态') or r.get('许可',''),'historical_sha256':r.get('历史SHA256',''),
           'archive_parent_asset_id':'','parsing_status':'not_started'}
        assets.append(a)
    for r in body:add(r,'main','文件路径（本机不是下载链接）')
    for r in si:add(r,'supplementary' if r['独立附件是否计数']=='是' else 'derived','当前路径（本机不是下载链接）')
    # Auxiliary source originals are audited separately from main PDFs and official SI.
    pmc_sources=json.loads((p/'methods/audit/current_pmc_supplementary_pass_20261015.json').read_text())['records']
    # The pilot R09236 transport was reused by the later PMC pass and is recorded
    # in its own earlier audit, not in the later record's transport_bundle field.
    pilot=json.loads((p/'methods/audit/environment_recovery_pilot_identity_si_b_20261015.json').read_text())
    def find_pilot_transport(v):
        if isinstance(v,dict):
            if v.get('record_id')=='R09236' and v.get('status')==200 and v.get('path') and str(v.get('artifact_role','')).startswith('repository_generated_transport_bundle'):
                pmc_sources['R09236']['transport_bundle']={'path':v['path'],'sha256':v['sha256'],'bytes':v['bytes']}
            for child in v.values():find_pilot_transport(child)
        elif isinstance(v,list):
            for child in v:find_pilot_transport(child)
    find_pilot_transport(pilot)
    for id,record in pmc_sources.items():
        for role,pathstr,digest,size in [
            ('evidence_xml',record.get('xml_path'),record.get('xml_sha256'),None),
            ('transport_archive',record.get('transport_bundle',{}).get('path'),record.get('transport_bundle',{}).get('sha256'),record.get('transport_bundle',{}).get('bytes'))]:
            source=Path(pathstr or '/nonexistent')
            if not source.is_file():continue
            if sha(source)!=digest:raise ValueError('Auxiliary evidence SHA changed: '+id)
            if role=='evidence_xml' and not record.get('identity',{}).get('verified'):raise ValueError('Unverified XML source')
            canonical=f'papers/{id}/evidence/{digest[:12]}_{safe_name(source.name)}'
            assets.append({'record_id':id,'asset_id':id+'.'+role+'.'+digest[:16],'role':role,'official_attachment':False,
                'original_filename':source.name,'canonical_path':canonical,'source_repo_path':'','source_local_path':str(source),'resolved_source_path':str(source),
                'format':source.suffix.lower().lstrip('.'),'size_bytes':source.stat().st_size,'sha256':digest,'availability':'present_sha_verified',
                'storage_status':'local_only_not_backed_up','source_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/'+record['pmc']+('/fullTextXML' if role=='evidence_xml' else '/supplementaryFiles'),
                'source_xml_url':'','version':'repository_JATS_fulltext_representation_not_PDF' if role=='evidence_xml' else 'repository_generated_transport_not_official_SI',
                'license_evidence':record.get('license',{}).get('statement',''),'historical_sha256':'','archive_parent_asset_id':'','parsing_status':'not_started',
                'identity_basis':'prior exact article title/DOI/authors XML validation; current source SHA rechecked'})
    reviewed_alternates=json.loads((p/'methods/audit/current_alternate_bytes_manual_validation_20261015.json').read_text()).get('records',{})
    for id,r in reviewed_alternates.items():
        source=Path(r.get('candidate_path') or '/nonexistent')
        if not r.get('manual_identity_version_verified') or not source.is_file() or sha(source)!=r.get('sha256'):continue
        if any(a['record_id']==id and a['sha256']==r['sha256'] for a in assets):continue
        assets.append({'record_id':id,'asset_id':id+'.main.'+r['sha256'][:16],'role':'main','preferred_for_record':False,'official_attachment':False,
            'original_filename':source.name,'canonical_path':f'papers/{id}/main/{r["sha256"][:12]}_{safe_name(source.name)}',
            'source_repo_path':'','source_local_path':str(source),'resolved_source_path':str(source),'format':'pdf','size_bytes':source.stat().st_size,'sha256':r['sha256'],
            'availability':'present_sha_verified','storage_status':'local_only_not_backed_up','source_url':r.get('source_url',''),'source_xml_url':'','version':r['version'],
            'license_evidence':r.get('license',{}).get('name',''),'historical_sha256':r.get('historical_sha256_preserved',''),'archive_parent_asset_id':'','parsing_status':'not_started',
            'identity_basis':'prior manual identity/all-page/version review; nonpreferred bytes retained, not an additional article'})
    # Bind archive derivatives to actual CRC-checked parent bytes, never by filename alone.
    import zipfile
    for a in assets:
        if a['role']!='derived' or not a['resolved_source_path']:continue
        for parent in assets:
            if parent['record_id']!=a['record_id'] or parent['format']!='zip' or not parent['resolved_source_path']:continue
            with zipfile.ZipFile(parent['resolved_source_path']) as z:
                for member in z.infolist():
                    if not member.is_dir() and member.file_size==a['size_bytes'] and hashlib.sha256(z.read(member)).hexdigest()==a['sha256']:
                        a['archive_parent_asset_id']=parent['asset_id'];a['archive_member_path']=member.filename
        if not a['archive_parent_asset_id']:raise ValueError('Unbound derivative '+a['asset_id'])
    hist={r['原记录ID']:r for r in history};current={r['record_id']:r for r in assets if r['role']=='main' and r.get('preferred_for_record',True) and r['availability']=='present_sha_verified'}
    exact=[id for id,r in hist.items() if id in current and current[id]['sha256']==r['SHA256']]
    alternate=[id for id,r in hist.items() if id in current and current[id]['sha256']!=r['SHA256']]
    missing=[id for id in hist if id not in current];new=[id for id in current if id not in hist]
    pmc=json.loads((p/'methods/audit/current_pmc_supplementary_pass_20261015.json').read_text())['records']
    oldsi={r['原记录ID']:r for r in read_csv(p/'manual_review/supplementary_material_status_utf8.csv')}
    ownlinks=Path('/workspace/pdf_supplementary_mentions_current.json')
    # Retain previously reviewed own-paper evidence if present; no new scope search.
    own_evidence=json.loads(ownlinks.read_text()) if ownlinks.is_file() else {}
    dump(out/'previous_pdf_SI_scan_evidence.json',own_evidence)
    papers=[];external=[]
    for row in master:
        id=row['稳定记录ID'];group=[a for a in assets if a['record_id']==id];included=str(row['最终分类']).strip().split()[0] in ['1','2','3','4']
        rec=pmc.get(id,{});attachments=[a for a in group if a['official_attachment']]
        si_status='downloaded_partial' if attachments else 'not_checked'
        evidence=[]
        if rec:
            evidence.append({'source':'previous PMC article XML check','status':rec.get('status'),'xml_sha256':rec.get('xml_sha256'),'local_asset_declarations':len(rec.get('declared_local_attachments',[]))})
            if not attachments:si_status='checked_repository_no_declared_local_assets' if rec.get('identity',{}).get('verified') else 'access_failed'
            for link in rec.get('external_supplement_links',[]):
                external.append({'record_id':id,'type':'external_supplement_link_not_yet_classified','url':link.get('declared_href',''),'size_bytes':None,'auto_download':False,'evidence':link})
        if id=='R13833':si_status='access_failed';evidence.append({'source':'explicit ACS DOCX URL from own PDF','status':'HTTP403_challenge'})
        entry={'record_id':id,'title':row['完整题名'],'authors':row['作者'],'doi':row['DOI'],'category_unchanged':row['最终分类'],
               'preferred_main_asset_id':current[id]['asset_id'] if id in current else None,'included_for_download':included,'main_status':'downloaded_verified' if id in current else 'not_downloaded' if included else 'excluded_skip',
               'supplementary_status':si_status,'supplementary_coverage_complete':False,'supplementary_official_count':len(attachments),
               'supplementary_previous_detail':oldsi.get(id,{}),'supplementary_evidence':evidence,
               'external_data_links':[x for x in external if x['record_id']==id],
               'logical_directories':{'main':'mapped, originals stay at source_repo_path/source_local_path','supplementary':'mapped, no duplicate originals','extracted':'per-asset derived search artifacts'},
               'assets':group,'version_history':[{'sha256':hist[id]['SHA256'],'status':'historical_same_bytes' if id in exact else 'historical_original_missing','source':'immutable historical91 manifest'}] if id in hist else []}
        if id in current:entry['version_history'].append({'sha256':current[id]['sha256'],'version':current[id]['version'],'status':'current_verified_preferred_bytes'})
        entry['version_history'] += [{'sha256':a['sha256'],'version':a['version'],'status':'additional_verified_nonpreferred_bytes_retained'} for a in group if a['role']=='main' and not a.get('preferred_for_record',True)]
        dump(p/f'papers/{id}/metadata.json',entry)
        papers.append({k:v for k,v in entry.items() if k in ['record_id','title','doi','category_unchanged','included_for_download','main_status','supplementary_status','supplementary_coverage_complete','supplementary_official_count']})
    assert len(papers)==554 and sum(r['included_for_download'] for r in papers)==426
    dump(out/'assets.json',assets);write_csv(out/'assets_utf8.csv',assets)
    write_csv(out/'papers_utf8.csv',papers);dump(out/'external_data_links.json',external)
    pinned=json.loads((p/'methods/audit/current_remote_original_readback_20261015.json').read_text())
    remote_proof_unchanged=all(sha(p/r['相对保存路径'])==r['SHA256'] for r in durable)
    counts={role:{'files':sum(a['role']==role and a['availability']=='present_sha_verified' for a in assets),'bytes':sum(a['size_bytes'] for a in assets if a['role']==role and a['availability']=='present_sha_verified')} for role in ['main','supplementary','derived','evidence_xml','transport_archive']}
    parsed_before=[]
    for folder in [p/'papers',Path('/workspace/library-files/ad-oxygen-corpus/papers')]:
        if folder.exists():parsed_before.extend(f for f in folder.rglob('*') if f.is_file() and 'extracted' in f.parts)
    summary={'baseline_commit':subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD']).decode().strip(),'records':len(master),'included_records':sum(r['included_for_download'] for r in papers),'category_counts_1to6':[sum(str(r['category_unchanged']).split()[0]==str(i) for r in papers) for i in range(1,7)],'current':counts,'historical91_count':len(hist),'historical_exact_current':len(exact),'historical_alternate_ids':alternate,'historical_current_absent_ids':missing,'historical_original_bytes_missing':len(hist)-len(exact),'new_current_ids':new,'current_missing_body':sum(r['included_for_download'] and r['main_status']!='downloaded_verified' for r in papers),'git_original_files':len(durable),'git_original_bytes':sum(int(r['字节数']) for r in durable),'previous_remote_readback_commit':pinned['remote_commit'],'previous_remote_readback_reused_after_all54_hash_checks':remote_proof_unchanged and pinned['all_original_bytes_readback_verified'],'preferred_main_records':len(current),'additional_verified_main_variants':sum(a['role']=='main' and not a.get('preferred_for_record',True) for a in assets),'core_research_file_objects':sum(a['role'] in ['main','supplementary','derived'] and (a['role']!='main' or a.get('preferred_for_record',True)) for a in assets),'auxiliary_source_objects':sum(a['role'] in ['evidence_xml','transport_archive'] for a in assets),'XML_only_ids_still_require_PDF':[a['record_id'] for a in assets if a['role']=='evidence_xml' and a['record_id'] not in current],'original_assets_unique_sha':len(set(a['sha256'] for a in assets)),'original_assets_total_bytes':sum(a['size_bytes'] for a in assets),'new_pipeline_extracted_files_at_audit_start':len(parsed_before),'new_pipeline_extracted_bytes_at_audit_start':sum(f.stat().st_size for f in parsed_before),'no_originals_moved_or_removed':True,'scope_and_manual_judgments_modified':False,'external_links_currently_classified':len(external)}
    dump(out/'current_file_audit.json',summary);print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);args=ap.parse_args();audit(args.project)
