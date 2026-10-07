# 初次漏收原因、补充术语与检索验证

审计/补充检索日期：2026-10-07（Asia/Shanghai）。范围继续为2012-01-01至检索日。现行人工分类具有最终权限；包含类别5的完整库参与查重，类别5不用于下游纳入分析。没有重筛或改动原53条人工记录（原28＋本次附件25）。

## 审计对象和可核验依据

对象是综述参考文献追溯后确认纳入的58条净新增记录，56条期刊原研究、1条会议、1条学位论文。按追溯前400条库ID集合核实，58条均不在原已保留文献库中。因此，旧库的“已收录待确认→确认”不计作漏检。R13854实际是已收录R01238的重复引文，已合并、亦不在58条内。

使用保存的初始OpenAlex/PubMed/CrossRef返回、补充查询、两轮引文追溯、merged.json、excluded.json、candidates.json、screen-excluded.json及library.json，先规范化DOI匹配，缺DOI时完整规范题名、作者与年份核对；R13871在初始记录与现行记录均为2013年、同一Al-Mashhadani作者。另遍历954份原始JSON/XML缓存；55条有身份匹配，3条未找到。保留初始ID、题名、完整摘要（包括旧错误文本）、排除原因与原始缓存文件哈希，见omission_reasons_58_utf8.csv、omission_initial_evidence_58.json。初始两个筛选脚本SHA256及实际错误模式重放见initial_pattern_replay_cases.json；没有重新执行其筛选来覆盖当前判断。

## 主要阶段数量

|主要发生阶段|数量|实际记录证据|
|---|---:|---|
|初始已返回，但筛选排除/遗漏|55|40条在广义预筛excluded.json，15条在候选筛选screen-excluded.json|
|现存初始返回中未找到匹配|3|R13818、R13831、R13867；规范化返回及954缓存均未匹配|
|去重/元数据匹配/整合丢失得到证实|0|没有发现返回后无排除记录而意外丢失的本58条；R13854是已收录重复，不能算新增漏检|
|连发生阶段也不能确定|0|匹配55条有排除证据；另3条只能确认保存返回未匹配，其具体原因仍未知|

48条出现在初次直接关键词返回，另外7条仅在初次引文追溯返回，3条没有保存匹配。**“未找到匹配”限定于保留记录，不证明数据库从未索引，也不确定是词、日期/类型过滤、引文缺口还是其他机制。** 这3条的具体检出机制未知，应与发生阶段数量区别报告。

原保存排除理由细分：未找到氧/空气/曝气18；未找到AD/相关水解产酸16；一般氧背景无主动线索3；负向题名模式3；“非AD/含氧/耐氧”5；“基础代谢非AD”5；供氧被当测量背景2；接种物预处理1；化学氧化1；学位非期刊1。合计55。所列是旧理由，不表示本轮仍认同。

## 有实际代码/记录支持的问题

1. **aerobic并未被初始OXY完整涵盖。** OXY含aerat、oxygen、microaerob，却漏独立aerobic/microaerophilic和纯air mixing。R13821、R13824、R13843、R13844等已经返回却在氧词门槛被排除；这不是简单“数据库没有检出”。R13827更已取得摘要“Aerobic pre-treatment was applied prior to two-stage anaerobic digestion”，仍在后段被误认为普通背景。
2. **AD词序/拼写桥接不足。** R13845的anaerobic sludge digestion、R13840的hydrolysis acidification、R13860的anaerobic baffled biofilm-membrane reactor在预筛误排。后段分类又省略anaerobic reactor等表述，误排R13837、R13861、R13875；R13833用LCFA to methane而非标准AD短语。补充搜索词同时必须补充筛选识别，而不能只改查询。
3. **无词边界的负向规则。** classify.py的wine模式实际命中R13868、R13880、R13887、R13893的swine；gasification命中R13820煤气化废水。已按原题名重放并保存位置。修复应使用词边界，并把负向词作为人工定位提示，不作为先于摘要/语境的硬排除。
4. **研究目标被当成系统性质。** 脱硫、微污染物去除、硅氧烷转化不能替代供氧位置核查。R13835、R13859、R13860都已有返回，不能怪检索遗漏。已纳入的人工R00888与排除的R01827/R04719展示内供氧与独立沼气后处理边界；本轮不重判这些人工条目。新增原始研究R13914（AMODM）明确同一反应器中产甲烷，不能仅因methane oxidation目标排除；实际ID应以新增表为准。
5. **接种物/类型边界不一致。** R13823旧审计排除预曝气接种物，当前人工R11537单列独立好氧驯化3；应按实验是否专门氧处理并服务AD来判断，日常菌种培养仍不自动纳入。R13871过去按学位论文类型排除，现在作为学位资料单列，不能全部归为关键词或程序错误。R13867会议未返回可能与CrossRef初始journal-only过滤有关，但证据不足，不能把它写成确定原因。
6. **化学供氧不可一概而论。** R13856、R13878涉及CaO2；已确认原位释氧证据时按对应阶段纳入。CaO2/O2−/ROS名称不等于已证明分子氧供给，本轮相关新线索仍定向核查，而不机械全部加入。R11041人工预处理3只说明阶段边界，不是所有化学处理均合格的授权。

