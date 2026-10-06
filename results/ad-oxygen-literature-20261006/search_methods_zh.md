# 向厌氧消化系统主动引入氧气：检索方法与文献库说明

检索日期：2026-10-06（UTC）。发表范围：2012-01-01 至检索当天。最终统一文献库：400 条；已确认原始研究 145 条，综述 31 条，待全文确认候选 224 条。没有以目标文献数量或第一批结果作为停止条件。

## 最终记录与文件

| 类别 | 条数 | RIS 文件 |
|---|---:|---|
| 1 直接向 AD 反应器或内部循环供氧 | 92 | confirmed_original_research.ris |
| 2 向厌氧水解或产酸阶段供氧 | 27 | confirmed_original_research.ris |
| 3 独立好氧或微好氧预处理 | 26 | confirmed_original_research.ris |
| 4 综述 | 31 | reviews.ris |
| 待全文确认 | 224 | pending_fulltext_candidates.ris |

类别3与类别1/2在 Excel 中分开标记，但均属于已确认原始研究 RIS。相关会议论文及发表类型不明的记录保留在候选组，未混入已确认期刊原始研究。综述组包括供氧专题综述及明确讨论供氧的广义 AD 综述；后者在“待确认事项”列说明仅用于补充追溯。未能确认类型的潜在综述仍放候选组。

## 技能与实际工具

按照 nature-academic-search 的 multi-source-search 与 citation-file-mgmt 工作流实施；技能本地目录为项目的 `.agents/skills/nature-academic-search`，共享检索模块已安装。

实际检索及元数据核验来源为 OpenAlex、CrossRef、PubMed；开放全文补充使用 PMC。为了避免捆绑 MCP 搜索方法的小批量返回限制，系统检索由客户端直接调用技能对应来源的官方 API，执行完整 cursor/PMID ID 分页，使用相同的配置与已配置 PubMed 联系方式。直接 API 扩展脚本、原始响应和逐步日志已保存。MCP 在线检索另行进行了真实文献验证，而非用握手、HTTP 200 或格式转换代替检索成功。

实际 API 域名：`api.openalex.org`、`api.crossref.org`、`eutils.ncbi.nlm.nih.gov`。PMC 正文也通过 EUtilities efetch db=pmc 获取；DOI/出版社和 PMC 网页链接供用户访问，不能据此声称已访问出版社全文。

PubMed 按技能支持的本地运行配置使用此前授权的联系邮箱。邮箱没有复制到文献库、方法文件或复现包；复现需配置自己的 PUBMED_EMAIL 或技能支持的本地 config.toml。

未使用 Scopus 或 ScienceDirect 的付费 API。arXiv 已配置但不用于此处正式发表文章的主检索；未单独进行预印本数据库检索。Web of Science、Embase、Scopus、CNKI 和万方未覆盖。未把 Google Scholar 或 Semantic Scholar 当作已经成功检索的来源。

## 检索设计

从 AD/厌氧发酵/水解/产酸/产甲烷概念，与下列干预术语的拼写、复数和连字符变体组合：microaeration、micro-aeration、microaerobic、micro-aerobic、limited/controlled/intermittent/partial aeration、oxygen dosing/addition/supply/injection/oxygenation、air injection/addition/supply/sparging/dosing/mixing、microoxygenation/micro-oxygenation、microbubble/nanobubble/fine/ultrafine bubble、aerobic/microaerobic pretreatment。另用 biogas、anaerobic reactor/treatment/co-digestion、hydrolysis、acidification、hydrogen fermentation 扩展标题/摘要检索。

OpenAlex 使用 `title_and_abstract.search` 和明确的起止 publication_date，而不是仅搜索标题“微曝气”，也没有用全篇参考文献匹配所得大量噪声作为已筛选研究。G1—G10 每页200条，cursor 持续到空页/游标结束。PubMed 用 TIAB 通配及短语组合，日期用 Date - Publication；ESearch 获取完整 PMID 列表，EFetch 每批100条取摘要和书目信息。最大主查询2197条，未触发 PubMed 9999条的 ID 返回上限。

CrossRef 的 query.title 对多词/连字符具有宽松匹配，试探性多词查询可返回数万至数十万低相关记录。因此正式独立发现检索采用四个单词标题查询（microaeration、microaerobic、nanobubble、microbubble），每页1000条完整 cursor 分页；多词变体由 OpenAlex/PubMed 组合检索补足。这是 CrossRef 发现检索的覆盖限制，不声称四个单词查询穷尽了所有控制曝气文章。所有候选 DOI 另用 CrossRef `/works/{DOI}` 核验注册元数据，个别非 CrossRef DOI/失败保留而非编造。

