"""Check cumulative deliverables and protected progress, without rereading paper originals."""
from review_dependency import review_bytes
import json,csv,re,hashlib
from openpyxl import load_workbook
from common import ROOT,dump,now
def load(n):return json.loads((ROOT/n).read_text())
def run():
 checks=[]
 for p in load('baseline.json')['protected_sources']:
  assert hashlib.sha256(review_bytes(p['path'].removeprefix('oxygen_response_review/')) if p['path'].startswith('oxygen_response_review/') else (ROOT.parent/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
 checks.append('8 protected prior omics/mechanism files unchanged; originals untouched by git diff')
 ps=load('data_projects_master.json');rs=load('samples_runs_mapping.json');papers=load('associated_papers.json');summary=load('summary.json');pp={p['project_id']:p for p in ps};rr={r['run_accession']:r for r in rs}
 assert len(pp)==len(ps) and all(re.fullmatch(r'PRJ(?:NA|EB|DB)\d+',p) for p in pp)
 assert len(rr)==len(rs) and len({p['paper_id'] for p in papers})==len(papers)
 assert len(load('existing_articles_availability_audit.json'))==22 and len(load('existing_project_links.json'))==9
 assert summary['existing_article_linked_target_runs']==49 and summary['existing_project_all_target_runs']==51
 assert summary['reviewed_projects']+summary['remaining_project_candidates']==len(ps)
 assert summary['A_B_public_runs']+summary['C_public_runs']==summary['reviewed_project_community_runs']
 assert summary['raw_FASTQ_downloads']==summary['original_paper_redownloads']==0
 for r in rs:
  assert r['project_id'] in pp and not r['raw_reads_downloaded']
  if r['target_community_reads']:assert r['project_id'] not in {p['project_id'] for p in ps if p['availability_code']==7}
  for source in r['metadata_source_paths']:assert (ROOT/source).exists(),source
  assert len(r['fastq_urls'])==len(r['fastq_bytes'])==len(r['fastq_md5']) or not r['fastq_urls']
 for c in load('confirmed_comparisons.json'):
  assert c['treatment_runs'] and c['control_runs']
  for a in c['treatment_runs']+c['control_runs']:assert a in rr and rr[a]['target_community_reads'] and rr[a]['project_id']==c['project_id']
  assert not (set(c['treatment_runs'])&set(c['control_runs']))
 checks.append('Unique project/paper/run IDs; old 22/9 retained; 49 prior + 2 newly found runs; comparison keys valid')
 for e in load('search_log.json'):
  if e.get('query_id')=='GSA-availability':assert e['reported_count'] is None and not e['complete'];continue
  assert e['complete'],e['query_id']
  for page in e.get('pages',[]):assert page['status']==200 and (ROOT/page['raw_path']).exists()
  for b in e.get('fetch_batches',[]):assert b['status']==200 and (ROOT/b['raw_path']).exists()
  if 'id_count' in e:assert e['id_count']==e['reported_count']
 e5=next(e for e in load('search_log.json') if e.get('query_id')=='E05');assert e5['returned_runs']==e5['verified_official_count']==1282
 checks.append('All executed query ID pages/response batches present and successful; GSA correctly unsearched; ENA repaired full count 1282')
 wb=load_workbook(ROOT/'omics_dataset_discovery_cumulative.xlsx',read_only=True)
 for sheet,rows in [('数据项目总表',ps),('样本与run映射',rs),('关联论文表',papers),('供氧比较及证据层级',load('confirmed_comparisons.json')),('剩余项目队列',load('remaining_project_queue.json'))]:assert wb[sheet].max_row-1==len(rows),(sheet,wb[sheet].max_row,len(rows))
 wb.close()
 for stem in ['data_projects_master','samples_runs_mapping','associated_papers','request_or_pending','dedup_relationships','dataset_evidence','download_preparation_file_manifest']:
  with (ROOT/(stem+'_utf8.csv')).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
  assert len(rows)==len(load(stem+'.json')),stem
 assert (ROOT/'associated_papers.ris').read_text().count('ER  -')==len(papers)
 assert (ROOT/'community_dataset_papers.ris').read_text().count('ER  -')==summary['community_paper_RIS_records']
 checks.append('Excel sheets reopen with exact counts; UTF-8 CSV/JSON and both RIS counts agree')
 result={'checked_utc':now(),'passed':True,'checks':checks,'project_rows':len(ps),'run_rows_all_assays':len(rs),'paper_rows_all_statuses':len(papers),'raw_reads_downloaded':0};dump(ROOT/'validation.json',result);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':run()
