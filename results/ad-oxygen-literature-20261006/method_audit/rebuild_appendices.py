#!/usr/bin/env python3
"""OFFLINE methods audit. Reads saved records/git history; never searches or screens.

Only methods/ appendices and method_audit/ verification files are written.
It does not invoke any original retrieval/rendering script or change decisions.
"""
import collections,csv,datetime,hashlib,json,re,subprocess
from pathlib import Path
from urllib.parse import urlsplit,parse_qs,urlencode,urlunsplit

P=Path(__file__).resolve().parents[1];M=P/'oxygen_response_review';D=P/'omics_dataset_discovery';A=P/'method_audit'
BASELINE='0f9eeec20bc23a421165c8cff352137ba68fac48'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def csvout(p,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r)) or ['status']
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
def safeurl(u):
 parts=urlsplit(u);params=parse_qs(parts.query,keep_blank_values=True)
 params={k:v for k,v in params.items() if k.lower() not in ['api_key','apikey','access_token','token','email','mailto']}
 return urlunsplit((parts.scheme,parts.netloc,parts.path,urlencode(params,doseq=True),parts.fragment))
def md(x):return str(x if x is not None else '未保存/未知').replace('|','&#124;').replace('\n','<br>')
def link(raw):return f'[{raw}](../{raw})'
def request_rows(root):
 rows=[]
 for name in ['request_log.jsonl','reading_priority/request_log.jsonl']:
  f=root/name
  if not f.exists():continue
  for line in f.read_text().splitlines():
   x=json.loads(line);u=x.get('url_without_contact') or x.get('url') or '';qs=parse_qs(urlsplit(u).query,keep_blank_values=True)
   rows.append({'request_register':name,'query_id_or_name':x.get('query_id') or x.get('name'),'source':x.get('source') or urlsplit(u).netloc,'url_without_credentials_or_contact':safeurl(u),'parameters':{k:v for k,v in qs.items() if k.lower() not in ['api_key','apikey','token','access_token','email','mailto']},'retrieved_or_started_utc':x.get('retrieved_utc') or x.get('queried_utc') or x.get('started_utc'),'finished_utc':x.get('finished_utc'),'status':x.get('status'),'error':x.get('error'),'raw_path':x.get('path') or x.get('raw_path'),'bytes':x.get('bytes')})
 if root==M:
  for x in read(root/'all_pool/metadata_requests.json'):
   rows.append({'request_register':'all_pool/metadata_requests.json','query_id_or_name':'METADATA-DOI-'+str(x['batch']),'source':'OpenAlex DOI metadata (not discovery)','url_without_credentials_or_contact':x['endpoint']+'?'+urlencode(x['params_without_contact']),'parameters':x['params_without_contact'],'retrieved_or_started_utc':datetime.datetime.fromisoformat(x['started_Asia_Shanghai']).astimezone(datetime.timezone.utc).isoformat(),'finished_utc':datetime.datetime.fromisoformat(x['finished_Asia_Shanghai']).astimezone(datetime.timezone.utc).isoformat(),'status':x.get('status'),'error':x.get('error'),'raw_path':x['path'],'bytes':x.get('bytes'),'requested_DOIs':x['dois']})
 csvout(root/'methods/request_register_utf8.csv',rows);return rows
