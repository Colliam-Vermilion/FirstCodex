> **35条队列来源与条件补充说明**：[逐篇核对](reading_queue35/README.md)。35条不是已确认核心文献，也不是引用/JIF前35或四项全达标集；本轮已补读35条完整缓存摘要，仍未核全文。9条有2024 JIF缓存、25条未核实、1条预印本不适用；独立验证按具体主张保留未核实及已有部分支持。其余312条范围相关候选继续核实，35不是最终数量上限。

# 当前：全池优先级阶段完成首遍初筛（2026-10-24）

本轮已按新的工作顺序处理全部1536条：复用原20篇，新增1516条逐项题名/摘要关键句初筛，未开始0条；**不代表完整摘要或全文核实**。新增347候选、477待确认、336背景、356排除。原20篇评价原样保留。OpenAlex引用可用1459条，缺失77条；按543个期刊/ISSN缓存键统一匹配，412条有已有2024期刊指标，其余留空，未重复查询原20指标。

- **[同一累计Excel](oxygen_response_review_cumulative.xlsx)** · **[全池阶段说明与边界](all_pool/README.md)** · [当前机器进度](all_pool/progress.json)
- [364条暂定优先CSV](all_pool/provisional_priorities_utf8.csv) · [RIS](all_pool/provisional_priority_set.ris) · [35条新增重点续跑顺序](all_pool/next_stage_queue_utf8.csv)
- [全池逐项判断](all_pool/semantic_screening_records_utf8.csv) · [479条累计待确认](all_pool/pending_confirmation_queue_utf8.csv) · [336条背景追溯](all_pool/background_trace_queue_utf8.csv)

下一阶段优先补读新35条的方法/结果，原17推荐复用；新增独立验证未核实，不将候选当机制已证实。没有重新发现检索、重复下载原件或更改原AD分类/人工判断。31个检查点已分批推送原结果分支。元数据阶段实测48.25秒；没有完整语义筛选耗时测量。

下方为此前B001及原20评价的**历史阶段说明**，其中“1516未筛”“后续从第21条开始”等旧进度已经由上面的全池进度替代；历史检索边界、证据来源和原20内容仍保留。

---

# 新增：优先精读五维评价（2026-10-24）

已先评价B001全部20篇，保留所有既有检索/筛选/队列及原六表。新增“优先精读”“机制验证关联”“评价口径”三个工作表；推荐17篇（6核心、4基础、7边界），8篇仅摘要支持并标暂定，3篇暂缓而非范围排除。20篇统一OpenAlex引用数据；11篇有可复用2024 JIF/JCR，缺失留空。没有用指标抵消证据不足。

- **[同一累计Excel](oxygen_response_review_cumulative.xlsx)** · **[精读集RIS17](reading_priority/priority_reading_set.ris)** · [逐篇五维CSV](reading_priority/priority_reading_utf8.csv)
- [推荐理由/适用边界/独立验证说明](reading_priority/README.md) · [26行具体机制验证关联](reading_priority/mechanism_validation_links_utf8.csv) · [评价口径](reading_priority/evaluation_policy_utf8.csv) · [评价进度](reading_priority/progress.json)

不同团队跨类群支持与同对象严格独立复制分开；本轮未确认后者，不代表文献中不存在。原“重点阅读”粗排保留，本次优先级以新增工作表为准。后续新增已筛文章再增量评价，不重检索或推进未筛队列。

---

# 厌氧微生物氧响应机制：B001完成（2026-10-24）

从最新远端`2c4aa35daca259bdc311cd54d720e5627ada5ba0`读取README、554条133列总库、既有检索和原件。此为独立新范围，包含非AD机制研究；旧AD分类、53条人工判断、原件、omics和JCR结果保持原字节，不沿用128条旧AD排除作为本轮排除。完整保护核验见[validation.json](validation.json)。

## 实际完成量

|来源/步骤|实际返回记录（可含跨查询重复）|执行边界|
|---|---:|---|
|PubMed 17组主题查询|732|完整ID列表及全部EFetch批次；2012-01-01至2026-10-24|
|Crossref 3组|300|每组前100相关性结果；报告总量与未取回尾部另存，不宣称穷尽|
|OpenAlex 3组|79|64/10/5，cursor均自然结束|
|后向已知PMID核验|4|来自实际读到的2020原研究参考文献，含3篇2012年前文献|
|OpenAlex前向引用|32|同一原研究种子，完整分页|
|合计|1147|全部成功返回原始文件及逐输入映射已保存|

