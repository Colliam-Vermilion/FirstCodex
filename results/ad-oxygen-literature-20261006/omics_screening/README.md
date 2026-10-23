# 当前批次B010（进行中）

以最新远端f7ce38867为基准，最后26条未开始研究按ID顺序处理。已逐篇保存前12条R13938–R13954，均为非目标；剩余14条尚未开始，不记阴性。累计Excel/CSV/JSON已同步检查点。

[累计Excel](omics_screening_cumulative.xlsx) · [本批进度CSV](batch_B010_results_utf8.csv) · [逐篇检查点](checkpoint_log.jsonl)

# 群落宏基因组／宏转录组累计全文筛查

B009以GitHub最新提交`ef74a5e4c60f20b219d4013ac584698231f8f882`为基准，按稳定ID筛查R13880–R13937接下来的50条未开始研究任务：**48完成、2待确认；3宏基因组、0宏转录组、45非目标。** 原分类、人工判断、载体类型和旧批次结论保留。每篇即时保存；首20篇检查点`b2ddc70`已正常推送。

[同一份累计Excel](omics_screening_cumulative.xlsx) · [本批50篇CSV](batch_B009_results_utf8.csv) · [累计JSON](screening_records.json) · [累计CSV](screening_records_utf8.csv) · [证据](evidence.json) · [项目/样本/实验/run](data_projects_samples.json) · [待确认/相关线索](pending_related.json) · [统计](summary.json) · [批次](batches.json) · [逐篇检查点](checkpoint_log.jsonl)

## 本批目标研究及数据获取

|ID|实际测序与证据|数据获取与限制|
|---|---|---|
|R13884|新产生群落DNA宏基因组；PDF3§2.3.2随机Covaris200–400bp/NEXTFlex/Illumina，MG-RAST；SI表x1/y1独特三样本与正文PDF6引用核实归属|[PRJNA357876](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA357876)，官方SRP096931、3BioSample/6WGS实验和6public run，METAGENOMIC/RANDOM/PAIRED/HiSeq2500。原文TP-EBD:SRS192581缺末位，官方TPEBD1/2是SRS1925817；原值/规范值均保存。|
|R13904|新产生宏基因组＋16S（分开）；PDF5厌氧残渣总DNA/NovaSeq6000 PE150、MEGAHIT/MetaGeneMark/KEGG/CAZy/CARD，明确MG|唯一[PRJNA1347783](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1347783)紧随预处理16S PE250方法，官方仅3AMPLICON，不能当MG公开项目。全文13页、SI61段及所有图页未找到独立MG编号/相关索取声明。PDF11称“No datasets were generated or analysed during the current study.”与实验矛盾，原样保留；无编号仍纳入目标。|
|R13920|新产生群落DNA宏基因组；PDF3§2.3–2.4随机400bp/NEXTFLEX DNA接头建库、MEGAHIT/ORF/基因注释|文中[PRJNA1438379](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1438379)，官方SRA和BioProject准确编号均count0，保留为状态2，不能推断不存在/受限/未公开。PDF10仅泛指“Data will be made available on request.”，不标明确reads可索取。正文HiSeq2000与NovaSeq/HiSeqX试剂不一致，未擅自修正。|

R13884公开run：SRR5183016–SRR5183019、SRR5182962–SRR5182963，共6条；3样本每个有两run、相同spots，**不推为6生物重复或6独立样本**。SM-EBD接种物→SRS1925844/SAMN06161529；MP-EBD37°C→SRS1925843/SAMN06161530；TP-EBD46°C→SRS1925817/SAMN06161531。原文37°C第54天/46°C第75天描述保留，非供氧/无氧平行组。官方原始响应见[batches/B009](batches/B009/)，未下载reads或联系作者。

## 逐篇结论

