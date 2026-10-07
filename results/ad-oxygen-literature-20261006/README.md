# AD主动供氧文献库：现行统一交付

更新：2026-10-07，完成综述追溯58条漏收原因审计和15组补充检索。确认新增30篇（28原研究＋2综述），现行**505条、107列**。原475条完整记录及53个人工分类不改动；库内范围待确认0，本轮另外58条证据不足线索在主库外单列，不混入确认数量。

|类别|所有类型|期刊文献|
|---|---:|---:|
|1 AD反应器/内部循环供氧|191|181|
|2 专门厌氧水解/产酸供氧|56|55|
|3 独立预处理（相关研究）|85|82|
|4 综述性来源|45|45|
|5 排除，仅查重/审计|128|118|
|6 范围待确认|0|0|
|合计|505|481|

已确认期刊原始研究318；学位/学生报告6、其他非期刊18分别列出。类别5仅用于查重和审计，不进入下游纳入分析。类别4含R07033综述性技术说明；R11773沿用原人工综述判断，独立类型核验未完成。R13890为非生物湿式空气氧化预处理。

## 文件导航

- [漏收原因与改进检索方法](methods/10_omission_analysis_and_supplement_search_zh.md)、[58篇逐项原因](methods/audit/omission_reasons_58_utf8.csv)、[关键词表](methods/audit/supplement_keywords_utf8.csv)、[15组完整执行查询及数量](methods/audit/supplement_search_log_utf8.csv)。
- [本轮新增30篇](methods/audit/supplement_confirmed_new_utf8.csv)、[新增增量RIS](final_results/supplement_confirmed_new.ris)：已在全量分类内，增量是替代导入，不要重复导入。
- [补充检索58条具体疑点](manual_review/supplement_evidence_insufficient_utf8.csv)、[218条定向处理](methods/audit/supplement_targeted_screening_218_utf8.csv)、[46条版本/非期刊关联线索](methods/audit/supplement_version_and_gray_leads_utf8.csv)。线索尚未并入主库，不作为默认需用户下载全文任务；下一步先补摘要/引用语境，分类与获取继续分开。
- [全部10263条查重记录](methods/audit/supplement_dedup_all_returns_utf8.csv)、[验证统计及限制](methods/audit/supplement_search_validation_summary.json)、[新增已分类缺全文资料提取表](manual_review/supplement_classified_missing_fulltext_utf8.csv)。9873条宽词池尚未逐篇筛尽；不能称全文复核或检索饱和。

- [最终Excel](final_results/ad_oxygen_download_review_20261006.xlsx)及[UTF-8 CSV](final_results/ad_oxygen_download_review_utf8.csv)：同一505条记录。Excel新增“36人工分类同步”表，原36复核表作为历史证据保留。
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

第09轮同步用户明确分类，第10轮仅筛选新的补充线索，不重判既有记录。K优先；K空白沿用J；两列无明确值才保留待确认。原28条人工记录不改动，原自动判断/疑点/证据保留于总库“人工同步前”字段、原36复核表及canonical evidence_history。附件只有分类标签，未附新增逐篇理由，不据此编造阅读经历、曝气参数或新的实验事实。

原475条记录的全文获取状态、来源、路径与既有获取证据均保持不变。新增30条未取得正文，分类依据逐篇列明。零待确认表示范围已判定，不表示全部取得全文。R13871本次按用户category1归类，仍为学位论文、未取得全文；不混入期刊原始研究数量。原5thesis及1student-report结构不变。

## EndNote导入

六期刊分类RIS分别181、55、82、45、118、0条；学位/报告RIS6、其他非期刊RIS18。八个分区互斥覆盖505条。新增补检RIS30和追溯RIS58都是替代增量，不与全量重复导入。空的类别6 RIS表示无现行待确认记录。期刊原始研究合并RIS318是期刊类别1–3的替代导入；追溯新增RIS58为替代增量，包含已在全量分区内的论文，**不要重复导入**。旧库已合并R13854至R01238，别名保留在RIS N1及审计中。

EndNote：File → Import → File；Import Option选择Reference Manager (RIS)，Text Translation选择Unicode (UTF-8)。作者分别AU记录，期刊JOUR、学位THES、报告RPRT、会议CONF、未知GEN。

## 方法与局限

