# FirstCodex

本仓库保存微曝气厌氧消化（AD）综述的文献、原件与分析准备成果。项目从主动氧/空气输入的工艺研究检索起步，经过筛选与用户校正、全文/补充材料整理、期刊统计和组学方法核验，再扩展到厌氧微生物氧响应机制及可复用测序数据。各阶段保留稳定文献ID、判断依据和来源，文献数、文件数、项目数与run数分别统计。

**[完整项目介绍与全部成果导航](results/ad-oxygen-literature-20261006/README.md)**

本页及完整介绍位于结果分支 `results/ad-oxygen-literature-20261006`，介绍修复日期为2026-10-25（Asia/Shanghai）。没有因这次文档修复重新检索、筛选、修改人工判断/进度或下载论文原件。

|研究阶段|为什么做、实际做了什么、结果与限制|
|---|---|
|[1. 微曝气AD文献检索](results/ad-oxygen-literature-20261006/README.md#stage-1)|围绕主动供氧的位置/阶段检索2012年至2026-10-06/07研究；Nature学术技能配合官方API、人工分类同步、43综述追溯、漏检审计及补检形成554条库。保存的宽词返回仍未筛尽，不能声称绝对完整。|
|[2. 正文与补充材料](results/ad-oxygen-literature-20261006/README.md#stage-2)|用Nature Downloader、ScanSci和公开/授权来源获取，再按身份、版本及SHA合并本地/云端文件。2026-10-23清单为388篇全文、154原格式SI，规范对象665；缺目标正文38，附件归属及合并后全量索引仍待补。|
|[3. 期刊与JCR统计](results/ad-oxygen-literature-20261006/README.md#stage-3)|核刊名/ISSN/载体，统一2024指标年/2025发布版；386目标期刊论文核实272条，缺114。逐学科分区、来源和部分覆盖限制保留，不将缺失视为非Q1。|
|[4. MG/MT全文方法筛查](results/ad-oxygen-literature-20261006/README.md#stage-4)|从426范围任务逐篇查方法、建库及数据声明，排除16S等扩增子/预测功能。B001–B010确认21MG+1MT，341研究均进入方法筛查但8仍待确认；文章确认不等于原始reads公开。|
|[5. 氧暴露机制扩展](results/ad-oxygen-literature-20261006/README.md#stage-5)|从AD拓展到纯/共培养、酶学、沉积物与肠道等可迁移机制；1536关联池完成首遍分层初筛，35篇后读完整缓存摘要，仍未全文核实。引用/JIF辅助，严格独立支持未确认，Crossref尾部等缺口明示。|
|[6. 测序数据与关联论文](results/ad-oxygen-literature-20261006/README.md#stage-6)|复用旧22篇后双向查询ENA/BioProject/SRA/PubMed，核项目—样本—run及处理键。审计69项目，38有公开群落reads清单；设计缺口、技术重复及未下载FASTQ分别记录，不能据公开项目数推断独立实验数。|
|[7. 成果导航与续跑](results/ad-oxygen-literature-20261006/README.md#stage-7)|集中提供各阶段Excel、RIS、原件、方法和队列；未完成工作按阶段保留。新增工作应追加相应章节，不用最新任务覆盖整体介绍。|

常用入口：[AD总Excel](results/ad-oxygen-literature-20261006/final_results/ad_oxygen_download_review_20261006.xlsx) · [规范原件](results/ad-oxygen-literature-20261006/original_files/) · [JCR Excel](results/ad-oxygen-literature-20261006/final_results/journal_jcr_statistics_20261023.xlsx) · [组学筛查Excel](results/ad-oxygen-literature-20261006/omics_screening/omics_screening_cumulative.xlsx) · [机制Excel](results/ad-oxygen-literature-20261006/oxygen_response_review/oxygen_response_review_cumulative.xlsx) · [数据发现Excel](results/ad-oxygen-literature-20261006/omics_dataset_discovery/omics_dataset_discovery_cumulative.xlsx)

[章节恢复对照](results/ad-oxygen-literature-20261006/method_audit/readme_restoration/chapter_map.md)与[运行历史附录](results/ad-oxygen-literature-20261006/HISTORY.md)说明原内容的去向。主要研究阶段在首页正常可见；只有逐轮环境、网络和执行回执单独归档。