def mech_queries(req):
 rows=[]
 for log in read(M/'search_log.json'):
  qid=log['query_id'];requests=[r for r in req if r['query_id_or_name']==qid];discovery=[r for r in requests if 'esearch' in r['url_without_credentials_or_contact'] or '/works?' in r['url_without_credentials_or_contact']];primary=discovery or requests
  params=primary[0]['parameters'] if primary else {};paths=list(dict.fromkeys(r['raw_path'] for r in requests if r.get('raw_path')))
  row={'query_id':qid,'database':log['database'],'theme':log.get('theme'),'query_verbatim':log.get('query') or log.get('filter') or params.get('id') or '见原始日志','field':log.get('field') or ('明确PMID编号EFetch' if qid=='T01' else 'OpenAlex cites过滤'),'date_utc':log.get('date_utc'),'request_times_as_recorded':[r['retrieved_or_started_utc'] for r in requests],'time_filter':'2012-01-01—2026-10-24' if qid!='T01' else '不设时间过滤；4个指定PMID含3篇2012年前','sort_as_sent':params.get('sort') or '未显式指定；服务端默认，不推定固定排序','page_size_as_sent':params.get('retmax') or params.get('rows') or params.get('per-page'),'pagination':('ESearch retmax=9999一次完整ID；EFetch每100 ID' if qid.startswith('P') else '仅首100；未取下一页' if qid.startswith('C') else '固定4 PMID，无发现分页' if qid=='T01' else 'cursor，per-page=200；3主题有1000脚本上限，实际未触及；F01按日志终止'),'reported_count':log.get('reported_count'),'retrieved_records':log.get('retrieved_records'),'cap_or_termination':log.get('limit'),'unretrieved_reported_tail':log.get('unretrieved_reported_tail'),'query_translation':log.get('query_translation'),'actual_parameters':params,'raw_paths':paths,'request_urls':[r['url_without_credentials_or_contact'] for r in primary],'source_log':'search_log.json'}
  rows.append(row)
 return rows
def dataset_queries(req):
 rows=[]
 for log in read(D/'search_log.json'):
  qid=log['query_id'];urls=[];paths=[];pars=[]
  for page in log.get('pages',[]):
   raw=page.get('raw_path');paths.append(raw)
   if raw and (D/raw).with_suffix('.meta.json').exists():
    meta=read((D/raw).with_suffix('.meta.json'));u=safeurl(meta['url']);urls.append(u);pars.append(parse_qs(urlsplit(u).query,keep_blank_values=True))
  q=(log.get('query') if log.get('query') is not None else '未执行数据库检索；仅GSA入口测试')
  p0=pars[0] if pars else {};isena=qid.startswith('E');isncbi=qid.startswith(('N','P'))
  rows.append({'query_id':qid,'database':log['database'],'theme_or_reason':log.get('reason'),'query_verbatim':q,'field':'ENA read_run: '+('study_title及/或description按实际式；description是brief sequence description，不是完整BioProject摘要' if 'description=' in q else 'study_title，兼有library_source') if isena else ('NCBI PubMed：显式[Title/Abstract]仅P01，其余自动映射' if qid.startswith('P') else 'NCBI BioProject默认检索字段/自动映射' if qid.startswith('N') else '不适用'),'date_utc':str(log.get('started_utc') or '2026-10-24')[:10],'started_utc':log.get('started_utc'),'finished_utc':log.get('finished_utc'),'time_filter':'未发送发表/提交日期过滤','sort_as_sent':p0.get('sort') or '未显式指定；服务端默认','page_size_as_sent':p0.get('limit') or p0.get('retmax'),'pagination':'初轮多数limit=1000/offset=0；E05修复为limit=0全量；现脚本已改，实际参数见各行' if isena else 'ESearch retmax=1000，retstart逐1000；EFetch每100 ID' if isncbi else '未执行','reported_count':log.get('reported_count',log.get('verified_official_count')),'retrieved_records':log.get('returned_runs',log.get('id_count')),'record_unit':'run，可跨查询重复' if isena else 'BioProject记录' if qid.startswith('N') else 'PubMed ID/论文元数据' if qid.startswith('P') else '未查询，不能记0','complete':log.get('complete'),'query_translation':log.get('query_translation'),'warnings':log.get('warninglist'),'interpretation_warning':log.get('interpretation_warning'),'actual_page_parameters':pars,'request_urls':urls,'raw_paths':paths+[x['raw_path'] for x in log.get('fetch_batches',[]) if x.get('raw_path')]+([log['raw_source']] if log.get('raw_source') else []),'superseded_attempt':log.get('superseded_partial_attempt'),'source_log':'search_log.json'})
 return rows
