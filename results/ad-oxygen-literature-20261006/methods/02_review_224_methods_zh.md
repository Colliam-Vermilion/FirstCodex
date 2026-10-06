> 阶段方法快照：下文中的数量和旧文件名属于该阶段，不是当前交付目录。旧交付文件已由最终版替代，可通过清理前提交 `af86f8c303c4b0a385f7a07f6fa23184ecdf55e1` 追溯。当前文件导航、最终数量及导入方案见 [README](../README.md)。文中运行环境路径仅是证据来源位置，不是下载链接。

# AD主动供氧文献库：224条待确认记录复核

复核日期：2026-10-06。沿用原纳入时间和范围，仅定向补证与复核原224条待确认记录，没有重建文献库或重复进行广泛主题检索。原400条记录、稳定ID及原文件均保留。本轮新增字段同时保存原筛选状态、原待确认事项、原题名和原DOI；逐篇原因均标为“本轮复核判定”，不声称恢复此前未记录的人工过程。

## 流程与证据规则

先审计原文献表、原始记录和筛选记录；建立224条逐篇疑点，先验证15条覆盖气体组成、供氧阶段、后处理、化学氧化、文献类型等不同问题，再连续处理其余209条。以明确摘要为有效筛选证据，不强制全文；缺剂量、频率或DO条件不阻碍范围纳入。全文关键词仅定位，继续阅读方法和上下文，必要时检查反应器图。明确排除须有范围证据，不以下载失败排除。

分类：1直接向AD或内部循环供氧；2厌氧水解/产酸段供氧；3独立好氧/微好氧预处理；4综述；5排除；6仍待确认。范围同时覆盖不同底物、气泡供氧、控制曝气、气相供氧和反应器内电解产氧；化学过氧化物处理本身不等同主动引入空气/分子氧。

## 补充查询与获取记录

- 对224条逐篇回查已有摘要、PubMed/NCBI、OpenAlex及Crossref。195条原DOI中193条Crossref回查成功，2条404；无DOI记录继续保留。DOI和题名匹配后才接受补充，曾检出一个无关PubMed命中，已拒绝，不写入文献。
- 对缺摘要记录执行精确DOI与题名查询；对83条未解决DOI继续查询Semantic Scholar并核对标识符。原56条缺摘要中补得8条，目前224条中176条有摘要、48条仍无摘要；个别新增摘要片段过短，仍保留待确认。
- PubMed查询采用具体DOI的[aid]限定和题名限定；PMC核查采用具体DOI而非泛关键词。OpenAlex按已有work ID读取；Crossref为/api/works/{DOI}；Semantic Scholar为paper/batch的DOI:{DOI}。这些是逐条补证，不计作新主题检索。429响应串行降速重试；不能将限流视为代理拦截。
- 对未解决记录检查权威数据库OA位置、出版商citation_pdf_url、公开仓储及PMC。全文共检查8篇PMC JATS正文、6篇开放PDF及1份研究海报；合计14篇文章全文、1份海报。PDF逐个校验%PDF头、可读取页数及题名/DOI身份。补充材料未全部获得，逐条注明。
- nature-downloader缓存技能已读取并检查依赖。Node 24需要NODE_USE_ENV_PROXY=1才能使用当前代理；实际直接公开PDF路线成功取得R08127的21页全文。自动OA路线可识别元数据但部分出版社PDF入口被当前代理阻断，不能将MCP启动或200元数据视为全文成功。

## 网络与访问局限

当前可访问NCBI、Crossref、OpenAlex及部分PMC/Europe PMC、Semantic Scholar和公开仓储。部分出版社重定向仍报“Tunnel connection failed: 403 Forbidden”（CONNECT代理阶段），包括linkinghub.elsevier.com、www.sciencedirect.com及link.springer.com的实际访问。普通目标HTTP 403/404与代理CONNECT拒绝分别记录，不单凭状态码归因。已将观察到的必要域名补充到云环境网络配置草稿；草稿保存不代表当前所有连接均已解除限制。如需继续，环境设置中寻找Internet access/Networking及Allowed domains，发布配置并重启相应环境后复试。未使用Scopus、ScienceDirect付费凭据、机构登录或任何绕过访问控制方式。

## 关键范围判断与纠错

- R05213全文仅24小时AD接种物水解子实验比较空气/氮气头空间，因此纳入类别1；40天甲烷实验冲氮，不能将空气或H2O2效果移植到该实验。
- R12483开放全文Fig.5及Methods 2.4–2.5表明透气瓶真菌预处理30天后另行冲氮BMP，纳入类别3。原DOI在Crossref及doi.org均404，出版商RIS未列DOI，复核版清空未核实DOI并保留原值；更正题名采用出版商与PDF。
- R08127全文显示MBBR曝气与回流路径，但目标厌氧段是否属于范围内AD/水解产酸及回流供氧意图仍不足以判断，保持类别6。
- R05473仅取得一页本科研究海报，不能当完整文章全文；正式发表版本和氨气提气路仍需确认。
- R04269/R04270同题名同摘要但DOI不同，均有独立排除依据；保留两个稳定ID并标注版本疑点。无重复稳定ID或重复DOI，不声称已证明这两个记录代表不同文章。

