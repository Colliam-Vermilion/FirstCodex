# 厌氧微生物空间结构与气体传质专题

本专题区分细胞／EPS／孔隙的结构、H₂/CH₄/O₂等浓度分布、传质参数与实际功能，并将产甲烷AD直接证据与Anammox、牙科生物膜、沉积物方法参照分开。**本轮在线补检尚未完成：2026-10-30四个官方API被当前环境代理以CONNECT 403拒绝。下面已完成的是对保存材料的实际本地专题检索、去重、阅读和证据提取，不能冒充已完成新的外部数据库检索。**

## 目前从证据能回答什么

- 2007年“Layered structure…”种子可从旧组学论文候选复用：摘要既有FISH类群定位又有H₂/CH₄/pH/ORP微剖面，报告H₂的Deff为2.66×10⁻⁵ cm²/s、约水中的57%。活性／失活材料、温度、拟合方法与尺寸待全文核查；不能把这个值当所有颗粒常数。
- R01414原件给出真正的ORP开关反馈：−310 mV开、−290 mV关，开阀0.14 mL/s纯氧，底部注入；未核实液相DO、累计供氧量或局部剖面。−320至−270 mV为实际运行范围，不能与开关阈值混用。负号经原PDF图像核对，文本抽取会漏负号。
- R03161操纵液面／润湿面积并测脱硫率；面积效应还可能含生物膜量或活性变化。Table1的g S/(m²·d)是表观反应去除率，不是Deff、kf、kLa或纯物理通量。
- 共培养的DO低于检出限时仍有空气输入，说明低主体DO不等于氧输入为零。记录DO不等于DO反馈控制；FISH聚集不等于已测到保护性微区。
- 本轮未新增已全文确认的CT／三维重建论文，也未取得真正絮体间的距离或通量实测。用户提供的3D CT种子和其他3个种子仍需联网独立核实，不按题名照写发现。

## 累计结果与阅读深度

[累计Excel](spatial_gas_transfer_cumulative.xlsx) · [文献与筛选CSV](literature_master_utf8.csv) · [JSON](literature_master.json) · [已处理相关文献RIS](spatial_gas_transfer_reviewed.ris) · [全部本地候选RIS](spatial_gas_transfer_candidates.ris)

总数与已处理数以[现行进度](progress.json)和[汇总](summary.json)为准。专题表是原库和组学关联记录的按ID视图，不另发重复文献ID，不改原范围／人工判断。未处理行明确“未开始”，没有把规则命中当成语义筛选完成。

|证据表|能读到什么|
|---|---|
|[三维结构与定位](structure_localization_evidence_utf8.csv)|二维切片、FISH定位、共聚焦／三维重建尚待确认分别标记；细胞与EPS/孔隙不同，孔隙不等于流量。|
|[气体参数与剖面](gas_transfer_parameters_utf8.csv)|保留原始单位、参数方法、温度/材料等缺口；不把氧穿透深度或硫化物反应率当传质系数。|
|[细胞间／絮体间交换](cell_interfloc_exchange_utf8.csv)|遗传、模型或聚集观察分开；目前无已核实的絮体间通量/距离实测，H₂与甲酸不混同。|
|[ORP、DO与供氧](oxygen_control_evidence_utf8.csv)|设定值、开关逻辑、氧输入记录、DO测量、局部剖面和参考电极缺口逐项标出。|
|[待全文／待核疑点](fulltext_pending_utf8.csv)|用户种子未独立核对、参数条件缺失、方法和图表待读，与明确无此证据不同。|
|[未处理队列](remaining_queue_utf8.csv)|稳定顺序和ID，检查点不是停止上限。|
|[本轮阅读](reading_log_utf8.csv)|完整缓存摘要或复用原件的相关段落，均不等于通读全文。|

## 实际怎样检索与去重

本地输入来自机制库`catalog.json`及组学发现`paper_discovery_candidates_enriched.json`，两者完整遍历；按DOI、PMID、规范化题名精确关联，优先保留原机制ID。题名相同但DOI不同保留疑点，不强合并。原始来源路径、ID和别名保留在[输入映射](local_input_mapping.json)、[身份来源索引](local_identity_registry.json)、[冲突](local_identity_conflicts.json)。没有改写另一分支或组学原记录。

