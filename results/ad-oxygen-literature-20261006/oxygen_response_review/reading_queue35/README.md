> **阶段记录：35篇来源审计阶段。** 当前整合方法与阶段衔接以[详细方法](../methods/METHODS.md)和[当前入口](../README.md)为准；下文的“本轮/下一步”属于当时阶段，不代表后来重新检索或全文已核完。

# 35条优先阅读队列：来源、理由和条件核对

这35条不是已经筛选确认的核心文献。当前不能确认其中任何一条同时满足高被引、高期刊影响、AD对象高度相关和具体机制独立验证四项条件。缺失/未核实不等于不符合范围。

## 形成来源与评价口径

- **队列是什么**：35条是从新增347条范围/机制潜力候选中由助手按具体靶点、潜在干预证据及主题覆盖人工指定的阅读队列，不是按引用/JIF选出的前35，也不是四项全部达标的终选集；固定FOCUS列表见scripts/pool_finalize.py。
- **来源**：基于22374f2e4提交冻结35个原ID及顺序；30条带PubMed来源、6条带OpenAlex来源、6条关联原AD库，来源可重叠。原AD库条目无新检索来源时如实记为原库，不冒充本轮新检出。
- **初筛类别**：原35条均为“核心候选”；这是原标签，规范解释为“范围相关/机制潜力候选，待核”，不是筛选确认的核心文献。保留旧判断供审计，本轮不静默改成终选纳入。
- **阅读深度**：入队时是题名/摘要关键句，且可复用原20评价中的已存关联；本轮逐篇补读35条完整缓存摘要。新增全文方法/结果核实0；完整缓存摘要不是全文。
- **高被引条件**：34条有OpenAlex缓存计数，2条为0，1条缺失。没有约定高被引阈值或同年/领域基准，除0不支持高被引外，不据数字擅自宣布达标；缺值不写0。引用不是范围门槛。
- **期刊影响力条件**：9条有2024 JIF/JCR机构索引缓存，25条未核实，1条为预印本不适用。沿用同年缓存及原来源，不重查JIF；有数值不等于已满足未定义的“高影响”阈值，也不等于Clarivate账户导出核实。
- **AD相关条件**：逐篇区分AD直接体系、具体产甲烷/互营/硫循环属及功能类群、仅共享代谢靶点/结构。未核实同株常见性留未核实，不凭同门/同科或泛厌氧判高度相关；纯酶/肠道/海泥/超嗜热体系列外推边界。
- **独立验证条件**：全部35的同对象/同特定主张严格独立重复未核实。已有同团队支持和跨类群暂定支持按具体DOI复用；跨团队跨类群支持不等于本篇特定链条已独立复制，更不等于广泛验证。
- **四项是否同时满足**：当前0条能确认同时满足四项；这是核实状态，不是判定35条均不符合范围或均没有价值。非AD理论、阴性结果和新文仍可优先阅读。
- **应当收窄的主张**：生物膜分层不自动证明氧屏蔽；酸抑制后恢复不等于去氧后恢复；离体FDP金属中心不等于胞内清氧；失活突变体修复不等于活细胞氧后恢复；相关/转录不等于因果/通量；ALE表述仍需遗传稳定性证据。
- **其余文献继续**：35不是最终数量上限。其余312条新增范围相关候选另列继续核实，累计479待确认、336背景追溯及原20评价全部保留。未入35不代表排除，其他候选可随证据升级/降级并进入阅读队列。
- **没有完成的工作**：本轮没有重新检索、追查缺JIF、下载/复核论文原件或开展新的无限引用追溯；仅补读缓存摘要并解释来源和条件。

## 逐篇总览

原初筛类别均为“核心候选”（原始标签，仅指范围/机制潜力）；入队时为题名/关键句层面，本轮35条完整缓存摘要均已读取，全文核实均未完成。高被引未采用统一阈值；引用、年均引用及JIF只是可核信息。空JIF不能按期刊印象补造。

