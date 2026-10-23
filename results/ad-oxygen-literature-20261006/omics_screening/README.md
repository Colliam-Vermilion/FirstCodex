# 群落宏基因组／宏转录组累计全文筛查

B007（2026-10-23）读取GitHub基准`fc718c194eacf1cf0bf23cfcd7c9fa7647792724`，按稳定ID选取R10673–R13557接下来的50篇未开始研究。**48完成、2待确认：8宏基因组、1宏转录组、39非目标**。每篇即时保存JSON、证据和检查点；前20研究以`4e33d50`正常推送。没有重筛旧记录，没有新增文献检索、缺件全文或reads下载，也未联系作者。

- **[同一份累计Excel](omics_screening_cumulative.xlsx)**、[本批50篇CSV](batch_B007_results_utf8.csv)、[累计JSON](screening_records.json)、[累计CSV](screening_records_utf8.csv)。
- [证据JSON](evidence.json)、[证据CSV](evidence_utf8.csv)、[数据项目/样本/run](data_projects_samples.json)、[项目CSV](data_projects_samples_utf8.csv)、[待确认/相关线索](pending_related.json)。
- [累计统计](summary.json)、[批次进度](batches.json)、[逐篇检查点](checkpoint_log.jsonl)、[本批审计](batch_B007_audit.json)、[本地验证](batches/B007/local_validation.json)、[远端独立读回](batches/B007/remote_readback.json)、[交付文件SHA](batches/B007/delivery_manifest.json)。
- [SHA覆盖审计](source_coverage_audit.json)、[正文解析](parsed/)、[附件解析](parsed_attachments/)、[定位日志](term_location_log.json)、[目标词人工上下文判断](batches/B007/term_hit_manual_dispositions.json)、[原页视觉核验](batches/B007/visual/provenance.json)。定位工具仅检索，不自动分类；无命中仍完整阅读方法。

## 本批目标研究与数据获取

