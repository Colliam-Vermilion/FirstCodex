> 阶段方法快照：下文中的数量和旧文件名属于该阶段，不是当前交付目录。旧交付文件已由最终版替代，可通过清理前提交 `af86f8c303c4b0a385f7a07f6fa23184ecdf55e1` 追溯。当前文件导航、最终数量及导入方案见 [README](../README.md)。文中运行环境路径仅是证据来源位置，不是下载链接。

# nature-downloader：83篇定向全文获取与筛选更新

执行日期：2026-10-06。仅处理此前确定的83条候选，不开展新的主题检索。实际读取完整技能SKILL.md、README、机构浏览器工作流和交付/失败说明，以用户“必要补充材料”要求作为SI选择，调用始终使用--si。未提供出版商付费凭据，按用户指定出版商OA→PMC/合法仓储/作者稿→HKUST机构入口顺序处理。

## 环境与工具能力

- Node 24.19、Python 3.12、pypdf、pdfplumber、PyYAML、jsonschema及pdftotext可用；下载脚本语法检查通过。设置NODE_USE_ENV_PROXY=1使用当前网络代理。下载确实通过nature-downloader的batch_download.mjs完成，另以pypdf核验内容。
- Chromium及Playwright已存在，但无可由用户交互操作的浏览器控制通道；127.0.0.1:3456和:9222均连接拒绝。不能接入或复用用户本机HKUST/Fudan登录会话，因此不尝试收集密码、MFA码、Cookie或令牌。
- 学校入口只保存于运行环境内独立config目录，来自可读取的HKUST官方EZProxy说明，不写入仓库。没有保存任何机构账号配置或认证信息。
- Unpaywall需要联系邮箱：本轮未启用该查询，已询问是否可复用PubMed联系邮箱但未据此自动配置。它不妨碍已可用的PMC和已知合法入口，但限制额外OA发现。

## 首批5篇测试

|ID|入口与结果|
|---|---|
|R04350|出版商OA/MDPI公共PDF，18页，题名、作者与DOI核验成功|
|R01853|出版社重定向CONNECT被拦截；NTU返回HTTP405 Human Verification，未获正文|
|R04700|TU Delft官方仓储公开PDF，51页，核验为Additional Thesis|
|R08127|出版商公开PDF，21页；与前轮SHA256相同，重下载对照|
|R10714|出版社CONNECT拦截；Cranfield HTTP403 Just a moment，未获正文|

测试下载、内容验证和错误分流后继续处理全部83条。两条后台I/O工作线程用于元数据和公开入口；没有批量打开机构登录标签。已保存每篇进度；工具输出、原始响应、PDF/提取全文及配置均在Git仓库外。

## 下载与核验结果

- 新获4篇期刊全文：R04350、R08069、R10372、R11658；新获1份学位论文：R04700；另重新下载前轮已有R08127。六个不同ID的完整PDF均有%PDF头、非零页数及可读正文，完成题名/作者/DOI身份核对；无DOI和PDF未印DOI的情形明确标注。
- R11658原记录作者缺失，依据出版商PDF首页及页眉补齐五位作者、期刊1(4)及pp.38–42，再核验题名与DOI。R04700为学位论文，不冒充出版版本/接受稿/预印本；R08069原DOI在Crossref及doi.org均404且PDF首页未印DOI；新版本DOI字段留空，原值保留原DOI列，不声称已核实。
- R11845下载的是第7届WASTES会议的一页摘要，记录其会议与p.48，未计作论文全文。R05473为一页研究海报，也未计作全文。下载状态表保存这两类文件路径及身份说明。
- 标记为出版版本的文件均有相符期刊版式与书目数据。本轮没有取得可确认的作者接受稿或预印本；未核实的版本不会猜测。
- 主文献判定是全文定向核查，并非逐页完整通读。核查Methods、装置/流程图与相关结果；R04700 Fig.3.1/3.2、R10372 Fig.1、R11658 Fig.1已视觉检查。

## 六份完整PDF的定向判断

### R04350 — Temperature-Phased Biological Hydrolysis and Thermal Hydrolysis Pretreatment for Anaerobic Digestion Performance Enhancement

