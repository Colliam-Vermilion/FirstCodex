# 群落宏基因组／宏转录组累计全文筛查

B008以GitHub最新基准`fc81882d43dea97732de61d90aa3a8b1f0cd4401`，按稳定ID选取R13558–R13879接下来的50篇未开始研究。**49完成、R13834待确认；4宏基因组、0宏转录组、45非目标。** 每篇保存JSON/证据/检查点；前20篇已以`211f863`正常推送。原分类、人工判断及已有结果保留；未重新检索文献、追下载缺全文或下载reads，未联系作者。

[同一份累计Excel](omics_screening_cumulative.xlsx) · [本批50篇CSV](batch_B008_results_utf8.csv) · [累计JSON](screening_records.json) · [累计CSV](screening_records_utf8.csv) · [证据](evidence.json) · [数据项目/样本/实验/run](data_projects_samples.json) · [待确认/线索](pending_related.json) · [统计](summary.json) · [批次](batches.json) · [逐篇检查点](checkpoint_log.jsonl)

## 本批目标研究和数据获取

|ID|类型与证据|数据获取|
|---|---|---|
|R13671|新产生宏基因组；正文PDF3和核实SI MethodsS1段38；DNA PE/NovaSeq6000、MEGAHIT/ORF/ARG-OAP|PDF8列3个BioProject，官方仅[PRJNA1447957](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1447957)为12WGS/METAGENOMIC/PAIRED/NovaSeq6000，12实验和12run均public。另PRJNA1447972/PRJNA1448473各24AMPLICON，虽原文统称MG，排除目标统计。|
|R13817|新产生宏基因组＋宏蛋白组，非MT；PDF3–4和SI§1.5段31–34；DNA/MAG|正文PDF13明确“The authors do not have permission to share data.” 无编号；未标公开或可索取。未定位存储项目，不能冒用“已定位受限项目”。|
|R13856|新产生宏基因组；PDF3与核实SI TextS1段12–21；随机400bp/NEXTflexDNA连接/NovaSeq/MEGAHIT|全文12页和SI904段未找到编号或相关数据索取声明；目标研究保留。|
|R13866|新产生宏基因组；PDF4§2.4，Covaris400bp/NEXTFLEXRapidDNASeq/NovaSeqPE|全文11页及核实SI7页未找到编号或相关索取声明；目标研究保留。双反应器消化液混合后测序，不作为2个独立测序重复。|

R13671公开目标run为SRR37918003–SRR37918014，样本/实验逐行保留。官方库原始代号CZ/CN/ZZ/ZN尚未与文中MN/MD/PN/PD唯一对应；扩增子21/35天与正文21/49天不一致，正文0/21/49天与SI21/49天差异也保留。不能凭编号或排序推定供氧组/温度。BioSample按已知项目检索count0未补足映射，不影响SRA已公开WGS核实。所有官方原始响应见[batches/B008](batches/B008/)。对其余目标研究的完整已知DOI官方SRA查询count0，不证明没有数据。

## 逐篇结论

|ID|进度|结论与方法依据|
|---|---|---|
|R13558|已完成|未报告测序；GC/HPLC/水质及工程监测|
|R13671|已完成|群落DNA宏基因组＋16S扩增子（新产生，分开标记）|
|R13683|已完成|16S V3–V4 NovaSeq6000扩增子＋PICRUSt2预测（非目标）|
|R13691|已完成|细菌/古菌16S及真菌ITS扩增子（非目标）|
|R13737|已完成|细菌/古菌16S及真菌ITS扩增子（非目标）|
|R13816|已完成|16S V4 MiSeq扩增子＋PICRUSt2预测（非目标）|
|R13817|已完成|群落DNA宏基因组＋宏蛋白组（新产生；非宏转录组）|
|R13818|已完成|未报告测序；GC及水质/硫化物工程监测|
|R13819|已完成|古菌16S克隆文库/毛细管测序（非目标）|
|R13820|已完成|未报告测序；GC-MS/SEM/水质和代谢活性|
|R13821|已完成|未报告测序；真菌培养/酶活与GC/HPLC|
|R13822|已完成|16S PCR扩增子Illumina（非目标）|
|R13823|已完成|未报告测序；BHP/BMP、GC及物质平衡|
|R13824|已完成|未报告测序；橄榄废水理化/多酚及产气|
|R13825|已完成|未报告测序；污泥水解/蛋白糖/产气|
|R13826|已完成|未报告测序；GC/BMP与动力学模型|
|R13827|已完成|未报告测序；两阶段产气/气相色谱/理化|
|R13831|已完成|16S V4–V5 MiSeq扩增子（非目标）|
|R13832|已完成|16S V3–V4 MiSeq扩增子（非目标）|
|R13833|已完成|16S MiSeq扩增子＋菌株16S Sanger/DGGE（非目标）|
|R13834|待确认|群落DNA/MiSeq分析，扩增子还是shotgun未说明|
|R13836|已完成|16S V4 MiSeq扩增子（非目标）|
|R13837|已完成|未报告测序；HPLC/GC/离子色谱与工程监测|
|R13838|已完成|未报告测序；元素/纤维/GC及产气|
|R13840|已完成|16S V3–V4扩增子＋宏蛋白质谱（非目标）|
|R13841|已完成|未报告测序；TGA/GC/理化与产气|
|R13842|已完成|古菌16S V4–V5 PCR扩增子（非目标）|
|R13843|已完成|未报告测序；SSAD/BMP/GC/HPLC及实验设计|
|R13844|已完成|未报告测序；菌剂/产气和氨激光光谱|
|R13845|已完成|细菌/古菌16S扩增子MiSeq（非目标）|
|R13850|已完成|未报告测序；工程水质/GC/SMA|
|R13851|已完成|16S V3–V4 MiSeq扩增子（非目标）|
|R13853|已完成|未报告测序；污泥臭气/ORP/GC及嗅辨|
|R13855|已完成|16S V3–V4 MiSeq扩增子（非目标）|
|R13856|已完成|群落DNA shotgun宏基因组＋16S扩增子（新产生）|
|R13857|已完成|16S V3–V4 iSeq100扩增子（非目标）|
|R13859|已完成|未报告测序；GC/脱硫/CFD模型|
|R13860|已完成|16S V3–V4 PCR扩增子（非目标）|
|R13861|已完成|16S PCR-DGGE（非目标）|
|R13862|已完成|未报告测序；定义菌共培养/GC/HPLC与显微镜|
|R13863|已完成|未报告测序；飞灰/预处理/VS-COD与产气|
|R13864|已完成|16S MiSeq扩增子（非目标）|
|R13866|已完成|群落DNA shotgun宏基因组（新产生）|
|R13868|已完成|16S rRNA基因MiSeq测序（非目标）|
|R13871|已完成|未报告测序；学位研究的气液传质/产气/CFD与比色|
|R13875|已完成|未报告测序；GC/HPLC/污泥工程监测|
|R13876|已完成|未报告测序；纤维/GC/HPLC与能量模型|
|R13877|已完成|16S PCR-DGGE及条带序列分析（非目标）|
|R13878|已完成|16S V3–V4 MiSeqPE300扩增子（非目标）|
|R13879|已完成|未报告测序；SEM/XRD/GC与经济分析|

