"""Model reading judgments on the frozen 193-record local continuation queue.

These annotations are not keyword-generated screening. A means the complete
cached abstract was read; T means title only, with abstract/fulltext still due.
Every add saves a per-record state; no existing 40 notes or old scope is changed.
"""
import json
from datetime import datetime,timezone
from pathlib import Path
T=Path(__file__).resolve().parents[1]
Q=json.loads((T/'local_followup_baseline.json').read_text())
C={r['id']:r for r in json.loads((T/'candidate_records.json').read_text())}
NOTES={}
PREV={r['id']:r for r in json.loads((T/'followup_screening.json').read_text())} if (T/'followup_screening.json').exists() else {}
def add(i,tier,reason,finding,limits,quote=None,depth='A',imaging=None,control=None,parameters=None,exchange=None,scales=()):
 rid=Q[i-1]['id'];c=C[rid]
 if quote:assert quote in (c.get('abstract') or ''),(i,quote)
 n={'id':rid,'baseline_queue_order':i,'priority_tier':tier,'reading_depth':'完整缓存摘要；正文方法/参数仍待核实' if depth=='A' else '仅题名初筛；本轮未读摘要或正文','screening_stage':'完整缓存摘要初筛' if depth=='A' else '题名初筛','scope_decision':'本专题不优先' if tier=='范围外' else '待确认' if depth=='T' or tier.startswith('待核') else '专题相关（摘要层面）','decision_reason':reason,'actual_finding':finding,'author_interpretation_and_alternatives':limits,'evidence_quote':quote,'evidence_locator':'候选记录完整缓存摘要' if depth=='A' else '候选记录题名','transfer_compartments':list(scales),'structure_evidence':imaging,'control_evidence':control,'parameters':parameters or [],'exchange_evidence':exchange,'status':'摘要初筛' if depth=='A' else '题名初筛待摘要','new_external_fulltext_downloaded':False,'old_scope_judgment_changed':False,'screened_at_utc':datetime.now(timezone.utc).isoformat(),'source_links':c['source_links']}
 n['screened_at_utc']=PREV.get(rid,{}).get('screened_at_utc') or n['screened_at_utc']
 NOTES[rid]=n
 (T/'followup_screening.json').write_text(json.dumps(list(NOTES.values()),ensure_ascii=False,indent=2)+'\n')
 if len(NOTES)%20==0:
  p=T/'checkpoints'/f'L{len(NOTES):03d}.json'
  if not p.exists():p.write_text(json.dumps({'kind':'local_continuation','total_new_initially_screened':len(NOTES),'ids':list(NOTES),'online_queries_completed_this_followup':0,'complete_abstracts':sum(n['screening_stage']=='完整缓存摘要初筛' for n in NOTES.values()),'title_only':sum(n['screening_stage']=='题名初筛' for n in NOTES.values()),'last_id':rid,'recorded_utc':n['screened_at_utc']},ensure_ascii=False,indent=2)+'\n')

