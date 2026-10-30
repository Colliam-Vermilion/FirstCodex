#!/usr/bin/env python3
"""Build editorial tables and verbatim evidence cards from existing files only.

No network, no scope screening, no writes under the original review directory.
The prose annotations are in curate_records.py. README prose is edited separately.
"""
import csv,datetime,hashlib,json,re,sys
from pathlib import Path
from openpyxl import Workbook
from curate_records import ARTICLES

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'scientific_guide'
P=ROOT/'results/ad-oxygen-literature-20261006'
M=P/'oxygen_response_review'
BASE='3966c96f48f3194a4e27fc9ada0837f009345f35'
PROPOSITIONS={
 'P1a':('Part 1','投氧量、气相比例、DO和ORP能否说明每个细胞的实际暴露？','把输入、实测浓度和空间传递分开，不跨单位直接换算。'),
 'P1b':('Part 1','同样接触氧，暴露时长、重复次数和历史会改变结果吗？','急性、持续微氧、间歇和去氧恢复分别比较，不找一个通用阈值。'),
 'P2a':('Part 2','厌氧细胞受损是分子氧直接作用，还是ROS造成的？','区分分子氧、超氧、H2O2及铁化学途径；靶点依菌株而异。'),
 'P2b':('Part 2','耗氧与解毒系统各解决什么问题，付出什么代价？','离体活性、遗传必要性和群落净效应是不同证据。'),
 'P2c':('Part 2','受损细胞可以修复、暂停生长或调整代谢吗？','分开蛋白修复、生理调节与已证明的遗传适应。'),
 'P3a':('Part 3','哪些成员增加、减少或替代，天然群落是否反应一致？','相对丰度、绝对量、存活和活性不能互换。'),
 'P3b':('Part 3','颗粒、生物膜与聚集是否真的形成缺氧保护区？','直接氧微剖面与形态/组成推断分开。'),
 'P4a':('Part 4','耗氧伙伴在保护厌氧过程，还是竞争底物和产物？','互作需干预或通量支持，共现和净变化不能唯一确定机制。'),
 'P4b':('Part 4','氧如何重分配碳、电子及最终产物？','去除率、基因/转录、代谢物净量和定量通量分开。'),
 'P4c':('Part 4','去氧后哪些功能恢复，组成与功能是否同时恢复？','恢复时间依功能、损伤、底物与群落历史，不能给出跨体系统一时标。'),
}
TAG_MAP={
 'M1':('细胞损伤',['Part 2']), 'M2':('清除氧/氧化物',['Part 2']),
 'M3':('能量与碳代谢',['Part 2','Part 4']), 'M4':('群落互作',['Part 4']),
 'M5':('空间保护',['Part 1','Part 3']), 'M6':('恢复与适应',['Part 2','Part 3','Part 4']),
 'M7':('促进/抑制的条件',['Part 1','Part 4']),
}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def csvout(p,rows):
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,keys,lineterminator='\n');w.writeheader()
  for row in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else '\n'.join(t.rstrip() for t in v.splitlines()).rstrip() if isinstance(v,str) else v for k,v in row.items()})
def md(s):return str(s if s is not None else '').replace('|','&#124;').replace('\n','<br>')
def local(path):return '../../'+path.relative_to(ROOT).as_posix()

