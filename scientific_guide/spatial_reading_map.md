# 空间结构—气体传质的阅读导图

这是帮助比较研究尺度的示意，不是某个反应器已经测得的统一结构。[回科学首页](../README.md) · [专题累计Excel](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/spatial_gas_transfer_cumulative.xlsx) · [专题文献—命题表](spatial_gas_proposition_links_utf8.csv)

**现行状态（2026-11-01）：**原12组查询已在2026-10-30完整分页取回。9篇上传正文已读方法/结果/讨论和关键图表，附件缺口与未筛队列单列。[统一精读入口](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/uploads_20261101/README.md)；旧网络失败状态见[历史快照](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/uploads_20261101/history/scientific_guide_spatial_reading_map.md)。

## 先辨传质经过哪里，再看谁在那里

```mermaid
flowchart LR
 G[气相：气体组成、流量、压力] -->|气液交换 kLa| B[主体液相：混合与浓度]
 B -->|表面液膜 kf| S[聚集体表面]
 S -->|内部溶解态扩散 Deff| I[内部细胞周围]
 I --> R[产生或消耗：反应速率]
 R -->|H2、CH4、CO2、H2S等可向外移动| I
 O[ORP反馈：控制电位] -.-> B
 D[DO反馈：控制测点氧浓度] -.-> B
```

气液交换是跨界面进入/离开液相；外液膜是主体到聚集体表面的一段阻力；内部扩散描述溶解态分子在聚集体中的移动。细胞反应一面消耗、一面产生物质，决定了浓度梯度。图中没有假定气泡必须穿过污泥，也没有认为所有流动都能由一个Deff描述。

|先读的问题|首选材料及当前证据|不能跨越的解释|
|---|---|---|
|分层和产氢／产甲烷发生在哪里？|Satoh等2007；FISH＋H2/CH4/pH/ORP微剖面，**上传全文方法/结果/讨论核实**，[证据](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/evidence/ODS-PMID17905889.md)|特定颗粒有内层乙酸裂解产甲烷古菌，不代表古菌总在中心；局部浓度剖面不是三维细胞坐标。|
|三维成像究竟重建了什么？|Gambelli等2018摘要明确电子断层；Wrede等2008为同切片光/电镜和EPS标记；[结构表](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/structure_localization_evidence_utf8.csv)|细胞电子断层、切片、共聚焦堆栈和整颗粒CT不能互称。CT种子已于2026-10-30核实正文；体素不是活体通量或类群定位。|
|表面积变化是否支持气液/润湿界面限制？|R03161改变桶放置/润湿面积并测H2S氧化；已读相关原文，p3–4/7–8|生物膜量、活性与面积共变；反应去除率不是纯物理kLa或扩散系数。|
|ORP、DO、固定输入分别控制什么？|R01414为ORP开关；R07202为相对基线ORP；R06080为非产甲烷颗粒DO反馈；[控制表](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/oxygen_control_evidence_utf8.csv)|测了DO不等于DO反馈；气相O2不等于液相DO；ORP电极基准不清时不能比较绝对值。|
|H2和甲酸是否一样？|Day等2022的代谢突变株竞争与搅拌；Hamilton等2015为模型；[交换表](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/cell_interfloc_exchange_utf8.csv)|遗传证据可区分载体，模型可提出条件；二者都不自动给出距离—通量测量。|
|混合／气泡供给与内部扩散是否同一件事？|Luo等2013粪便／乳清AD比较H₂扩散器及搅拌；[缓存证据](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/evidence/ODS-PMID23143533.md)|气液交换与pH／CO₂限制不同；没有从摘要取得kLa。|
|天然甲烷群落是否一定紧密球状？|Gründger等2019冷泉ANME-1丝束／斑块与SRB松散相伴；[缓存证据](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/evidence/ODS-PMID31278352.md)|CLSM尚未核堆栈／体重建；松散关联不是絮体间交换通量。|
|絮凝提高酸转化是否就是距离效应？|Pinela等2024高氨富集中的铁氧化物／非导电沸石与石墨烯比较；[缓存证据](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/evidence/ODS-PMID39110235.md)|絮凝、附着、磷沉淀和功能共变；需距离干预／载体通量，不能只归DIET。|