|顺序|ID／简题|来源|当前阅读角色／选择理由|引用数／年均|2024 JIF|AD关联|独立验证条件|
|---:|---|---|---|---:|---:|---|---|
|1|OR-FA5B37263F6F<br>古菌RNA聚合酶氧敏FeS簇|PubMed|直接靶点机制优先阅读；产甲烷古菌转录机器有明确氧敏金属簇靶点，可连接氧暴露与蛋白稳定性|19 / 1.304|未核实|AD产甲烷常见属及功能类群相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|2|R09148<br>乳酸氧化与产甲烷菌清氧|原AD库/PubMed|直接过程/靶点机制优先阅读；氧脉冲驯化产甲烷菌中，乳酸代谢、耗氧和能量保存发生联系|7 / 2.084|未核实|AD产甲烷常见属及底物过程相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|3|OR-124B294CA364<br>M.marburgensis纯/混培养氧暴露|PubMed|氧耐受条件优先阅读；比较同种不同株及来源混菌群，适合判断伙伴与菌株差异|4 / 1.709|9.0|AD氢营养产甲烷功能相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|4|R11596<br>Pseudomonas保护脂酸互营共培养|原AD库/PubMed/OpenAlex|直接共培养机制优先阅读；互营菌/产甲烷菌组合加减兼性伙伴并改变O2，具有可检验的保护作用设计|14 / 7.212|9.0|AD相同属及脂酸互营功能强相关|已有同团队前后续/比较关联；不构成已核实的独立验证|
|5|OR-8E58C5BBDB53<br>下水道SRB/产甲烷生物膜分层|PubMed|空间背景阅读；直接氧进入待范围核实；原先因微电极、分层活性及AD相关类群入队，可比较空间分工|119 / 9.809|3.7|AD相同属/硫与甲烷功能相关，但氧问题待核|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|6|R07494<br>MC1微氧培养与过载AD恢复|原AD库|AD应用背景阅读；氧恢复机制待核；微氧群落培养产甲烷菌后生物强化AD，可核查伴生菌帮助和温度边界|16 / 3.666|未核实|直接AD体系及产甲烷功能相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|7|OR-F4B8A98806CB<br>GrcA恢复失活全长PFL|PubMed|修复机制背景优先阅读；实际氧冲击恢复待核；遗传模型可区分修复活性与酶量变化，补充PFL修复生化证据|15 / 3.292|未核实|AD发酵通路/氧敏靶点可比，非AD同种已核实|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|8|OR-49242898AE4A<br>M.acetivorans MsvR氧化还原调控|OpenAlex|调控靶点背景优先阅读；细胞氧进入待核；产甲烷古菌特异调控蛋白，半胱氨酸与DNA结合提供具体靶点|12 / 0.904|未核实|AD产甲烷属/调控靶点相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|9|OR-81B738B20350<br>M.wolfeii氧耐受培养适应|PubMed|菌株选择/耐氧边界优先阅读；新近氢营养产甲烷菌连续/批培养耐氧，不能因零引用漏掉|0 / 0.0|9.0|AD相关氢营养产甲烷属/功能相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|10|OR-01782ECD28E3<br>限氧下N-damo/Anammox共存|PubMed|非AD核心类群的共存机制优先阅读；厌氧氮/甲烷氧化与好氧伙伴在持续供氧下共存，有直接活性测量|9 / 1.638|3.7|AD出水过程相关；不是AD主体产甲烷机制|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|11|OR-E9124F54EA76<br>固定化Dehalococcoides耐氧|PubMed|空间/固定化干预优先阅读；固定化与悬浮对照、明确氧暴露和脱氯活性，可检验物理保护|6 / 3.622|11.3|非AD典型类群；物理屏蔽机制类比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|12|OR-A8CEEF69FB67<br>干湿循环中无显著额外氧效应|PubMed|阴性/适用边界优先阅读；AD来源菌群空气/N2干燥再湿对照，避免只挑正面效应|10 / 2.466|未核实|直接AD接种群落相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|13|OR-8C75CC78BFD2<br>B.theta中心代谢O2/ROS损伤|PubMed|经典理论机制优先阅读；同一厌氧菌中区分超氧损伤延胡索酸酶与分子氧损伤PFOR|110 / 4.289|未核实|非AD同种已核实；PFOR/发酵/FeS靶点强可比|已有同团队前后续/比较关联；不构成已核实的独立验证|
|14|OR-3D3C740308F5<br>S.wolfei FDP新FeS中心|PubMed|AD互营菌靶点背景优先阅读；胞内清氧待核；研究对象就是脂肪酸互营菌，可具体定位FDP结构域与电子传递问题|0 / 0.0|未核实|AD相同互营属/功能类群强相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|15|OR-F6D3E9F8E669<br>鼠李糖/RhaR调节B.theta氧耐受|OpenAlex|底物/遗传调控优先阅读；具体碳源与调控因子使氧应答不同，适合讨论底物决定促进或抑制|25 / 13.389|未核实|非AD同种已核实；发酵与PFOR靶点可比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|16|R10086<br>厌氧污泥底物依赖微曝气抑制|原AD库/PubMed|直接AD活性/互作优先阅读；乙醇与直接产甲烷底物O2剂量响应不同，可拆分发酵伙伴作用|16 / 5.873|未核实|直接AD污泥及互营功能相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|17|OR-E551A6ADF474<br>氧脉冲时长改变铁还原/甲烷|PubMed/OpenAlex|氧暴露历程边界优先阅读；不同氧期时长改变竞争优势，且有13C-DNA示踪|6 / 3.634|11.3|功能竞争可类比AD；非AD同种/属已核实|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|18|OR-5D303857796F<br>B.theta Frd不是预期ROS源|PubMed|生化反例/适用边界优先阅读；直接排除一个看似合理ROS源，避免从E.coli酶推广到所有厌氧菌|40 / 4.081|未核实|非AD同种已核实；延胡索酸呼吸/红氧靶点可比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|19|OR-C63E5057C2A6<br>P.furiosus电子分流SOR/FDP|PubMed|直接遗传/电子流理论优先阅读；缺失株加生理产物变化，且有rubredoxin/H2酶阴性结果|62 / 4.413|未核实|非AD典型类群；Fd/H2/防御靶点可比|已有不同团队跨类群/体系原始支持（沿用旧表、暂定）；未确认本篇具体电子路线或同对象独立重复|
|20|OR-3B1D70862C75<br>P.vulgatus微量氧/CO2产酸|PubMed|气体浓度条件优先阅读；在线气体与有机酸分析，提供可定位的低氧容忍窗口|11 / 3.819|未核实|非AD同种已核实；厌氧糖发酵/有机酸功能可比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|21|R13833<br>LCFA微氧连续反应器兼性菌|原AD库|直接AD关联/边界优先阅读；不同红氧条件与底物负荷比较，并报告暂时抑制后恢复|58 / 6.869|11.3|直接AD功能及兼性伴生菌相关|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|22|OR-15A62A4556E3<br>D.vulgaris氧暴露可逆分裂阻断|PubMed|单细胞恢复生理优先阅读；直接观察氧暴露期间的细胞分裂，为群落不变但生理受抑提供依据|38 / 3.493|未核实|AD硫酸盐还原功能/相同属可比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|23|OR-E05033DBC651<br>CODH气道封闭耐氧工程|PubMed|纯酶靶点/争议配对优先阅读；对氧进入通道作定点工程，连接空间可达性与NiFe/FeS簇损伤|5 / 3.602|未核实|非AD同种已核实；CODH低电位NiFe/FeS靶点可比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|24|OR-82F6FC6E3A3E<br>F.alocis SOR敲除氧敏感|PubMed|遗传/酶学基础机制优先阅读；SOR既有重组酶活又有缺失株氧/空气存活差异|24 / 3.764|未核实|非AD常见同种/属已核实；SOR防御系统类比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|25|R13274<br>微曝气食品发酵乳酸及红氧|原AD库|AD上游酸化/剂量边界优先阅读；含中度促进与过量抑制，兼有产物及转录，适合区分生理与功能潜力|2 / 2.0|9.0|AD上游水解酸化功能相关；非产甲烷全过程|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|26|OR-631665AE20A2<br>海泥碳脉冲与H2暂态解耦|PubMed|阴性O2/扰动混杂边界优先阅读；同时考察氧、机械扰动与碳，氧效应小而剧烈振荡有影响|2 / 0.619|未核实|AD发酵-H2互作功能可比；非同种已核实|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|27|OR-E0944369CA6F<br>YfiD结构与PFL修复模型|PubMed|结构/修复背景优先阅读；具体修复蛋白结构与截短PFL相容性，帮助设计修复机制论证|18 / 2.457|未核实|AD发酵通路/氧敏自由基酶可比，非AD同种已核实|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|28|OR-A47D88A5BD92<br>C.difficile PerR单点突变|PubMed|遗传调控/模型菌边界优先阅读；单核苷酸变异及互补可解释实验室参考株耐氧偏高，警示菌株选择|18 / 3.193|未核实|非AD常见同种/属已核实；PerR/rubrerythrin防御可比较|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|29|OR-CEDAA95DD383<br>T.onnurineus底物依赖氧促进|PubMed/OpenAlex|非AD古菌促进条件边界优先阅读；O2促进依赖酵母浸粉底物，适合反驳简单厌氧菌遇氧全抑制|5 / 0.647|未核实|非AD典型类群；发酵/红氧平衡靶点可比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|30|OR-071CAFC18C32<br>纤维/酸化恢复离体肠菌抗氧|PubMed|群落干预/化学环境边界优先阅读；有四组O2/纤维因子设计和SCFA/pH，可分离宿主影响|1 / 1.0|未核实|AD发酵功能可类比；非AD相同群落已核实|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|31|OR-3A00C82F8A2B<br>YfiD救援氧损伤PFL酶学|PubMed|直接离体修复理论优先阅读；酶活/光谱与截短干预区分损伤程度和可修复窗口|11 / 2.231|未核实|AD发酵PFL靶点可比；具体AD菌同源未核实|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|32|OR-7018E028D4E6<br>B.fragilis DPS样蛋白护DNA|PubMed|遗传/金属稳态基础机制优先阅读；bfr缺失耐氧下降并有DNA自由基保护，连接金属和损伤|36 / 2.399|未核实|非AD同种已核实；铁稳态/DNA保护靶点可比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|33|OR-52D6CC670C6A<br>工程B.theta突破好氧生长屏障|PubMed/OpenAlex|预印本优先阅读；非已确认核心；多靶点修复候选可整合中心代谢/合成/红氧限制，保留新近研究|缺失 / 缺失|预印本不适用|非AD同种已核实；可迁移代谢靶点待方法核查|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|34|OR-C78553A0F4D0<br>B.fragilis EcfO/Reo抗氧调控|PubMed|遗传/调控基础机制优先阅读；调控因子与抗sigma伙伴有删除和互作，较纯组学更直接|27 / 1.931|未核实|非AD同种已核实；应激调控靶点可比但分布有限|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|
|35|OR-454A09DABEFE<br>丁酰CoA→BCR/FDP还原O2|PubMed|直接电子链酶学理论优先阅读；把发酵中间体电子流与O2还原连接，有重构复合体与快速动力学|7 / 3.253|未核实|非AD常见同种/属已核实；丁酰CoA/Etf/FDP靶点可比|未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证|

## 逐篇完整记录

### 1. OR-FA5B37263F6F — Subunit D of RNA polymerase from Methanosarcina acetivorans contains two oxygen-labile [4Fe-4S] clusters: implications for oxidant-dependent regulation of transcription.

- 年份/期刊/DOI：2012；The Journal of biological chemistry；https://doi.org/10.1074/jbc.m111.331199
- 来源及原库关联：['PubMed']；查询ID ['P10']；原库ID []；初筛批次 P020。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：M.acetivorans RNA聚合酶氧不稳定FeS簇，产甲烷靶点重点；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：产甲烷古菌转录机器有明确氧敏金属簇靶点，可连接氧暴露与蛋白稳定性。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-FA5B37263F6F]/abstract_enriched`。
- 微生物/AD条件：Methanosarcina acetivorans；异源表达E. coli；AD产甲烷常见属及功能类群相关；Methanosarcina为AD相关产甲烷属；具体同株在AD中的常见性未核实。
- 机制证据仍仅由摘要报告：纯化复合体、FeS重构与结构域删除、氧暴露后簇丢失和聚集。需核实：离体D-L二聚体不等于完整RNA聚合酶在AD细胞内转录受抑；不能从潜在调节写成已证实调控。
- 高被引条件：19次，年均1.304；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_b6de20b010a87e.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 2. R09148 — Lactate oxidation is linked to energy conservation and to oxygen detoxification via a putative terminal cytochrome oxidase in Methanosarcina acetivorans

- 年份/期刊/DOI：2023；Archives of Biochemistry and Biophysics；https://doi.org/10.1016/j.abb.2023.109667
- 来源及原库关联：['Original AD library', 'PubMed']；查询ID ['OLD554', 'P16']；原库ID ['R09148']；初筛批次 P008。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：Methanosarcina乳酸氧化、能量与氧解毒相联系，是原库外范围可重判的重点代谢候选。本轮更明确的阅读理由：氧脉冲驯化产甲烷菌中，乳酸代谢、耗氧和能量保存发生联系。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=R09148]/abstract_enriched`。
- 微生物/AD条件：Methanosarcina acetivorans；E. coli dld互补宿主；AD产甲烷常见属及底物过程相关；乙酸/乳酸共代谢与产甲烷相关；海洋菌株培养条件不同于混合底物AD。
- 机制证据仍仅由摘要报告：14C示踪、耗氧/HQNO抑制、异源互补及酶学线索。需核实：末端bd氧化酶仍为putative；抑制剂和转录不等于本菌该氧化酶的遗传因果证明。
- 高被引条件：7次，年均2.084；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_998902a65881a6.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 3. OR-124B294CA364 — Comparison of methane yield of a novel strain of Methanothermobacter marburgensis in pure and mixed adapted culture derived from a methanation bubble column bioreactor.