## 实际用词及作者关键词

supplement_keywords_utf8.csv分供氧方式、AD过程、底物、研究目标，逐词列真实ID、出现字段/片段、语法和噪声风险。作者关键词仅用PubMed KeywordList；初始取得16条非空，本轮补充后25条。其余33条没有非空作者关键词，不把OpenAlex主题或CrossRef subject冒作作者关键词。

关键表达：aerobic pre-treatment、pre-aeration、aerobic hydrolysis、thermophilic aerobic digestion；microaerophilic、semi-aerobic、oxygen-limited aeration、limited air exposure；membrane aerated、bubbleless micro-aeration、air mixing；nano-bubble water/NBW、fluidic oscillation；calcium peroxide/oxygen-releasing；ORP/redox potential；LCFA/oleate/siloxanes conversion；sulfide removal及micropollutant biotransformation。氧化还原、微污染物和氨抑制词是研究目标，不是供氧证明。底物词用于补充而不设置必要门槛。

初始PubMed broad查询已有oxygen*/aerat*，初始OpenAlex亦含aeration/oxygen、气泡及aerobic pretreatment；旧查询中已有的词需要补的是拼写/词序、字段、来源和筛选规则，不能称全部为新增搜索词。oxygen pulses、venturi aeration、oxygen-enriched air等未在本58条验证，表中明确为待验证扩展。本轮不声称这些未执行词带来新增。

## 按数据库适配的完整检索式

本轮使用nature-academic-search multi-source-search指导。当前无挂载可调用的academic MCP工具，采用技能支持的官方API客户端分页；既有运行环境和PubMed配置复用，配置/邮箱不进入交付。完整15条执行检索式、字段、日期和返回数见supplement_search_log_utf8.csv；同样文本另列下文。

OpenAlex使用title_and_abstract.search、cursor/per-page200，日期from_publication_date:2012-01-01,to_publication_date:2026-10-07。该字段为词干检索，不能在此用通配符*；首次HTTP400后改显式词形组合，6组全部重跑成功。PubMed使用TIAB、短语、通配词尾和Date - Publication，获取全部PMID，EFetch每批100。CrossRef不支持直接等价TIAB布尔检索，query.title是相关性匹配：选择3个单词microaerophilic/semiaerobic/microoxygenation，journal-article及日期过滤，每页1000，完整cursor；不把伪AND布尔句写入CrossRef声称精确。

### OpenAlex S1_aerobic_stage

```text
(anaerobic OR biogas OR methanogenesis OR methanogenic OR "methane production" OR "methane yield" OR "hydrolysis acidification" OR acidogenic OR "acid fermentation") AND ("aerobic pretreatment" OR "aerobic pre-treatment" OR "aerobic pre treatment" OR "aerobic hydrolysis" OR "aerobic digestion" OR "aeration pretreatment")
```

字段：title_and_abstract.search；过滤：from_publication_date:2012-01-01,to_publication_date:2026-10-07。报告423，取得423，分页3。

### OpenAlex S2_low_oxygen

