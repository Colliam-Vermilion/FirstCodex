# 新环境恢复与全部原件备份（2026-10-17，当前）

以远端提交 `bac51bfccceae13a91745322ed5793260e30a85c` 实际文件恢复：40正文、9官方附件、5历史派生件。554条及全部人工判断保留，类别1–4共426条，不重新检索或分类。

当前实际核验正文 **98篇**，缺正文 **328篇**。实际对象角色：{'main': 100, 'supplementary': 11, 'derived': 5, 'evidence_xml': 17, 'evidence_html': 38}。历史记录但无原件者明确标记“历史已获取，当前原件未恢复”，历史SHA和替代版本分开保留。3篇重新下载、上传及独立远端读回门槛已完成，后续按5篇或10分钟检查点推送；仅远端核验通过后称已备份。

- [最新状态](inventory/recovery_20261017/status.json)、[逐文件备份/独立读回清单](inventory/recovery_20261017/backup_manifest_utf8.csv)、[远端核验回执](inventory/recovery_20261017/remote_readback.json)
- [正文原件](original_files/fulltext/)、[补充材料原件](original_files/supplementary/)、[逐ID解析结果](papers/)、[统一原件清单](inventory/assets_utf8.csv)
- [426获取状态](manual_review/current_environment_acquisition426_utf8.csv)、[尚缺正文](manual_review/current_environment_need_fulltext_utf8.csv)、[历史缺件队列](inventory/recovery_20261017/historical_reacquisition_queue_utf8.csv)、[SI逐篇状态](manual_review/supplementary_material_status_utf8.csv)
- [总Excel](final_results/ad_oxygen_download_review_20261006.xlsx)、[总CSV](final_results/ad_oxygen_download_review_utf8.csv)、[分组RIS](final_results/)
- [安装脚本](methods/runtime_support/recover_20261017.sh)、[恢复/下载/解析/备份脚本](methods/recovery_20261017.py)、[现有文献及SI续取脚本](methods/continue_records_20261017.py)

所有取得且允许保存的原件、解析结果和记录直接备份到本私有结果分支；不依赖旧环境或外部存储。既有ZIP仅为历史元数据包，无论文原件，不新增重复原件整包。以下数量、局部交付和未备份说明均为历史快照，当前以本节及20261017清单为准。


# 第18轮：文件审计、统一标准与全文检索（2026-10-15）

以远端提交 `0c5fd5b93ae89e5db723df8a1caeb0b3d278c53e` 和实际文件为基准。554条、分类208/57/111/50/128/0及53条人工判断不改，不重新检索或范围分类。

当前主选正文89个ID（80历史SHA相同、2历史另字节副本、7新增）；另外保留R11596一份同文不同字节版本，所以实际正文PDF共90份、仍是89个ID。历史91原字节缺11。官方SI12、ZIP派生6；另17个JATS全文XML及10个仓储传输包为来源证据，不混作PDF或官方SI。统一清单135个不同SHA对象，约302.15 MB；原有original_files的54个持久对象全部保留并复核，没有退回样例。

已实际解析全部可解析现有文件：54,387检索片段、229份自动结构化表格、907个解析文件和SQLite全文索引；可回到ID/源SHA/PDF页、XML章节XPath、Word段落/表格、Excel工作表/单元格。53页OCR增加文字，7页无新增文字，模型及图像视觉内容明确未索引。全文文字索引覆盖93个ID，含4个缺PDF但已有XML的ID，不等于93篇PDF已取得。

- [文件审计和统一标准](methods/18_file_audit_and_fulltext_standard_zh.md)、[统一汇总Excel](inventory/unified_library_inventory.xlsx)
- [论文状态554](inventory/papers_utf8.csv)、[原件/来源135统一清单](inventory/assets_utf8.csv)、[解析文件清单](inventory/extracted_files_utf8.csv)、[实际文件SHA核查](inventory/current_inventory_sha_verification.json)
- [真实目录及来源映射示例](papers/R03161/metadata.json)、[现有Git原件](original_files/README.md)、[图引用/传输包映射](inventory/source_media_map.json)
- [Windows下载、全部SI、解析和回填流程](windows/README_zh.md)、[337缺PDF队列](windows/main_records337_utf8.csv)、[SI426核查队列](windows/supplementary_review426_utf8.csv)
- [Git原件及样例独立读回凭证](inventory/github_delivery_readback.json)（54原件＋58解析文件全SHA通过）
- [全量私有存储方案及需用户连接的步骤](methods/19_private_storage_and_return_zh.md)、[私有包准备回执](inventory/private_package_preparation.json)、[包独立还原测试](inventory/private_package_roundtrip_validation.json)