- 版本：出版版本
- 阅读范围：PDF/正文pp.3–4，Materials and Methods 2.2 Bench-Scale Sludge Hydrolysis Pretreatment、2.3 Biological Methane Potential Test；p.6 Results 3.2
- 判断：5 排除；Methods 2.2明确水解瓶冲氮并用气密盖密闭，2.3的BMP同样冲氮密封；生物水解由温度分相控制，热水解为165°C加热。没有以空气/分子氧输入为干预的实验，故排除；氧仅出现在气相色谱标准组成。
- 定位摘录：The BH experimental steps included filling the combined sludge in two-liter plastic bottles, flushing the mixed sludge for one minute using nitrogen (N 2) gas, capping the testing bottles with airtight lids, placing the capped sludge-filled bottles in the incubators at preset temperatures, and shaki…
- 缺失/待确认：无范围疑点；未取得全部补充材料。
- 来源：https://www.mdpi.com/2073-4441/10/12/1812/pdf?version=1544784645
- 本地PDF：`/workspace/ad-oxygen-review/download-round-20261006/downloads/R04350/publisher-1/PDFs/Temperature-Phased_Biological_Hydrolysis_and_Thermal_Hydrolysis_Pretreatment_for_Anaerobic_Digestion_Performance_Enhancement.pdf`

### R08069 — Model-based analysis of microaeration for biogas desulfurization using a biomembrane

- 版本：出版版本（有期刊版式、卷期、文章编号及出版日期）
- 阅读范围：PDF/正文pp.1–2，Introduction末段、Materials and Methods: Lab-scale biomembrane set-up、Pilot-scale biomembrane set-up、Modelling biomembrane-based microaeration；p.5 Simulation set-up及Results；pp.10–11 Conclusions
- 判断：5 排除；Introduction及Methods明确用2017/2018已发表实验数据校准、验证模型；被建模装置以合成沼气在膜外流动、空气在膜内流动，并非向AD反应器/内部循环供氧。本研究为模型分析，无新增目标供氧实验，因此排除；原始实验引用仅供后续追溯，不据此自动改判其他记录。
- 定位摘录：MATERIALS AND METHODS Lab-scale biomembrane set-up Data from Pokorna-Krayzelova et al., [13] Were used to validate the model of hydrogen sulfide removal in a lab-scale biomembrane reactor.
- 缺失/待确认：SI在正文被引用但未取得；排除依据不依赖SI。原DOI在Crossref及doi.org均404，PDF首页未印该DOI；新版本DOI字段留空，原值保留在原DOI列，不能声称已核实。
- 来源：https://biblio.ugent.be/publication/01KKBWHJNN2VYJ09JTHVHMET5M/file/01KKBWQY3Y6Q316VHE9DPEZS6R
- 本地PDF：`/workspace/ad-oxygen-review/download-round-20261006/downloads/R08069/repository-1-1/PDFs/Model-based_analysis_of_microaeration_for_biogas_desulfurization_using_a_biomembrane.pdf`

### R10372 — Influence of Aeration, Introduction of Probiotics, and Supply of Water on Landfill Gas Production—Study of Models

- 版本：出版版本
- 阅读范围：PDF/正文pp.3–5，Materials and Methods、Fig.1（已视觉核查）、Tables 1–2；pp.8–10 Results 3.4–3.6
- 判断：6 仍待确认；Methods、Fig.1和Tables 1–2确认五个19 L模拟填埋反应器，3–5组主动供空气，4/5组在同一器内好氧–厌氧处理；因此主动操作和设备边界疑点已解除。但研究以模拟填埋稳定化为背景，不是明确的AD或专门厌氧水解产酸工艺，不能仅凭甲烷生成把填埋模型等同AD。保持类别6，待确认模拟填埋体系是否符合既定AD/相关厌氧过程范围，不擅自扩大范围。
- 定位摘录：The third, fourth, and fifth landfill models that required aeration were additionally equipped with aerators.
- 缺失/待确认：范围边界：是否将以填埋稳定化为目标的好氧–厌氧模拟体系视作AD/相关厌氧过程。正文已取得，无需再下载同一文件；如明确属于范围，供氧位置对应类别1。气量/气源文字有内部不一致，另行注明而非以剂量缺失阻碍判断。
- 来源：https://www.mdpi.com/2227-9717/12/9/1859/pdf?version=1725083301
- 本地PDF：`/workspace/ad-oxygen-review/download-round-20261006/downloads/R10372/publisher-1/PDFs/Influence_of_Aeration,_Introduction_of_Probiotics,_and_Supply_of_Water_on_Landfill_Gas_Production—Study_of_Models.pdf`

### R11658 — IMPACT OF MICRO-AERATION ON FUNGAL COMMUNITY FROM ANAEROBIC DIGESTION

