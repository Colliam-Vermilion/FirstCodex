# 厌氧微生物空间结构与气体传质专题

<!-- CURRENT_ONLINE_STATUS START -->
## 2026-10-30 在线恢复后的当前状态

原12组专题查询已全部执行并完整分页；未设置2012年起始下限。查询取回完成与文章初筛、正式纳入、全文核实是不同阶段。原233条初筛未重做，原始行冻结于`checkpoints/pre_online_233_master.json`；S02的阅读深度/参数另据新读正文升级。

|查询|来源|实际取回（含组间重复）|完整分页状态|
|---|---|---:|---|
|Q01|PubMed|5|completed|
|Q02|PubMed|27|completed|
|Q03|PubMed|11|completed|
|Q04|PubMed|101|completed|
|Q05|PubMed|6|completed|
|Q06|PubMed|28|completed|
|Q07|PubMed|15|completed|
|Q08|PubMed|2|completed|
|Q09|OpenAlex|102|completed|
|Q10|OpenAlex|520|completed|
|Q11|OpenAlex|1232|completed|
|Q12|OpenAlex|57|completed|

完整12组返回合计 **2106条**。加入第一代前/后向引文元数据、种子核对和额外Europe PMC首批后，共2636条来源记录，统一去重为2442个本轮身份：187个匹配已有全库身份，2255个为全库中未匹配到的暂定新身份。后者不是新增相关或正式纳入数。全库查重同时使用此前13,817条池和当前3,752条机制/组学身份索引；52次题名相同但DOI冲突事件保留，不强合并。

同一专题累计视图现为2653个身份。本轮新增185条阅读判断，其中60条读完返回的完整摘要字段、125条只读题名；54条在摘要层面判为相关/方法参照（含其后升级全文者），不是正式全文纳入。**本轮新读正文方法/结果共3篇**，其中S01为真正整颗粒三维重建；原有5条全文片段/证据复用不重复计为新全文。

|种子|同一ID|独立核对|现行阅读深度|
|---|---|---|---|
|S01|SG-822165E8E403|Crossref DOI＋PubMed|全文方法/结果核实|
|S02|ODS-PMID17905889|Crossref DOI＋PubMed|全文方法/结果核实|
|S03|SG-52CE8A5581BA|Crossref DOI＋PubMed|元数据/完整正式摘要核实；正文未核实|
|S04|SG-7E776DC9CBE3|Crossref DOI＋PubMed|元数据/完整正式摘要核实；正文未核实|
|S05|SG-69FE36B49E26|Crossref DOI＋PubMed|元数据/完整正式摘要核实；正文未核实|

第一代OpenAlex后向共217条、前向共283条元数据全部取回。Crossref另完整保留232条原始参考文献，其中44条尚未通过所返DOI关联到当前身份，继续保留追溯任务。Crossref与OpenAlex的参考文献覆盖不同（例如S05为57与41），不强行抹平，不把被引条数算为独立机制验证，也未宣称无限层级追溯完成。

### 新证据与边界

- **S01，2024 μCT（全文方法/结果）：**双能量Os差分图像及三维孔洞；原始体素198.8 nm、显示795.2 nm。Os含细胞/EPS，gold-ISH未成功；固定脱水包埋，未测活体孔隙通量或O2剖面。截面面积与面积占比不可当作孔径/体积孔隙度。
- **S02，2007微剖面（全文方法/结果）：**35°C、约2 mm、氯仿失活后H2中心阶跃拟合Deff=(2.66±0.13)e-5 cm²/s；CH4的57%相对水比为假设。活性剖面、净生成率和表面释放率由反应扩散模型联系，不冒充全部独立实测参数。
- **2002丙酸双菌（全文方法/结果）：**H2/甲酸载体比较；常规培养/酶测37°C、H2时序30°C。10 µm距离为假定、理论H2通量2.5或0.3 nmol ml^-1 min^-1，非实测菌间流量。
- **S03/S04（完整正式摘要）：**菌间距5.30→0.29 µm与最大可能H2通量1.1→10.3必须分成图像距离与计算上限；O2响应约5倍、Deff约2.3倍只保留比值，绝对条件待正文。
- **ORP控制（正式摘要）：**硫化物控制目标与低硫时COD分流并存；不推普适安全ORP/DO阈值。仍没有本轮已核实的真正不同絮体间距离—通量实测。

