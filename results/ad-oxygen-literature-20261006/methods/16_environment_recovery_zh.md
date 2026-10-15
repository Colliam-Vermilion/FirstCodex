# 新环境恢复与下载门槛（2026-10-15）

最新进展：初次CONNECT403之后，独立复测Crossref和原PDF来源已实际返回200。5份历史正文重新取回并核验，3份明确CC BY4.0正文及R09236官方SI ZIP、解包Excel已放入结果目录。远端持久取回验证待完成；其余来源仍有403/挑战/NTUA503，不能由局部成功推断全部可用。以下初查和首次请求失败作为历史证据保留。

本轮只恢复既有项目和获取工具，不执行主题文献检索、引文扩展或范围重分类。

## 远端基线及成果

从 `Colliam-Vermilion/FirstCodex` 结果分支
`results/ad-oxygen-literature-20261006` 获取实际最新提交
`ec0cba326b45075e9a902a2aa850c78948198813`（2026-10-12）。不使用旧对话数量替代文件。

- 总CSV及JSON均554条；原CSV110列、554唯一ID，509个非空且唯一DOI。
- 实际类别1–6：208/57/111/50/128/0；获取目标426，排除128条跳过。
- 53条人工结果保留（原28条＋pending36的25条K人工值）；pending36另11条J回退同样保留。
- 历史全文核验清单91条、91个不同SHA；既有未获全文335条。
- 主表97个非空SHA不能直接当成成功数，其中6个来自其他历史字段，详见基线审计。
- 初查原件：源提交仓库0 PDF/Word，历史91个文件路径及5个分包均不存在；可见Git历史未补入原件。
- 旧统一ZIP161成员逐字节对应结果表、方法及审计，0篇PDF。`supplement_*`指补检审计，不是论文补充附件。

原110列及全部旧JSON字段原样保留。现行CSV/XLSX追加8个“新环境/当前原件”字段，共118列；旧获取成功、页数、路径和SHA仍作为历史保留，不能当当前持有文件。

新增独立清单：

- `manual_review/historical91_original_recovery_queue_utf8.csv`：历史成功91篇，初始全部“当前原件不可访问，尚未核验”；现已恢复5份，86份仍不可访问。不凭历史成功跳过，也不未经检查整批重下。
- `manual_review/scansci_download_status_utf8.csv`：426条，旧获取字段保留，新增当前状态；91恢复＋335既有未得，互斥覆盖。
- `manual_review/supplementary_material_status_utf8.csv`：426条单独SI状态。PDF、Word、Excel、CSV、ZIP及其他实际附件均在范围内；没有独立附件不等于没有SI。
- `methods/audit/current_original_files_manifest_utf8.csv`：当前实际原件字节清单：3份CCBY正文、1个官方SI ZIP及1个解包派生Excel（派生件不重复计官方附件）。

## 工具恢复和旧修复核实

ScanSci PDF固定PyPI `1.18.0`，完整官方源码/技能固定
`3df79f8211ec2fb542170d132e330fc7bb92ab96`，安装在仓库外
`/workspace/tools/scansci-pdf-runtime`，新建独立venv，没有复制旧环境。
实际stdio MCP初始化成功，18个工具，真实读回 `legal_only`、灰色源关闭及已授权邮箱；
`pip check`和安装脚本重复执行通过。这不表示原生聊天工具已自动注册或联网下载成功。

重新读源码发现旧适配仍需要：1.18.0设置NO_PROXY且Session不自动继承代理，部分来源传入verify=False，
内部来源竞速未因parallel_sources=false全部关闭。启动适配每次从**当前**平台代理及CA变量读取，
强制可信TLS及显式代理；未把旧代理地址写入文件，未关闭TLS，未改上游源码。
离线捕获验证verify=False及空proxies不能绕过该适配，不发送测试网络请求。
不使用通用SDK的内部竞速作为串行批处理调度。灰色源、Tor、机构通道及自动登录均关闭。

MCP单个已知DOI的 `prepare_queue(action=resolve_oa)` 实测返回缺少可选 `scansci-find` CLI，
没有发网络请求；此门面尚不可用。仅为精确DOI/已知来源获取，无需新增主题检索组件。
此结果与实际HTTP CONNECT拒绝分开记录，不以MCP握手当作在线功能通过。

可复现支持文件在 `methods/runtime_support/`。安装命令：

```bash
bash /workspace/FirstCodex/results/ad-oxygen-literature-20261006/methods/runtime_support/install.sh
```

邮箱由环境设置 `SCANSCI_CONTACT_EMAIL` 或仓库外已有配置读取，授权值已在当前机器私有配置中；
支持脚本、结果表和Git不写邮箱值、API key、代理地址、学校会话或cookie。
完整技能目录保留在工具的固定上游checkout，不只复制SKILL.md。
Nature Skills已按用户补充的官方来源 `Yuan1z0825/nature-skills` 核实旧短SHA，
完整提交为 `b543e8b998eb2df1fd44641cc8b262c638c2b442`。
旧版完整三个目录在 `/workspace/tools/nature-skills/skills/`，
`nature-academic-search` / `nature-downloader` / `nature-shared` 分别48/67/21个文件，
没有只复制SKILL.md。当前可取HEAD为 `19be8d45e0d5233aa44be6d4572e655b9914ff54`，本轮沿用旧版，
没有无依据升级。独立运行环境为 `/workspace/tools/nature-runtime`；安装支持在 `runtime_support/nature/`。
不运行会覆盖其他客户端配置的原始安装器，而用外置launcher和私有配置保留新环境设置。
Node24.19支持 `NODE_USE_ENV_PROXY=1`；旧代理适配按当前变量启用，TLS校验不关闭。

