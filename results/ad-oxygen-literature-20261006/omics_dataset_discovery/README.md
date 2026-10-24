# 测序数据集发现与关联论文检索

实际检索/审计日期：2026-10-24 UTC。基准提交 `d8e4ee59577b3307a7814f6c91dd442107cb8aef`。机制综述已暂存；原 omics_screening、oxygen_response_review 的判断、进度、Excel与原件保留。保护文件SHA见[baseline](baseline.json)，续接位置见[暂存记录](mechanism_review_paused.json)。未从零重筛原426条全文审计记录。

[累计Excel](omics_dataset_discovery_cumulative.xlsx) · [项目CSV](data_projects_master_utf8.csv) · [样本/run CSV](samples_runs_mapping_utf8.csv) · [关联论文CSV](associated_papers_utf8.csv) · [群落关联论文RIS](community_dataset_papers.ris) · [全部关联候选RIS](associated_papers.ris) · [统计JSON](summary.json) · [续跑进度](progress.json)

## 实际完成与计数口径

| 项目 | 结果 | 解释 |
|---|---:|---|
| 既有目标文章 | 22：21 MG、1 MT | 不是22篇MG加额外MT |
| 既有项目号 | 9，7有公开目标reads | 另2当前ENA/SRA未检出公开run，不证明私有或不存在 |
| 既有文章关联run | 49 | 完整项目另找到2个厌氧WGS，共51群落run、48归档BioSample |
| 本轮新增项目审计 | 60 | 连续三批20，加原9共69；检查点已分批推送 |
| 已审计公开群落项目 | 38，其中31新增 | A层5、B层20、C层13；未将新发现的扩增子AD当新增A层shotgun |
| A/B公开规模 | 25项目、349 run、261归档BioSample | 含待补分组项目；不是349生物重复或25独立实验 |
| C背景公开规模 | 13项目、333 run、280归档BioSample | 单列，不与A/B合并推断氧效应 |
| 全部公开群落目标run | 682 | 特殊单细胞/纯培养/宿主/扩增子不计入；未下载/质控reads |
| 比较记录 | 16项 | 12项有已读全文方法+官方样本键，4项仅元数据暂定；共享对照/反应器/时间 |
| 项目候选及剩余 | 487；418未审计 | 包括宽泛查询与论文数据引用，不是487个合格数据集 |
| 关联论文记录 | 原22+新增47，共69 | 新增47中42此前未入库；含特殊、排除及待筛，不是47篇确认纳入 |
| 关联已核公开群落项目的论文 | 20 | 原8+新增关联12；12中9篇新论文、3篇复用机制库 |

已知同队列关系暂分35个公开归档研究组；**全部独立研究数及生物学样本总数未知，留空**。同一实验可拆很多项目，DNA/RNA可能分项目，多篇文章也可复用数据。[去重表](dedup_relationships_utf8.csv)记录同研究、官方别名、共享样本及官方MD5重复线索。12个核心消化器取样的反应器键明确，不将这一子集外推为全池生物样本数。比较记录绝非16独立研究或16个有重复的统计检验。

## 先审计原22篇

[逐篇现状/原文声明](existing_articles_availability_audit.json)复用旧全文方法、页码、项目号，不重新下载PDF。R09236与R12985共同使用PRJNA1013451，不重复计研究。原7个公开项目中，PRJNA1013451和PRJNA1287080有旧全文及官方样本键共同确认的供氧对照（5项比较，共享反应器/时间）；其余仍缺处理键、匹配时间或比较设计。

- PRJNA565588：旧2个微曝气WGS外，新增SRR16980862/63两个厌氧WGS；采样日、SINGLE/PAIRED及别名冲突待核，不能直接拼匹配对照。
- PRJNA1086167：官方protein/starch/blank与论文SRR顺序冲突，不自动修正。
- PRJNA1128434、PRJNA1447957：保留原始代号，氧/CO2/DW或温度×空气处理键未核。
- PRJNA357876：6run/3归档样本，温度/阶段背景C，无匹配氧对照。
- PRJNA1369098、PRJNA1438379：论文有号，当前未检出公开run，类别3。
- R13274明确raw metatranscriptomic reads可索取（类别4）；6篇仅泛指数据可索取（类别5），不推断包含FASTQ。R13817明确作者无权分享，不能写可索取。另4篇目标编号/声明未定位或矛盾；R13904的16S编号不能代替MG编号。

## 优先下载准备及边界

[7项目优先表](download_preparation_priority_utf8.csv)及[所选比较文件入口](download_preparation_file_manifest_utf8.csv)已生成。“准备”表示有官方文件清单和比较键，**不是已下载或质量验证**。累计表含项目/样本/实验/run、建库来源/策略/选择、平台、布局、官方URL/bytes/MD5和原始计数字段。ENA read_count与SRA spots保留原字段，双端不能混算。