|ID|进度|方法核查结论|
|---|---|---|
|R13880|已完成|未报告测序；酶活/F420和理化|
|R13881|已完成|未报告测序；光谱/GC-MS和生物毒性|
|R13882|已完成|16S V3–V4 MiSeq扩增子（非目标）|
|R13883|已完成|未报告测序；HPLC/GC/SEM/FTIR|
|R13884|已完成|群落DNA shotgun宏基因组（新产生）|
|R13886|已完成|16S rRNA/cDNA MiSeq扩增子＋PICRUSt2（非目标）|
|R13887|已完成|未报告测序；酶活/ETS和理化|
|R13888|已完成|16S PCR-DGGE克隆测序＋qPCR（非目标）|
|R13889|已完成|未报告测序；ICP/水质和产气|
|R13890|已完成|16S V3–V4 MiSeq扩增子（非目标）|
|R13891|已完成|细菌/古菌16S MiSeq扩增子＋FAPROTAX（非目标）|
|R13893|已完成|细菌/古菌16S PCR扩增子（非目标）|
|R13895|已完成|未报告测序；碱吸收甲烷/纤维化学|
|R13896|待确认|群落测序类型未报告，待确认|
|R13897|已完成|未报告测序；纤维/GC及响应面|
|R13898|已完成|未报告测序；GC/FTIR及能量平衡|
|R13899|已完成|未报告测序；渗滤液/气体化学监测|
|R13900|已完成|未报告测序；元素/气体及Gompertz模型|
|R13901|已完成|未报告测序；GC/FTIR及产气模型|
|R13902|已完成|未报告测序；NMR/GC/FTIR及吸水模型|
|R13903|已完成|未报告测序；DNS/GC及响应面|
|R13904|已完成|群落DNA宏基因组＋16S扩增子（新产生）|
|R13905|已完成|未报告测序；酶活/OUR及BMP|
|R13906|已完成|未报告测序；MPN培养计数与GC|
|R13907|已完成|未报告测序；二维GC和废物成分|
|R13908|已完成|未报告测序；二维GC/固体化学|
|R13909|已完成|未报告测序；填埋工程/水质和呼吸指数|
|R13910|已完成|未报告测序；BMP/氨吹脱及理化|
|R13911|已完成|16S 338F/806R Illumina扩增子（非目标）|
|R13912|已完成|未报告测序；GC/FTIR/XRD/SEM/SSA|
|R13913|已完成|16S V4及真菌ITS PCR扩增子（非目标）|
|R13914|已完成|16S rDNA Illumina测序＋功能估计（非目标）|
|R13915|已完成|16S 515F-Y/926R MiSeq扩增子（非目标）|
|R13916|已完成|未报告测序；ORP/DO动力学与GC|
|R13917|已完成|细菌/古菌16S Illumina扩增子（非目标）|
|R13919|待确认|群落DNA/MiSeq策略未明确，待确认|
|R13920|已完成|群落DNA shotgun宏基因组（新产生）|
|R13921|已完成|未报告测序；GC/ELISA及理化|
|R13922|已完成|16S 338F/806R MiSeq扩增子（非目标）|
|R13926|已完成|未报告测序；填埋气体/水质|
|R13927|已完成|16S PCR-DGGE条带克隆测序＋qPCR（非目标）|
|R13929|已完成|未报告测序；动态曝气/理化和GC|
|R13930|已完成|未报告测序；酶活/呼吸及GC|
|R13931|已完成|未报告测序；ICP-AES/气体水质|
|R13932|已完成|未报告测序；GC/COD分级和荧光|
|R13933|已完成|未报告测序；气体/渗滤液与PCA|
|R13934|已完成|未报告测序；吹脱/BMP与理化|
|R13935|已完成|古菌16S靶区NovaSeq扩增子（非目标）|
|R13936|已完成|未报告测序；Fenton/吹脱/BMP及理化|
|R13937|已完成|16S V3–V4 MiSeq扩增子（非目标）|

## 待确认、附件和队列校准

