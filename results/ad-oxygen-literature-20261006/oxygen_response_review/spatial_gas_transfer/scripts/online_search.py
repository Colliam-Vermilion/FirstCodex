#!/usr/bin/env python3
"""Resume queued official-API discovery after runtime network access is applied.

--list-only never calls the network. --run preserves complete response pages and
logs. CONNECT403 stops the affected host; no alternate route bypasses policy.
This runner has not been online-validated while the runtime rejects API hosts.
"""
import argparse,datetime,hashlib,json,os,time,urllib.error,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
from prepare import T,read,dump,now,SEEDS
class Blocked(Exception):pass
blocked=set();requests=[]
def get(base,params,source,name):
 host=urllib.parse.urlsplit(base).hostname
 if host in blocked:raise Blocked(host+' paused after prior denial')
 public={k:v for k,v in params.items() if k not in ['email','mailto','api_key','apikey','token']}
 key=hashlib.sha256((base+'?'+urllib.parse.urlencode(public)).encode()).hexdigest()[:20]
 suffix='.xml' if params.get('retmode')=='xml' else '.json'
 dest=T/'raw/online'/source/(name+'_'+key+suffix);meta=dest.with_suffix('.request.json')
 if dest.exists() and meta.exists() and read(meta).get('status')==200:return dest.read_bytes(),str(dest.relative_to(T))
 dest.parent.mkdir(parents=True,exist_ok=True)
 row={'source':source,'name':name,'endpoint':base,'parameters_without_contact':public,'started_utc':now(),'status':None,'raw_path':str(dest.relative_to(T))}
 url=base+('?' if params else '')+urllib.parse.urlencode(params)
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'SpatialGasTransferReview/1.0','Accept':'application/json,application/xml'}),timeout=40) as response:
   body=response.read();row.update(status=response.status,content_type=response.headers.get('content-type'))
  dest.write_bytes(body);row.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
 except urllib.error.HTTPError as exc:
  error_body=exc.read();error_path=dest.with_suffix('.error.body');error_path.write_bytes(error_body)
  row.update(status=exc.code,error_class=type(exc).__name__,error_body_path=str(error_path.relative_to(T)),error_body_sha256=hashlib.sha256(error_body).hexdigest())
  if exc.code in [401,403,429]:blocked.add(host)
  if exc.code==429:row['retry_after_as_sent']=exc.headers.get('Retry-After')
  raise Blocked(str(row)) from exc
 except urllib.error.URLError as exc:
  row.update(error_class=type(exc).__name__,error=str(exc))
  if '403' in str(exc):blocked.add(host)
  raise Blocked(str(exc)) from exc
 finally:
  row['finished_utc']=now();dump(meta,row);requests.append(row)
  with (T/'online_request_log.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
 time.sleep(.4 if source=='PubMed' else .5)
 return body,str(dest.relative_to(T))
def main():
 pa=argparse.ArgumentParser(description=__doc__);pa.add_argument('--list-only',action='store_true');pa.add_argument('--run',action='store_true');args=pa.parse_args()
 queue=read(T/'online_query_queue.json')
 if not args.run:print(json.dumps({'queued_queries':len(queue),'seed_DOIs':len(SEEDS),'network_calls':0,'instruction':'先在环境设置应用/发布网络，--run执行后才能认定查询有实际结果；非在线验证通过'},ensure_ascii=False));return
 email=os.environ.get('NATURE_CONTACT_EMAIL') or os.environ.get('PUBMED_EMAIL')
 cfg=Path('/workspace/tools/nature-runtime/config/contact.json')
 if not email and cfg.exists():email=read(cfg).get('contact_email')
 logs=[];eutils='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
 # Each exact DOI response is authoritative metadata, not a topical search.
 works=[]
 for sid,d,title in SEEDS:
  try:
   body,path=get('https://api.crossref.org/works/'+urllib.parse.quote(d,safe='/'),{},'Crossref',sid)
   work=json.loads(body)['message'];works.append({'seed_key':sid,'work':work,'raw_path':path})
  except (Blocked,KeyError,ValueError) as exc:logs.append({'query_id':sid,'database':'Crossref DOI','status':'failed_or_paused','error':str(exc)})
 dump(T/'seed_crossref_results.json',works)
 for q in queue:
  qid=q['query_id'];log={'query_id':qid,'database':q['database'],'query_verbatim':q['query_verbatim'],'started_utc':now(),'pages':[],'status':'started','retrieved_records':0}
  try:
   if q['database']=='PubMed':
    params={'db':'pubmed','term':q['query_verbatim'],'retmode':'json','retmax':0,'tool':'SpatialGasTransferReview'}
    if email:params['email']=email
    b,path=get(eutils+'esearch.fcgi',params,'PubMed',qid+'_count');count=int(json.loads(b)['esearchresult']['count']);log['reported_count']=count;log['count_path']=path
    log['date_filter']='不设起始年；原始返回完整保存，正式/在线出版日需逐条核对，未来日期不得直接纳入执行日范围'
    if count>9999:
     log.update(status='needs_query_split',reason='PubMed ESearch >9999; split by publication-year blocks and retain pre-2012 interval before marking complete');logs.append(log);continue
    ids=[]
    for start in range(0,count,1000):
     p=params|{'retmax':1000,'retstart':start};b,path=get(eutils+'esearch.fcgi',p,'PubMed',qid+'_IDs_'+str(start));result=json.loads(b)['esearchresult']['idlist'];ids+=result;log['pages'].append({'retstart':start,'records':len(result),'raw_path':path})
    assert len(ids)==len(set(ids))==count
    for start in range(0,len(ids),100):
     p={'db':'pubmed','id':','.join(ids[start:start+100]),'retmode':'xml','tool':'SpatialGasTransferReview'}
     if email:p['email']=email
     b,path=get(eutils+'efetch.fcgi',p,'PubMed',qid+'_fetch_'+str(start));n=len(ET.fromstring(b).findall('.//PubmedArticle'));log.setdefault('fetches',[]).append({'raw_path':path,'article_records':n});log['retrieved_records']+=n
    log['complete_id_list']=True;log['status']='completed' if log['retrieved_records']==count else 'partial_fetch_needs_resolution'
   else:
    cursor='*';seen=set();end=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()
    while cursor:
     p={'search':q['query_verbatim'],'filter':'to_publication_date:'+end,'per-page':200,'cursor':cursor}
     if email:p['mailto']=email
     b,path=get('https://api.openalex.org/works',p,'OpenAlex',qid+'_page_'+str(len(log['pages'])));data=json.loads(b);items=data.get('results',[]);log['reported_count']=data.get('meta',{}).get('count');log['pages'].append({'cursor_as_sent':cursor,'raw_path':path,'records':len(items)});log['retrieved_records']+=len(items)
     nxt=data.get('meta',{}).get('next_cursor')
     if not items or not nxt:break
     if nxt in seen:raise ValueError('repeated cursor; not complete')
     seen.add(nxt);cursor=nxt
    log['status']='completed'
  except (Blocked,ValueError,KeyError,ET.ParseError) as exc:log.update(status='failed_or_partial',error=str(exc))
  log['finished_utc']=now();logs.append(log);dump(T/'online_search_log.json',logs)
 # Citation tracing is a separate namespace, not extra topical query hits.
 traces=[]
 for sid,d,st in SEEDS:
  try:
   p={}
   if email:p['mailto']=email
   b,path=get('https://api.openalex.org/works/https://doi.org/'+urllib.parse.quote(d,safe='/'),p,'OpenAlex',sid+'_identity')
   work=json.loads(b);wid=work['id'].rstrip('/').split('/')[-1]
   traces.append({'seed_key':sid,'direction':'backward','source_work_id':wid,'raw_identity_path':path,'referenced_works_complete_as_returned':work.get('referenced_works',[]),'status':'reference identifiers retrieved; not evidence support or article screening'})
   cursor='*';pages=[];count=0;seen=set()
   while cursor:
    p={'filter':'cites:'+wid+',to_publication_date:'+datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat(),'per-page':200,'cursor':cursor}
    if email:p['mailto']=email
    b,path=get('https://api.openalex.org/works',p,'OpenAlex',sid+'_citing_'+str(len(pages)));data=json.loads(b);items=data.get('results',[]);pages.append({'raw_path':path,'cursor':cursor,'records':len(items)});count+=len(items);nxt=data.get('meta',{}).get('next_cursor')
    if not items or not nxt:break
    if nxt in seen:raise ValueError('repeated citation cursor, incomplete')
    seen.add(nxt);cursor=nxt
   traces.append({'seed_key':sid,'direction':'forward','pages':pages,'retrieved_records':count,'status':'complete discovery pages; citations are not independent mechanistic verification'})
  except (Blocked,KeyError,ValueError) as exc:traces.append({'seed_key':sid,'direction':'online tracing','status':'failed_or_paused','error':str(exc)})
  dump(T/'online_citation_trace_log.json',traces)
 # Never change the local search_log.json or declare screening completed here.
 dump(T/'online_search_log.json',logs)
 print(json.dumps({'queries_with_logs':len(logs),'completed':[l['query_id'] for l in logs if l.get('status')=='completed'],'paused_hosts':sorted(blocked),'next_action':'先解析完整返回、与现有全库身份去重，再逐篇判断；不要用接口返回覆盖人工判断'},ensure_ascii=False))
if __name__=='__main__':main()
