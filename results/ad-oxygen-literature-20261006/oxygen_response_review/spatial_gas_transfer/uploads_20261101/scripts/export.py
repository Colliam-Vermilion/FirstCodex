import json,csv,os,re,hashlib,sys,shutil
from pathlib import Path
from urllib.parse import quote
from openpyxl import load_workbook
R=Path('/workspace/FirstCodex');T=R/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer';P=T/'uploads_20261101';G=R/'scientific_guide'
sys.path.insert(0,str(T/'scripts'));from render import csvout,ris

def read(p):return json.load(open(p))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fold(s):return ''.join(c for c in s.casefold() if c.isalnum())
def doi(s):return re.sub(r'^https?://(?:dx\.)?doi.org/','',s or '',flags=re.I).strip().lower().rstrip('.')
def link(src,target):return quote(os.path.relpath(target,src.parent),safe='/')
if (P/'checkpoint.json').exists():
 raise SystemExit('Checkpoint already merged; do not duplicate rows. Use existing JSON and a new continuation batch.')
M=read(T/'literature_master.json');B={r['id']:r for r in M};E=read(P/'fulltext_evidence.json');I=read(P/'file_inventory.json');meta={doi(r['doi']):r for r in read(P/'seed_metadata_verification.json')}
for e in E:
 m=meta.get(e['doi'],{});e['authors']=m.get('authors') or (['Hisashi Satoh','Yuki Miura','Ikuo Tsushima','Satoshi Okabe'] if '01426' in e['doi'] else ['Aimee K. Wessel','Talha A. Arshad','Mignon Fitzpatrick','Jodi L. Connell','Roger T. Bonnecaze','Jason B. Shear','Marvin Whiteley']);e['year']=e['author_year'].rsplit(', ',1)[-1]
 rid=e['id'];r=B.get(rid)
 if not r:r={'id':rid,'title':e['title'],'doi':e['doi'],'authors':e['authors'],'year':e['year'],'journal':m.get('journal','Applied and Environmental Microbiology'if '01426' in e['doi']else 'mBio'),'status':'上传全文核实','scope_decision':e['role'],'reading_depth':e['reading_depth'],'source_role':'用户上传全文补建记录','old_scope_judgment_changed':False};M.append(r);B[rid]=r
 else:r.setdefault('before_upload_review_20261101',{k:r.get(k)for k in ['reading_depth','status','actual_finding','author_interpretation_and_alternatives','locator']})
 r.update(reading_depth=e['reading_depth'],upload_review_20261101=e,actual_finding=e['finding'],author_interpretation_and_alternatives=e['boundary'],locator=e['locator'],status='全文方法/结果/讨论核实；附件缺口单列')
 e['evidence_card']=str((P/'evidence'/f'{rid}.md').relative_to(R))
(P/'evidence').mkdir(exist_ok=True)
for e in E:
 f=R/e['evidence_card'];lines=[f"# {e['id']} · {e['title']}",f"{e['author_year']} · DOI {e['doi']} · {e['role']}",f"**阅读深度：**{e['reading_depth']}。页码均为PDF文件页码；原刊页码可在逐页文本核对。",f"[上传原件]({link(f,R/e['original_path'])}) · [逐页文本]({link(f,R/e['text_path'])})",f"SHA256：`{e['sha256']}`"]
 for k,label in [('methods_and_resolution','对象、测量与空间分辨'),('conditions','实验条件与暴露时间'),('finding','关键观察'),('parameters_and_inference','参数来源与模型'),('boundary','反例与解释边界'),('locator','优先阅读位置')]:lines+=['',f'## {label}','',e[k]]
 lines+=['','关联命题：P1a（输入与暴露）、P1c（串联传质）、P3b（聚集/分层）；功能权衡另见P4。',''];f.write_text('\n\n'.join(lines))