### 实际访问限制与复现

OpenAlex cursor第二页目标HTTP401要求key，原错误正文保留；公开支持的普通`page`分页成功，Q10/Q11全部翻至末页，未注册key、发邮件或重装工具。PubMed全ID取回后每100条EFetch；OpenAlex每200条至计数末页，逐页重复ID/动态计数由`online_validation.json`检查。原PubMed队列不含执行日上限过滤，故未来预排日期/在线正式日期仍逐条待核，未因此确认未来研究纳入。

S01/S02的PMC EUtilities XML只有前置信息，随后公开PMC HTML正文确实可读；另外的浏览器验证页、扫描老文仅摘要页、EuropePMC fullTextXML HTTP500均不计为已读全文。S03出版社页仅摘要/访问提示；S04尝试出现代理CONNECT403，S05 Wiley目标HTTP403。不能从这些结果断言文章不存在。S05公开仓库链接的目标域名不在当前允许表，未绕过策略访问。原始成功页、请求参数（去除联系信息）、校验散列和错误日志都保留；较早失败记录若未保留目标错误正文会在日志审计单列，不凭状态码编造内容。

额外“厌氧消化主动供氧”Europe PMC记录保留在`raw/online/extra_EuropePMC/`：417是命中数，只有25条实际返回参与去重，不是原12组之一，不把417计为新增纳入。

### 当前剩余与继续入口

尚有2235条在线身份未初筛，126条待完整摘要（含原截断缺口），250个已有相关身份的具体全文/补证任务。数字指任务层级，不能相加当独立文献总数。

优先继续：`remaining_queue.json`、`abstract_pending_queue.json`和`fulltext_pending.json`；`online_screening.json`保留逐篇判断。原截断论文OR-84CED3EF8A62的OpenAlex重取字段仍在同处以省略号结束，未冒充补齐正式摘要。

[累计Excel](spatial_gas_transfer_cumulative.xlsx) · [累计CSV](literature_master_utf8.csv) · [累计JSON](literature_master.json) · [全部候选RIS](spatial_gas_transfer_candidates.ris) · [已初筛RIS（含题名层和不优先）](spatial_gas_transfer_reviewed.ris) · [新全文证据](online_fulltext_evidence.json) · [检索实际日志](online_search_log.json) · [引用实际日志](online_citation_trace_log.json) · [四部分导读增补位置](guide_online_update.json)。

渲染增量使用`render_online.py`与`append_online_guide.py`；不要运行旧prepare/render/update_guide覆盖现行视图。checkpoint ONLINE001/002均为阶段保存，不是总量上限。

---

## 网络恢复前的历史说明（以下原文保留）

以下“在线未完成／403／233条”等描述是发布新环境之前的历史快照。当前状态以上述在线恢复后的表格及progress.json为准。

<!-- CURRENT_ONLINE_STATUS END -->

本专题区分细胞／EPS／孔隙的结构、H₂/CH₄/O₂等浓度分布、传质参数与实际功能，并将产甲烷AD直接证据与Anammox、牙科生物膜、沉积物方法参照分开。**本轮在线补检尚未完成：2026-10-30四个官方API被当前环境代理以CONNECT 403拒绝。下面已完成的是对保存材料的实际本地专题检索、去重、阅读和证据提取，不能冒充已完成新的外部数据库检索。**

## 2026-10-30接续状态（北京时间18:55后的本地累计）

本轮从保存的193条未处理队列逐项继续，没有重新检索原1,536条或改变其判断。原40条专题判断保留，累计233条均有初筛状态；**这不是233篇已全文确认**。

