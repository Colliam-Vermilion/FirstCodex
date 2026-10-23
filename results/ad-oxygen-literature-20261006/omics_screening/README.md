# 当前批次B007进行中（2026-10-23）

按远端fc718c1继续下一批50研究。已逐篇保存20研究：18完成、R11168/R11534待确认；确认宏基因组R10819，泛指数据可索取。未处理项不作阴性。累计表及JSON已更新；本批尚未结束。

# 群落宏基因组/宏转录组累计全文筛查

更新：2026-10-23，B006按GitHub最新进度顺序完成R06897–R10605的50篇未开始研究：**6篇确认宏基因组、44篇非目标；宏转录组0篇**。本批无新增测序类型待确认。6篇均为本研究新产生数据，未发现仅复用既有群落组学的研究。累计162研究完成、3研究待确认、176未开始；下一批从 **R10673** 开始，默认20篇。

- **[同一份累计Excel](omics_screening_cumulative.xlsx)**、[本批50篇CSV](batch_B006_results_utf8.csv)、[累计JSON](screening_records.json)、[累计CSV](screening_records_utf8.csv)、[证据JSON](evidence.json)、[证据CSV](evidence_utf8.csv)、[数据项目/样本/run](data_projects_samples.json)、[待确认/非目标线索](pending_related.json)。
- [累计统计](summary.json)、[批次进度](batches.json)、[逐篇检查点](checkpoint_log.jsonl)、[本批审计](batch_B006_audit.json)、[本地验证](batches/B006/local_validation.json)、[独立远端核验](batches/B006/remote_readback.json)、[交付文件SHA](batches/B006/delivery_manifest.json)。
- [SHA覆盖审计](source_coverage_audit.json)、[正文解析](parsed/)、[附件解析](parsed_attachments/)、[定位日志](term_location_log.json)、[目标词上下文解释](batches/B006/term_hit_manual_dispositions.json)、[低文字页原页核查](batches/B006/visual/provenance.json)。关键词仅用于定位，结论来自完整方法和上下文。

## 目标研究与数据获取

|ID|数据获取|独立原始数据项目|样本与限制|
|---|---|---|---|
|R07202|状态1：官方确认公开|[PRJNA565588](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA565588)|本文2个BioSample：SAMN13634953/954，对应SRR10742654/653；7个MAG主记录另列，非7个reads项目。论文PE125/日标签与官方SINGLE/文库名存在差异|
|R08462|状态5：仅泛指数据可索取，是否含reads不明|未定位编号|SMA stageIII供氧前/IV供氧后；原文PDF12“Data will be made available on request”，未明确原始测序数据|
|R09236|状态1：官方确认公开|[PRJNA1013451](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1013451)|21个公开WGS样本，核心12样本为4消化器×3时间，其余9为进料/初始/擦拭等；额外1个样本时间标签差异保留|
|R10163|状态1：官方确认公开，策略/映射需复核|[PRJNA1086167](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1086167)|正文结果PDF8列SRR28311681/682/683；681/683的作者处理对应与官方文库名相反；官方OTHER/MiSeq，论文NovaSeq/Hiseq|
|R10492|状态1：官方确认公开，混合测序逐run分开|[PRJNA1128434](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1128434)|目标Met run为SRR29552641/642/643；另6个AMPLICON非目标。A30/B30/C30尚未唯一对应DW/CO2NW/O2NW；官方OTHER/HiSeq2000与论文NovaSeq不同|
|R10605|状态5：仅泛指数据可索取，是否含reads不明|未定位编号|day30无曝气/微曝气条件；PDF11泛指“Data will be made available on request”。SI的RT-qPCR是real-time quantitative PCR，非RNA-seq|

文章数6与独立项目数4分开；4篇官方确认公开、2篇泛指可索取，**明确相关原始测序数据可向作者索取为0篇**。不能将泛指声明升级为状态4。R10163虽数据声明泛指可索取，正文结果提供了run，故仍定位并核实公开数据。OTHER不擅自改写为WGS：文章宏基因组类型由DNA打断/建库及分析方法确认，官方字段原样保留。

R07202另有WGS master JADLKJ000000000–JADLKP000000000及Figshare注释链接。7个Nuccore主记录与bin身份核实，MAG BioSample与2个原始reads BioSample分开；Figshare官方API被代理403阻断，访问未核实，不影响NCBI reads公开确认。所有官方原始响应在[batches/B006](batches/B006/)，未下载原始reads或碱基。R08462/R10605的已知DOI在SRA精确元数据查询count0，不证明无数据或未公开。

## 50篇逐篇结论

