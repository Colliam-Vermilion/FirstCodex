# 第13轮：ScanSci PDF 1.18.0访问障碍诊断与Windows机构工作流

日期：2026-10-12。基线提交：8c07a88c5208adacaec983e7f5ab270b551272bf。只做小批诊断，不重跑370条。总库554条，类别1–6仍为208/57/111/50/128/0；人工判断、摘要/正文筛选证据、书目和获取状态均不改。426个类别1–4下载目标中已有56份核验全文（13复用、43新下载），剩余369失败+R05473单页研究海报=370。PDF仍只在运行环境，无新下载或新上传。

## 1. 采用的官方说明及实际代码

读取官方仓库README、skills/scansci-pdf/SKILL.md、skill/SKILL.md及已安装1.18.0的network.py、config.py、sources/unpaywall.py、sources/core_api.py、pipeline.py、server.py、main.py。官方快照3df79f8211ec2fb542170d132e330fc7bb92ab96；版本固定1.18.0。README：[官方来源](https://github.com/Rimagination/scansci-pdf/blob/3df79f8211ec2fb542170d132e330fc7bb92ab96/README.md)。不是根据另一环境/workspace/tools假定安装。

## 2. 非互斥障碍统计及证据边界

分母370条尚无核验全文；统计来自5720条去重历史访问证据及逐条source_failures。每一条可有多种障碍，不能相加当总数，亦不能当作本轮当前状态。

|观察|涉及记录数|解释|
|---|---:|---|
|代理CONNECT拒绝|359|ProxyError + `Tunnel connection failed: 403 Forbidden`，目标没有HTTP响应|
|实际HTTP403|117|下列签名进一步区分，不能全部归因目标服务|
|实际HTTP429|73|82条去重响应证据覆盖全部426目标；这里为370分母的73个ID|
|Unpaywall配置缺失|347|实际source_failures明确要求真实email；本轮已修复|
|其他连接/HTTP错误|97|含早期DNS解析失败及404/406/5xx，不等于现在仍DNS失败|
|浏览器工具不可用|347|SDK返回browser_unavailable；该提示还含不适用的灰色来源建议，本轮未采用|
|观察到429后冷却未发送|346|不是346条HTTP429，更不是出版商均拒绝|
|机构通道未认证|370|整个可选通道未建立，不能证明370篇都需要订阅；逐篇是否需订阅仍未知|

403正文进一步有65个ID遇到`Just a moment...`目标/CDN挑战页、58个遇到`Domain forbidden`网关拒绝正文、16个响应信息不足。三组也可重叠。`Domain forbidden`不等同出版商拒绝；历史记录缺服务器头，无法确定是云代理还是上游网关。详见[403签名审计](audit/scansci_http403_signature_audit.json)、[逐篇矩阵](audit/scansci_obstacle_matrix_utf8.csv)、[原始去敏证据](audit/scansci_access_evidence_utf8.csv)。早期NameResolutionError已在上一轮显式Session代理修正后补测，仍保留为历史证据。

重定向域名按异常`ConnectionPool(host=...)`核对：请求起点doi.org并不意味着被拦截的是doi.org。例R00795的真实拒绝目标是linkinghub.elsevier.com。已纠正域名审计；历史77个域名中排除本轮暂跳过的Scopus/CNKI，保留75个合法来源域名，不能声称75个当前都被拦截。

## 3. 本轮实际修复和小批测试

用户授权邮箱已写到仓库外`/workspace/scansci-pdf-runtime/data/config.json`的`email`，文件权限0600。ScanSci的load_config和重启后的实际stdio MCP `scansci_pdf_config(key="email")`均读到授权值；审计仅保存相等性，不公开邮箱/config。草稿新增/保留`SCANSCI_CONTACT_EMAIL`绑定，启动bootstrap写入email。PubMed绑定和Nature配置保留。

Unpaywall检验R03564已下载OA控制以及5条历史失败R00313/R00363/R00379/R00430/R00651：全部200且返回真实论文DOI、完整题名；具体同一性检验见[Unpaywall身份核验](audit/scansci_unpaywall_identity_validation.json)。例如R03564 DOI `10.3390/en10020258`，返回题名“The Influence of Micro-Oxygen Addition on Desulfurization Performance and Microbial Communities during Waste-Activated Sludge Digestion in a Rusty Scrap Iron-Loaded Anaerobic Digester”，OA出版版本位置指向MDPI。复用其已有19页核验PDF，不重复下载。此结果只证明Unpaywall真实元数据/OA发现可用，绝非所有候选已取得PDF。

5篇入口复测：R00313 WUR仓储200 HTML；R00363 scientific.net 403 `Your request was blocked.`，仅此短正文不能判断拒绝层；R00379和R00430 IWA403 `Just a moment...`；R00651 Springer200 HTML。没有任何一条仅凭HTML200升级为全文成功。来源测试：OpenAIRE200并返回total=1的论文XML，CORE实际SDK端点200，Semantic Scholar200；Elsevier API、linkinghub.elsevier.com、www.sciencedirect.com仍CONNECT403。Wiley API400说明CONNECT通过但请求参数/接口条件未满足，不能当API权限已通过。uvadoc.uva.es503正文为`upstream connect error or disconnect/reset before headers. reset reason: connection timeout`，属于网关上游连接超时；digital.csic.es虽然200，但正文是`Making sure you’re not a bot!`挑战页，并非仓储内容。

诊断过程中一次CORE手写路径`/v3/works/search`返回404 `No route found`，是测试路径错误，已按安装代码修正为`/v3/search/works`并返回200；不是网络拦截，亦不是ScanSci原代码错误。两次实录都保留。

## 4. 代理、CA和429

1.18.0的__init__.py将NO_PROXY/no_proxy设为*，network._get_session设置trust_env=False；实际选择为SCANSCI_PDF_PROXY优先，其次network_proxy，不使用普通HTTPS_PROXY。当前launch.py导入bootstrap，显式从平台HTTPS_PROXY衔接SCANSCI_PDF_PROXY和Session.proxies；匹配检查为true，但不公开代理地址。通用requests.Session也接入同一显式代理，解决部分来源独立创建Session的漏接。CA从REQUESTS_CA_BUNDLE/SSL_CERT_FILE读取；TLS验证开启，对第三方verify=False强制回到可信CA或True。不安装独立VPN、不绕行代理、不关闭证书校验。

实际代码发现：polite_delay默认因`fixed_request_delay_enabled=false`直接返回，仅调整5–12秒无效。本轮启用true；batch_workers=1、institutional_workers=1、parallel_sources=false、parallel_probes=false、request_delay_min=5/max=12。配置已写当前实例及可复现安装/启动草稿。

本轮源/入口请求串行，间隔至少5秒；同一主机429有Retry-After则解析秒数或HTTP日期，等待不短于指示时间，无此头则至少60秒并暂停该主机。长等待不阻塞其他来源，保存恢复时间，不立刻重试。同一请求最终重定向主机负责冷却，不能把Springer限流错误地传播到doi.org全部来源（上一轮已纠正并补测254条）。本轮429来源复测返回200，但单次通过不证明已消除共享出口限流，不能恢复高并发。

## 5. 白名单草稿与需要用户操作

读取草稿revision15，基线active-version标识未提供后续运行版本观测；此次保存仍返回requires_publish=true。工具无法读取设置界面或当前实例实际策略版本，不能确认整份草稿已发布/传播。OpenAIRE/CORE等现在可响应，说明这些路径当前可达；Elsevier三域仍实测CONNECT拒绝，说明所需路径没有全部生效。

请在当前项目关联的Codex云环境设置寻找 **Internet access / 网络访问（联网）**、**Allowed domains / 允许域名**、**Environment variables / 环境变量**、以及 **Save/保存、Publish/发布环境**。具体按钮文案无法从本环境查看；不要只保存草稿。开启联网，保持restricted并添加官方主机/重定向目标，保留既有Nature/PubMed规则。优先检查 **api.elsevier.com、linkinghub.elsevier.com、www.sciencedirect.com**。完整域名和“历史/本轮”状态见[必要域名表](audit/scansci_required_domains_utf8.csv)。Unpaywall需api.unpaywall.org；发现源需api.openalex.org、api.openaire.eu、api.core.ac.uk、api.semanticscholar.org；解析需doi.org；PDF可能在独立出版商CDN/仓储，需按实际重定向补充，不只开放API域名。

本轮将实际CONNECT目标中原草稿遗漏的16个合法域名追加，保留153条既有规则，成为169条显式主机规则。联系人绑定、低速安装/start配置均已保存，仍需用户发布并在相关任务/重连实例复测。若公开PDF正文也被云代理拒绝，不能以增加校园登录解决；反之目标CDN挑战页不能保证靠白名单解决。HKUST机构域名和身份提供方本轮没有进行认证网络访问，因此不伪造尚未观察的MFA跳转域名。

## 6. 在Windows安装同版本并由本人登录HKUST

在本人Windows电脑安装Python3.11及以上（建议3.12）与最新Chrome/Edge。下载原结果分支到本地，以下PowerShell从结果目录执行。不要复制云端代理URL、CA或浏览器cookie到Windows；本地不继承云端配置。网络出口是本机当前网络/VPN，仍需实际验证订阅。

```powershell
py -3.12 -m venv .scansci-venv
$python = Join-Path $PWD '.scansci-venv\Scripts\python.exe'
$scansci = Join-Path $PWD '.scansci-venv\Scripts\scansci-pdf.exe'
& $python -m pip install 'scansci-pdf[patchright,instsci]==1.18.0'
& $python -m patchright install chromium
& $python -c "import importlib.metadata; print(importlib.metadata.version('scansci-pdf'))"
# 配置在仓库外，账户会话也在本机，不上传Git
$env:SCANSCI_PDF_DATA_DIR = Join-Path $env:LOCALAPPDATA 'ScanSciPDF-AD'
New-Item -ItemType Directory -Force $env:SCANSCI_PDF_DATA_DIR | Out-Null
& $scansci config-cmd download_strategy legal_only
& $scansci config-cmd scihub_enabled false
& $scansci config-cmd use_tor_for_scihub false
& $scansci config-cmd batch_workers 1
& $scansci config-cmd institutional_workers 1
& $scansci config-cmd parallel_sources false
& $scansci config-cmd parallel_probes false
& $scansci config-cmd fixed_request_delay_enabled true
& $scansci config-cmd request_delay_min 5
& $scansci config-cmd request_delay_max 12
& $scansci config-cmd browser_headless false
& $scansci config-cmd browser_backend patchright
& $scansci config-cmd ezproxy_enabled true
& $scansci config-cmd ezproxy_login_url 'https://{host_dashed}.lib.ezproxy.hkust.edu.hk'
# 输入本人此前授权的联系邮箱；不要将含个人值的配置提交
$contact = Read-Host 'Unpaywall contact email'
& $scansci config-cmd email $contact
Remove-Variable contact
& $scansci browser-doctor
& $scansci login --login-type ezproxy
```

浏览器弹出后，仅在HKUST官方登录/身份认证页面由本人输入密码并完成MFA；不向Codex提供密码，不导出cookies提交仓库。若没有出现可见窗口或停在登录页，认证未完成。README采用域名重写：onlinelibrary.wiley.com → onlinelibrary-wiley-com.lib.ezproxy.hkust.edu.hk，保留原文章路径和query；不使用通用login?url=前缀。云端仅设置正确模板并保持ezproxy_enabled=false，因为没有本人可操作的登录浏览器；无DISPLAY/无浏览器交互工具，安装Chromium不代表交互能力或认证成功。

如使用本地MCP，配置新的mcp_servers.scansci-pdf.command指向本地scansci-pdf.exe、args=['run']，环境SCANSCI_PDF_DATA_DIR指向上述LOCALAPPDATA目录；与Nature现有服务器并存，不替换。调用scansci_pdf_channel_status(kind='ezproxy')确认代理自身会话cookie有效，随后从图书馆代理访问一篇确有订阅的文章并核验PDF。配置完成/跳回出版商原站不是认证成功。官方资源起点：[HKUST Library](https://library.hkust.edu.hk/) → Library Search/Databases/E-journals → 正式资源链接；具体MFA域名以该官方跳转为准。

## 7. 导入队列、避重复及回同步

本轮导出完整370记录ID队列，其中347条有DOI（347个唯一规范化DOI）、23条无DOI。已取得56全文全部排除出队列；不论PDF是否拷到Windows，均不再请求这56条。无DOI按题名、作者、年份和官方入口手工找；R05473仍明确为海报，找不到论文不能将海报当完整论文。

Windows先运行5篇，不直接批量370：

```powershell
$papers = Join-Path $env:USERPROFILE 'Documents\AD-Oxygen-PDF'
New-Item -ItemType Directory -Force $papers | Out-Null
& $scansci batch '.\manual_review\windows_pilot5_queue_utf8.csv' --output $papers --no-lanes
# 仅当5篇实际PDF核验与机构权限测试通过，再扩大；遇429按Retry-After停相应主机
# & $scansci batch '.\manual_review\windows_doi_download_queue_utf8.csv' --output $papers --no-lanes
```

使用--no-lanes避免并行预探测；legal_only+scihub_enabled=false保持合法来源。SDK表格解析器识别doi/title/channel，但内部QueueEntry不保留record_id，因此另存[完整ID映射表](../manual_review/windows_remaining_fulltext_queue_utf8.csv)，不能按输出顺序回填；若DOI重复，多原ID映射同一有效文件并保存匹配日志。无DOI队列不送入需要DOI的自动batch，单独处理。现有56PDF若要取回，沿用[核验清单](audit/scansci_verified_pdf_manifest_utf8.csv)及retrieve_verified_fulltexts.py从原合法来源重取（--verify-only可核对已复制文件）；云端分包路径不是下载链接。可通过平台受支持文件导出或本人批准的私有存储迁移，未自动上传。

每份文件核查PDF签名、全部页面可解析、论文正文/Methods/References、首页完整题名/作者、DOI及出版/接受稿/预印本版本；摘要页、错误页、登录页、海报不计全文。用`记录ID_年份_简短题名.pdf`命名，别按行号分配ID。文件SHA在PowerShell：`Get-FileHash -Algorithm SHA256 <PDF>`。填[本地状态模板](../manual_review/windows_local_status_template_utf8.csv)：保留原ID、来源URL、版本、页数、路径、SHA和身份/正文核验依据。路径只是Windows本地路径，不是共享下载链接。上传填好的CSV即可请求按ID同步获取状态；如要复核正文可提供对应PDF/授权存储，不能只凭成功提示升级全文。

回填规则：验证ID唯一且主库存在，规范化DOI匹配，已有56SHA不重下载；仅更新全文获取状态及来源/文件核验，追加旧状态历史。原category/final_category_code、manual53、人工作证据、题名/DOI书目一律冻结。PDF不进Git；本地session/cookies/config/API key不进Git。根据实际Windows权限和全文证据再回写，不将本文未执行的Windows命令声称已验证。

## 8. Elsevier API需要分别验证什么

1. 在[Elsevier Developer Portal](https://dev.elsevier.com/)本人机构邮箱账户创建ScienceDirect Article Retrieval API key。保存在本机仓库外配置elsevier_api_key或MCP配置工具；不发到聊天/不提交Git。key是API身份，不是全文权限。
2. 本机校园网络/学校VPN若提供真正校园出口，可用于API机构IP识别；普通HTTPS网页EZProxy会话不能自动给api.elsevier.com校园IP。SCANSCI_PDF_PROXY/network_proxy优先级要核对；若用明确机构授权代理，确认TLS、其出站IP及Elsevier识别机构，不能把云平台普通代理当校园代理。is_campus_network=true只是设置，不能授予权限。
3. `& $scansci elsevier-check --doi '10.1016/j.wasman.2022.09.035'`并检验可用的订阅文章。若CONNECT403，尚未到Elsevier；先网络放行。若401/key错误，先key。若NOT_ENTITLED，核对真实出口和学校订阅/API权限。若403 `Requestor configuration settings insufficient`，key+出口全文设置不足，向机构Elsevier管理员确认API全文/TDM许可；已在校园出口仍可能不获API全文授权。insttoken是无法取得机构出口时由机构管理员提供的替代路径，不假定必需或已存在。
4. 200也需核对响应全文内容、题名DOI，不能把摘要JSON或元数据当正文/PDF。本轮没有Elsevier key，且API CONNECT被拒绝，未测试机构权限。用户Windows在校园网，不意味着云端程序有校园出口；两端必须独立测。

## 9. 交付与恢复条件

本轮不改变现行Excel/CSV/RIS内容，因无新的核验全文，避免将可达HTML或Unpaywall结果伪写成获取成功。增加诊断/访问证据/Windows队列，更新README和统一ZIP。发布白名单或本机机构登录后，先复测5篇并取得至少真实全文及身份核验，再讨论扩大；不能仅凭MCP握手、配置或HTTP200恢复370条批处理。读取原53条人工标记以及主库554完整ID集合并核验文件SHA不变。
