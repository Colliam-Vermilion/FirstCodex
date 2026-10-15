# Windows：下载、全部关联附件、解析及按ID回填

从GitHub克隆/更新**原结果分支**，从`results/ad-oxygen-literature-20261006`目录运行。数据根建议`D:\AD-Library`，不放进Git工作区。现有original_files保持原位置；metadata映射读取，不重复复制。Python核心流程已在Linux真实执行并测试；PowerShell包装脚本经过静态检查，当前环境无Windows/PowerShell，不能声称已在Windows执行。

## 1. 安装与当前队列

```powershell
.\windows\Start-Library.ps1 -Action Setup -LibraryRoot D:\AD-Library
$P = 'D:\AD-Library\.venv\Scripts\python.exe'
```

需要Python3.11+及py启动器；按固定requirements安装PyMuPDF/openpyxl/python-docx/Pillow。OCR另需本机Tesseract可执行程序和eng语言在PATH；缺失会留下ocr_needed记录，不当完成OCR。不要复制云端代理、CA、会话或旧虚拟环境。

- `main_records337_utf8.csv`：337个缺正文PDF ID（328原未获＋9历史当前无PDF），包含题名/DOI/来源及旧SHA。
- `known_pdf_urls_utf8.csv`：29个既有PDF候选URL，覆盖27个ID；不是全部337篇的可自动下载直链。候选未证明身份，不冒充绑定下载成功。
- `doi_queue317_utf8.csv`及`scansci_mcp_requests317.jsonl`：317个有DOI的缺PDF记录，明确`download_si:true`；其余20个无DOI在`no_doi_manual20_utf8.csv`，不猜DOI。
- `supplementary_review426_utf8.csv`：426个纳入ID均需按独立SI状态核查，包含已有正文，检查出版商及相关仓储，不因已有12附件跳过其他ID。

以上带数量的文件保留本轮快照；默认脚本读取`*_current_utf8.csv`及`scansci_mcp_requests_current.jsonl`，每次merge后自动按最新metadata刷新，避免旧337队列覆盖回填进度。

R03477/R09804/R11844/R05213已有XML文字但尚无PDF，仍在337内。337是缺PDF格式清单，不是断言337篇都没有正文文字；本机还原并实际核验XML及相关媒体后，若已满足研究需要，应先复用而非强制补PDF。未还原到本机时也不能凭清单假设XML文件可读。旧91成功不能使缺原件记录被跳过。先取得私有包并还原时，已有54 Git对象与81私有对象按SHA复用；本机没有的文件不能仅凭清单标已有。

## 2. 已知公开来源下载，支持恢复

```powershell
.\windows\Start-Library.ps1 -Action Download -LibraryRoot D:\AD-Library
```

实际文件先入`intake/<ID>/main`，保留`.part`和ETag/Last-Modified。只有带一致验证器的HTTP Range才拼接，服务器忽略Range则重新接收完整对象，核对Content-Length/Content-Range和SHA。每来源间隔至少6秒，429暂停并保存Retry-After，401/403暂停该主机；其他来源继续。重复运行跳过同SHA完整候选和已登记原件。失败默认不重试；**仅在网络/来源确有变化后**使用`-RetryFailed`。主文件有待审候选时先审核，不为同ID盲目下其他版本。

工具会拒绝HTML/登录/挑战、无效PDF及坏ZIP/OOXML；`downloaded_pending_review`不是全文核验通过。若候选身份错误，保留证据后：

```powershell
& $P .\methods\corpus\download_local.py --root D:\AD-Library reject --id $ID --file $File --evidence '实际不符的题名、作者、DOI或期刊目录等依据'
```

其余来源用本人官方浏览器、学校授权网络/登录/MFA下载，保存实际文件，随后登记。不索取密码，也不将登录页另存为附件。

## 3. 可选ScanSci 1.18.0，明确SI开关

安装及本人机构登录可复用`methods/13_scansci_diagnosis_windows_zh.md`中Windows步骤；只沿用版本和说明，不沿用云端临时路径/代理。ScanSci独立venv与配置放仓库外；联系邮箱、安全来源和本机认证自行配置，灰色来源保持关闭。不是必须安装此可选组件才能手工下载/回填。

对已安装的stdio MCP，先运行探针（不下载论文）：

```powershell
& $P -m pip install -r .\methods\corpus\requirements-mcp.txt
& $P .\methods\corpus\run_scansci_mcp.py --root D:\AD-Library --command D:\AD-ScanSci\Scripts\scansci-pdf.exe --server-arg run --probe-only
```

实际需要该exe指向本机安装位置。工具验证legal_only及灰色源关闭；云端同版实际stdio探针已通过18工具并确认download_si参数。去掉`--probe-only`，加`--limit 5`即串行处理5个未完成DOI，重复运行继续；每条显式`download_si:true`、`strategy:legal_only`。结果仍是候选，需人工核对身份/版本/附件。该SDK内部仍可能多来源竞速，**不能声称来源内严格串行**；需要严格来源限流时用上一节直链下载器和本人浏览器。

## 4. 核对正文版本，登记实际文件

先核对题名、作者、DOI/年份、完整正文/参考文献和版本声明。版本代码：publisher_version、accepted_manuscript、preprint、author_manuscript_unconfirmed、thesis、other_complete_body。公开仓储不自动代表出版版。

```powershell
$ID = Read-Host '原文献ID，例如R00313'
$File = Read-Host '已经核验的正文PDF完整路径'
$Version = Read-Host '版本代码'
$URL = Read-Host '实际出版商或仓储永久URL'
$Evidence = Read-Host '题名作者DOI/年份、完整正文、版本的页码及依据'
& $P .\methods\corpus\download_local.py --root D:\AD-Library register --id $ID --role main --file $File --version $Version --url $URL --reviewed --evidence $Evidence
```

