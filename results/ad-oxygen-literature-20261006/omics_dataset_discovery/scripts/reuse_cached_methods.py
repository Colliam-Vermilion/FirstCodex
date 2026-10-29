"""Reuse two already archived official JATS files; no new paper download."""
from review_dependency import review_bytes
import json,xml.etree.ElementTree as ET
from common import ROOT,dump,now
def run():
 ass=json.loads((ROOT/'project_assessments.json').read_text());papers=json.loads((ROOT/'new_associated_papers.json').read_text());comp=json.loads((ROOT/'confirmed_comparisons.json').read_text());notes=[]
 for acc,pid,pmid,filename,titles in [('PRJNA551662','OR-3035DF955A54','34409684','F34409684_jats.xml',['Incubations','Nucleic acid extraction, 16S rRNA gene amplicon and metagenomic sequence analyses','DATA AVAILABILITY STATEMENT']),('PRJNA1163300','OR-5DA7260E019E','40057977','F40057977_jats.xml',['Sediment community cell extraction and experimental incubations for single amplified genome experiments','Deoxyribonucleic acid and ribonucleic acid extraction and sequencing','Data availability'])]:
  root=ET.fromstring(review_bytes('raw/pmc_fulltext/'+filename));secrows=[]
  for sec in root.findall('.//sec'):
   title=' '.join(sec.find('title').itertext()) if sec.find('title') is not None else ''
   if title in titles:secrows.append({'section':title,'xml_section_id':sec.get('id'),'verbatim':' '.join(' '.join(sec.itertext()).split())})
  doi=next((n.text for n in root.findall('.//article-id') if n.get('pub-id-type')=='doi'),None);pmcid=next((n.text for n in root.findall('.//article-id') if n.get('pub-id-type')=='pmc'),None);source='https://pmc.ncbi.nlm.nih.gov/articles/'+str(pmcid)+'/' if pmcid else 'https://pubmed.ncbi.nlm.nih.gov/'+pmid+'/'
  ev={'project_id':acc,'paper_id':pid,'official_page':source,'existing_cached_source':'../oxygen_response_review/raw/pmc_fulltext/'+filename,'source_type':'复用官方全文JATS，仅实际阅读方法和数据声明章节','sections_read':secrows,'checked_utc':now()};notes.append(ev)
  p={'paper_id':pid,'pmid':pmid,'doi':doi,'pmcid':pmcid,'title':' '.join(root.find('.//article-title').itertext()),'year':next((n.text for n in root.findall('.//pub-date/year')),None),'journal':' '.join(root.find('.//journal-title').itertext()),'project_accessions':[acc],'existing_literature_id':pid,'newly_discovered_paper':False,'reading_level':'本轮已读缓存官方全文的方法/数据声明章节；非全文通读','project_link_evidence':[{'evidence':'官方全文数据声明明确项目号','source_path':ev['existing_cached_source'],'location':titles[-1],'verbatim':secrows[-1]['verbatim']}],'source_paths':[ev['existing_cached_source']],'source_queries':['reuse_cached_official_fulltext_methods'],'availability':'以官方项目清单及方法核实为准'}
  if not any(x['paper_id']==pid for x in papers):papers.append(p)
  for c in comp:
   if c['project_id']==acc:c['design_evidence_level']='缓存官方全文方法+官方样本映射';c['method_evidence_path']='reused_cached_fulltext_methods.json';c['method_source_page']=source
  if acc=='PRJNA551662':
   a=ass[acc];a['oxygen_delivery_and_dose_as_recorded']='0%, 5%, 10% v/v O2；95%/90% N2配气，至少6次替换headspace';a['oxygen_time_and_frequency']='每2–3日flush维持O2，98日后100%N2吹扫再厌氧134日，总232日；另独立短期21% O2实验不混入';a['temperature']='room temperature（原文未给数值）';a['substrate']='Sphagnum泥炭；AWT/BWT/UNS层位';a['biological_replicates']='培养各处理triplicate；232日前合并重复抽提DNA、232日按重复抽提。公开20WGS是不平衡子集，不能按培养triplicate补不存在的文库';a['mapping_status']='0/5/10% O2和原始Time Point/Layer可核；T标签到具体日仍保留待键表，pooling按方法保留';a['limitations']='需区分98日供氧和之后134日厌氧恢复；T代码未强行转日，公开0% O2每比较仅1库，非平衡三重复设计；DNA不是RNA，病毒/ARG重分析需深度与组装质控';a['priority']='优先扩展DNA：方法证实氧输入和厌氧恢复，20WGS；按氧剂量、层位、pooling分层，探索性分析'
  else:
   a=ass[acc];a['oxygen_delivery_and_dose_as_recorded']='0% vs 25% atmospheric oxygen headspace（作者换算约4% O2）；2.5ml头气置换为环境空气';a['oxygen_time_and_frequency']='24 h';a['temperature']='21°C';a['substrate']='1mM laminarin；只有添加laminarin样本RNA成功并pool';a['biological_replicates']='培养triplicate，但RNA从添加laminarin的培养混池，最终每氧条件1库；不能用3个培养瓶冒充3个测序重复';a['mapping_status']='cDNA1加空气/cDNA2不加空气；两者均含laminarin并混池，由全文RNA抽提章节补证';a['limitations']='1:100沉积物细胞稀释后0.2um过滤；同实验DNA未产出可用metagenome；SAG/WGA另列，8个JGI其他地点DNA不是本实验配对MG。2个混池RNA无独立文库重复';a['priority']='优先小RNA：明确24h氧输入对照，适合机制探索/效应方向，不能做有重复差异检验'
   for c in comp:
    if c['project_id']==acc:c.update(treatment='air+laminarin pooled RNA',control='anoxic+laminarin pooled RNA',caveat=a['limitations'])
 dump(ROOT/'project_assessments.json',ass);dump(ROOT/'new_associated_papers.json',papers);dump(ROOT/'confirmed_comparisons.json',comp);dump(ROOT/'reused_cached_fulltext_methods.json',notes)
 print('reused official cached methods',len(notes))
if __name__=='__main__':run()
