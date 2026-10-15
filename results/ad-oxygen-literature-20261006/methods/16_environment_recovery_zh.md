# 新环境恢复与工具核实（2026-10-15）

本文件记恢复基线及工具适配；后续获取和交付以[第17轮](17_current_retrieval_and_delivery_zh.md)及当前汇总为准。

## 实际远端基线

恢复源 `Colliam-Vermilion/FirstCodex` 结果分支 `results/ad-oxygen-literature-20261006` 的完整提交 `ec0cba326b45075e9a902a2aa850c78948198813`（2026-10-12）。源CSV/JSON554条，原CSV110列，554唯一ID、509非空唯一DOI；类别1–6为208/57/111/50/128/0。53条人工结果（28＋25条K）和另11条J回退全部保留。获取仅426条类别1–4，跳过排除128，不运行新检索和重分类。

源历史清单91个ID/不同SHA，原未获335。主表97个非空SHA不能当97篇成功。初查源仓库和可见历史0篇PDF/Word；91旧路径和5个旧分包均不存在。旧统一ZIP161成员只有表格/RIS/方法/审计，不是原件备份。基线证据在 `audit/environment_recovery_baseline_20261015.json`。

保留全部原110列和旧JSON字段、人工附件、RIS及历史91清单；追加12个当前状态字段共122列。旧获取字段为历史，不代表当前持有。历史恢复队列初始“当前原件不可访问，尚未核验”，后按实际字节更新，旧SHA不覆盖。最新当前状态看独立426简表；89篇当前正文不能替代历史91原件计数。

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

## 网络及恢复门槛

新环境最初restricted、package_managers预设保留，自定义域为空。先从旧清单及实际来源恢复127域，再根据实际遇到的来源增加9域及GitHub可见性核查api.github.com，共137。依据表在 `audit/environment_recovery_network_domains_utf8.csv`，完整可填写列表在 `network_allowed_domains_20261015.txt`。工具只能保存草稿，不能实时应用或发布；当前策略版本及后续成功的因果不能从草稿推断。

首次7项API/来源及5篇PDF均CONNECT403。网络观察变化后真实复测，R03564/R01238/R07903/R09236及R04477的正文核验通过、SHA均与历史相同；R03155的NTUA503保持失败。正式版/接受稿分别记录，不把HTML、预览或海报计全文。R09236从EuropePMC取得官方SI ZIP，官方MD5/大小及派生Excel五张表通过。

提交 `e822732c4efbd199e2828e3cf255e3cd27c4511b` 的3篇CC BY正文及SI原件，从新的独立裸Git库通过远端HTTPS取回，按ID/SHA核验同字节；证据 `audit/environment_recovery_remote_original_readback_20261015.json`。门槛通过后才继续335原未获及历史缺件队列；不是在首次失败后盲目批量。最终批次证据及实际持久数量见第17轮。

环境设置步骤：保留现有restricted规则和预设，审阅本次137域、安装/启动说明及仓库提交，保存并发布；实例更新后只复测受影响来源。API key、代理、CA和机构会话按新实例实际绑定核查。学校登录/MFA由本人官方界面完成，不索取密码。邮箱值仅在仓库外私有配置及环境变量要求中，Git不保存值。
