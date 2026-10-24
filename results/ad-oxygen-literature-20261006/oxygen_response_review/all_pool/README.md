> **阶段记录：全池初筛阶段。** 当前整合方法与阶段衔接以[详细方法](../methods/METHODS.md)和[当前入口](../README.md)为准；下文的“本轮/下一步”属于当时阶段，不代表后来重新检索或全文已核完。

> **35条队列来源与条件补充说明**：[逐篇核对](../reading_queue35/README.md)。35条不是已确认核心文献，也不是引用/JIF前35或四项全达标集；本轮已补读35条完整缓存摘要，仍未核全文。9条有2024 JIF缓存、25条未核实、1条预印本不适用；独立验证按具体主张保留未核实及已有部分支持。其余312条范围相关候选继续核实，35不是最终数量上限。

# 全池补全、初筛与暂定优先集（2026-10-24，上海时区）

当前基准为本轮开始远端提交 `625dac5eb84d06fb15e5ff7d884f475730f9af06` 的1536条池：原AD库554条全部参与新范围判断，保留旧ID、旧分类和人工结论。没有重新检索、删掉未重命中的原库记录，或重新下载未改动的论文原件。

## 完成量与阅读边界

|项目|实际数量|含义|
|---|---:|---|
|全池|1536|书目记录，不是独立实验或纳入研究数|
|本轮新增逐项初筛|1516|31个检查点，通常50条，P004为32条，P031为34条|
|原20篇|20|筛选对象及原精读评价保留；未重复查询其OpenAlex指标|
|累计已初步处理|1536|包含原20篇不同阅读深度；新增均非全文核实|
|尚未开始初筛|0|不代表下述待确认已经解决|
|新增核心范围/机制潜力候选|347|暂定标签，不代表因果机制已证明|
|新增待确认|477|先补读完整摘要，必要时再读全文；不强行纳入/排除|
|新增理论/综述/模型背景|336|单列追溯队列，不混入原始机制优先数|
|新增排除|356|每条保留具体理由与读取依据|
|全池暂定优先集|364|347新增候选＋原17推荐；包含可迁移机制与阴性边界|
|待确认累计|479|新增477＋原20内的2条|
|下一阶段新增重点候选|35|来自整个池的跨主题选择；与原17一起形成52条重点展示集|

**新增1516条采用助手逐项读取题名和所选摘要关键句的首遍语义分流，不是完整摘要通读。** 片段可截断，P003以后显示片段保存于`abstract_evidence_excerpt`及`packets/`；P001/P002未保存当时显示片段，对应字段仅缓存摘要前450字定位，不作逐字已读引文；完整已获取摘要位于`metadata_enrichment.json`。不能由片段未出现信息断言原摘要/全文不存在该证据。“待确认”可先补读完整摘要，不强制所有477条都先找全文。新增全文核实0，新增独立验证判断0。原20已有全文片段证据、3个评价工作表和26行验证关联原样保留。

`computational_prescreen.json`是1516条自动词线索路由，**不作为完成量**。只有`decisions/`的逐项判断进入初筛统计。系统、微生物名称、AD关联及氧情境另有明确标记的文本辅助注释，不能据此确认同物种/同属在AD中常见、实验处理设计或机制因果。

## 元数据与指标

- OpenAlex引用可用1459／1536；缺77条保持空值。查询确认的0才写0。先复用已有返回和原20指标，新增31次DOI批量官方API请求，原始响应、查询参数、状态、大小及时间见`metadata_requests.json`和`raw/`。本轮未启动文献发现检索，未做付费数据库访问。
- 已有摘要1214条，复用OpenAlex补至1306条，仍缺230条。没有逐篇追查缺指标。
- 期刊/ISSN形成543个统一缓存键；412条记录匹配已有2024 JIF/JCR机构索引缓存，其他留空。缓存来源快照保留；并非本轮Clarivate账户导出，不凭期刊印象补分区，不以JIF缺失阻塞筛选。
- 引用来源统一OpenAlex，查询日期2026-10-24；按可用出版日给年均引用，最小计1年，缺日用年份1月1日并标明。它不是学科/同年校正。科学层内仅作辅助，不让新近研究因低累计引用被排除。
- 元数据阶段有完整工具计时：**48.25秒**。`prescreen_stage.json`是计算路由计时，`render_timing.jsonl`/`finalize_timing.jsonl`是导出计时；检查点时间仅覆盖写入动作，不冒充完整语义阅读耗时。本轮语义筛选完整耗时没有独立测量，不估算。

## 使用交付文件