|阶段／阅读深度|累计条数|本轮新增|含义|
|---|---:|---:|---|
|复用相关全文段落／既有全文证据|5|0|没有重新下载，非整篇精读。|
|读完缓存abstract字段|220|185|已读字段全部文字；不保证逐篇等同正式完整摘要。部分字段混入正文／致谢，逐篇列限制。|
|缓存片段初筛|2|2|OR-84CED3EF8A62源字段本身截断；OR-B9BE2F0A2077仅读前1,700字符，属医学非微生物生理背景。|
|仅题名判断为本专题不优先|6|6|运动／临床、植物生理、牙科提取物或酵母细胞铁运输等，未声称读摘要。|
|尚未开始本地初筛|0|—|不代表全文补证或在线补检已完成。|

本专题有29条暂不优先、4条待确认，其余200条为不同层级的相关／导航材料，**不是200篇核心或正式全文纳入**。本地可读而尚未补读的相关摘要队列为0；仍有1条源摘要截断待正式来源补齐。相关全文／证据任务为199个已有身份，另4个种子待元数据核对，共203行；不等于还需下载203篇。16篇导航综述／观点也在相关材料中。临时阅读层级字母不等同于组学数据项目的A/B/C分层，具体体系、方法和边界以逐篇字段为准。

累计增加到12条参数／剖面记录、17条供氧控制记录。新增包括人工PVA膜O₂扩散系数、Anammox凝胶／颗粒相对De，以及非AD膜的氧微剖面；均保留材料、溶质和方法缺口，不与活性AD颗粒混并。新建19条文献—命题关联，专题累计68条。没有新增外部文献、全文、独立机制验证或已核实絮体间H₂通量。

[本轮逐篇判断](followup_screening.json) · [剩余摘要缺口](abstract_pending_queue_utf8.csv) · [待全文与疑点](fulltext_pending_utf8.csv) · [逐20条历史检查点](checkpoints/) · [现行进度](progress.json)。检查点L020–L180记录当时阅读深度，后来补读会升级现行表；它们是历史快照。题名初筛与补摘要阶段没有截断为20篇后停止。新文献的作者从已存PubMed XML补齐，见[本地元数据来源](saved_metadata_augmentation.json)，没有再次查询API。

## 目前从证据能回答什么

- 2007年“Layered structure…”种子可从旧组学论文候选复用：摘要既有FISH类群定位又有H₂/CH₄/pH/ORP微剖面，报告H₂的Deff为2.66×10⁻⁵ cm²/s、约水中的57%。活性／失活材料、温度、拟合方法与尺寸待全文核查；不能把这个值当所有颗粒常数。
- R01414原件给出真正的ORP开关反馈：−310 mV开、−290 mV关，开阀0.14 mL/s纯氧，底部注入；未核实液相DO、累计供氧量或局部剖面。−320至−270 mV为实际运行范围，不能与开关阈值混用。负号经原PDF图像核对，文本抽取会漏负号。
- R03161操纵液面／润湿面积并测脱硫率；面积效应还可能含生物膜量或活性变化。Table1的g S/(m²·d)是表观反应去除率，不是Deff、kf、kLa或纯物理通量。
- 共培养的DO低于检出限时仍有空气输入，说明低主体DO不等于氧输入为零。记录DO不等于DO反馈控制；FISH聚集不等于已测到保护性微区。
- 本轮未新增已全文确认的CT／三维重建论文，也未取得真正絮体间的距离或通量实测。用户提供的3D CT种子和其他3个种子仍需联网独立核实，不按题名照写发现。

## 累计结果与阅读深度

[累计Excel](spatial_gas_transfer_cumulative.xlsx) · [文献与筛选CSV](literature_master_utf8.csv) · [JSON](literature_master.json) · [已初筛记录RIS（含本专题不优先）](spatial_gas_transfer_reviewed.ris) · [全部本地候选RIS](spatial_gas_transfer_candidates.ris)

