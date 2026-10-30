"""Append spatial-transfer knowledge; keep every old homepage paragraph intact."""
import io,json,re,subprocess
from pathlib import Path
from openpyxl import load_workbook
from prepare import T,M,P,R,read,dump
from render import csvout
BASE='fcd0ad3119900af9f75c9b9220575b8ff79a0170';G=R/'scientific_guide'
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R)
GROUPS={
 'P1c':('Part 1','氧等气体通过哪些串联环节到达或离开细胞？', ['ODS-PMID17905889','OR-9AE95458315B','OR-6A3D9B1E5D73','R03161','R01133','R08069','R13832','R06227','R05611','R09240','R13923','ODS-PMID30236845','ODS-PMID39311608','ODS-PMID26498000','OR-1E3E423A9EFE']),
 'P1d':('Part 1','ORP反馈、DO反馈和固定供氧分别控制什么，哪些暴露仍未知？',['R01414','R07202','R06080','OR-06716459121E','R03161','R13944','R13280','R13833']),
 'P3c':('Part 3','哪些成像真正给出三维结构，细胞、EPS与孔隙是否被分别定位？',['ODS-PMID17905889','ODS-PMID17547018','ODS-PMID32994285','OR-8E58C5BBDB53','OR-06716459121E','OR-F8559A118DBF','OR-8E15795B9DD4','ODS-PMID18405985','ODS-PMID29150508','OR-52E6BA12BEDD','OR-1925EF467A30','OR-B0B72D22FA67','ODS-PMID40222284','ODS-PMID38218075']),
 'P4d':('Part 4','距离、混合和载体选择如何改变H2/甲酸交换与产甲烷？',['ODS-PMID36374033','ODS-PMID26147299','ODS-PMID35699440','ODS-PMID35918706','ODS-PMID17905889','ODS-PMID19490126','R13833','ODS-PMID42323140']),
 'P4e':('Part 4','哪些证据来自细胞间或絮体内，哪些真正测量了絮体间交换？',['ODS-PMID36374033','ODS-PMID26147299','ODS-PMID35918706','ODS-PMID35699440']),
}
def mlink(path,origin=R):return Path(path).relative_to(origin).as_posix()
def label(r):return ((r.get('authors') or ['作者待核对'])[0].split(',')[0]+'等，'+str(r.get('year') or '年份待核'))
def card(r):return T/'evidence'/(r['id']+'.md')
def cite(r):return f'[{label(r)}]({mlink(card(r))})'
def table(ids,C):
 out=['|代表研究与阅读深度|对象／证据|结果及限制|DOI与证据|','|---|---|---|---|']
 for rid in ids:
  r=C[rid];url=f'[{r["doi"]}](https://doi.org/{r["doi"]})' if r.get('doi') else 'DOI待核'
  vals=[label(r)+'；'+('相关全文段落/原证据' if r['reading_depth'].startswith('全文') else '仅缓存摘要'),r['title']+'；'+r['decision_reason'],r['actual_finding']+'。'+r['author_interpretation_and_alternatives'],url+f' · [证据卡]({mlink(card(r))})']
  out.append('|'+ '|'.join(str(x).replace('|','&#124;').replace('\n','<br>') for x in vals)+'|')
 return '\n'.join(out)