add(1,'C 电位响应背景','产甲烷群落加入电子受体并记录气体/电位','摘要将引入O2等受体后的产甲烷下降与培养基电位升高联系','没有摘要可核的空间分布或传质参数；电位相关不证明氧浓度因果',quote='The decrease of methanogenesis under the electron acceptors introduction is connected with the increase of the culture medium redox potential.')
add(2,'范围外','深海功能基因多样性，不直接回答结构或传质','克隆文库揭示mcrA/pmoA/dsrAB谱系','基因存在不等于空间定位、气体通量或暴露，原综述范围不变')
add(3,'导航综述','综述区分H2/可溶介体与直接电子传递','介绍胞外电子流与分离的供受体代谢','不是新实测D/kLa或距离，需追溯原始研究')
add(4,'C 天然界面','天然微生物席成分和上下层生物地球化学','白席含硫丝和Arcobacter探针阳性细胞；下方SR与AOM活性，硫化物在席内耗尽','显微/FISH和活性支持界面分工；未核三维体成像、O2剖面或流速，流型是解释',imaging={'method':'显微及FISH，方法维度待全文','true_3D_verified':False},scales=['沉积物界面反应'])
add(5,'范围外','甲烷氧化菌铜/盐耐受的搅拌培养，非空间/传质研究','铜添加提高甲烷氧化与耐盐','不据搅拌反应器名称推断传质测量；可作其他机制背景')
add(6,'C 天然形态背景','温泉还原流体形成丝状硫氧化群落','元素能谱检出细胞硫颗粒，丝状与浮游群落以硫氧化菌为主','细胞内硫颗粒不是孔隙或溶解气体通量；产甲烷菌仅检出，不作AD定位结论',imaging={'method':'丝状生物量/能谱元素分析','true_3D_verified':False})
add(7,'C 天然垂向活性','湖底不同深度的MOB数量与潜在活性并不一致','pmoA拷贝峰在5–8cm，充足CH4/O2培养的潜在活性随深度下降','潜在活性在补足气体下测得，非原位通量或氧剖面；不能把基因峰当活性峰',quote='Potential activity, which was measured in the presence of sufficient amounts of methane and oxygen, decreased linearly from the sediment surface to deeper layers.')
add(8,'A 产甲烷气液传质','H2输入AD，比较扩散器孔径及搅拌','扩散器/混合影响H2气液交换与沼气组成；150rpm陶瓷扩散器表现最好；单用粪便加H2后pH>8，乳清共消化可缓冲','摘要未给kLa或颗粒内D；搅拌/孔径改善不是内部扩散证明；pH效应需分开',quote='The H(2) distribution systems (diffusers with different pore sizes) and liquid mixing intensities were demonstrated to affect the gas-liquid mass transfer of H(2) and the biogas composition.',scales=['气液传质','主体混合'])
add(9,'A AD载体成像','活化沸石上的水解菌/产甲烷菌附着，SEM及CLSM','观察载体生物膜；优势群包括Clostridium、Pseudomonas和Methanoculleus，结合水解酶分析','摘要写CLSM不等于确认z-stack体重建；没有微氧/气体通量证据',quote='visualisation of biofilm formation via scanning electron microscopy and confocal laser scanning microscopy',imaging={'method':'SEM及CLSM（摘要）；堆栈/三维重建待全文','targets':['附着微生物','生物膜'],'true_3D_verified':False})
add(10,'C 天然ANME空间','冷泉沉积层位及FISH合成营养伴生形态','ANME-2c在浅层硫酸盐丰富处与细菌相伴，ANME-1深层伴生方式不同，ANME-3为不伴细菌的小聚集体','不同ANME/层位关联，不是产甲烷AD；未量距离和交换通量，不能统一成所有古菌居中',imaging={'method':'FISH＋深度分层分子分析；维度待核','true_3D_verified':False})
add(11,'C 天然矿物/空间','黑海AOM微生物席中SRB内外铁硫矿物','观察胞内外铁硫化物与细胞裂解后链状颗粒','不是孔隙流量或导电互作证明；矿化与气体传质区分',imaging={'method':'微生物席/矿物显微形态，维度待核','true_3D_verified':False})
add(12,'范围外','热液沉积物组学功能，无摘要可核的空间传质测量','硫/甲烷氧化及呼吸相关表达；梯度生态位解释','转录/蛋白不等于气体通量，不能从趋化基因推三维空间结构')
add(13,'C 天然反应输运模型','秘鲁陆架地层中硫酸盐—甲烷带迁移','矿物/脂质和反应输运模型支持沉积碳通量周期驱动SMT深度变化','地质时间与AD时空尺度差异大；是模型解释/古记录，不是氧冲击或AD颗粒测量',scales=['沉积物扩散—反应模型'])
add(14,'C DAMO气液传质','比较三种培养反应器，考虑CH4传质/流失','磁搅气升反应器的总/比n-damo活性最高，最高76.9mgN/L/d','反应器间底物抑制/洗出也不同；无摘要kLa数值；非产甲烷AD',scales=['气液传质（方法参照）'])
add(15,'B 互营电子传递边界','磁铁矿促进丙酸产甲烷并理论比较DIET与H2','甲烷速率提高至33%，作者提出磁铁矿电导通路，理论可达速率高于H2','作者most probably及理论上限不等于直接DIET实测，更不等于气体D或絮体间通量',quote='Theoretical calculations revealed that DIET allows electrons to be transferred among syntrophic partners at rates which are substantially higher than those attainable via interspecies H2 transfer.',scales=['电子传递与H2理论比较'])
add(16,'A AD混合/结构','10°C乳业废水流化床混合与载体聚并','混合不足伴水解不佳；过度附着引起载体聚并分层与沉降流失，H2营养古菌减少','混合、负荷和群落共变；比活性高不等于数量高；无气体Deff或3D量化',scales=['主体混合','附着层/载体结构'])
add(17,'C 天然层位/培养','泥火山剖面结合泥角砾体外培养，改变CH4/硫酸盐','30–55cm与165–205cm两个AOM区，深区活性更高；培养富集ANME-2','剖面与体外响应不同尺度，未测细胞间距离；深层高活性非氧保护证据',scales=['沉积层反应分布'])
add(18,'A AD附着分级','生物炭粒径/附着强弱与产甲烷','0.5–1mm与75µm生物炭改善时滞/速率；Methanosarcina偏紧密结合，Methanosaeta分布受粒径和结合组分影响','分级/指纹不是细胞3D坐标；吸附缓冲与选择定殖共变，不能独归H2距离',imaging={'method':'附着强弱分级＋指纹/测序，非三维坐标','true_3D_verified':False})
add(19,'C 天然来源微宇宙','湖沉积样品以5个初始O2水平培养10/16周','高O2(150–225µM)与低O2(15–75µM)选择不同甲烷氧化/甲基营养类群','初始氧张力不是时间/空间DO剖面；伙伴由组成支持，未直接量交叉营养或空间位点')
add(20,'B 电合成生物膜参照','H2/CO2富集后阴极乙酸合成','乙酸电子回收58±5%，H2副产物30±10%；电化学/共聚焦提示阴极生物膜参与','作者称likely H2，未证气体交换通量或特异空间机制；阴极面积反应率非kLa',imaging={'method':'共聚焦（摘要），3D重建未核','true_3D_verified':False})
add(21,'C 天然扩散供给模型','深部地层孔隙水和模拟显示基底流体供给','Ca/Cl/硫酸盐扩散供给与深层AOM/群落对应，模型估AOM约0.2pmol/cm³/d','为地层反应输运推断，非AD颗粒；未检ANME，活性归属存在不确定',scales=['沉积物扩散—反应模型'])
add(22,'C 界面红氧转换','沉积物—水界面中宇宙连续受体耗尽','监测上覆水化学与基因表达；硝酸盐/硫酸盐还原表达强变，产甲烷/甲烷氧化变化较小','主要由有氧转厌氧，不当作再氧暴露实验；上覆水监测不是内部O2微剖面')
add(23,'A 膜供气甲烷化','H2/CO2无泡膜供给，pH4.5–5.5运行70天','膜供气维持甲烷化，Methanobacterium占优；酸性限制产乙酸型群落','无泡不等于直接测膜kL/生物膜Deff；群落解释需与气体参数分开',quote='CO2 and H2 were diffused into the culture medium through the membrane without bubble formation',scales=['膜供气'])
add(24,'范围外','纤维素/木聚糖长期富集，未直接测空间/传质','35°C得到高效氢营养产甲烷群落，55°C未建立','可作水解/互营背景；本专题不据富集推距离或气体通量')
add(25,'C 天然气体逸出','声学/同位素与活性比较三类甲烷喷流','不同海湾热成因/微生物来源不同，部分有Thiodendron生物膜','气泡逸出、溶解扩散及生物产气不同；未给本轮可核三维/传质系数',scales=['沉积物—水气体释放'])
add(26,'C 天然可渗透沉积物','浅海砂质CH4渗漏，活性/FISH/生物地球化学','20–50cm深且厚至40cm的AOM区，作者解释为渗透砂对流供给；聚集形态多样','对流解释尚非本轮核实流速/通量；不能直接套进污泥Deff',quote='likely caused by advective flow of pore water',imaging={'method':'原位杂交＋群落/活性（摘要）','true_3D_verified':False},scales=['孔隙水对流（解释）','沉积层反应'])
add(27,'导航综述','DIET综述辨别扩散介体与导电传递','指出混合体系促DIET常未达到定义培养预期，吸附/生物膜可能共因','不是新气体参数；只作原始研究追溯与机制边界')
add(28,'A 外置甲烷化生物膜','不同供H2/CO2反应器，扩散器表面生物膜','最佳气体CH4>98%，气泡柱扩散器表面优势为M.thermautotrophicus','摘要没量kLa/内部气体或菌间距离；出气浓度不等于传质效率',scales=['气液供给','扩散器附着'])
add(29,'C DAMO/Anammox层次反例','膜供气改变絮体/膜和类群位置','膜内薄层偏DAMO/Anammox细菌，外层100–200µm颗粒偏DAMO古菌，与既有模拟位置不同','甲烷氧化而非产甲烷AD；位置观察不自动3D，也不量H2/絮体间交换',quote='The spatial distribution of microorganisms in HfMBR was different from simulation results in the literature.',imaging={'method':'两层膜/颗粒和群落定位；3D待核','true_3D_verified':False})
add(30,'C 重塑土团聚体','重塑6/12/18mm土团聚体及碳位置/水位周期','降水位时CH4逸出下降且N2O暂升；核心置碳的N2O约高80%；模型/解释分开物理储气与产气','人为重塑非原位结构；排气变化非全是生物响应；模型分摊不是微区通量直接测定',scales=['团聚体扩散—反应','气体储存/释放'])