- [同一累计Excel](../oxygen_response_review_cumulative.xlsx)：保留原9表，更新文献总表/续跑队列；新增全池筛选、全池指标、全池暂定优先、背景追溯队列、待确认队列、重点全文候选、下一阶段新候选、全池评价口径。原优先精读、机制验证关联、评价口径为原20精读结果；全池暂定优先是新任务产物，二者阅读深度不同。
- [全部逐项初筛CSV](semantic_screening_records_utf8.csv)／[JSON](semantic_screening_records.json)；[进度JSON](progress.json)。保留旧ID、原库关联和原分类的完整总表在上一层`catalog.json`及`literature_master_utf8.csv`。
- [364条暂定优先CSV](provisional_priorities_utf8.csv)／[JSON](provisional_priorities.json)／[RIS](provisional_priority_set.ris)。辅助排序及外推限制有独立字段。不能把“核心候选”标签解释成“核心机制已验证”。
- [35条新增重点续跑CSV](next_stage_queue_utf8.csv)／[JSON](next_stage_queue.json)／[RIS](new_focus_set.ris)；[52条含既有17展示集](focus_fulltext_queue_utf8.csv)。下一步按`next_stage_order`优先处理新35条，先复用已有原件；原17是参考复用，不优先重复加工。
- [479条待确认CSV](pending_confirmation_queue_utf8.csv)、[336条背景追溯CSV](background_trace_queue_utf8.csv)、[11组可能版本关联](possible_version_groups.json)。同题仅是提示，不静默合并或当独立验证。原`identity_conflicts.json`继续保留。
- [评价口径](evaluation_policy.json)、[更正记录](corrections.json)、[检查点](checkpoints/)、[API记录](metadata_requests.json)。P012漏项导致的判断文字错位已更正，Git保留更正前后；最终判断包与决策逐项对应。

RIS为替代导入子集，ID相同的全池/优先/重点RIS不要同时无去重导入；Excel和JSON是当前进度依据。RIS已做字段/ID结构验证，未声称已在Windows EndNote实际导入。

## 科学优先级与后续核验

先依据AD工艺/功能关联和潜在实验直接性，再考虑独立支持是否已知；新增记录独立支持一律未核实。新35条由助手在全池首遍后按具体靶点/过程、直接干预线索和主题覆盖选择，不用高引用或JIF顶替范围判断。主要值得补读的方向如下，均为**暂定候选线索**：

|主题|代表记录|下一步要确认的具体问题|
|---|---|---|
|损伤/修复|OR-3A00C82F8A2B；OR-FA5B37263F6F|PFL损伤修复与古菌转录酶FeS氧敏是否有直接实验、O2/ROS区分|
|解毒/电子流|OR-3D3C740308F5；R09148|FDP铁硫中心及乳酸氧化耦合解毒；题名中的putative末端细胞色素不能写成已证实|
|代谢条件|OR-81B738B20350；OR-124B294CA364；OR-CEDAA95DD383|产甲烷菌纯/混培养耐氧及古菌底物依赖促进；不能跨底物/温度泛化|
|互作|R11596；R13833|兼性菌耗氧保护LCFA互营是否有共培养、耗氧或去除伙伴实验，而非仅丰度/网络|
|空间保护|OR-E9124F54EA76；OR-8E58C5BBDB53|固定化/生物膜中是否直接测氧扩散、局部厌氧和活性|
|恢复/边界|OR-15A62A4556E3；OR-A8CEEF69FB67；OR-E551A6ADF474|可逆分裂阻断、干湿中无可辨氧效应、脉冲时长改变铁还原/甲烷竞争|

OR-52D6CC670C6A为预印本，推荐暂定；OR-E05033DBC651存在已检出的对应通信OR-E64FF1DBCE8D，下一步需合读，尚未裁定争议。基因存在/组学表达不等于酶活和通量，网络非互作，导电材料非DIET，驯化恢复非遗传进化。

自然环境中氧扩散、水位、温度、矿物、根输入与底物常共变；肠道研究还受宿主及营养影响。新候选可提供机制模板，不能直接替代AD氧剂量结论。瘤胃直接氧操纵、AD水解菌纯培养、真正重复暴露遗传适应、群落内直接O2微剖面仍需核覆盖；不从初筛数量推断证据已充足。

## 稳定续跑与重建

`next_stage_queue.json`保存跨主题交替的35条稳定顺序，处理后逐篇写状态；待确认队列先补读完整摘要。不要重新检索或重复查询原20指标。新全文核实应保存实际读取的方法/结果、引用原句及页码/章节；独立支持只追踪具体主张的原始研究，未核实留空/未核实，不无限追溯。

