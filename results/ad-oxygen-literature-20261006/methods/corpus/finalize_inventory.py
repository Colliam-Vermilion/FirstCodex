"""Join extraction provenance into the inventory; publish only three permissive examples."""
from pathlib import Path
from collections import Counter
import argparse,json,csv,shutil,re,hashlib,xml.etree.ElementTree as ET
from audit_library import dump,sha,write_csv,read_csv
SAMPLES={'R03161','R06325','R09236'}
DATA_HOSTS=re.compile(r'(?:ncbi\.nlm\.nih\.gov|ebi\.ac\.uk|zenodo\.org|figshare\.com|datadryad\.org|osf\.io|github\.com|gitlab\.com|data\.[A-Za-z0-9.-]+)',re.I)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--root',type=Path,required=True);args=ap.parse_args();p=args.project.resolve();root=args.root.resolve()
    assets=json.loads((p/'inventory/assets.json').read_text());summary=json.loads((root/'extraction_summary.json').read_text());reports={r['asset_id']:r for r in summary['all_reports']};files=[]
    for a in assets:
        r=reports[a['asset_id']];a['parsing_status']=r['status'];a['extraction']={'relative_directory':'papers/'+a['record_id']+'/extracted/'+a['asset_id'],'search_chunks':r.get('search_chunks',0),'tables':r['table_count'],'ocr_pages':r['ocr_pages'],'ocr_pending_pages':r['ocr_pending_pages'],'full_output_is_not_yet_cloud_backup':True,'sample_repo_directory':''}
        pages=Path(r['output_directory'])/'pages.jsonl'
        r['ocr_no_additional_text_pages']=[]
        if pages.exists():
            for line in pages.read_text().splitlines():
                page=json.loads(line)
                if page['text_method']=='ocr_no_additional_text':r['ocr_no_additional_text_pages'].append(page['pdf_page'])
        for f in sorted(Path(r['output_directory']).rglob('*')):
            if not f.is_file():continue
            rel=f.relative_to(root).as_posix();publish=a['record_id'] in SAMPLES and a['role'] in ['main','supplementary','derived']
            if publish:
                if a['storage_status']!='git_remote_verified':raise ValueError('Sample asset lacks existing permissive Git original')
                dest=p/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest);a['extraction']['sample_repo_directory']=a['extraction']['relative_directory']
            files.append({'record_id':a['record_id'],'asset_id':a['asset_id'],'relative_path':rel,'source_sha256':a['sha256'],'size_bytes':f.stat().st_size,'sha256':sha(f),'artifact_kind':'extracted','published_sample':publish,'current_local_path':str(f),'storage_status':'git_pending_commit' if publish else 'local_only_not_backed_up'})
    # Real external-data links: inspect the already identity-verified XMLs, own data/code
    # availability sections only. References and another article's datasets are excluded.
    external=[];xmlrecords=json.loads((p/'methods/audit/current_pmc_supplementary_pass_20261015.json').read_text())['records']
    for id,record in xmlrecords.items():
        xmlpath=Path(record.get('xml_path') or '/nonexistent')
        if not record.get('identity',{}).get('verified') or not xmlpath.is_file():continue
        if sha(xmlpath)!=record.get('xml_sha256'):raise ValueError('XML evidence changed: '+id)
        doc=ET.parse(xmlpath).getroot()
        for section in doc.iter():
            title=' '.join(''.join(e.itertext()) for e in section.findall('title'))
            sec_type=section.attrib.get('sec-type','')
            if not re.search(r'data.availability|availability.of.data|data.and.material|data.access|code.availability',title+' '+sec_type,re.I):continue
            text=' '.join(''.join(section.itertext()).split());urls=[]
            for link in section.iter():
                url=link.attrib.get('{http://www.w3.org/1999/xlink}href','')
                if url.startswith(('https://','http://')) and DATA_HOSTS.search(url):urls.append(url)
            urls += [u for u in re.findall(r'https?://[^\s<>]+',text) if DATA_HOSTS.search(u)]
            accessions=sorted(set(re.findall(r'\b(?:PRJNA\d+|PRJEB\d+|SRP\d+|SRA\d+|GSE\d+|E-MTAB-\d+)\b',text)))
            for url in dict.fromkeys(urls):external.append({'record_id':id,'url':url.rstrip('.,);'),'type':'external_sequencing_data' if re.search(r'ncbi|ebi',url,re.I) else 'external_data_or_code_repository','accessions':accessions,'size_bytes':None,'size_status':'not_supplied_in_source_section','download_status':'external_data_link_recorded_not_downloaded','auto_download':False,'source_xml_sha256':record['xml_sha256'],'source_location':'JATS section: '+(title or sec_type),'evidence_excerpt':text[:1200]})
            if accessions and not urls:external.append({'record_id':id,'url':'','type':'external_sequencing_accession','accessions':accessions,'size_bytes':None,'size_status':'not_supplied','download_status':'accession_recorded_not_downloaded','auto_download':False,'source_xml_sha256':record['xml_sha256'],'source_location':'JATS section: '+(title or sec_type),'evidence_excerpt':text[:1200]})
    unique={(x['record_id'],x['url'],tuple(x['accessions'])):x for x in external};external=list(unique.values())
    previous_check=p/'inventory/external_data_link_check.json'
    if previous_check.exists():
        check=json.loads(previous_check.read_text())
        for row in external:
            if 'PRJNA1013451' in row['accessions'] and check.get('identity_verified'):row.update(url=check['url'],url_provenance=check['url_construction'],link_access_check=check,type='external_sequencing_data')
    dump(p/'inventory/external_data_links.json',external)
    dump(p/'inventory/assets.json',assets);write_csv(p/'inventory/assets_utf8.csv',assets)
    for f in (p/'papers').glob('*/metadata.json'):
        meta=json.loads(f.read_text());meta['assets']=[a for a in assets if a['record_id']==meta['record_id']];meta['external_data_links']=[x for x in external if x['record_id']==meta['record_id']];meta['preferred_main_asset_id']=next((a['asset_id'] for a in meta['assets'] if a['role']=='main' and a.get('preferred_for_record',True)),None);meta['source_mapping_standard']='logical papers paths map to original_files or private canonical originals; no extra original directory';dump(f,meta)
    dump(p/'inventory/extracted_files.json',files);write_csv(p/'inventory/extracted_files_utf8.csv',files)
    summary['ocr_no_additional_text_pages']=sum(len(r['ocr_no_additional_text_pages']) for r in reports.values());summary['all_reports']=list(reports.values());summary['sample_record_ids']=sorted(SAMPLES);summary['sample_extracted_files']=sum(f['published_sample'] for f in files);summary['sample_extracted_bytes']=sum(f['size_bytes'] for f in files if f['published_sample']);summary['external_data_link_records']=len(external)
    dump(p/'inventory/extraction_summary.json',summary)
    # New Windows queues use the latest 337 missing IDs, not the old 91 history count.
    downloads={r['原记录ID']:r for r in read_csv(p/'manual_review/scansci_download_status_utf8.csv')};history={r['原记录ID']:r for r in read_csv(p/'methods/audit/scansci_verified_pdf_manifest_utf8.csv')};papers=read_csv(p/'inventory/papers_utf8.csv');recordqueue=[];urlqueue=[];siqueue=[]
    for paper in papers:
        id=paper['record_id'];meta=json.loads((p/f'papers/{id}/metadata.json').read_text())
        if not meta['included_for_download']:continue
        d=downloads[id]
        siqueue.append({'record_id':id,'doi':meta['doi'],'title':meta['title'],'current_status':meta['supplementary_status'],'official_files_current':meta['supplementary_official_count'],'publisher_url':d['官方文章/仓储入口'],'check_publisher':True,'check_repository':True,'all_formats':True,'explicit_none_requires_evidence':True,'external_data_auto_download':False})
        if meta['main_status']=='downloaded_verified':continue
        actual=d['实际PDF来源URL（下载或历史记录明确）'];candidates=json.loads(d['公开PDF候选URL（非下载URL绑定实录）'] or '[]');urls=[]
        for url in ([actual] if actual else [])+candidates:
            if not isinstance(url,str) or not url.startswith(('http://','https://')):continue
            if re.search(r'catalog|mediapack|price.list|brochure|author.guidelines',url,re.I):continue
            if url.startswith('http://'):url='https://'+url[7:]
            if url not in urls:urls.append(url)
        recordqueue.append({'record_id':id,'title':meta['title'],'doi':meta['doi'],'category_unchanged':meta['category_unchanged'],'queue':'historical_current_absent9' if id in history else 'previously_unobtained328','historical_sha256':history.get(id,{}).get('SHA256',''),'source_urls':json.dumps(urls,ensure_ascii=False),'official_page':d['官方文章/仓储入口'],'local_main_directory':f'papers/{id}/main','status':'not_downloaded','identity_and_version_review_required':True})
        for url in urls:
            # Known PDF candidates only; landing pages stay in the manual record queue.
            if not re.search(r'\.pdf(?:$|[?#])|/pdf(?:/|$|[?#])|/accepted_manuscript/|/servlets/purl/',url,re.I):continue
            urlqueue.append({'record_id':id,'role':'main','url':url,'filename':history.get(id,{}).get('PDF文件名',id+'_main.pdf'),'expected_sha256':history.get(id,{}).get('SHA256',''),'source_binding':'historical_actual_url' if actual and url in [actual,'https://'+actual[7:]] else 'known_candidate_not_yet_identity_verified','external_data':False})
    assert len(recordqueue)==337 and len(siqueue)==426
    write_csv(p/'windows/main_records337_utf8.csv',recordqueue);write_csv(p/'windows/known_pdf_urls_utf8.csv',urlqueue,fields=['record_id','role','url','filename','expected_sha256','source_binding','external_data']);write_csv(p/'windows/supplementary_review426_utf8.csv',siqueue)
    dump(p/'inventory/parser_run_receipt.json',{'files':len(files),'bytes':sum(f['size_bytes'] for f in files),'sample_files':summary['sample_extracted_files'],'sample_bytes':summary['sample_extracted_bytes'],'search_index_bytes':(root/'search.sqlite').stat().st_size,'search_index_chunks':summary['search_chunks'],'pdf_pages_including_SI_and_nonpreferred_copy':summary['pdf_pages'],'preferred_main_pdf_pages':sum(r.get('pdf_pages',0) for aid,r in reports.items() if next(a for a in assets if a['asset_id']==aid)['role']=='main' and next(a for a in assets if a['asset_id']==aid).get('preferred_for_record',True)),'ocr_pages_with_added_text':summary['ocr_pages'],'ocr_no_added_text_pages_require_visual_interpretation':summary['ocr_no_additional_text_pages'],'structured_tables':summary['structured_tables'],'unparsed_asset_ids':[r['asset_id'] for r in reports.values() if r['status']=='retained_not_content_indexed'],'known_pdf_url_queue_rows':len(urlqueue),'remaining_main_ids':337,'SI_review_ids':426,'new_search_or_classification':False})
    print(json.dumps({'assets':len(assets),'extracted_files':len(files),'sample_files':summary['sample_extracted_files'],'sample_bytes':summary['sample_extracted_bytes'],'tables':summary['structured_tables'],'external_data_links':len(external),'main_queue':len(recordqueue),'SI_queue':len(siqueue),'known_pdf_urls':len(urlqueue)},ensure_ascii=False))


if __name__=='__main__':main()
