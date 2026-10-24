# 微曝气厌氧消化文献库、全文资源与后续研究

本项目从“**主动向厌氧消化（AD）系统引入少量氧气或空气，会怎样改变过程表现和微生物功能**”出发，逐步形成可追溯文献库、正文与补充材料原件库、期刊统计和群落测序方法审计，再扩展到跨体系氧响应机制与可复用测序数据发现。最初工艺检索与后来的机制/数据工作线范围不同，不能用后者的结果数量替代原AD库，也不能把文献数、原件文件数、项目数或测序run数混算。

**介绍整理日期：2026-10-25（Asia/Shanghai）。** 本次只恢复介绍与导航，没有新检索、重筛、修改人工判断/进度或重新下载/核哈希论文原件。以下每阶段标明对应结果快照，原方法、审计证据和新增详细方法均保留。阅读本页不需要展开任何折叠块。[仓库入口](../../README.md) · [章节恢复对照](method_audit/readme_restoration/chapter_map.md) · [运行历史附录](HISTORY.md)

## 目录

1. [最初的微曝气AD检索、校正、追溯与补检](#stage-1)
2. [全文、补充材料获取与原件整理](#stage-2)
3. [期刊与JCR统计](#stage-3)
4. [宏基因组／宏转录组全文方法筛查](#stage-4)
5. [厌氧环境氧暴露机制扩展检索](#stage-5)
6. [可复用测序数据与关联论文发现](#stage-6)
7. [成果导航、待完成工作与维护规则](#stage-7)

<a id="stage-1"></a>
## 1. 最初的微曝气AD文献检索：文献库怎样形成

### 研究目的、时间和工艺边界

初检于2026-10-06执行，发表范围为2012-01-01至检索当天；后续追溯/补检扩至2026-10-07。研究对象是**主动氧/空气输入**与AD、专门厌氧水解/产酸或服务于AD的独立预处理的关系，不限底物、反应器、供氧气相/液相或气泡形式。直接向消化器或内部循环供氧归类别1，专门厌氧水解/产酸供氧归2，独立好氧/微好氧预处理归3；综述为4，范围外记录为5，尚缺决定性范围事实时为6。

位置与阶段比“脱硫”“氨去除”等研究目标更重要：内部供氧脱硫可纳入，独立沼气净化/终端消化后好氧处理排除。明确有意设定的含氧处理与意外漏气不同；纳米气泡必须查气源，不能把N2/CO2气泡当供氧。CaO2等材料需区分实际分子氧释放与化学氧化/ROS，不因名称含氧就纳入。范围判断与全文可获取性独立：缺全文、剂量或DO细节本身不是排除理由。学位、会议、海报与期刊版本分列，内容相关不等于同一独立实验。按原边界，有意曝气后进入产甲烷的相关填埋模拟可保留，纯好氧稳定化不算；在线/正式年份及早期再版的差异另记，不把再版元数据当新实验。

### 实际技能、数据库与查询

按照 **nature-academic-search** 的多源检索与文献管理流程，实际使用OpenAlex、Crossref、PubMed，PMC补正文。初期有真实MCP检索与ID回查验证；系统发现查询主要通过官方API分页，避免小批调用返回上限。后续无可用学术MCP时也采用官方HTTP备用路径，不能把“安装了技能”当作每阶段MCP都成功。Semantic Scholar在后续定向补摘要时使用，不应倒写为初检的全面来源；WoS、Scopus、Embase、CNKI、万方没有完成检索。

检索将AD/发酵/水解/产酸/产甲烷词，与microaeration及连字符变体、microaerobic、controlled/limited/intermittent aeration、oxygen dosing/addition/supply、air injection/mixing、micro/nanobubble、aerobic pretreatment等分组组合。OpenAlex使用题名/摘要字段和cursor（200/页）；PubMed使用TIAB及日期、完整PMID列表和100条EFetch批次。Crossref初检采用4个单词标题查询并完整cursor分页，不能将其相关性匹配描述成等价布尔TIAB搜索。P5/P6等DOI/PMID补查用于补元数据，不重复计发现量。完整原式与限制见[方法01](methods/01_search_methods_zh.md)。

初期还按28个种子做前/后向引文检索；这与后来的43篇综述参考文献专项追溯是两个步骤。原多源返回归一化为13,817条唯一记录，经广义预筛及候选审查留下400条阶段文献库。这个400是当时保留记录，不是现行总量或所有返回已逐篇读过全文。

### 定向筛选、证据澄清与用户人工校正

224条待确认先用15条试审校准，再处理其余209条；补题名、摘要、相关Methods和必要流程图。保存的阅读层级为题名48、摘要161、相关全文定向核查14、海报1，**没有224篇全文通读的证据**。随后针对83条获取全文，并对80条重新核范围，纠正过高证据门槛、气路/阶段误解等；缺失的分类事实与仅缺剂量、版本或下载权限分开。

用户先提供28条分类，后在36候选表K列提供25条非空人工分类，共形成53条人工分类对象。按稳定ID同步，K非空优先、K空白11条沿用J，不按行号猜匹配；重复R13854通过别名归R01238。用户附件只有标签，不能把旧模型理由说成用户手写理由，也不推断其阅读深度。原自动判断和原始附件字节保留，人工分类不改变全文获取状态。证据分别在[方法02](methods/02_review_224_methods_zh.md)、[方法03](methods/03_evidence_clarification_zh.md)、[方法04](methods/04_download_review_methods_zh.md)、[方法05](methods/05_scope_reassessment_correction_zh.md)、[人工28同步06](methods/06_manual_classification_sync_zh.md)及[人工36同步09](methods/09_pending36_manual_sync_zh.md)。

### 综述引用追溯、漏检审计与两轮补检

为了发现标准“microaeration + anaerobic digestion”表达以外的研究，2026-10-07专项追溯原43篇综述。15篇取得完整可见参考列表、27篇只有部分Crossref引用、1篇没有列表，保存5,044条实际取得引用；不能称43篇综述全部通读或引用全部筛完。结合引用语境和原研究题名/摘要审查，最终形成58条净新增相关文献；另有重复、排除、早期研究和未决线索，详见[方法07](methods/07_review_reference_chase_zh.md)、[36候选复核08](methods/08_pending36_reaudit_zh.md)、[引用覆盖表](methods/audit/review_reference_tracking_43_utf8.csv)。

对这58条追查原返回/缓存发现：55条初始已返回却被预筛或候选规则排除，只有3条在保存材料中未找到匹配。已复现的问题包括漏独立aerobic/microaerophilic/air mixing、AD词序桥接不足、wine误中swine、按目标替代系统边界，以及学位/接种物预处理边界不一致。不能把全部漏收归为数据库没检到；未匹配3条的具体原因仍未知。没有用错误规则重新覆盖现有判断。

因此执行15组补充查询，并审查重点线索；再复用这些完整返回，增加5组digester及hydrolysis/acidogenesis“过程桥接”查询。这里不强制每条同时出现精确短语anaerobic digestion。后5组实际新增905条来源记录，确认新增49条文献，逐输入去重和范围证据均保存。详见[漏检与15组补检方法10](methods/10_omission_analysis_and_supplement_search_zh.md)、[5组继续检索方法11](methods/11_continued_search_and_screening_zh.md)及[实际查询表](methods/audit/continuation_search_log_utf8.csv)。

|有日期的形成阶段|当时主库|变化的含义|
|---|---:|---|
|2026-10-06 初检|400|后续校正以稳定ID和原证据续跑，不另建不相联库|
|2026-10-07 综述追溯/重复校正后|475|43综述追溯及36候选复核；重复合并和排除也保留审计身份|
|2026-10-07 人工同步后、15组补检|505|53人工判断保留；新增确认30条，不等于所有宽词结果已筛完|
|2026-10-07 过程桥接续检|554|新增49条；此后获取、JCR及组学任务未改原范围分类|

现存总表为**554条、133列**（后续追加获取/规范字段，不是新检索扩大文献数），类别1–6为208/57/111/50/128/0，范围任务1–4合计426。期刊、学位和其他非期刊分开。原库内类别6为0不代表库外没有疑点：仍有98条主库外范围候选、4条范围明确但元数据待核线索，以及10,107个旧/新返回身份未处理。不能把“查询分页结束”说成“所有返回筛尽”；这些队列与机制线的1,536条新范围池也不是同一集合。

<a id="stage-2"></a>
## 2. 全文与补充材料：从获取尝试到可取回原件

### 为什么单独核验下载和存储

范围相关不等于已取得正文，下载接口成功也不等于得到正确文件。项目先用 **nature-downloader** 处理定向候选，之后恢复 **ScanSci PDF 1.18.0** 的实际stdio MCP，并从公开出版商、PMC、合法仓储、机构授权及用户本地文件继续获取。代理CONNECT、目标站403/挑战、限流和机构认证未完成分别记录；某来源受阻不自动停止其他来源，也不索取学校密码。下载失败不证明无开放全文，未认证机构也不能判订阅不足；HTTP200还必须核文件内容。

早期Nature Downloader/ScanSci处理主要面向正文，不能因工具支持SI就声称已收齐补材。后续Windows请求明确启用`download_si:true`，并另行检查出版商/仓储附件及数据声明；该开关仍不保证每篇附件完整。补充材料保留PDF、Word、Excel、TXT、图片、ZIP等原格式；CSV、视频、代码等若实际遇到也应保留，不为展示编造已收文件。大型测序仓储先记链接/类型/大小，不当普通SI整库下载。

### 如何核正文、版本和附件

正文核题名、作者、DOI/年份、页面结构、Methods/Results/参考文献及版本。出版版、接受稿、学位和其他完整版本分别登记；同文不同字节不覆盖。摘要、会议一页摘要、海报、目录/搜索页、登录/错误页和作者变更表不计目标论文全文。R13968/R13969各7个分章组成一篇学位论文，不当7篇；会议论文集中的目标章节也不把整本当单独期刊文献。

附件检查文件能否实际打开及其文章归属；未检查、访问失败、未定位、明确无附件不能混为一类。ZIP原包与成员派生保留父子关系，不双计官方附件。库存与组学审计均保留未唯一归属的候选，目录名相同或“看起来相关”不足以完成身份核实。

### 本地与云端合并后的最新已存快照

2026-10-23合并本地439文件/295个ID与原云端234文件，按SHA256统一为**665个不同字节规范对象**；来源路径映射703行包含旧路径及30个历史main副本，不是703原件。沿用 `original_files/<ID>/fulltext/`、`supplementary/`、`abstract_poster/`、`uncertain/`、`evidence/`、`derived/` 等，不另建重复原件套装。

|2026-10-23核验口径|结果|解释|
|---|---:|---|
|目标全文|388个文献ID、402个正文文件|同文版本和分章导致文件数不同于文章数|
|缺目标全文|38个ID|仅摘要3、仅海报1、另缺正文34；不能将其全部称没有任何文件|
|科研补充材料原件|154个不同字节文件|DOCX109、PDF16、DOC9、XLSX9、JPG4、TXT4、ZIP3；另5个派生成员不重复计|
|归属限制|库存快照61件，后续组学审计报告52件待核|不同阶段/清单的归属状态尚需按源SHA对齐，不用相减推断已全部解决；原库存未被本次改写|

4个本地正文身份冲突和历史非目标候选留在uncertain，不计目标全文；R13964误放的同字节SI规范归R13834，旧来源保留。文件实际以普通Git blob持久保存于本私有结果分支，没有LFS指针；当次最大文件约27.32 MB。已有独立新克隆对665规范对象及工作簿大小/SHA/可读性核验的回执，本次不重复下载或核哈希。**环境本地路径、配置发布和只含表格的ZIP均不等于论文备份。**

原件与来源：[规范目录](original_files/) · [目录说明](original_files/README.md) · [665规范对象清单](inventory/merge_20261023/unified_files_utf8.csv) · [703来源映射](inventory/merge_20261023/source_path_mapping_utf8.csv) · [文件核验记录](inventory/merge_20261023/file_content_verification.json) · [已存远端读回](inventory/merge_20261023/remote_readback.json)。完整方法为[本地合并与身份核验21](methods/21_local_merge_and_jcr_20261023_zh.md)，较早下载/恢复的逐轮数量只在[历史附录](HISTORY.md)解释。

### 解析、Windows下载与回填

2026-10-15建立了PDF按页、JATS按章节、Word段落/表格、Excel工作表/单元格的解析与来源定位，扫描页按需OCR；图片/视频/模型不声称完成内容检索。该阶段54,387片段、229自动表格、907解析文件属于当时快照，**后来的388篇合并未重建全量索引**，不能将旧索引当覆盖全部现有原件。

[文件/解析标准18](methods/18_file_audit_and_fulltext_standard_zh.md)、[Windows流程](windows/README_zh.md)和[私有回传标准19](methods/19_private_storage_and_return_zh.md)保留可恢复下载、逐附件登记、按ID/SHA合并和原件不被提取文本替代的规则。Windows包装当时仅静态检查，不能称已在Windows实跑；旧337/317等队列和“私有存储未连接”是2026-10-15状态，不覆盖现有全量Git备份及[38条现行缺目标全文表](manual_review/current_environment_need_fulltext_utf8.csv)。新增本地文件须按当前清单复用再合并，不能照旧数量全量重下。

<a id="stage-3"></a>
## 3. 期刊与JCR统计：统一载体和指标口径

合并原件后，为回答“涉及哪些期刊、Q1覆盖多少、缺哪些指标”，2026-10-23核对DOI、刊名、ISSN及实际文献载体。规范字段与旧书目/范围分类分别保留：DOI注册元数据或索引中的“期刊”标签不直接等于已核实期刊论文，平台名、会议、技术说明和学位也不能混入同一分母。因此JCR的规范期刊分母不等于早期RIS中按原载体字段计算的数量。

采用**2024指标年／2025发布版**，逐JCR学科保留分区，不用中科院、SJR或JIF高低推断分区。主要依据已保存的武汉大学机构JCR栏目搜索索引快照；没有取得Clarivate账户完整导出，部分机构原页受网络限制。未知留空，不能当作非Q1；“全部已核实学科Q1”也不保证官方未显示学科均已覆盖。

|2026-10-23统计集合|已存结果|
|---|---|
|纳入范围内规范期刊论文|386条，JCR核实272（70.5%）、缺114|
|至少一个已核实学科Q1|213篇、28刊|
|全部已核实学科均Q1|201篇、25刊|
|已取得核验全文的期刊论文|369条，其中Q1为213；不与所有554记录混为分母|

[期刊/JCR Excel](final_results/journal_jcr_statistics_20261023.xlsx)包含文献明细、期刊汇总、统计汇总、逐学科分区、待核实与文件清单；[机器可读统计](inventory/merge_20261023/jcr_summary.json)、[待核实项](inventory/merge_20261023/jcr_pending_utf8.csv)与[方法21](methods/21_local_merge_and_jcr_20261023_zh.md)提供来源。下一步需同年份完整学科导出及载体疑点补证，本轮没有更新JIF。机制线后来按其更大期刊池复用缓存，412个文献匹配值是另一集合，不能覆盖这里的272/386。

<a id="stage-4"></a>
## 4. 宏基因组／宏转录组全文筛查：22篇如何确认

这一阶段为了从已有AD文献中找出真正使用群落shotgun DNA/RNA的研究，服务后续功能再分析，**不是看到metagenome、Illumina或KEGG字样就纳入**。宏基因组（MG）要求群落总DNA的非靶标测序或相应明确再分析，宏转录组（MT）要求群落RNA/cDNA策略；16S/18S/ITS、mcrA靶基因扩增、PICRUSt预测、PCR-DGGE、FISH、单纯基因定量及讨论/未来建议不计目标。纯培养/单细胞与病毒富集另列，不混群落集合。

按稳定ID逐篇读取方法、建库/样本、实际结果和数据声明；关键词只定位，还要看完整相关Methods、表/图和必要SI。没有命中也核方法，扫描/低文字页按需看原页；章节学位的证据落到真实分章与局部页码。每篇记录原文、页码、来源及明确不确定性；未公开编号不等于没做测序，只有项目号也不证明目标策略。R13944用HiSeq的16S/mcrA仍是扩增子，R13948的sequencing batch是反应器用语；这些实际案例见[累计筛查说明](omics_screening/README.md)。

B001–B010连续按批、按篇保存并推送。B010于2026-10-24（UTC+8）处理最后26篇，目标新增0，不能由前批命中多少推断后批结果。426范围任务最终为**333研究完成＋8策略待确认＋34缺正文跳过＋51综述不适用**；341篇核验正文研究全部进入过方法筛查，未开始0，8篇不能计阴性。51是实际筛查类型口径，包含后来识别的综述，不反改原AD分类。

确认目标**22篇＝21 MG＋1 MT，兼有0；21篇本研究产生、1篇既有数据复用**。当时8篇有官方公开目标数据、1篇明确reads可索取；另6篇只有泛指可索取、5篇未找到目标编号/声明、2篇有号但公开未核。9个项目号中7个当时官方公开，关联49唯一run；样本数/run数并非文章数。后续完整项目复核新增2个厌氧WGS，当前数据发现线为51，不能把49和51当同一时点冲突。

[累计Excel](omics_screening/omics_screening_cumulative.xlsx) · [逐篇判断](omics_screening/screening_records_utf8.csv) · [530条原文证据](omics_screening/evidence.json) · [项目/样本关联](omics_screening/data_projects_samples.json) · [批次](omics_screening/batches.json) · [8条及其他疑点](omics_screening/pending_related.json) · [B010核验/读回](omics_screening/batches/B010/remote_readback.json)。全文方法筛查不是所有文章从头到尾通读，也没有下载原始reads或联系作者。后续仍需解决8篇策略不明及附件身份，不能因为“未开始0”称全部确定。

<a id="stage-5"></a>
## 5. 厌氧环境氧暴露机制：从AD工艺扩展到机制证据

仅靠AD性能/组学可能不足以解释氧损伤、清除、防御与互作，因此2026-10-24增加独立机制范围：产甲烷/互营/发酵培养、严格厌氧菌、沉积物/湿地/土壤以及有可迁移机制的肠道等体系。原AD库排除的非AD研究也参与新范围判断。急性冲击、持续微氧、反复暴露和去氧恢复分别标记；分子O2与独立H2O2/ROS、化学调ORP分开，不能把不同情境合并解释。

实际执行PubMed 17组、Crossref 3组、OpenAlex 3组，并以2020年Bacteroides原研究为种子做有限前/后向追溯。完整过程、命中驱动扩词、阅读与判断方式、4个真实案例，以及Crossref各前100未补齐等限制，均在本次保留的[详细方法](oxygen_response_review/methods/METHODS.md)和[完整查询附表](oxygen_response_review/methods/QUERY_APPENDIX.md)。早期技能/MCP失败与官方API成功分开，不能与最初AD检索的成功验证混为同一次调用。

1,147是含重复返回行，映射为1,039个返回身份，其中57与原库重叠、982新增；原554全部保留，所以新范围池1,536，并非纳入数。[逐ID集合关系](oxygen_response_review/methods/flow_membership_utf8.csv)与原始返回可追溯，不凭数字相减猜来源。14项身份冲突与11组可能版本仍待核，不能视为独立研究。

首20按机制/体系分层选择，10读相关全文段落、10只读摘要；后来对其做五维精读评价，17推荐（其中8摘要暂定）、3暂缓。“范围符合17”与“推荐17”只重叠16，离体酶学与DAMO暂缓的区别已说明。原20以外1,516条完成的是**题名/摘要关键句初筛**：347候选、477待确认、336背景、356排除，不是完整摘要审阅；230条仍缺摘要。原17推荐与347新候选组成364暂定优先，累计待确认479；另1条DAMO范围相关但精读暂缓保留。

从347里按具体靶点/潜在干预和主题覆盖选择35篇阅读队列，后来补读了完整缓存摘要，但新增全文核实/严格独立验证均为0。它们不是指标前35、终选上限或已确认核心，其余312候选仍需核。AD相关性和具体证据优先，引用与JIF只辅助；同团队跟进、不同团队跨类群支持、反例与同对象严格复制分开，不能用被引量或综述重复引用替代独立验证。

[同一累计Excel](oxygen_response_review/oxygen_response_review_cumulative.xlsx) · [原20五维评价](oxygen_response_review/reading_priority/README.md) · [35逐篇来源/条件](oxygen_response_review/reading_queue35/README.md) · [主张验证关联](oxygen_response_review/reading_priority/mechanism_validation_links_utf8.csv) · [全池进度](oxygen_response_review/all_pool/progress.json)。这条线因切换数据发现已暂存；P001/P002当时显示片段未保存、P012错位更正、Europe PMC旧摘要与后来3篇成功正文并存等审计发现继续保留。后续应补具体摘要/方法与主张，不重复主题检索或把未核实说成无证据。

<a id="stage-6"></a>
## 6. 可复用测序数据与关联论文：从文章名单走向分析设计

为研究氧输入对群落/功能及潜在ARG、MGE、病毒与宿主的影响，数据发现先复用原22篇方法/数据证据和9项目号，再在ENA/BioProject直接检索，同时从PubMed/论文声明找项目、从项目Publication字段和论文→SRA关联反查论文。ENA执行16组、BioProject 4组、PubMed 4组加4组追溯；SRA承担项目号精确核验及关联，不冒称也完成同样一轮主题检索。未强制ARG/virus/MGE或统一发表年，以免漏掉可重注释的群落shotgun。

相关性分A（AD/产甲烷供氧核心方向）、B（其他厌氧环境氧响应）、C（无明确氧比较的参考背景）；**层次不代表设计已全部核实**。逐项目结合source/strategy、实验题名、建库及方法识别：有RNA-Seq实际是16S，也有WGS实际为MT。纯培养、扩增子、病毒富集、单细胞/WGA及仅组装数据分别记录，不拿MAG代替raw reads。

先规范项目别名及SRA/ENA镜像，再对项目—BioSample—Experiment—Run、处理/对照、时间、重复与文件入口做映射。同BioSample可有多个文库或混池，同实验多run可为分lane/技术重复，不能直接扩充生物学n；同一项目多论文或同实验拆多项目也不能当独立研究。剂量原单位、样本键冲突、DNA/RNA物理配对和深度未知均如实保留。

截至2026-10-24数据快照，连续审计旧9＋新增60＝69项目；38有公开目标群落reads清单，其中A5/B20/C13。A/B的25项目含349 run/261归档BioSample，C另333 run/280归档BioSample，不能合并推断氧效应。16项对比键中12有已读全文方法支持、4仅元数据暂定，共享研究/对照/反应器，不能称16独立实验。全部独立研究数和生物学样本总数仍未知。

7项目可准备后续文件获取：4个已有相关全文/样本键（AD的PRJNA1013451/1287080，扩展的551662/1163300），另3个RNA项目仍须补方法/重复/混杂。n=1、混池、不平衡及阶段变化使其未必适合有重复的差异检验。ARG/MGE/病毒分析还要看总DNA偏向、深度、宿主污染与组装；RNA不能代替DNA丰度，短reads共现不证明宿主或传播。

[详细方法与4案例](omics_dataset_discovery/methods/METHODS.md) · [全部实际查询](omics_dataset_discovery/methods/QUERY_APPENDIX.md) · [60项目顺序/来源](omics_dataset_discovery/methods/SELECTION_AUDIT.md) · [累计Excel](omics_dataset_discovery/omics_dataset_discovery_cumulative.xlsx) · [样本/run映射](omics_dataset_discovery/samples_runs_mapping_utf8.csv) · [逐项目可行性](omics_dataset_discovery/analysis_feasibility_by_project_utf8.csv)。

GSA只测试入口而被阻断，未执行数据库检索；FASTQ入口HEAD抽检被代理403，**公开清单不等于实际下载/校验FASTQ，本轮下载为0**。ENA E05已修复分页并全取1282；PubMed短语自动扩展的2125条完整保留但未筛为目标。487项目池中418未审计；论文续跑队列2,228行还漏排了12篇旧22已审计记录，原队列本次不改，应按ID/DOI/PMID联合清理后续跑。[身份重叠审计](omics_dataset_discovery/methods/queue_identity_audit.json)明确给出可定位ID，不称全部为新论文。

<a id="stage-7"></a>
## 7. 成果导航、未完成工作与后续维护

### 各阶段的现行入口

|阶段/资源|Excel、原件或机器可读结果|方法、导入与续跑|
|---|---|---|
|原AD文献库|[总Excel](final_results/ad_oxygen_download_review_20261006.xlsx) · [554条CSV](final_results/ad_oxygen_download_review_utf8.csv)|[methods/01–11入口](#stage-1) · [主库外98候选](manual_review/continuation_scope_candidates_utf8.csv) · [10,107未处理返回](manual_review/continuation_unprocessed_returns_utf8.csv)|
|原件与补材|[665规范对象](original_files/) · [库存Excel](inventory/unified_library_inventory.xlsx) · [原件清单](inventory/merge_20261023/unified_files_utf8.csv) · [来源映射](inventory/merge_20261023/source_path_mapping_utf8.csv)|[合并/核验方法21](methods/21_local_merge_and_jcr_20261023_zh.md) · [38缺目标全文](manual_review/current_environment_need_fulltext_utf8.csv) · [Windows回填](windows/README_zh.md)|
|期刊/JCR|[统计Excel](final_results/journal_jcr_statistics_20261023.xlsx) · [JCR统计JSON](inventory/merge_20261023/jcr_summary.json)|[缺指标/载体疑点](inventory/merge_20261023/jcr_pending_utf8.csv) · [方法21](methods/21_local_merge_and_jcr_20261023_zh.md)|
|MG/MT全文方法审计|[累计Excel](omics_screening/omics_screening_cumulative.xlsx) · [结论](omics_screening/screening_records.json) · [证据](omics_screening/evidence.json)|[B001–B010过程](omics_screening/README.md) · [批次/进度](omics_screening/batches.json) · [8待确认及相关线索](omics_screening/pending_related.json)|
|氧响应机制|[累计Excel](oxygen_response_review/oxygen_response_review_cumulative.xlsx) · [364暂定优先CSV](oxygen_response_review/all_pool/provisional_priorities_utf8.csv)|[详细方法](oxygen_response_review/methods/METHODS.md) · [查询附表](oxygen_response_review/methods/QUERY_APPENDIX.md) · [35来源与阅读深度](oxygen_response_review/reading_queue35/README.md) · [其余312候选](oxygen_response_review/reading_queue35/other_in_scope_continuation_queue.json)|
|测序数据/关联论文|[累计Excel](omics_dataset_discovery/omics_dataset_discovery_cumulative.xlsx) · [项目表](omics_dataset_discovery/data_projects_master_utf8.csv) · [文件入口](omics_dataset_discovery/raw_file_entry_manifest_utf8.csv)|[详细方法](omics_dataset_discovery/methods/METHODS.md) · [查询附表](omics_dataset_discovery/methods/QUERY_APPENDIX.md) · [下载准备](omics_dataset_discovery/download_preparation_priority_utf8.csv) · [续跑](omics_dataset_discovery/progress.json)|
|方法与运行证据|[上轮方法审计](method_audit/README.md) · [本次章节对照](method_audit/readme_restoration/chapter_map.md)|[有日期的运行历史](HISTORY.md) · [历史成果链接索引](method_audit/readme_restoration/source_link_index.md)|

### RIS与EndNote：全量和子集不是累加导入

原554条可用六个期刊分类RIS加学位/报告及其他非期刊共8个互斥分区；类别5仅审计，类别6为空。[期刊原始研究合并RIS](final_results/confirmed_original_research.ris)为类别1–3的替代方案；[追溯58](final_results/new_from_review_chase.ris)、[补检30](final_results/supplement_confirmed_new.ris)、[续检49](final_results/continuation_confirmed_new.ris)均已含总库，不与全量重复导入。期刊RIS的历史载体标签与JCR规范分母不同，详见第3节。

机制线[原17精读RIS](oxygen_response_review/reading_priority/priority_reading_set.ris)、[364暂定优先RIS](oxygen_response_review/all_pool/provisional_priority_set.ris)、[35新候选RIS](oxygen_response_review/all_pool/new_focus_set.ris)彼此有重叠，不是3个互斥集合。数据线[群落关联RIS](omics_dataset_discovery/community_dataset_papers.ris)与[全部关联候选RIS](omics_dataset_discovery/associated_papers.ris)也为替代子集；后者含特殊/待筛关联，不是全纳入。EndNote选择Reference Manager (RIS)及Unicode UTF-8，保留稳定ID并去重；没有声称已在用户Windows实际导入。

### 尚未完成的工作

- **原AD检索覆盖：**10,107返回身份未处理、98范围候选、部分综述引用和新综述追溯仍有缺口。保存材料能定位55条旧误排，但另3条未匹配的检出原因无法确定。
- **原件与解析：**38个ID缺目标全文，附件归属清单在库存/后续审计间尚需对齐；合并后未重建全部全文索引，旧扫描/自动表格未逐项人工校正。原始文件不能由提取文本替代。
- **期刊与组学：**JCR缺114条及完整学科信息；8篇测序策略待确认，缺正文/综述不计阴性。22目标论文不保证都有公开或可匹配分组的reads。
- **机制与数据：**35仍是阅读队列，479待确认及其余候选未核完，严格独立复制未确认；418项目未审计，2,228论文队列含12旧文重复，7项目下载准备也不等于有充分生物重复或FASTQ已取回。

**维护规则：**以后新增工作追加到对应研究阶段或新增章节，保留已有方法、用户判断和成果入口；不再把首页替换为最新任务或整体折叠原介绍。数量必须同时说明日期、集合和完成深度。方法/论文/原件变更分开记录，结果分支正常提交，不因介绍修复修改主分支、重筛或重下原件。