重建同一累计表：`python scripts/pool_screen.py render`（无网络请求、不下载原件）。它调用`pool_finalize.py`；旧`render_results.py`也已加全池保护，避免恢复成只有B001。导入逐项新判断：`python scripts/pool_screen.py apply <judgments.json>`；最多50项，验证ID/可选题名、合法状态和唯一性，已完成ID跳过。不要再次运行初始发现或覆盖冻结基线。

## 新35条的可执行读取顺序

|顺序|ID|主题|年|题名|DOI链接|
|---:|---|---|---|---|---|
|1|OR-FA5B37263F6F|M1 损伤与修复|2012|Subunit D of RNA polymerase from Methanosarcina acetivorans contains two oxygen-labile [4Fe-4S] clusters: implications for oxidant-dependent regulation of transcription.|https://doi.org/10.1074/jbc.m111.331199|
|2|R09148|M2 古菌及厌氧菌解毒|2023|Lactate oxidation is linked to energy conservation and to oxygen detoxification via a putative terminal cytochrome oxidase in Methanosarcina acetivorans|https://doi.org/10.1016/j.abb.2023.109667|
|3|OR-124B294CA364|M3 代谢切换与条件|2024|Comparison of methane yield of a novel strain of Methanothermobacter marburgensis in pure and mixed adapted culture derived from a methanation bubble column bioreactor.|https://doi.org/10.1016/j.biortech.2024.131021|
|4|R11596|M4 群落互作|2025|Facultative anaerobic bacteria enable syntrophic fatty acids degradation under micro-aerobic conditions|https://doi.org/10.1016/j.biortech.2024.131829|
|5|OR-8E58C5BBDB53|M5 空间保护|2014|Stratified microbial structure and activity in sulfide- and methane-producing anaerobic sewer biofilms.|https://doi.org/10.1128/aem.02146-14|
|6|R07494|M6 恢复及反例|2022|Bioaugmentation with methanogens cultured in a micro-aerobic microbial community for overloaded anaerobic digestion recovery|https://doi.org/10.1016/j.anaerobe.2022.102603|
|7|OR-F4B8A98806CB|M1 损伤与修复|2022|The Autonomous Glycyl Radical Protein GrcA Restores Activity to Inactive Full-Length Pyruvate Formate-Lyase In Vivo.|https://doi.org/10.1128/jb.00070-22|
|8|OR-49242898AE4A|M2 古菌及厌氧菌解毒|2013|Redox-sensitive DNA binding by homodimeric Methanosarcina acetivorans MsvR is modulated by cysteine residues|https://doi.org/10.1186/1471-2180-13-163|
|9|OR-81B738B20350|M3 代谢切换与条件|2026|Developing a robust biomethanation process by improving oxygen tolerance of Methanothermobacter wolfeii strain BSEL.|https://doi.org/10.1016/j.biortech.2026.135041|
|10|OR-01782ECD28E3|M4 群落互作|2021|Simultaneous Anaerobic and Aerobic Ammonia and Methane Oxidation under Oxygen Limitation Conditions.|https://doi.org/10.1128/aem.00043-21|
|11|OR-E9124F54EA76|M5 空间保护|2025|Enhanced resilience to oxygen exposure and toxicity of chlorinated solvents in immobilized Dehalococcoides mccartyi.|https://doi.org/10.1016/j.jhazmat.2025.137769|
|12|OR-A8CEEF69FB67|M6 恢复及反例|2022|Absence of oxygen effect on microbial structure and methane production during drying and rewetting events.|https://doi.org/10.1038/s41598-022-20448-5|
|13|OR-8C75CC78BFD2|M1 损伤与修复|2001|How does oxygen inhibit central metabolism in the obligate anaerobe Bacteroides thetaiotaomicron.|https://doi.org/10.1046/j.1365-2958.2001.02343.x|
|14|OR-3D3C740308F5|M2 古菌及厌氧菌解毒|2025|An iron-sulfur cluster as a new metal center in a flavodiiron protein.|https://doi.org/10.1002/pro.70204|
|15|OR-F6D3E9F8E669|M3 代谢切换与条件|2024|Bacteroides thetaiotaomicron enhances oxidative stress tolerance through rhamnose-dependent mechanisms|https://doi.org/10.3389/fmicb.2024.1505218|
|16|R10086|M4 群落互作|2024|Effect of micro-aeration on syntrophic and methanogenic activity in anaerobic sludge|https://doi.org/10.1007/s00253-023-12969-4|
|17|OR-E551A6ADF474|M6 恢复及反例|2025|Duration of O2 Exposure Determines Dominance of FeII vs CH4 Production in Tropical Forest Soils.|https://doi.org/10.1021/acs.est.4c12329|
|18|OR-5D303857796F|M1 损伤与修复|2017|The Fumarate Reductase of Bacteroides thetaiotaomicron, unlike That of Escherichia coli, Is Configured so that It Does Not Generate Reactive Oxygen Species.|https://doi.org/10.1128/mbio.01873-16|
|19|OR-C63E5057C2A6|M2 古菌及厌氧菌解毒|2012|Mechanism of oxygen detoxification by the surprisingly oxygen-tolerant hyperthermophilic archaeon, Pyrococcus furiosus.|https://doi.org/10.1073/pnas.1208605109|
|20|OR-3B1D70862C75|M3 代谢切换与条件|2023|Carbon dioxide and trace oxygen concentrations impact growth and product formation of the gut bacterium Phocaeicola vulgatus.|https://doi.org/10.1186/s12866-023-03127-x|
|21|R13833|M4 群落互作|2018|Insight into the Role of Facultative Bacteria Stimulated by Microaeration in Continuous Bioreactors Converting LCFA to Methane|https://doi.org/10.1021/acs.est.8b00894|
|22|OR-15A62A4556E3|M6 恢复及反例|2015|Single-Cell Analysis of Growth and Cell Division of the Anaerobe Desulfovibrio vulgaris Hildenborough.|https://doi.org/10.3389/fmicb.2015.01378|
|23|OR-E05033DBC651|M1 损伤与修复|2025|Fortification of FeS Clusters Reshapes Anaerobic CO Dehydrogenase into an Air-Viable Enzyme Through Multilayered Sealing of O2 Tunnels.|https://doi.org/10.1002/anie.202508565|
|24|OR-82F6FC6E3A3E|M2 古菌及厌氧菌解毒|2020|Role of Superoxide Reductase FA796 in Oxidative Stress Resistance in Filifactor alocis.|https://doi.org/10.1038/s41598-020-65806-3|
|25|R13274|M3 代谢切换与条件|2026|Micro-aeration enhances lactic acid production in food waste fermentation|https://doi.org/10.1016/j.biortech.2025.133807|
|26|OR-631665AE20A2|M6 恢复及反例|2023|Pulses of labile carbon cause transient decoupling of fermentation and respiration in permeable sediments.|https://doi.org/10.1002/lno.12411|
|27|OR-E0944369CA6F|M1 损伤与修复|2019|Solution structure and biochemical characterization of a spare part protein that restores activity to an oxygen-damaged glycyl radical enzyme.|https://doi.org/10.1007/s00775-019-01681-2|
|28|OR-A47D88A5BD92|M2 古菌及厌氧菌解毒|2021|A Point Mutation in the Transcriptional Repressor PerR Results in a Constitutive Oxidative Stress Response in Clostridioides difficile 630Δerm.|https://doi.org/10.1128/msphere.00091-21|
|29|OR-CEDAA95DD383|M3 代谢切换与条件|2019|Oxygen-mediated growth enhancement of an obligate anaerobic archaeon Thermococcus onnurineus NA1.|https://doi.org/10.1007/s12275-019-8592-y|
|30|OR-071CAFC18C32|M6 恢复及反例|2026|Dietary fiber fermentation restores microbiome resilience to oxygen stress in a host-independent ex vivo model.|https://doi.org/10.1128/mbio.03934-25|
|31|OR-3A00C82F8A2B|M1 损伤与修复|2021|Rescuing activity of oxygen-damaged pyruvate formate-lyase by a spare part protein.|https://doi.org/10.1016/j.jbc.2021.101423|
|32|OR-7018E028D4E6|M2 古菌及厌氧菌解毒|2012|Characterization of the Bacteroides fragilis bfr gene product identifies a bacterial DPS-like protein and suggests evolutionary links in the ferritin superfamily.|https://doi.org/10.1128/jb.05260-11|
|33|OR-52D6CC670C6A|M3 代谢切换与条件|2026|Rational engineering of facultative anaerobiosis enables commensal survival in the oxygenated gut.|https://doi.org/10.64898/2026.06.05.730451|
|34|OR-C78553A0F4D0|M2 古菌及厌氧菌解毒|2013|The extracytoplasmic function sigma factor EcfO protects Bacteroides fragilis against oxidative stress.|https://doi.org/10.1128/jb.01491-12|
|35|OR-454A09DABEFE|M2 古菌及厌氧菌解毒|2024|New Electron-Transfer Chain to a Flavodiiron Protein in Fusobacterium nucleatum Couples Butyryl-CoA Oxidation to O2 Reduction.|https://doi.org/10.1021/acs.biochem.4c00279|