R13896：PDF4§2.4只说第36天菌群分析及引用[16]；PDF12§3.6称microbial sequencing，没有靶区、引物或随机建库/平台。PDF16泛指数据可向作者索取，不证明目标测序或原始reads。

R13919：PDF3§2.5仅DNA/MiSeq、引用Rollemberg2019及Mothur/群落统计；全文7页无16S靶区/引物/shotgun建库、项目号或相关索取声明。两篇均保留待确认，无完成时间，不作阴性。准确已知DOI官方SRA无结果仅作核对记录，不改变判断。

R13886为RNA→cDNA后的16S数据和PICRUSt2，不是宏转录组。R13891虽称metagenomic，实际338F/806R及古菌16S PCR/MiSeq/FAPROTAX，非MG。R13914功能基因是16S后的KEGG估计；R13912“sequencing batch”指序批式反应器。非目标PRJNA906293/PRJNA1056946/PRJNA1497691、SAMN10410857和DGGE参考序列均留排除说明，不计目标项目。

最终直接对照基线全部未开始队列，R13906虽然原载体类型待核实，仍应进入本批。已补查12页完整研究（PDF1标ICBAA会议、PDF2为培养MPN/GC/理化），保留原类型字段；原先顺延选入且尚未提交的R13938恢复未开始，本批严格50条，终点R13937。下一批从R13938继续。检查点保留真实完成顺序和时间，未伪造为ID排序。

本批68原格式源＝50正文PDF＋18补充原件（DOCX12、DOC6），共129,546,435字节，源大小/SHA与库存逐件校验；无ZIP，无新增原件副本。解析增量以当前源SHA绑定。6DOC用antiword解析，另用已有LibreOffice临时转PDF查看原嵌图；R13889 PDF34/35/37/38低文字页查看为流程/pH/VSS/产甲烷图；R13904/R13920全SI图页和R13912 pH图均已查看。见[38页/图的视觉出处](batches/B009/visual/provenance.json)，派生图不计原件。

R13884 SI用SM/MP/TP-EBD独特标签与正文Venn/表x1/y1引用核实归属，筛查层解决；全库仍53件附件唯一归属待核实。其他候选附件未凭目录分配编号。旧原库存、JCR、研究分类和main不改。

## 累计与交付核验

426任务中：341核验全文研究队列，**307完成＋8待确认＋26未开始**；另34缺正文、51综述单列。累计315研究已核查。目标22篇＝21MG＋1MT，兼有0；21新产生、1复用。8篇官方公开、1明确相关测序可索取、6泛指可索取、5无目标编号/相关声明、2文中编号公开未核实。独立目标项目号9个，其中7官方公开；唯一公开目标run49。本批新增3目标文章、1个官方公开项目及6run；未核实PRJNA1438379作为已有文中项目号单列，不标可下载。

本批新增57条源SHA/页码/章节绑定原文证据，累计495条。 [本批审计](batch_B009_audit.json) · [本地验证](batches/B009/local_validation.json) · [交付SHA清单](batches/B009/delivery_manifest.json) · [独立新克隆远端读回](batches/B009/remote_readback.json) · [源覆盖](source_coverage_audit.json) · [定位与人工上下文判定](batches/B009/term_hit_manual_dispositions.json)。最终回执核对交付文件和本批68原件真实字节大小/SHA，并打开远端Excel；回执对应的数据提交单独记录。

下一批起点**R13938**，默认20条：R13938、R13939、R13940、R13941、R13942、R13943、R13944、R13945、R13948、R13950、R13951、R13954、R13955、R13956、R13957、R13958、R13959、R13960、R13962、R13963。以最新提交进度取未开始项，类型待核实/学位/其他完整研究不因载体排除；待确认独立复核，用户指定数量优先。

历史：[B008交付说明](https://github.com/Colliam-Vermilion/FirstCodex/tree/ef74a5e4c60f20b219d4013ac584698231f8f882/results/ad-oxygen-literature-20261006/omics_screening)。
