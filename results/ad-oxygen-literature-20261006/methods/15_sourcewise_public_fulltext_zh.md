# 第15轮：按来源继续公开全文获取

2026-10-12，基线fd4eedbcb99d15fb8e6b59bb3780105098ac6c10。纠正上一轮把5篇失败作为全队列暂停条件的决定。已有56成功来源证明公开获取可用，5篇只能代表自身障碍，不能外推到其他记录。

从R03564实际已成功MDPI CDN重新取得19页PDF，题名/作者/DOI/正文/版次核验通过，SHA与原文件完全一致；对照不算新增，其他55文件未重新下载。原56逐一SHA核验且不进入下载队列。

370条未获核验全文全部执行分来源流程（包括此前5篇继续补查）；类别5的128条不下载，类别6主库0，库外98候选不自动加入。优先复用已有出版商/仓储/OA位置；再用Unpaywall/OpenAIRE寻找明确文章全文位置，并对仍失败的DOI记录补查当前OpenAlex/CORE（100条精确DOI查询返回上限，截断记录另列）。无DOI记录另外以OpenAlex题名检索最多5条身份候选，要求题名、首作者与已知年份一致，保留这一定位上限而不把它称为穷尽搜索。OA标记、HTML200及浏览器启动不是PDF成功。保存每条路径/状态及新增PDF身份证据。

PMC旧oa.fcgi公开包端点实际返回404，不是空包列表证明无OA；改从Europe PMC正式文章位置解析getPdf入口，5条PMCID均取得核验PDF（R04092/R05542/R07238/R08646/R10894）。此变化体现一个来源路径失效不停止其他路线。

补充文件核验解除4条自动检查失败：R06152印尼语正文/参考文献及出版商citation_doi/citation_pdf_url绑定；R13819官方Marquette仓储DOI与明确Download链接绑定作者接受稿；R13967正式2012 ACEEE会议出版版本；R06611是48页图像作者稿，全页OCR72711字符，第7页Methods、第31页References，仓储封面及正文题名作者/DOI一致。原自动结果保留在audit，不能把外部DOI核验说成PDF中印有DOI，也不能将文本提取不足等同没有完整论文。

最大2个文章任务，同时每个主机仅一个HTTP请求；API同主机间隔至少1.1秒，普通页面至少3秒。使用ScanSci网络/文件工具而不使用其仍会内部并行竞速的download调度；TLS保持可信CA验证，明确使用当前平台代理。429按Retry-After秒数/HTTP日期或无头时300秒冷却，至少60秒；主机冷却期间继续其他来源。已明确Elsevier CONNECT、IWA挑战、Scientific.net拒绝及Semantic Scholar连续429的路线在本轮直接记录跳过，不反复发送。新CONNECT/明确挑战仅暂停对应主机，不全局停止。

OpenAIRE初段提取包括了若干机构官网/关联数据URL；恢复点后改为仅文章fulltext/instance位置，剔除rels机构主页及ENA数据集。初段这些非全文请求保留审计但不能视为文章全文路径或索取新增白名单的依据；localhost/无效元数据不作为平台修复域名。检索引用匹配和文献范围未重新筛选。

R00313：WUR出版记录页正常、未展示文件附件；OpenAIRE发现https://edepot.wur.nl/206140，重定向目标library.wur.nl的/WebQuery/edepot/206140遭CONNECT403。此域名已追加网络草稿，保存仍requires_publish=true，不能称路径已恢复。原Springer仍订阅预览。保留具体公开全文路径，列入网络修复与机构替代路径，不写没有免费全文。

已处理370，新增核验记录35、实际新增独立PDF35，保留原56，当前核验全文91，仍未取得核验全文335，未处理0。获取成功不改变范围、人工判断或书目。身份/正文不符合文件单列，不计成功；不是科学全文完整阅读。

人工处理三张清单分别为：明确subscription preview证据需本人机构登录17条；403/挑战/正常浏览器路线76条；CONNECT或已证实网络路线受阻246条。可重叠，且只列仍未取得全文的记录；被其他仓储成功解决的记录移出人工下载任务。不是把所有失败归为订阅，也不是三类相加等于待获取数。其他残余原因及本轮来源记录见逐篇370状态表。

更新总JSON/Excel110列/CSV、RIS获取备注、426下载状态、当前未获全文表、Windows队列、README及统一ZIP；保留旧方法和历史获取字段。旧工作表未获370明确为第14轮历史，当前表独立更新。PDF按原ID命名，路径/版本/页数/SHA/来源均在下载清单，PDF及账号/config/原运行日志不进Git。跨任务持久化需平台保存/发布文件快照；取回可通过平台支持导出/本人授权私有存储，或从记录实际URL重取并核对SHA，云端本地路径不是下载链接。

现行[新增全文](../manual_review/scansci_new_verified_fulltexts_utf8.csv)、[机构登录](../manual_review/scansci_action_institution_utf8.csv)、[本人浏览器](../manual_review/scansci_action_browser_utf8.csv)、[平台网络](../manual_review/scansci_action_network_utf8.csv)、[逐篇状态](audit/scansci_sourcewise_record_status_utf8.csv)、[实际请求](audit/scansci_sourcewise_access_events.jsonl)、[汇总](audit/scansci_sourcewise_summary.json)。
