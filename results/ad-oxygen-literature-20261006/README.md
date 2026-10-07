# AD主动供氧文献库：现行统一交付

更新：2026-10-07。复用完整旧检索并执行5组过程桥接查询，新增905条来源记录；确认新增49条文献（27篇期刊原始研究、13篇学位论文、4篇会议资料、5篇综述/综述章节）。现行**554条、107列**，原505条及53个人工判断逐值不变。此次没有获取或阅读原文全文。

|类别|所有类型|期刊文献|
|---|---:|---:|
|1 AD反应器/内部循环供氧|208|187|
|2 专门厌氧水解/产酸供氧|57|56|
|3 独立预处理（相关研究）|111|102|
|4 综述性来源|50|48|
|5 排除，仅查重/审计|128|118|
|6 库内范围待确认|0|0|
|合计|554|511|

已确认期刊原始研究345；学位/学生报告19、其他非期刊24另列。类别5不用于纳入分析。主库外98条具体范围疑点候选、4条范围明确但元数据待核验资料**不计入554条**。全池尚有10107个身份未处理（其中宽词9633）；不能称全部筛尽。新增文献数量不是独立实验数量，学位/会议关联另记。

## 本轮文件导航

- [继续检索与筛选方法](methods/11_continued_search_and_screening_zh.md)、[5组完整查询/分页](methods/audit/continuation_search_log_utf8.csv)、[互斥统计及限制](methods/audit/continuation_search_validation_summary.json)。旧15组已完整，复用不重复执行。
- [新增49条文献表](methods/audit/continuation_confirmed_new_utf8.csv)、[49条增量RIS](final_results/continuation_confirmed_new.ris)、[元数据核验与限制](methods/audit/continuation_metadata_verification_utf8.csv)。已含在全量中，增量RIS是替代导入。
- [453行逐项筛选审计](methods/audit/continuation_targeted_screening_utf8.csv)、[旧58候选处理对照](methods/audit/continuation_prior58_resolution_utf8.csv)。旧58中12明确排除，46仍缺分类关键事实，不以缺全文/参数保留待确认。
- [10894身份完整去重/状态表](methods/audit/continuation_dedup_all_returns_utf8.csv)、[11168行逐输入匹配](methods/audit/continuation_dedup_input_matching_utf8.csv)。3对同PMID无DOI身份别名已核对，主库既有记录不删除；库内排除也查重。
- [98条主库外范围候选](manual_review/continuation_scope_candidates_utf8.csv)、[版本及范围明确的元数据待核验表](methods/audit/continuation_versions_and_metadata_utf8.csv)、[学位/会议与期刊关联线索](methods/audit/continuation_study_version_links_utf8.csv)。不是默认用户全文下载任务，先核对具体疑点。
- [10107条未处理返回及完整摘要](manual_review/continuation_unprocessed_returns_utf8.csv)：按稳定线索ID继续筛选，保留来源/查询，不视为排除或已完成。
- [新增已分类但缺全文](manual_review/continuation_classified_missing_fulltext_utf8.csv)：不要求重复范围筛选。[1998原研究/2020再版关联](manual_review/continuation_early_republished_utf8.csv)不计入当前新增研究。
- [最终Excel](final_results/ad_oxygen_download_review_20261006.xlsx)、[UTF-8总CSV](final_results/ad_oxygen_download_review_utf8.csv)与[唯一统一ZIP](ad_oxygen_literature_final.zip)：同一554记录。XLSX保留历史证据表，新增本轮筛选/查询/候选/旧58处理表。

## 历史方法与审计

methods/01–11依次保留检索、224筛选、阅读层级、83下载、80复核、人工同步、43综述追溯、36复核、36人工同步、漏收原因与15补检、此次继续检索的方法。