基准远端`2f43003d4cb9d75ded15be63ddd38c54f5380270`。严格选取接下来50条未开始研究，逐篇阅读完整方法及现有相关补方法后保存JSON、证据和检查点。前20篇以`e22d1b2`正常推送后继续余30篇。没有重筛此前已完成文章。新增68条证据，累计314条。

|ID|结论|测序类型或核查依据|
|---|---|---|
|R06897|未使用目标测序|16S PCR-DGGE切带再扩增测序（非目标）|
|R06979|未使用目标测序|未报告测序；GC/理化与Gompertz模型|
|R07039|未使用目标测序|16S rDNA扩增子HiSeq（非目标）|
|R07184|未使用目标测序|未报告测序；H2S/GC监测及AQUASIM模型|
|R07202|确认宏基因组|群落DNA shotgun宏基因组（新产生）；无实际宏转录组|
|R07238|未使用目标测序|未报告测序；流式细胞术/ATP/脂肪酶及理化|
|R07455|未使用目标测序|未报告测序；气量/GC及理化|
|R07641|未使用目标测序|未报告测序；AMPTS/BMP及元素/固体分析|
|R07903|未使用目标测序|未报告测序；组分/HPLC/GC分析|
|R07908|未使用目标测序|未报告测序；GC/ICP-OES/HPLC及运行分析|
|R07919|未使用目标测序|未报告测序；木质素/产气及动力学|
|R07952|未使用目标测序|16S扩增子MiSeq（非目标）|
|R08016|未使用目标测序|未报告测序；固体/水质/产气与能耗|
|R08280|未使用目标测序|16S细菌/古菌扩增子＋PICRUSt预测（非目标）|
|R08308|未使用目标测序|16S及真菌ITS扩增子MiSeq（非目标）|
|R08346|未使用目标测序|未报告测序；ETS生化活性及理化/GC|
|R08387|未使用目标测序|16S与真菌ITS扩增子MiSeq（非目标）|
|R08393|未使用目标测序|16S扩增子MiSeq＋PICRUSt预测（非目标）|
|R08456|未使用目标测序|细菌/古菌16S扩增子MiSeq（非目标）|
|R08462|确认宏基因组|群落DNA shotgun宏基因组＋16S扩增子/qPCR（分别标记）|
|R08552|未使用目标测序|未报告测序；产气/理化及五种动力学模型|
|R08665|未使用目标测序|16S扩增子MiSeq＋ARG/MGE qPCR（非目标）|
|R08877|未使用目标测序|SI明确16S V3–V4扩增子NovaSeq6000（非目标）|
|R08911|未使用目标测序|未报告测序；批次/连续AD、GC与动力学|
|R08977|未使用目标测序|未报告测序；硫形态/HPLC/XRF与工程监测|
|R09147|未使用目标测序|16S扩增子NovaSeq6000＋ADM1-Ox（非目标）|
|R09150|未使用目标测序|未报告测序；三厂全规模监测及硫平衡|
|R09217|未使用目标测序|16S细菌/古菌扩增子MiSeq（非目标）|
|R09230|未使用目标测序|PCR扩增子MiSeq（非目标）；PRJNA883421|
|R09236|确认宏基因组|群落DNA shotgun宏基因组（新产生；含病毒分类但非仅病毒组）|
|R09568|未使用目标测序|ARG/MGE及16S qPCR、耐药菌培养（非目标）|
|R09618|未使用目标测序|16S细菌/古菌扩增子MiSeq（非目标）|
|R09649|未使用目标测序|16S扩增子MiSeq（非目标）|
|R09902|未使用目标测序|未报告测序；自动气体传感/GC与回归|
|R10086|未使用目标测序|未报告测序；SMA/GC/HPLC及氧抑制计算|
|R10090|未使用目标测序|16S扩增子＋Tax4Fun预测（非目标）|
|R10097|未使用目标测序|未报告测序；热预处理/BMP/GC及能量计算|
|R10163|确认宏基因组|群落DNA shotgun宏基因组（新产生）；官方策略OTHER需保留差异|
|R10187|未使用目标测序|16S细菌/古菌扩增子MiSeq（非目标）|
|R10191|未使用目标测序|16S扩增子/qPCR＋LC-MS非靶向代谢组（非目标）|
|R10250|未使用目标测序|未报告测序；BMP/GC/UFLC与模型|
|R10290|未使用目标测序|未报告测序；现场气体/DO/ORP监测|
|R10300|未使用目标测序|16S V3–V4扩增子MiSeq（非目标）|
|R10372|未使用目标测序|未报告测序；填埋模型/气体与理化|
|R10377|未使用目标测序|未报告测序；HPLC/理化及定量图像QIA|
|R10383|未使用目标测序|未报告测序；电化学/DO/GC及动力学|
|R10492|确认宏基因组|群落DNA shotgun宏基因组＋细菌/古菌16S（新产生，分开标记）|
|R10525|未使用目标测序|16S V3–V4扩增子MiSeq（非目标）|
|R10586|未使用目标测序|16S细菌/古菌扩增子Illumina PE250（非目标）|
|R10605|确认宏基因组|群落DNA shotgun宏基因组＋16S/qPCR（新产生；无群落RNA-seq）|

