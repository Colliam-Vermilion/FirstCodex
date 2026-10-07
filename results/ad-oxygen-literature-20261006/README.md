# AD主动供氧文献库：统一最终交付

更新：2026-10-07，43条综述引文追溯；时间范围2012-01-01至2026-10-07。原400条和28条人工最终判断完整保留；新增40篇确认研究、36篇候选，现行476条。

## 当前数量

|类别|所有类型|期刊文献|
|---|---:|---:|
|1 AD反应器/内部循环供氧|174|165|
|2 厌氧水解/产酸供氧|51|50|
|3 独立预处理|61|58|
|4 综述性来源|43|43|
|5 排除，仅查重审计|111|102|
|6 待确认|36|33|
|合计|476|451|

已纳入期刊原始研究273条；学位/学生报告5条、其他非期刊20条单列。类别4含R07033综述性技术说明，并非标准综述；R11773遵循用户人工分类，独立类型证据仍缺失。类别5不进入下游纳入分析，但保留查重及审计。

## 追溯覆盖及文件导航

43篇中15篇有完整参考文献、27篇只有部分引用元数据、1篇未取得；实际取得5044条引用。完整列表不等于阅读全文或全部被引文献已筛清。201条引用缺完整解析题名等缺口见逐篇审计；未把不能访问的综述记为完成。

- [最终Excel](final_results/ad_oxygen_download_review_20261006.xlsx)：476条101列；新增追溯43、引用匹配5044、新研究40、早期45和候选36工作表。文件名保留以保持原链接。
- [UTF-8 CSV](final_results/ad_oxygen_download_review_utf8.csv)：与Excel文献库逐值一致。
- [逐篇综述追溯](methods/audit/review_reference_tracking_43_utf8.csv)、[引用匹配](methods/audit/reference_matching_utf8.csv)、[逐项候选判断](methods/audit/reference_candidate_decisions_utf8.csv)。
- [新增确认40篇](final_results/new_from_review_chase_utf8.csv)及[新增RIS](final_results/new_from_review_chase.ris)。
- [早期相关45条](manual_review/early_related_references_utf8.csv)：43条研究线索、2条综述线索，不计入当前时间范围。
- [真正待确认36条](manual_review/scope_pending_utf8.csv)及[具体问题表](manual_review/review_chase_pending_utf8.csv)：均为本轮新增候选，未恢复已完成人工判断的旧记录。
- [综述来源及访问失败审计](methods/audit/review_source_access_audit_utf8.csv)、[版本/同研究关系](methods/audit/study_version_relationships_utf8.csv)、[未继续追溯的新综述19条](methods/audit/additional_review_leads_utf8.csv)。
- [28篇缺完整参考文献及机构访问入口](manual_review/reviews_missing_complete_references_utf8.csv)：27篇部分覆盖、1篇无列表，仍需后续补齐。
- [本轮方法与局限](methods/07_review_reference_chase_zh.md)。methods/01–06保留历次检索式、日期、筛选/下载方法及数量；历史审计数量不是现行数量。
- [统一ZIP](ad_oxygen_literature_final.zip)：唯一压缩包，与现行目录一致，不含自身或PDF。

## EndNote导入

六类期刊RIS条数为165、50、58、43、102、33；加学位报告5及其他非期刊20，互斥覆盖476条。期刊类别1–3合并[confirmed_original_research.ris](final_results/confirmed_original_research.ris)273条，是类别1–3的替代导入方案，不能同时导入。新增RIS40条为增量替代文件，已经包含在全量分类RIS内；不要与全量重复导入。类别6证据不足，不混入已确认研究。学位报告及会议等非期刊资料分别保留文献类型。

EndNote：File → Import → File；Import Option选Reference Manager (RIS)，Text Translation选Unicode (UTF-8)。作者逐条AU。旧库需按稳定ID更新，避免批量重复导入。

## 全文状态与人工审计

范围分类与全文获取分开。原28条人工结论为最终判断，其原始表、同步记录及原证据保留，获取状态不变。新增确认不代表已下载或阅读全文。[新研究已分类缺全文](manual_review/new_classified_missing_fulltext_utf8.csv)用于可选参数提取，不需重复范围筛选。

此前[80条获取性审查](manual_review/fulltext_access_audit_80_utf8.csv)、[83条下载记录](manual_review/download_status_83_utf8.csv)、[76条已分类缺全文](manual_review/classified_missing_fulltext_utf8.csv)是原阶段范围，不代表现行全库缺全文总数。用户人工判断不会因自动下载失败而撤销。PDF保存在运行环境，路径不是GitHub附件；不提交配置、账户、凭据或浏览器会话。

final_record_metadata.json为现行结构化主库；evidence_history、manual_classification及来源综述引用保持可追溯。[现行验证](methods/audit/final_validation.json)检查ID、类别、格式一致性及原人工记录保留。参考文献部分覆盖、未解析引用与新综述尚未追溯仍构成漏检风险。

## 保留文件清单