## 待确认、附件和解析限制

R13834完整方法仅写DNA提取、MiSeq和引用他文方法；当前正文与已归属SI缺靶区、引物、shotgun建库及编号。MiSeq/OTU不足以判定16S或宏基因组，保留待确认，没有完成时间，未作阴性。此前5项R01917/R05396/R06623/R11168/R11534保持待确认，未重筛。

R13840虽在结果PDF13/15写metagenome，实际方法PDF4–5为16S扩增子，SI TextS3段32为胰酶处理/蛋白质谱/PEAKS，蛋白fold-change不算DNA/RNA测序。R13683功能expression/upregulated实为PICRUSt2；R13877为16S-DGGE和单菌SDS-PAGE，非MT。

本批77原格式对象＝50正文PDF＋27补充原件（DOCX19、PDF5、XLSX2、DOC1），共220,268,470字节；没有ZIP或新增原件副本。275页R13871学位论文完整Chapter3 PDF74–113及附录PDF272–275、相关实验/CFD章节方法已查，为气液传质、产气和COD/VFA比色，无核酸测序。R13878原DOC用现有antiword重新解析，题名作者及属丰度表核查。

R13879 SI字体编码异常，已查看原页：装置/日产甲烷两图，不将文本无命中当阴性。R13826/R13860/R13866低文字图页及R13832两DOCX的3WMF＋JPEG/PNG嵌图均查看，见[视觉出处](batches/B008/visual/provenance.json)。R13816 SI按题名、作者全名单和机构核实，筛查层解决归属；其余候选附件保留限制，全库54件唯一归属待核实。不按目录归属项目号。原库存、分类、原件与main未修改。

## 累计、核验和续跑

累计426任务：341有核验全文研究中259完成、6待确认、76未开始；另34缺正文、51综述单列。累计265研究已核查。目标19篇＝18MG＋1MT，兼有0；18新产生、1复用。7篇官方公开、1明确相关测序数据可索取、6泛指数据索取、1篇文中编号公开未核实、4篇无编号（其中R13817明确无共享权限）。独立目标项目号7个，其中6个官方公开核实；唯一公开目标run43。本批新增1个独立公开目标项目/12run，非目标扩增子不混入。

新增60条源SHA绑定原文证据，累计438条，保留PDF页码/章节或附件段落/工作表位置。[本批审计](batch_B008_audit.json)、[本地验证](batches/B008/local_validation.json)、[独立远端读回](batches/B008/remote_readback.json)、[交付SHA清单](batches/B008/delivery_manifest.json)、[源覆盖](source_coverage_audit.json)、[定位与人工上下文判定](batches/B008/term_hit_manual_dispositions.json)。

下一批起点**R13880**，接下来20篇：R13880、R13881、R13882、R13883、R13884、R13886、R13887、R13888、R13889、R13890、R13891、R13893、R13895、R13896、R13897、R13898、R13899、R13900、R13901、R13902。以GitHub最新screening_records.json的未开始项按稳定ID继续；用户指定数量优先。不重筛已完成项，待确认独立复核。

历史：[B007说明和交付](https://github.com/Colliam-Vermilion/FirstCodex/tree/fc81882d43dea97732de61d90aa3a8b1f0cd4401/results/ad-oxygen-literature-20261006/omics_screening)。