规范化DOI、PMID及题名去重为**1039个返回身份**，57个关联原库、982个为原库外候选；另14条题名/DOI冲突审计项保持分开待核，不当作已解析同文。原554条全部进入新范围关联池，因此累计表为**1536条**＝原554＋新982，包含497条本轮未重新命中的原库记录。1536不是纳入数。

首批20逐篇保存：**17核心范围、1离体酶学机制证据、2待确认、0明确排除**。阅读依据为10篇相关全文Methods/Results段落、10篇仅题名/摘要；筛选阶段为全文核实9、摘要初筛9、待确认2，待确认的两篇分别已读相关全文和仅摘要。没有声称20篇阅读全文。20条综合机制行允许多标签，标签数不是独立研究数。

Nature Academic Search完整固定版本已复用：stdio列出16工具，但实际检索内部errors有来源错误；独立CLI遇429。正式检索通过成功的官方API完成。Europe PMC搜索成功、两篇全文XML返回500，改用NCBI PMC；其中6个NCBI XML只有front而无body，仍按摘要记录。未使用WoS或Scopus付费访问，不假定机构登录，不下载测序原始数据。

## 下载与核查

- **[累计Excel](oxygen_response_review_cumulative.xlsx)**：文献总表、机制证据、重点阅读、检索日志25项、引文追溯85项、续跑队列。
- [首批20结果CSV](batch_B001_results_utf8.csv)、[20条机制证据CSV](mechanism_evidence_utf8.csv)／[JSON](mechanism_evidence.json)、[优先阅读清单](priority_reading_utf8.csv)。包含处理/对照、原始剂量单位、时间/频率、底物、方法、响应、证据性质、短引/定位、限制及AD外推边界。
- [全池文献CSV](literature_master_utf8.csv)／[JSON](catalog.json)、[逐输入去重映射](dedup_input_mapping_utf8.csv)、[身份冲突](identity_conflicts.json)、[新旧范围分离及原库SHA](baseline.json)。
- **[首批EndNote RIS](oxygen_response_B001.ris)**，含待确认状态；[全池RIS](oxygen_response_all_candidates.ris)含大量未筛记录，不能当纳入库。这两个RIS为替代导入，不要同时重复导入。EndNote选择Reference Manager (RIS)、Unicode (UTF-8)。尚未在Windows EndNote软件中实际导入，文件结构及ID集合已校验。
- [机制发现、证据边界和综述框架](MECHANISM_SYNTHESIS_zh.md)、[检索/续跑协议](PROTOCOL_zh.md)、[检索日志](search_log_utf8.csv)、[真实扩词与原因](term_expansions.json)、[来源状态](source_availability.json)。
- [原始返回](raw/)、[API访问时间/URL/字节SHA](request_log.jsonl)、[逐原件来源及SHA](source_document_register.json)、[逐段/页文本定位](evidence_sources/)。两个既有AD PDF直接复用现有original_files；未复制另套原件。其余全文XML与摘要响应按实际内容分级，XML路径名不代表已有正文。official_url是官方记录/DOI参考链接；是否实际访问出版商HTML不由此推定，实际请求看request_log，旧PDF为读取Git原件。

## 当前疑点与下一批

OR-6FAF906F2BA4（PMID38580315）全文依ORP/气压推断氧侵入，未直接测O2；AQDS和硒蛋白组的因果贡献未分离。R11680独立重审后仍需氧对照：摘要只有起始残留氧，干预主要为真菌/生物炭，不据电容或菌属丰度认定DIET。详见机制说明。

剩余**1516条未筛池**＝本轮返回中尚未筛的1019条＋497条未重新命中的原库记录，保存在[CSV](remaining_queue_utf8.csv)／[JSON](remaining_queue.json)。从冻结顺序21 **OR-A62BB0EB055B**开始，后续“继续下一批”只读本轮进度和必要证据，不重新检索、不重做本20篇。各条的词提示仅为排队，不作范围判定。2篇待确认单列补证，不视为阴性。

85条后向引文仅4项完成选定元数据核验，其余未处理；3篇早期原始研究（2001/2004/2008）单独标记并入队。前后向目前仅一个种子，Crossref不穷尽，瘤胃/地下环境、修复/遗传适应和直接空间保护仍是缺口。

累计表、RIS、40条短引位置和原库SHA均通过脚本验证。远端交付的独立读取结果见[remote_readback.json](remote_readback.json)。所有结果分批推送原结果分支；main不修改。
