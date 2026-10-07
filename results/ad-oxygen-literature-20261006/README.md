# AD主动供氧文献库：现行统一交付

检索日期及截止日期：2026-10-06；发表范围2012-01-01至当日。当前更新：2026-10-07用户人工分类同步，保留400个稳定记录ID，未重新检索或自动筛选。

## 当前数量

类别：1 AD反应器/内部循环供氧；2 厌氧水解/产酸供氧；3 独立好氧/微好氧预处理；4 综述；5 排除；6 仍待确认。

|类别|所有文献类型|期刊文献|
|---|---:|---:|
|1|157|149|
|2|43|42|
|3|46|43|
|4|43|43|
|5|111|102|
|6|0|0|
|合计|400|379|

期刊原始研究234条（149+42+43）。学位/学生报告5条、其他会议/海报/专利等16条单列；类别1–3所有类型共246条，不能全部称期刊原始研究。

用户附件最后一列“结果”28条全部同步，空白0、异常0。人工判断优先，原判断和证据保留；全文获取状态不变。当前待范围判断0条。此前80条中76条已分类但尚未获论文全文，列为可选资料提取/追溯，包含排除及非期刊资料，不需要重复筛选。该76不是全库缺全文总数。

## 最终文件及EndNote

- [Excel](final_results/ad_oxygen_download_review_20261006.xlsx)：400条91列；包括人工同步28条、历史80篇复核对照、当前人工待确认、已分类缺全文76条、学位/报告及下载状态83条。
- [UTF-8 CSV](final_results/ad_oxygen_download_review_utf8.csv)：与Excel文献库逐值一致；追加人工分类及同步前判断字段。
- 六个category1–category6 RIS只含期刊，分别149、42、43、43、102、0条。category6为空，无需导入。
- [学位/学生报告RIS](final_results/theses_and_student_reports.ris)：5条。
- [其他非期刊RIS](final_results/other_nonjournal_records.ris)：16条。
- [期刊原始研究合并RIS](final_results/confirmed_original_research.ris)：234条，**替代期刊类别1–3的导入，不同时导入两套**。
- [统一最终ZIP](ad_oxygen_literature_final.zip)：包括本目录所有现行交付文件，不含ZIP自身及PDF。此前整理版本没有ZIP，本轮仅生成此一个。

全审计库可导入六类期刊RIS+学位报告RIS+其他非期刊RIS，互斥合计400条；不要再导入合并文件。若只建已纳入期刊库，导入合并234条及综述43条。旧库请按稳定ID更新，避免重复批量导入。EndNote：File → Import → File，Import Option选Reference Manager (RIS)，Text Translation选Unicode (UTF-8)。AU逐作者；THES学位、RPRT学生报告、CONF会议/海报、PAT专利。

## 人工处理及全文状态

- [当前待确认CSV](manual_review/scope_pending_utf8.csv)及[说明](manual_review/scope_pending_zh.md)：0条，仅表头；人工已分类记录全部移出。
- [76条已分类缺全文](manual_review/classified_missing_fulltext_utf8.csv)：可选资料补充，不是筛选任务；已排除记录不要求下载，海报/摘要不应强求不存在的期刊全文。
- [80条全文可获取性审查](manual_review/fulltext_access_audit_80_utf8.csv)：范围类别更新，获取状态、访问记录保留。
- [83条下载状态](manual_review/download_status_83_utf8.csv)：只更新范围相关字段；失败原因、来源、PDF路径、版本、页数等不变。
- [学位/学生报告表](manual_review/theses_and_student_reports_utf8.csv)及[说明](manual_review/theses_and_student_reports_zh.md)。

人工分类不代表已下载或阅读全文。PDF仅在运行环境中，路径不是GitHub下载链接。原网络代理、机构访问未认证等限制保留，不因人工分类而改成“已获得全文”。没有提交账户配置、密码、令牌或浏览器会话。

## 方法及审计

methods/01–05完整保留检索式、检索日期、筛选标准、阶段数量、实际证据阅读范围、下载及复核方法和局限；历史数量为对应阶段快照，不是当前数量。

