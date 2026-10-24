# 可复用群落MG／MT数据与关联论文发现

目标是找到可二次分析的群落shotgun DNA/RNA及可追溯的氧处理设计，进一步评估ARG、MGE、病毒/宿主分析的可能性。论文相关不等于原始数据可用；有公开项目也不等于能做氧差异检验。原机制综述已暂存，原件和原判断保留。

**先读：[详细方法（双向发现、层次/可用性、样本关系、四个实际案例）](methods/METHODS.md)**。全部实际式与参数见[检索式附表](methods/QUERY_APPENDIX.md)，新增60的选择顺序与来源见[审计表](methods/SELECTION_AUDIT.md)。本次更新只审计方法，没有新检索、重筛或FASTQ下载。

## 实际过程和判断

先从既有omics审计中取明确“确认宏…”的22篇（21MG、1MT），复用方法/声明/页码及9个项目号，不重筛原全文库。然后ENA按氧情境×环境×library_source分16组、BioProject按主题4组、PubMed按论文4组加追溯4组；SRA承担精确项目核验和论文关联，未另做同样一轮广泛主题词检索。未设统一年份过滤，也不强制ARG/virus/MGE。

```mermaid
flowchart LR
 A[论文声明与平台主题查询] --> B[官方项目／样本／实验／run]
 B --> C[镜像／别名与类型核对]
 C --> D[处理对照／时间／重复映射]
 D --> E[公开清单及分析条件分层]
 E --> F[下载准备或待补证]
```

A对应AD/产甲烷供氧核心方向，B对应其他厌氧体系氧响应，C是无明确供氧比较的参考背景。层次和可用性分开：A候选仍可能缺样本键，C虽公开也不能推断氧效应。结合方法、描述、实验题名和建库字段识别类型；RNA-Seq可能是16S，WGS也可能是MT。扩增子、纯培养/单细胞、病毒富集及仅派生数据单列。

BioProject是归档集合，BioSample是归档样本，Experiment是建库/测序实验，Run是测序输出。分lane/技术run、双端文件和混池都不能直接扩充生物学n；同BioSample的DNA/RNA也需核物理配对。

## 当前结果的真实单位

|对象|结果与限制|
|---|---|
|旧22篇/9项目|7项目有公开目标reads清单，2未检出公开目标run；原49 run外新增2个厌氧WGS，共51/48归档BioSample|
|新增审计|连续三批60，不是指标前60或最终数量上限；其中31有公开群落reads，分B19/C12|
|累计公开群落集合|38项目：A5/B20/C13；A/B为349 run、261归档BioSample，C另333 run/280归档BioSample|
|比较记录|16项对比键，12有已读相关全文方法、4仅元数据；共享研究/对照/反应器，不能当16独立实验|
|尚未处理|487项目池中69审计、418未审计；保存论文队列2228行含12篇原22已审计重复，需联合ID/DOI/PMID清理（本轮未改队列）。另包含PubMed短语自动扩展的宽泛背景|

新增47篇论文关联候选（42此前未入库）不等于47篇确认符合范围；仅其中12篇已连到本轮核实的公开群落项目。数据可索取、泛指索取、未定位、作者无权分享分别保存，不代联系作者。

## 可安排下载与尚缺什么

优先AD为PRJNA1013451/1287080；扩展DNA为PRJNA551662；小RNA机制比较为PRJNA1163300。这4个有已读相关全文方法和样本键，但仍有单反应器、单文库、混池或不平衡采样限制。PRJDB17922、PRJNA1403469、PRJNA347538有暂定RNA处理键，可准备文件获取，方法/重复/时间混杂仍需先核。其他有潜力项目缺关键设计键，不因公开就直接进差异分析。

GSA入口403，未执行平台检索；ENA E05分页问题已以limit=0取全1282并核count。PubMed P06短语未识别后扩展2125条，完整保留但未称范围筛完。7个旧公开项目FASTQ入口HEAD被环境代理403阻断；**官方URL/bytes/MD5清单不是FASTQ下载或内容校验成功**。本轮FASTQ下载为0。

- [累计Excel](omics_dataset_discovery_cumulative.xlsx) · [项目CSV](data_projects_master_utf8.csv) · [样本/run全类型审计](samples_runs_mapping_utf8.csv)
- [A/B群落run](oxygen_candidate_community_runs_utf8.csv) · [C背景run](background_community_runs_utf8.csv) · [7项目下载准备](download_preparation_priority_utf8.csv) · [所选比较文件入口](download_preparation_file_manifest_utf8.csv)
- [群落数据关联RIS](community_dataset_papers.ris) · [全部关联候选RIS](associated_papers.ris) · [待确认/可索取](request_or_pending_utf8.csv)
- [官方项目缓存](project_cache/) · [查询日志](search_log.json) · [剩余队列/续跑](progress.json) · [交付表格GitHub读回验证](remote_readback.json)

ARG/MGE/病毒分析还需评估总DNA偏向、深度、宿主污染和组装；RNA不能替代DNA丰度，短reads共现不证明宿主关联。后续从保存队列补元数据、独立研究去重和方法，不重复检索或重下未变化论文原件。当前全部独立研究数、生物样本总数未知，明确留空。

## 可见的执行阶段与原有成果

本工作线先审计原22篇，再扩展平台和关联论文，连续三批核新增60项目，随后补缓存全文方法、去重/可行性和交付。上文保留完整方法概览；[全项目介绍](../README.md#stage-6)说明其与最初AD库和MG/MT全文筛查的联系，不将本数据发现阶段代替前面的研究。

|阶段|可追溯入口|限制|
|---|---|---|
|旧22审计/D001|[逐篇可用性](existing_articles_availability_audit.json)、[旧方法证据](existing_target_evidence.json)|有号、明确reads索取、泛指索取和无权分享分开|
|平台发现/D002–D004|[完整查询](methods/QUERY_APPENDIX.md)、[60顺序/来源](methods/SELECTION_AUDIT.md)|不是前60指标排名；418项目尚未审计|
|方法补证/分层交付/D005|[两篇缓存全文方法](reused_cached_fulltext_methods.json)、[比较键](oxygen_comparison_records.json)|12项方法支持与4项元数据暂定分开；并非16独立实验|
|方法审计发现|[详细方法](methods/METHODS.md)、[队列身份重叠](methods/queue_identity_audit.json)|原2228队列残留12篇已审计旧文，本次仍未改队列|

[原始结果说明的9208快照](https://github.com/Colliam-Vermilion/FirstCodex/blob/9208deddd624e99b1314bac359c22349c8554c64/results/ad-oxygen-literature-20261006/omics_dataset_discovery/README.md)与[运行历史](../HISTORY.md)保留具体回执；研究范围、结果入口和限制在本页及完整方法正常可见，不再整体折叠。