```text
(anaerobic OR biogas OR methanogenesis OR methanogenic OR "methane production" OR "methane yield" OR "hydrolysis acidification" OR acidogenic OR "acid fermentation") AND (microaerophilic OR "micro-aerophilic" OR "semi-aerobic" OR semiaerobic OR "oxygen-limited" OR "limited air exposure")
```

字段：title_and_abstract.search；过滤：from_publication_date:2012-01-01,to_publication_date:2026-10-07。报告1061，取得1061，分页6。

### OpenAlex S3_membrane_delivery

```text
(anaerobic OR biogas OR methanogenesis OR methanogenic OR "methane production" OR "methane yield" OR "hydrolysis acidification" OR acidogenic OR "acid fermentation") AND (bubbleless OR "membrane aerated" OR "membrane aeration" OR "air mixing" OR "sludge holding" OR "air stripping")
```

字段：title_and_abstract.search；过滤：from_publication_date:2012-01-01,to_publication_date:2026-10-07。报告307，取得308，分页2。

### OpenAlex S4_bubble_water

```text
(anaerobic OR biogas OR methanogenesis OR methanogenic OR "methane production" OR "methane yield" OR "hydrolysis acidification" OR acidogenic OR "acid fermentation") AND ("nano-bubble water" OR "nanobubble water" OR "nano bubble water" OR "microbubble water" OR "fluidic oscillation")
```

字段：title_and_abstract.search；过滤：from_publication_date:2012-01-01,to_publication_date:2026-10-07。报告62，取得62，分页1。

### OpenAlex S5_hidden_intervention

```text
(anaerobic OR biogas OR methanogenesis OR methanogenic OR "methane production" OR "methane yield" OR "hydrolysis acidification" OR acidogenic OR "acid fermentation") AND ("calcium peroxide" OR "oxygen release" OR "oxygen-releasing" OR "redox potential" OR composting OR "hydrothermal pretreatment with air")
```

字段：title_and_abstract.search；过滤：from_publication_date:2012-01-01,to_publication_date:2026-10-07。报告7303，取得7307，分页37。

### OpenAlex S6_process_bridge

```text
(anaerobic OR biogas OR methanogenesis OR methanogenic OR "methane production" OR "methane yield" OR "hydrolysis acidification" OR acidogenic OR "acid fermentation") AND ("hydrolysis acidification" OR "hydrolysis process" OR "anaerobic sludge" OR "anaerobic reactor" OR "LCFA to methane" OR "volatile siloxanes") AND (microaeration OR "micro-aeration" OR microaerobic OR "micro-aerobic" OR "limited aeration" OR microaerophilic)
```

字段：title_and_abstract.search；过滤：from_publication_date:2012-01-01,to_publication_date:2026-10-07。报告108，取得108，分页1。

### CrossRef C_microaerophilic

```text
microaerophilic
```

字段：query.title；过滤：from-pub-date:2012-01-01,until-pub-date:2026-10-07,type:journal-article。报告145，取得145，分页2。

### CrossRef C_semiaerobic

```text
semiaerobic
```

字段：query.title；过滤：from-pub-date:2012-01-01,until-pub-date:2026-10-07,type:journal-article。报告6，取得6，分页2。

### CrossRef C_microoxygenation

```text
microoxygenation
```

字段：query.title；过滤：from-pub-date:2012-01-01,until-pub-date:2026-10-07,type:journal-article。报告10，取得10，分页2。

### PubMed S1_aerobic_stage

```text
(anaerobic[tiab] OR biogas[tiab] OR methanogen*[tiab] OR "methane production"[tiab] OR "methane yield"[tiab] OR "hydrolysis acidification"[tiab] OR acidogen*[tiab]) AND ((aerobic[tiab] AND (pretreat*[tiab] OR "pre-treatment"[tiab] OR hydrolys*[tiab] OR digest*[tiab])) OR "aeration pretreatment"[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/07"[Date - Publication])
```

字段：TIAB；过滤：publication date。报告1095，取得1095，分页11。

### PubMed S2_low_oxygen

```text
(anaerobic[tiab] OR biogas[tiab] OR methanogen*[tiab] OR "methane production"[tiab] OR "methane yield"[tiab] OR "hydrolysis acidification"[tiab] OR acidogen*[tiab]) AND (microaerophil*[tiab] OR "micro-aerophilic"[tiab] OR semiaerob*[tiab] OR "semi-aerobic"[tiab] OR "oxygen-limited"[tiab] OR "limited air exposure"[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/07"[Date - Publication])
```

