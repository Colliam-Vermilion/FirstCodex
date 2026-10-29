# 氧暴露机制综述分支迁移（2026-10-29）

基准：`2f952089deb28b2112ec90d0534dc7dff7e5e316`。原分支`results/ad-oxygen-literature-20261006`；综述分支`review/oxygen-response-mechanisms`。创建前工作区干净，同名远端不存在；仓库默认fetch仅更新main，已显式fetch结果分支并核对远端，综述检出快速前进到此基准后才编辑。没有重置或强制推送。

## 范围清单

|归属|实际路径与处理|
|---|---|
|综述专属|`results/ad-oxygen-literature-20261006/oxygen_response_review/`全部1,872个原已跟踪文件，基准105,775,207字节。包括63个raw文件、20个evidence_sources文件、20个首批decisions、全池1,664项、32项reading_priority、11项reading_queue35、8项methods和17项scripts及累计Excel/RIS。先在新分支完整核验，再从原分支正常提交移除。逐文件大小与SHA见[完整清单](exclusive_files_utf8.csv)。|
|共同保留|`final_results/`、`manual_review/`、`methods/`、`inventory/`、`original_files/`、`papers/`、原始AD数据库、Windows/localdownload，以及`omics_screening/`、`omics_dataset_discovery/`均按基准继承到新分支，并继续留在原分支。无论文、附件、分类、人工判断或组学记录因文章重合被删除。|
|共享审计|`method_audit/`、`HISTORY.md`涵盖两条线，保留两侧，历史结果不重算；现行链接按分支解析，历史快照保留其日期。|
|需跨分支读取|数据发现复用机制catalog身份、两份官方JATS与四个初始化保护快照。没有重复打包或复制原件；[配置](dependency_sources.json)固定基准提交与SHA，[解析器](../../omics_dataset_discovery/scripts/review_dependency.py)用`git show <commit>:<path>`读Git对象，不假设相邻分支在工作目录。|
|归属交叠而保留|数据发现的`associated_papers*`、`dataset_evidence*`、`new_associated_papers.json`、`reused_cached_fulltext_methods.json`、`mechanism_review_paused.json`、baseline及方法审计中的综述来源说明。它们是关联和溯源记录，不应因含OR-ID或综述路径删除；未改其科学内容。没有发现需另移的独立专属目录。|

## 两分支入口与续跑

- [机制综述入口](https://github.com/Colliam-Vermilion/FirstCodex/blob/review/oxygen-response-mechanisms/results/ad-oxygen-literature-20261006/oxygen_response_review/README.md)、[方法](https://github.com/Colliam-Vermilion/FirstCodex/blob/review/oxygen-response-mechanisms/results/ad-oxygen-literature-20261006/oxygen_response_review/methods/METHODS.md)、[Excel](https://github.com/Colliam-Vermilion/FirstCodex/blob/review/oxygen-response-mechanisms/results/ad-oxygen-literature-20261006/oxygen_response_review/oxygen_response_review_cumulative.xlsx)：只在新分支继续补读和机制判断；35仍为阅读队列，364暂定优先及479待确认不变。
- [原分支完整介绍](https://github.com/Colliam-Vermilion/FirstCodex/blob/results/ad-oxygen-literature-20261006/results/ad-oxygen-literature-20261006/README.md)、[数据发现](https://github.com/Colliam-Vermilion/FirstCodex/blob/results/ad-oxygen-literature-20261006/results/ad-oxygen-literature-20261006/omics_dataset_discovery/README.md)：AD资源维护和组学分析继续原分支。
- 新分支由原分支建立，会继承历史和共享数据，后续更新不会自动同步；本轮隔离后续工作，不清理Git历史或删除继承的组学资料。相同原件可被两条工作线引用。

## 无网络的共享依赖检查

```bash
python results/ad-oxygen-literature-20261006/omics_dataset_discovery/scripts/review_dependency.py
python results/ad-oxygen-literature-20261006/branch_migration/oxygen_response_mechanisms_20261029/validate_migration.py
```

正常完整clone继承基准Git对象；浅克隆若缺少对象，可在已授权仓库使用：

```bash
git fetch origin 2f952089deb28b2112ec90d0534dc7dff7e5e316
```

再执行只读检查。读取的是固定历史字节，既有证据中旧相对路径通过该配置映射；浏览器查看用配置中的不可变GitHub链接。以后需要采用新综述身份库时应显式升级配置、重新核对ID映射，不能无声跟随分支头。

本轮不执行原始研究脚本。原`method_audit/rebuild_appendices.py`同时写两条线的附表，已加迁移后保护，避免原分支缺综述时创建目录；既有历史验证器因绑定旧基准，现行入口改用迁移只读检查。旧验证JSON与远端读回JSON均为当时快照，未伪装成本轮结果。

## 顺序与验收

先推送新分支，再从独立clone取回并逐文件核清单SHA／大小，打开Excel／RIS／JSON，核方法、证据和续跑；通过后才删除原分支专属文件。读回报告以`*_readback.json`保存，后续报告引用已验收提交；不为把报告自身计入被验收内容而循环改写结果。原分支删除清单即[逐文件清单](exclusive_files_utf8.csv)的全部path，Git历史保留。本轮无检索、重筛、原件重下、重复ZIP、main变更或强制推送。

## 已完成的独立读回

- [新综述分支读回](review_readback.json)：验收内容提交`68e0e8f3a05d283e4325fcef526c3707dbaba949`，全部1,872项大小和SHA匹配，Excel及6份RIS可读，7项固定依赖可读取。
- [原分支清理读回](data_readback.json)：验收内容提交`c8a5a32b4e8d3d769b21d49e0f5a99813c8f3fd3`，1,872项专属路径均已移除；原分支仍可读7项依赖，共享非文档／非脚本文件的Git对象未变。读回均来自各自独立、经GitHub取回的部分克隆，不共享执行仓库的对象库，不重复下载共享论文原件。
- 后续报告提交仅增加迁移证据或改进只读检查，综述科学结果与原分支数据保持上述验收内容；不改main，不强推。
