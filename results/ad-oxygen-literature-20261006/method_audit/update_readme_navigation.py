#!/usr/bin/env python3
"""Documentation only: make current methods primary, retain old README in place."""
from pathlib import Path
P=Path(__file__).resolve().parents[1]
START='<!-- HISTORICAL_README_BEGIN -->';END='<!-- HISTORICAL_README_END -->'
def write(path,intro):
 old=path.read_text()
 if START in old:old=old.split(START,1)[1].split(END,1)[0].strip('\n')
 path.write_text(intro.strip()+'\n\n<details>\n<summary>整合前README及历史阶段报告（折叠保留；当前流程以上方方法为准）</summary>\n\n'+START+'\n'+old.rstrip()+'\n'+END+'\n\n</details>\n',encoding='utf-8')
def run():
 write(P/'README.md','''
# 微曝气AD项目：两条工作线的方法导航

这里保留原AD文献库，并分别开展了“氧响应机制解释”和“可复用测序数据发现”。二者目标、纳入对象和完成深度不同。本次更新只从现存脚本、原始返回、逐项判断及提交历史重建方法；**没有新增检索、重新筛选或更改累计结果**。整合前报告折叠保留，避免历史“未筛1516”等旧状态遮蔽当前进度。

|想解决的问题|工作线与当前入口|完整方法及实际查询|
|---|---|---|
|氧为什么损伤/保护厌氧微生物，怎样联系AD机制？|[oxygen_response_review](oxygen_response_review/README.md)|[详细方法与真实案例](oxygen_response_review/methods/METHODS.md) · [完整检索式附表](oxygen_response_review/methods/QUERY_APPENDIX.md)|
|哪些公开群落DNA/RNA能复用，处理和样本能否对上？|[omics_dataset_discovery](omics_dataset_discovery/README.md)|[详细方法与真实案例](omics_dataset_discovery/methods/METHODS.md) · [完整检索式附表](omics_dataset_discovery/methods/QUERY_APPENDIX.md) · [新增60项目来源/选择](omics_dataset_discovery/methods/SELECTION_AUDIT.md)|
|复核本次说明是否改动原判断、数量是否来自实际集合？|[方法审计记录](method_audit/audit_summary.json)|[离线复建脚本](method_audit/rebuild_appendices.py) · [阶段提交快照](method_audit/stage_history.json) · [校验记录](method_audit/validation.json)|

原AD总表仍在[final_results](final_results/)，原件仍在[original_files](original_files/)；原ID、分类及用户人工判断保留。新范围判断由助手模型作出，不称用户人工复核。

## 机制文献线怎样流转

问题从AD扩展到其他厌氧环境的具体靶点、代谢和互作。实际查询PubMed、Crossref、OpenAlex，随后以一个原始研究为种子做有限前/后向追溯；不是强制omics检索。

```mermaid
flowchart LR
 A[数据库返回与原AD记录] --> B[规范身份／保留旧ID]
 B --> C[分层阅读与模型逐项初筛]
 C --> D[优先／待确认／背景／排除]
 D --> E[后续全文及具体主张核验]
```

1,147是可重复的返回行；按逐输入映射得到1,039个返回身份，其中57与原554重叠，982为新增身份。旧554全部保留，因此池为1,536，**不是纳入数**。首20与后来新增1,516的阅读深度不同；新增全池仅题名/摘要关键句初筛。35篇之后读了完整缓存摘要，仍是阅读队列，不是已确认核心或全文核完。364暂定优先、479待确认等集合的具体来源和那1条范围相关但精读暂缓的例外，详见方法集合表。

Crossref每组前100的尾部仍未补齐；MCP/CLI失败由官方API替代，不把工具安装当成功。引用/JIF辅助排序，不能替代AD相关性、因果证据或独立支持。

## 数据发现线怎样流转

先复用旧omics审计的22篇（21MG+1MT）和9个项目号，再从ENA/BioProject直接查询，从PubMed及项目Publication字段双向关联。主目标是群落shotgun DNA/RNA；扩增子、纯培养/单细胞、病毒富集及派生组装分列。

```mermaid
flowchart LR
 A[论文声明与官方平台查询] --> B[项目／样本／实验／run关联]
 B --> C[核类型／镜像／项目别名]
 C --> D[核氧处理／对照／时间／重复]
 D --> E[下载准备或具体缺口队列]
```

累计审计69项目（旧9+新增60），38有公开群落reads清单：A5/B20/C13。A/B的349 run和C的333 run单列，不当生物重复。16项对比键中12有已读全文方法支持、4仅元数据暂定；共享研究、对照或反应器，不能称16独立实验。GSA未成功检索，FASTQ入口抽检被代理阻断；**公开清单不等于FASTQ已下载验证**。418项目尚未审计；论文队列2228含12篇原22已审计旧文，身份过滤待修，还含宽泛自动扩展结果，不能称全部新候选。

本次方法说明的验算基准为提交0f9eeec20。历史统计及下一步建议只代表各自提交时点；现有累计数据在两条工作线原Excel/CSV/JSON中，方法审计没有重写它们。
''')
 write(P/'oxygen_response_review/README.md','''
# 厌氧微生物氧暴露／氧冲击机制文献

本工作线为微曝气AD综述解释损伤、防御、代谢、互作、空间和恢复机制，允许非AD的纯培养、酶学及自然环境研究。它与原AD库关联，但不继承旧AD排除结论；没有要求omics。原分类和用户判断保留，新范围筛选是助手模型判断。

**先读：[详细方法（范围、逐阶段判断、四个真实案例、局限）](methods/METHODS.md)**。复现实际查询看[检索式附表](methods/QUERY_APPENDIX.md)；核数量关系看[逐ID集合表](methods/flow_membership_utf8.csv)。本次是方法整理，不新增检索或重筛；整合前报告在页底折叠。

## 实际过程

2012-01-01至2026-10-24，PubMed按对象、氧情境和机制分17组；Crossref做3组相关性文本补充，各取100；OpenAlex做3组题名/摘要查询并翻cursor。另从2020年Bacteroides原始研究的参考文献选4 PMID，并取32条前向引用。早期机制研究另标。MCP返回内部错误、CLI429没有算成功，实际结果来自官方API；WoS/Scopus未检索。

```mermaid
flowchart LR
 A[原始返回＋原AD记录] --> B[DOI／PMID／题名身份映射]
 B --> C[首批分层阅读与其余片段初筛]
 C --> D[范围与证据层级分开判断]
 D --> E[暂定优先／待确认／后续核实]
```

从AD扩展时优先具体功能与靶点，而非同门同科；急性冲击、持续微氧、反复暴露和去氧恢复分开。H2O2/ROS或化学调ORP不冒充直接O2干预；基因/组学不直接等于活性、互作或因果。

## 当前数量分别指什么

|对象|数量及含义|
|---|---|
|原始检索输入|1,147行，组间/来源可重复；Crossref尾部仍未补|
|返回身份与关联池|1,039返回身份；57关联原库、982新身份；旧554全部保留，池1,536|
|首20|10读相关全文段落、10仅摘要；范围17+离体酶学1+待确认2。后来推荐17不是同一“范围17”集合|
|新增1,516|题名/摘要关键句初筛：347候选、477待确认、336背景、356排除；不称完整摘要/全文审阅|
|累计优先/待确认|364暂定优先=新增347+原17推荐；479待确认=477+原2；另1条DAMO范围相关但精读暂缓不在这两队列|
|新35阅读队列|从347候选跨主题指定，后来读完完整缓存摘要；新增全文核实0。其余312候选继续核实，35不是终选上限|

引用统一OpenAlex快照、期刊指标沿用2024机构索引缓存；缺值留空，无“高被引/高JIF”统一阈值。原20有具体主张验证关联，但未确认同对象同条件严格独立复制；新35也不能称广泛验证。详见方法的五维评价和阅读深度表。

## 文件和下一步

- [同一累计Excel](oxygen_response_review_cumulative.xlsx) · [总表CSV](literature_master_utf8.csv) · [catalog JSON](catalog.json)
- [364暂定优先](all_pool/provisional_priorities_utf8.csv) · [479待确认](all_pool/pending_confirmation_queue_utf8.csv) · [原20五维评价](reading_priority/evaluations.json)
- [35篇逐篇来源/条件/阅读深度](reading_queue35/README.md) · [其余312续跑](reading_queue35/other_in_scope_continuation_queue.json) · [机制进度](all_pool/progress.json)
- [原始查询日志](search_log.json) · [返回到ID映射](dedup_input_mapping_utf8.csv) · [身份冲突](identity_conflicts.json)

机制工作线已因切换数据发现而暂存。后续先补待确认记录的完整摘要/必要全文，核35及其他候选的具体主张；不重跑主题检索，不重复查询原20指标。P001/P002未保存当时所示片段、Crossref截断、P012错位更正、版本冲突和访问失败均在详细方法中明示。这里没有用本次新阅读改写旧判断。
''')
 write(P/'omics_dataset_discovery/README.md','''
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
''')
 # Stage-specific reports remain useful, but their obsolete next-step prose is not current policy.
 for relative,label in [('oxygen_response_review/all_pool/README.md','全池初筛阶段'),('oxygen_response_review/reading_priority/README.md','原20五维评价阶段'),('oxygen_response_review/reading_queue35/README.md','35篇来源审计阶段')]:
  p=P/relative;text=p.read_text();notice=f'> **阶段记录：{label}。** 当前整合方法与阶段衔接以[详细方法](../methods/METHODS.md)和[当前入口](../README.md)为准；下文的“本轮/下一步”属于当时阶段，不代表后来重新检索或全文已核完。\n\n'
  if not text.startswith('> **阶段记录：'):p.write_text(notice+text,encoding='utf-8')
if __name__=='__main__':run()
