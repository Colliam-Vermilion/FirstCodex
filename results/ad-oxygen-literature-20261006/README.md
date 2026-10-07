# AD主动供氧文献库：现行统一交付

更新：2026-10-07，完成新增36候选逐篇证据复核及方法审计。原28条人工分类保持不变。原候选11篇完成分类，1条重复R13854并入已有R01238，24篇仍有具体范围疑点。现行**475条去重记录、107列**，原400个ID全部保留；R13854别名和原证据可追溯。

|类别|所有类型|期刊文献|
|---|---:|---:|
|1 AD反应器/内部循环供氧|176|167|
|2 专门厌氧水解/产酸供氧|54|53|
|3 独立预处理（相关研究）|64|61|
|4 综述性来源|43|43|
|5 排除，仅查重/审计|114|105|
|6 真正待确认|24|22|
|合计|475|451|

已确认期刊原始研究281；学位/学生报告6、其他非期刊18单列。类别4含R07033综述性技术说明；R11773沿用人工综述判断、独立类型核验未完成。类别3中R13890为非生物湿式空气氧化前处理，属性已注明，不混称生物微曝气。

## 文件导航

- [最终Excel](final_results/ad_oxygen_download_review_20261006.xlsx)及[UTF-8 CSV](final_results/ad_oxygen_download_review_utf8.csv)：同一475条主库。Excel含36篇逐项复核、人工案例28对应及历史审计。
- **[36篇复核对照与原/新证据](methods/audit/pending36_scope_reaudit_utf8.csv)**：保留全部36个原ID，包括合并条目；题名、摘要、二手语境、理由、缺失信息、人工案例和是否仍需用户处理逐项提供。
- [本轮实际方法审计及5个问题的回答](methods/08_pending36_reaudit_zh.md)、[人工28条案例对应](methods/audit/manual28_candidate_comparisons_utf8.csv)、[重复ID映射](methods/audit/record_id_aliases_utf8.csv)、[来源获取审计](methods/audit/pending36_evidence_access_utf8.csv)。
- [真正待确认24条](manual_review/scope_pending_utf8.csv)：真菌底物处理有氧操作12、气泡气源/用途5、位置/系统/干预性质7。只需列明的关键一段/图，不要求阅读全文；缺DOI、剂量或全文本身不是待确认理由。
- [追溯新增确认48篇](final_results/new_from_review_chase_utf8.csv)及[其中缺全文的资料提取表](manual_review/new_classified_missing_fulltext_utf8.csv)：已分类，不需重复范围筛选。
- [43篇综述追溯](methods/audit/review_reference_tracking_43_utf8.csv)、[5044条引用匹配](methods/audit/reference_matching_utf8.csv)、[28篇仍缺完整引用列表](manual_review/reviews_missing_complete_references_utf8.csv)。
- [早期相关45条](manual_review/early_related_references_utf8.csv)：43条研究线索、2条综述线索，不计入2012-01-01至2026-10-07主库。新综述线索19篇尚未追溯。
- [唯一最终ZIP](ad_oxygen_literature_final.zip)：现行交付文件，逐字节核验，不含ZIP自身/PDF。

原43综述完整参考文献15、部分27、未取得1；取得完整列表不等于阅读全文。201条未解析完整题名、部分引用覆盖及未追溯新综述仍有漏检风险。

## 证据与全文状态

本轮可读研究摘要25篇：原18、外部补6、重复匹配复用1；检查已有二手语境11篇，原论文PDF定向核查2篇。R13871原“摘要”是58字符版权声明，已从现行摘要清除，旧文本保留审计；文献类型由White Rose索引补为学位论文。

本轮仅R13839和R01238（由重复R13854定位）实际取得正式PDF后更新全文获取状态，其余分类变化不改变获取状态。R13839供气在分解舱之后的排放过滤舱，按Methods/图2排除。R13878根据明确二手氧释放AD语境纳入，不强制原文剂量。作者摘要、二手陈述与推断分别标明；不声称阅读全文。

用户原表仅“结果”列标签，没有逐篇文字理由；同步前自动理由未冒称为人工理由。28条结论、旧证据及原始人工表完整保留。此前80/224/83审计、76缺全文表为历史阶段范围，不是全库获取数量。PDF只保存在运行环境，路径不是GitHub附件。

## EndNote导入

六期刊分类RIS分别167、53、61、43、105、22；学位/报告RIS6、其他非期刊RIS18。八个分区互斥覆盖475条；待确认24=期刊22+学位1+未知类型1，后两条在相应非期刊RIS中；类别5不用于下游纳入分析。期刊原始研究合并RIS281是期刊类别1–3的替代导入；追溯新增RIS48也是替代增量（包含1条会议），已经在全量分类中，**不要重复导入**。旧库合并/移除R13854并更新R01238，ID别名在RIS N1及审计中保留。

EndNote：File → Import → File；Import Option选Reference Manager (RIS)，Text Translation选Unicode (UTF-8)。作者逐AU，学位THES、报告RPRT、会议CONF、其他未知GEN保留正确类型。

## 方法与验证

methods/01–08保留检索式、日期、范围标准、阶段数量、证据实际阅读范围、获取失败及方法局限。07的476条/40新增/36候选是阶段快照；08及主库为现行。[验证报告](methods/audit/final_validation.json)检查475个唯一ID、原400/人工28、Excel/CSV逐值、RIS分区、重复别名与ZIP一致。无配置、凭据、PDF或会话数据提交。

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