- 年份/期刊/DOI：2024；Bioresource technology；https://doi.org/10.1016/j.biortech.2024.131021
- 来源及原库关联：['PubMed']；查询ID ['P01', 'P12']；原库ID []；初筛批次 P022。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：M.marburgensis纯/混培养氧暴露240min产甲烷，直接AD功能候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：比较同种不同株及来源混菌群，适合判断伙伴与菌株差异。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-124B294CA364]/abstract_enriched`。
- 微生物/AD条件：Methanothermobacter marburgensis Clermont及Marburg株；来源混合培养；AD氢营养产甲烷功能相关；相同产甲烷属及H2/CO2途径可比；生物气升级柱与有机物AD不同。
- 机制证据仍仅由摘要报告：纯/混培养与最长240 min O2暴露的甲烷产率比较。需核实：摘要没有完整报告各氧处理结果，不能预判混菌一定保护；剂量与对照需全文。
- 高被引条件：4次，年均1.709；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_1b961c2c407979.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=9.0；JCR类别/分区=[{"category": "AGRICULTURAL ENGINEERING", "quartile": "Q1"}, {"category": "AGRICULTURAL ENGINEERING", "quartile": "Q1"}, {"category": "BIOTECHNOLOGY & APPLIED MICROBIOLOGY", "quartile": "Q1"}, {"category": "ENERGY & FUELS", "quartile": "Q1"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=zk&id=3976；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_0.json`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 4. R11596 — Facultative anaerobic bacteria enable syntrophic fatty acids degradation under micro-aerobic conditions