Nature下载器的SI能力须单独注意：旧版bare DOI加 `--si` 在正文成功后仍需要CDP浏览器，
直链 `--pdf-url --si` 则没有实际查附件而会写not_found；当前上游HEAD也未修复该点。
因此本轮不会把该字段写为“无SI”，必须从实际出版商/仓储文章页核查并下载所有附件格式。
同题名覆写和宽泛licence误判OA的旧问题，通过按原ID分目录、独立核验来源/身份/版次避免，
不修改书目信息或范围分类；未直接复制旧临时路径或旧虚拟环境。

## 网络迁移及真实下载

新环境只读配置起初为restricted，只有package_managers预设、自定义域名为空。
从旧75域表、91清单实际/候选来源及必要API/附件CDN复用127个域名；
保留新环境预设，不照搬旧草稿169的数量，也不添加已知误提取的机构主页、数据集、
localhost或不明IP。WUR具体全文跳转 `library.wur.nl` 保留。

通过支持接口保存网络草稿，返回 `status=saved`、`requires_publish=true`。
**保存草稿未应用当前运行网络；此接口没有实时应用或发布能力。**
完整可填写清单为 `methods/network_allowed_domains_20261015.txt`，逐域依据见
`methods/audit/environment_recovery_network_domains_utf8.csv`。

用户操作：在当前环境设置的Internet access/网络访问中保留restricted及已有规则，
审阅并保存本次域名与安装/启动配置，然后发布环境；运行实例更新/重连后，再复测受影响请求。
不要更换成旧环境代理地址，不索取学校密码，不认为新API key能解除CONNECT层拦截。
机构订阅需要本人可操作的官方登录/MFA，未完成时单列，不能归因为“没有免费全文”。

初次7项单条/入口验证（Crossref、OpenAlex、Unpaywall、PMC、MDPI、PDF CDN、OSTI）全部
`Tunnel connection failed: 403 Forbidden`，未收到目标服务HTTP响应。

先从历史成功来源选5篇真实下载：

|ID|实际历史/候选来源|本轮结果|
|---|---|---|
|R03564|MDPI PDF CDN|CONNECT403，0文件|
|R01238|AIDIC正式PDF|CONNECT403，0文件|
|R03155|NTUA学位仓储|CONNECT403，0文件|
|R07903|OSTI作者接受稿|CONNECT403，0文件|
|R09236|MDPI正式PDF入口|CONNECT403，0文件|

请求的精确URL及错误在 `methods/audit/environment_recovery_pilot5_20261015.json`。
首次请求没有文件可核验。后续网络变化后重测，R03564/R01238/R07903/R09236及补测R04477共5份正文核验通过，SHA均与历史一致；R03155仍503。R09236经EuropePMC全文XML及supplementaryFiles取得1个官方ZIP（与官方MD5/大小一致），内含Sample key.xlsx五张工作表。其他样本入口状态单列，不写成“无SI”。
同主机已明确CONNECT阻断后不反复请求；没有扩大到335/91的批量。

## 原件保存、用户下载与独立读回

初查无原件；后续已在`/workspace/library-files/ad-oxygen-fulltexts`恢复5份正文。
其中R03564/R04477/R09236三份明确CCBY正文及R09236的原始SI ZIP、派生Excel已放到
`original_files/`准备提交结果分支，持久取回以独立远端读回审计为准。
R01238和R07903仅在当前机器，未完成外部备份；本机目录不是用户下载链接。
统一ZIP此后会包含原件目录；每次以实际ZIP成员和SHA为准，不能把旧统一ZIP当原件备份。
不能把“能从出版商再下载”冒充已备份原文件。

后续必须先取得3–5篇，通过题名、作者、DOI/年份、正文结构及版本核对；
再将原件字节及SI附件保存到用户可取回的持久对象，记录大小/SHA、版本、实际URL和下载方式。
可提交到该结果分支的小样本原件必须明确其可共享版本；其他原件应使用本人授权的私有文件存储。
本轮仅把明确CCBY4.0样本提交授权结果分支，不将未知可见性的GitHub仓库当私有原件库。
只有从持久对象重新取回相同字节、以独立进程/任务核对SHA后，才允许写“持久取回通过”。

`methods/verify_current_original_files.py`供独立取得原件后核验交付清单：空清单时退出2（初查已实际验证），有文件时必须逐个核验SHA及大小；
明确返回 `original_bytes_available=false`，不会将零文件当验证通过。
旧 `retrieve_verified_fulltexts.py`保留，可按历史SHA从原URL重取；它不是备份恢复或云端附件下载。

尚未通过小样本和持久取回门槛，因此本轮批量未启动。网络生效后先恢复此门槛，
再按最新335未得队列和独立91恢复队列分来源继续；正文/SI分开，保留ID和历史SHA。
来源内串行，普通页面至少3秒、已配置ScanSci5–12秒；429按Retry-After冷却，
单个来源拦截不停止其他可用来源。身份或SHA不同须重新核验，不能直接替换历史记录。

本轮独立不变性检查：原CSV110列、全部旧JSON字段、人工附件及分类逐值保持；
CSV118列与XLSX主库逐值一致。历史核验清单不改，首次恢复基线原件数0；后续样本当前正文5份，正式SI附件1个，派生Excel另列。
检查证据为 `methods/audit/environment_recovery_validation_20261015.json`。
