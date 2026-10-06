# AD主动供氧文献库：最终交付

检索日期与截止日期：2026-10-06；发表范围：2012-01-01至检索当天。以最后核验的 download_review_20261006 数据为准。本次只整理交付文件，不重新检索或改变筛选决定。原始及中间交付仍可通过Git历史查阅。

## 最终数量

|分类|数量|分类RIS|
|---|---:|---|
|1 直接向AD反应器或内部循环供氧|120|category1_direct_ad.ris|
|2 向厌氧水解/产酸阶段供氧|38|category2_hydrolysis_acidogenesis.ris|
|3 独立好氧/微好氧预处理|35|category3_independent_pretreatment.ris|
|4 综述|40|category4_reviews.ris|
|5 排除（保留审计）|87|category5_excluded_audit.ris|
|6 仍待确认|80|category6_pending_fulltext.ris|
|合计|400|六个分类文件的互斥并集|

已确认原始研究193条（1–3类）。待确认80条 = 尚需获取论文全文77条 + 已有正文但仍未决3条（R04700、R08127、R10372）。83条下载对象中，3条完成分类更新，80条仍未决；6条取得完整正文，包括一次重复下载、4篇新期刊全文和1份学位论文。海报或会议摘要不计为论文全文。

## 文件导航

### final_results/：唯一最终数据版本

- [Excel](final_results/ad_oxygen_download_review_20261006.xlsx)：400条、65列；保留完整检索日志、引文种子、早期排除审计及阶段复核工作表。
- [UTF-8 CSV](final_results/ad_oxygen_download_review_utf8.csv)：与Excel“文献库”逐单元格一致。
- 六个category1–category6分类RIS：与400条记录逐篇对应、互斥无遗漏。
- [confirmed_original_research.ris](final_results/confirmed_original_research.ris)：合并1–3类的193条，属于**替代导入方案**，不是新增文献。

EndNote：File → Import → File；筛选器Reference Manager (RIS)，Text Translation选Unicode (UTF-8)。选择分类1、2、3分别导入，**或**仅导入合并confirmed_original_research.ris，不能两套同时导入。综述、候选可另导入对应文件；排除RIS只供审计，不属于已纳入库。若为完整审计导入全部六类，则不要再导入合并文件。保留稳定记录ID供更新匹配。相同题名但不同DOI的版本疑点继续保留标记，不擅自合并。

### manual_review/：人工处理

- [77条完整待下载清单CSV](manual_review/manual_download_needed_utf8.csv)及[逐篇说明](manual_review/manual_download_needed_zh.md)：原ID、题名、DOI、官方HKUST/Fudan入口、下载失败原因及全文核查问题。
- [已有正文的3条CSV](manual_review/already_obtained_pending_3_utf8.csv)及[具体疑点与下一步](manual_review/already_obtained_pending_3_zh.md)。
- [83条最终下载状态](manual_review/download_status_83_utf8.csv)：版本、来源、文件路径、哈希、身份核验、失败信息及处理决定。运行环境中的PDF路径不是GitHub下载链接；PDF未提交。
- [80条人工复核工作流](manual_review/remaining_review_workflow_80_utf8.csv)：逐篇判定标准、章节定位和待填写证据字段。

机构入口需本人官方登录及MFA；当前云环境未认证，不能据此断言订阅不足。未获全文不作为排除理由。缺少剂量参数不阻碍已明确符合范围的研究纳入。

### methods/：各阶段方法与必要审计

- [01检索方法](methods/01_search_methods_zh.md)：完整检索式、日期、来源、分页、引文追溯、去重、筛选标准及局限。
- [02原224条复核方法](methods/02_review_224_methods_zh.md)：首批15条流程、补摘要、筛选与阶段数量。
- [03证据依据澄清](methods/03_evidence_clarification_zh.md)：逐篇筛选与全文阅读区别、14篇实际定向阅读、1份海报，以及当时83条疑点。
- [04全文下载及复核方法](methods/04_download_review_methods_zh.md)：首批5条、合法获取路线、6份正文核查、访问失败分流及最终数量。
- audit/保存搜索日志110条、引文种子28条、224条筛选与实际证据依据、14篇定向全文定位、海报审计、15条筛选流程审计、3条分类变更、各阶段数量和最终400条结构化元数据。它们是方法证据，不是替代最终库。
- [整理验证报告](methods/audit/cleanup_validation.json)：删除前迁移核验、Excel/CSV/RIS一致性和数量。