- 年份/期刊/DOI：2025；Bioresource Technology；https://doi.org/10.1016/j.biortech.2024.131829
- 来源及原库关联：['Original AD library', 'PubMed', 'OpenAlex']；查询ID ['OLD554', 'P04', 'P11', 'P13', 'O03']；原库ID ['R11596']；初筛批次 P001。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：合成互营培养±兼性菌及O2比较，脂肪酸降解保护的优先机制候选。本轮更明确的阅读理由：互营菌/产甲烷菌组合加减兼性伙伴并改变O2，具有可检验的保护作用设计。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=R11596]/abstract_enriched`。
- 微生物/AD条件：Syntrophomonas wolfei/zehnderi；Methanospirillum hungatei；Methanobacterium formicicum；Pseudomonas spp.；AD相同属及脂酸互营功能强相关；具体互营脂肪酸氧化菌及H2营养产甲烷伙伴；比泛厌氧相似更直接。
- 机制证据仍仅由摘要报告：合成共培养、±Pseudomonas、0–10% O2与脂肪酸转甲烷。需核实：需全文核实清氧通量和其他伙伴作用；不证明DIET，也非群落中总有益。
- 高被引条件：14次，年均7.212；OpenAlex，查询2026-10-24，原始缓存`raw/openalex/O03_page_000.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=9.0；JCR类别/分区=[{"category": "AGRICULTURAL ENGINEERING", "quartile": "Q1"}, {"category": "AGRICULTURAL ENGINEERING", "quartile": "Q1"}, {"category": "BIOTECHNOLOGY & APPLIED MICROBIOLOGY", "quartile": "Q1"}, {"category": "ENERGY & FUELS", "quartile": "Q1"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=zk&id=3976；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_0.json`。
- 独立验证条件：已有同团队前后续/比较关联；不构成已核实的独立验证；严格同对象/同主张独立重复未确认。
  - 复用旧表 CL06：10.1111/1462-2920.15124 ↔ 10.1016/j.biortech.2024.131829；共享团队后续支持；具体主张：兼性菌帮助互营脂肪酸群落在微氧下转化；限制：2024后续仅摘要；不能当完全独立再现，不证明DIET。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 5. OR-8E58C5BBDB53 — Stratified microbial structure and activity in sulfide- and methane-producing anaerobic sewer biofilms.

- 年份/期刊/DOI：2014；Applied and environmental microbiology；https://doi.org/10.1128/aem.02146-14
- 来源及原库关联：['PubMed']；查询ID ['P05']；原库ID []；初筛批次 P023。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：氧进入/直接机制范围待回查；暂作背景或理论阅读。
- 原入队理由：下水道硫/甲烷生物膜分层活性，空间重点候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：原先因微电极、分层活性及AD相关类群入队，可比较空间分工。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-8E58C5BBDB53]/abstract_enriched`。
- 微生物/AD条件：Methanosaeta；Desulfobulbus/Desulfovibrio等SRB；AD相同属/硫与甲烷功能相关，但氧问题待核；下水道与AD有可比产甲烷和硫还原类群，但水力/底物与硫酸盐不同。
- 机制证据仍仅由摘要报告：硫化物微电极、切片FISH、群落及模型支持分层。需核实：完整缓存摘要未报告O2进入干预或O2微剖面，不能当氧屏蔽直接证据；全文若仍无氧过程应仅作空间背景。
- 高被引条件：119次，年均9.809；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_d67f680d5c898c.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=3.7；JCR类别/分区=[{"category": "BIOTECHNOLOGY & APPLIED MICROBIOLOGY", "quartile": "Q2"}, {"category": "MICROBIOLOGY", "quartile": "Q2"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=zk&id=6584；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_20.json`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 6. R07494 — Bioaugmentation with methanogens cultured in a micro-aerobic microbial community for overloaded anaerobic digestion recovery

- 年份/期刊/DOI：2022；Anaerobe；https://doi.org/10.1016/j.anaerobe.2022.102603
- 来源及原库关联：['Original AD library']；查询ID ['OLD554']；原库ID ['R07494']；初筛批次 P005。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：氧进入/直接机制范围待回查；暂作背景或理论阅读。
- 原入队理由：微氧菌群培养甲烷菌并修复AD负荷抑制，优先共培养保护/恢复候选。本轮更明确的阅读理由：微氧群落培养产甲烷菌后生物强化AD，可核查伴生菌帮助和温度边界。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=R07494]/abstract_enriched`。
- 微生物/AD条件：M.acetivorans C2A；Methanosaeta thermophila NBRC101360；MC1混合菌；直接AD体系及产甲烷功能相关；有热/中温AD恢复及化学/灭菌对照，具体接种类群明确。
- 机制证据仍仅由摘要报告：微氧混培、接种强化、气体产量/pH/16S测量。需核实：恢复对象是过载/酸抑制，不是已证实的去氧后恢复；中温无明确效果；耗氧保护因果未确立。
- 高被引条件：16次，年均3.666；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_998902a65881a6.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 7. OR-F4B8A98806CB — The Autonomous Glycyl Radical Protein GrcA Restores Activity to Inactive Full-Length Pyruvate Formate-Lyase In Vivo.

- 年份/期刊/DOI：2022；Journal of bacteriology；https://doi.org/10.1128/jb.00070-22
- 来源及原库关联：['PubMed']；查询ID ['P10', 'P15']；原库ID []；初筛批次 P006。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：氧进入/直接机制范围待回查；暂作背景或理论阅读。
- 原入队理由：GrcA在体恢复失活PFL，直接修复机制候选；须核实O2处理和补偿试验。本轮更明确的阅读理由：遗传模型可区分修复活性与酶量变化，补充PFL修复生化证据。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-F4B8A98806CB]/abstract_enriched`。
- 微生物/AD条件：Escherichia coli PflB/GrcA；AD发酵通路/氧敏靶点可比，非AD同种已核实；PFL连接丙酮酸、甲酸/乙酰CoA及H2；需核AD菌是否具同源GrcA系统。
- 机制证据仍仅由摘要报告：PflB-G734A、grcA缺失及关键残基干预与甲酸/H2产量。需核实：主要是失活突变体模型，不能说已直接测得活细胞氧冲击后PFL修复；无独立验证核实。
- 高被引条件：15次，年均3.292；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_d67f680d5c898c.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
  - 配对阅读指针：10.1007/s00775-019-01681-2；结构/模拟氧损伤模型；与本篇体内失活突变体不同，团队独立性未核。
  - 配对阅读指针：10.1016/j.jbc.2021.101423；离体氧损伤修复；独立性及同主张再现未核。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 8. OR-49242898AE4A — Redox-sensitive DNA binding by homodimeric Methanosarcina acetivorans MsvR is modulated by cysteine residues

- 年份/期刊/DOI：2013；BMC Microbiology；https://doi.org/10.1186/1471-2180-13-163
- 来源及原库关联：['OpenAlex']；查询ID ['O01']；原库ID []；初筛批次 P018。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：氧进入/直接机制范围待回查；暂作背景或理论阅读。
- 原入队理由：M.acetivorans MsvR半胱氨酸调DNA结合，防御调控重点；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：产甲烷古菌特异调控蛋白，半胱氨酸与DNA结合提供具体靶点。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-49242898AE4A]/abstract_enriched`。
- 微生物/AD条件：Methanosarcina acetivorans MsvR；比较M.thermautotrophicus MsvR；AD产甲烷属/调控靶点相关；同属产甲烷代谢可比，但不同种的结合靶点已有差异。
- 机制证据仍仅由摘要报告：纯化蛋白、凝胶过滤和位点突变、氧化/还原DNA结合。需核实：离体红氧条件不等于细胞O2挑战；缓存摘要Results与Conclusions对结合氧化还原条件表述有不一致，必须核全文。
- 高被引条件：12次，年均0.904；OpenAlex，查询2026-10-24，原始缓存`raw/openalex/O01_page_000.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 9. OR-81B738B20350 — Developing a robust biomethanation process by improving oxygen tolerance of Methanothermobacter wolfeii strain BSEL.

- 年份/期刊/DOI：2026；Bioresource technology；https://doi.org/10.1016/j.biortech.2026.135041
- 来源及原库关联：['PubMed']；查询ID ['P01']；原库ID []；初筛批次 P002。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：产甲烷菌纯培养氧耐受与生物甲烷化直接相关，是新优先候选；剂量/适应机制待全文。本轮更明确的阅读理由：新近氢营养产甲烷菌连续/批培养耐氧，不能因零引用漏掉。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-81B738B20350]/abstract_enriched`。
- 微生物/AD条件：Methanothermobacter wolfeii BSEL；AD相关氢营养产甲烷属/功能相关；生物气升级H2/CO2输入及嗜热培养与常规AD底物/温度不同。
- 机制证据仍仅由摘要报告：作者称ALE；串代/连续培养O2挑战、产甲烷和形态变化。需核实：需方法、稳定传代及遗传/重测序证据判断是否遗传适应，不能只据驯化和生物膜变化称进化机制。
- 高被引条件：0次，年均0.0；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_1b961c2c407979.json`；当前0次，不支持高被引；新文仍可因机制相关保留。
- 期刊影响力条件：JIF2024=9.0；JCR类别/分区=[{"category": "AGRICULTURAL ENGINEERING", "quartile": "Q1"}, {"category": "AGRICULTURAL ENGINEERING", "quartile": "Q1"}, {"category": "BIOTECHNOLOGY & APPLIED MICROBIOLOGY", "quartile": "Q1"}, {"category": "ENERGY & FUELS", "quartile": "Q1"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=zk&id=3976；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_0.json`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 10. OR-01782ECD28E3 — Simultaneous Anaerobic and Aerobic Ammonia and Methane Oxidation under Oxygen Limitation Conditions.

- 年份/期刊/DOI：2021；Applied and environmental microbiology；https://doi.org/10.1128/aem.00043-21
- 来源及原库关联：['PubMed']；查询ID ['P01', 'P11']；原库ID []；初筛批次 P019。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：氧限制下厌氧甲烷/氨氧化共培养，互作及活性重点候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：厌氧氮/甲烷氧化与好氧伙伴在持续供氧下共存，有直接活性测量。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-01782ECD28E3]/abstract_enriched`。
- 微生物/AD条件：N-damo微生物；Anammox；好氧氨/甲烷氧化菌；产甲烷菌；AD出水过程相关；不是AD主体产甲烷机制；可比较氧清除与厌氧过程并存；Anammox/N-damo代谢不能直接等同产甲烷。
- 机制证据仍仅由摘要报告：膜进样质谱MIMS原位活动、批试验、FISH/宏基因组。需核实：共存和活动不自动证明特定伙伴的保护因果或空间O2屏蔽；不同氮底物边界。
- 高被引条件：9次，年均1.638；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_d67f680d5c898c.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=3.7；JCR类别/分区=[{"category": "BIOTECHNOLOGY & APPLIED MICROBIOLOGY", "quartile": "Q2"}, {"category": "MICROBIOLOGY", "quartile": "Q2"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=zk&id=6584；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_20.json`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 11. OR-E9124F54EA76 — Enhanced resilience to oxygen exposure and toxicity of chlorinated solvents in immobilized Dehalococcoides mccartyi.

- 年份/期刊/DOI：2025；Journal of hazardous materials；https://doi.org/10.1016/j.jhazmat.2025.137769
- 来源及原库关联：['PubMed']；查询ID ['P12']；原库ID []；初筛批次 P008。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：固定化脱卤菌氧暴露后保留功能，优先空间保护/恢复边界。本轮更明确的阅读理由：固定化与悬浮对照、明确氧暴露和脱氯活性，可检验物理保护。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-E9124F54EA76]/abstract_enriched`。
- 微生物/AD条件：Dehalococcoides mccartyi 195及含Dhc脱氯菌群；非AD典型类群；物理屏蔽机制类比；严格厌氧呼吸菌可示范保护结构，但脱卤代谢不是AD主路径。
- 机制证据仍仅由摘要报告：水凝胶包埋/悬浮对照、12 h–7 d O2暴露及脱氯活性。需核实：人为凝胶不等于天然AD颗粒/EPS；需核实氧扩散或局部DO是否直接测量，氯溶剂胁迫须分开。
- 高被引条件：6次，年均3.622；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_89595ec5103266.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=11.3；JCR类别/分区=[{"category": "ENGINEERING, ENVIRONMENTAL", "quartile": "Q1"}, {"category": "ENVIRONMENTAL SCIENCES", "quartile": "Q1"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=sci&id=6955；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_9.json`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 12. OR-A8CEEF69FB67 — Absence of oxygen effect on microbial structure and methane production during drying and rewetting events.

- 年份/期刊/DOI：2022；Scientific reports；https://doi.org/10.1038/s41598-022-20448-5
- 来源及原库关联：['PubMed']；查询ID ['P01', 'P12']；原库ID []；初筛批次 P017。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：干湿交替有/无氧对甲烷及群落无效应，阴性边界重点；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：AD来源菌群空气/N2干燥再湿对照，避免只挑正面效应。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-A8CEEF69FB67]/abstract_enriched`。
- 微生物/AD条件：不同结构的AD来源产甲烷群落；直接AD接种群落相关；来源为厌氧消化器，干燥状态与连续液态AD差异大。
- 机制证据仍仅由摘要报告：连续干湿循环、有氧/无氧干燥、甲烷与群落响应。需核实：无显著差异限于该设计，不是所有氧冲击无效；有机物耗竭和干燥掩蔽效应需核。
- 高被引条件：10次，年均2.466；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_2d3b26d0b89c1a.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 13. OR-8C75CC78BFD2 — How does oxygen inhibit central metabolism in the obligate anaerobe Bacteroides thetaiotaomicron.

- 年份/期刊/DOI：2001；Molecular microbiology；https://doi.org/10.1046/j.1365-2958.2001.02343.x
- 来源及原库关联：['PubMed']；查询ID ['T01']；原库ID []；初筛批次 P014。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：B.thetaiotaomicron氧抑制中心代谢，靶点重点候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：同一厌氧菌中区分超氧损伤延胡索酸酶与分子氧损伤PFOR。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-8C75CC78BFD2]/abstract_enriched`。
- 微生物/AD条件：Bacteroides thetaiotaomicron；非AD同种已核实；PFOR/发酵/FeS靶点强可比；与AD发酵低电位代谢有具体途径关联，肠菌培养基/底物不同。
- 机制证据仍仅由摘要报告：曝气前后产物与酶活、离体氧/超氧及FeS重构。需核实：2001早期基础；与2020同团队论文对PFOR恢复性表述差异需核，不能写普遍可恢复。
- 高被引条件：110次，年均4.289；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_2d3b26d0b89c1a.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：已有同团队前后续/比较关联；不构成已核实的独立验证；严格同对象/同主张独立重复未确认。
  - 复用旧表 CL01：10.1111/mmi.14516 ↔ 10.1046/j.1365-2958.2001.02343.x；同团队早期支持；具体主张：B. thetaiotaomicron PFOR可被分子O2直接损伤；限制：2001摘要与2020对PFOR恢复性的表述差异需另查。
  - 复用旧表 CL01-repair：10.1111/mmi.14516 ↔ 10.1046/j.1365-2958.2001.02343.x；同团队早晚恢复性表述差异（待核实）；具体主张：PFOR受氧损伤后是否可恢复需按酶/条件核实；限制：2001全文方法未核实，不能凭摘要判哪篇错误；须区分酶种类、剂量及修复试验。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 14. OR-3D3C740308F5 — An iron-sulfur cluster as a new metal center in a flavodiiron protein.