总数与已处理数以[现行进度](progress.json)和[汇总](summary.json)为准。专题表是原库和组学关联记录的按ID视图，不另发重复文献ID，不改原范围／人工判断。首次仅40条有判断；193条原队列已冻结在`local_followup_baseline.json`，接续后不再将其写成未开始。逐篇模型阅读判断保存在`followup_screening.json`，不是关键词规则或用户人工复核。

|证据表|能读到什么|
|---|---|
|[三维结构与定位](structure_localization_evidence_utf8.csv)|二维切片、FISH定位、共聚焦／三维重建尚待确认分别标记；细胞与EPS/孔隙不同，孔隙不等于流量。|
|[气体参数与剖面](gas_transfer_parameters_utf8.csv)|保留原始单位、参数方法、温度/材料等缺口；不把氧穿透深度或硫化物反应率当传质系数。|
|[细胞间／絮体间交换](cell_interfloc_exchange_utf8.csv)|遗传、模型或聚集观察分开；目前无已核实的絮体间通量/距离实测，H₂与甲酸不混同。|
|[ORP、DO与供氧](oxygen_control_evidence_utf8.csv)|设定值、开关逻辑、氧输入记录、DO测量、局部剖面和参考电极缺口逐项标出。|
|[待全文／待核疑点](fulltext_pending_utf8.csv)|用户种子未独立核对、参数条件缺失、方法和图表待读，与明确无此证据不同。|
|[未开始队列](remaining_queue_utf8.csv)|当前为空；[待补摘要](abstract_pending_queue_utf8.csv)和[待全文](fulltext_pending_utf8.csv)仍独立保留，不把空队列冒充全过程完成。|
|[本轮阅读](reading_log_utf8.csv)|题名、片段、整个缓存字段与原件相关段落分开，均不等于通读全文。|

## 实际怎样检索与去重

本地输入来自机制库`catalog.json`及组学发现`paper_discovery_candidates_enriched.json`，两者完整遍历；按DOI、PMID、规范化题名精确关联，优先保留原机制ID。题名相同但DOI不同保留疑点，不强合并。原始来源路径、ID和别名保留在[输入映射](local_input_mapping.json)、[身份来源索引](local_identity_registry.json)、[冲突](local_identity_conflicts.json)。没有改写另一分支或组学原记录。

7组已执行的本地查询见[日志CSV](search_log_utf8.csv)和[完整日志](search_log.json)；每组完整返回放在`raw/local/L01–L07.json`，没有取前100条的限制。L01–L06按对象×空间/传质/控制匹配题名和摘要；L07精确复用用户指定与已存全文/导读线索。其覆盖范围受此前检索和保存材料限制，不是截至今日全世界文献的搜索。

### 五篇种子和引用追溯

[种子核对表](seed_audit_utf8.csv)明确哪些仅来自用户线索。只有S02有已保存官方元数据、PMID17905889及完整摘要；另4项未独立取回，不生成“已验证”文章或伪RIS。

S02的保存PubMed记录含完整42条参考文献，本轮全部读出并保存[后向追溯](backward_citation_trace.json)，包括1990年代的微传感器、群落定位与颗粒研究。它们目前是可追溯原始引文线索，不等于42篇已读或已纳入。前向追溯已实际检索历史全文索引`search.sqlite`，见[范围与SQL](citation_trace_log.json)，当前为0匹配；该索引不是完整引文数据库，也不覆盖后来合并的全部原件。在线OpenAlex前向/参考文献接口及其他四种子的追溯仍未完成。

### 网络、工具和待执行查询

Nature源码提交`b543e8b998eb2df1fd44641cc8b262c638c2b442`已安装；本轮stdio启动和离线输入校验成功、列出16工具，见[真实工具验证](raw/preflight/nature_stdio_validation.json)。当前聊天没有直接挂载学术MCP工具；本地SDK能启动不等于学术API能访问。

