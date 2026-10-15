"""Refresh current local queues after an ID/SHA merge; dated baseline queues remain."""
from pathlib import Path
import json,argparse
from audit_library import read_csv,write_csv


def refresh(project):
    p=Path(project);base=p/'windows/main_records337_utf8.csv'
    if not base.exists():return
    records=read_csv(base);remaining=[]
    for r in records:
        meta=json.loads((p/'papers'/r['record_id']/'metadata.json').read_text())
        if meta['included_for_download'] and meta['main_status']!='downloaded_verified':remaining.append(r)
    ids={r['record_id'] for r in remaining};urls=[r for r in read_csv(p/'windows/known_pdf_urls_utf8.csv') if r['record_id'] in ids]
    write_csv(p/'windows/main_records_current_utf8.csv',remaining,fields=list(records[0]))
    write_csv(p/'windows/known_pdf_urls_current_utf8.csv',urls,fields=list(read_csv(p/'windows/known_pdf_urls_utf8.csv')[0]))
    write_csv(p/'windows/doi_queue_current_utf8.csv',[r for r in remaining if r['doi']],fields=list(records[0]));write_csv(p/'windows/no_doi_manual_current_utf8.csv',[r for r in remaining if not r['doi']],fields=list(records[0]))
    si=read_csv(p/'windows/supplementary_review426_utf8.csv')
    for r in si:
        meta=json.loads((p/'papers'/r['record_id']/'metadata.json').read_text());r['current_status']=meta['supplementary_status'];r['official_files_current']=meta['supplementary_official_count']
    write_csv(p/'windows/supplementary_review_current_utf8.csv',si)
    with (p/'windows/scansci_mcp_requests_current.jsonl').open('w',encoding='utf-8') as f:
        for r in remaining:
            if r['doi']:f.write(json.dumps({'record_id':r['record_id'],'tool':'scansci_pdf_download','arguments':{'identifier':r['doi'],'output_dir':f'intake/{r["record_id"]}/scansci','strategy':'legal_only','scihub_enabled':False,'use_tor':False,'use_vpnsci':False,'download_si':True,'markdown':False}},ensure_ascii=False)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);refresh(ap.parse_args().project)
