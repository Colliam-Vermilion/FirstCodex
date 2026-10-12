# 第14轮：发布后当前实例实测及5篇全文下载复测

日期2026-10-12，基线提交1ddd0dc53c354716b26315296ef1a5b971663922。等待关联环境starting→ready后，启动新的Python/ScanSci进程，使用当前平台显式代理和可信CA。读取配置时revision=null、base_version_id已换成6acc9ccc386081999282f7bc81eed942的已发布版本，三个Elsevier域名均在显式规则中。这是发布完成的配置证据，实际联网另外测试；无运行实例active-policy-version接口，不能声称所有白名单规则均已生效。

## 实际网络结果

三个Elsevier主机仍分别返回ProxyError及`Tunnel connection failed: 403 Forbidden`：api.elsevier.com、linkinghub.elsevier.com、www.sciencedirect.com。没有目标HTTP响应，所以不是Elsevier账号/订阅拒绝。这不是只读取草稿revision后得出的判断。

5篇R00313/R00363/R00379/R00430/R00651实际ScanSci legal_only下载、Unpaywall OA发现及公开仓储入口检查均完成；本轮逐篇请求都没有CONNECT错误。R00313/R00651的Springer文章页200，IWA两篇403 `Just a moment...`挑战页，scientific.net一篇403 `Your request was blocked.`（缺足够网关归因证据）。网络可达与取得内容严格区分。

R00313：Unpaywall称绿色OA，WUR仓储页面200但未找到PDF入口；不是已验证公开全文。Springer文章HTML明确给PDF入口，实际请求该入口200却回到订阅预览HTML，`This is a preview of subscription content`及`log in via an institution`。R00651同样如此。两篇出版商订阅渠道需要登录的证据明确，单列机构访问清单，但仍可继续寻找公开作者版本。

R00363：Unpaywall称OA但仅给落地页，scientific.net拒绝页挡住访问；R00379/R00430没有Unpaywall OA位置且IWA挑战页挡住访问。三篇不能因此归因为订阅不足，也不能断言没有公开全文。

总计88条观察（含3条独立Elsevier环境探测及2条未发送的冷却观察）：64个200、13个403、3个203、3个429、3个CONNECT ProxyError、2个冷却跳过。200包括元数据、HTML以及部分非论文链接，绝不计为全文成功。额外对两篇Springer明确PDF入口做了请求，结果都是HTML，单独实录。没有PDF文件通过签名/题名/作者/DOI/版本/正文核验，新增全文0，已有56文件保留并核对SHA。

Semantic Scholar本轮R00313/R00430/R00363实际429，均无Retry-After；执行主机至少60秒冷却，R00379/R00651的相应S2请求未发送。无机构认证，无灰色来源，无TLS关闭或独立VPN。文章串行测试；代码审计补充发现1.18.0的download内部仍按来源数建立ThreadPoolExecutor，parallel_sources=false并不能关闭这条竞速路径。因此此前“关闭来源并行”的表述只证明配置设置，不足以证明SDK执行串行来源；本轮不声称每个来源都串行。请求监视器按最终主机执行429冷却。以后扩大前应采用受控的串行来源调用或专用串行HTTP调度，不能仅凭batch_workers=1认为所有来源串行。

## 是否应重启或新建任务

已等待本次环境启动完成，并启动新下载进程；单纯重启ScanSci不会改变云端CONNECT策略。配置已发布但三域仍被实际云代理拒绝，现有工具不能区分运行实例策略传播缺失、规则绑定异常或平台其他出口限制。不能保证重启/新建任务就解除，也不能声称剩余问题都是订阅。

请在环境管理界面确认当前任务选中了刚发布的那个环境版本，核对三域仍在Internet access/Allowed domains规则中。若平台显示当前任务尚未使用新版本，先按界面Reconnect/重连或New task/新建任务选择该版本，再仅测试上述3个主机及原5篇。若界面显示已是新版本、或新任务仍CONNECT403，应联系平台支持并提供本轮去敏错误实录、环境/版本信息及这三个完整主机，请其核对运行egress策略/域名规则；不继续反复改邮箱、添加API key或索取学校密码来解决CONNECT。我们无法直接查看/更换该实例运行策略，发布/重连入口以真实界面为准。

## 下载状态及后续边界

5篇未获核验PDF的状态保留，更新其最新失败步骤，并把第12轮CONNECT原因明确保留为历史，避免读者将历史原因误当本轮现状。总库554条、类别1–6为208/57/111/50/128/0及全部人工判断不改。分类RIS只追加此次获取备注；Excel/CSV与JSON、426下载状态及370未获全文表同步。已核验56文件不重下载，剩余365条本轮未复测；尚无真实公开PDF流程成功证据，因此不启动全队列。R00313/R00651单列本轮明确机构访问清单，其他记录是否需要认证不猜测。

证据入口：manual_review/scansci_postpublication_pilot5_status_utf8.csv，methods/audit/scansci_postpublication_access_events.json，scansci_postpublication_pilot5_results.json，scansci_postpublication_publisher_pdf_checks.json，scansci_postpublication_environment_observation.json。PDF不上传Git，配置/邮箱/API key/cookies及原始运行日志不提交；方法和去敏证据进入原结果目录，更新唯一ZIP。
