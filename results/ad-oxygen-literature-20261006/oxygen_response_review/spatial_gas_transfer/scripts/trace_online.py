"""Complete first-generation seed citation retrieval with supported numbered pages."""
import json,urllib.parse
from online_search import get,blocked
from prepare import T,read,dump,now
logs=[]
for seed in read(T/'seed_audit.json'):
 sid=seed['seed_key'];blocked.clear()
 try:
  b,path=get('https://api.openalex.org/works/https://doi.org/'+urllib.parse.quote(seed['supplied_doi'],safe='/'),{},'OpenAlex',sid+'_identity')
  work=json.loads(b);wid=work['id'].split('/')[-1];refs=work.get('referenced_works',[])
  row={'seed_key':sid,'direction':'backward','identity_path':path,'source_work_id':wid,'reference_ids':refs,'reported_count':len(refs),'pages':[],'retrieved_records':0}
  for start in range(0,len(refs),50):
   b,path=get('https://api.openalex.org/works',{'filter':'openalex:'+'|'.join(x.split('/')[-1] for x in refs[start:start+50]),'per-page':200},'OpenAlex',sid+'_references_'+str(start))
   d=json.loads(b);row['pages'].append({'raw_path':path,'records':len(d['results'])});row['retrieved_records']+=len(d['results'])
  row['status']='completed' if row['retrieved_records']==len(refs) else 'identifier_resolution_gap';logs.append(row);dump(T/'online_citation_trace_log.json',logs)
  row={'seed_key':sid,'direction':'forward','source_work_id':wid,'pages':[],'retrieved_records':0}
  page=1
  while True:
   b,path=get('https://api.openalex.org/works',{'filter':'cites:'+wid+',to_publication_date:2026-10-30','per-page':200,'page':page},'OpenAlex',sid+'_citing_numbered_'+str(page))
   d=json.loads(b);items=d['results'];row['reported_count']=d['meta']['count'];row['pages'].append({'page':page,'raw_path':path,'records':len(items)});row['retrieved_records']+=len(items)
   if not items or page*200>=row['reported_count']:break
   if page>=50:raise ValueError('10,000 basic paging limit reached; must split before completion')
   page+=1
  row['status']='completed';logs.append(row)
 except Exception as e:logs.append({'seed_key':sid,'direction':'online tracing','status':'failed_or_partial','error':str(e)})
 dump(T/'online_citation_trace_log.json',logs);print(sid,[(x['direction'],x.get('retrieved_records'),x['status']) for x in logs if x['seed_key']==sid],flush=True)
