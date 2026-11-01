from pathlib import Path
import re,json,os,hashlib
R=Path('/workspace/FirstCodex');T=R/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer';P=T/'uploads_20261101';G=R/'scientific_guide';H=P/'history';H.mkdir(exist_ok=True)
for f in [R/'README.md',G/'README.md',G/'spatial_reading_map.md']:(H/(f.parent.name+'_'+f.name)).write_text(f.read_text())
entry='results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/uploads_20261101/README.md'
f=R/'README.md';s=f.read_text();pos=s.index('### P1a')
box='''### 从供氧条件到微生物实际氧暴露

判断氧的作用，先问测点在哪里，再问该处浓度持续多久。主体DO、絮体表面DO与内部细胞周围DO可以不同；在供氧条件下存活，既可能因为细胞耐氧，也可能因为它实际接触的氧较少。以下原理box解释传递环节；EPS和聚集的具体证据留在Community structure，保护与底物竞争、甲烷消耗的权衡留在Community function。

> **为什么向反应器供氧，不等于所有微生物都暴露于氧？**
>
> 氧先跨气液界面，再随主体液体混合，到达絮体或颗粒表面时还可能经过外液膜，随后才向内部扩散。这几段阻力各有尺度：气液交换常用kLa，外液膜用kf，内部扩散用Deff；一个参数不能代表全部环节。
>
> 絮体表面接触含氧液体，不等于所有内部细胞经历相同DO。氧一边传入，一边被活细胞及还原性化合物消耗；物理扩散阻力、生物耗氧和化学耗氧需要分开判断。粒径、可扩散表面积、孔隙与密度、外部DO、活性及供氧持续时间共同决定氧能到多深。扩散时间可粗略随长度平方/D增大，但活性材料还须加入反应和时间变化的边界。
>
> 不能预设所有絮体都有无氧核心，也不能预设所有絮体完全氧化。Daigger 2007既测到大絮体近零DO，也测到小絮体非零平台及模型失配；Fan 2017在其1.5–2 mg/L测定条件下未测到无氧区。Chiu 2007在同一类颗粒改变外DO，内部穿透随之改变。因此“低DO”不能自动解释为“EPS阻氧”。

[空间结构与传质统一精读表]('''+entry+''')列出9篇上传全文、关键图表、方法、参数来源、反例和原件；其中Daigger、Chu沿用原ID，未重复计为新检索发现。

'''
s=s[:pos]+box+s[pos:]
s=s.replace('**在线补检尚未完成，12组查询仍待执行**','**原12组已于2026-10-30完整取回；筛选与全文补证仍未完成**')
# Integrate scientific content directly under Community structure, keeping its original questions and examples.
p=s.index('\n',s.index('## Part 3.'))+1
para='''
### 空间结构怎样改变暴露：本轮全文带来的约束

“聚集保护”至少包含几何路径、材料阻力和活性消耗三个可能过程。Wessel 2014的Fig4改变相同体积微笼的可扩散底面积，架高后低氧报告信号消失，支持几何边界的作用；报告信号存在延迟且需氧成熟，不能据此确认零氧核心。Chiu 2007的Fig8说明单用稳态剖面不能把扩散系数与耗氧常数独立识别。Fan 2017的EPS、菌量和粒径同时变化，没有分离EPS自身的效应。

Sabra 2000的Fig6–7显示氧条件相关的海藻酸荚膜形态改变，提出保护固氮酶的解释，但没有直接测胞内O₂或荚膜O₂扩散系数。Berg 2020的NMR实测对象是水自扩散；结构T2图不能直接转换成氧图，恒定平均D、小幅异质性模型也不能排除强表层阻力。这些证据支持具体可检验机制，尚不能给出微曝气AD通用EPS阻氧参数。

AD中，Satoh 2007把FISH切片与H₂/CH₄微剖面联系起来，内层是**乙酸裂解产甲烷古菌**，不是“产乙酸古菌”；不同物质剖面取自不同颗粒，净生成率由模型计算。González-Gil 2001则通过粒径和上流速度区分乙酸转化的内外传质限制，其CH₄内部剖面为计算结果。二者均没有微曝气O₂处理，不能当作结构保护耐氧的直接验证。

详细条件、数值矛盾及图表位置见[统一精读表]('''+entry+''')；保护可能降低氧暴露，也可能限制底物进入，功能净收益仍须结合Part 4判断。
'''
s=s[:p]+para+s[p:];f.write_text(s)
f=G/'README.md';s=f.read_text();lines=s.splitlines();lines[3]='**现行空间传质入口（2026-11-01）：**[统一精读表与原件](../'+entry+') · [阅读导图](spatial_reading_map.md) · [累计Excel](../'+str(T.relative_to(R))+'/spatial_gas_transfer_cumulative.xlsx)。原12组于2026-10-30完整取回，文献筛选与全文补证仍在继续。本轮9篇上传全文及新增摘要参照见专题检查点；旧网络失败和阅读状态移至[有日期历史快照](../'+str(H.relative_to(R))+'/scientific_guide_README.md)。下文2026-10-29/30数字仅指当时范围。';f.write_text('\n'.join(lines)+'\n')
f=G/'spatial_reading_map.md';s=f.read_text();s=re.sub(r'\*\*接续状态：\*\*[^\n]+','**现行状态（2026-11-01）：**原12组查询已在2026-10-30完整分页取回。9篇上传正文已读方法/结果/讨论和关键图表，附件缺口与未筛队列单列。[统一精读入口](../'+entry+')；旧网络失败状态见[历史快照](../'+str(H.relative_to(R))+'/scientific_guide_spatial_reading_map.md)。',s,count=1)
s=s.replace('**本轮仅缓存摘要**','**上传全文方法/结果/讨论核实**').replace('内层产乙酸古菌','内层乙酸裂解产甲烷古菌')
s=s.replace('CT种子尚未独立核实，不照抄题名结论。','CT种子已于2026-10-30核实正文；体素不是活体通量或类群定位。')
s=s.replace('有效扩散测量对象是否失活、温度、标定/拟合方法和边界层尚未从正文核实','35°C氯仿失活颗粒H₂阶跃拟合；CH₄比值为假定')
start=s.index('网络恢复后优先独立核对五篇种子')
s=s[:start]+'''原五篇种子已在2026-10-30独立核对，S01为整颗粒μCT、S02为颗粒微剖面全文；本轮另有9篇上传全文逐篇核实。继续从[统一精读表](../'''+entry+''')的“后续必须回答”、[摘要缺口](../'''+str(T.relative_to(R))+'''/abstract_pending_queue.json)、[全文疑点](../'''+str(T.relative_to(R))+'''/fulltext_pending.json)及[未筛队列](../'''+str(T.relative_to(R))+'''/remaining_queue.json)接续。前向引用173条仅取回元数据，不是已读或纳入；其原始页和分页状态在本轮citation_trace_log.json。不能重跑旧渲染脚本覆盖全文增量。
'''
s+='''
## 先看哪篇、哪张图

- **外部DO为什么不等于内部DO？**先看Daigger的Fig5–9，再对比Fan的Fig3：两类核心状态均有条件性实测，非普适粒径阈值。
- **稳态为什么不足以反推D？**看Chiu 2007 Fig8的可行参数对与瞬态约束。
- **空间结构是否一定导致更大阻力？**看Berg Table2及Fig2–4，分开水自扩散实测和O₂模型；强分层/对流不在其小异质性模型结论内。
- **几何能否独立改变低氧？**看Wessel Fig4架高实验；生物报告不能判零氧。
- **AD中谁在何处产气？**看Satoh Fig3–6，位置、浓度、计算活性和失活扩散试验分开；看González-Gil Fig4–9区分乙酸动力学拟合与计算CH₄剖面。

完整9篇题名、ID、问题、图表、边界、阅读深度和全文入口集中在上述统一精读表。
''';f.write_text(s)
f=T/'README.md';s=f.read_text();s=s.replace('# 厌氧微生物空间结构与气体传质专题','# 厌氧微生物空间结构与气体传质专题\n\n**现行入口（2026-11-01）：**[统一文章目录与精读表](uploads_20261101/README.md) · [本轮检查点](uploads_20261101/checkpoint.json)。9篇上传全文使用单一原件映射，现有候选补筛与在线新增分开，累计Excel已同步。以下2026-10-30数字是上一轮有日期的历史统计；本轮增量不覆盖旧判断。',1);f.write_text(s)
# Preserve canonical uploaded PDF; keep old root path as a compatible symlink.
for d in json.load(open(P/'duplicate_files.json')):
 p=R/d['other_path'];target=R/d['canonical']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==d['sha256']
 if p.exists() and not p.is_symlink():p.unlink();p.symlink_to(os.path.relpath(target,p.parent))