- 版本：出版版本（期刊1(4)，pp.38–42，2024；PDF首页题名、五位作者及DOI已核验）
- 阅读范围：PDF第2–4页（正文pp.39–41），Materials and methods、Fig.1（已视觉核查）、Results and discussions及Table 1、Conclusions
- 判断：2 向厌氧水解或产酸阶段供氧；Methods明确两阶段半连续中温AD，水解段分别运行无氧、超微曝气范围及三档微曝气剂量；Fig.1为双反应器装置照片，Results/Table 1报告各供氧阶段水解、甲烷及真菌指标，因此不是仅计划或会议摘要。主动供氧位于专门水解阶段，纳入类别2。
- 定位摘录：The experimental conditions evaluated different dissolved oxygen dosing conditions in the hydrolytic reactor.
- 缺失/待确认：Methods的4.7与Table 1的4.8剂量不一致；气源、每档运行时长及SI待补。缺失参数不阻碍范围纳入。
- 来源：https://bsuj.bsu.edu.az/readpdf.php?file=236e3d6763a43f726c9814e7b5de8bc1.pdf
- 本地PDF：`/workspace/ad-oxygen-review/download-round-20261006/downloads/R11658/publisher-1/PDFs/IMPACT_OF_MICRO-AERATION_ON_FUNGAL_COMMUNITY_FROM_ANAEROBIC_DIGESTION.pdf`

### R04700 — Effect of aeration by micro - bubbles on methane production in anaerobic digestion

- 版本：其他：学位论文/Additional Thesis；不是期刊出版版本、作者接受稿或预印本
- 阅读范围：PDF第1–3页（学位论文身份与摘要）、第14–21页（正文pp.7–14），Materials and Methodology 3.1–3.3.3；Fig.3.1/3.2已视觉核查
- 判断：6 仍待确认；首页明确为Additional Thesis。Methods 3.3.1–3.3.2及Fig.3.1/3.2确认先以3/5 bar空气白水在独立柱中处理接种污泥，再用其作BMP接种物，供氧位置疑点已解除，内容范围对应独立预处理。当前记录是学位论文，尚未定位正式研究文章，仍以类别6保留发表版本疑点，不因无剂量或未取得全文而待确认。
- 定位摘录：This pressurized air is allowed to flow for 5 - 10 minutes and then the pressure vessel inlet valve is closed.
- 缺失/待确认：仅需寻找/核对正式文章版本；若允许将学位论文作为独立灰色文献，可按内容归入类别3并保持THES类型。
- 来源：https://repository.tudelft.nl/file/File_d8b73973-6e26-4f66-9162-3212f6b93431
- 本地PDF：`/workspace/ad-oxygen-review/download-round-20261006/downloads/R04700/repository-1-1/PDFs/Effect_of_aeration_by_micro_-_bubbles_on_methane_production_in_anaerobic_digestion.pdf`

### R08127 — ORGANIC REMOVAL IN DOMESTIC WASTEWATER USING ANAEROBIC TREATMENT SYSTEM-MBBR WITH FLOW RECIRCULATION RATIO AND INTERMITTENT AERATION

- 版本：出版版本（与前轮PDF SHA256一致，属于重新下载）
- 阅读范围：PDF第4–8页（正文pp.299–303），Sections 2.1–2.3及Fig.1；第12–13页（正文pp.307–308）相关运行讨论，沿用前轮已读证据
- 判断：6 仍待确认；重新下载并核对的方法/流程仍显示曝气在好氧MBBR、回流至前级anoxic隔室；不能把有回流连接自动解释为主动向AD或水解产酸供氧。前级过程性质及回流氧干预意图仍需明确，保持类别6；已有全文，不再将未获取全文列作障碍。
- 定位摘录：Figure 1 Technical reactor design of modified septic tank of fixed bed anoxic - moving bed biofilm reactor from a side view This reactor above has a similar design to the basic schematic technology of the Johkaso system especially related with the oil and grease trap, sedimentation tank, and also di…
- 缺失/待确认：需确认前级为AD/厌氧水解产酸而非单纯缺氧脱氮，并证实供氧回流为有意干预；可查SI或询问作者，无需再次索取同一正文。
- 来源：https://e-journal.trisakti.ac.id/index.php/urbanenvirotech/article/download/12776/8498
- 本地PDF：`/workspace/ad-oxygen-review/download-round-20261006/downloads/R08127/publisher-1/PDFs/ORGANIC_REMOVAL_IN_DOMESTIC_WASTEWATER_USING_ANAEROBIC_TREATMENT_SYSTEM-MBBR_WITH_FLOW_RECIRCULATION_RATIO_AND_INTERMITTENT_AERATION.pdf`

## 补充材料

直接PDF路由的si.not_found只表示未给出可定位SI的落地页，不能证明该文章无SI。已检查可访问的落地页及正文对SI的引用；MDPI主落地页返回Access Denied，R08069引用Table S1.1等但未取得附件。本轮未取得独立SI。R11658 Methods的4.7与Table 1的4.8剂量差异、R10372空气/氧量表述冲突均单列，不凭缺参数阻碍范围判断。