def main():
 OUT.mkdir(exist_ok=True);(OUT/'evidence').mkdir(exist_ok=True)
 cat=load(M/'catalog.json');C={c['id']:c for c in cat};S={s['id']:s for s in load(M/'screening.json')};E={e['id']:e for e in load(M/'mechanism_evidence.json')};meta={m['id']:m for m in load(M/'all_pool/metadata_enrichment.json')}
 # Only these cached全文 sections were rechecked for this guide. The two legacy
 # PDF papers and membrane coculture rely on existing extracts, not new通读.
 full_read={'OR-C8E113321FD5':['Molecular oxygen itself inactivates PFOR.','How is pyruvate dissimilation restored'],
 'OR-7C60AA03CC08':['Effect of oxygen on growth and methane production','Generation of air-adapted'],
 'OR-30A5634DFFB8':['Experimental Setup','Impact of Oxygen','Recovery'],
 'OR-3035DF955A54':['Incubations','Transient O2 exposure','O2 directs microbial'],
 'OR-6A3D9B1E5D73':['Incubation of sediment cores','Chemical fluxes','Identification of 16S'],
 'OR-5DA7260E019E':['Description of sample site','Sediment community cell extraction','Active anaerobic lineages']}
 articles=[];relations=[];readlog=[];natural=[]
 for editorial in ARTICLES:
  rid=editorial['id'];c=C[rid];s=S[rid];e=E.get(rid);a=dict(editorial)
  assert c.get('doi'),rid
  authors=c.get('authors') or []
  first=authors[0].split(',')[0] if authors else '作者待核对'
  label=first+('等' if len(authors)>1 else '')+'，'+str(c.get('year','年份待核'))
  abstract=meta[rid].get('abstract_enriched') or c.get('abstract') or ''
  assert abstract.strip(),rid
  if rid in full_read:
   depth='已核实相关全文段落；本轮重核指定方法/结果，非全文通读'
   new_read='本轮定向重核仓库已存全文方法/结果段落'
  elif e and e.get('screening_stage')=='全文核实':
   depth='已核实相关全文段落；本轮复用既有提取证据，非重新通读'
   new_read='本轮复核既有全文提取记录并阅读缓存摘要；未重新阅读原件'
  else:
   depth='仅依据完整缓存摘要；相关全文方法/结果尚待核实'
   new_read='本轮阅读既有完整缓存摘要；没有新增全文核实'
  a.update(title=c['title'],authors=authors,author_year=label,year=c.get('year'),journal=c.get('journal'),doi=c['doi'],official_url='https://doi.org/'+c['doi'],reading_depth=depth,source_queries=c.get('queries',[]),prior_screening_decision=s.get('screening_decision'),prior_reading_depth=s.get('reading_level'),prior_mechanism_labels=c.get('mechanism_themes',[]),evidence_card='scientific_guide/evidence/'+rid+'.md',source_provenance=c.get('provenance',[]))
  if e:
   a.update(existing_evidence_id=e.get('evidence_id'),existing_source_file=e.get('source_file'),existing_quote=e.get('quote'),existing_quote_location=e.get('quote_location'))
  quotes=[]
  if rid in full_read:
   source=load(M/'evidence_sources'/f'{rid}.json')
   for p in source['paragraphs']:
    if p.get('element_type') not in ['p','page']:continue
    if any(t.lower() in p.get('section','').lower() for t in full_read[rid]) and '/body' in p['locator']:
     if len(quotes)<8:quotes.append({'section':p.get('section'),'locator':p['locator'],'verbatim':p['text']})
   # The explicit chemical-penetration paragraph must be included in the card.
   if rid=='OR-6A3D9B1E5D73':
    required=next(p for p in source['paragraphs'] if 'oxygen penetration depth in the sediment' in p['text'].lower())
    if not any(q['locator']==required['locator'] for q in quotes):quotes.append({'section':required['section'],'locator':required['locator'],'verbatim':required['text']})
  if e and e.get('quote') and not any(q.get('locator')==e.get('quote_location') for q in quotes):quotes.append({'section':e.get('quote_section'),'locator':e.get('quote_location'),'verbatim':e['quote']})
  a['selected_verbatim_evidence']=quotes
  out=[f'# {label} — {a["short_title_zh"]}','',c['title'],'',f'文献ID：`{rid}`。DOI：[ {c["doi"]} ](https://doi.org/{c["doi"]})。','',f'**阅读状态：{depth}。** 原筛选判断保持：{s.get("screening_decision")}；本页是新增科学说明，不是重新筛选。','',f'对象：{a["study_object"]}。氧处理：{a["oxygen_treatment"]}。','',f'目前可支持：{a["finding"]}','',f'限制：{a["boundary"]}','',f'与AD联系：{a["AD_connection"]}','',f'命题：{", ".join(a["propositions"])}；[科学首页](../../README.md) · [完整对应表](../literature_proposition_map_utf8.csv)','', '## 已有来源及本轮阅读','',new_read+'。所有材料均在本轮开始前已保存；没有联网获取新全文或开展新检索。','',f'- [缓存完整摘要]({local(M/"all_pool/metadata_enrichment.json")})，定位`[id={rid}]/abstract_enriched`；[原书目与来源]({local(M/"catalog.json")})，定位`[id={rid}]`。']
  if e:
   out += [f'- [原证据记录]({local(M/"mechanism_evidence.json")})，定位`{e.get("evidence_id")}`；[段落／页码定位]({local(M/"evidence_sources"/(rid+".json"))})。']
   sf=M/e['source_file']
   assert sf.exists(),sf
   out += [f'- [实际保存的原文／原来源文件]({local(sf.resolve())})。已保存不等于已通读；阅读深度见上。']
  out+=['','## 完整缓存摘要（原文）','','> '+abstract.replace('\n','\n> ')]
  if quotes:
   out+=['','## 支持说明的原文片段及位置','']
   for q in quotes:out += [f'### {q.get("section") or "摘要/原证据"}','','位置：`'+str(q.get('locator'))+'`','','> '+q['verbatim'].replace('\n','\n> '),'']
  rendered='\n'.join(t.rstrip() for t in '\n'.join(out).splitlines()).rstrip()+'\n'
  (OUT/'evidence'/f'{rid}.md').write_text(rendered)
  readlog.append({'id':rid,'author_year':label,'date_Asia_Shanghai':'2026-10-29','action':new_read,'source_paths':(['results/ad-oxygen-literature-20261006/oxygen_response_review/evidence_sources/'+rid+'.json'] if e else [])+['results/ad-oxygen-literature-20261006/oxygen_response_review/all_pool/metadata_enrichment.json'],'sections_rechecked':full_read.get(rid,[]),'new_network_fulltext_fetch':False,'original_scope_or_priority_changed':False,'reading_state_for_homepage':depth})
  for prop in a['propositions']:
   assert prop in PROPOSITIONS
   part,question,rule=PROPOSITIONS[prop]
   role='在所列对象和条件下支持/限定命题；不代表普遍规律'
   if rid in ['OR-83A7A70A485C','OR-A8CEEF69FB67','OR-631665AE20A2']:role='反例或阴性/条件证据，反对不加限定的普遍推论'
   if rid in ['OR-9AE95458315B','OR-8E58C5BBDB53','OR-3AD765670E11','OR-E8FFBEA256B0','OR-30C473F441F1','OR-BA5AE666B938','OR-49562AF42977']:role='背景/间接证据；不单独验证氧进入的因果机制'
   if rid=='R07202':role='基因功能潜力支持的作者解释；非活性或因果互作证明'
   if rid=='OR-1925EF467A30' and prop=='P3b':role='作者的空间保护解释；仅摘要不能确认直接氧分布测量'
   relations.append({k:a[k] for k in ['id','author_year','title','year','journal','doi','study_object','oxygen_treatment','finding','boundary','AD_connection','reading_depth','prior_screening_decision','prior_reading_depth','prior_mechanism_labels','evidence_card','source_queries']}|{'part':part,'proposition_id':prop,'proposition_question':question,'support_role':role,'mapping_status':'本轮逐项整理的科学说明；不改变原筛选','evidence_rule':rule,'missing_evidence':a['boundary'],'verbatim_locations':[q.get('locator') for q in quotes] if quotes else ['all_pool/metadata_enrichment.json [id='+rid+']/abstract_enriched'],'existing_evidence_id':a.get('existing_evidence_id'),'existing_quote_as_saved':a.get('existing_quote'),'existing_quote_locator':a.get('existing_quote_location')})
  if a.get('natural'):
   design,env,scope=a['natural'];natural.append({k:a[k] for k in ['id','author_year','title','doi','oxygen_treatment','finding','boundary','reading_depth','evidence_card','source_queries','prior_screening_decision']}|{'study_design':design,'environment':env,'directness_and_scope':scope})
  articles.append(a)
 # Full coverage without manufacturing article-level claims for unread records.
 fullmap=list(relations);mapped={a['id'] for a in articles}
 for c in cat:
  if c['id'] in mapped:continue
  s=S[c['id']];tags=c.get('mechanism_themes',[]) or []
  parts=sorted({p for t in tags for k,(_,ps) in TAG_MAP.items() if str(t).startswith(k) for p in ps})
  fullmap.append({'id':c['id'],'title':c['title'],'year':c.get('year'),'journal':c.get('journal'),'doi':c.get('doi'),'prior_screening_decision':s.get('screening_decision'),'prior_reading_depth':s.get('reading_level'),'prior_mechanism_labels':tags,'part':parts,'proposition_id':None,'mapping_status':'仅保留旧标签到四部分的导航；未逐项建立科学命题，不作为本轮结论证据','reading_depth':'本轮未新增阅读；原状态见prior_reading_depth'})
 csvout(OUT/'literature_proposition_map_utf8.csv',fullmap);dump(OUT/'literature_proposition_map.json',fullmap)
 csvout(OUT/'discussed_evidence_links_utf8.csv',relations);dump(OUT/'discussed_articles.json',articles)
 csvout(OUT/'natural_communities_utf8.csv',natural);dump(OUT/'natural_communities.json',natural)
 csvout(OUT/'reading_log_20261029_utf8.csv',readlog);dump(OUT/'reading_log_20261029.json',readlog)
 props=[dict(proposition_id=k,part=v[0],question=v[1],evidence_rule=v[2]) for k,v in PROPOSITIONS.items()]
 dump(OUT/'propositions.json',props);csvout(OUT/'propositions_utf8.csv',props)
 tagrows=[{'original_tag':k,'original_topic':v[0],'new_parts':v[1],'rule':'概念导航，一篇可多部分；不重写旧分类或逐篇证据判断'} for k,v in TAG_MAP.items()]
 csvout(OUT/'seven_to_four_mapping_utf8.csv',tagrows)
 logs=load(M/'search_log.json');coverage=[]
 for term in ['sediment','peat','wetland','flooded soil','reoxygenation','oxygen exposure','redox fluctuation']:
  # Literal concept words, not substrings: "peat" is not "repeated".
  pattern=re.compile(r'(?<![A-Za-z])'+re.escape(term)+r'(?![A-Za-z])',re.I)
  qs=[q for q in logs if pattern.search(str(q.get('query') or q.get('filter') or ''))]
  qids={q['query_id'] for q in qs};matches=[a for a in articles if set(a['source_queries'])&qids and a.get('natural')]
  coverage.append({'term':term,'executed_query_ids':sorted(qids),'executed_queries':[{k:q.get(k) for k in ['query_id','database','query','filter','date_utc','reported_count','retrieved_records']} for q in qs],'matching_discussed_natural_records':[a['id'] for a in matches],'read_status':'命中来源按组合查询记录，不表示能将OR组合的返回归给单独关键词；仅所列证据卡所示材料已阅读','coverage_gap':'未在本轮新增检索；Crossref C03只取前100，天然体系覆盖未保证穷尽；根系供氧/生物扰动/根际/植物输氧未作单独专门查询'})
 dump(OUT/'query_coverage.json',coverage);csvout(OUT/'query_coverage_utf8.csv',coverage)
 wb=Workbook();wb.remove(wb.active)
 for name,rows in [('全部文献—命题',fullmap),('本页逐项证据',relations),('天然群落与边界',natural),('科学命题',props),('七类至四部分',tagrows),('实际查询覆盖',coverage),('本轮补读',readlog)]:
  ws=wb.create_sheet(name);keys=list(dict.fromkeys(k for r in rows for k in r));ws.append(keys)
  for row in rows:
   vals=[json.dumps(row.get(k),ensure_ascii=False) if isinstance(row.get(k),(list,dict)) else row.get(k) for k in keys]
   assert all(not isinstance(v,str) or len(v)<=32767 for v in vals)
   ws.append(vals)
  ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
  for col in ws.columns:ws.column_dimensions[col[0].column_letter].width=min(55,max(16,len(str(col[0].value))+4))
 wb.save(OUT/'scientific_reading_guide.xlsx')
 dump(OUT/'summary.json',{'editorial_baseline_commit':BASE,'date_Asia_Shanghai':'2026-10-29','existing_catalog_records_preserved':len(cat),'articles_discussed':len(articles),'proposition_relations_reviewed_for_guide':len(relations),'catalog_ids_represented_in_full_map':len({r['id'] for r in fullmap}),'full_map_rows':len(fullmap),'other_records_without_new_proposition_judgment':len(cat)-len(articles),'natural_and_boundary_records':len(natural),'cached_fulltext_articles_rechecked_for_guide':len(full_read),'existing_fulltext_extracts_reused_without_new_original_reading':sum(a['id'] in E and a['id'] not in full_read and E[a['id']].get('screening_stage')=='全文核实' for a in articles),'network_searches':0,'new_paper_downloads':0,'old_screening_changes':0,'old_priority_or_progress_changes':0,'original_root_README_sha256':hashlib.sha256((ROOT/'technical/root_README_original_20261029.txt').read_bytes()).hexdigest()})
 print(json.dumps(load(OUT/'summary.json'),ensure_ascii=False))
if __name__=='__main__':main()

# Preserve the later spatial-transfer additions when regenerating the first guide.
if __name__=='__main__':
 import runpy,sys
 spatial=ROOT/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/scripts/update_guide.py'
 if spatial.exists():
  sys.path.insert(0,str(spatial.parent))
  runpy.run_path(str(spatial),run_name='__main__')