methods/01–10保留原检索、筛选、下载、证据与人工同步方法；07、08的数量是阶段快照，10及主库为现行。原43综述完整引用列表15、部分27、未取得1；引用5044条。201条未解析完整题名及未追溯的新综述仍有漏检风险。第09轮仅人工同步；第10轮执行补充检索，但新增2篇综述参考文献尚未追溯，宽词池尚未筛尽。

[验证报告](methods/audit/final_validation.json)核验505唯一ID、DOI、分类分区、Excel/CSV逐值、36匹配、原28完整记录及全文状态不变、附件原字节、ZIP逐字节一致。不提交配置、凭据、PDF或浏览器数据。





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
- [final_results/supplement_confirmed_new.ris](final_results/supplement_confirmed_new.ris)
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
- [manual_review/supplement_classified_missing_fulltext_utf8.csv](manual_review/supplement_classified_missing_fulltext_utf8.csv)
- [manual_review/supplement_evidence_insufficient_utf8.csv](manual_review/supplement_evidence_insufficient_utf8.csv)
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
- [methods/10_omission_analysis_and_supplement_search_zh.md](methods/10_omission_analysis_and_supplement_search_zh.md)
- [methods/audit/actual_evidence_basis_224_utf8.csv](methods/audit/actual_evidence_basis_224_utf8.csv)
- [methods/audit/additional_review_leads_utf8.csv](methods/audit/additional_review_leads_utf8.csv)
- [methods/audit/citation_seeds_utf8.csv](methods/audit/citation_seeds_utf8.csv)
- [methods/audit/classification_changes.json](methods/audit/classification_changes.json)
- [methods/audit/cleanup_validation.json](methods/audit/cleanup_validation.json)
- [methods/audit/final_record_metadata.json](methods/audit/final_record_metadata.json)
- [methods/audit/final_validation.json](methods/audit/final_validation.json)
- [methods/audit/initial_pattern_replay_cases.json](methods/audit/initial_pattern_replay_cases.json)
- [methods/audit/initial_unmatched3_fuzzy_checks.json](methods/audit/initial_unmatched3_fuzzy_checks.json)
- [methods/audit/manual28_candidate_comparisons_utf8.csv](methods/audit/manual28_candidate_comparisons_utf8.csv)
- [methods/audit/manual_classification_conflicts_utf8.csv](methods/audit/manual_classification_conflicts_utf8.csv)
- [methods/audit/manual_classification_sync_20261007_utf8.csv](methods/audit/manual_classification_sync_20261007_utf8.csv)
- [methods/audit/manual_classification_sync_summary.json](methods/audit/manual_classification_sync_summary.json)
- [methods/audit/omission_initial_evidence_58.json](methods/audit/omission_initial_evidence_58.json)
- [methods/audit/omission_reasons_58_utf8.csv](methods/audit/omission_reasons_58_utf8.csv)
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
- [methods/audit/supplement_confirmed_new_utf8.csv](methods/audit/supplement_confirmed_new_utf8.csv)
- [methods/audit/supplement_dedup_all_returns_utf8.csv](methods/audit/supplement_dedup_all_returns_utf8.csv)
- [methods/audit/supplement_keywords_utf8.csv](methods/audit/supplement_keywords_utf8.csv)
- [methods/audit/supplement_late_identity_checks.json](methods/audit/supplement_late_identity_checks.json)
- [methods/audit/supplement_primary_metadata_62.json](methods/audit/supplement_primary_metadata_62.json)
- [methods/audit/supplement_recovered_chase_ids_utf8.csv](methods/audit/supplement_recovered_chase_ids_utf8.csv)
- [methods/audit/supplement_search_log_utf8.csv](methods/audit/supplement_search_log_utf8.csv)
- [methods/audit/supplement_search_validation_summary.json](methods/audit/supplement_search_validation_summary.json)
- [methods/audit/supplement_targeted_screening_218_utf8.csv](methods/audit/supplement_targeted_screening_218_utf8.csv)
- [methods/audit/supplement_version_and_gray_leads_utf8.csv](methods/audit/supplement_version_and_gray_leads_utf8.csv)
- [methods/audit/targeted_fulltext_14_utf8.csv](methods/audit/targeted_fulltext_14_utf8.csv)
- [methods/manual_classification_20261007_original.csv](methods/manual_classification_20261007_original.csv)
- [methods/manual_classification_pending36_20261007_original.csv](methods/manual_classification_pending36_20261007_original.csv)