本轮只新增3个允许共享ID（R03161/R06325/R09236）的58个解析样例，包含正文与Excel/Word附件；没有独立CSV、视频或代码研究样例。完整907文件解析、索引及81个未入Git原件/来源对象已准备私有交付包，外部存储尚未连接，不能称全量已备份。GitHub保留已验证54原件；后续存储连接不能成为暂停审计和工具交付的理由。

以下恢复轮次及更早段落为历史快照；本轮统一当前状态以inventory及papers为准，旧总表/人工附件保持原字节。

# 新环境恢复与继续获取（2026-10-15，现行）

源提交 `ec0cba326b45075e9a902a2aa850c78948198813` 的554条总库、53条人工结果及方法/脚本已恢复。类别1–6仍为208/57/111/50/128/0，原110列逐值保留，追加12个当前状态字段，共122列。本轮没有重新文献检索或范围分类，128条排除记录跳过。

当前已核验正文89篇：80篇与历史原件SHA完全相同、2篇历史ID取得已核验不同字节版本、7篇原未获全文现已取得。历史91的原SHA不覆盖，11份历史字节尚缺，其中9个ID当前仍无正文。当前缺全文337篇＝原未获队列剩328篇＋历史当前无正文9篇。

补充材料已核验10篇的12个官方附件（PDF3、DOCX4、XLSX2、ZIP3）；6个解包派生文件另列，包括5个Excel及1个SketchUp模型，不重复计官方附件。未取得或入口受阻不写“无SI”。

- [现行方法、结果和交付边界](methods/17_current_retrieval_and_delivery_zh.md)、[恢复/工具方法](methods/16_environment_recovery_zh.md)
- [当前426篇简表](manual_review/current_environment_acquisition426_utf8.csv)、[当前缺正文337篇](manual_review/current_environment_need_fulltext_utf8.csv)、[原未获现剩328篇](manual_review/scansci_need_fulltext_utf8.csv)、[91历史恢复队列](manual_review/historical91_original_recovery_queue_utf8.csv)
- [最终Excel](final_results/ad_oxygen_download_review_20261006.xlsx)、[554条总CSV](final_results/ad_oxygen_download_review_utf8.csv)、[SI426状态](manual_review/supplementary_material_status_utf8.csv)
- [可取回原件目录及许可](original_files/README.md)、[实际持久对象清单](methods/audit/current_original_files_manifest_utf8.csv)、[全部当前正文及本机/持久区分](methods/audit/current_local_verified_body_files_utf8.csv)、[SI及派生件清单](methods/audit/current_supplementary_files_manifest_utf8.csv)
- [独立远端原件读回证据](methods/audit/current_remote_original_readback_20261015.json)、[当前统计](methods/audit/environment_recovery_summary_20261015.json)、[域名137项](methods/network_allowed_domains_20261015.txt)

40份明确CC BY/CC0正文、9个许可允许的官方SI及5个派生Excel保存真实字节到结果分支 `original_files/`。其余49份正文、3个官方SI及1个模型派生件目前仅在本机；尚需用户指定的私有持久存储，不能称已交付或已备份。GitHub可逐文件下载原件，或对该结果分支选择 Download ZIP；`ad_oxygen_literature_final.zip` 现为**表格/方法/审计包，不含论文和SI二进制原件**，请勿混淆两个ZIP。

小样本3篇正文＋官方SI及派生件已于提交 `e822732c4efbd199e2828e3cf255e3cd27c4511b` 从独立Git对象库远端取回、SHA一致，之后才启动批量。全部可发布原件的最终读回状态以上述审计为准。新云任务本身的冷启动尚未实测。

Nature固定 `b543e8b998eb2df1fd44641cc8b262c638c2b442`、ScanSci PDF1.18.0及实际stdio MCP已验证。Crossref/Unpaywall及部分出版商/仓储真实成功；CONNECT拦截、出版商挑战、NTUA503/EBI500和机构限制分别保留，不称全部网络恢复。137域、安装/启动说明已保存配置草稿，**需要在环境设置审阅、保存并发布**；草稿不等于当前策略已应用，环境发布不作为原件备份。

以下第15轮及更早段落均为历史记录；当时的数量、目录和下载/交付结论仅代表当时，不覆盖本页及第17轮当前状态。

# 第15轮：其他公开渠道继续获取（2026-10-12）

已用既有公开PDF对照验证实际下载；370条未获全文继续分来源处理，保留已有56。新增35份独立PDF（35条记录），现有核验全文91条，尚未取得335条，未处理0。总库554、全部人工判断及范围数量不改。某个来源受阻没有停止其他来源。