字段：TIAB；过滤：publication date。报告496，取得494，分页5。

### PubMed S3_membrane_delivery

```text
(anaerobic[tiab] OR biogas[tiab] OR methanogen*[tiab] OR "methane production"[tiab] OR "methane yield"[tiab] OR "hydrolysis acidification"[tiab] OR acidogen*[tiab]) AND (bubbleless[tiab] OR "membrane aerated"[tiab] OR "membrane aeration"[tiab] OR "air mixing"[tiab] OR "sludge holding"[tiab] OR "air stripping"[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/07"[Date - Publication])
```

字段：TIAB；过滤：publication date。报告103，取得103，分页2。

### PubMed S4_bubble_water

```text
(anaerobic[tiab] OR biogas[tiab] OR methanogen*[tiab] OR "methane production"[tiab] OR "methane yield"[tiab] OR "hydrolysis acidification"[tiab] OR acidogen*[tiab]) AND ("nano-bubble water"[tiab] OR "nanobubble water"[tiab] OR "nano bubble water"[tiab] OR "microbubble water"[tiab] OR "fluidic oscillation"[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/07"[Date - Publication])
```

字段：TIAB；过滤：publication date。报告33，取得33，分页1。

### PubMed S5_hidden_intervention

```text
(anaerobic[tiab] OR biogas[tiab] OR methanogen*[tiab] OR "methane production"[tiab] OR "methane yield"[tiab] OR "hydrolysis acidification"[tiab] OR acidogen*[tiab]) AND ("calcium peroxide"[tiab] OR "oxygen release"[tiab] OR "oxygen-releasing"[tiab] OR "redox potential"[tiab] OR compost*[tiab] OR "hydrothermal pretreatment with air"[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/07"[Date - Publication])
```

字段：TIAB；过滤：publication date。报告1471，取得1471，分页15。

### PubMed S6_process_bridge

```text
(anaerobic[tiab] OR biogas[tiab] OR methanogen*[tiab] OR "methane production"[tiab] OR "methane yield"[tiab] OR "hydrolysis acidification"[tiab] OR acidogen*[tiab]) AND ("hydrolysis acidification"[tiab] OR "hydrolysis process"[tiab] OR "anaerobic sludge"[tiab] OR "anaerobic reactor"[tiab] OR "LCFA to methane"[tiab] OR "volatile siloxanes"[tiab]) AND (microaerat*[tiab] OR "micro-aeration"[tiab] OR microaerob*[tiab] OR "micro-aerobic"[tiab] OR "limited aeration"[tiab] OR microaerophil*[tiab]) AND ("2012/01/01"[Date - Publication] : "2026/10/07"[Date - Publication])
```

字段：TIAB；过滤：publication date。报告41，取得41，分页1。

## 实际验证及覆盖限制

15组实际完成：OpenAlex6、PubMed6、CrossRef3。原始标准works/期刊记录返回12667条（跨查询重复）；PubMed另有2条BookArticle，PMID30969550/29489261为非AD临床书目，494期刊＋2书目解释对应查询报告496，并非漏取2个PMID。按规范化DOI优先；无DOI时题名、共有作者姓、相邻年份及相容类型核对查重，得到10263条；170条匹配当前原475库，其中18条已排除，全部沿用，不重新加入。

宽词池已按标题及可得摘要作定向定位，218条进入逐项核查表：30条确认新增（28原始研究、2综述）；73条有明确范围外证据；58条存在具体影响阶段/系统/气体判断的疑点，单列不入主库；46条非期刊/版本线索单列关联；11条背景线索未作最终范围判定。9873条宽词发现池未逐篇筛尽，包含大量临床、堆肥、土壤、普通污水和一般AD背景。**这不是全面补检饱和的结论，也不是已确认排除9873条。** 聚焦依据是具体干预/过程表达，不按目标新增数量截断；有范围证据就纳入，缺参数不阻碍。已读取的证据层级逐篇列明，不声称218篇都阅读全文或都完整读过摘要。