## 失败分流

- 网络阻塞：具体错误包括“Tunnel connection failed: 403 Forbidden”，发生在CONNECT阶段；不等同目标机构订阅不足。
- 目标站点验证/拦截：NTU HTTP405正文为“Human Verification”；Cranfield、IWA/RSC部分入口HTTP403“Just a moment”；EPFL HTTP429正文“WAF: bot suspect activity”，不简单当普通限流。
- UGent的四条仓储记录显示“full text | UGent only”，代表该仓储副本的机构限制，不表示HKUST订阅不足。未绕过其限制。
- 未发现公开全文：仅指本轮已检查入口没有取得可验证正文；不声称全网不存在OA，尤其Unpaywall未启用、部分域名仍受代理限制。
- 需登录与工具限制：HKUST正式EZProxy返回200、标题“Shibboleth Authentication Request”，表单目标为官方shib.ust.hk。到达认证请求不算文献访问成功；没有完成登录/MFA，83篇HKUST及Fudan订阅权限均未知，无法判为订阅不足。
- 本轮编排遇到source字段字符串/字典兼容错误及PDF文字ﬂ连字，已分别修正解析与NFKC定位，属于代码/文本提取问题而非网络故障。每个ID最终均有下载尝试记录。

## 官方机构访问与人工流程

HKUST说明：https://library.hkust.edu.hk/find-borrow/resources/ezproxy-campus-access-subscription-resources 。该官方页面明确可给DOI链接前加https://lib.ezproxy.hkust.edu.hk/login?url=，并要求本人HKUST SSO和Duo MFA。清单中每篇DOI入口按这一已核实官方方法构造，尚未认证，不能承诺可下载。无DOI记录使用官方数据库导航并复制完整题名查询。

Fudan官方入口：https://libdbnav.fudan.edu.cn/ ；校外访问说明：https://library.fudan.edu.cn/118/list.htm 。该官方页面提供WebVPN及师生VPN说明；账号是否有效、具体订阅是否覆盖均未验证。

按manual_download_needed_utf8.csv中的77条逐篇在本人浏览器打开官方入口、自行登录和MFA，核对题名作者DOI后保存完整PDF及需要的SI。若数据库明确无订阅，可试合法Fudan入口、作者公开版或图书馆文献传递。不要保存登录/验证码/错误页为PDF；文件名建议原ID加题名。获取后按remaining_review_workflow_80_utf8.csv的逐项标准记录页码、原句、供气及阶段再判1–6。

80条仍待确认：77条尚无论文全文；R04700、R08127、R10372已有正文但分别有发表版本或范围问题，清单明确标注无需重下载同一全文。48条缺摘要仍在未决集合中，另有R06129一句片段摘要，文句已澄清，不能称已读完整摘要。

## 更新数量与文件验证

|类别|本轮83条最终状态|统一400条|
|---|---:|---:|
|1|0|120|
|2|1|38|
|3|0|35|
|4|0|40|
|5|2|87|
|6|80|80|

原400个稳定ID全部保留，原文件不覆盖；R04269/R04270同题名不同DOI的版本疑点仍保留。六类别RIS互斥覆盖400条，原始研究合并RIS为类别1–3的193条，不应与单类别重复导入。EndNote选择Reference Manager (RIS)、Unicode (UTF-8)。新增结果只包括表格、RIS、说明与审计数据；ZIP不包含PDF、提取全文、原始工具日志、配置、账号或浏览器数据。

更多合法来源仍可能存在；这是一轮受网络和交互认证能力限制的定向尝试，不是全网全文可得性的穷尽证明。

## 网络配置草稿

本轮新增必要域名已经通过平台工具保存到配置草稿；返回requires_publish=true，保存不等于应用或发布。若继续在云环境访问，需在环境设置找到Internet access/Networking、Allowed domains，保存并发布环境配置后复测。部分官网后来可读，但若干目标仍在CONNECT阶段拒绝，不能声称所有白名单已在当前运行环境生效。

新增域名：library.hkust.edu.hk、library.fudan.edu.cn、lib.ezproxy.hkust.edu.hk、julac-hkust.primo.exlibrisgroup.com、libdbnav.fudan.edu.cn、webvpn.fudan.edu.cn、dspace.lib.ntua.gr、eprints.usq.edu.au、ir.giec.ac.cn、ir.qibebt.ac.cn、api.nva.unit.no、www.research.unipd.it、idp.springer.com。配置文件不随结果提交。