P5 为缺摘要候选的 DOI→PubMed 查找，P6 为 OpenAlex 已给 PMID 但尚未读取 PubMed 记录的权威核验，不是独立发现检索。重跑相同查询使用已有原始响应缓存；整份 chronological search-log.jsonl 留存重复执行，Excel/search_log.csv 按相同来源、步骤、检索式、种子取最后一次执行，避免重复计算。

## 引文追溯

第一轮 23 个种子，第二轮 5 个新增种子，合计 28 个。包括核心供氧综述、相关原始研究，以及用于扩展但后续可能判为背景/范围外的候选；种子本身不等于纳入。种子完整名单、DOI、参考ID数和被引获取数见 citation_seeds.csv 与 Excel“引文种子”。

后向检索读取种子的 OpenAlex referenced_works，按每批50个ID查询，并执行2012年至检索日限制。前向检索使用 `cites:W...` 与同样日期过滤，每页200条 cursor 遍历，未限制被引条数。新增核心综述（包括2015年 H2S 微曝气综述）再次做一轮前向和后向检索。两轮归一化追溯文件分别包含 2731 与 529 条，文件内已按 OpenAlex ID 合并；与其他来源的重叠在总库继续去重。

没有逐篇对最终全部400条进行无限层级引文递归。OpenAlex 可能缺少某些文章的参考文献或被引链接；未索引/未解析参考无法自动覆盖。没有宣称达到严格的引文饱和或绝对找齐。

## 去重与筛选流程

跨来源按规范化 DOI 首先合并；同 PMID 合并；无 DOI 时以规范化完整题名、作者姓与相同/相邻发表年核对（在线与正式年可能相差1年）。另核对完全同题名的无 DOI 记录并完成 1 次补充合并。同题名但 DOI/作者/年份冲突的记录保留并标记，不盲目合并不同版本。元数据以出版社向 CrossRef 注册信息和读取到的 PubMed 记录优先；OpenAlex 用于补充摘要、缺失字段和引文图谱。

多来源与追溯合并后 13817 条唯一记录；广义范围预筛排除 12733 条，进入候选筛选 1084 条；候选阶段排除 683 条，再合并 1 条，留下 400 条。算式：1084 − 683 − 1 = 400。

范围筛选先由脚本按术语/场景辅助，随后结合题名、摘要及可得方法段核对并保存具体审计决定。不是独立双人系统综述筛选，不提供虚构的 inter-reviewer agreement。缺摘要或摘要无法确认主动供氧气体/位置/阶段的记录保留为“待全文确认”，不据题名推断具体供氧量或结果。

排除：明确的消化后好氧处理；独立外部沼气净化而未向消化器本体或其液体循环供氧；单纯 COD/元素含氧量/ROS 指标；非 AD 的生态、植物、生理耐氧研究；无主动供氧实验的意外暴露；仅用 H2/N2/CO2 的气泡组且无空气/O2组；臭氧、过氧化物等化学氧化但无主动空气/O2的干预；数据集、学位论文、书章、独立预印本版本等非目标发表记录。独立好氧/微好氧生物预处理进入类别3；仅以空气增强物理超声但尚未确认目标生物供氧实验的记录保留候选。

对多阶段文章按主要供氧阶段归类；直接 AD 与水解/产酸同时供氧时，类别及原文摘录反映其范围，待确认事项指出需要补足多组位置。填埋模拟器中为进入水解/产酸/产甲烷阶段而主动供氧的研究作为相关反应器形式保留；终止厌氧阶段后长期好氧稳定化排除。

## 年份与数据提取

“正式发表年份”采用 CrossRef published-print/正式期刊 published 日期及 PubMed 卷期年，在线发表年份在不同于正式年时另列。两篇正式卷期元数据为2027、在线日期为2026的记录保留，因为检索日之前已经在线发表，并标明两种年份；不是误将2027当成检索截止年。检索来源 date 过滤可能在在线/正式日期不一致时漏检，跨来源合并缓解但不能完全消除。

记录的作者逐个保留；题名、期刊、卷期、页码/文章编号和 DOI 不补造。364 条有 CrossRef 元数据核验，186 条实际读取 PubMed，两组有重叠；30 条未发现可核验 DOI，仍可通过 PMID/OpenAlex 或原始链接访问。

