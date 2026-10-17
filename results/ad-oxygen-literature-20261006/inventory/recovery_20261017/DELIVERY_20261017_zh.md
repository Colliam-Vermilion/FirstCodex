# 2026-10-17 恢复、继续获取与私有Git备份交付

恢复基线：远端bac51bfccceae13a91745322ed5793260e30a85c，实际49份原件（40正文、9官方SI）和5份历史派生Excel，共54件。

当前：101篇有效正文、115份正文PDF、12份官方SI；严格正文+SI原件127份、290712157字节。

本轮正文新增首次获取8个ID；重新获取历史正文55份（54个ID，含不同字节版本）。本轮正文新增文件75份、重新获取SI3份，全部原格式保留。两篇硕士论文各7个分章PDF，完整组作为一篇计数。

已读回证明覆盖127份严格原件，290712157字节；已取得但尚未读回的严格原件0份、当前解析文件0份。独立对象库和逐文件SHA/大小/可读性证据见backup_manifest_utf8.csv；本汇总的数据证明提交为2f0be721c6f1868f2499703dbac2e8af671cf2e5，之后的最终元数据提交另做sync-final核验。

尚缺正文325个ID。逐ID原因和暂停策略证据见remaining_main_failure_matrix_utf8.csv。明确声明但尚未取得的官方SI：1份。

- R13833 / es8b00894_si_001.docx：https://pubs.acs.org/doi/suppl/10.1021/acs.est.8b00894/suppl_file/es8b00894_si_001.docx；来源403/挑战或CONNECT拦截，未计为已下载。

SI逐记录状态：{'downloaded': 10, 'explicit_no_attachments_in_complete_JATS': 7, 'access_failed': 343, 'checked_no_file_links_found_coverage_unconfirmed': 58, 'identity_review_required': 4, 'not_checked': 3, 'partial_or_access_failed': 1}。文章页未发现链接、访问失败、身份未核验和尚未检查均不判无附件。外部数据5处声明对应4个项目，链接/披露大小见external_data_links_utf8.csv；未下载数据库。

历史旧SHA正文仍缺8份；已有其他核验版本的ID为['R10086', 'R13955']，不将替代版本称为旧字节恢复。

当前解析1531个文件；60327条文本块、243张自动表格、53页英文OCR。SQLite quick_check=ok，microaeration查询命中1128条。OCR/表格未逐数值人工校对。HTML仅为来源证据，ZIP内容按成员SHA建索引，不重复原字节。

72项历史解析路径未作为当前文件恢复，原因按源对象区分：{'historical_acquired_current_original_not_restored': 17, 'available_as_verified_original_archive_member': 5, 'redundant_transport_archive_not_retained': 50}。其中50项是冗余传输包旧索引，5项是已在官方ZIP中SHA核验的模型旧解析，17项绑定未恢复的旧正文SHA；历史清单保留，不能冒称旧文件已恢复。

554条原库前110字段全部一致，人工原始附件SHA一致；没有新主题检索、重新分类或修改main。安装、实际MCP及三篇上传门槛证据见同目录JSON，完整方法见../../methods/20_new_environment_backup_20261017_zh.md。

环境安装/启动/网络配置保存为草稿。需在环境设置保存并发布才可供后续任务使用；新任务冷启动未实测，不能用环境快照代替本次Git原件备份。
