from pathlib import Path
import json,hashlib,os,sys,re,shutil
from openpyxl import load_workbook
R=Path('/workspace/FirstCodex');T=R/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer';P=T/'uploads_20261101';G=R/'scientific_guide';sys.path.insert(0,str(T/'scripts'));from render import csvout,ris
read=lambda p:json.load(open(p))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Add the already-existing Stewart review to the local rescreen ledger, not new inclusions.
M=read(T/'literature_master.json');r=next(r for r in M if r['id']=='SG-7F5A16A6C6BB');a=json.loads(read(P/'raw/Q1.json')['content'][0]['text'])['results'][0];L=read(P/'local_rescreen.json');L.append({'id':r['id'],'title':r['title'],'basis':'完整官方PubMed摘要','abstract':a['abstract'],'finding':'有效扩散渗透性用于反应扩散、有效扩散系数用于非反应瞬态；参数依溶质类别与密度而变','boundary':'综述汇总并非单次AD O₂实测；0.43等平均值不能套用微曝气AD','source_path':str((P/'raw/Q1.json').relative_to(R)),'decision':'可迁移理论参照','prior_scope_preserved':r.get('scope_decision')});r['rescreen_20261101']=L[-1];r['reading_depth']='完整官方PubMed摘要；正文未读';dump(P/'local_rescreen.json',L);csvout(P/'local_rescreen_utf8.csv',L);dump(T/'literature_master.json',M);csvout(T/'literature_master_utf8.csv',M)
for filename in ['spatial_gas_transfer_candidates.ris','spatial_gas_transfer_reviewed.ris']:
 if filename.endswith('candidates.ris'):ris(T/filename,M)
 else:ris(T/filename,[r for r in M if not r.get('reading_depth','').startswith('未读')])
sumry=read(P/'checkpoint.json');sumry['local_candidates_rescreened']=6;dump(P/'checkpoint.json',sumry);dump(T/'checkpoints/UPLOADS20261101.json',sumry)
# Current science supersedes stale paragraph claims; historical original prose remains in dated snapshots.
f=R/'README.md';s=f.read_text();s=re.sub(r'\[Chu等，2005（正式摘要）\].*?绝对尺寸、温度及拟合程序待正文。','[Chu等，2005（上传全文核实）]('+str((P/'evidence/SG-7E776DC9CBE3.md').relative_to(R))+')将35°C批次消化与另行O₂中心阶跃拟合联系起来。正文给出D=2.9×10⁻¹⁰与1.97×10⁻⁹ m²/s，其比值约6.79，却又称2.3倍；摘要5倍响应与正文12–20 s对约10 s亦不能直接一致化。因此保留原始数值冲突，不再把摘要倍数当已核实参数。较大r²/D可抵消较大D的趋势；O₂并非消化底物的直接传输测量。',s,count=1)
s=s.replace('Satoh等，2007；仅缓存摘要','Satoh等，2007；上传全文核实').replace('有效扩散测量对象是否失活、温度、标定/拟合方法和边界层尚未从正文核实','H₂系数为35°C氯仿失活颗粒中心阶跃拟合，CH₄相对系数沿用H₂假定').replace('用户提供的同步辐射微CT种子10.1128/aem.00563-24尚未独立取回核对，故不据题名写孔隙发现。','同步辐射微CT种子10.1128/aem.00563-24已于2026-10-30核实正文：固定包埋样品的结构可见，但不是活体通量，详见下方全文补证。')
f.write_text(s)
# annotate legacy parameter rows without deleting their original values
params=read(T/'gas_transfer_parameters.json')
for r in params:
 if r.get('id')=='SG-7E776DC9CBE3':r['current_20261101_caution']='上传全文p4数值与摘要倍数不一致，不据此比较/汇总D；详见uploads_20261101/evidence/SG-7E776DC9CBE3.md'
dump(T/'gas_transfer_parameters.json',params);csvout(T/'gas_transfer_parameters_utf8.csv',params)
# Old evidence cards retain text, with a current pointer at top.
for e in read(P/'fulltext_evidence.json'):
 f=T/'evidence'/f"{e['id']}.md"
 if f.exists():f.write_text('> **2026-11-01更新：**[上传全文精读卡](../uploads_20261101/evidence/'+e['id']+'.md)已核实方法、结果、讨论和关键图表；以下为原有阅读深度的历史记录，原判断保留。\n\n'+f.read_text())
# update cumulative workbooks' local ledger and main data, leaving every pre-existing worksheet available.
def sheet(wb,name,rows):
 if name in wb.sheetnames:del wb[name]
 ws=wb.create_sheet(name);keys=list(dict.fromkeys(k for r in rows for k in r));ws.append(keys)
 for r in rows:
  vals=[]
  for k in keys:
   v=r.get(k);v=json.dumps(v,ensure_ascii=False)if isinstance(v,(dict,list))else v
   if isinstance(v,str):v=re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]','',v);v=v if len(v)<32767 else '完整字段见JSON；ID='+str(r.get('id'))
   vals.append(v)
  ws.append(vals)
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
for f in [T/'spatial_gas_transfer_cumulative.xlsx',G/'scientific_reading_guide.xlsx']:
 wb=load_workbook(f);sheet(wb,'本轮现有候选补筛',L)
 if f.parent==T:sheet(wb,'文献与专题筛选',M);sheet(wb,'传质参数及剖面',params)
 wb.save(f)
# latest status separate from dated prior counts
p=read(T/'progress.json');p['upload_continuation_20261101']=sumry;p['candidates']=len(M);p['remaining']=len(read(T/'remaining_queue.json'));p['abstract_pending_after_title']=len(read(T/'abstract_pending_queue.json'));p['resume']='uploads_20261101/README.md：附件、原文矛盾、前向引文和剩余队列；不运行旧渲染覆盖本轮';dump(T/'progress.json',p)
for f in [P/'README.md']:
 s=f.read_text();s=s.replace('本轮2条新增只有题名的理论线索','Hassett新候选通过ScanSci legal_only尝试全文，未找到PDF，保留正式摘要判断；未访问灰色来源。见new_fulltext_attempt.json。\n\n本轮2条新增只有题名的理论线索');f.write_text(s)
for f in (P/'texts').glob('*.txt'):f.unlink()
# All content-producing sources are preserved; guard the one-off merge against duplicating relations.
for filename in ['inventory.py','export.py','finalize.py']:
 src=Path('/workspace/oxygen-spatial-20261101')/filename
 if src.exists():shutil.copy(src,P/'scripts'/filename)
f=P/'scripts/export.py';s=f.read_text();anchor="M=read(T/'literature_master.json');";s=s.replace(anchor,"if (P/'checkpoint.json').exists():\n raise SystemExit('Checkpoint already merged; do not duplicate rows. Use existing JSON and a new continuation batch.')\n"+anchor);f.write_text(s)
# record seed seven in requested order
E=read(P/'fulltext_evidence.json');order=[5,2,0,1,4,3,6];seed=[{'id':E[i]['id'],'doi':E[i]['doi'],'previously_recorded':E[i]['previous_record'],'fulltext':'用户上传原件','depth':E[i]['reading_depth'],'card':E[i]['evidence_card']}for i in order];dump(P/'seven_seed_audit.json',seed);csvout(P/'seven_seed_audit_utf8.csv',seed)
print(sumry)
