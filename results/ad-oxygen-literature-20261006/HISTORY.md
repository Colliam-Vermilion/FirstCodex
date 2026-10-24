# 运行历史与阶段快照附录

此处集中环境恢复、网络、临时交付门槛、重复运行回执和有时效的计数。**最初检索/筛选、原件整理、JCR、组学和两条扩展研究均在[完整介绍](README.md)正常可见，不需要展开折叠块。** 方法01–11及后续研究方法保留原文件，不被笼统视为过期。

介绍修复：2026-10-25（Asia/Shanghai）。原README全文可在[修复前9208deddd固定快照](https://github.com/Colliam-Vermilion/FirstCodex/blob/9208deddd624e99b1314bac359c22349c8554c64/results/ad-oxygen-literature-20261006/README.md)及[上轮方法更新前0f9eeec20](https://github.com/Colliam-Vermilion/FirstCodex/blob/0f9eeec20bc23a421165c8cff352137ba68fac48/results/ad-oxygen-literature-20261006/README.md)核对；这些是原文证据，不是以整个旧介绍替代当前项目主体。

## 有日期的运行状态

|日期/阶段|当时记录|今天怎样使用|
|---|---|---|
|2026-10-06/07 初检至续检|400→475→505→554条，人工校正与查询/引用审计逐步加入|研究方法和形成依据见[第1阶段](README.md#stage-1)及methods/01–11；不用旧数量覆盖554总表|
|2026-10-12 ScanSci首轮|复用13、新下载43，共56篇核验全文；370未获|[方法12](methods/12_scansci_pdf_download_zh.md)及[审计](methods/audit/scansci_download_summary.json)保留逐次获取证据；不是现有全文总数|
|2026-10-12 网络/机构诊断|Elsevier CONNECT403、IWA挑战页、Unpaywall元数据可用；5篇/串行限流复测|[Windows/诊断13](methods/13_scansci_diagnosis_windows_zh.md)、[后续公开来源15](methods/15_sourcewise_public_fulltext_zh.md)；元数据成功不等于PDF，配置草稿不等于策略生效|
|2026-10-12 公开渠道继续|新增35份，合计91篇；当时PDF仍只在旧运行环境|历史SHA与后来原件恢复分开；不能把当时“下载成功”当新环境已持有，亦不再用“仅临时路径”否定后来Git备份|
|2026-10-15 环境恢复|89篇ID、80历史同字节、2其他字节版本、7新增；历史91原字节缺11|[方法16](methods/16_environment_recovery_zh.md)、[方法17](methods/17_current_retrieval_and_delivery_zh.md)；只代表该时点，不代表现在只剩89篇|
|2026-10-15 文件/解析标准|135不同SHA来源对象，54原件先入Git；其余当时待私有存储；337缺PDF队列|[方法18](methods/18_file_audit_and_fulltext_standard_zh.md)、[方法19](methods/19_private_storage_and_return_zh.md)、[当时读回](inventory/github_delivery_readback.json)；现行原件、38缺目标正文以第2阶段为准|
|2026-10-17 再恢复/持续备份|101篇核验正文、分批实际上传/远端读回|[恢复交付记录](inventory/recovery_20261017/DELIVERY_20261017_zh.md)、[备份清单](inventory/recovery_20261017/backup_manifest_utf8.csv)、[回执](inventory/recovery_20261017/remote_readback.json)；是本地合并前的云端基线|
|2026-10-23 本地上传与main副本清理|439本地+234既有输入按字节归665；30个main同字节副本经保全读回再正常提交清理|[方法21](methods/21_local_merge_and_jcr_20261023_zh.md)、[合并汇总](inventory/merge_20261023/merge_summary.json)、[独立新克隆回执](inventory/merge_20261023/remote_readback.json)；本次介绍修复未改main或原件|
|2026-10-24 组学/机制/数据阶段|B010、全池初筛/35完整摘要、D001–D005项目审计各有独立检查点|研究意义/方法见[第4](README.md#stage-4)、[第5](README.md#stage-5)、[第6阶段](README.md#stage-6)，不是纯运行日志；旧“下一批/尚未开始”仅属当时|
|2026-10-25 方法说明审计|补两份详细方法、查询附表和真实案例；发现队列12旧文漏排等|[方法审计](method_audit/README.md)保持；该轮README整体折叠现已更正，不回滚其研究说明或审计发现|

## 工具、网络和存储的历史边界

Nature技能固定版本与ScanSci 1.18.0的恢复、依赖/MCP探针不说明以后每个环境都已可调用；具体检索/下载仍以当次真实结果为准。早期可调用Nature MCP、后来官方HTTP备用及技能调用内部错误是不同阶段，不能合并成永久可用/永久失败。代理CONNECT错误、出版商挑战、订阅权限和仓储错误分开，不以失败断言无开放全文；没有机构密码或会话可随仓库迁移。

早期域名清单、配置草稿和发布回执是环境设置证据，**不是原件备份**。2026-10-23的original_files规范对象已通过私有结果分支真实Git blob备份及独立读回；旧“还需连接存储/只交付样例”不能覆盖这个后来状态。旧ZIP `ad_oxygen_literature_final.zip`只是该次表格/RIS/方法包，不含论文原件，也不保证囊括后续新增工作线；原件以[规范目录](original_files/)为准。

Windows 2026-10-15说明的限流、验证、SI和回填规则仍有用；其337/317/12等数字与私有包前提已过时，当前获取队列要按[38缺目标全文表](manual_review/current_environment_need_fulltext_utf8.csv)和规范清单重对，不能直接执行旧全量任务。

## 原章节与成果入口如何保留

[章节对照](method_audit/readme_restoration/chapter_map.md)列每个原标题的现行位置，[原成果链接索引](method_audit/readme_restoration/source_link_index.md)保留旧文件的可达入口/替代位置。两份新增详细方法、全部查询附表和案例不移动。机制/数据子README不再把整份原介绍折叠，重要研究说明已在当前介绍/详细方法中，过期阶段回执可由上述固定快照核对。

未保存的初始阅读/模型细节不补造，未取得的参考文献与原始数据不冒称完整。此附录不改文献分类、用户标签、库存、原件或任何筛选进度。
