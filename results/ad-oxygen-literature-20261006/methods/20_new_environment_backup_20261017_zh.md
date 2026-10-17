# 2026-10-17 新环境恢复与全部原件私有备份

## 恢复依据与保留边界

从远端结果分支 `results/ad-oxygen-literature-20261006` 的
`bac51bfccceae13a91745322ed5793260e30a85c` 恢复，实际按ID、大小、SHA256
复核了40份正文、9份官方附件和5份既有派生Excel。旧89/91不能当新环境持有数。
554条原记录、类别1–4的426条下载范围、128条排除以及全部人工判断不变，
没有关键词检索或重新分类。原110列、人工附件及旧方法均保留；当前获取字段单独更新。

`inventory/recovery_20261017/baseline*.json` 保留恢复前的清单与完整字段。
历史91原SHA清单另外并入逐对象恢复队列；已取得替代版本不代表旧字节恢复。
缺少原件明确标记“历史已获取，当前原件未恢复”。旧工作区不存在，不访问失效实例。

## 工具重建与实际验证

- Nature完整来源 `Yuan1z0825/nature-skills`，固定
  `b543e8b998eb2df1fd44641cc8b262c638c2b442`；保留全部源码及
  nature-academic-search/downloader/shared完整48/67/21文件目录。
  独立Python环境 `/workspace/tools/nature-runtime/venv`，Node24.19开启
  `NODE_USE_ENV_PROXY=1`。实际stdio MCP初始化、工具调用、已知DOI联网解析、
  downloader直接PDF下载均验证。直链PDF的SI not_found不当无附件证据。
- ScanSci PyPI固定1.18.0，历史完整源码固定
  `3df79f8211ec2fb542170d132e330fc7bb92ab96`。
  额外核实发现v1.18.0标签解引用为ec812f085f392a9b67768fbcad7ddeb340e0245f，
  两者不是同一提交；本轮重建支持固定此前源码提交，不混称标签与旧源码。
  完整目录 `/workspace/tools/scansci-pdf`，运行环境
  `/workspace/tools/scansci-pdf-runtime/venv`。
  实际18工具stdio MCP、设置读回及合法来源实际下载均通过。
- 首次原生Git获取公开工具失败，实际HTTPS codeload和官方GitHub提交API可用后，
  通过有固定SHA256的完整官方源码归档重建。归档校验失败必须停止，不能改期望值放行。
  保持TLS、CA和制品验证；旧上游verify=False由仓库外transport适配强制恢复可信验证。
- 两个依赖环境分开，按各自历史lock安装并通过依赖一致性检查；安装脚本重复执行通过。
  不改上游源码、全局用户配置或项目人工数据。源码和虚拟环境在项目checkout外。

安装：

```bash
cd /workspace/FirstCodex
export PYTHONDONTWRITEBYTECODE=1
bash results/ad-oxygen-literature-20261006/methods/runtime_support/recover_20261017.sh
```

联系邮箱在环境设置 `SCANSCI_CONTACT_EMAIL`、`NATURE_CONTACT_EMAIL` 或仓库外
私有配置中提供；不写入安装脚本或Git。合法来源开启，灰色来源/Tor/自动机构登录关闭。
学校账号、MFA和浏览器会话仅由本人在官方交互界面操作，不导出cookie或索取密码。

## 首批真实上传门槛

R01238、R03455、R02454从既有官方/仓储链接实际重取，前部题名/作者/出版信息及
正文结构核对，6/11/4页全部解析，与历史核验原件SHA完全一致。
立即推送提交eb7a4054b9c30a014b262b8aafa8369bbf07a73c后，独立Git对象库经
远端HTTPS重新取回，大小、SHA256及可读性通过，之后才开始批量。
证据在 `inventory/recovery_20261017/pilot_downloads.json` 和 `pilot_gate.json`。
恢复的旧原件不冒充本轮三篇重新下载样本。

## 继续获取与备份

使用现有隔离checkout，除非用户明确要求，不建立Git worktree。不改main、不强推。
每次提交前先fetch并核对远端祖先关系；远端推进或分叉时保留工作并处理合并，禁止覆盖。
GitHub API已实际确认仓库private及push权限，权限值在专门审计JSON中，不包含凭据。

```bash
cd /workspace/FirstCodex
export PYTHONDONTWRITEBYTECODE=1
PY=/workspace/tools/scansci-pdf-runtime/venv/bin/python
P=results/ad-oxygen-literature-20261006
"$PY" "$P/methods/recovery_20261017.py" audit
"$PY" "$P/methods/recovery_20261017.py" parse
# 只在真实三篇门槛尚未完成时运行pilot，再sync和独立核验。
"$PY" "$P/methods/recovery_20261017.py" batch
"$PY" "$P/methods/continue_records_20261017.py" supplementary
"$PY" "$P/methods/continue_records_20261017.py" known
"$PY" "$P/methods/continue_records_20261017.py" publisher-supplements
"$PY" "$P/methods/recovery_20261017.py" audit
"$PY" "$P/methods/recovery_20261017.py" parse
"$PY" "$P/methods/recovery_20261017.py" sync
```

正文/附件原字节放 `original_files/`，全部取得且允许保存的原件和解析输出直接进本私有分支，
不再把许可未明确的私有研究副本留在临时环境等待其他存储。
正文版本逐文件记出版版、接受稿、预印本或明确的其他版本；不能以下载成功代替身份核验。
历史SHA一致可复用旧身份验证，加当前逐页解析；新SHA的PDF必须人工核对自身题名/作者/
DOI或学位出版信息及正文，自动命中引用文献不能证明身份。

