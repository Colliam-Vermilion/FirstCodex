# 第17轮：原件恢复、现行获取与交付（2026-10-15）

## 数据和队列

从远端源提交ec0cba326b45075e9a902a2aa850c78948198813恢复，总库554、原110列逐值保留，类别208/57/111/50/128/0，53人工值及J回退不改。新增12个当前状态字段，CSV/XLSX122列。`current_environment_acquisition426_utf8.csv`是当前426篇获取简表；旧字段/第1–15轮文档是历史证据。旧JSON字段不覆盖，只替换本轮独立节点。

|互斥当前正文分组|篇数|处理|
|---|---:|---|
|历史原件SHA完全相同|80|可按原ID/SHA复用实际字节|
|历史ID、已核验不同字节版本|2|R10086期刊正式版、R13955博士论文；保留旧SHA另记当前SHA|
|原335未获中的新增全文|7|身份、正文、版本人工核验后接收|
|历史91中当前仍无正文|9|继续独立恢复队列|
|原335中仍未获正文|328|保留来源及失败/未尝试原因|
|当前纳入记录合计|426|89有当前全文、337无当前全文|

历史91字节尚缺11份＝9个无正文ID＋2个另版ID。历史“曾成功”不可用来跳过当前缺件；将来旧环境恢复可按ID/SHA合并。历史91清单的SHA、成功标记和旧路径均原样保留。历史累计曾获取98个ID也不能当当前持有98份。

新增7篇：R04510和R02719为接受稿；R02282为仓储Postprint/作者R1稿，接受阶段未独立证明；R13889为仓储作者稿；R13905明确pre-print；R13932为HAL接受稿/Postprint；R13956为BanglaJOL正式版，题名、4作者、年和卷期页核对，PDF未打印原库DOI，不能由此宣称DOI独立验证。均保留原ID、题名、DOI和类别；不能将作者稿写成出版社正式版。

## 已执行的获取和验证

先小样本真实下载和SI核查，再独立远端原字节读回，门槛通过后批量。对原335的每篇检查已有来源计划，162篇有本轮实际请求；其余是无明确绑定URL、同来源已阻断等显式未尝试，不能称335篇均已重新联网。历史缺件在已恢复样本及SHA复用检查后只处理86条，R03155保留503证据不无变化重试。

使用 `continue_known_fulltexts.py`：每条原ID原子状态、SHA复用、同主机锁、至少3秒间隔、最多2篇跨来源工作；429按Retry-After且至少60秒冷却。CONNECT/挑战仅暂停对应来源。续跑读取已完成状态；仅在配置/来源有实际变化后用 `--retry-failed`。所有新字节即使包含题名/DOI也只是候选，须核对正文头部/作者/来源和版次，不能把引用目标论文的综述计成目标全文。已纠正候选同名覆盖，文件名附SHA；实际目录/期刊索引页已排除，无法读回的被覆盖候选不算核验。

审计：`audit/current335_source_pass_20261015.json`、`current_historical_source_results_20261015.json`、`current_source_pass_outcomes_utf8.csv`和访问事件JSONL；人工核验及离线反例回归单列。分类、范围和文献池不作修改。无需新检索即可继续已知DOI和明确全文位置获取。

## 补充材料

既有19条PMCID中17条全文XML身份匹配，10个ID共12个官方附件：PDF3、DOCX4、XLSX2、ZIP3，约18.1MB。ZIP内解包6个派生文件＝5个Excel和1个34.8MB SketchUp模型；不是额外6个官方附件。支持CSV及其他真实格式，但本轮没有取得CSV附件，不虚报。

逐个核对原论文XML引用、附件ID、实际文件格式/大小、SHA及XML提供的MD5；PDF逐页解析，Word/Excel/ZIP检查内部结构及CRC。原件/派生件分别记录。程序 `retrieve_existing_pmc_supplements.py`只处理现有已纳入ID/PMCID，授权联系邮箱从仓库外环境读入。

R10894/PMC11499478及R04119/PMC6197294的EBI XML500，不无变化重试；R05542空SI节仍待出版商核查。其余XML未列本地资产不等于全球无SI。89份正文另作自己的SI入口扫描，排除引文中他文SI；R03455、R13819、R13957已有内嵌附录，正文原件本身保留。R06611主要为图像，快速文本扫描不能确认无SI。R13833明确ACS Word附件URL返回403挑战页，主机暂停；其他来源继续。Nature的not_found未必执行附件检查，不作为无SI证据。

## 原文件的持久保存和取回

结果分支 `original_files/` 保存40篇自身明确CC BY/CC0正文、9个许可允许的官方SI及5个派生Excel，共54个字节对象。来源、作者、DOI、许可、原SHA和当前SHA在 `original_files/ATTRIBUTION_utf8.csv` 和 `audit/current_original_files_manifest_utf8.csv`。许可未明确或禁止再分发的49篇正文、3个官方SI及1个模型派生件仅在当前机器，未上传未知可见性的GitHub；需要用户指定的私有持久存储。仓库可见性API被拒，未假定该库为私有。

用户在GitHub结果分支 `original_files/` 打开文件选择Download raw file，或该分支Code → Download ZIP。独立克隆/解压结果分支后，从项目目录运行：

```bash
python methods/verify_current_original_files.py
```

该验证逐文件核对SHA/字节数，空清单失败。独立远端裸Git取回实际对象的证据在 `audit/current_remote_original_readback_20261015.json`；验证不读取原下载目录，也不以manifest代替原件。全新云任务的冷启动尚未实际测试，独立空Git库取回已实际执行。快照发布、原URL可再下载、本机路径或草稿保存都不是原件备份。

`ad_oxygen_literature_final.zip`是元数据交付包：包括全部表格/RIS/方法/审计和原件说明/许可清单，**不包括PDF/Word/Excel/ZIP等原件二进制**，避免统一ZIP重复占用及超过单文件限制。GitHub整个分支Download ZIP则包含已提交原件。这两个入口不同，按实际manifest校验。

## 剩余配置和下一步

Nature b543e8b998eb2df1fd44641cc8b262c638c2b442完整三技能和ScanSci PDF1.18.0（上游3df79f8211ec2fb542170d132e330fc7bb92ab96）已装，stdio MCP分别16/18工具；实际已知DOI元数据请求、相关既有测试、pip check及重复安装通过。恢复适配只读取当前代理/CA并强制TLS，不复制旧虚拟环境/地址。Nature SI需CDP的路由尚缺浏览器；ScanSci prepare_queue(resolve_oa)尚缺可选scansci-find，其失败与HTTP故障分开；既有来源获取不依赖它。

137域保留新环境原package_managers预设；安装/启动、邮箱变量要求和实际仓库提交保存在配置草稿，requires_publish=true。接口不支持实时应用/发布。用户需在环境设置审阅、保存并发布；之后复测特定来源。检索API/出版商/仓储已有实际成功，但Elsevier等CONNECT403、ACS挑战403、NTUA503和EBI500仍有明确证据，不能宣称全部畅通。

R00313 WUR具体eDepot路径返回200 HTML，明确仅WUR师生可访问；Unpaywall对该DOI虽标repositoryOA却无PDF URL，不能覆盖实际机构限制，也不假定HKUST能完成WUR认证。不索取密码。下一轮只从当前337缺正文、91历史缺字节和独立SI状态继续；已核验和持久字节先按SHA复用。私有原件的存储目标未给定，不能将剩余本机副本称为跨任务已保留。