341 条具备摘要。尝试获取31篇 PMC 正文，最终库有 14 条已获取 PMC 全文，只有确实使用方法摘录的研究才标“全文方法段、摘要及元数据”；取得全文本身并不自动完成范围判定。其余全文状态区分“开放链接已发现”“未获取”和“已获取”。没有系统获取出版社付费全文或补充材料。

底物类型可以从明确题名或摘要识别；反应器、供氧位置、条件和结果主要保留英文来源摘录，方便复核。供氧条件列仅填写摘要/方法中明确的数值投加或 DO/ORP 条件，不将甲烷增幅当供氧剂量，不从相似文章借用参数。空白表示未核实，不表示零值或不适用。缺少完整方法时在待确认事项中说明。主要结果为来源摘要原文简述，不能视为已经完成独立复现实验或效果量抽取。

## 在线检索实际验证

nature-academic-search 的实际 MCP `search_papers(query="microaeration anaerobic digestion", sources=["pubmed"], rows=3)` 返回真实记录，包括：

- Enhancing Anaerobic Digestion of Agricultural By-Products: Insights and Future Directions in Microaeration. PMID 41155115；DOI 10.3390/bioengineering12101117。
- Review on microaeration-based anaerobic digestion: State of the art, challenges, and prospectives. PMID 31923694；DOI 10.1016/j.scitotenv.2019.136388。
- Enhanced anaerobic digestion performance and sludge filterability by membrane microaeration for anaerobic membrane bioreactor application. PMID 38703955；DOI 10.1016/j.biortech.2024.130787。

另通过 `get_paper_by_id(id="41155115", id_type="pmid")` 重新获取，核对题名和 PMID 完全一致且摘要非空；该 DOI 的题名同时得到 CrossRef 注册记录支持。验证保存为 mcp-verification.json。此三条的小规模调用仅是技能在线可用性验证，不构成系统检索结果上限。

## RIS 与 Excel 验证

三个 RIS 都使用 UTF-8，无 BOM。每条从 TY 开始、以 ER 结束；作者逐个 AU 字段。JOUR 用于期刊文章；已知会议记录用 CONF，类型未明确者用 GEN，并在 N1 说明。已确认原始研究、综述、候选三个分组互斥，其稳定ID的并集恰好等于Excel文献库；DOI 无重复。逐条核对题名、DOI、作者数量/顺序、年份及分组。保留可得摘要、期刊、卷期、页码或文章编号、URL；未知值不补造。

Excel 附“文献库”“统计与说明”“检索日志”“引文种子”“候选排除审计”，含完整摘要和核验URL。统计由 COUNTIF/SUM 链接文献库分类计算。导出后检查公式错误、实际单元格和预览，并检查 ZIP/XML 结构、表格记录ID与三个RIS的集合一致。

EndNote：打开目标库 → File → Import → File → 选择 RIS → Import Option 选择 Reference Manager (RIS)（若不在列表中，Other Filters 查找）→ Text Translation 选择 Unicode (UTF-8) → Import。建议先分别导入三个文件到不同组，保留候选组，避免将待确认当成已确认。软件本机导入未实际执行；文件级结构和内容已验证。

## 复现与后续全文核对

复现包包含归一化源记录、统一库、排除列表、检索日志、审计决定及 Python/JS 脚本。API原始响应和已获取PMC正文保存在当前环境的 ad-oxygen-review/raw、fulltext 目录；响应复现包另行提供，不包含邮箱和本地私有 config.toml。HTTP响应缓存名由请求哈希生成，原始API参数中联系邮箱不写入方法日志。

优先补取候选中的 Chemical Engineering Journal、Fuel、Renewable Energy、Journal of Cleaner Production 等工程学期刊摘要/全文；核对纳米气泡的气体类型与供氧阶段；对广義综述的微曝气小节逐篇补追；补充 WoS/Scopus/CNKI/万方可提高覆盖。已经保存统一稳定记录ID，后续可将候选改为确认并重新生成三个分组，避免从头开始。

当前结果是尽可能全面的多源可复核文献库，仍受来源索引、摘要/全文可得性、题名/摘要术语匹配与引文图谱覆盖限制；不承诺绝对完整。

## 完整检索式与条数

下表保留所有发现检索式及ID补查；API filter 与分页数见 search_log.csv。重复执行已合并。引文查询逐批及逐种子详见日志。

### PubMed P1_micro