每5篇处理记录或10分钟先到即保存并推送取得的字节和日志，结束前最后同步。
新原件必须独立读回校验后才标已备份；同一不可变Git blob已读回后，后续批次核对远端
树中的同blob身份并复用该次SHA/可读性凭证，原件变化或新文件仍实际读回，不重复下载不变文件。
回执明确区分本批实际读回与既有对象复核，保留原读回提交。
最终只含回执/方法等元数据的同步可用 `sync-final`，最新远端核验结果保存在仓库外
`/workspace/tools/final_remote_readback_20261017.json`，避免把回执自身提交ID循环写进自身。

同来源有节奏请求，CONNECT拒绝、HTTP403挑战、HTTP429及503/超时分开记录。
单请求增加60秒总时限，同一附件传输包在一次处理内复用。一个来源失败不阻断其他来源。
不对挑战反复请求，不将失败解释为无附件或学校一定无订阅。

## 补充材料和数据

检查完整JATS和身份匹配的文章页；下载其明确声明的PDF、Word、Excel、CSV、图像、
视频、代码或ZIP等原格式。页面没有找到链接不自动判无附件。
完整JATS明确未声明本地附件、页面明确声明无附件、尚未检查、访问失败、部分成功及
外部数据库链接分别记账。大型数据库只记链接/披露大小；未披露总大小明确记未知，
不将HTML页面Content-Length误作数据库总量，不自动整库下载。

仓储生成的transport ZIP不与同一组附件重复入库；研究者本来提供的官方ZIP作为原附件
保留，解包成员只建位置/SHA索引及处理结果，不新增重复原字节副本。先前已在Git的5份
派生Excel原样保留。原有统一ZIP为历史元数据包，不宣称含正文，也不重新把原件整包重复提交。

官方GitHub规则已从github/docs实时读取：Git单文件50MiB警告、100MiB阻止，网页上传
25MiB与本次原生Git推送不同。当前取得文件均低于Git单文件限制，不需要LFS，未假定LFS
额度可用。后续遇到大文件必须先核实当前规则/仓库支持及配额，不能只上传清单称原件已保存。

## 冷启动与交付边界

安装脚本和启动说明已保存环境配置草稿；草稿保存、运行实例准备、发布快照和新任务
冷启动验证是不同事件。新环境发布由用户在环境设置完成；Git原件备份不依赖发布快照。
本轮未把未来新任务冷启动称为实测完成。当前正文、SI、缺件和远端核验数量以最新
`inventory/recovery_20261017/` 回执为准，不以本文中的阶段性数量推断完成。

## 已执行的后续恢复和完整解析

`targeted_repository_followups_20261017.py` 只跟随既有目标文章公开的下载表单、
同一Cranfield原始文件包和Chulalongkorn条目API。R09240的31页出版版已核验，
两篇2015年硕士论文R13968、R13969的封面、批准页、目录及章节I–V和参考文献/
附录核对完毕。各7份原PDF、合计117/87页构成完整正文，保留原分章方式，
不把封面单独宣称完整论文。每份的顺序、大小、SHA和来源见资产清单与
`multipart_identity_reviews_20261017.json`。`register_reviewed_multipart_20261017.py`
只注册已有明确核验决定及全部原件齐备的组，默认不自动判断新PDF身份。

R07238的mmc1.docx已通过保存的准确PII和完整JATS声明文件名，从官方出版商CDN
重取，49526字节及SHA与历史一致，Word容器校验通过。可重复脚本为
`recover_declared_attachment_20261017.py`。该条目的两个官方附件均已恢复。
同一ZIP中的g a.skp与旧派生文件34855493字节、SHA一致，保留在官方ZIP中，
不另外生成重复原件。10个旧传输ZIP只保留历史记录，全部对应官方附件已单独保存。

完整解析使用独立、锁定依赖的第三个环境，实际运行：

```bash
cd /workspace/FirstCodex
P=results/ad-oxygen-literature-20261006
export PYTHONDONTWRITEBYTECODE=1
/workspace/tools/corpus-runtime/venv/bin/python "$P/methods/corpus/extract_search.py" extract \
  --project "/workspace/FirstCodex/$P" --root "/workspace/FirstCodex/$P" --ocr --workers 2
/workspace/tools/scansci-pdf-runtime/venv/bin/python "$P/methods/finalize_recovery_20261017.py"
/workspace/tools/scansci-pdf-runtime/venv/bin/python "$P/methods/recovery_20261017.py" audit
/workspace/tools/scansci-pdf-runtime/venv/bin/python "$P/methods/recovery_20261017.py" sync
```

解析原件与来源SHA绑定，保留PDF页/块坐标、Word段落、Excel工作表/单元格及JATS
段落位置。实际处理3025页PDF、53页英文OCR，生成60327条文本块和243张表格。
OCR和表格是未逐数值复核的派生结果；保留原件供核对。58份HTML仅保留来源证据，
不宣称已提取其正文；3份官方ZIP建立成员/SHA目录，不执行代码或复制整组原件。
`search.sqlite`为本地全文索引，数据库完整性及FTS查询均另行校验；这不是新的外部检索。

附件入口中误匹配的18个参考文献/分享/全站导航链接已从当前外部数据列表移出，
原记录及纠正理由保留。`curate_supplementary_evidence_20261017.py` 从已取得正文
中核验5处数据提交声明（4个不同项目），只请求ENA公开FASTQ字节数清单，
记录数据集链接、披露大小和来源页/段落，不下载测序数据库。
项目合计大小可能大于论文实际使用的子集，清单明确标注这种范围限制。

不要运行旧 `corpus/finalize_inventory.py` 的3样例发布策略覆盖本轮全量授权备份。
最终交付汇总、逐ID失败矩阵和独立读回清单位于 `inventory/recovery_20261017/`；
未取得的正文与尚未查明的附件，不能解释为不存在或学校肯定无订阅。