|ID|类型／产生方式|数据获取及证据位置|
|---|---|---|
|R10819|宏基因组，新产生|无编号；PDF11仅“Data will be made available on request”，是否含reads不明。正文阶段I/II与取样II/III命名歧义保留。|
|R11724|宏基因组，新产生|[PRJNA1287080](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1287080)，PDF3。官方R4-M→[SRR34383440](https://www.ncbi.nlm.nih.gov/sra/SRR34383440)、R1-M→[SRR34383441](https://www.ncbi.nlm.nih.gov/sra/SRR34383441)，均公开OTHER/METAGENOMIC/PAIRED/NovaSeq6000；另8个AMPLICON实验/run排除。|
|R11751|宏基因组，新产生|SI TextS4 PDF6明确随机DNA打断/HiSeq2500；全文和已归属19页SI未找到编号或相关测序数据声明。SI FigS4有A1–A3/B1–B3六点，但重复层级未说明。|
|R12127|宏基因组，新产生|SI TextS7 DOCX段落58明确内标/Covaris/DNA连接建库/NovaSeq6000PE150。PDF8仅泛指数据可索取；无编号。9条合成内标不是9个样本。|
|R12509|宏基因组，新产生|PDF3 CTAB/随机350bp/连接建库/PE150；PDF12泛指可索取，无MG编号。候选SI MH472967/OP218265为单菌partial16S最近参考序列，不归为本文MG项目。|
|R12562|宏基因组，新产生|PDF3给[PRJNA1369098](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1369098)；NCBI SRA及BioProject均count0，保留编号和状态2，不能据此推断不存在、未公开或受限。|
|R12985|宏基因组，既有公开数据复用|PDF19/21给[PRJNA1013451](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1013451)及21个BioSample，与R09236完全相同。官方21WGS/RANDOM/PAIRED/NovaSeq6000均公开；两文章共用1独立数据集，不重复计项目/run。|
|R13086|宏基因组，新产生|PDF3总DNA片段化/PE建库；4条件各一个多位置生物膜混样。PDF13泛指可索取，未给编号。LC-MS代谢组不是RNAseq。|
|R13274|宏转录组，新产生|PDF3发酵混合群落总RNA、混合细菌去rRNA/RNA文库/NovaSeq6000PE150。PDF11明确raw metatranscriptomic sequencing data可向通讯作者合理索取，需说明研究用途并签数据使用协议；无公共编号，不能标公开可下载。|

本批9目标文章：8新产生、1复用；**2篇有官方公开数据，只有1个新增独立公开项目（2个新增公开目标run）**。另1篇明确相关RNA数据可索取、4篇仅泛指可索取、1篇无编号/相关声明、1篇文中编号公开状态未核实。R11724的OTHER不擅改WGS，官方library source为METAGENOMIC的8个AMPLICON也不能作为宏基因组。所有官方原始响应保存在[batches/B007](batches/B007/)，[跨文章项目关联](batches/B007/project_article_relationships.json)记录去重。

R11751最初未加引号DOI查询被NCBI扩展为10.1021并返回1条，不是本文关联证据，未归任何编号；完整DOI加引号查询count0。所有DOI查询无结果均不证明没有数据。原始响应及解释保留。

## 50篇逐篇结论

|ID|结论|方法与核查要点|
|---|---|---|
|R10673|未使用目标测序|16S细菌/古菌扩增子（非目标）|
|R10714|未使用目标测序|16S扩增子及功能酶预测（非目标）|
|R10724|未使用目标测序|未报告测序；全规模脱硫/气体/运行监测|
|R10761|未使用目标测序|细菌/古菌16S扩增子MiSeq（非目标）|
|R10819|确认宏基因组|群落DNA shotgun宏基因组（新产生）|
|R10833|未使用目标测序|16S细菌/古菌扩增子（非目标）|
|R11041|未使用目标测序|未报告测序；微藻培养/光谱/电化学/氧化应激|
|R11094|未使用目标测序|16S V4 MiSeq扩增子＋qPCR/菌株培养（非目标）|
|R11099|未使用目标测序|16S细菌/古菌扩增子Illumina（非目标）|
|R11104|未使用目标测序|细菌/古菌16S扩增子（非目标）|
|R11168|证据不足，待确认|明确16S；KEGG功能基因/表达数据来源未说明，是否另有群落组学待确认|
|R11393|未使用目标测序|16S扩增子HiSeq2000（非目标）|
|R11421|未使用目标测序|细菌/古菌16S扩增子MiSeq（非目标）|
|R11477|未使用目标测序|16S扩增子＋PICRUSt2预测（非目标）|
|R11519|未使用目标测序|16S扩增子MiSeq＋PICRUSt预测（非目标）|
|R11534|疑似宏基因组，建库证据待确认|作者报告宏基因组/NovaSeq/ORF分析，但扩增与建库描述冲突|
|R11535|未使用目标测序|16S扩增子/克隆测序（非目标）|
|R11537|未使用目标测序|未报告测序；ETS活性/GC及理化|
|R11596|未使用目标测序|未报告测序；定义共培养/显微镜与GC/HPLC|
|R11655|未使用目标测序|细菌/古菌16S扩增子（非目标）|
|R11658|未使用目标测序|未报告测序；麦角固醇液相定量/LC-MS及GC|
|R11682|未使用目标测序|未报告测序；酶活显色/滴定、BMP及能量平衡|
|R11693|未使用目标测序|16S V4 MiSeq扩增子＋Tax4Fun2预测（非目标）|
|R11724|确认宏基因组|群落DNA宏基因组＋16S扩增子（新产生，分开标记）|
|R11751|确认宏基因组|群落DNA shotgun宏基因组（新产生）；宏转录组仅引用|
|R11843|未使用目标测序|16S V4 MiSeq扩增子（非目标）|
|R12127|确认宏基因组|群落DNA shotgun宏基因组绝对定量＋真菌ITS（新产生）|
|R12279|未使用目标测序|未报告测序；GC/HPLC/UV-Vis及工程监测|
|R12384|未使用目标测序|未报告测序；毒性/AMA/BMP及GC/HPLC|
|R12483|未使用目标测序|未报告测序；菌菇基质培养、纤维组分/DNSA/COD/BMP|
|R12509|确认宏基因组|群落DNA shotgun宏基因组（新产生；单菌16S身份另列）|
|R12562|确认宏基因组|群落DNA宏基因组（新产生；ARG 16S归一化非扩增子预测）|
|R12839|未使用目标测序|16S扩增子MiSeq＋PICRUSt2预测（非目标）|
|R12841|未使用目标测序|16S扩增子MiSeq/DADA2（非目标）|
|R12874|未使用目标测序|未报告测序；聚乳酸DSC/FTIR/黏度与BMP|
|R12923|未使用目标测序|分离菌株16S/ITS鉴定（非目标）；未报告群落组学|
|R12951|未使用目标测序|16S扩增子＋PICRUSt2预测（非目标）|
|R12953|未使用目标测序|16S扩增子＋PICRUSt/PICRUSt2预测（非目标）|
|R12957|未使用目标测序|细菌/古菌16S扩增子（非目标）|
|R12964|未使用目标测序|16S扩增子＋PICRUSt/FAPROTAX预测（非目标）|
|R12985|确认宏基因组|群落DNA shotgun宏基因组；复用同团队前作R09236公开数据|
|R13086|确认宏基因组|群落DNA shotgun宏基因组（新产生）；LC-MS代谢组另列|
|R13236|未使用目标测序|16S扩增子MiSeq＋PICRUSt2预测（非目标）|
|R13274|确认宏转录组|混合微生物群落RNA宏转录组（新产生）；16S/ITS另为扩增子|
|R13275|未使用目标测序|16S PCR扩增子HiSeq2000（非目标；作者误称metagenomic）|
|R13282|未使用目标测序|未报告测序；GC、纤维组分及工程监测|
|R13283|未使用目标测序|未报告测序；示范规模UASB/解吸气体/水质监测|
|R13293|未使用目标测序|16S V4 MiSeq扩增子＋PICRUSt2预测（非目标）|
|R13458|未使用目标测序|16S扩增子MiSeq＋PICRUSt2预测（非目标）|
|R13557|未使用目标测序|16S扩增子（非目标）|

## 待确认和相关限制

本批R11168：完整方法只明确16S，但Fig5报告功能/抗氧化基因丰度及表达，未说明这些数据来自预测、DNA shotgun或RNA建库；候选SI只有三图，不能推定阳性或阴性。R11534：正文委托已核实SI TextS7，声称NovaSeq/MEGAHIT/ORF/NR/KEGG，但同时说PCR与16S分析相同，缺随机DNA建库和可核对项目，保留疑似不计确认阳性。两项都没有完成时间，以screened_at保存筛查时间。

此前R01917、R05396、R06623继续待确认，未重筛。R12562属于文章已确认宏基因组、数据公开状态未核实，不能混成阴性或已定位受限项目。R10819阶段命名、R11751重复层级、R12985/R09236额外样本week标签差异均另列。R13275虽反复写metagenomic，具体方法为16S引物/amplicon library/OTU；R12964和R13293的gene expression/active genes按正文功能预测解释，不当宏转录组。

## 原件和附件覆盖

本批核验**86个原格式对象：51正文PDF（50篇，其中R11596有2个字节版本）＋35补充原件（DOCX28、PDF2、JPG3、ZIP1、XLSX1）**。R11596两个版本逐页规范化文字完全一致，但各自SHA解析分别保存，不覆盖或重复计文章。R12985 ZIP的4个XLSX成员均与既有派生文件同SHA，复用并记录ZIP成员谱系；这4件不重复计原件。90份源解析与人工核查说明均SHA绑定，旧search.sqlite不冒充覆盖本批新增文件。

正文完整方法逐篇阅读；DOCX读全部相关补方法、表头/图注及编号位置；XLSX检查全部非空单元格中的编号并读表头/样本列；PDF低文字图页原页已看，JPG三图原图已看，未把图片不可检索当阴性。本批无需新增OCR。R11751 SI以题名/作者/机构核实，R11843 DOCX以题名/完整作者/机构核实；其余候选附件保留身份限制，不能凭文件夹分配编号。目前全库55件附件唯一归属待核实；原库存/原分类不改。R12483为泰文原始实验研究，已读完整方法PDF5–8，非综述。R12509为青贮复氧研究，保留其原研究范围分类。

新增64条证据，累计378条；保留PDF从1起页码、章节和Word段落/工作表位置。R13274数据索取声明原文及条件保留，没有联系作者。

## 累计与续跑

范围426任务：341有核验正文的实际研究中**210完成、5待确认、126未开始**；另34研究缺正文跳过、51综述不适用。累计215研究已核查，含此前新增识别综述的已处理记录216。累计目标15文章＝14宏基因组＋1宏转录组，二者兼有0；14新产生、1复用。6篇官方公开目标数据、1篇明确相关测序数据可索取、6篇泛指可索取、1篇无编号/声明、1篇编号公开未核实。独立项目号6个（5个官方公开核实、1个公开未核实），唯一公开目标run31个；文章数与项目/run分开。

读取GitHub最新screening_records.json，取progress=未开始、按稳定ID顺序，后续默认20篇，用户指定数量优先；待确认项保留独立复核队列。下一批从**R13558**开始，接下来20篇：

R13558、R13671、R13683、R13691、R13737、R13816、R13817、R13818、R13819、R13820、R13821、R13822、R13823、R13824、R13825、R13826、R13827、R13831、R13832、R13833。

每篇先处理中，完整方法和上下文核查后即时保存；不确定不写完成时间。不重新检索、追下载缺件或下载reads。增量重建同一Excel/CSV并推送原结果分支；勿运行初始化覆盖累计结果。

历史回执：[B001](remote_readback.json)、[B002](batches/B002/remote_readback.json)、[B003](batches/B003/remote_readback.json)、[B004](batches/B004/remote_readback.json)、[B005](batches/B005/remote_readback.json)、[B006](batches/B006/remote_readback.json)。