def query_doc(root,rows,scope):
 out=['# 实际查询附表（离线从保存材料复原）','',f'工作线：{scope}。审计基准提交 `{BASELINE}`；本次不调用数据库。机制P06与数据P06是不同命名空间。','', '[详细方法](METHODS.md) · [机器可读CSV](queries_utf8.csv) · [JSON，含自动翻译/警告](queries.json) · [全部实际请求参数/URL](request_register_utf8.csv) · [原查询日志](../search_log.json)','', '下表是原返回，不是去重/纳入数。未显式发送排序或日期参数，不补写理想设置。辅助元数据、全文入口、项目/样本编号核验不冒充新的主题检索；完整调用另见请求表。','', '|ID|数据库|报告总量|实际取回|单位/截断|','|---|---|---:|---:|---|']
 for r in rows:
  unit=r.get('record_unit')
  if root==M:unit='论文元数据；完整ID/EFetch' if r['query_id'].startswith('P') else '论文条目；每组仅首100，尾部未取' if r['query_id'].startswith('C') else '指定PMID元数据，非全面早期检索' if r['query_id']=='T01' else '前向引文，非支持性验证' if r['query_id']=='F01' else 'works；cursor结束，未触上限'
  out.append(f"|[{r['query_id']}](#query-{r['query_id'].lower()})|{r['database']}|{md(r.get('reported_count'))}|{md(r.get('retrieved_records'))}|{md(unit)}|")
 for r in rows:
  out += ['',f"<a id=\"query-{r['query_id'].lower()}\"></a>",f"## {r['query_id']} — {r.get('theme') or r.get('theme_or_reason') or r['database']}",'','完整发送式/编号（不把数据库自动映射当原输入）：','','```text',str(r['query_verbatim']),'```','',f"字段：{r['field']}。日期：{r['date_utc']}。时间过滤：{r['time_filter']}。",'',f"排序：{md(r['sort_as_sent'])}。分页：{r['pagination']}。报告/实际：{md(r.get('reported_count'))} / {md(r.get('retrieved_records'))}。"]
  params=r.get('actual_parameters',r.get('actual_page_parameters'));out += ['', '<details><summary>保存的请求参数（包括实际分页）</summary>','','```json',json.dumps(params,ensure_ascii=False,indent=2),'```','','</details>','']
  if r.get('unretrieved_reported_tail') is not None:out += [f"未取回报告尾部：**{r['unretrieved_reported_tail']}**；没有证据显示后续补齐。",'']
  if r.get('warnings') or r.get('interpretation_warning'):out += ['接口警告/解释边界：', '```json',json.dumps({'warnings':r.get('warnings'),'interpretation':r.get('interpretation_warning')},ensure_ascii=False,indent=2),'```','']
  if r.get('superseded_attempt'):out += ['E05失败尝试：首1000之后offset=1000请求400，旧部分返回保留在原日志superseded_partial_attempt；本行统计只使用修复后的limit=0完整1282。','']
  out += ['原始响应：'+' · '.join(link(p) for p in r['raw_paths'] if p),'']
 out += ['## 辅助调用与复现边界','', '请求附表逐条保留数据库、参数、时间、状态、响应文件；查询当日数据库会更新，重放只能复现方法，不保证未来数量相同。原主题脚本具写入/续跑行为，不应为本次文档审计直接重跑。','']
 if root==M:out += ['首20 DOI指标批量、8篇机制支持PMID及全文入口、全池31批DOI补元数据，均在请求附表并与主题查询分开；不计入1,147。未执行扩展词见[术语记录](../term_expansions.json)，尤其riboflavin、PerR、sigma B和rumen yeast不能称已新增检索。','']
 else:out += ['逐项目SRA精确编号ESearch（retmax=200，每200分页）及EFetch（每100）、ENA filereport、PubMed→SRA ELink/UID ESummary、BioProject Publication反查、3个Assembly编号查询都列于请求附表；它们是编号核验/关联或派生数据核验，不是同一组广泛主题检索。GSA没有实际查询。','']
 (root/'methods/QUERY_APPENDIX.md').write_text('\n'.join(out),encoding='utf-8');dump(root/'methods/queries.json',rows);csvout(root/'methods/queries_utf8.csv',rows)
