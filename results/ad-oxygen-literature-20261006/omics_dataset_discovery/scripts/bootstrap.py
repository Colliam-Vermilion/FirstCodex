from review_dependency import review_bytes
import json,re,hashlib,subprocess
from common import ROOT,dump,now,fetch,url
P=ROOT.parent;OLD=P/'omics_screening'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();targets=[r for r in json.loads((OLD/'screening_records.json').read_text()) if r['conclusion'].startswith('确认宏')];assert len(targets)==22
source_rows=json.loads((OLD/'data_projects_samples.json').read_text());targetids={r['record_id'] for r in targets};evidence=[r for r in json.loads((OLD/'evidence.json').read_text()) if r['record_id'] in targetids];projects={}
for d in source_rows:
 if d['record_id'] in targetids and d.get('target_eligible'):
  key=d.get('dataset_key','');m=re.search(r'PRJ(?:NA|EB|DB)\d+',key)
  if m:projects.setdefault(m[0],[]).append(d)
files=['omics_screening/screening_records.json','omics_screening/data_projects_samples.json','omics_screening/evidence.json','omics_screening/summary.json','oxygen_response_review/all_pool/progress.json','oxygen_response_review/reading_priority/evaluations.json','oxygen_response_review/reading_queue35/source_conditions_audit.json','oxygen_response_review/oxygen_response_review_cumulative.xlsx']
dump(ROOT/'baseline.json',{'source_commit':head,'created_utc':now(),'target_articles':len(targets),'MG':sum(r['conclusion']=='确认宏基因组' for r in targets),'MT':sum(r['conclusion']=='确认宏转录组' for r in targets),'known_project_accessions':sorted(projects),'protected_sources':[{ 'path':s,'sha256':hashlib.sha256(review_bytes(s.removeprefix('oxygen_response_review/')) if s.startswith('oxygen_response_review/') else (P/s).read_bytes()).hexdigest()} for s in files]})
dump(ROOT/'mechanism_review_paused.json',{'status':'按用户指示暂存，不继续机制综述筛选或改写其进度','source_commit':head,'progress_path':'https://github.com/Colliam-Vermilion/FirstCodex/blob/review/oxygen-response-mechanisms/results/ad-oxygen-literature-20261006/oxygen_response_review/all_pool/progress.json','priority_queue_audit':'https://github.com/Colliam-Vermilion/FirstCodex/blob/review/oxygen-response-mechanisms/results/ad-oxygen-literature-20261006/oxygen_response_review/reading_queue35/source_conditions_audit.json','resume_rule':'从原文件续跑；本任务不覆盖原综述成果','new_active_task':'群落宏基因组/宏转录组原始数据发现与关联论文'})
dump(ROOT/'existing_target_articles.json',targets);dump(ROOT/'existing_target_evidence.json',evidence);dump(ROOT/'existing_project_links.json',projects);dump(ROOT/'existing_dataset_rows.json',[r for r in source_rows if r['record_id'] in targetids and r.get('target_eligible')]);print('targets',len(targets),'projects',len(projects),'evidence',len(evidence))