| 项目 | 用途和证据 | 限制 |
|---|---|---|
| PRJNA1013451，A | 21 WGS；12核心取样为4反应器×3时间，氧/声音析因 | 每处理1反应器；时间点非独立重复；已存在resistome再分析论文 |
| PRJNA1287080，A | 2 MG：R1对照、R4每日20mL空气，40日终点 | 每条件1文库，培养重复不等于测序重复 |
| PRJNA551662，B | 20 WGS；0/5/10% v/v O2，98日供氧后134日厌氧；全文§2.2/2.6已读 | 部分时间点混池；公开文库不平衡，0%比较各仅1库；Time Point代码未擅自换日 |
| PRJNA1163300，B | 2 MT；24h约4% O2 vs厌氧，两者1mM laminarin，21°C；全文培养/RNA章节已读 | RNA混池，每条件1库；同实验无可用MG；SAG及其他地点JGI DNA不是配对MG |
| PRJDB17922，B；关联17921 DNA | 6 MT，氧增加前/后各3标签；DNA另7库 | strategy误标WGS；需核独立重复、剂量和DNA/RNA物理配对 |
| PRJNA1403469，B | 4 MT：两SBR各自AN/AE；另2 MG | DNA按反应器整体，非逐阶段配对；时间/底物混杂，每阶段1RNA库 |
| PRJNA347538，B | 32 MT run=16 RNA实验；day15 oxic/anoxic 8/6run | 每实验2run需辨技术关系；RNA共用1 BioSample，不是1生物样本或32重复；方法待核 |

其他高潜力待补键项目：PRJNA1426923（55 WGS，实验室/现场再氧合、filter与疑似质控混合）；PRJEB65123（12MG+16MT，四周氧历史）；PRJDB36680（15MG+13MT，官方别名PRJCA039809）；PRJNA322450（12MG+22MT，共用BioSample需SI）；PRJNA381321（6MT快/慢再氧合）。[可索取/待确认表](request_or_pending_utf8.csv)逐项列缺口。

[A/B群落run](oxygen_candidate_community_runs_utf8.csv)、[C背景run](background_community_runs_utf8.csv)及[非目标run索引](non_target_assay_run_index_utf8.csv)独立交付；总映射表3794行保留全部已查官方run的类型审计，不应将其当目标数据规模。

ARG/MGE首选群落总DNA，仍须核扩增/提取偏向、宿主污染、深度、组装和重复。短reads共现不证明ARG宿主、质粒传播或病毒宿主。总DNA可探索DNA病毒/前噬菌体，不保证RNA病毒或低丰度病毒。RNA是表达数据，不能替代DNA丰度；RNA-SIP密度分级、WGA、单细胞分列。PRJNA301899/818156/1186224官方Assembly查到1/12/26条派生记录，类别6表示当前raw未定位，不断言其他项目无reads；GenBank/RefSeq别名不当独立组装样本。

## 检索覆盖与证据

使用nature-academic-search的可用来源策略及官方HTTP接口；技能MCP未挂载，不称MCP已恢复。NCBI BioProject/SRA/PubMed/Assembly及ENA实际成功；GSA入口代理403，**未执行GSA检索，返回数未知**。[来源测试](source_availability_utf8.csv)。

ENA执行16组；BioProject 4组；PubMed 4组主检索+4组项目追溯。[日志](search_log.json)保留实际查询/翻译/警告、日期、分页、完整返回及错误；[原始响应](raw/)和[请求日志](request_log.jsonl)可读回。E05原offset失败后以官方limit=0全取1282并核count，失败历史保留，非只取1000。其他ENA组完整保存实际返回，NCBI全ID分页并批量取元数据。

P06追溯短语未被识别，PubMed自动扩展返回2125条，完整保存为低优先背景队列，不能称精确题名命中或已筛。各PubMed路径去重缓存2275篇，2228待关联/范围筛查。新增47篇关联也不代表纳入；3篇仅定位参考文献中的数据引用，[精确字段/原文](paper_project_mention_evidence.json)单列，不能据此认定本文产生项目。

官方项目描述、实验题名/样本属性、摘要和已读全文章节分层记录：[证据与位置](dataset_evidence_utf8.csv)、[复用两篇全文方法](reused_cached_fulltext_methods.json)。未知剂量/温度/重复/样本键留空，不把16S、功能预测、纯培养、植物宿主、病毒富集或SAG混入主集合。

7个旧公开项目FASTQ HTTPS HEAD抽检均被当前环境代理403；清单给出URL/bytes/MD5，但**未实际下载FASTQ并核MD5**，代理阻断不等于未公开。下一阶段云端传输需允许 `ftp.sra.ebi.ac.uk:443`，GSA需 `ngdc.cncb.ac.cn:443`。可在环境网络设置允许后重测，或本地用官方镜像下载。本轮没有改变网络配置、下载FASTQ、重新下载原件或联系作者。

## 文件及续跑

`project_cache/<项目号>/`缓存完整ENA run清单、NCBI样本/实验/建库/属性、项目XML、UID分页及状态；`raw/<来源>/`按URL哈希存响应及状态。CSV为UTF-8 BOM；JSON保留完整长字段；Excel单元格截至32700字符。GitHub本轮交付发现结果和文件入口，**不是FASTQ备份**。

复现导出：`python scripts/finalize_outputs.py`，依赖Python标准库和openpyxl。新增核实先依[剩余项目稳定队列](remaining_project_queue_utf8.csv)复用缓存，由collect_projects.py补元数据，再人工更新project_assessments/sample_annotations和比较/论文证据，重建累计表、验证并推送原分支。不要重跑已完成查询或把自动分流提示当筛选结论。

后续：补优先项目处理键/独立重复/配对；Lake Washington同实验多子项目及合成群落先去重；从418项目及2228篇关联候选续跑；保留GSA受阻、待公开、明确reads索取、泛指索取、不允许分享的不同状态。项目数、论文数、生物样本数和可分析氧比较数分别报告。

[GitHub独立读回验证](remote_readback.json)：通过官方Git Blobs API重新取得Excel、RIS、统计及进度，逐字节/SHA256一致，Excel重开通过。此验证只针对交付表格，不表示FASTQ已经保存。