- 年份/期刊/DOI：2025；Protein science : a publication of the Protein Society；https://doi.org/10.1002/pro.70204
- 来源及原库关联：['PubMed']；查询ID ['P02', 'P04', 'P10']；原库ID []；初筛批次 P006。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：氧进入/直接机制范围待回查；暂作背景或理论阅读。
- 原入队理由：S.wolfei FDP突变/FeS结构及氧防御，新增直接酶学优先候选，非细胞原位验证。本轮更明确的阅读理由：研究对象就是脂肪酸互营菌，可具体定位FDP结构域与电子传递问题。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-3D3C740308F5]/abstract_enriched`。
- 微生物/AD条件：Syntrophomonas wolfei Class E FDP；AD相同互营属/功能类群强相关；丁酸/脂肪酸互营对象相关；此工作主要是分离蛋白而非完整AD群落。
- 机制证据仍仅由摘要报告：纯化野生型/位点突变/截短、EPR/Raman确认[3Fe-4S]中心。需核实：新金属中心证据不等于已证明胞内耐氧功能或完整电子链；Class E不能套用Class H结论。
- 高被引条件：0次，年均0.0；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_b22a4c3bfbf5e4.json`；当前0次，不支持高被引；新文仍可因机制相关保留。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
  - 配对阅读指针：10.1111/febs.17040；S.wolfei另一类别FDP；仅比较线索，不能复制Class E新FeS中心结论。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 15. OR-F6D3E9F8E669 — Bacteroides thetaiotaomicron enhances oxidative stress tolerance through rhamnose-dependent mechanisms

- 年份/期刊/DOI：2024；Frontiers in Microbiology；https://doi.org/10.3389/fmicb.2024.1505218
- 来源及原库关联：['OpenAlex']；查询ID ['F01']；原库ID []；初筛批次 P023。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：B.thetaiotaomicron鼠李糖依赖氧化耐受，代谢保护重点候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：具体碳源与调控因子使氧应答不同，适合讨论底物决定促进或抑制。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-F6D3E9F8E669]/abstract_enriched`。
- 微生物/AD条件：Bacteroides thetaiotaomicron；RhaR/PFOR；非AD同种已核实；发酵与PFOR靶点可比；肠道单糖培养与AD混合底物不同，菌属相近不足以判高相关。
- 机制证据仍仅由摘要报告：鼠李糖/葡萄糖对照、rhaR缺失/过表达、ROS与代谢产物。需核实：摘要自己说明PFOR并非主要ROS源；需核过表达/缺失到酶活和耗氧的因果，不把表达等同通量。
- 高被引条件：25次，年均13.389；OpenAlex，查询2026-10-24，原始缓存`raw/openalex/F01_page_000.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 16. R10086 — Effect of micro-aeration on syntrophic and methanogenic activity in anaerobic sludge

- 年份/期刊/DOI：2024；Applied Microbiology and Biotechnology；https://doi.org/10.1007/s00253-023-12969-4
- 来源及原库关联：['Original AD library', 'PubMed']；查询ID ['OLD554', 'P04', 'P13']；原库ID ['R10086']；初筛批次 P005。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：厌氧污泥互营/产甲烷活性与O2耗用、乙醇保护，优先共培养/代谢候选。本轮更明确的阅读理由：乙醇与直接产甲烷底物O2剂量响应不同，可拆分发酵伙伴作用。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=R10086]/abstract_enriched`。
- 微生物/AD条件：厌氧污泥互营/产甲烷菌；好氧/兼性菌；直接AD污泥及互营功能相关；乙醇与乙酸/H2-CO2底物对比与AD过程有明确联系。
- 机制证据仍仅由摘要报告：0–5%顶空O2、底物消耗、甲烷速率及耗氧测量。需核实：耗氧与较轻抑制支持伙伴保护，但不是已做逐一伙伴删除的因果证明；不能外推全部底物。
- 高被引条件：16次，年均5.873；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_00998003b34a42.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 17. OR-E551A6ADF474 — Duration of O2 Exposure Determines Dominance of FeII vs CH4 Production in Tropical Forest Soils.

- 年份/期刊/DOI：2025；Environmental science & technology；https://doi.org/10.1021/acs.est.4c12329
- 来源及原库关联：['PubMed', 'OpenAlex']；查询ID ['P07', 'O01']；原库ID []；初筛批次 P024。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：土壤氧暴露时长决定铁/甲烷优势，剂量与恢复边界重点；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：不同氧期时长改变竞争优势，且有13C-DNA示踪。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-E551A6ADF474]/abstract_enriched`。
- 微生物/AD条件：土壤铁还原菌Anaeromyxobacter及产甲烷群落；功能竞争可类比AD；非AD同种/属已核实；Fe(III)电子受体、热带土矿物与液态AD不同。
- 机制证据仍仅由摘要报告：固定6 d无氧、8/24/72 h有氧；Fe/CH4和13C示踪。需核实：较长氧期后甲烷更多不等于O2直接促进产甲烷菌；铁还原竞争及矿物库需分开。
- 高被引条件：6次，年均3.634；OpenAlex，查询2026-10-24，原始缓存`raw/openalex/O01_page_000.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=11.3；JCR类别/分区=[{"category": "ENGINEERING, ENVIRONMENTAL", "quartile": "Q1"}, {"category": "ENVIRONMENTAL SCIENCES", "quartile": "Q1"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=zk&id=3966；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_6.json`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 18. OR-5D303857796F — The Fumarate Reductase of Bacteroides thetaiotaomicron, unlike That of Escherichia coli, Is Configured so that It Does Not Generate Reactive Oxygen Species.