- [06人工同步方法](methods/06_manual_classification_sync_zh.md)
- [原始人工表（原GB18030字节）](methods/manual_classification_20261007_original.csv)
- [逐条同步对照（UTF-8）](methods/audit/manual_classification_sync_20261007_utf8.csv)
- [人工同步汇总](methods/audit/manual_classification_sync_summary.json)
- [现行验证](methods/audit/final_validation.json)

final_record_metadata.json为唯一现行400条结构化数据，含前轮evidence_history及人工同步前完整记录。scope_reassessment_80、scope_reassessment_summary、cleanup_validation及其他审计保留原阶段信息，不能据其旧数量判断现行库。未新增原文证据，不承诺文献绝对找齐。

## 保留文件清单

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
- [final_results/other_nonjournal_records.ris](final_results/other_nonjournal_records.ris)
- [final_results/theses_and_student_reports.ris](final_results/theses_and_student_reports.ris)
- [manual_review/classified_missing_fulltext_utf8.csv](manual_review/classified_missing_fulltext_utf8.csv)
- [manual_review/download_status_83_utf8.csv](manual_review/download_status_83_utf8.csv)
- [manual_review/fulltext_access_audit_80_utf8.csv](manual_review/fulltext_access_audit_80_utf8.csv)
- [manual_review/scope_pending_utf8.csv](manual_review/scope_pending_utf8.csv)
- [manual_review/scope_pending_zh.md](manual_review/scope_pending_zh.md)
- [manual_review/theses_and_student_reports_utf8.csv](manual_review/theses_and_student_reports_utf8.csv)
- [manual_review/theses_and_student_reports_zh.md](manual_review/theses_and_student_reports_zh.md)
- [methods/01_search_methods_zh.md](methods/01_search_methods_zh.md)
- [methods/02_review_224_methods_zh.md](methods/02_review_224_methods_zh.md)
- [methods/03_evidence_clarification_zh.md](methods/03_evidence_clarification_zh.md)
- [methods/04_download_review_methods_zh.md](methods/04_download_review_methods_zh.md)
- [methods/05_scope_reassessment_correction_zh.md](methods/05_scope_reassessment_correction_zh.md)
- [methods/06_manual_classification_sync_zh.md](methods/06_manual_classification_sync_zh.md)
- [methods/audit/actual_evidence_basis_224_utf8.csv](methods/audit/actual_evidence_basis_224_utf8.csv)
- [methods/audit/citation_seeds_utf8.csv](methods/audit/citation_seeds_utf8.csv)
- [methods/audit/classification_changes.json](methods/audit/classification_changes.json)
- [methods/audit/cleanup_validation.json](methods/audit/cleanup_validation.json)
- [methods/audit/final_record_metadata.json](methods/audit/final_record_metadata.json)
- [methods/audit/final_validation.json](methods/audit/final_validation.json)
- [methods/audit/manual_classification_sync_20261007_utf8.csv](methods/audit/manual_classification_sync_20261007_utf8.csv)
- [methods/audit/manual_classification_sync_summary.json](methods/audit/manual_classification_sync_summary.json)
- [methods/audit/research_poster_1_utf8.csv](methods/audit/research_poster_1_utf8.csv)
- [methods/audit/review_audit_224_utf8.csv](methods/audit/review_audit_224_utf8.csv)
- [methods/audit/scope_reassessment_80_utf8.csv](methods/audit/scope_reassessment_80_utf8.csv)
- [methods/audit/scope_reassessment_changes_80.json](methods/audit/scope_reassessment_changes_80.json)
- [methods/audit/scope_reassessment_decisions_80.json](methods/audit/scope_reassessment_decisions_80.json)
- [methods/audit/scope_reassessment_summary.json](methods/audit/scope_reassessment_summary.json)
- [methods/audit/screening_pilot_15_audit_utf8.csv](methods/audit/screening_pilot_15_audit_utf8.csv)
- [methods/audit/search_log_utf8.csv](methods/audit/search_log_utf8.csv)
- [methods/audit/stage_summaries.json](methods/audit/stage_summaries.json)
- [methods/audit/targeted_fulltext_14_utf8.csv](methods/audit/targeted_fulltext_14_utf8.csv)
- [methods/manual_classification_20261007_original.csv](methods/manual_classification_20261007_original.csv)
- [ad_oxygen_literature_final.zip](ad_oxygen_literature_final.zip)