历史方法文档原文保留，并明确标注阶段快照；旧文件名是历史叙述，不代表仍存在的交付目录。历史方法若提及运行脚本、响应缓存或复现包，不表示本目录包含这些运行文件；完整查询已保存在方法、搜索日志及Excel中。原始版本可在清理前提交af86f8c303c4b0a385f7a07f6fa23184ecdf55e1查阅。

本轮未新增ZIP，删除全部旧ZIP、重复数据版本与测试交付。保留15条筛选流程审计及工作簿首批5条记录，它们属于正式方法验证证据，不是附件连通性测试文件。结果不承诺绝对找齐；来源索引、术语匹配、引文覆盖及全文访问均有局限。

## 保留文件完整清单

- [README.md](README.md)
- [final_results/ad_oxygen_download_review_20261006.xlsx](final_results/ad_oxygen_download_review_20261006.xlsx)
- [final_results/ad_oxygen_download_review_utf8.csv](final_results/ad_oxygen_download_review_utf8.csv)
- [final_results/category1_direct_ad.ris](final_results/category1_direct_ad.ris)
- [final_results/category2_hydrolysis_acidogenesis.ris](final_results/category2_hydrolysis_acidogenesis.ris)
- [final_results/category3_independent_pretreatment.ris](final_results/category3_independent_pretreatment.ris)
- [final_results/category4_reviews.ris](final_results/category4_reviews.ris)
- [final_results/category5_excluded_audit.ris](final_results/category5_excluded_audit.ris)
- [final_results/category6_pending_fulltext.ris](final_results/category6_pending_fulltext.ris)
- [final_results/confirmed_original_research.ris](final_results/confirmed_original_research.ris)
- [manual_review/already_obtained_pending_3_utf8.csv](manual_review/already_obtained_pending_3_utf8.csv)
- [manual_review/already_obtained_pending_3_zh.md](manual_review/already_obtained_pending_3_zh.md)
- [manual_review/download_status_83_utf8.csv](manual_review/download_status_83_utf8.csv)
- [manual_review/manual_download_needed_utf8.csv](manual_review/manual_download_needed_utf8.csv)
- [manual_review/manual_download_needed_zh.md](manual_review/manual_download_needed_zh.md)
- [manual_review/remaining_review_workflow_80_utf8.csv](manual_review/remaining_review_workflow_80_utf8.csv)
- [methods/01_search_methods_zh.md](methods/01_search_methods_zh.md)
- [methods/02_review_224_methods_zh.md](methods/02_review_224_methods_zh.md)
- [methods/03_evidence_clarification_zh.md](methods/03_evidence_clarification_zh.md)
- [methods/04_download_review_methods_zh.md](methods/04_download_review_methods_zh.md)
- [methods/audit/actual_evidence_basis_224_utf8.csv](methods/audit/actual_evidence_basis_224_utf8.csv)
- [methods/audit/citation_seeds_utf8.csv](methods/audit/citation_seeds_utf8.csv)
- [methods/audit/classification_changes.json](methods/audit/classification_changes.json)
- [methods/audit/cleanup_validation.json](methods/audit/cleanup_validation.json)
- [methods/audit/final_record_metadata.json](methods/audit/final_record_metadata.json)
- [methods/audit/research_poster_1_utf8.csv](methods/audit/research_poster_1_utf8.csv)
- [methods/audit/review_audit_224_utf8.csv](methods/audit/review_audit_224_utf8.csv)
- [methods/audit/screening_pilot_15_audit_utf8.csv](methods/audit/screening_pilot_15_audit_utf8.csv)
- [methods/audit/search_log_utf8.csv](methods/audit/search_log_utf8.csv)
- [methods/audit/stage_summaries.json](methods/audit/stage_summaries.json)
- [methods/audit/targeted_fulltext_14_utf8.csv](methods/audit/targeted_fulltext_14_utf8.csv)
