import json,os,hashlib,re,sys,shutil
from pathlib import Path
from urllib.parse import quote
from openpyxl import load_workbook
R=Path('/workspace/FirstCodex');T=R/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer';P=T/'uploads_20261101';G=R/'scientific_guide';sys.path.insert(0,str(T/'scripts'));from render import csvout
read=lambda p:json.load(open(p))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Forward citation metadata deduplicated; never mark these rows as screened.
M=read(T/'literature_master.json');doi=lambda s:re.sub(r'^https?://doi.org/','',s or '',flags=re.I).lower().rstrip('.');fold=lambda s:''.join(c for c in s.lower()if c.isalnum());bydoi={doi(r.get('doi')):r['id']for r in M if r.get('doi')};bytitle={fold(r.get('title','')):r['id']for r in M};queue={}
for f in [P/'raw/Wessel_citing_page1.json',P/'raw/Berg_citing_page1.json']:
 for r in read(f)['results']:
  key=doi(r.get('doi'))or r['id'];match=bydoi.get(doi(r.get('doi')))or bytitle.get(fold(r.get('title')or''));q=queue.setdefault(key,{'openalex_id':r['id'],'doi':doi(r.get('doi')),'title':r.get('title'),'existing_id':match,'source_pages':[],'status':'元数据去重；未读正式摘要','next_action':'先核查累计阅读状态；未读者取完整摘要，按问题人工筛选'});q['source_pages'].append(str(f.relative_to(R)))
dump(P/'forward_citation_unread_queue.json',list(queue.values()));csvout(P/'forward_citation_unread_queue_utf8.csv',list(queue.values()))
N=read(P/'online_screening.json');f=P/'README.md';s=f.read_text()+'\n## 后续补筛文章（与上传文章共用入口）\n\n|ID／文章|当前判断与依据|边界／入口|\n|---|---|---|\n'
for r in N:
 card=P/'evidence'/f"{r['id']}.md";rel=lambda p:quote(os.path.relpath(p,card.parent),safe='/');card.write_text(f"# {r['id']} · {r['title']}\n\n阅读深度：{r['reading_depth']}；{r['scope_decision']}。\n\n{r.get('abstract')or '本次返回无摘要，不能据题名得出机制结论。'}\n\n边界：{r['author_interpretation_and_alternatives']}\n\n[实际响应]({rel(R/r['source_path'])}) · [统一原件与阅读入口](../README.md)\n\n没有取得全文；不得写成方法与图表已核实。\n");s+=f"|{r['id']} · {r['title']}|{r['reading_depth']}|{r['author_interpretation_and_alternatives']} · [证据卡](evidence/{r['id']}.md)|\n"
s+='\n前向引文173条来源行去重为'+str(len(queue))+'个身份，其中'+str(sum(bool(q['existing_id'])for q in queue.values()))+'个匹配本专题累计ID；这是元数据匹配数，不是新增纳入或已筛数。[去重后待筛队列](forward_citation_unread_queue_utf8.csv)。\n';f.write_text(s)
# Preserve all original proposition entries, append current fulltext evidence links.
mapfile=G/'literature_proposition_map.json';rows=read(mapfile)
for e in read(P/'fulltext_evidence.json'):
 for prop,part in [('P1a','Part 1'),('P1c','Part 1'),('P3b','Part 3')]:rows.append({'id':e['id'],'title':e['title'],'doi':e['doi'],'year':e['year'],'part':part,'proposition_id':prop,'finding':e['finding'],'boundary':e['boundary'],'reading_depth':e['reading_depth'],'evidence_card':e['evidence_card'],'mapping_status':'2026-11-01上传全文增补；旧判断保留','source_links':[{'path':e['original_path'],'sha256':e['sha256']}]})
dump(mapfile,rows);csvout(G/'literature_proposition_map_utf8.csv',rows)
wb=load_workbook(G/'scientific_reading_guide.xlsx');name='全部文献—命题';del wb[name];ws=wb.create_sheet(name);keys=list(dict.fromkeys(k for r in rows for k in r));ws.append(keys)
for r in rows:
 vals=[]
 for k in keys:
  v=r.get(k);v=json.dumps(v,ensure_ascii=False)if isinstance(v,(dict,list))else v
  if isinstance(v,str):v=re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]','',v);v=v if len(v)<32767 else '完整字段见JSON'
  vals.append(v)
 ws.append(vals)
ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions;wb.save(G/'scientific_reading_guide.xlsx')
z=read(G/'summary.json');z['upload_update_20261101']=read(P/'checkpoint.json');z['upload_update_20261101'].update(forward_unique_unread=len(queue),new_fulltext_proposition_rows=27);dump(G/'summary.json',z)
for name in ['validate.py','complete_assets.py','docs.py','download_new.py']:
 shutil.copy(Path('/workspace/oxygen-spatial-20261101')/name,P/'scripts'/name)
# Remove a redundant conditional assertion in the saved documentation helper.
f=P/'scripts/docs.py';s=f.read_text().replace('import re,json,os','import re,json,os,hashlib').replace("assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256'] if False else True","assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256']");f.write_text(s)
print('forward_unique',len(queue),'existing topical matches',sum(bool(q['existing_id'])for q in queue.values()))