- 年份/期刊/DOI：2017；mBio；https://doi.org/10.1128/mbio.01873-16
- 来源及原库关联：['PubMed']；查询ID ['P03', 'P10']；原库ID []；初筛批次 P013。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：B.thetaiotaomicron延胡索酸还原酶ROS生成特性，生化机制候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：直接排除一个看似合理ROS源，避免从E.coli酶推广到所有厌氧菌。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-5D303857796F]/abstract_enriched`。
- 微生物/AD条件：Bacteroides thetaiotaomicron Frd；E.coli同源酶；非AD同种已核实；延胡索酸呼吸/红氧靶点可比；具体同源酶反应可迁移性有限；AD酶电子结构需单独核实。
- 机制证据仍仅由摘要报告：生化ROS测量、亚基互换及相关酶比较。需核实：电子密度转移是解释性假说；实际胞内ROS主要来源仍未确定，不写全部Frd都清氧或都产ROS。
- 高被引条件：40次，年均4.081；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_652161c1add374.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
  - 配对阅读指针：10.1099/mic.0.054403-0；本池B.fragilis Frd产ROS研究标题提供反例比较指针；未核其全文及团队，不能当本篇同对象复制。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 19. OR-C63E5057C2A6 — Mechanism of oxygen detoxification by the surprisingly oxygen-tolerant hyperthermophilic archaeon, Pyrococcus furiosus.

- 年份/期刊/DOI：2012；Proceedings of the National Academy of Sciences of the United States of America；https://doi.org/10.1073/pnas.1208605109
- 来源及原库关联：['PubMed']；查询ID ['P02']；原库ID []；初筛批次 P017。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：P.furiosus O2耐受与H2循环解毒，古菌代谢重点；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：缺失株加生理产物变化，且有rubredoxin/H2酶阴性结果。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-C63E5057C2A6]/abstract_enriched`。
- 微生物/AD条件：Pyrococcus furiosus；SOR及putative FDP_A；非AD典型类群；Fd/H2/防御靶点可比；超嗜热发酵古菌不是产甲烷古菌，仅共享具体还原力/清氧问题。
- 机制证据仍仅由摘要报告：SOR/FDP_A/氢化酶/rubredoxin缺失，O2消耗及H2产量。需核实：不同类群支持不能当AD古菌同对象复制；rubredoxin非必要性有条件，完整电子路线仍有限。
- 高被引条件：62次，年均4.413；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_b6de20b010a87e.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：已有不同团队跨类群/体系原始支持（沿用旧表、暂定）；未确认本篇具体电子路线或同对象独立重复；严格同对象/同主张独立重复未确认。
  - 复用旧表 CL04：10.1111/febs.17040 ↔ 10.1073/pnas.1208605109；不同团队跨类群原始支持（暂定）；具体主张：FDP家族可参与厌氧微生物耐氧；限制：摘要核验；putative FDP_A，不同类别；不能替代S. wolfei细胞内验证。
  - 复用旧表 CL05：10.1128/jb.00175-24 ↔ 10.1073/pnas.1208605109；不同团队跨类群原始支持（暂定）；具体主张：SOR可参与O2/超氧防御；限制：当前两方相关主张以摘要核实，O2与超氧挑战不同；不验证AD古菌全部必要性。
  - 复用旧表 CL12：10.1128/aem.02491-15 ↔ 10.1073/pnas.1208605109；不同团队跨体系支持（暂定），非AOR/rbr特定机制验证；具体主张：氧解毒可与还原力/电子流重新分配相联系；限制：仅摘要；发酵底物/温度不同，不能验证C. ljungdahlii的AOR或乙醇路径。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 20. OR-3B1D70862C75 — Carbon dioxide and trace oxygen concentrations impact growth and product formation of the gut bacterium Phocaeicola vulgatus.

- 年份/期刊/DOI：2023；BMC microbiology；https://doi.org/10.1186/s12866-023-03127-x
- 来源及原库关联：['PubMed']；查询ID ['P03']；原库ID []；初筛批次 P028。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：Phocaeicola微量O2及CO2生长产物，发酵菌条件重点；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：在线气体与有机酸分析，提供可定位的低氧容忍窗口。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-3B1D70862C75]/abstract_enriched`。
- 微生物/AD条件：Phocaeicola vulgatus（原Bacteroides vulgatus）；非AD同种已核实；厌氧糖发酵/有机酸功能可比；肠菌培养CO2依赖和单菌底物不同于AD，不能照搬浓度阈值。
- 机制证据仍仅由摘要报告：RAMOS气体在线监测、CO2/O2浓度梯度与生长/产物。需核实：气相vol%不是液相DO；生存阈值和CO2交互需分开，不把耐氧当氧有益。
- 高被引条件：11次，年均3.819；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_d80f48727534bf.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 21. R13833 — Insight into the Role of Facultative Bacteria Stimulated by Microaeration in Continuous Bioreactors Converting LCFA to Methane

- 年份/期刊/DOI：2018；Environmental Science &amp; Technology；https://doi.org/10.1021/acs.est.8b00894
- 来源及原库关联：['Original AD library']；查询ID ['OLD554']；原库ID ['R13833']；初筛批次 P011。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：微曝气LCFA产甲烷兼性菌作用，AD互作重点候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：不同红氧条件与底物负荷比较，并报告暂时抑制后恢复。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=R13833]/abstract_enriched`。
- 微生物/AD条件：Pseudomonas spp.及脂酸转化/产甲烷群落；直接AD功能及兼性伴生菌相关；连续油酸/棕榈酸转化接近AD脂类问题；特定负荷与反应器边界。
- 机制证据仍仅由摘要报告：反应器比较、活性恢复、兼性菌分离及相关性。需核实：摘要明确很多证据为相关，不能把Pseudomonas丰度/分离当耗氧保护已证明；ORP不等于直接DO。
- 高被引条件：58次，年均6.869；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_5257422391c40d.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=11.3；JCR类别/分区=[{"category": "ENGINEERING, ENVIRONMENTAL", "quartile": "Q1"}, {"category": "ENVIRONMENTAL SCIENCES", "quartile": "Q1"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=zk&id=3966；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_6.json`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 22. OR-15A62A4556E3 — Single-Cell Analysis of Growth and Cell Division of the Anaerobe Desulfovibrio vulgaris Hildenborough.

- 年份/期刊/DOI：2015；Frontiers in microbiology；https://doi.org/10.3389/fmicb.2015.01378
- 来源及原库关联：['PubMed']；查询ID ['P12']；原库ID []；初筛批次 P015。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：D.vulgaris单细胞氧暴露可逆分裂阻断，恢复重点候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：直接观察氧暴露期间的细胞分裂，为群落不变但生理受抑提供依据。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-15A62A4556E3]/abstract_enriched`。
- 微生物/AD条件：Desulfovibrio vulgaris Hildenborough；AD硫酸盐还原功能/相同属可比；硫循环功能与AD相关，但同株在AD中的常见性及与产甲烷竞争条件未核。
- 机制证据仍仅由摘要报告：实时单细胞成像、O2暴露与分裂恢复。需核实：可逆停分裂是表型，不等于已确认保护性因果机制或遗传适应；作者may表述保留。
- 高被引条件：38次，年均3.493；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_b002cef5fd762b.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 23. OR-E05033DBC651 — Fortification of FeS Clusters Reshapes Anaerobic CO Dehydrogenase into an Air-Viable Enzyme Through Multilayered Sealing of O2 Tunnels.

- 年份/期刊/DOI：2025；Angewandte Chemie (International ed. in English)；https://doi.org/10.1002/anie.202508565
- 来源及原库关联：['PubMed']；查询ID ['P10']；原库ID []；初筛批次 P007。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：厌氧CODH的O2通道/FeS保护突变工程，直接氧敏感靶点机制候选。本轮更明确的阅读理由：对氧进入通道作定点工程，连接空间可达性与NiFe/FeS簇损伤。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-E05033DBC651]/abstract_enriched`。
- 微生物/AD条件：Carboxydothermus hydrogenoformans CODH2；非AD同种已核实；CODH低电位NiFe/FeS靶点可比；可比较AD含CODH的碳代谢靶点，但分离酶CO/CO2转化与群落甲烷不同。
- 机制证据仍仅由摘要报告：突变A559W/V610H、结构、空气半衰期及电酶反应。需核实：本池有对应通信条目，应配对读；未读通信内容，不能说争议已解决或原文被证伪。
- 高被引条件：5次，年均3.602；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_b22a4c3bfbf5e4.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
  - 配对阅读指针：10.1002/anie.1942100；本池对应通信条目；尚未读取内容，不能作为反证已成立。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 24. OR-82F6FC6E3A3E — Role of Superoxide Reductase FA796 in Oxidative Stress Resistance in Filifactor alocis.

- 年份/期刊/DOI：2020；Scientific reports；https://doi.org/10.1038/s41598-020-65806-3
- 来源及原库关联：['PubMed']；查询ID ['P02']；原库ID []；初筛批次 P006。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：Filifactor SOR突变提高O2/空气敏感性，重要遗传防御候选。本轮更明确的阅读理由：SOR既有重组酶活又有缺失株氧/空气存活差异。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-82F6FC6E3A3E]/abstract_enriched`。
- 微生物/AD条件：Filifactor alocis ATCC35896；FA796-SOR；非AD常见同种/属已核实；SOR防御系统类比；口腔厌氧菌可提供酶家族因果模板，AD类群是否同样依赖SOR待核。
- 机制证据仍仅由摘要报告：FA796缺失、重组超氧还原、氧/空气及H2O2应激。需核实：必须把O2与H2O2试验分开，不能泛化SOR对全部AD类群必要。
- 高被引条件：24次，年均3.764；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_2d3b26d0b89c1a.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 25. R13274 — Micro-aeration enhances lactic acid production in food waste fermentation

- 年份/期刊/DOI：2026；Bioresource Technology；https://doi.org/10.1016/j.biortech.2025.133807
- 来源及原库关联：['Original AD library']；查询ID ['OLD554']；原库ID ['R13274']；初筛批次 P003。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：乳酸发酵供氧剂量＋宏转录及Lactobacillus相关路径，优先酸化代谢候选。本轮更明确的阅读理由：含中度促进与过量抑制，兼有产物及转录，适合区分生理与功能潜力。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=R13274]/abstract_enriched`。
- 微生物/AD条件：Lactobacillus amylolyticus及食品废物混合发酵群落；AD上游水解酸化功能相关；非产甲烷全过程；乳酸发酵目标与最大甲烷产量不同，氧导致碳流保留/消耗须核。
- 机制证据仍仅由摘要报告：四曝气负荷、半连续反应器、乳酸/效率及宏转录组。需核实：通路转录不等于酶活/净通量已证实，不能声称同剂量必然提升后续AD甲烷。
- 高被引条件：2次，年均2.0；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_1b961c2c407979.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=9.0；JCR类别/分区=[{"category": "AGRICULTURAL ENGINEERING", "quartile": "Q1"}, {"category": "AGRICULTURAL ENGINEERING", "quartile": "Q1"}, {"category": "BIOTECHNOLOGY & APPLIED MICROBIOLOGY", "quartile": "Q1"}, {"category": "ENERGY & FUELS", "quartile": "Q1"}]；有2024机构缓存值；未约定高影响阈值，不判已达标。来源：https://topj.lib.whu.edu.cn/show.asp?cat=zk&id=3976；快照：`../inventory/merge_20261023/jcr_sources/jcr_search_0.json`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 26. OR-631665AE20A2 — Pulses of labile carbon cause transient decoupling of fermentation and respiration in permeable sediments.

- 年份/期刊/DOI：2023；Limnology and oceanography；https://doi.org/10.1002/lno.12411
- 来源及原库关联：['PubMed']；查询ID ['P06']；原库ID []；初筛批次 P019。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：沉积物氧暴露/物理扰动/碳输入对H2，代谢解耦候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：同时考察氧、机械扰动与碳，氧效应小而剧烈振荡有影响。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-631665AE20A2]/abstract_enriched`。
- 微生物/AD条件：海洋沉积物发酵菌与硫酸盐还原菌；AD发酵-H2互作功能可比；非同种已核实；海泥以硫酸盐呼吸为主，AD终端产甲烷不同。
- 机制证据仍仅由摘要报告：野外H2、流槽与O2/物理/有机物实验。需核实：不能把碳脉冲或机械裂解引起H2积累归于氧抑制；快速恢复解释仍需核实活动分辨。
- 高被引条件：2次，年均0.619；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_b22a4c3bfbf5e4.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 27. OR-E0944369CA6F — Solution structure and biochemical characterization of a spare part protein that restores activity to an oxygen-damaged glycyl radical enzyme.

