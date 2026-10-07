# AD主动供氧文献库：现行统一交付

更新：2026-10-07，已同步用户36篇复核附件。J列“新分类”、K列“人工分类”；K非空25条以人工结果为准，K空白11条沿用J。24条范围分类发生变化，1条K结果与原分类相同。原28条人工记录完整保留。现行**475条去重记录、107列**，没有范围待确认记录；缺全文状态未改变。R13854通过既有别名匹配R01238，不增加重复文献。

|类别|所有类型|期刊文献|
|---|---:|---:|
|1 AD反应器/内部循环供氧|185|175|
|2 专门厌氧水解/产酸供氧|54|53|
|3 独立预处理（相关研究）|65|62|
|4 综述性来源|43|43|
|5 排除，仅查重/审计|128|118|
|6 范围待确认|0|0|
|合计|475|451|

已确认期刊原始研究290；学位/学生报告6、其他非期刊18分别列出。类别5仅用于查重和审计，不进入下游纳入分析。类别4含R07033综述性技术说明；R11773沿用原人工综述判断，独立类型核验未完成。R13890为非生物湿式空气氧化预处理。

## 文件导航

- [最终Excel](final_results/ad_oxygen_download_review_20261006.xlsx)及[UTF-8 CSV](final_results/ad_oxygen_download_review_utf8.csv)：同一475条记录。Excel新增“36人工分类同步”表，原36复核表作为历史证据保留。
- [本次36条同步对照表](methods/audit/pending36_manual_sync_utf8.csv)：每个原ID、现行ID、J/K原值、采用列、原/新分类、全文状态及别名匹配说明。
- [附件原件](methods/manual_classification_pending36_20261007_original.csv)：保留原字节，实际GB18030编码，虽然原文件名含utf8；Excel可按GB18030/简体中文打开。更新后的总库及对照表采用UTF-8 BOM，RIS为UTF-8。
- [本次同步方法及核验](methods/09_pending36_manual_sync_zh.md)、[同步统计](methods/audit/pending36_manual_sync_summary.json)。原人工28案例表与原附件均保留。
- [现行范围待确认清单](manual_review/scope_pending_utf8.csv)：0条，保留表头。没有把K空白当作未分类或排除。
- [追溯新增确认58篇](final_results/new_from_review_chase_utf8.csv)及[已分类但缺全文的资料提取表](manual_review/new_classified_missing_fulltext_utf8.csv)：不要求再次范围筛选；获取状态与人工分类独立。
- [原36自动复核及证据](methods/audit/pending36_scope_reaudit_utf8.csv)、[原方法审计](methods/08_pending36_reaudit_zh.md)、[人工28案例对应](methods/audit/manual28_candidate_comparisons_utf8.csv)、[重复ID映射](methods/audit/record_id_aliases_utf8.csv)。这些是历史阶段证据，不代表现行待确认数量。
- [43篇综述追溯](methods/audit/review_reference_tracking_43_utf8.csv)、[5044条引用匹配](methods/audit/reference_matching_utf8.csv)、[28篇仍缺完整引用列表](manual_review/reviews_missing_complete_references_utf8.csv)。
- [早期相关45条](manual_review/early_related_references_utf8.csv)：不计入2012-01-01至2026-10-07主库。新综述线索19篇尚未追溯。
- [唯一最终ZIP](ad_oxygen_literature_final.zip)：所有现行交付文件，不含ZIP自身或论文PDF。

## 分类权限与全文状态

本次仅同步用户明确分类，不重新自动筛选。K优先；K空白沿用J；两列无明确值才保留待确认。原28条人工记录不改动，原自动判断/疑点/证据保留于总库“人工同步前”字段、原36复核表及canonical evidence_history。附件只有分类标签，未附新增逐篇理由，不据此编造阅读经历、曝气参数或新的实验事实。

所有记录的全文获取状态、来源、路径与既有获取证据均保持不变。零待确认表示范围已判定，不表示全部取得全文。R13871本次按用户category1归类，仍为学位论文、未取得全文；不混入期刊原始研究数量。原5thesis及1student-report结构不变。

## EndNote导入

六期刊分类RIS分别175、53、62、43、118、0条；学位/报告RIS6、其他非期刊RIS18。八个分区互斥覆盖475条。空的类别6 RIS表示无现行待确认记录。期刊原始研究合并RIS290是期刊类别1–3的替代导入；追溯新增RIS58为替代增量，包含已在全量分区内的论文，**不要重复导入**。旧库已合并R13854至R01238，别名保留在RIS N1及审计中。

EndNote：File → Import → File；Import Option选择Reference Manager (RIS)，Text Translation选择Unicode (UTF-8)。作者分别AU记录，期刊JOUR、学位THES、报告RPRT、会议CONF、未知GEN。

## 方法与局限

methods/01–09保留原检索、筛选、下载、证据与人工同步方法；07、08的数量是阶段快照，09及主库为现行。原43综述完整引用列表15、部分27、未取得1；引用5044条。201条未解析完整题名及未追溯的新综述仍有漏检风险。本次没有重新检索，用户分类不能填补参考文献覆盖缺口。

[验证报告](methods/audit/final_validation.json)核验475唯一ID、DOI、分类分区、Excel/CSV逐值、36匹配、原28完整记录及全文状态不变、附件原字节、ZIP逐字节一致。不提交配置、凭据、PDF或浏览器数据。

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
- [methods/08_pending36_reaudit_zh.md](methods/08_pending36_reaudit_zh.md)
- [methods/09_pending36_manual_sync_zh.md](methods/09_pending36_manual_sync_zh.md)
- [methods/audit/actual_evidence_basis_224_utf8.csv](methods/audit/actual_evidence_basis_224_utf8.csv)
- [methods/audit/additional_review_leads_utf8.csv](methods/audit/additional_review_leads_utf8.csv)
- [methods/audit/citation_seeds_utf8.csv](methods/audit/citation_seeds_utf8.csv)
- [methods/audit/classification_changes.json](methods/audit/classification_changes.json)
- [methods/audit/cleanup_validation.json](methods/audit/cleanup_validation.json)
- [methods/audit/final_record_metadata.json](methods/audit/final_record_metadata.json)
- [methods/audit/final_validation.json](methods/audit/final_validation.json)
- [methods/audit/manual28_candidate_comparisons_utf8.csv](methods/audit/manual28_candidate_comparisons_utf8.csv)
- [methods/audit/manual_classification_conflicts_utf8.csv](methods/audit/manual_classification_conflicts_utf8.csv)
- [methods/audit/manual_classification_sync_20261007_utf8.csv](methods/audit/manual_classification_sync_20261007_utf8.csv)
- [methods/audit/manual_classification_sync_summary.json](methods/audit/manual_classification_sync_summary.json)
- [methods/audit/pending36_evidence_access_utf8.csv](methods/audit/pending36_evidence_access_utf8.csv)
- [methods/audit/pending36_manual_sync_summary.json](methods/audit/pending36_manual_sync_summary.json)
- [methods/audit/pending36_manual_sync_utf8.csv](methods/audit/pending36_manual_sync_utf8.csv)
- [methods/audit/pending36_reaudit_summary.json](methods/audit/pending36_reaudit_summary.json)
- [methods/audit/pending36_scope_reaudit_utf8.csv](methods/audit/pending36_scope_reaudit_utf8.csv)
- [methods/audit/record_id_aliases_utf8.csv](methods/audit/record_id_aliases_utf8.csv)
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
- [methods/manual_classification_pending36_20261007_original.csv](methods/manual_classification_pending36_20261007_original.csv)