## 交付与导入

统一表含原400条：未在本轮复核的176条沿用原判断；224条全部填写逐篇问题、最终分类和证据定位。六类别RIS是400条的互斥分组；confirmed_original_research.ris合并类别1–3，方便导入，但不要与三个单类别文件重复导入。排除RIS仅供审计。EndNote选择File → Import → File，Import Option为Reference Manager (RIS)，Text Translation为Unicode (UTF-8)。作者各占一条AU，题名、DOI、ID及分组与Excel/CSV逐项核对。正式版本不明、学位论文/海报不冒充期刊文章。

全文与运行缓存保留在当前环境，结果目录不包含邮箱、API密钥、环境配置或原始网络日志。原始7个交付文件不覆盖；复核版位于review_20261006子目录。

## 首批15条流程验证

- **R00028** A study on the feasibility of micro-aeration for pre-treatment on the anaerobic co-digestion of food waste with brown water → 6 仍待确认。摘要确认低剂量氧和单双级BMP；单级直接投氧与独立预处理各自实施位置未区分，且学位/报告版本需核验。 证据：摘要；“he principle objective of the experiment was to investigate on whether supplying oxygen at a low dosage, or micro-aeration, would had a positive effect on the hydrolysis of the anaerobic digestion of food waste and brown water.”。https://openalex.org/W2978789636

- **R00036** Advanced Thermal Hydrolysis: Optimization of a Novel Thermochemical Process to Aid Sewage Sludge Treatment → 5 排除。实验干预为热水解联合过氧化氢，不是空气或分子氧供给；氧化剂当量不可当作曝气剂量。 证据：摘要；“ATH is based on a thermal hydrolysis (TH) process plus hydrogen peroxide (H(2)O(2)) addition and takes advantage of a peroxidation/direct steam injection synergistic effect.”。https://doi.org/10.1021/es204203y

- **R00074** Bench Scale Study for Oxygen Uptake and Anaerobic Digestion of Industrial Wastewater → 5 排除。摘要将厌氧CSTR与用于好氧可处理性评价的呼吸测定明确分开；不是向AD或其水解阶段供氧。 证据：摘要；“…hibitory constituents in the feed and was eventually inactivated.Impact of oxygen demand was evaluated using respirometry in order to determine stoichiometric and kinetic parameters as well as component concentrations and viability of co-treatment using aerobic treatment methods such as activated sl…”。https://openalex.org/W2625977732

- **R00134** Determination of Oxygen by Means of a Biogas and Gas - Interference Study Using an Optical Tris (4,7-Diphenyl-1,10-Phenanthroline) Ruthenium(II) Dichloride Complex Sensor. → 5 排除。研究干预为气体混合室中的光学氧传感器表征及在线测氧，不是AD主动供氧实验。 证据：摘要；“A special gas-mixing chamber was developed for gas interference study, and on-line experiments are presented for oxygen determination within the pilot biogas reactor.”。https://openalex.org/W2408779733

- **R00166** Effect of leachate recirculation and aeration on volatile fatty acid concentrations in aerobic and anaerobic landfill leachate → 5 排除。分别运行好氧和厌氧填埋反应器，曝气属于独立好氧处理对照，未构成AD前处理或厌氧阶段主动供氧。 证据：摘要；“In this study, two aerobic (A1, A2) and two anaerobic (AN1, AN2) reactors with (A1, AN1) and without (A2, AN2) leachate recirculation were used in order to determine the change of volatile fatty acids components in landfill leachate.”。https://doi.org/10.1177/0734242x11417983

- **R00214** Flocculation, Anaerobic and Microaerobic Treatment Process of Normal Temperature Low Concentration Domestic Sewage → 5 排除。摘要明确MUSB微好氧段位于UASB厌氧处理之后，仅为后处理。 证据：摘要；“DO of microaerobic MUSB technique after anaerobic treatment is 0.2mg/L-0.5mg/L with air and water ratio of 1:1.”。https://doi.org/10.4028/www.scientific.net/amr.518-523.2530

- **R00257** Intermittent Aeration and Continuous Flow Biofilm Process for Treatment of Rural Domestic Sewage → 6 仍待确认。摘要给出水解酸化区和接触氧化区，但未明确间歇曝气是否进入水解区还是只进入后续氧化区。 证据：摘要；“…ing rate of 60% was 0.88 m3/(m3·d),and the hydraulic load in the contact oxidation zone with media filling rate of 75% was 4.57 m3/(m3·d).The operation results of six months showed that the average removal rates of COD,BOD5,NH3-N,TP and SS were 74.8%,83%,51.4%,60.3% and 81.8%,respectively,and the co…”。https://openalex.org/W2376561243