最初四来源均CONNECT 403的记录见[首次访问结果](raw/preflight/observations.json)。本轮按用户要求只读核查并各发一次最小查询，**没有重装Nature或再次保存草稿**：[完整诊断](raw/preflight/20261030_retest/README.md)区分任务绑定实例、执行器启动策略、草稿revision 7、当前revision 1且current/enforced的有效策略，以及真实请求。四域名都在草稿、都不在有效允许表，真实请求均为CONNECT 403；没有目标HTTP 403/429或有效目标JSON/XML。18:53再次观测仍未变化，不重复失败请求。

请在FirstCodex环境设置将现有草稿发布并应用到本任务的运行环境，而非仅保存。不能单凭旧回执`requires_publish=true`认定唯一故障原因；目前未见已放行的有效策略，无法确认放行后目标授权或限流情况。若后续确认已应用且有效表允许却仍CONNECT拒绝，保留实例／配置版本和单次请求证据交平台侧检查，不承诺重启解决。没有可用来源时仍继续独立本地任务；恢复后按来源继续12组查询与种子核验，再与同一233条身份索引去重。

[在线查询队列](online_query_queue.json)保存12组完整式及时间/分页策略，**状态均为尚未执行**。不设2012年下限；到实际执行日结束。PubMed取全ID并分批EFetch，OpenAlex走cursor到结束；Crossref用于种子DOI核对和参考文献，若补广泛查询需完整cursor或明确拆分，不默认首100。WoS/Scopus当前无访问能力，不称已检索。接口恢复前，不通过其他网络路径绕过拒绝。

## 原件、解析与续跑

本轮复用`original_files/`已有正文和`raw/pmc_fulltext/`的官方全文，未重复下载PDF或创建ZIP。[evidence/](evidence/)保存用于定位的页码文本；`source_base`与`source_path`共同指向现有原件，解析不能替代原件。附件尚未因本轮重新检查而标成“无附件”。

脚本：`prepare.py`只建立本地查询视图，`trace_saved.py`提取已存引文及检索旧全文索引，`curation.py`保留原40条判断并读入本轮`followup_screening.json`，`followup_curation.py`保留193条逐篇模型阅读注释及补读过程，`render.py`更新同一累计表。不重新运行prepare覆盖已保存状态。继续时先读`progress.json`，本地初筛已完成；下一步是源摘要缺口、相关全文和12组在线查询。网络先实测成功再执行；取回记录与同一身份索引去重，不能把0外部新增写成领域没有其他文献。

原科学首页和命题将原文保留并追加专题说明；[首页](../../../../README.md)、[科学导读](../../../../scientific_guide/README.md)与本表关联。阶段检查见`checkpoints/`，后续读回报告单独保存，不覆盖原文献数据。

在线续跑入口：`python results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/scripts/online_search.py --list-only`只列任务，已离线验证；网络生效后用`--run`，完整保存每页和失败状态。在线路径当前未验证成功。它不自动筛选、写旧库或取得全文；返回后仍需身份合并、日期/版本核实和阅读。经典来源队列见[citation_followup_queue.json](citation_followup_queue.json)。

辅助全文定位另存[FTS查询日志](fulltext_index_navigation_log.json)：5个短语查询均保存无LIMIT的完整索引返回，初次前12条导航已明确区分；这些是既有全文索引的证据定位，不增加书目命中数。

本次接续的[远端独立读回](remote_readback_20261030_followup.json)针对提交`67d1ed9b87b3af52a9ec0f0e1976508b0488a59e`的116个变更文件逐字节／SHA256比对，并在另一检出位置打开累计Excel、核查初筛状态及314个仓库文件链接；26个共享目标按Git树核查存在，不重复获取未改动论文原件。旧40条专题判断及原1,536条范围／优先级／证据／进度均保留。随后提交仅增加此读回报告和网络诊断措辞。
