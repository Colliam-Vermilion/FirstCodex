# AD主动供氧文献库：现行统一交付

检索日期/截止日期：2026-10-06；发表范围2012-01-01至当日。本版完成全部80条范围重新复核，沿用400个稳定ID，不新增重复版本目录。逐篇筛选与阅读全文、范围分类与全文获取分别记录。

## 当前数量

|范围类别|所有文献类型|期刊文献（分类RIS）|
|---|---:|---:|
|1 AD反应器/内部循环供氧|145|139|
|2 厌氧水解/产酸供氧|41|40|
|3 AD前好氧/微好氧预处理|42|39|
|4 综述|42|42|
|5 排除|102|95|
|6 真正仍待范围判断|28|24|
|合计|400|379|

期刊原始研究218条（139+40+39）；另保留5条学位论文/学生报告和16条会议、海报、专利等非期刊资料。类别1–3共228条范围记录，包括3条学位/报告和7条会议/海报资料，不能把228全部称期刊原始研究。

80条本轮复核：52条完成分类，28条保留具体疑点。完成者仅题名24、摘要22、用户已核摘要摘述+题名1、定向全文4、研究海报1。48条已分类但未获论文全文另列为可选资料提取，**不是范围筛选任务**。R01349的供氧位置采用用户已核读摘要的摘述，独立原摘要仍未取得，该限制明确保留。

## 最终文件与EndNote导入

- [Excel](final_results/ad_oxygen_download_review_20261006.xlsx)：400条83列；包括80篇复核对照、28条真正待判范围、48条已分类缺全文、学位/报告及下载状态83等工作表。
- [UTF-8 CSV](final_results/ad_oxygen_download_review_utf8.csv)：与Excel文献库一致；旧字段与前轮证据保留，追加本轮字段。
- final_results/六个category1–category6 RIS：**只含期刊文献**，对应上表右列。
- [theses_and_student_reports.ris](final_results/theses_and_student_reports.ris)：5条学位/FYP记录，单列不混入期刊研究。
- [other_nonjournal_records.ris](final_results/other_nonjournal_records.ris)：16条会议、海报及专利，KW保留范围分类。
- [confirmed_original_research.ris](final_results/confirmed_original_research.ris)：218条期刊原始研究，**替代期刊类别1、2、3的导入**，不能同时导入两套。

前八个分类文件互斥、合计400条，无遗漏。若导入全审计库，选六类期刊RIS+学位报告RIS+其他非期刊RIS，不再导入合并文件。若只建已纳入期刊库，选合并218条并另导入42条综述。排除和候选仅用于审计/候选组。此前旧RIS请保留另库或按稳定ID更新，勿与本版直接重复批量导入。

EndNote：File → Import → File，Import Option选Reference Manager (RIS)，Text Translation选Unicode (UTF-8)。作者分别AU，学位THES、FYP报告RPRT、会议/海报CONF、专利PAT；不把摘要/海报当正式期刊文章。

## 人工处理导航

- [28条真正待判范围CSV](manual_review/scope_pending_utf8.csv)和[逐条疑点/官方入口](manual_review/scope_pending_zh.md)：只保留影响类别的信息；优先看摘要，必要时Methods/图，不强制整篇通读。
- [48条已分类但缺论文全文](manual_review/classified_missing_fulltext_utf8.csv)：可选补参数/效果量，无需重复筛选；海报/会议摘要不要求找不存在的期刊全文。
- [80条全文可获取性审查](manual_review/fulltext_access_audit_80_utf8.csv)：实际访问入口/响应、开放或限制证据与本地文件信息，分开于范围分类。
- [83条最终下载状态](manual_review/download_status_83_utf8.csv)：保留此前获取处理记录，更新当前范围决定及R03155新获109页正文。
- [学位和学生报告表](manual_review/theses_and_student_reports_utf8.csv)及[机构、可获取性和期刊关联说明](manual_review/theses_and_student_reports_zh.md)。

PDF只留运行环境，路径不是GitHub下载链接。R00888出版社网页/PDF入口已定位但遭本环境代理CONNECT403；R04605官方开放博士PDF入口存在，但存储重定向遭代理阻断。不称“无法免费获取”。学校订阅权限未认证，使用清单官方入口自行登录/MFA；没有提交任何账户配置、凭据或会话数据。

## 方法与审计

- methods/01–04：完整保留检索、224条初次复核、14篇实际定向阅读/海报澄清、83篇下载复核各阶段方法；其旧数量/文件名为明确标注的历史快照，不是当前目录导航。
- [05方法修正与五例校准](methods/05_scope_reassessment_correction_zh.md)：本轮范围标准纠正、证据层级、正文实际读页和访问局限。
- [80篇复核对照](methods/audit/scope_reassessment_80_utf8.csv)：原类别/理由/证据、新分类、作者陈述/推断、全文状态、是否需用户处理。
- audit/继续保留110条搜索日志、28个引文种子、224条审计、14篇阅读定位、海报与流程试验、阶段统计；final_record_metadata.json是唯一现行400条结构化元数据，包含80篇evidence_history，历史版本通过Git追溯。
- [本轮汇总](methods/audit/scope_reassessment_summary.json)及[当前格式验证](methods/audit/final_validation.json)。cleanup_validation.json只记录上一轮目录清理时的检查，哈希不是本轮新数据的哈希。

剩余28条中，12条已有完整摘要但仍缺关键方法信息，优先定向查Methods/流程图；16条优先补完整摘要或出版物类型，其中R11773不必先找全文。新摘要若明确回答疑点即可分类，不将28条都当成阅读全文任务。

没有增加ZIP或重复交付目录。来源覆盖、题名/摘要信息量和全文访问仍有限，不承诺绝对完整；全文未获不是排除理由。

## 完整保留文件清单

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
- [methods/audit/actual_evidence_basis_224_utf8.csv](methods/audit/actual_evidence_basis_224_utf8.csv)
- [methods/audit/citation_seeds_utf8.csv](methods/audit/citation_seeds_utf8.csv)
- [methods/audit/classification_changes.json](methods/audit/classification_changes.json)
- [methods/audit/cleanup_validation.json](methods/audit/cleanup_validation.json)
- [methods/audit/final_record_metadata.json](methods/audit/final_record_metadata.json)
- [methods/audit/final_validation.json](methods/audit/final_validation.json)
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