- 年份/期刊/DOI：2019；Journal of biological inorganic chemistry : JBIC : a publication of the Society of Biological Inorganic Chemistry；https://doi.org/10.1007/s00775-019-01681-2
- 来源及原库关联：['PubMed']；查询ID ['P10', 'P15']；原库ID []；初筛批次 P006。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：氧损伤甘氨酰自由基酶的备用蛋白结构/恢复活性，优先修复机制。本轮更明确的阅读理由：具体修复蛋白结构与截短PFL相容性，帮助设计修复机制论证。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-E0944369CA6F]/abstract_enriched`。
- 微生物/AD条件：Escherichia coli YfiD/PFL；AD发酵通路/氧敏自由基酶可比，非AD同种已核实；PFL参与甲酸/乙酰CoA产生；AD菌YfiD同源性和体内修复未核。
- 机制证据仍仅由摘要报告：NMR/CD、PFL模拟氧损伤变体、蛋白水解与结构模型。需核实：模型与模拟损伤不能当AD完整细胞氧后恢复；与2021/2022研究须核团队与实验差别。
- 高被引条件：18次，年均2.457；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_00998003b34a42.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
  - 配对阅读指针：10.1016/j.jbc.2021.101423；后续酶学候选；不据年份或不同DOI认定独立团队。
  - 配对阅读指针：10.1128/jb.00070-22；体内遗传模型候选；对象/处理不同，非直接独立复制已核。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 28. OR-A47D88A5BD92 — A Point Mutation in the Transcriptional Repressor PerR Results in a Constitutive Oxidative Stress Response in Clostridioides difficile 630Δerm.

- 年份/期刊/DOI：2021；mSphere；https://doi.org/10.1128/msphere.00091-21
- 来源及原库关联：['PubMed']；查询ID ['P02', 'P03']；原库ID []；初筛批次 P008。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：C.difficile PerR单碱基变异与耐氧表型，重要遗传调控候选，非直接演化适应证明。本轮更明确的阅读理由：单核苷酸变异及互补可解释实验室参考株耐氧偏高，警示菌株选择。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-A47D88A5BD92]/abstract_enriched`。
- 微生物/AD条件：Clostridioides difficile 630及630Δerm；PerR/rbr1；非AD常见同种/属已核实；PerR/rubrerythrin防御可比较；不能因同属Clostridia就判高度AD相关；需核AD目标菌同源系统。
- 机制证据仍仅由摘要报告：PerR位点变异、DNA结合、rbr1表达及野生型PerR引入。需核实：实验室株特例不代表AD群落演化适应；H2O2感应调控与氧耐受效应要分开。
- 高被引条件：18次，年均3.193；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_652161c1add374.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 29. OR-CEDAA95DD383 — Oxygen-mediated growth enhancement of an obligate anaerobic archaeon Thermococcus onnurineus NA1.

- 年份/期刊/DOI：2019；Journal of microbiology (Seoul, Korea)；https://doi.org/10.1007/s12275-019-8592-y
- 来源及原库关联：['PubMed', 'OpenAlex']；查询ID ['P02', 'O02']；原库ID []；初筛批次 P016。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：T.onnurineus氧促进依底物改变，直接古菌生理边界；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：O2促进依赖酵母浸粉底物，适合反驳简单厌氧菌遇氧全抑制。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-CEDAA95DD383]/abstract_enriched`。
- 微生物/AD条件：Thermococcus onnurineus NA1；非AD典型类群；发酵/红氧平衡靶点可比；超嗜热、非产甲烷且无heme/cytochrome，不能直接代表AD古菌。
- 机制证据仍仅由摘要报告：不同底物O2生长及转录组。需核实：清氧再生NAD(P)+为plausible机制，转录上调不等于必要性或电子流已直接证明。
- 高被引条件：5次，年均0.647；OpenAlex，查询2026-10-24，原始缓存`raw/openalex/O02_page_000.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 30. OR-071CAFC18C32 — Dietary fiber fermentation restores microbiome resilience to oxygen stress in a host-independent ex vivo model.

- 年份/期刊/DOI：2026；mBio；https://doi.org/10.1128/mbio.03934-25
- 来源及原库关联：['PubMed']；查询ID ['P14']；原库ID []；初筛批次 P003。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：无宿主肠道模型中氧压力与纤维发酵恢复，适合交叉营养/底物保护候选。本轮更明确的阅读理由：有四组O2/纤维因子设计和SCFA/pH，可分离宿主影响。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-071CAFC18C32]/abstract_enriched`。
- 微生物/AD条件：Eubacterium/Roseburia/Bifidobacterium及Enterobacteriaceae等离体粪菌；AD发酵功能可类比；非AD相同群落已核实；宿主外发酵便于机制拆分；降pH在AD可能抑制甲烷，不能直接套促进结论。
- 机制证据仍仅由摘要报告：0/5% O2与±纤维、SCFA/pH及16S。需核实：CAG共丰度群不等于直接互作；酸化是否必要/充分需控制，恢复不等于遗传适应。
- 高被引条件：1次，年均1.0；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_652161c1add374.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 31. OR-3A00C82F8A2B — Rescuing activity of oxygen-damaged pyruvate formate-lyase by a spare part protein.

- 年份/期刊/DOI：2021；The Journal of biological chemistry；https://doi.org/10.1016/j.jbc.2021.101423
- 来源及原库关联：['PubMed']；查询ID ['P10']；原库ID []；初筛批次 P006。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：氧损伤PFL后备用蛋白恢复活性，优先修复机制候选。本轮更明确的阅读理由：酶活/光谱与截短干预区分损伤程度和可修复窗口。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-3A00C82F8A2B]/abstract_enriched`。
- 微生物/AD条件：细菌PFL/YfiD（模型蛋白体系，菌种仍核方法）；AD发酵PFL靶点可比；具体AD菌同源未核实；可说明氧敏自由基酶修复而非只新生合成，不能替代群落证据。
- 机制证据仍仅由摘要报告：酶学/光谱、YfiD端部及PFL截短干预。需核实：分离酶氧损伤修复，不证明所有AD菌均能修复；与2019/2022研究不预设独立。
- 高被引条件：11次，年均2.231；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_5b4fe46b1bfb43.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
  - 配对阅读指针：10.1007/s00775-019-01681-2；摘要自述此前结构工作；同团队/独立性仍须作者与方法核查。
  - 配对阅读指针：10.1128/jb.00070-22；体内模型候选；不能把失活突变体与氧损伤等同。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 32. OR-7018E028D4E6 — Characterization of the Bacteroides fragilis bfr gene product identifies a bacterial DPS-like protein and suggests evolutionary links in the ferritin superfamily.

