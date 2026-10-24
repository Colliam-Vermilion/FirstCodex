"""Human-reviewed official descriptions/experiment/sample fields, not keyword-only screening."""
import json,re
from common import ROOT,dump,now

ass=json.loads((ROOT/'project_assessments.json').read_text())
annotations=json.loads((ROOT/'sample_annotations.json').read_text()) if (ROOT/'sample_annotations.json').exists() else {}
comparisons=json.loads((ROOT/'confirmed_comparisons.json').read_text())
rows={
'PRJNA551662':('B',1,'泥炭先供氧、后厌氧产甲烷；20个WGS，另34扩增子。官方%O2 Treatment和Time Point可映射。','0/5/10% O2原始标签；T1/T2/T3有pooled，T5分UNS/AWT/BWT；时间单位及培养瓶独立性待方法核实。','优先DNA：氧剂量标签明确；层位和混样分层分析，不能把20run当20重复'),
'PRJNA293548':('B',2,'沉积物石油×Nereis扰动的12个群落RNA文库，项目叙述氧/红氧波动。','control/HC/nereis/nereis_HC各replicate1–3；生物扰动与氧输入混杂，不能等同纯O2干预。','待补氧剖面/培养方法；不凭nereis标签建立独立氧效应'),
'PRJNA322450':('B',2,'诱导底水氧转变的沉积物：12 DNA+22 RNA run，另131扩增子。','所有目标run共用同一个BioSample；实验题名多为通称，需论文SI/原文件名恢复样本键。','DNA/RNA丰富但映射不足；同BioSample不证明物理样本一一配对'),
'PRJNA347538':('B',1,'低氧沉积物氧化时间序列至15天：32 RNA run；实验题名有turned oxic/anoxic、day、rep。','每个RNA实验有2run，共16实验，目标共用1BioSample；day15 oxic4个实验、anoxic3个实验。','优先RNA：day15氧化/厌氧标签明确，先核分lane和培养重复；不以归档BioSample数代替样本量'),
'PRJNA1426923':('B',2,'挪威Paddehavet厌氧/人工再氧合沉积物55个WGS，包括实验室培养及现场4个月前后。','4A/3C等代号缺氧处理键；现场、培养、filter和ENC/EPC/NK/PK疑似质控混在同项目，未计生物样本数。','高潜力DNA：先取样本键及质控说明，不直接55样本做差异'),
'PRJEB65123':('B',2,'四周草地土壤频繁短厌氧/长厌氧/持续氧化历史，最终统一厌氧培养；12 DNA+16 RNA。','O/SA/LA/ORIG，T1/2/3和数字保留原标签，未猜全称与时间单位；DNA/RNA归档样本不同。','优先配套DNA/RNA候选；需完整处理键/重复/建库说明；属于氧历史不是即时氧冲击'),
'PRJNA381321':('B',2,'热带土壤Fe红氧循环快/慢再氧合，6个群落RNA实验。','3个Fast Ox与3个Slow Ox题名；F1/3/5等数字可能取样序号，未据此宣称n=3生物重复。','氧速率对照有价值；缺无氧对照和时间/剂量，待方法'),
'PRJNA1163300':('B',1,'海岸厌氧沉积物瞬时空气/laminarin处理，2群落RNA文库。','SRR30843209 cDNA1明确25% atmospheric air (~4% oxygen)；SRR30843208 cDNA2未加空气标签；laminarin交叉需全文核。','优先小规模RNA机制核验：每条件1文库，不能可靠估计群落差异离散度'),
'PRJNA1112840':('B',2,'湿地土壤control anaerobic/aerobic/sulfate/aerobic+sulfate四条件；公开仅3个WGS。','LW_TOP_C1/C2/C3未说明四条件对应；不擅自认定这3个是3个处理或3个重复。','候选氧×硫酸盐DNA，缺处理键，不能直接做氧差异'),
'PRJNA330349':('B',2,'Rifle地下沉积物Oxygen_injection B1，1个群落WGS。','只有B1氧注入样本标签；未定位同研究厌氧对照。','追踪Rifle同研究项目，单样本不估计氧效应'),
'PRJNA330207':('B',2,'Rifle地下沉积物Oxygen_injection C2，1个群落WGS。','只有C2氧注入样本标签；未证实与B1实验独立或与对照的关系。','追踪同研究及对照，不能把B/C当处理/对照')}
excluded={
'PRJNA1149829':'11个AMPLICON；全尺度AD微曝气脱硫范围相关，但当前项目非shotgun',
'PRJNA1405076':'20个AMPLICON；16S+PICRUSt2，功能预测不是宏基因组',
'PRJNA1002618':'34个AMPLICON；食品AD微曝气，当前项目无目标reads',
'PRJNA1491653':'30个AMPLICON；16S细菌/古菌V3-V4，非shotgun',
'PRJNA807302':'35个AMPLICON；DGG-B产甲烷苯富集氧冲击研究重要，但此项目非shotgun',
'PRJNA736312':'326个AMPLICON；消化液干湿/氧实验，非目标数据类型',
'PRJNA1241260':'56个AMPLICON；氧波动与SIP/网络不证明有shotgun',
'PRJNA1123272':'80个AMPLICON；描述提及MG/MT但当前公开实验只有扩增子，需查另存项目，不能否定研究存在MG/MT',
'PRJNA1479055':'33个AMPLICON；另红氧由不同化学还原剂调节，不能直接视为氧输入'}
for acc,(tier,code,rationale,mapping,priority) in rows.items():
 ass[acc]={'tier':tier,'availability_code':code,'availability':'公开且处理/实验标签明确；完整方法及独立重复仍待核' if code==1 else '公开但分组/元数据需补充','rationale':rationale,'mapping_status':mapping,'priority':priority,'limitations':mapping,'oxygen_comparisons_confirmed':0,'biological_replicates':'未知；样本编号、rep标签或run数不直接等于独立生物重复','confirmed_biological_specimen_count':None,'confirmed_experimental_units':None,'audit_batch':'D004','evidence_paths':['project_cache/'+acc+'/collection_status.json','project_cache/'+acc+'/ncbi_sra_packages.json','project_cache/'+acc+'/ena_runs.json']}