- **R00273** Management of hydrogen sulfide in anaerobic digestion of enzyme pretreated marine macro-algae → 1 直接向 AD 反应器或内部循环系统供氧。摘要明确在连续海藻厌氧消化中实施微曝气并比较中温和高温过程效应；发表类型及剂量另行核验不阻碍范围判断。 证据：摘要；“Micro-aeration was found to be more efficient in the thermophilic reactor while its effect on the mesophilic process was negligible.”。https://openalex.org/W1725776391

- **R00356** Potential of biogas and methane production from anaerobic digestion of poultry slaughterhouse effluent → 5 排除。摘要明确实验因素为HRT和筛分固体，未研究主动供氧；COD是指标而不是供氧操作。 证据：摘要；“For data analysis, a completely randomized design was performed in a 4 × 2 factorial arrangement (4 HRT: 7, 14, 21 and 28 days and separation with 1 mm sieve or without separation), with repetition over time.”。https://doi.org/10.1590/s1516-35982012001100013

- **R00363** Production of High Calorific Biogas from Organic Wastewater and Enhancement of Anaerobic Digestion → 4 综述。摘要为多种沼气增热值及AD强化工艺的概述，明确讨论微好氧过程，作为相关综述追溯。 证据：摘要；“New anaerobic digestion processes, such as micro-aerobic process, electrolysis enhancing methane production process, process of internal circulation anaerobic digester (ICAD) with sewage source heat pump, may all enhance biogas producton or lower biogas production cost.”。https://doi.org/10.4028/www.scientific.net/amr.550-553.522

- **R00384** Sanitization efficacy of anaerobic digestion and aeration of slurry from the aspect of limiting emission of Salmonella into the environment. → 5 排除。对猪粪分别做厌氧消化和曝气消毒效能对比；不是向AD供氧或AD前曝气处理。 证据：摘要；“A higher rate of elimination and shorter time of survival of all the tested bacteria was observed, compared with the use of aeration.”。https://openalex.org/W893670044

- **R00429** The removal of 1,4-dioxane from polyester manufacturing process wastewater using an up-flow Biological Aerated Filter (UBAF) packed with tire chips → 5 排除。摘要明确曝气滤池进料为厌氧处理单元出水，是AD后好氧处理。 证据：摘要；“The UBAF was fed with effluent, containing an average of 31 mg/L of 1,4-dioxane, discharged from an anaerobic treatment unit at H Co.”。https://doi.org/10.1080/10934529.2012.630291

- **R00516** Aeration and pH Combined Regulation for the Phase Separation of Anaerobic Digestion → 2 向厌氧水解或产酸阶段供氧。摘要明确在两相AD水解段按8小时间隔主动曝气以抑制甲烷，实现相分离。 证据：摘要；“…phase,adjusted the initial pH of the hydrolysis phase below 6.5,aerated three times daily at interval of 8h with ≥ 1 L air per L of container volume,the methane production in hydrolysis phase could be effectively suppressed,and achieve the phase separation basically.”。https://openalex.org/W2363726478

- **R00608** Comparative Study of Micro-aerobic and Anaerobic Hydrolysis Acidifications of Petrochemical Wastewater → 2 向厌氧水解或产酸阶段供氧。摘要明确微好氧与厌氧水解酸化对比并控制DO约0.5mg/L，符合相关厌氧水解产酸阶段供氧。 证据：摘要；“…n the high salt content and refractory industrial wastewater.The dissolved oxygen(DO) of micro-aerobic condition is about 0.5 mg/L,and the oxidation reduction potential(ORP) of anaerobic reactor is below-300 mV.The results showed that the average removal rate of CODCr with micro-aerobic hydrolysis a…”。https://openalex.org/W2349051635

- **R00642** Effect of Combined Pretreatment of Waste Activated Sludge for Anaerobic Digestion Process → 5 排除。实验干预为碱和低温热处理联合，不属于主动供空气/氧气。 证据：摘要；“lkaline and low-temperature thermal pretreatment has been used to the subsequent anaerobic digestion of waste activated sludge (WAS) respectively.”。https://doi.org/10.1016/j.proenv.2013.04.097

## 本轮数量

|类别|224条复核|统一400条|
|---|---:|---:|
|1|28|120|
|2|10|37|
|3|9|35|
|4|9|40|
|5|85|85|
|6|83|83|

剩余83条的完整题名、访问链接和逐篇未决问题见manual_fulltext_needed_zh.md及同名CSV/工作表。未完成独立双人筛选；全文获取有限，不能承诺全部范围判断和参数提取已无遗漏。