```text
("anaerobic digestion"[tiab] OR "anaerobic fermentation"[tiab] OR "anaerobic hydrolysis"[tiab] OR acidogen*[tiab] OR methanogen*[tiab]) AND (microaerat*[tiab] OR "micro aeration"[tiab] OR "micro-aeration"[tiab] OR microaerob*[tiab] OR "micro aerobic"[tiab] OR "micro-aerobic"[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/06"[Date - Publication])
```

报告总数：129；实际获取：129；页数：ID列表后按100批取；状态：complete。

### OpenAlex G1_micro

```text
("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND (microaeration OR "micro-aeration" OR microaerobic OR "micro-aerobic" OR "micro aerobic" OR "micro aeration")
```

报告总数：259；实际获取：259；页数：2；状态：complete。

API filter：`title_and_abstract.search:("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND (microaeration OR "micro-aeration" OR microaerobic OR "micro-aerobic" OR "micro aerobic" OR "micro aeration"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### OpenAlex G2_dosing

```text
("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND ("oxygen dosing" OR "oxygen addition" OR oxygenation OR "air injection" OR "oxygen injection" OR "air addition" OR "oxygen supply")
```

报告总数：246；实际获取：246；页数：2；状态：complete。

API filter：`title_and_abstract.search:("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND ("oxygen dosing" OR "oxygen addition" OR oxygenation OR "air injection" OR "oxygen injection" OR "air addition" OR "oxygen supply"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### OpenAlex G3_controlled

```text
("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND ("limited aeration" OR "controlled aeration" OR "intermittent aeration" OR "low aeration" OR "partial aeration" OR "low oxygen" OR "oxygen limited")
```

报告总数：131；实际获取：131；页数：1；状态：complete。

API filter：`title_and_abstract.search:("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND ("limited aeration" OR "controlled aeration" OR "intermittent aeration" OR "low aeration" OR "partial aeration" OR "low oxygen" OR "oxygen limited"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### OpenAlex G4_bubbles

```text
("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND (nanobubble OR nanobubbles OR "nano-bubble" OR microbubble OR microbubbles OR "micro-bubble" OR "fine bubble")
```

报告总数：124；实际获取：124；页数：1；状态：complete。

API filter：`title_and_abstract.search:("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND (nanobubble OR nanobubbles OR "nano-bubble" OR microbubble OR microbubbles OR "micro-bubble" OR "fine bubble"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### PubMed P2_broad

```text
("anaerobic digestion"[tiab] OR "anaerobic fermentation"[tiab] OR "anaerobic hydrolysis"[tiab] OR acidogen*[tiab] OR methanogen*[tiab]) AND (oxygen*[tiab] OR aerat*[tiab] OR "air injection"[tiab] OR "air supply"[tiab] OR "air addition"[tiab] OR "air dosing"[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/06"[Date - Publication])
```

报告总数：2197；实际获取：2197；页数：ID列表后按100批取；状态：complete。

### PubMed P3_bubbles

```text
("anaerobic digestion"[tiab] OR "anaerobic fermentation"[tiab] OR "anaerobic hydrolysis"[tiab] OR acidogen*[tiab] OR methanogen*[tiab]) AND (nanobubbl*[tiab] OR microbubbl*[tiab] OR "nano bubble"[tiab] OR "micro bubble"[tiab] OR "fine bubble"[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/06"[Date - Publication])
```

报告总数：41；实际获取：41；页数：ID列表后按100批取；状态：complete。

### PubMed P4_pretreatment

```text
("anaerobic digestion"[tiab] OR "anaerobic fermentation"[tiab] OR "anaerobic hydrolysis"[tiab] OR acidogen*[tiab] OR methanogen*[tiab]) AND (aerobic[tiab] AND (pretreat*[tiab] OR "pre treatment"[tiab])) AND ("2012/01/01"[Date - Publication] : "2026/10/06"[Date - Publication])
```

报告总数：104；实际获取：104；页数：ID列表后按100批取；状态：complete。

### OpenAlex G5_broad

```text
("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND (aeration OR aerated OR oxygen OR "air sparging" OR "air dosing")
```

报告总数：5683；实际获取：5684；页数：29；状态：complete。

API filter：`title_and_abstract.search:("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND (aeration OR aerated OR oxygen OR "air sparging" OR "air dosing"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### OpenAlex G6_pretreatment

```text
("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND ("aerobic pretreatment" OR "aerobic pre-treatment" OR "microaerobic pretreatment" OR "biological desulfurization" OR "in situ desulfurization")
```

报告总数：79；实际获取：79；页数：1；状态：complete。

API filter：`title_and_abstract.search:("anaerobic digestion" OR "anaerobic fermentation" OR "anaerobic hydrolysis" OR acidogenesis OR methanogenesis) AND ("aerobic pretreatment" OR "aerobic pre-treatment" OR "microaerobic pretreatment" OR "biological desulfurization" OR "in situ desulfurization"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### OpenAlex G7_biogas

```text
(biogas OR "anaerobic reactor" OR "anaerobic treatment" OR "anaerobic co-digestion") AND (microaeration OR "micro-aeration" OR microaerobic OR aeration OR oxygenation OR "oxygen dosing" OR "air injection")
```

报告总数：1026；实际获取：1026；页数：6；状态：complete。

API filter：`title_and_abstract.search:(biogas OR "anaerobic reactor" OR "anaerobic treatment" OR "anaerobic co-digestion") AND (microaeration OR "micro-aeration" OR microaerobic OR aeration OR oxygenation OR "oxygen dosing" OR "air injection"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### OpenAlex G8_hydrolysis

```text
(hydrolysis OR acidification OR acidogenic OR "hydrogen fermentation") AND (microaeration OR "micro-aeration" OR microaerobic OR "micro-aerobic" OR "limited aeration" OR "oxygen dosing")
```

报告总数：203；实际获取：203；页数：2；状态：complete。

API filter：`title_and_abstract.search:(hydrolysis OR acidification OR acidogenic OR "hydrogen fermentation") AND (microaeration OR "micro-aeration" OR microaerobic OR "micro-aerobic" OR "limited aeration" OR "oxygen dosing"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### OpenAlex G9_bubbles

```text
(biogas OR "anaerobic co-digestion" OR "methane production" OR acidification) AND ("air nanobubble" OR "oxygen nanobubble" OR "O2 nanobubble" OR "oxygen microbubble" OR "ultrafine bubble")
```

报告总数：20；实际获取：20；页数：1；状态：complete。

API filter：`title_and_abstract.search:(biogas OR "anaerobic co-digestion" OR "methane production" OR acidification) AND ("air nanobubble" OR "oxygen nanobubble" OR "O2 nanobubble" OR "oxygen microbubble" OR "ultrafine bubble"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### CrossRef C1

```text
microaeration
```

报告总数：66；实际获取：66；页数：2；状态：complete。

API filter：`from-pub-date:2012-01-01,until-pub-date:2026-10-06,type:journal-article`

### CrossRef C2

```text
microaerobic
```

报告总数：295；实际获取：295；页数：2；状态：complete。

API filter：`from-pub-date:2012-01-01,until-pub-date:2026-10-06,type:journal-article`

### CrossRef C3

```text
nanobubble
```

报告总数：954；实际获取：954；页数：2；状态：complete。

API filter：`from-pub-date:2012-01-01,until-pub-date:2026-10-06,type:journal-article`

### CrossRef C4

```text
microbubble
```

报告总数：2770；实际获取：2770；页数：4；状态：complete。

API filter：`from-pub-date:2012-01-01,until-pub-date:2026-10-06,type:journal-article`

### OpenAlex G10_microoxygen

```text
("anaerobic digestion" OR biogas OR "anaerobic fermentation" OR acidogenesis OR "anaerobic hydrolysis") AND (microoxygenation OR "micro-oxygenation" OR "micro oxygen" OR "micro-oxygen" OR "oxygen-enriched" OR "air mixing" OR "micro-oxygen dosing")
```

报告总数：79；实际获取：79；页数：1；状态：complete。

API filter：`title_and_abstract.search:("anaerobic digestion" OR biogas OR "anaerobic fermentation" OR acidogenesis OR "anaerobic hydrolysis") AND (microoxygenation OR "micro-oxygenation" OR "micro oxygen" OR "micro-oxygen" OR "oxygen-enriched" OR "air mixing" OR "micro-oxygen dosing"),from_publication_date:2012-01-01,to_publication_date:2026-10-06`

### PubMed P5_DOI_abstract_1

```text
("10.1016/j.fuel.2022.123604"[AID] OR "10.1016/j.jwpe.2024.104814"[AID] OR "10.1016/j.cej.2025.172265"[AID] OR "10.1016/j.cej.2024.155731"[AID] OR "10.1016/j.renene.2022.06.106"[AID] OR "10.1016/j.cej.2024.151930"[AID] OR "10.1016/j.biotechadv.2012.11.005"[AID] OR "10.1016/j.cej.2015.11.070"[AID] OR "10.1016/j.cherd.2019.04.020"[AID] OR "10.1016/j.jece.2026.125159"[AID] OR "10.1016/j.renene.2026.126304"[AID] OR "10.1016/j.jclepro.2019.119651"[AID] OR "10.1007/978-3-031-28193-8_5"[AID] OR "10.1016/j.ijhydene.2016.01.141"[AID] OR "10.1007/s13399-019-00430-4"[AID] OR "10.1016/j.jece.2023.110163"[AID] OR "10.1016/j.cej.2025.163319"[AID] OR "10.1016/j.cej.2025.166351"[AID] OR "10.1016/j.cej.2025.166500"[AID] OR "10.1016/j.bej.2020.107873"[AID] OR "10.1016/j.jclepro.2021.126434"[AID] OR "10.1016/j.jwpe.2023.103643"[AID] OR "10.1016/j.jclepro.2026.147650"[AID] OR "10.1016/j.jece.2025.117766"[AID] OR "10.1016/j.bej.2017.06.009"[AID] OR "10.1016/j.biteb.2022.101265"[AID] OR "10.1016/j.renene.2021.09.089"[AID] OR "10.1016/j.biteb.2024.101949"[AID] OR "10.1007/s10163-020-01072-9"[AID] OR "10.2175/193864718824828948"[AID] OR "10.1016/j.renene.2025.124351"[AID] OR "10.1016/j.cej.2020.125652"[AID] OR "10.1016/j.cej.2023.147956"[AID] OR "10.1007/s12155-025-10889-x"[AID] OR "10.1016/j.renene.2025.123258"[AID] OR "10.1016/j.jwpe.2025.108560"[AID] OR "10.1007/s11164-023-05167-4"[AID] OR "10.1016/j.renene.2025.124921"[AID] OR "10.1016/j.cej.2025.171515"[AID] OR "10.1016/j.jclepro.2021.127942"[AID])
```

报告总数：1；实际获取：1；页数：ID列表后按100批取；状态：complete。

### PubMed P5_DOI_abstract_2

```text
("10.1016/j.rser.2021.111074"[AID] OR "10.1016/j.jwpe.2026.110326"[AID] OR "10.1016/j.biteb.2025.102484"[AID] OR "10.1016/j.cej.2025.164185"[AID] OR "10.1007/s11164-020-04250-4"[AID] OR "10.1007/s12649-016-9785-9"[AID] OR "10.1016/j.cej.2020.125116"[AID] OR "10.1016/j.cej.2016.11.020"[AID] OR "10.9786/kswm.2015.32.6.547"[AID] OR "10.22805/jit.2019.39.1.021"[AID] OR "10.1007/s13399-020-01124-y"[AID] OR "10.1016/j.psep.2026.109242"[AID] OR "10.1016/j.cej.2026.178822"[AID] OR "10.1016/j.cej.2025.165354"[AID] OR "10.1007/s11157-015-9386-2"[AID] OR "10.1016/j.jece.2026.123307"[AID] OR "10.2175/193864715819558758"[AID] OR "10.1016/j.seppur.2017.07.077"[AID] OR "10.1016/j.biortech.2013.05.084"[AID] OR "10.1016/j.biortech.2015.05.048"[AID] OR "10.1016/j.biortech.2014.05.058"[AID] OR "10.1016/j.cej.2014.04.027"[AID] OR "10.1016/j.biortech.2014.02.001"[AID] OR "10.1016/j.ibiod.2019.05.017"[AID] OR "10.1016/j.biortech.2014.04.109"[AID] OR "10.1016/j.jclepro.2018.11.253"[AID] OR "10.1016/j.memsci.2017.05.076"[AID] OR "10.1016/j.fuel.2021.121696"[AID] OR "10.1016/j.biortech.2012.12.114"[AID] OR "10.1016/j.jhazmat.2019.02.034"[AID] OR "10.1016/j.cej.2025.168425"[AID] OR "10.1016/j.fuel.2024.133456"[AID] OR "10.1016/j.biortech.2025.132425"[AID])
```

报告总数：8；实际获取：8；页数：ID列表后按100批取；状态：complete。

### PubMed P6_PMID_authority

```text
efetch db=pubmed id=22466581,28976998,37966187,34463202,22949260,34302159,30566095,39821078,29888986,32882933,31954086,22217090,27350297,26841606,40173215,41983979
```

报告总数：—；实际获取：16；页数：ID列表后按100批取；状态：complete。

OpenAlex G5 初报5683条、分页实际5684条，反映动态索引更新；不是人为多算一条。最终按 DOI/PMID/题名去重。