dump(P/'fulltext_evidence.json',E)
# Existing candidates: retrieve/read full official abstracts; keep original scope judgments.
local=[]
notes={'SG-66E719E38CD9':('主体DO>4 mg/L时无氧区消失，0.1–0.2 mm有氧表层依赖进水COD及耗氧；跨厂不能固定穿透深度','直接微电极的正式摘要；粒径/温度/电极细节待正文。'), 'SG-6E33DBD11D46':('粒径100→250 µm中心DO下降10–55%，<100 µm未见明显变化；组成和环境异质性相关','正式摘要支持；不能把粒径相关全部归EPS。'), 'SG-47E08464D7E8':('活性表层<125 µm消耗大部分O₂，CLSM细胞层约100 µm；强调分层模型','同作者同期相似体系，非独立跨实验室重复；DOI不同，不能并成上传Chiu文章。'), 'SG-52CE8A5581BA':('3D FISH菌间距5.30→0.29 µm；H₂最大可能通量1.1→10.3为计算上限','完整正式摘要复用；不是实测菌间流量，温度/3D距离定义待正文。'), 'SG-17EA4C20E788':('NMR学位论文涵盖颗粒MRI及传输，保留作为方法背景','摘要覆盖多种尺度，不是直接O₂微剖面或EPS独立干预；论文全文未读。')}
for rid,(finding,boundary) in notes.items():
 r=B[rid];f=P/'raw'/f'{rid}.json'
 a=json.loads(read(f)['content'][0]['text']) if f.exists()else r
 local.append({'id':rid,'title':r['title'],'basis':'完整官方摘要'if f.exists()else '复用完整缓存摘要字段','abstract':a.get('abstract',''),'finding':finding,'boundary':boundary,'source_path':str(f.relative_to(R))if f.exists()else str((T/'literature_master.json').relative_to(R)),'decision':'可迁移方法证据'if rid!='SG-52CE8A5581BA' else 'AD互营距离证据','prior_scope_preserved':r.get('scope_decision')})
 r.setdefault('before_rescreen_20261101',{k:r.get(k)for k in ['reading_depth','status']});r['rescreen_20261101']=local[-1];r['reading_depth']=local[-1]['basis']+'；正文未读'
dump(P/'local_rescreen.json',local);csvout(P/'local_rescreen_utf8.csv',local)
# Online reference leads, searches and duplicate handling are distinct from uploaded papers.
new=[];hits=[]
for f in sorted((P/'raw').glob('*.json')):
 if not re.match(r'(REF\d|Q\d)\.json',f.name):continue
 z=json.loads(read(f)['content'][0]['text']);arr=z.get('results',[z])
 for a in arr:
  match=next((r for r in M if (doi(a.get('doi'))and doi(r.get('doi'))==doi(a.get('doi')))or (a.get('pmid')and str(r.get('pmid'))==str(a['pmid']))or fold(r.get('title',''))==fold(a.get('title',''))),None)
  if match:hits.append({'title':a.get('title'),'id':match['id'],'status':'重复已有记录','source':f.name});continue
  key=doi(a.get('doi'))or a.get('pmid')or fold(a['title']);rid='SG-'+hashlib.sha256(key.encode()).hexdigest()[:12].upper();a.update(id=rid,status='完整摘要补筛'if a.get('abstract')else '题名线索待摘要',reading_depth='完整返回摘要；未读正文'if a.get('abstract')else '仅元数据/题名',scope_decision='可迁移方法/材料参照（摘要层）'if a.get('abstract')else '待判断',source_role='本轮定向检索/参考文献追溯',source_path=str(f.relative_to(R)),old_scope_judgment_changed=False)
  bounds={'REF0':'中心阶跃+一维拟合，ECP/孔隙为解释，非EPS单独因果；不能与活性层D混用','REF1':'基础扩散理论入口，Crossref无摘要，未据题名纳入','REF2':'纯化alginate添加是材料干预，但增长下降不等于直接氧D实测；须核正文区分黏度/传质/其他效应','REF3':'分层模型反例入口，无摘要，待全文或正式摘要','Q1':'综述比较的是diffusive permeability与diffusion coefficient；按溶质/密度分组，不能把汇总比值当AD O₂常数','Q2':'IFFAS絮体/附着膜比较；摘要仅suggesting partial penetration，未确认直接氧剖面，不据类群位置反推氧保护'}
  a['author_interpretation_and_alternatives']=bounds[f.stem];new.append(a);M.append(a);B[rid]=a;hits.append({'id':rid,'title':a['title'],'status':'新增相关摘要参照'if a.get('abstract')else '新增待摘要线索','source':f.name})