新增ID R13894–R13924，R13918撤回并保留空号、不复用。新增28原研究分为内部AD6、专门水解产酸2、独立预处理20，另综述2。原475整条记录/53人工完整对象均不改动；现行主库505条，类别1–6为191、56、85、45、128、0。期刊原始研究318。追溯新增58文件仍为原58；补充新增30单独RIS只是增量导入替代方案，已包含在全量分类中，避免重复导入。

污水软饮料处理线索原拟独立预处理，经R00257/R13851边界校准后发现摘要仅报告COD与两级厌氧单元、未确认AD/专门产酸性质，故列证据不足，未加入。新研究包括O2-NBW稻草浸泡前处理与含air/O2/O3三组的AD纳米气泡研究；后者虽O3效果最好，仍因实际air/O2组符合范围。正式2027的air mixing论文PMID42648380，电子发表2026-08-26，在时间范围内；正式2026-10-15的composting/extrusion研究已于2026-09-05上线，两类年份分开。

CrossRef首次高并发DOI核验出现HTTP429，降为单请求间隔1.5秒后62篇元数据核验均200并检查身份字段；200本身不是在线检索/全文证据。PMC10880661的XML虽200但仅front且声明出版者不允许XML正文下载，未把它当全文读取。未绕过访问控制。

未覆盖WoS/Scopus/Embase/CNKI/万方；索引摘要缺失、非英文表达、未追溯新增2篇综述及宽词池未筛尽均可能继续漏收。建议下一轮先修复并复查原预筛排除池及本轮剩余线索，优先补摘要/引用语境，再进一步开放更多低特异词；不能用加词替代筛选质量修正。

本轮15组组合查询实际重新返回原58漏收中的41篇；逐来源/查询组在supplement_recovered_chase_ids_utf8.csv。不能将组合OR命中解释为某个单词的独立新增贡献。

## 补充核验与下一轮可执行建议（下列新方案未执行）

3条无初始匹配记录另作规范题名近似核对，记录见initial_unmatched3_fuzzy_checks.json。R13831的近似结果R03575具有不同DOI/年份，不按相似题名直接判作同文献或整合丢失。

实际漏收题名还出现digester、digester headspace及plug-flow digester，建议将消化器词作为过程桥接。下一轮可用PubMed：

```text
(digester*[TIAB] OR "anaerobic sludge digestion"[TIAB] OR "hydrolysis acidification"[TIAB]) AND (microaera*[TIAB] OR microaerophil*[TIAB] OR aerat*[TIAB] OR "air mixing"[TIAB] OR "oxygen dosing"[TIAB]) AND ("2012/01/01"[Date - Publication] : "2026/10/07"[Date - Publication])
```

OpenAlex对应词干字段title_and_abstract.search，显式使用(digester OR digesters OR "anaerobic sludge digestion" OR "hydrolysis acidification") AND (microaeration OR microaerophilic OR aeration OR "air mixing" OR "oxygen dosing")，沿用本轮日期过滤。该独立桥接查询尚未执行，不能计入本轮15组成功检索。CrossRef建议另设type:proceedings-article并单词查询microaerophilic或microaeration；本轮仅执行journal-article，会议渠道扩展仍待验证。

为判断新增纳米气泡综述的范围，另核对了其CrossRef元数据列出的90条引文中与原库匹配的R13887、R05544、R06979及R13880；这些是二手引文关联辅助，不代表完整逐条追溯90条，更不能代替原研究证据。本轮新增2篇综述仍未完成系统参考文献追溯。

数量单位说明：218条定向候选与完整查重台账中的220条关联返回并非一一对应；两篇无DOI的填埋研究题名各对应两种元数据类型，因身份信息不足未强制合并，亦未纳入主库。故台账为170既有＋30新增＋190其他候选关联返回＋9873未逐篇核查返回＝10263；候选表另以218条候选行逐项记录。

最后范围复查：拟新增R13918仅题名证明微曝气厌氧硫酸盐废水反应器，没有AD/专门水解产酸功能证据；已移至58条候选，主库505条。Semantic Scholar补得parabens论文完整摘要，明确UASB内供空气且不损害methanogenesis，支持其类别1；见supplement_late_identity_checks.json。上述按DOI定向身份补查不计入15组主题查询。