- [58篇漏收原因](methods/audit/omission_reasons_58_utf8.csv)、[关键词表](methods/audit/supplement_keywords_utf8.csv)、[旧15查询](methods/audit/supplement_search_log_utf8.csv)、[第10轮方法](methods/10_omission_analysis_and_supplement_search_zh.md)。
- [旧218处理快照](methods/audit/supplement_targeted_screening_218_utf8.csv)、[旧58候选快照](manual_review/supplement_evidence_insufficient_utf8.csv)及[旧10263行返回快照](methods/audit/supplement_dedup_all_returns_utf8.csv)均为历史，不代表现行候选状态；当前看第11轮表。
- [第10轮新增30篇](methods/audit/supplement_confirmed_new_utf8.csv)/[增量RIS](final_results/supplement_confirmed_new.ris)、[追溯新增58篇](final_results/new_from_review_chase_utf8.csv)/[增量RIS](final_results/new_from_review_chase.ris)：同样已含全量，不重复导入。
- [人工36同步对照](methods/audit/pending36_manual_sync_utf8.csv)、[原件](methods/manual_classification_pending36_20261007_original.csv)、[人工28案例](methods/audit/manual28_candidate_comparisons_utf8.csv)、[重复ID映射](methods/audit/record_id_aliases_utf8.csv)。附件原字节保留，其中36附件实际GB18030，原文件名utf8不能代替编码核验。
- [43综述追溯](methods/audit/review_reference_tracking_43_utf8.csv)、[5044引文匹配](methods/audit/reference_matching_utf8.csv)、[28篇缺完整引用](manual_review/reviews_missing_complete_references_utf8.csv)、[早期45历史文献](manual_review/early_related_references_utf8.csv)。原43综述完整15、部分27、未取得1；201条未解析引用、未追溯新综述仍有覆盖缺口。
- [库内范围待确认](manual_review/scope_pending_utf8.csv)：0行，不包含主库外98候选；[下载83记录](manual_review/download_status_83_utf8.csv)与以前人工获取清单保持原获取证据，分类同步没有改动获取状态。

## 分类与全文状态

原505完整对象及CSV行不改写，包含排除和所有人工判断。K人工优先、K空沿用J的既有结论不更动。新增按主动氧/空气、位置与阶段分类；独立沼气净化/终端消化后处理排除，内部供氧脱硫纳入，AD前或阶段间有氧预处理单列。全文可获取性独立，未下载不能判无免费全文；此次未称摘要筛选为全文复核。

学位与学生报告单列；本轮13学位正式授予年未独立核验时主表留空，RIS PY采用索引年份并在N1说明来源限制。新会议和书章不混入期刊研究数。中文作者缩略名及CrossRef疑机构作者项逐项标记，未编造缺失字段。R07033沿用原综述技术说明，R11773保留原人工综述分类；类型独立核验仍见旧审计。

## EndNote导入与替代方案

全量可使用六个期刊分类RIS（187、56、102、48、118、0）+学位/报告RIS19+其他非期刊RIS24：**八分区互斥覆盖554条**。类别5只用于审计，进行下游纳入分析可跳过。期刊原始研究合并RIS345是期刊类别1–3的替代方案；新增49、此前30、追溯58增量RIS也都是替代导入，**不要与全量重复导入**。其他非期刊RIS含会议、专利与2新综述章节；依据KW类别筛选。

EndNote：File → Import → File；Import Option选择Reference Manager (RIS)，Text Translation选择Unicode (UTF-8)。作者逐个AU，JOUR期刊、THES学位、RPRT报告、CONF会议、CHAP书章、GEN未知。保留ID/N1和KW分类。

## 完整性和继续处理

完整查询不等于完整筛选。13574累计来源返回（含2书目）进入11168行复用/新输入，10894去重身份；原库266、新增49、排除319、范围候选98、版本/身份51、范围明确元数据待核验4、未处理10107，互斥合计一致。后续先按未处理表检查完整题名/摘要，必要时补语境或Methods，按全库（含排除）查重，保留人工判断，避免复跑完整查询。