- [README.md](README.md)
- [ad_oxygen_literature_final.zip](ad_oxygen_literature_final.zip)
- [final_results/ad_oxygen_download_review_20261006.xlsx](final_results/ad_oxygen_download_review_20261006.xlsx)
- [final_results/ad_oxygen_download_review_utf8.csv](final_results/ad_oxygen_download_review_utf8.csv)
- [final_results/category1_direct_ad.ris](final_results/category1_direct_ad.ris)
- [final_results/category2_hydrolysis_acidogenesis.ris](final_results/category2_hydrolysis_acidogenesis.ris)
- [final_results/category3_independent_pretreatment.ris](final_results/category3_independent_pretreatment.ris)
- [final_results/category4_reviews.ris](final_results/category4_reviews.ris)
- [final_results/category5_excluded_audit.ris](final_results/category5_excluded_audit.ris)
- [final_results/category6_pending_fulltext.ris](final_results/category6_pending_fulltext.ris)
- [final_results/confirmed_original_research.ris](final_results/confirmed_original_research.ris)
- [final_results/new_from_review_chase.ris](final_results/new_from_review_chase.ris)
- [final_results/new_from_review_chase_utf8.csv](final_results/new_from_review_chase_utf8.csv)
- [final_results/other_nonjournal_records.ris](final_results/other_nonjournal_records.ris)
- [final_results/theses_and_student_reports.ris](final_results/theses_and_student_reports.ris)
- [manual_review/classified_missing_fulltext_utf8.csv](manual_review/classified_missing_fulltext_utf8.csv)
- [manual_review/download_status_83_utf8.csv](manual_review/download_status_83_utf8.csv)
- [manual_review/early_related_references_utf8.csv](manual_review/early_related_references_utf8.csv)
- [manual_review/fulltext_access_audit_80_utf8.csv](manual_review/fulltext_access_audit_80_utf8.csv)
- [manual_review/new_classified_missing_fulltext_utf8.csv](manual_review/new_classified_missing_fulltext_utf8.csv)
- [manual_review/review_chase_pending_utf8.csv](manual_review/review_chase_pending_utf8.csv)
- [manual_review/reviews_missing_complete_references_utf8.csv](manual_review/reviews_missing_complete_references_utf8.csv)
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
- [methods/07_review_reference_chase_zh.md](methods/07_review_reference_chase_zh.md)
- [methods/audit/actual_evidence_basis_224_utf8.csv](methods/audit/actual_evidence_basis_224_utf8.csv)
- [methods/audit/additional_review_leads_utf8.csv](methods/audit/additional_review_leads_utf8.csv)
- [methods/audit/citation_seeds_utf8.csv](methods/audit/citation_seeds_utf8.csv)
- [methods/audit/classification_changes.json](methods/audit/classification_changes.json)
- [methods/audit/cleanup_validation.json](methods/audit/cleanup_validation.json)
- [methods/audit/final_record_metadata.json](methods/audit/final_record_metadata.json)
- [methods/audit/final_validation.json](methods/audit/final_validation.json)
- [methods/audit/manual_classification_conflicts_utf8.csv](methods/audit/manual_classification_conflicts_utf8.csv)
- [methods/audit/manual_classification_sync_20261007_utf8.csv](methods/audit/manual_classification_sync_20261007_utf8.csv)
- [methods/audit/manual_classification_sync_summary.json](methods/audit/manual_classification_sync_summary.json)
- [methods/audit/reference_candidate_decisions_utf8.csv](methods/audit/reference_candidate_decisions_utf8.csv)
- [methods/audit/reference_matching_utf8.csv](methods/audit/reference_matching_utf8.csv)
- [methods/audit/research_poster_1_utf8.csv](methods/audit/research_poster_1_utf8.csv)
- [methods/audit/review_audit_224_utf8.csv](methods/audit/review_audit_224_utf8.csv)
- [methods/audit/review_reference_chase_summary.json](methods/audit/review_reference_chase_summary.json)
- [methods/audit/review_reference_tracking_43_utf8.csv](methods/audit/review_reference_tracking_43_utf8.csv)
- [methods/audit/review_source_access_audit_utf8.csv](methods/audit/review_source_access_audit_utf8.csv)
- [methods/audit/scope_reassessment_80_utf8.csv](methods/audit/scope_reassessment_80_utf8.csv)
- [methods/audit/scope_reassessment_changes_80.json](methods/audit/scope_reassessment_changes_80.json)
- [methods/audit/scope_reassessment_decisions_80.json](methods/audit/scope_reassessment_decisions_80.json)
- [methods/audit/scope_reassessment_summary.json](methods/audit/scope_reassessment_summary.json)
- [methods/audit/screening_pilot_15_audit_utf8.csv](methods/audit/screening_pilot_15_audit_utf8.csv)
- [methods/audit/search_log_utf8.csv](methods/audit/search_log_utf8.csv)
- [methods/audit/stage_summaries.json](methods/audit/stage_summaries.json)
- [methods/audit/study_version_relationships_utf8.csv](methods/audit/study_version_relationships_utf8.csv)
- [methods/audit/targeted_fulltext_14_utf8.csv](methods/audit/targeted_fulltext_14_utf8.csv)
- [methods/manual_classification_20261007_original.csv](methods/manual_classification_20261007_original.csv)