dump(P/'online_screening.json',new);dump(P/'online_hit_disposition.json',hits)
# Update cumulative outputs without rerunning the old pipeline.
dump(T/'literature_master.json',M);csvout(T/'literature_master_utf8.csv',M);ris(T/'spatial_gas_transfer_candidates.ris',M);ris(T/'spatial_gas_transfer_reviewed.ris',[r for r in M if not r.get('reading_depth','').startswith('未读')]);ris(P/'uploaded_and_followup.ris',[B[e['id']]for e in E]+new)
for name in ['remaining_queue','abstract_pending_queue','fulltext_pending']:
 q=read(T/(name+'.json'));done={e['id']for e in E}|({x['id']for x in local}if name!='fulltext_pending'else set());q=[r for r in q if r.get('id')not in done]
 if name=='fulltext_pending':q += [{'id':e['id'],'title':e['title'],'status':'正文已读；仅剩附件或原文矛盾澄清','next_action':e['boundary']}for e in E]
 dump(T/(name+'.json'),q);csvout(T/(name+'_utf8.csv'),q)
rels=read(G/'spatial_gas_proposition_links.json')
for e in E:
 for prop,part in [('P1a','Part 1'),('P1c','Part 1'),('P3b','Part 3')]:
  rels.append({'id':e['id'],'title':e['title'],'doi':e['doi'],'proposition_id':prop,'part':part,'finding':e['finding'],'boundary':e['boundary'],'reading_depth':e['reading_depth'],'evidence_card':e['evidence_card'],'update':'2026-11-01上传全文；旧关联行保留作为历史阅读深度'})
dump(G/'spatial_gas_proposition_links.json',rels);csvout(G/'spatial_gas_proposition_links_utf8.csv',rels)
def sheet(wb,name,rows):
 if name in wb.sheetnames:del wb[name]
 ws=wb.create_sheet(name);keys=list(dict.fromkeys(k for r in rows for k in r))or ['status'];ws.append(keys)
 for r in rows:
  vals=[]
  for k in keys:
   v=r.get(k);v=json.dumps(v,ensure_ascii=False)if isinstance(v,(dict,list))else v
   if isinstance(v,str)and len(v)>32767:v='完整字段见JSON；ID='+str(r.get('id'))
   if isinstance(v,str):v=re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]','',v)
   vals.append(v)
  ws.append(vals)
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
for f in [T/'spatial_gas_transfer_cumulative.xlsx',G/'scientific_reading_guide.xlsx']:
 wb=load_workbook(f)
 if f.parent==T:sheet(wb,'文献与专题筛选',M)
 for n,rows in [('上传全文精读',E),('本轮现有候选补筛',local),('本轮在线补筛',new),('原件与版本映射',I),('空间传质命题关联',rels)]:sheet(wb,n,rows)
 wb.save(f)
