"""Render cumulative topical views; never overwrite original scope decisions."""
import csv,json,re,xml.etree.ElementTree as ET
from pathlib import Path
from openpyxl import Workbook
from prepare import T,M,P,R,read,dump,now
from curation import NOTES
def csvout(path,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r)) or ['status']
 with path.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,keys,lineterminator='\n');w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else '\n'.join(t.rstrip() for t in v.splitlines()).rstrip() if isinstance(v,str) else v for k,v in r.items()})
def ris(path,rows):
 lines=[]
 for r in rows:
  lines+=['TY  - JOUR','ID  - '+r['id'],'TI  - '+' '.join(r['title'].split())]
  for a in r.get('authors',[]):lines+=['AU  - '+a]
  for k,tag in [('journal','JO'),('year','PY'),('doi','DO'),('abstract','AB')]:
   if r.get(k):lines+=[tag+'  - '+' '.join(str(r[k]).split())]
  if r.get('doi'):lines+=['UR  - https://doi.org/'+r['doi']]
  lines+=['N1  - 专题状态: '+r['status']+'; 阅读深度: '+r.get('reading_depth','未开始'),'ER  -','']
 path.write_text('\n'.join(lines).rstrip()+'\n')
def main():
 old={c['id']:c for c in read(M/'catalog.json')};candidates=read(T/'candidate_records.json');C={c['id']:c for c in candidates}
 assert set(NOTES)<=set(C),set(NOTES)-set(C)
 rows=[];structure=[];parameters=[];exchange=[];controls=[];needs=[];reading=[]
 for c in candidates:
  rid=c['id'];note=NOTES.get(rid);item=dict(c);item.update(note or {'status':'未开始','scope_decision':'尚未专题判断','reading_depth':'本轮未阅读','decision_reason':None})
  item['old_review_id']=rid if rid in old else None;item['other_existing_id']=rid if rid not in old else None
  item['source_role']='复用机制库' if rid in old else '复用组学关联论文候选；本专题首次处理，不改原数据工作线'
  item['existing_scope_decision_preserved']=old.get(rid,{}).get('screening_decision')
  item['date_issue']='保存年份晚于执行年，待核，不据此确认纳入截至当日研究' if str(c.get('year','')).isdigit() and int(c['year'])>2026 else None
  rows.append(item)
  if not note:continue
  record={'id':rid,'title':c['title'],'doi':c.get('doi'),'reading_depth':note['reading_depth'],'finding':note['actual_finding'],'limits':note['author_interpretation_and_alternatives'],'source_links':c['source_links']}
  if note.get('structure_evidence'):structure.append(record|note['structure_evidence'])
  for param in note['parameters']:parameters.append(record|param)
  if note.get('exchange_evidence'):exchange.append(record|note['exchange_evidence'])
  if note.get('control_evidence'):controls.append(record|note['control_evidence'])
  reading.append({'id':rid,'date_recorded_utc':now(),'basis':note['reading_depth'],'source_links':c['source_links'],'old_judgment_changed':False,'original_redownloaded':False})
  if not note['reading_depth'].startswith('全文'):needs.append({'id':rid,'doi':c.get('doi'),'title':c['title'],'next_action':'获取/复用相关全文方法与图表，核实参数及具体限制','specific_gap':note['author_interpretation_and_alternatives'],'status':'待全文/补证','source_role':item['source_role']})
 for s in read(T/'seed_audit.json'):
  if not s['assigned_existing_id']:needs.append({'seed_key':s['seed_key'],'doi':s['supplied_doi'],'title':s['supplied_title'],'next_action':'官方元数据核对题名/DOI、全库身份查重、取得正文/附件后再判断','status':'网络403阻断；只有用户提供线索，未独立核实'})
 done=[r for r in rows if r['id'] in NOTES];remaining=[{'order':n+1,'id':r['id'],'title':r['title'],'status':'未开始','next_action':'先题名/摘要专题判断；优先产甲烷结构/传质，非AD方法参照单列'} for n,r in enumerate(rows) if r['id'] not in NOTES]
 for n,r in enumerate(remaining,1):r['order']=n
 for name,data in [('literature_master',rows),('structure_localization_evidence',structure),('gas_transfer_parameters',parameters),('cell_interfloc_exchange',exchange),('oxygen_control_evidence',controls),('fulltext_pending',needs),('remaining_queue',remaining),('reading_log',reading)]:dump(T/(name+'.json'),data);csvout(T/(name+'_utf8.csv'),data)
 logs=read(T/'search_log.json');traces=read(T/'backward_citation_trace.json')+read(T/'forward_local_citation_trace.json')
 csvout(T/'search_log_utf8.csv',logs);csvout(T/'citation_trace_utf8.csv',traces);csvout(T/'seed_audit_utf8.csv',read(T/'seed_audit.json'))
 ris(T/'spatial_gas_transfer_candidates.ris',rows);ris(T/'spatial_gas_transfer_reviewed.ris',done)
 wb=Workbook();wb.remove(wb.active)
 for name,data in [('文献与专题筛选',rows),('三维结构与定位',structure),('传质参数及剖面',parameters),('细胞间与絮体间',exchange),('供氧控制',controls),('已执行本地检索',logs),('在线待执行检索',read(T/'online_query_queue.json')),('引用追溯',traces),('种子核对',read(T/'seed_audit.json')),('待全文与疑点',needs),('未处理续跑',remaining)]:
  ws=wb.create_sheet(name);keys=list(dict.fromkeys(k for r in data for k in r)) or ['status'];ws.append(keys)
  for row in data:
   vals=[json.dumps(row.get(k),ensure_ascii=False) if isinstance(row.get(k),(list,dict)) else row.get(k) for k in keys]
   assert all(not isinstance(v,str) or len(v)<=32767 for v in vals)
   ws.append(vals)
  ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
 wb.save(T/'spatial_gas_transfer_cumulative.xlsx')
 summary={'updated_utc':now(),'candidates':len(rows),'processed':len(done),'remaining':len(remaining),'original_review_ids_reused':sum(r['id'] in old for r in rows),'other_existing_paper_ids_reused':sum(r['id'] not in old for r in rows),'new_external_articles_discovered':0,'new_bibliographic_leads_from_saved_seed_references':len(read(T/'backward_citation_trace.json')),'new_external_queries_completed':0,'local_queries_completed':len(logs),'related_fulltext_or_existing_fulltext_evidence_reused':sum(n['reading_depth'].startswith('全文') for n in NOTES.values()),'abstract_only_processed':sum(not n['reading_depth'].startswith('全文') for n in NOTES.values()),'full_3D_reconstruction_papers_verified':0,'parameter_or_profile_records':len(parameters),'control_records':len(controls),'direct_interfloc_distance_or_flux_measurements_verified':0,'network_state':'proxy_CONNECT_403; saved draft not runtime application','online_status':'必须网络生效后重测并执行，不能把本地遍历当作新外部检索完成','seed_metadata_independently_available_from_saved_sources':1,'seed_metadata_unverified':4}
 dump(T/'summary.json',summary);dump(T/'progress.json',summary|{'completed_ids':list(NOTES),'next_id':remaining[0]['id'] if remaining else None,'resume':'复用raw和已读ID；网络先测官方API成功后再执行online_query_queue；不重复已有主题判断','checkpoint_files':sorted(p.name for p in (T/'checkpoints').glob('*.json'))})
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