原文件名保存为元数据，canonical文件名加SHA前缀防覆盖。未明确审核不接受；排除ID拒绝登记。新版本保留旧版和SHA，云端合并不会自动提升为首选或抹去旧记录。

## 5. 独立核查及获取全部关联附件

打开出版商和相关仓储页面，检查Supporting Information/Supplementary、附件区及数据/代码可用性声明。也可先提取页面候选：

```powershell
$Page = Read-Host '已核对归属的出版商或仓储文章页URL'
& $P .\methods\corpus\download_local.py --root D:\AD-Library discover-si --id $ID --url $Page
```

生成`supplementary_candidates_utf8.csv`，逐项核对是该论文附件，确认后将真实附件行的association_verified改true；外部大型数据行保留external_data=true。候选页标题/链接不是自动身份认证。JavaScript页面/登录失败或无检测链接仍不是明确无SI。把已审附件CSV作为`Start-Library.ps1 -Action Download -Queue <该CSV>`输入，或本人浏览器下载全部PDF/Word/Excel/CSV/TXT/图片/视频/代码/压缩包，保留原格式。

```powershell
$File = Read-Host '已核验实际附件的完整路径'
$URL = Read-Host '实际附件永久URL'
$Evidence = Read-Host '归属文章、附件标识、数量、格式及打开核验依据'
& $P .\methods\corpus\download_local.py --root D:\AD-Library register --id $ID --role supplementary --file $File --url $URL --reviewed --association-reviewed --evidence $Evidence
```

官方ZIP保留原包，并安全提取其成员为derived，保留CRC/SHA和父包关系，不执行代码。**PMC supplementaryFiles传输包不是官方SI**；按`--role transport_archive`登记来源包，原作者声明的附件另逐个登记。完整JATS可按`--role evidence_xml`登记；必须确认article/body和身份，不能算历史PDF恢复。旧Office/视频/模型等无法自动内容解析时人工打开核验，原件保留、状态注明未索引。

全篇确无SI只有在出版商和仓储均有明确检查证据、且不存在已获官方附件时，才可登记：

```powershell
& $P .\methods\corpus\download_local.py --root D:\AD-Library si-status --id $ID --status explicit_none --publisher-checked --repository-checked --evidence '具体页面/日期/未提供附件的依据'
```

其他状态支持not_checked、downloaded_partial、access_failed、external_data_link。大型测序/外部数据库仅记录登录号、URL、类型和已知大小；不自动下整个库。

## 6. 提取与检索

```powershell
.\windows\Start-Library.ps1 -Action ExtractNew -LibraryRoot D:\AD-Library -Ocr
.\windows\Start-Library.ps1 -Action Search -LibraryRoot D:\AD-Library -Query 'methane AND oxygen'
& $P .\methods\corpus\extract_search.py search --root D:\AD-Library --query '微曝气' --contains
```

新登记文件用intake/assets.json；已有混合库在私有包Hydrate及Git原件可读后可运行ExtractExisting。没有私有原件会报告missing，不能声称全库可检索。输出chunks/pages/cells/workbook/tables及SQLite，保留ID、源SHA、页/章节/工作表/单元格位置。OCR/自动表格未人工校对；图片、视频、模型只保留说明，不虚报内容检索。

## 7. 批量回传与ID/SHA合并

```powershell
.\windows\Start-Library.ps1 -Action ExportReturn -LibraryRoot D:\AD-Library -Package D:\AD-Library\return_20261015_01.zip
```

包只含已明确核验的原件、其解析结果和SI检查记录，不含浏览器profile、cookie或工具配置。每成员SHA/大小及包SHA先校验；已有不同内容的同名包拒绝覆盖，请使用新批次名。需要小批量可直接运行：

```powershell
& $P .\methods\corpus\transfer_library.py prepare-return --root D:\AD-Library --out D:\AD-Library\return_02.zip --ids R00313,R00363
# 收到Codex成功合并回执后，排除已接受的asset ID，避免重复上传：
& $P .\methods\corpus\transfer_library.py prepare-return --root D:\AD-Library --out D:\AD-Library\return_next.zip --exclude-ack D:\AD-Library\last_return_merge.json
```

先选定私有云位置，按第19轮方案配置rclone；不提交原件包、凭据、会话到可能公开的GitHub：

```powershell
.\windows\Sync-Private.ps1 -Direction Upload -Remote 'adprivate:AD-Oxygen/incoming/20261015-01' -Package D:\AD-Library\return_20261015_01.zip -Python $P
```

脚本实际上传后重新下载到空临时目录，再核对包及每成员SHA。使用immutable对象；相同已完成包可复用，变化请用新批次目录。单对象的字节续传依赖后端，不作所有后端保证；已完成批次通过SHA跳过，不因一包失败重传全部。

Codex获得同一私有目录的独立授权后，先实际下载并用可信包SHA校验、Hydrate到新目录，再运行`transfer_library.py --project <项目> merge-return --root <还原目录>`，更新inventory与papers，运行`render_inventory.py`生成最新汇总表。按ID及SHA匹配，不按行序；先校验整批、重复跳过、同文不同SHA并存，排除ID/损坏文件拒绝。原人工分类及历史91 SHA不改。回传的解析片段可复制到全库解析根后运行`extract_search.py index --root <全库解析根>`重建索引。回填前后必须运行`verify_inventory.py`核对实际文件，旧轮次Excel保持为历史快照。

本轮未连接外部私有存储，也未在真实Windows执行；已测试跨平台Python的恢复、错误页拒绝、429、ZIP/表格及回传去重行为，并在独立进程做全量包还原。实际上传和新的Codex实例读取需要连接后完成，不能由上述脚本的存在推定已完成。