for acc,reason in excluded.items():
 ass[acc]={'tier':'特殊/非目标','availability_code':7,'availability':'不符合目标数据类型（当前已公开run）','rationale':reason,'mapping_status':'未将扩增子纳入群落shotgun集合','assay_exclusion':'非目标：扩增子','priority':'不进入reads下载；有明确MG/MT线索者继续追踪其他项目','limitations':reason,'audit_batch':'D004','oxygen_comparisons_confirmed':0}
for acc in rows:
 xs=json.loads((ROOT/'project_cache'/acc/'ncbi_sra_packages.json').read_text())
 for x in xs:
  if x.get('library_strategy')=='AMPLICON':continue
  attrs={v['tag']:v['value'] for v in x.get('sample_attributes',[])};title=x.get('experiment_title','');alias=x.get('sample_alias','');a={'treatment_label':alias,'mapping_status':ass[acc]['mapping_status']}
  if acc=='PRJNA551662':
   a.update(treatment_label=attrs.get('%O2 Treatment')+'% O2; '+attrs.get('Layer',''),oxygen_exposure=attrs.get('%O2 Treatment')!='0',timepoint=attrs.get('Time Point'),time_unit='原始Time Point标签，单位待核',core_comparison_eligible=True)
  elif acc=='PRJNA347538':
   m=re.search(r"turned (oxic|anoxic)' day (\d+) rep (\d+)",title)
   if m:a.update(treatment_label='turned '+m[1],timepoint=int(m[2]),time_unit='day',oxygen_exposure=m[1]=='oxic',biological_replicate='实验原始rep '+m[3]+'；独立培养来源待核',experimental_unit_id=x.get('experiment_accession'),core_comparison_eligible=int(m[2])==15)
  elif acc=='PRJNA1163300':a.update(treatment_label=title,oxygen_exposure=x['run_accession']=='SRR30843209',core_comparison_eligible=True)
  elif acc=='PRJNA293548':a.update(treatment_label=alias,biological_replicate=attrs.get('replicate_id'),oxygen_exposure=None)
  elif acc=='PRJNA381321':a.update(treatment_label=title,oxygen_exposure=True)
  elif acc=='PRJEB65123':a.update(treatment_label=attrs.get('sample name') or alias)
  annotations[x['run_accession']]=a

def add(acc,key,treated,control,caveat):
 c={'comparison_id':'C-'+acc+'-'+key,'project_id':acc,'treatment':key.split('-vs-')[0],'control':key.split('-vs-')[-1],'treatment_runs':treated,'control_runs':control,'independent_reactor_replicates_per_group':None,'design_evidence_level':'官方实验/样本标签；完整方法及生物重复待核','caveat':caveat}
 if c['comparison_id'] not in {v['comparison_id'] for v in comparisons}:comparisons.append(c)
 ass[acc]['oxygen_comparisons_confirmed']+=1
xs=json.loads((ROOT/'project_cache/PRJNA551662/ncbi_sra_packages.json').read_text())
for tm,layer in [('1','pooled'),('5','UNS'),('5','BWT')]:
 def group(o):return [x['run_accession'] for x in xs if x['library_strategy']!='AMPLICON' and {a['tag']:a['value'] for a in x.get('sample_attributes',[])}.get('%O2 Treatment')==o and {a['tag']:a['value'] for a in x.get('sample_attributes',[])}.get('Time Point')==tm and {a['tag']:a['value'] for a in x.get('sample_attributes',[])}.get('Layer')==layer]
 for oxy in ['5','10']:
  if group(oxy) and group('0'):add('PRJNA551662',oxy+'percent-vs-0percent-T'+tm+'-'+layer,group(oxy),group('0'),'原始%O2/Time Point/Layer明确；对照各仅1文库，pooled非生物重复；时间单位与独立性待全文')
xs=json.loads((ROOT/'project_cache/PRJNA347538/ncbi_sra_packages.json').read_text())
add('PRJNA347538','oxic-vs-anoxic-day15',[x['run_accession'] for x in xs if "turned oxic' day 15" in x.get('experiment_title','')],[x['run_accession'] for x in xs if "turned anoxic' day 15" in x.get('experiment_title','')],'8 vs 6 run对应4 vs 3实验；每实验2run先合并，独立培养和先前氧历史须方法核实')
add('PRJNA1163300','air-vs-unlabelled-air',['SRR30843209'],['SRR30843208'],'空气处理题名明确；对照/laminarin因素须完整方法再核；n=1文库，不作有重复统计')
dump(ROOT/'project_assessments.json',ass);dump(ROOT/'sample_annotations.json',annotations);dump(ROOT/'confirmed_comparisons.json',comparisons)
dump(ROOT/'checkpoints/D004.json',{'saved_utc':now(),'stage':'第三批20新增项目完成官方项目/实验/样本审计','project_accessions':list(rows)+list(excluded),'raw_reads_downloaded':0,'next_action':'补项目关联论文、全池去重/续跑与分析可行性汇总'})
print('D004 reviewed',len(rows)+len(excluded),'public community',len(rows),'new metadata comparisons',sum(ass[x]['oxygen_comparisons_confirmed'] for x in rows))