[当前验证报告](methods/audit/final_validation.json)核验554唯一ID/DOI、原505与53人工记录不变、Excel/CSV逐值、8RIS分区、增量、候选不混库、统一ZIP逐字节一致。新增检索日期上限为2026-10-07，未声称找齐全部文献。只提交结果、方法与审计，不提交PDF、运行日志、配置、凭据或浏览器数据。

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
- [final_results/continuation_confirmed_new.ris](final_results/continuation_confirmed_new.ris)
- [final_results/new_from_review_chase.ris](final_results/new_from_review_chase.ris)
- [final_results/new_from_review_chase_utf8.csv](final_results/new_from_review_chase_utf8.csv)
- [final_results/other_nonjournal_records.ris](final_results/other_nonjournal_records.ris)
- [final_results/supplement_confirmed_new.ris](final_results/supplement_confirmed_new.ris)
- [final_results/theses_and_student_reports.ris](final_results/theses_and_student_reports.ris)
- [manual_review/classified_missing_fulltext_utf8.csv](manual_review/classified_missing_fulltext_utf8.csv)
- [manual_review/continuation_classified_missing_fulltext_utf8.csv](manual_review/continuation_classified_missing_fulltext_utf8.csv)
- [manual_review/continuation_early_republished_utf8.csv](manual_review/continuation_early_republished_utf8.csv)
- [manual_review/continuation_scope_candidates_utf8.csv](manual_review/continuation_scope_candidates_utf8.csv)
- [manual_review/continuation_unprocessed_returns_utf8.csv](manual_review/continuation_unprocessed_returns_utf8.csv)
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
- [methods/11_continued_search_and_screening_zh.md](methods/11_continued_search_and_screening_zh.md)
- [methods/audit/actual_evidence_basis_224_utf8.csv](methods/audit/actual_evidence_basis_224_utf8.csv)
- [methods/audit/additional_review_leads_utf8.csv](methods/audit/additional_review_leads_utf8.csv)
- [methods/audit/citation_seeds_utf8.csv](methods/audit/citation_seeds_utf8.csv)
- [methods/audit/classification_changes.json](methods/audit/classification_changes.json)
- [methods/audit/cleanup_validation.json](methods/audit/cleanup_validation.json)
- [methods/audit/continuation_confirmed_new_utf8.csv](methods/audit/continuation_confirmed_new_utf8.csv)
- [methods/audit/continuation_cowpea_version_identity.json](methods/audit/continuation_cowpea_version_identity.json)
- [methods/audit/continuation_dedup_all_returns_utf8.csv](methods/audit/continuation_dedup_all_returns_utf8.csv)
- [methods/audit/continuation_dedup_input_matching_utf8.csv](methods/audit/continuation_dedup_input_matching_utf8.csv)
- [methods/audit/continuation_early_reprint_identity.json](methods/audit/continuation_early_reprint_identity.json)
- [methods/audit/continuation_metadata_verification_utf8.csv](methods/audit/continuation_metadata_verification_utf8.csv)
- [methods/audit/continuation_primary_identity_checks_utf8.csv](methods/audit/continuation_primary_identity_checks_utf8.csv)
- [methods/audit/continuation_prior58_resolution_utf8.csv](methods/audit/continuation_prior58_resolution_utf8.csv)
- [methods/audit/continuation_search_log_utf8.csv](methods/audit/continuation_search_log_utf8.csv)
- [methods/audit/continuation_search_validation_summary.json](methods/audit/continuation_search_validation_summary.json)
- [methods/audit/continuation_study_version_links_utf8.csv](methods/audit/continuation_study_version_links_utf8.csv)
- [methods/audit/continuation_targeted_screening_utf8.csv](methods/audit/continuation_targeted_screening_utf8.csv)
- [methods/audit/continuation_versions_and_metadata_utf8.csv](methods/audit/continuation_versions_and_metadata_utf8.csv)
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