- [新增全文清单](manual_review/scansci_new_verified_fulltexts_utf8.csv)、[现行426下载状态](manual_review/scansci_download_status_utf8.csv)、[当前仍未取得全文](manual_review/scansci_need_fulltext_utf8.csv)
- [本人机构登录](manual_review/scansci_action_institution_utf8.csv)、[本人浏览器](manual_review/scansci_action_browser_utf8.csv)、[平台网络修复](manual_review/scansci_action_network_utf8.csv)：可重叠，只列仍待获取记录
- [本轮方法、WUR具体全文路径、保存/取回限制](methods/15_sourcewise_public_fulltext_zh.md)、[370条逐篇状态](methods/audit/scansci_sourcewise_record_status_utf8.csv)

以下第14轮及更早内容为历史；其“不扩大队列”判断已纠正，当前获取状态以第15轮为准。PDF没有自动上传Git，唯一ZIP只含表格/RIS/方法与审计。

# 第14轮：发布后实际联网与5篇下载复测（2026-10-12）

配置接口已读到新的已发布版本，但实际Elsevier API/跳转/出版商三域仍CONNECT403；原5篇本轮均无CONNECT错误，只有2篇Springer文章预览可访问，IWA/Scientific.net仍拒绝/挑战。实际PDF成功0，未扩大剩余365条；已核验全文仍56份。总库554及全部人工分类不变。

- [逐篇五步结果及下一步](manual_review/scansci_postpublication_pilot5_status_utf8.csv)
- [本轮有明确出版商机构登录证据的2篇](manual_review/scansci_pilot5_institution_access_utf8.csv)，其余3篇不归因为订阅
- [完整方法、重连/新任务能否解决的证据边界](methods/14_postpublication_pilot5_retest_zh.md)
- [真实访问错误/429实录](methods/audit/scansci_postpublication_access_events.json)、[Springer PDF入口200实际是HTML的证据](methods/audit/scansci_postpublication_publisher_pdf_checks.json)

以下第13/12轮为历史阶段说明；网络现状以第14轮实际请求为准。

# 第13轮访问诊断与Windows机构工作流（2026-10-12）

现行总库和人工分类保持554条、类别1–6为208/57/111/50/128/0；已核验PDF仍56份。本轮仅5条历史失败+1条OA控制及来源端点小批复测，没有重跑370条。

- [完整诊断、白名单设置、Windows同版本安装/HKUST登录MFA/Elsevier API/按ID回同步](methods/13_scansci_diagnosis_windows_zh.md)
- [370条非互斥障碍矩阵](methods/audit/scansci_obstacle_matrix_utf8.csv)、[统计](methods/audit/scansci_obstacle_statistics.json)、[403归因证据](methods/audit/scansci_http403_signature_audit.json)、[实际域名/重定向与复测状态](methods/audit/scansci_required_domains_utf8.csv)
- [Unpaywall小批真实结果](methods/audit/scansci_unpaywall_small_retest.json)、[题名DOI核验](methods/audit/scansci_unpaywall_identity_validation.json)、[实际MCP读邮箱核验（不含邮箱值）](methods/audit/scansci_mcp_email_check.json)、[入口复测](methods/audit/scansci_network_small_retest.json)、[来源端点复测](methods/audit/scansci_endpoint_retest.json)
- [Windows完整ID队列](manual_review/windows_remaining_fulltext_queue_utf8.csv)、[仅DOI自动队列](manual_review/windows_doi_download_queue_utf8.csv)、[5篇测试](manual_review/windows_pilot5_queue_utf8.csv)、[无DOI手工队列](manual_review/windows_no_doi_manual_queue_utf8.csv)、[回填模板](manual_review/windows_local_status_template_utf8.csv)。队列跳过现有56全文，不按输出顺序匹配。

Unpaywall授权邮箱已配置到仓库外，6个DOI均返回真实匹配记录；这不是新增PDF成功。串行+5–12秒延迟现已启用，包括1.18.0必需的fixed_request_delay_enabled。Elsevier API/跳转/出版商仍CONNECT403，IWA为挑战页，不能混为同一问题。白名单/联系人/可复现设置已保存草稿，requires_publish=true；当前接口不能确认已发布的运行策略，需要用户在环境设置检查保存、发布和实例传播。云端没有供本人完成登录的交互浏览器，HKUST只配置重写模板并保持通道关闭，未认证。

以下第12轮内容为当时的获取记录；其中“邮箱未配”等是历史状态，现状以第13轮为准。

# AD主动供氧文献库：现行统一交付