- 年份/期刊/DOI：2012；Journal of bacteriology；https://doi.org/10.1128/jb.05260-11
- 来源及原库关联：['PubMed']；查询ID ['P03']；原库ID []；初筛批次 P009。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：B.fragilis bfr缺失降低耐氧，优先铁稳态/遗传防御候选。本轮更明确的阅读理由：bfr缺失耐氧下降并有DNA自由基保护，连接金属和损伤。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-7018E028D4E6]/abstract_enriched`。
- 微生物/AD条件：Bacteroides fragilis；bfr/DPS-like蛋白；非AD同种已核实；铁稳态/DNA保护靶点可比；肠道病原及铁储存方式与AD菌可能不同，不凭铁蛋白家族泛化。
- 机制证据仍仅由摘要报告：bfr null突变、O2/铁表达、体外DNA保护与晶体结构。需核实：O2存活和羟自由基DNA裂解是不同证据；体外保护不等于AD细胞内普遍必要。
- 高被引条件：36次，年均2.399；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_d67f680d5c898c.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 33. OR-52D6CC670C6A — Rational engineering of facultative anaerobiosis enables commensal survival in the oxygenated gut.

- 年份/期刊/DOI：2026；bioRxiv : the preprint server for biology；https://doi.org/10.64898/2026.06.05.730451
- 来源及原库关联：['PubMed', 'OpenAlex']；查询ID ['P03', 'P08', 'F01']；原库ID []；初筛批次 P013。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：工程修复厌氧共生菌氧敏代谢，潜在因果重点候选；基于题名/所示摘要关键句，未全文核实。。本轮更明确的阅读理由：多靶点修复候选可整合中心代谢/合成/红氧限制，保留新近研究。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-52D6CC670C6A]/abstract_enriched`。
- 微生物/AD条件：Bacteroides thetaiotaomicron工程菌；非AD同种已核实；可迁移代谢靶点待方法核查；肠菌/炎症宿主环境与AD不同；多靶点策略不能直接移植AD菌。
- 机制证据仍仅由摘要报告：摘要报告多组学及理性修复、10% O2生长。需核实：预印本未全文/同行评审核实；PubMed主DOI与OpenAlex来源DOI不同需身份映射，引用缺失不能写0。
- 高被引条件：缺失次，年均缺失；OpenAlex，查询未取得，原始缓存`无匹配`；引用缺失，无法判断。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；预印本不适用期刊JIF，不能按拟投期刊评价。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
  - 配对阅读指针：10.64898/2026.06.05.730451；PubMed主记录预印本DOI。
  - 配对阅读指针：10.2139/ssrn.6997560；OpenAlex前向来源DOI不同；版本身份待核，不当第二独立研究。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 34. OR-C78553A0F4D0 — The extracytoplasmic function sigma factor EcfO protects Bacteroides fragilis against oxidative stress.

- 年份/期刊/DOI：2013；Journal of bacteriology；https://doi.org/10.1128/jb.01491-12
- 来源及原库关联：['PubMed']；查询ID ['P03']；原库ID []；初筛批次 P009。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：B.fragilis EcfO氧化应激保护遗传调控，防御机制候选。本轮更明确的阅读理由：调控因子与抗sigma伙伴有删除和互作，较纯组学更直接。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-C78553A0F4D0]/abstract_enriched`。
- 微生物/AD条件：Bacteroides fragilis EcfO/Reo；非AD同种已核实；应激调控靶点可比但分布有限；EcfO靶脂蛋白局限Bacteroidetes，不能泛化产甲烷古菌或所有AD菌。
- 机制证据仍仅由摘要报告：ecfO/reo缺失、蛋白互作、染色质结合及氧暴露。需核实：不同氧化胁迫须分开；需核存活设计、互补和靶基因功能，不把表达网络当全因果。
- 高被引条件：27次，年均1.931；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_d67f680d5c898c.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

### 35. OR-454A09DABEFE — New Electron-Transfer Chain to a Flavodiiron Protein in Fusobacterium nucleatum Couples Butyryl-CoA Oxidation to O2 Reduction.

- 年份/期刊/DOI：2024；Biochemistry；https://doi.org/10.1021/acs.biochem.4c00279
- 来源及原库关联：['PubMed']；查询ID ['P02']；原库ID []；初筛批次 P007。逐来源原始文件及PMID在JSON/Excel的source_record_provenance。
- 初筛类别：核心候选；规范解释：范围相关/机制潜力初筛候选；非已确认核心文献。当前边界：范围相关/机制潜力初筛候选，待全文及具体主张核实。
- 原入队理由：Fusobacterium从丁酰CoA氧化到FDP还原O2的直接电子链，是新代谢/解毒候选。本轮更明确的阅读理由：把发酵中间体电子流与O2还原连接，有重构复合体与快速动力学。
- 阅读深度：入队时题名及摘要关键句语义审阅（未阅读全文）；当前本轮完整缓存摘要已读；全文方法/结果未核实。缓存定位：`all_pool/metadata_enrichment.json` 的 `[id=OR-454A09DABEFE]/abstract_enriched`。
- 微生物/AD条件：Fusobacterium nucleatum subsp.polymorphum ATCC10953；BCR-FDP；非AD常见同种/属已核实；丁酰CoA/Etf/FDP靶点可比；可迁移具体电子链思路，不因同为厌氧发酵菌就判高度AD相关。
- 机制证据仍仅由摘要报告：复合体、FAD半醌光谱、stopped-flow及O2→H2O选择性。需核实：离体链条不等于已证明菌体或AD群落中保护贡献；基因共现不能独立验证该功能。
- 高被引条件：7次，年均3.253；OpenAlex，查询2026-10-24，原始缓存`all_pool/raw/openalex_0ed8f781870296.json`；引用数可核，但无统一阈值/同年领域基准，未判高被引达标。
- 期刊影响力条件：JIF2024=空；JCR类别/分区=[]；2024指标未核实，暂无法判断；不阻塞范围筛选。来源：未核实；快照：`无`。
- 独立验证条件：未核实独立支持/反例链；不声称不存在，也不据引用或综述数认定广泛验证；严格同对象/同主张独立重复未确认。
- 四项合并结论：当前不能确认四项同时满足；不是四项均不符合的结论。队列身份：优先阅读队列，非已确认核心文献。

## 下载与继续工作

- [同一累计Excel](../oxygen_response_review_cumulative.xlsx)：新增“35篇来源与条件”“35篇评价口径”“其他候选续核”，原20评价保留。
- [35篇CSV](source_conditions_audit_utf8.csv)／[JSON](source_conditions_audit.json)；[原35队列快照](baseline_queue35.json)；[本轮摘要阅读日志](abstract_reading_log.json)。
- [其余312条范围相关候选CSV](other_in_scope_continuation_queue_utf8.csv)／[JSON](other_in_scope_continuation_queue.json)。它们仍待核实，35不是截断线；其他条目可进入队列。累计479待确认、336背景及原20各自状态继续保留。
- 原[35条RIS](../all_pool/new_focus_set.ris)仍是阅读队列导入文件，不是终选核心集。
- 四项条件的缺口按具体主张补证；没有重新检索或重复查询原20指标，没有新的全文核实或独立验证断言。
