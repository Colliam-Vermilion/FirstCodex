"""Grouped ENA discovery with full pagination; no per-query top-N truncation."""
import json,time,hashlib
from common import ROOT,dump,now,url,getjson,fetch
BASE='https://www.ebi.ac.uk/ena/portal/api/'
SOURCE='(library_source="METAGENOMIC" OR library_source="METATRANSCRIPTOMIC")'
QUERIES=[
('E01','study_title="*microaer*"'),('E02','study_title="*microox*"'),
('E03','study_title="*oxygen*" AND (study_title="*anaerob*" OR study_title="*methan*" OR study_title="*syntroph*" OR study_title="*ferment*")'),
('E04','study_title="*aerat*" AND (study_title="*digest*" OR study_title="*sludge*" OR study_title="*ferment*")'),
('E05','study_title="*oxygen*" AND (study_title="*sediment*" OR study_title="*soil*" OR study_title="*peat*" OR study_title="*wetland*")'),
('E06','study_title="*redox*" AND (study_title="*sediment*" OR study_title="*soil*" OR study_title="*anaerob*" OR study_title="*methan*")'),
('E07','study_title="*reoxygen*"'),
('E08','study_title="*intermittent*" AND (study_title="*aerat*" OR study_title="*oxygen*")'),
('E09','description="*oxygen exposure*" AND (description="*anaerob*" OR description="*methan*" OR description="*sediment*")'),
('E10','description="*oxygen shock*" OR description="*oxygen pulse*" OR description="*oxygen intrusion*"'),
('E11','study_title="*oxygen stress*" OR description="*oxygen stress*"'),
('E12','description="*redox fluctuat*" OR description="*redox oscillat*"'),
('E13','study_title="*side-stream*aerat*" OR description="*side-stream*aerat*"'),
('E14','study_title="*oxygen*" AND library_source="METATRANSCRIPTOMIC"'),
('E15','study_title="*air*nanobub*" OR study_title="*oxygen*nanobub*"'),
('E16','study_title="*oxygen*" AND study_title="*recover*"')]
FIELDS='study_accession,secondary_study_accession,run_accession,experiment_accession,sample_accession,study_title,experiment_title,sample_alias,scientific_name,library_strategy,library_source,library_layout,base_count,fastq_ftp,fastq_bytes'
def run():
 logs=json.loads((ROOT/'search_log.json').read_text()) if (ROOT/'search_log.json').exists() else [];register={x['accession']:x for x in json.loads((ROOT/'discovered_projects.json').read_text())} if (ROOT/'discovered_projects.json').exists() else {}
 for qid,expr in QUERIES:
  if any(x.get('query_id')==qid and x.get('complete') for x in logs):continue
  query='('+expr+') AND '+SOURCE;event={'query_id':qid,'database':'ENA read_run','query':query,'started_utc':now(),'page_limit':1000,'pages':[],'returned_runs':0,'project_accessions':[],'complete':False};seen=set();off=0
  while True:
   j,m=getjson(url(BASE+'search',result='read_run',query=query,fields=FIELDS,format='json',limit=1000,offset=off),'ENA');event['pages'].append({'offset':off,'status':m.get('status'),'raw_path':m.get('raw_path'),'records':len(j) if isinstance(j,list) else None,'error':m.get('error') or m.get('parse_error')})
   if not isinstance(j,list):event['failure']='API未返回JSON数组';break
   ids={x['run_accession'] for x in j}
   if ids and ids<=seen:event['failure']='分页返回重复，停止避免伪称完整';break
   seen|=ids;event['returned_runs']+=len(j)
   for row in j:
    acc=row['study_accession'];v=register.setdefault(acc,{'accession':acc,'source_queries':[],'study_title':row['study_title'],'run_accessions_discovered':[],'raw_source_paths':[]})
    for field,value in [('source_queries',qid),('run_accessions_discovered',row['run_accession']),('raw_source_paths',m['raw_path'])]:
     if value not in v[field]:v[field].append(value)
   if len(j)<1000:event['complete']=True;break
   off+=1000;time.sleep(1.05)
  event['project_accessions']=sorted({x['accession'] for x in register.values() if qid in x['source_queries']});event['finished_utc']=now();logs=[x for x in logs if x.get('query_id')!=qid]+[event];dump(ROOT/'search_log.json',logs);dump(ROOT/'discovered_projects.json',list(register.values()));print(qid,'runs',event['returned_runs'],'projects',len(event['project_accessions']),'complete',event['complete'],flush=True);time.sleep(1.05)
if __name__=='__main__':run()