## 距离至少有三个尺度

1. **两个细胞之间：**短程H2／甲酸交换、产生者与消费者的反应耦合。要有实际距离或干预才能讨论最优距离。
2. **同一絮体内部：**内部扩散、空间分布和反应共同决定交换；不是对流均一的两细胞系统。
3. **不同絮体之间：**还要经过两侧表面、主体液相和混合流场。本轮已读材料没有直接核实跨絮体距离或气体通量测量，相关种子仍待全文。

H2是溶解态小分子；甲酸主要是液相物种，不应笼统画成气泡。CO2/H2S存在酸碱物种分布，温度、盐度、pH和压力也影响边界条件。

## 参数表应怎样读

|量|物理含义与常见单位|本轮可写到什么程度|
|---|---|---|
|D / Deff|分子／有效扩散系数，m²/s|Satoh摘要H2 Deff=2.66×10^-5 cm²/s；PVA-E人工膜O2 D=0.42×10^-4 cm²/s；Anammox凝胶De约颗粒3倍但探针溶质未核。这是三类材料／参数，不能混并；温度、测量／拟合和失活与否待全文。|
|kL / kf|界面或液膜传质系数，m/s|已读材料未取得可独立核实的直接测定数值，不拿模型假定或反应率补空。|
|kLa|体积传质系数，s^-1等|不是气流量，也不是DO。当前没有已全文核实可直接汇总的kLa测量值。|
|J|单位面积物质通量，mol/(m²·s)等|要注明物种、界面面积和梯度。脱硫g S/(m²·d)是反应器面积归一去除率，不能不加限定当无反应物理传质通量。|
|反应速率|产生/消耗物质的速率，基于体积、质量或生物量|受菌量、活性、底物和传质共同影响；不能由甲烷增加唯一反推Deff增大。|

Fick定律把浓度梯度与扩散通量联系起来：一维、连续介质近似下，$J=-D_{eff}dC/dx$。有反应时必须再给反应项和边界条件；不能把失活颗粒的扩散测量直接写成活性颗粒的净通量，也不能不说明条件就推广一个氧穿透深度。

## 本轮仍需哪些证据

原五篇种子已在2026-10-30独立核对，S01为整颗粒μCT、S02为颗粒微剖面全文；本轮另有9篇上传全文逐篇核实。继续从[统一精读表](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/uploads_20261101/README.md)的“后续必须回答”、[摘要缺口](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/abstract_pending_queue.json)、[全文疑点](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/fulltext_pending.json)及[未筛队列](../results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/remaining_queue.json)接续。前向引用173条仅取回元数据，不是已读或纳入；其原始页和分页状态在本轮citation_trace_log.json。不能重跑旧渲染脚本覆盖全文增量。

## 先看哪篇、哪张图

- **外部DO为什么不等于内部DO？**先看Daigger的Fig5–9，再对比Fan的Fig3：两类核心状态均有条件性实测，非普适粒径阈值。
- **稳态为什么不足以反推D？**看Chiu 2007 Fig8的可行参数对与瞬态约束。
- **空间结构是否一定导致更大阻力？**看Berg Table2及Fig2–4，分开水自扩散实测和O₂模型；强分层/对流不在其小异质性模型结论内。
- **几何能否独立改变低氧？**看Wessel Fig4架高实验；生物报告不能判零氧。
- **AD中谁在何处产气？**看Satoh Fig3–6，位置、浓度、计算活性和失活扩散试验分开；看González-Gil Fig4–9区分乙酸动力学拟合与计算CH₄剖面。

完整9篇题名、ID、问题、图表、边界、阅读深度和全文入口集中在上述统一精读表。