7组已执行的本地查询见[日志CSV](search_log_utf8.csv)和[完整日志](search_log.json)；每组完整返回放在`raw/local/L01–L07.json`，没有取前100条的限制。L01–L06按对象×空间/传质/控制匹配题名和摘要；L07精确复用用户指定与已存全文/导读线索。其覆盖范围受此前检索和保存材料限制，不是截至今日全世界文献的搜索。

### 五篇种子和引用追溯

[种子核对表](seed_audit_utf8.csv)明确哪些仅来自用户线索。只有S02有已保存官方元数据、PMID17905889及完整摘要；另4项未独立取回，不生成“已验证”文章或伪RIS。

S02的保存PubMed记录含完整42条参考文献，本轮全部读出并保存[后向追溯](backward_citation_trace.json)，包括1990年代的微传感器、群落定位与颗粒研究。它们目前是可追溯原始引文线索，不等于42篇已读或已纳入。前向追溯已实际检索历史全文索引`search.sqlite`，见[范围与SQL](citation_trace_log.json)，当前为0匹配；该索引不是完整引文数据库，也不覆盖后来合并的全部原件。在线OpenAlex前向/参考文献接口及其他四种子的追溯仍未完成。

### 网络、工具和待执行查询

Nature源码提交`b543e8b998eb2df1fd44641cc8b262c638c2b442`已安装；本轮stdio启动和离线输入校验成功、列出16工具，见[真实工具验证](raw/preflight/nature_stdio_validation.json)。当前聊天没有直接挂载学术MCP工具；本地SDK能启动不等于学术API能访问。

官方Crossref、PubMed、OpenAlex和Europe PMC的种子接口测试均为代理CONNECT 403，未取得上游元数据。见[访问结果](raw/preflight/observations.json)。当前网络草稿已保存学术域名并补充`journals.asm.org`，保存成功、仍需发布；没有把草稿当运行配置。请在环境设置保存并发布／应用后重测。

[在线查询队列](online_query_queue.json)保存12组完整式及时间/分页策略，**状态均为尚未执行**。不设2012年下限；到实际执行日结束。PubMed取全ID并分批EFetch，OpenAlex走cursor到结束；Crossref用于种子DOI核对和参考文献，若补广泛查询需完整cursor或明确拆分，不默认首100。WoS/Scopus当前无访问能力，不称已检索。接口恢复前，不通过其他网络路径绕过拒绝。

## 原件、解析与续跑

本轮复用`original_files/`已有正文和`raw/pmc_fulltext/`的官方全文，未重复下载PDF或创建ZIP。[evidence/](evidence/)保存用于定位的页码文本；`source_base`与`source_path`共同指向现有原件，解析不能替代原件。附件尚未因本轮重新检查而标成“无附件”。

脚本：`prepare.py`只建立本地查询视图，`trace_saved.py`提取已存引文及检索旧全文索引，`curation.py`保留逐篇科学判断，`render.py`更新同一累计表。继续时先读`progress.json`，跳过已处理ID；网络先实测成功再执行在线查询，取回记录后与同一身份索引去重。不要把这次网络阻断的0新增误写成专题没有其他文献。

原科学首页和命题将原文保留并追加专题说明；[首页](../../../../README.md)、[科学导读](../../../../scientific_guide/README.md)与本表关联。阶段检查见`checkpoints/`，后续读回报告单独保存，不覆盖原文献数据。

在线续跑入口：`python results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/scripts/online_search.py --list-only`只列任务，已离线验证；网络生效后用`--run`，完整保存每页和失败状态。在线路径当前未验证成功。它不自动筛选、写旧库或取得全文；返回后仍需身份合并、日期/版本核实和阅读。经典来源队列见[citation_followup_queue.json](citation_followup_queue.json)。

辅助全文定位另存[FTS查询日志](fulltext_index_navigation_log.json)：5个短语查询均保存无LIMIT的完整索引返回，初次前12条导航已明确区分；这些是既有全文索引的证据定位，不增加书目命中数。
