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
  lines+=['TY  - '+('JOUR' if r.get('journal') and r.get('year') else 'GEN'),'ID  - '+r['id'],'TI  - '+' '.join(r['title'].split())]
  for a in r.get('authors',[]):lines+=['AU  - '+a]
  for k,tag in [('journal','JO'),('year','PY'),('doi','DO'),('abstract','AB')]:
   if r.get(k):lines+=[tag+'  - '+' '.join(str(r[k]).split())]
  if r.get('doi'):lines+=['UR  - https://doi.org/'+r['doi']]
  lines+=['N1  - 专题状态: '+r['status']+'; 阅读深度: '+r.get('reading_depth','未开始'),'ER  -','']
 path.write_text('\n'.join(lines).rstrip()+'\n')
def main():
 previous_reading={r['id']:r['date_recorded_utc'] for r in read(T/'reading_log.json')} if (T/'reading_log.json').exists() else {}
 old={c['id']:c for c in read(M/'catalog.json')};candidates=read(T/'candidate_records.json');C={c['id']:c for c in candidates}
 authors=read(T/'saved_author_sources.json') if (T/'saved_author_sources.json').exists() else {}
 context={
 'ODS-PMID17905889':{'system':'产甲烷厌氧颗粒','methods':'FISH与CH4/H2/pH/ORP微传感器；Deff测量方法待正文','locator':'已保存官方完整摘要；PMID17905889'},
 'OR-06716459121E':{'system':'人工产甲烷—甲烷氧化共培养MBR','substrate':'乙酸26.2 mM；CH4/CO2等混合气供给','temperature':'室温约20°C','reactor_structure':'1.5 L工作体积，150 rpm；沉降/排出选择聚集体','methods':'FISH、主体DO与进出气体浓度；非已核实3D','locator':'Materials and methods/Reactor set-up; Co-cultivation; FISH microscopy；Results/Start-up'},
 'R01414':{'system':'平行AD反应器','substrate':'初级污泥，曾以MgSO4提高硫负荷','temperature':'35.0±0.2°C','reactor_structure':'液体50 L，顶空约20 L；底部陶瓷扩散器','methods':'ORP反馈、日气体组成、SCADA；未核实DO','locator':'PDF p2 §2.1–2.2，p3 §2.3–2.4'},
 'R07202':{'system':'产甲烷2 L CSTR','substrate':'象草；OLR1.5升至5.0 g VS/L/d','reactor_structure':'间歇ORP相对基线微曝气；非颗粒空间分布测量','methods':'宏基因组重建＋ORP控制，未给本轮已核实局部DO','locator':'PDF p2 §2.1'},
 'R03161':{'system':'奶牛粪AD及消化液脱硫单元','substrate':'奶牛粪/消化液及沼气H2S','temperature':'脱硫桶20–25°C；不等同田间全部运行条件','reactor_structure':'65/104 L桶；液面0.099/0.150 m²等；另竖直润湿布','methods':'面积干预、气相O2/H2S/CH4测量、气流与去除率','locator':'PDF p3–4 Methods，p7–8结果与Table1'},
 'OR-6A3D9B1E5D73':{'system':'天然沿岸沉积物完整柱芯','reactor_structure':'保留界面结构，上覆水曝气，分时取样','methods':'氧微剖面＋群落/转录','locator':'Results/Chemical fluxes；原evidence_sources JSON'},
 'OR-8E58C5BBDB53':{'system':'厌氧下水道生物膜','aggregate_or_biofilm_size':'平均厚约800 μm（摘要）','methods':'切片FISH、微电极、模型（摘要）','locator':'完整缓存摘要'},
 'OR-8E15795B9DD4':{'system':'Anammox颗粒，非产甲烷AD','aggregate_or_biofilm_size':'平均直径约5 mm（摘要）','methods':'NH4/NO2/NO3/pH微电极；非O2微剖面','locator':'完整缓存摘要'},
 'ODS-PMID29150508':{'system':'硝酸盐依赖厌氧甲烷氧化富集','aggregate_or_biofilm_size':'古菌细胞约1.5 μm；不是整聚集体直径','methods':'electron tomography、光/电镜、FISH和免疫金（摘要）','locator':'保存的官方完整摘要；正文体重建范围待核'},
 }
 assert set(NOTES)<=set(C),set(NOTES)-set(C)
 rows=[];structure=[];parameters=[];exchange=[];controls=[];needs=[];reading=[]
 for c in candidates:
  rid=c['id'];note=NOTES.get(rid);item=dict(c);item.update(note or {'status':'未开始','scope_decision':'尚未专题判断','reading_depth':'本轮未阅读','decision_reason':None})
  if not item.get('authors') and item.get('pmid') in authors:item['authors']=authors[item['pmid']]['authors'];item['author_metadata_source']=authors[item['pmid']]['source_path']
  if note:
   item.update({k:context.get(rid,{}).get(k) for k in ['system','substrate','temperature','aggregate_or_biofilm_size','reactor_structure','methods','locator']})
   if not item['locator']:item['locator']='完整缓存摘要；具体正文位置尚待核实'
   if not item['system']:item['system']=note['priority_tier']+'（详见actual_finding和decision_reason；具体条件未核字段留空）'
   item['context_not_reported_or_unchecked']='空值表示本轮尚未核实，不能推断原文未报告'
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
  reading.append({'id':rid,'date_recorded_utc':note.get('screened_at_utc') or previous_reading.get(rid) or now(),'last_reading_update_utc':note.get('reading_updated_at_utc'),'basis':note['reading_depth'],'abstract_completeness':note.get('abstract_completeness'),'source_links':c['source_links'],'old_judgment_changed':False,'original_redownloaded':False})
  if not note['reading_depth'].startswith('全文') and note['priority_tier']!='范围外':needs.append({'id':rid,'doi':c.get('doi'),'title':c['title'],'next_action':'补齐正式摘要；缓存已截断需取得原来源' if note.get('screening_stage')=='缓存片段初筛' else '先补读完整缓存摘要' if note['reading_depth'].startswith('仅题名') else '获取/复用相关全文方法与图表，核实参数及具体限制','specific_gap':note['author_interpretation_and_alternatives'],'status':'待摘要' if note['reading_depth'].startswith('仅题名') or note.get('screening_stage')=='缓存片段初筛' else '待全文/补证','source_role':item['source_role']})
 for s in read(T/'seed_audit.json'):
  if not s['assigned_existing_id']:needs.append({'seed_key':s['seed_key'],'doi':s['supplied_doi'],'title':s['supplied_title'],'next_action':'官方元数据核对题名/DOI、全库身份查重、取得正文/附件后再判断','status':'网络403阻断；只有用户提供线索，未独立核实'})
 done=[r for r in rows if r['id'] in NOTES];remaining=[{'order':n+1,'id':r['id'],'title':r['title'],'status':'未开始','next_action':'先题名/摘要专题判断；优先产甲烷结构/传质，非AD方法参照单列'} for n,r in enumerate(rows) if r['id'] not in NOTES]
 for n,r in enumerate(remaining,1):r['order']=n
 abstract_pending=[{'id':r['id'],'title':r['title'],'reason':r['decision_reason'],'status':r['status'],'next_action':'缓存字段本身截断，需要正式来源补齐' if r.get('screening_stage')=='缓存片段初筛' else '读取candidate_records.json同ID完整缓存摘要；不需网络'} for r in rows if (r.get('reading_depth','').startswith('仅题名') or r.get('screening_stage')=='缓存片段初筛') and r.get('priority_tier')!='范围外']
 for name,data in [('literature_master',rows),('structure_localization_evidence',structure),('gas_transfer_parameters',parameters),('cell_interfloc_exchange',exchange),('oxygen_control_evidence',controls),('fulltext_pending',needs),('remaining_queue',remaining),('abstract_pending_queue',abstract_pending),('reading_log',reading)]:dump(T/(name+'.json'),data);csvout(T/(name+'_utf8.csv'),data)
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
 summary={'updated_utc':now(),'candidates':len(rows),'processed':len(done),'remaining':len(remaining),'original_review_ids_reused':sum(r['id'] in old for r in rows),'other_existing_paper_ids_reused':sum(r['id'] not in old for r in rows),'new_external_articles_discovered':0,'new_bibliographic_leads_from_saved_seed_references':len(read(T/'backward_citation_trace.json')),'new_external_queries_completed':0,'local_queries_completed':len(logs),'related_fulltext_or_existing_fulltext_evidence_reused':sum(n['reading_depth'].startswith('全文') for n in NOTES.values()),'abstract_only_processed':sum(not n['reading_depth'].startswith('全文') for n in NOTES.values()),'full_3D_reconstruction_papers_verified':0,'abstract_explicit_electron_tomography_papers':sum(bool((n.get('structure_evidence') or {}).get('three_D_method_reported_in_abstract')) for n in NOTES.values()),'parameter_or_profile_records':len(parameters),'control_records':len(controls),'direct_interfloc_distance_or_flux_measurements_verified':0,'network_state':'proxy_CONNECT_403; saved draft not runtime application','online_status':'必须网络生效后重测并执行，不能把本地遍历当作新外部检索完成','seed_metadata_independently_available_from_saved_sources':1,'seed_metadata_unverified':4}
 dump(T/'summary.json',summary);dump(T/'progress.json',summary|{'completed_ids':list(NOTES),'next_id':remaining[0]['id'] if remaining else None,'resume':'复用raw和已读ID；网络先测官方API成功后再执行online_query_queue；不重复已有主题判断','checkpoint_files':sorted(p.name for p in (T/'checkpoints').glob('*.json'))})
 summary.update(abstract_only_processed=sum(n['reading_depth'].startswith('完整缓存摘要') for n in NOTES.values()),fragment_only_processed=sum(n.get('screening_stage')=='缓存片段初筛' for n in NOTES.values()),title_only_processed=sum(n['reading_depth'].startswith('仅题名') for n in NOTES.values()),abstract_pending_after_title=len(abstract_pending),locally_available_unread_abstract_queue=sum(n.get('screening_stage')=='题名初筛' and n['priority_tier']!='范围外' for n in NOTES.values()),topical_not_prioritized=sum(n['priority_tier']=='范围外' for n in NOTES.values()),local_followup_new_initial_screenings=len(read(T/'followup_screening.json')) if (T/'followup_screening.json').exists() else 0,network_state='current enforced policy excludes all four API hosts; all four minimal requests proxy CONNECT 403; saved draft includes hosts but is not evidence of application')
 dump(T/'summary.json',summary);dump(T/'progress.json',summary|{'completed_ids':list(NOTES),'completed_initial_screen_ids':list(NOTES),'next_id':remaining[0]['id'] if remaining else None,'resume':'优先abstract_pending_queue补摘要，再fulltext_pending补证；网络按raw/preflight/20261030_retest重测，12组在线尚未执行。题名初筛不等于全文核实。','checkpoint_files':sorted(p.name for p in (T/'checkpoints').glob('*.json'))})
 print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