def sets_and_selection():
 cat=read(M/'catalog.json');inputs=list(csv.DictReader((M/'dedup_input_mapping_utf8.csv').open(encoding='utf-8-sig')));old={r['assigned_id'] for r in inputs if r['query_id']=='OLD554'};returned={r['assigned_id'] for r in inputs if r['query_id']!='OLD554'};allids={r['id'] for r in cat};prior={r['id'] for r in read(M/'all_pool/baseline_screening.json')};new={p.stem for p in (M/'all_pool/decisions').glob('*.json')};rec={r['文献ID'] for r in read(M/'reading_priority/evaluations.json') if r['正式精读推荐']};scope={r['id'] for r in read(M/'all_pool/baseline_screening.json') if r['screening_decision']=='符合本轮核心范围'};dec=read(M/'screening.json')
 sets={n:{r['id'] for r in read(M/f'all_pool/{n}.json')} for n in ['provisional_priorities','pending_confirmation_queue','background_trace_queue','next_stage_queue']};newcore={r['id'] for r in dec if r['id'] in new and r['screening_decision']=='核心候选'};excluded={r['id'] for r in dec if r['screening_decision']=='排除'}
 assert old|returned==allids and len(old)==554 and len(returned)==1039 and len(old&returned)==57
 assert newcore|rec==sets['provisional_priorities'] and not newcore&rec and sets['next_stage_queue']<=newcore
 membership=[]
 for c in cat:
  rid=c['id'];membership.append({'id':rid,'title':' '.join(c['title'].split()),'in_original_554':rid in old,'in_returned_1039':rid in returned,'old_rehit':rid in old&returned,'old_not_rehit_preserved':rid in old-returned,'new_to_old_library':rid in returned-old,'in_first20':rid in prior,'in_first20_scope17':rid in scope,'in_first20_recommended17':rid in rec,'new_347_candidate':rid in newcore,**{'in_'+k:rid in v for k,v in sets.items()},'excluded':rid in excluded,'source_queries':c.get('queries'),'provenance':c.get('provenance')})
 csvout(M/'methods/flow_membership_utf8.csv',membership)
 omitted=allids-(sets['provisional_priorities']|sets['pending_confirmation_queue']|sets['background_trace_queue']|excluded)
 flow={'source_input_rows_including_old':len(inputs),'retrieval_rows':sum(r['query_id']!='OLD554' for r in inputs),'original_ids':len(old),'returned_assigned_ids':len(returned),'intersection_ids':len(old&returned),'new_to_old':len(returned-old),'old_preserved_not_rehit':len(old-returned),'union_catalog':len(allids),'new_core_candidates':len(newcore),'old17_scope_intersection_old17_recommendation':len(scope&rec),'scope17_not_recommended17':sorted(scope-rec),'recommended17_not_scope17':sorted(rec-scope),'priority364':len(sets['provisional_priorities']),'queue35':len(sets['next_stage_queue']),'other_new_candidates':len(newcore-sets['next_stage_queue']),'pending479':len(sets['pending_confirmation_queue']),'background336':len(sets['background_trace_queue']),'excluded356':len(excluded),'one_in_scope_but_held_outside_four_queues':sorted(omitted)}
 dump(M/'methods/set_flow_audit.json',flow)
 projects=read(D/'data_projects_master.json');reg={x['accession']:x for x in read(D/'discovered_projects.json')};ass=read(D/'project_assessments.json');oldproj=set(read(D/'existing_project_links.json'));pids={p['project_id'] for p in projects};assert pids==set(reg)|oldproj|set(ass)
 pmembership=[]
 for p in projects:
  acc=p['project_id'];d=reg.get(acc,{});qs=d.get('source_queries',[]);pmembership.append({'project_id':acc,'existing_9':acc in oldproj,'in_discovery_register':acc in reg,'ENA_query_hit':any(q.startswith('E') for q in qs),'BioProject_query_hit':any(q.startswith('N') for q in qs),'PubMed_SRA_backlink':any('PubMed→SRA' in q for q in qs),'paper_accession_mention':any(q.startswith('paper_accession:') for q in qs),'source_queries':qs,'review_status':p['review_status'],'audit_batch':ass.get(acc,{}).get('audit_batch'),'tier':p['tier'],'availability_code':p['availability_code'],'target_runs_count':p['target_runs_count']})
 csvout(D/'methods/project_pool_membership_utf8.csv',pmembership)
 selected=[]
 for batch in ['D002','D003','D004']:
  for x in read(D/f'batches/{batch}_selection.json'):
   acc=x['accession'];a=ass[acc];d=reg.get(acc,{});p=next(p for p in projects if p['project_id']==acc);selected.append({'batch':batch,'within_batch_order':x['order'],'global_selected_order':len(selected)+1,'project_id':acc,'selection_rationale_as_saved':x['rule'],'source_queries':d.get('source_queries'),'raw_source_paths':d.get('raw_source_paths'),'official_title':p['official_title'],'audit_rationale':a.get('rationale'),'tier':p['tier'],'availability_code':p['availability_code'],'target_runs':p['target_runs_count'],'mapping_status':p['mapping_status']})
 assert len(selected)==60 and len({x['project_id'] for x in selected})==60
 csvout(D/'methods/selected60_provenance_utf8.csv',selected)
 text=['# 新增60项目的实际选择顺序','', '[详细方法](METHODS.md) · [完整字段CSV](selected60_provenance_utf8.csv)','', '这是保存的模型选择顺序及理由，不是引文/JIF排序的前60，不是随机抽样；来源查询可重叠。表中“已审计”不等于满足氧效应统计分析条件。原9个项目另来自旧22篇审计。','', '|顺序|批次|项目|来源查询/关联|处理结论|分组/设计缺口|','|---:|---|---|---|---|---|']
 for x in selected:text.append(f"|{x['global_selected_order']}|{x['batch']}/{x['within_batch_order']}|{x['project_id']}|{md(', '.join(x['source_queries'] or []))}|{md(x['tier'])}；状态{x['availability_code']}；目标run={x['target_runs']}|{md(x['mapping_status'])}|")
 (D/'methods/SELECTION_AUDIT.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
 oldarticles=read(D/'existing_articles_availability_audit.json');oldids={x['paper_id'] for x in oldarticles};olddois={(x.get('doi') or '').lower().strip():x['paper_id'] for x in oldarticles if x.get('doi')};pq=read(D/'remaining_paper_queue.json');overlap=[{'queued_paper_id':x['paper_id'],'queued_PMID':x.get('pmid'),'doi':x.get('doi'),'already_audited_old_id':olddois.get((x.get('doi') or '').lower().strip()) or x['paper_id'],'match_basis':'已有稳定ID及/或规范化DOI匹配；不是重新范围筛选'} for x in pq if x['paper_id'] in oldids or (x.get('doi') or '').lower().strip() in olddois]
 assert len(overlap)==12
 dump(D/'methods/queue_identity_audit.json',{'saved_remaining_queue_rows':len(pq),'already_audited_old22_overlap':overlap,'overlap_count':len(overlap),'rows_after_removing_only_this_verified_overlap':len(pq)-len(overlap),'status':'本次只文档审计，未改写原队列/筛选；后续续跑应按ID/DOI/PMID联合去重','cause':'原22审计行未携带PMID，finalize_outputs按PMID过滤关联总表，未排除这些已审计旧文'})
 csvout(D/'methods/already_audited_queue_overlap_utf8.csv',overlap)
 ep=[]
 for line in (M/'request_log.jsonl').read_text().splitlines():
  x=json.loads(line)
  if 'europepmc' in x.get('url_without_contact','') and x.get('status')==200:
   import xml.etree.ElementTree as ET
   ep.append({'query_id':x['query_id'],'path':x['path'],'HTTP_status':200,'body_present':ET.fromstring((M/x['path']).read_bytes()).find('.//body') is not None,'retrieved_utc':x['retrieved_utc']})
 dump(M/'methods/source_summary_discrepancy.json',{'old_source_summary':'source_availability.json记载EuropePMC正文预检500；对应失败请求详情未单列保留，不能重建全部预检过程','subsequent_saved_successes':ep,'evidence_register_uses':'source_document_register.json选择NCBI PMC JATS或旧PDF；EuropePMC三个版本不重复计文献/阅读量','new_requests_in_this_audit':0})
 return flow,{'total_projects':len(projects),'discovery_register':len(reg),'old_projects_not_in_discovery_register':sorted(oldproj-set(reg)),'pool_union_verified':True,'selected_new_projects':len(selected),'remaining_projects':len(read(D/'remaining_project_queue.json')),'saved_remaining_paper_queue':len(pq),'already_audited_old22_still_queued':len(overlap)}
def history():
 rows=[]
 for work,commits,filename in [('oxygen_response_review',['374049c50','f9fdd267a','fd1601371','22374f2e4','d8e4ee595'],'summary.json'),('omics_dataset_discovery',['fd8dc67b0','99b5d68d9','288f246bc','ce5d9e1cb','57bb4237e'],'summary.json')]:
  for sha in commits:
   data=json.loads(subprocess.check_output(['git','show',sha+':'+str((P/work/filename).relative_to(P.parents[1]))],cwd=P.parents[1],text=True))
   desc=subprocess.check_output(['git','show','-s','--format=%H%n%cI%n%s',sha],cwd=P.parents[1],text=True).splitlines();rows.append({'workstream':work,'commit':desc[0],'committed_at':desc[1],'subject':desc[2],'summary_as_saved':data})
 dump(A/'stage_history.json',rows)
def main():
 if not M.exists():
  raise SystemExit("机制综述已迁移；不要在原分支运行双线历史重建器。使用branch_migration中的只读核验，综述方法到新分支维护。")
 for r in [M,D]:(r/'methods').mkdir(exist_ok=True)
 protected=A/'protected_sources.json'
 if not protected.exists():
  fs=[p for r in [M,D] for p in r.rglob('*') if p.is_file() and 'methods' not in p.relative_to(r).parts and '__pycache__' not in p.parts and p.suffix not in ['.md','.pyc','.pdf']]
  dump(protected,{'baseline_commit':BASELINE,'scope':'既有两条工作线除Markdown/PDF/新methods目录/解释器缓存外的所有文件；本轮不改结果、不重下原件','files':[{'path':str(p.relative_to(P)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(fs)]})
 for r in [M,D]:
  req=request_rows(r);rows=mech_queries(req) if r==M else dataset_queries(req);query_doc(r,rows,'厌氧氧响应机制' if r==M else 'MG/MT数据集发现')
 f,p=sets_and_selection();history();dump(A/'audit_summary.json',{'baseline_commit':BASELINE,'mechanism_sets':f,'dataset_pool':p,'new_database_queries':0,'new_screening_decisions':0,'source':'现存文件/本地Git对象；本脚本无网络请求'})
 for x in read(protected)['files']:assert hashlib.sha256((P/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
 print(json.dumps({'mechanism_sets':f,'dataset_pool':p,'protected_result_files':len(read(protected)['files'])},ensure_ascii=False))
if __name__=='__main__':main()