PRJNA565588全项目另有2个公开WGS实验AD_Rep1/AD_Rep2，已作为数据库相关线索单列，是否用于R07202及能否与其微氧样本配对尚未证实；项目内12个扩增子BioSample与既有R04899相同，保留其原判断。见[文章—项目关联](batches/B006/project_article_relationships.json)。

## 待确认与数据质量限制

此前R01917、R05396、R06623保持待确认，未重筛、未标完成/阴性；新增数据质量线索不混成“未使用目标测序”。R07202、R09236、R10163、R10492的具体布局/平台/分组差异见目标表及相关线索表。R07202的2个微氧稳态样本不等于3反应器都有组学数据，Rep3 DNA降解未测。R09236核心12个纵向样本不等于每处理有3个独立反应器生物重复。

R09230 PRJNA883421、R09618 PRJNA935990、R10586 PRJNA1060892/PRJNA1060904为扩增子项目，保留在线索表；R09230官方20实验均AMPLICON。R10492项目中的6个16S实验/run放在数据明细但target_eligible=false，独立项目不重复计。

R06897虽写shotgun，实际是DGGE切带再16S PCR产物；R10300虽写whole microbiota genome，具体方法仍16S PCR；R10090功能来自Tax4Fun；R08393来自PICRUSt。R10191为16S/qPCR与LC-MS代谢组，不当作宏转录组。R08877的16S方法在SI PDF16，已实际阅读，未仅凭正文理化方法直接判阴性。

## 原件、补充材料与身份覆盖

本批重新核验50正文PDF＋27补充原件，共77对象：补充DOCX17、PDF4、XLSX3、ZIP2、JPG1。原字节/规范路径不变。R09236 ZIP内Sample key.xlsx与既有派生XLSX同SHA，复用派生文件，独立标记ZIP成员位置及工作表/单元格，不重复计原件；R07238 ZIP只有SketchUp模型，保留成员谱系，未声称渲染CAD模型。

两个附件在筛查层新增核实唯一关联：R07202 DOCX的两个独有BioSample及reads/contigs统计与正文TableS1逐项相同；R08280 DOCX题名/完整作者/机构与正文相符。新增身份依据及历史待核实项的解决记录均保留，原库存字段不改；其余附件独立身份限制保留，当前余57件唯一身份待核实，不能凭文件夹归编号。

DOCX核查相关补方法、全部表头/图注及编号位置；XLSX以工作表/单元格保留，候选表不凭位置分配编号；PDF补充方法阅读全文。低文字页原图已检查：R08665 SI装置/结果图、R10492图、R10086末页空白。R09649 PDF10–11附2026 Corrigendum，仅澄清经济性/可持续性表述，无新增测序；单列证据，不新增研究任务。R10383候选JPG已看原图，为电化学曲线；其身份限制保留。本批无需新增OCR，未将图像页不可检索视为阴性。

范围426任务：341有核验正文的实际研究中162完成、3待确认、176未开始；另34研究缺正文跳过、51综述不适用（含4缺正文，B002新增识别R00915仅在筛查层单列）。累计165研究已核查，含1新增识别综述为166个已处理记录。原554行总库、人工分类、JCR及main保持。

## 续跑

读取GitHub最新screening_records.json，取progress为未开始、按稳定ID排序的接下来20篇；用户指定篇数优先。下一批从 **R10673** 开始，当前接下来20篇：

R10673、R10714、R10724、R10761、R10819、R10833、R11041、R11094、R11099、R11104、R11168、R11393、R11421、R11477、R11519、R11534、R11535、R11537、R11596、R11655。

每篇先写处理中，完整方法及上下文核查后即时保存；不确定保留待确认和screened_at，不能写完成时间。每批重建同一Excel/CSV，正常提交原结果分支并独立新克隆读回大小/SHA和Excel。勿运行初始化覆盖累计结果。scan_parsed.py仅定位，build_outputs.py仅重建表格。不开新文献检索、不追下载缺失正文、不下载reads、不联系作者，不按期刊/JCR限制。

历史回执：[B001](remote_readback.json)、[B002](batches/B002/remote_readback.json)、[B003](batches/B003/remote_readback.json)、[B004](batches/B004/remote_readback.json)、[B005](batches/B005/remote_readback.json)。