# Single reading entrance with relative references to authoritative originals.
f=P/'README.md';text=['# 空间结构与氧传质：统一精读入口','2026-11-01：9个上传文件对应9篇独立文章；均已读方法、结果、讨论及关键图表，未收到独立附件。3篇已有记录沿用ID，6篇补建；不将文件获取等同新增研究。','[专题累计表](../spatial_gas_transfer_cumulative.xlsx) · [文件/版本/SHA清单](file_inventory.json) · [逐篇结构化提取](fulltext_evidence.json) · [现有候选补筛](local_rescreen_utf8.csv) · [在线逐篇判断](online_screening.json) · [RIS](uploaded_and_followup.ris)','原件继续以用户上传路径为权威副本，专题以相对链接集中引用；texts为解析文本，evidence为精读卡，raw为实际查询响应，scripts为本轮方法，主目录累计表合并本轮。Satoh旧公开HTML为另一格式版本，不删除。没有整批复制PDF。','|文献ID／题名|研究问题与直观发现|首看图表／证据强度|边界／阅读深度／原件|','|---|---|---|---|']
for e in E:text.append(f"|{e['id']} · [{e['title']}]({link(f,R/e['evidence_card'])})|{e['finding']}|{e['locator']}；{e['role']}|{e['boundary']} {e['reading_depth']}。[原件]({link(f,R/e['original_path'])})|")
text+=['','## 全文导出的补检词与覆盖缺口','','|实际术语|解决的问题|本轮使用|','|---|---|---|','|diffusive permeability / effective diffusion coefficient|稳态反应通量与非反应瞬态参数不能混称|PubMed Q1，完整返回1条|','|PFG-STE / D–T2 correlation / ADC map|水自扩散、松弛与氧模型分开，记录失败成像|现有NMR候选完整摘要补筛|','|cbb3-2::gfp / multiphoton lithography / no-flux boundary|直接浓度与生物报告、几何因果干预分开|Wessel全文；前向引文元数据144条|','|Thiele modulus / transient step / active layer|辨别D与反应速率非唯一性|Chiu两文补筛及参考文献追溯|','|acetoclastic / apparent Ks / relative effective diffusivity|乙酸反应与气体扩散不同，区分内外阻力|González-Gil全文|','|alginate / capsule / G-M ratio / egg-box|数量、组成与胞内O₂证据分开|Sabra全文；Hassett参考文献摘要|','','实际查询参数、日期、返回量见[检索日志](search_log.json)；PubMed两组分别返回1和2条，均低于请求100条，单次已覆盖其返回总数。没有起始年限制。MCP本地stdio成功，元数据来源PubMed/Crossref；后续引用用OpenAlex官方API。Berg前向29条、Wessel144条各一页全部取回，尚未逐篇补筛，不能计为纳入。','[引用日志](citation_trace_log.json) · [重复处理](online_hit_disposition.json)。其余种子的后续引文尚未本轮追完；原12组不重跑。','','## 后续必须回答','','- Chu扩散数值与倍数、Fan方向/表格、Berg通量百分比与z采样差异：本轮保留冲突，不从矛盾数据计算汇总值。','- 补充附件缺口（Berg S1–S8、Wessel S1–S3、Satoh标定附件）未视为已读。','- 直接连接微曝气AD投氧、颗粒内部O₂、类群空间位置及功能响应的配套数据仍未由这9篇建立。','- 本轮2条新增只有题名的理论线索继续补摘要/正文；173条前向引文先与累计身份去重再读摘要，见citation_trace_log.json。','- 全专题未完成队列仍在../remaining_queue.json、../abstract_pending_queue.json、../fulltext_pending.json；这是明确续跑入口，没有宣称全库筛完。']
f.write_text('\n\n'.join(text[:4])+'\n\n'+'\n'.join(text[4:])+'\n')
summary={'date':'2026-11-01','baseline_commit':'591097727502b81b0e0a5bfa11d5ae07f05c7ca2','uploaded_files':9,'independent_articles':9,'fulltext_methods_results_discussion':9,'uploaded_existing_records':3,'uploaded_new_records':6,'local_candidates_rescreened':len(local),'online_new_abstract_inclusions':sum(bool(r.get('abstract'))for r in new),'online_new_title_leads':sum(not r.get('abstract')for r in new),'online_duplicates':sum(r['status']=='重复已有记录'for r in hits),'forward_metadata_unread':173,'cumulative':len(M),'next':'uploads_20261101/README.md 后续必须回答；剩余队列不重置'}
dump(P/'checkpoint.json',summary);dump(T/'checkpoints/UPLOADS20261101.json',summary);print(summary)