更新：2026-10-12，完成ScanSci PDF1.18.0安装、实际MCP下载及5篇验证，再处理全部类别1–4的426条。**复用13、新下载43，共56份通过全文身份/结构/版本核验；370未获核验全文，未处理0。**370含369未取回记录及1研究海报，未将海报计论文全文。当前环境没有完成HKUST机构认证。

主库仍为554条，现110列；分类数量1–6仍为208、57、111、50、128、0。所有原范围判断及53人工结果不改。类别5的128条跳过；库外98候选未自动扩大为下载任务。下载未处理0不等于旧10107宽词身份筛选已完成。

- [全文下载方法、验证与取回限制](methods/12_scansci_pdf_download_zh.md)、[下载统计](methods/audit/scansci_download_summary.json)。
- [426条逐篇获取清单](manual_review/scansci_download_status_utf8.csv)、[56有效PDF校验清单](methods/audit/scansci_verified_pdf_manifest_utf8.csv)、[370未获全文记录](manual_review/scansci_need_fulltext_utf8.csv)、[首批5验证](methods/audit/scansci_pilot5_utf8.csv)、[真实访问证据](methods/audit/scansci_access_evidence_utf8.csv)。
- [最终Excel](final_results/ad_oxygen_download_review_20261006.xlsx)、[UTF-8总CSV](final_results/ad_oxygen_download_review_utf8.csv)、[唯一统一结果ZIP](ad_oxygen_literature_final.zip)：不含论文PDF。全量RIS仅追加获取备注，范围分区和书目信息不改。
- [本地PDF分包及SHA](methods/audit/scansci_local_pdf_packages_utf8.csv)：文件仅在运行环境，不是下载附件。[从原来源重取/本地核验脚本](methods/retrieve_verified_fulltexts.py)：Python标准库，SHA一致才接受文件。26份URL有明确实际/历史绑定，其余30份标明来源名和候选链接，未猜测下载地址。

**PDF保存不等于已交付。**当前没有附件上传工具，PDF和分包未上传外部持久存储；跨任务保留需要在环境设置保存/发布当前快照，草稿已保存但尚未发布。可在自己的电脑运行上述脚本重取已验证版本，或通过平台支持的文件导出/经授权私有存储取回分包，再--verify-only校验。不把云端本地路径描述为下载链接。

运行环境仅HTTP公开下载可用；无供本人完成登录/MFA的交互浏览器。Unpaywall可选联系邮箱请在环境设置SCANSCI_CONTACT_EMAIL填写，启动适配写入仓库外工具配置；没有编造邮箱/API key或假定HKUST订阅已可用。部分来源代理CONNECT403/429造成覆盖限制；联网新增域名仍需发布草稿生效。技能/MCP已注册且PythonMCP客户端实际可调用，当前聊天工具列表可能需要重开会话。

以下保留检索及人工分类的历史方法；旧获取清单和旧增量RIS获取备注为阶段证据，现行取回状态看第12轮426表与文献库。

# 第11轮检索结果及历史说明（获取状态以第12轮为准）

更新：2026-10-07。复用完整旧检索并执行5组过程桥接查询，新增905条来源记录；确认新增49条文献（27篇期刊原始研究、13篇学位论文、4篇会议资料、5篇综述/综述章节）。现行**554条、110列（原107列＋3获取审计列）**，原505条及53个人工判断逐值不变。此次没有获取或阅读原文全文。

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
- [manual_review/scansci_download_status_utf8.csv](manual_review/scansci_download_status_utf8.csv)
- [manual_review/scansci_need_fulltext_utf8.csv](manual_review/scansci_need_fulltext_utf8.csv)
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
- [methods/12_scansci_pdf_download_zh.md](methods/12_scansci_pdf_download_zh.md)
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
- [methods/audit/scansci_access_evidence_utf8.csv](methods/audit/scansci_access_evidence_utf8.csv)
- [methods/audit/scansci_download_identity_queue_utf8.csv](methods/audit/scansci_download_identity_queue_utf8.csv)
- [methods/audit/scansci_download_summary.json](methods/audit/scansci_download_summary.json)
- [methods/audit/scansci_local_pdf_packages_utf8.csv](methods/audit/scansci_local_pdf_packages_utf8.csv)
- [methods/audit/scansci_pilot5_utf8.csv](methods/audit/scansci_pilot5_utf8.csv)
- [methods/audit/scansci_verified_pdf_manifest_utf8.csv](methods/audit/scansci_verified_pdf_manifest_utf8.csv)
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
- [methods/retrieve_verified_fulltexts.py](methods/retrieve_verified_fulltexts.py)
