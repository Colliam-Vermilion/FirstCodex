# 氧响应机制补充检索：范围和续跑协议

日期：2026-10-24 UTC。基准提交：`2c4aa35daca259bdc311cd54d720e5627ada5ba0`。

本轮独立于旧AD主动供氧范围。原554条及133列、128条旧排除、人工判断和全部原件保持原状（baseline.json保存SHA）。旧ID全部保留。新ID为规范身份键SHA256前12位的`OR-`标识；DOI优先、PMID其次、完整规范题名再次。相同题名但DOI冲突不自动合并，记录在identity_conflicts.json；这也包含Crossref返回的审稿报告、书章和旧库既有异DOI同题记录，不默认都为论文。

## 范围与证据

研究原厌氧/还原背景中的分子氧进入、低氧持续供给、间歇/重复暴露和去氧后恢复。标签分别保存，不合并急性抑制和长期适应。纯培养、共培养、酶学、代谢物、微电极、同位素和遗传干预均可；不强制omics。离体O2还原酶学单列为机制证据，不能等同完整细胞或AD反应器验证。H2O2/宿主氧爆发单独背景，不冒充直接O2处理。

机制M1损伤；M2耐氧解毒修复；M3能量/碳代谢；M4互作；M5空间保护；M6恢复/适应/替代；M7决定促进抑制的条件。功能潜力、转录、蛋白和实测活性分别记录；共现、基因或材料导电性不能证明互作、活性或DIET。适应性表型没有遗传证据不写进化适应。

## 本轮实际检索

按nature-academic-search多源流程，固定工具源码b543e8b998eb2df1fd44641cc8b262c638c2b442。MCP列出16工具，但真实检索的内部errors非空；CLI一次OpenAlex429。采用官方API完成分页，保留request_log.jsonl中的URL（不含联系人/凭据）、时间、返回字节SHA和所有原始响应。失败工具不计来源成功。

PubMed P01–P17：2012-01-01到2026-10-24，前14组按产甲烷菌、酶、肠道、互营、颗粒/生物膜、沉积物、泥炭/湿地、瘤胃、氧敏感酶、微氧代谢、恢复及AD分组，P15–17按实际命中扩展PFOR/PFL、cytochrome bd和selenoproteome。完整ESearch PMID和EFetch返回，实际QueryTranslation保留。使用自动词映射而非所有词限定TIAB，可能命中运动生理等噪声；未筛记录不视为纳入。OpenAlex O01–O03用title_and_abstract.search、相同日期及cursor，三组均自然结束。Crossref C01–C03是query.bibliographic相关性检索，每组取前100，保留实际超大报告数和未取回尾部；不声称完整遍历Crossref。完整查询与实际数在search_log.json/CSV，不能将来源报告总数当实际取回数。

以实际读到的B. thetaiotaomicron 2020原研究为种子，后向保存完整参考文献线索，并按原文编号核验2004纳摩尔氧生长、2001丙酮酸代谢、2008PFOR保护和2018内源超氧四项PubMed记录。前三项明确标早期文献，入待处理队列，不冒充本批全文已读。前向OpenAlex按cites:W3016413973、同日期窗完整分页，记录在forward_trace_log.json。真实命中扩展了PFOR/PFL、rubredoxin domains、cytochrome bd、selenoproteome、acetate/oleate、ORM2、laminarin等术语；扩展的原因和后续检索建议单列，不把建议当已执行查询。

PubMed/Crossref/OpenAlex实际可用；Europe PMC搜索可用但两篇XML接口500，停止同一失败来源，改用NCBI PMC。部分NCBI XML只有front/摘要，无body；必须按摘要证据标记。未使用WoS/Scopus付费访问、未登录学校、未下载测序原始数据。

## 首批与续跑

首批20的稳定名单和分层理由在batch_B001_selection.json。选择兼顾直接生化/遗传干预、工程共培养和不同生态体系，包含旧AD排除R11680，独立重判。每篇决定保存在decisions/<ID>.json并更新screening.json；Excel/CSV/JSON和RIS同批累计生成。剂量不在已读来源出现则填“未核实”，不换算气相百分比为DO。

reading_level与筛选阶段独立。全文核实表示实际查阅了与问题有关的Methods/Results段落，不表示读完每一页或全部附件。待确认可已读全文；摘要初筛不称全文核实。简短引文定位到PDF实际页或JATS章节XPath，摘要定位PubMed AbstractText序号。source_document_register.json记录源SHA与链接。

续跑先读取summary.json、screening.json及remaining_queue.json，按processing_order.json冻结顺序取下一批。顺序先固定首批20，再按机制词线索分桶轮转；桶内明确氧暴露题名、摘要可得和新检索命中优先，最后按年份/稳定ID排序。该词表仅排队，不作纳入/排除决定。不重检、不重做已完成篇；待确认单列，按uncertainties补必要信息。早期文献和引用线索状态单独保留。

全部原库554条也进入未筛池用于新范围判断，未命中本轮检索的原库记录不是新检索发现。保留池规模、独立返回身份、实际已筛20和最终纳入数量分开报告；本轮没有完成全部候选筛选或达到检索饱和。