def main():
 master=read(T/'literature_master.json');done_all=[r for r in master if r['status']!='未开始'];C={r['id']:r for r in master};mapped=set().union(*(set(x[2]) for x in GROUPS.values()));assert mapped<=set(C);done=[r for r in done_all if r['id'] in mapped]
 # Evidence cards keep the original source/quote, and make missing measurements
 # explicit rather than treating them as negative findings.
 for r in done:
  lines=[f'# {label(r)} — {r["title"]}','',f'文献ID：`{r["id"]}`。阅读深度：**{r["reading_depth"]}**。旧判断未修改。','',f'DOI：'+(f'[{r["doi"]}](https://doi.org/{r["doi"]})' if r.get('doi') else '尚未核实'),'',f'专题关联：{r["decision_reason"]}','',f'实际结果：{r["actual_finding"]}','',f'解释与边界：{r["author_interpretation_and_alternatives"]}','', '## 原有来源','']
  for link in r['source_links']:
   rel='../../../../../'+link['path'];lines += [f'- [{link["path"]}]({rel})，定位`{link["identity_field"]}={link["id"]}`。']
  if r.get('author_metadata_source'):lines += [f'- [作者官方元数据来源](../../../../../{r["author_metadata_source"]})。']
  pdf=T/'evidence'/(r['id']+'_pdf_pages.json')
  if pdf.exists():
   data=read(pdf);lines += [f'- [本轮页码文本]({pdf.name})；[现有PDF原件](../../../{data["source_path"]})。抽取有缺字时以原PDF为准；R01414阈值负号经页面图像核验。']
  if (M/'evidence_sources'/(r['id']+'.json')).exists():lines += [f'- [既有原文位置](../../evidence_sources/{r["id"]}.json)。']
  if r.get('locator'):lines += ['', '已核位置：'+r['locator']+'。']
  lines += ['', '## 完整缓存摘要（来源材料，不等于阅读全文）','', '> '+r.get('abstract','').replace('\n','\n> '),'']
  card(r).write_text('\n'.join(x.rstrip() for x in '\n'.join(lines).splitlines()).rstrip()+'\n')
 base_map=json.loads(old('scientific_guide/literature_proposition_map.json'));base_props=json.loads(old('scientific_guide/propositions.json'));relations=[];props=[]
 for pid,(part,q,ids) in GROUPS.items():
  props.append({'proposition_id':pid,'part':part,'question':q,'evidence_rule':'空间/传质专题新增，保留测量环节、尺度、参数来源与阅读深度；不更改旧分类'})
  for rid in ids:
   r=C[rid];relations.append({'id':rid,'title':r['title'],'year':r.get('year'),'journal':r.get('journal'),'doi':r.get('doi'),'author_year':label(r),'part':part,'proposition_id':pid,'proposition_question':q,'study_object':r.get('system') or r['priority_tier'],'oxygen_treatment':(r.get('control_evidence') or {}).get('type'),'finding':r['actual_finding'],'boundary':r['author_interpretation_and_alternatives'],'reading_depth':r['reading_depth'],'prior_screening_decision':r['existing_scope_decision_preserved'],'mapping_status':'专题新增科学关联；未修改既有范围判断','support_role':'范围/方法支持或限制，不等于独立验证；P4e行仅用于界定证据尺度' if pid!='P4e' else '指出该研究不能单独证明絮体间交换，不据此断言领域不存在证据','evidence_card':mlink(card(r)),'source_links':r['source_links']})
 current=list(base_map)+relations;oldids={r['id'] for r in base_map};newmapped={r['id'] for r in relations}
 for r in master:
  if r['id'] not in oldids and r['id'] not in newmapped:
   current.append({'id':r['id'],'title':r['title'],'year':r.get('year'),'journal':r.get('journal'),'doi':r.get('doi'),'proposition_id':None,'mapping_status':'尚未建立命题关联；专题初筛状态：'+r['status'],'reading_depth':r['reading_depth'],'topical_scope_decision':r['scope_decision'],'source_links':r['source_links']})
 dump(G/'spatial_gas_proposition_links.json',relations);csvout(G/'spatial_gas_proposition_links_utf8.csv',relations)
 dump(G/'literature_proposition_map.json',current);csvout(G/'literature_proposition_map_utf8.csv',current)
 dump(G/'propositions.json',base_props+props);csvout(G/'propositions_utf8.csv',base_props+props)
 wb=load_workbook(io.BytesIO(old('scientific_guide/scientific_reading_guide.xlsx')))
 for name,data in [('全部文献—命题',current),('科学命题',base_props+props),('空间传质专题',done_all),('空间专题关联',relations)]:
  if name in wb.sheetnames:del wb[name]
  ws=wb.create_sheet(name);keys=list(dict.fromkeys(k for r in data for k in r));ws.append(keys)
  for r in data:ws.append([json.dumps(r.get(k),ensure_ascii=False) if isinstance(r.get(k),(list,dict)) else r.get(k) for k in keys])
  ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
 wb.save(G/'scientific_reading_guide.xlsx')
 summary=json.loads(old('scientific_guide/summary.json'));summary.update(spatial_date='2026-10-30',spatial_processed=len(done_all),spatial_candidates=len(master),spatial_proposition_links=len(relations),spatial_external_discovery_completed=False,expanded_map_rows=len(current),expanded_map_unique_ids=len({r['id'] for r in current}),current_propositions=len(base_props+props),old_42_article_93_link_snapshot_preserved=True)
 dump(G/'summary.json',summary)
 prefix=mlink(T)
 b1=f'''### 专题增补：P1c—P1d · 气体怎样到达细胞，控制器又控制了什么？

先把**气液交换 → 主体混合 → 聚集体表面液膜 → 内部溶解态扩散 → 细胞反应**分开；气泡的存在、液相中H₂／CH₄分子的移动和气体经过膜的扩散也不同。加大混合可能减少外液膜阻力，同时改变颗粒剪切和气液交换，不能只归为一种机制。**2026-10-30本专题已对保存材料中的{len(done_all)}篇开展初筛／相关段落阅读；题名、摘要和全文深度在表中分别标明。在线补检尚未完成，不能视为完整文献覆盖。**

物理上，扩散是分子沿浓度差净移动。简单一维条件下可写为 $J=-D_{{eff}}\\,dC/dx$：$J$是面积通量，$D_{{eff}}$是聚集体的有效扩散系数。外液膜常以 $J=k_f(C_b-C_s)$ 表示主体与表面间的浓度落差；气液交换的单位液体体积速率常写成 $k_La(C^*-C_b)$。三者的单位、面积／体积基准和适用条件不同，不能互填。活性颗粒内浓度还由反应消耗／产生决定；稳态扩散—反应模型可写为 $0=\\nabla\\cdot(D_{{eff}}\\nabla C)-r(C)$，其中反应项和边界条件需要独立说明。液相CO₂、H₂S还受酸碱物种分布影响。

- **颗粒内：**Satoh等（2007）摘要报告H₂有效扩散系数2.66×10⁻⁵ cm²/s，约水中的57%。还须核正文的活性／失活材料、温度、尺寸和参数取得方法；它不是活性颗粒的净反应速率，也不能套用于氧或其他污泥。
- **界面：**Mulbry等的液面／润湿面积干预显示脱硫能力随面积提高，但可同时改变生物膜量／活性。g S/(m²·d)是表观反应去除率，不应填入kLa或Deff栏。
- **控制：**ORP反馈维持的是电位；DO反馈维持测点溶解氧；固定流量／比例／脉冲供气控制的是输入。三者均不能单独说明所有细胞的实际暴露。R01414为−310 mV开阀、−290 mV关阀；开阀氧流量0.14 mL/s。R07202则以各自厌氧基线+25 mV控制，不能借用同一绝对阈值。参考电极未核清时，不换算标准氢电极电位，更不换算DO。
- **低DO并非零输入：**共培养反应器持续供空气，但主体DO低于约3 μM检出限；这既不是零氧证明，也不是DO闭环。DO设定0.5 mg/L的另一实例是脱氮颗粒系统，属于方法参照，不能当作产甲烷AD最适值。

{table(['ODS-PMID17905889','R01414','OR-06716459121E','R03161','R06080'],C)}

[参数与剖面]({prefix}/gas_transfer_parameters_utf8.csv) · [控制逐项核对]({prefix}/oxygen_control_evidence_utf8.csv) · [完整专题与未完成查询]({prefix}/README.md) · [尺度阅读导图](scientific_guide/spatial_reading_map.md)

'''
 # Check the author rather than substituting a familiar name from memory.
 author03161=(C['R03161'].get('authors') or ['作者待核'])[0].split(',')[0]
 b1=b1.replace('Mulbry等',author03161+'等')
 b3=f'''### 专题增补：P3c · 看到了二维切片、细胞三维结构，还是整颗粒的孔隙？

**需要按成像对象和体积辨别。** FISH可定位类群，但单张图、冷冻切片、共聚焦图像堆栈与真正三维重建不能互称。CT的密度／元素对比、总细胞染色、特异性FISH和EPS染色各自识别不同对象；看到空腔，不等于量到了孔道连通性、流量或气体通量。

现有缓存摘要中，Gambelli等（2018）明确使用了**电子断层成像**，观察厌氧甲烷氧化富集中的细胞和候选管状接触结构；它是三维方法线索，尚未在本轮全文核对重建体积／分辨率，且不是整颗产甲烷AD颗粒CT。Wrede等（2008）采用的是同切片光／电镜与凝集素标记EPS，不能升格为体重建。用户提供的同步辐射微CT种子10.1128/aem.00563-24尚未独立取回核对，故不据题名写孔隙发现。

**也不预设古菌总在中心。** Satoh的特定颗粒有内层产乙酸型古菌；硅藻土AD研究的摘要则将发酵菌与产甲烷菌分别关联到紧密附着和悬浮群落。后者不是颗粒内坐标，但提示聚集体内层、载体附着及主体悬浮是不同尺度，不能套用一张统一层状示意图。粒径分级下活性不同，也可能反映群落和生物膜年龄，而非唯一证明内部扩散限制。

{table(['ODS-PMID29150508','ODS-PMID18405985','ODS-PMID40222284','ODS-PMID32994285'],C)}

[结构与定位证据]({prefix}/structure_localization_evidence_utf8.csv)逐项保留方法、对象和阅读深度；保护性空间机制仍需氧分布及结构干预配套证据。

'''
 b4=f'''### 专题增补：P4d—P4e · 交换发生在两个细胞、一个絮体内部，还是两个絮体之间？

**近距离可以缩短扩散路径，但载体、热力学和混合同样重要。** 在给定浓度差、扩散系数与几何条件下，路径较短可降低物质交换的扩散阻力；这不是不加条件的最优距离，也不能据此提供一个通用微米数值。用户给出的2012年丙酸互营菌间距离种子和1991年动态絮体模型仍待独立核对，不能先照写其距离或参数。

Day等（2022）的共培养研究用H₂／甲酸代谢突变株比较，支持**甲酸交换占优势**；搅拌促使H₂向顶空损失时，能用甲酸者优势更大。因此H₂和甲酸不宜只视为等效的“电子传递”。Hamilton等（2015）与CO₂甲烷化的通量平衡研究属于预测交换的模型；Doloman等的第三菌加入试验同时看到聚集和速率提高，但信号／酶调节也是替代解释。它们均不自动证明某个细胞间距离决定了通量。

**细胞间／絮体内不能写成絮体间。** 已读资料尚未提供本轮已核实的“两个不同絮体间距离—H₂/甲酸通量”直接测量。跨絮体还经过各自内部、表面液膜及主体混合，必须说明尺寸、间距、流场与测量／模型边界。这个缺口只描述本轮已读材料，不说明领域不存在此类研究。导电材料或EET相关基因也不等于已测气体物质交换。

{table(['ODS-PMID36374033','ODS-PMID26147299','ODS-PMID35699440','ODS-PMID35918706'],C)}

[细胞间／絮体间证据]({prefix}/cell_interfloc_exchange_utf8.csv) · [种子核对及具体缺口]({prefix}/seed_audit_utf8.csv) · [同一累计Excel]({prefix}/spatial_gas_transfer_cumulative.xlsx) · [相关文献RIS]({prefix}/spatial_gas_transfer_reviewed.ris)

'''
 home=(R/'README.md').read_text()
 for name in ['exposure','structure','function','navigation']:
  home=re.sub(r'<!-- SPATIAL_'+name+r'_BEGIN -->.*?<!-- SPATIAL_'+name+r'_END -->\n*','',home,flags=re.S)
 for name,anchor,block in [('exposure','<a id="part-2"></a>',b1),('structure','<a id="part-4"></a>',b3),('function','<a id="natural-communities"></a>',b4)]:
  assert anchor in home
  home=home.replace(anchor,f'<!-- SPATIAL_{name}_BEGIN -->\n'+block+f'<!-- SPATIAL_{name}_END -->\n\n'+anchor,1)
 notice=f'''<!-- SPATIAL_navigation_BEGIN -->
**2026-10-30专题增补口径：**下方原有42篇／1,536条等数字保留首版日期与范围；新增空间专题为233条已有资料命中，已处理40篇，其中其余193条仍待专题判断。统一文献—命题表现在覆盖{summary['expanded_map_unique_ids']}个已有身份（含95条复用的组学关联候选），不表示都已读或新检索取得。新增5个问题与{len(relations)}条关联见[专题命题表](scientific_guide/spatial_gas_proposition_links_utf8.csv)，[阅读导图](scientific_guide/spatial_reading_map.md)区分结构、传质、控制和互营；本轮在线检索仍未完成。
<!-- SPATIAL_navigation_END -->

'''
 anchor='## 完整文献关系、阅读入口与方法\n\n';assert anchor in home;home=home.replace(anchor,anchor+notice,1)
 (R/'README.md').write_text(home)
 print(json.dumps({'topical_links':len(relations),'guide_unique_ids':summary['expanded_map_unique_ids'],'guide_rows':len(current),'old_homepage_words_preserved':True},ensure_ascii=False))
if __name__=='__main__':main()
