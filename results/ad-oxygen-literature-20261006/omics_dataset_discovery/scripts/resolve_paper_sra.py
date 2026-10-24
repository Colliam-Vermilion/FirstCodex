import json,re,time,xml.etree.ElementTree as ET
from common import ROOT,dump,url,getjson
BASE='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
links=json.loads((ROOT/'paper_to_SRA_links.json').read_text());uids=sorted({u for x in links for u in x['SRA_uids']});resolved={}
for off in range(0,len(uids),100):
 j,m=getjson(url(BASE+'esummary.fcgi',db='sra',id=','.join(uids[off:off+100]),retmode='json'),'NCBI');time.sleep(.4)
 for uid in (j or {}).get('result',{}).get('uids',[]):
  v=j['result'][uid];ex=v.get('expxml','');proj=re.search(r'<Bioproject>([^<]+)</Bioproject>',ex);exp=re.search(r'<Experiment acc="([^"]+)"',ex)
  if proj:resolved[uid]={'project':proj[1],'experiment':exp[1] if exp else None,'official_summary_source':m['raw_path']}
reg={x['accession']:x for x in json.loads((ROOT/'discovered_projects.json').read_text())};papers={x['pmid']:x for x in json.loads((ROOT/'paper_discovery_candidates_enriched.json').read_text())};associations=[]
for row in links:
 for uid in row['SRA_uids']:
  if uid not in resolved:continue
  v=resolved[uid];acc=v['project'];a={'pmid':row['pmid'],'project':acc,'SRA_uid':uid,'experiment':v['experiment'],'relation':'官方PubMed→SRA ELink及ESummary明确BioProject','ELink_source':row['official_source'],'ESummary_source':v['official_summary_source']};associations.append(a)
  r=reg.setdefault(acc,{'accession':acc,'source_queries':['PubMed→SRA反查'],'study_title':'待完整项目元数据','run_accessions_discovered':[],'raw_source_paths':[]})
  if 'PubMed→SRA反查' not in r['source_queries']:r['source_queries'].append('PubMed→SRA反查')
  if v['official_summary_source'] not in r['raw_source_paths']:r['raw_source_paths'].append(v['official_summary_source'])
  if row['pmid'] in papers and acc not in papers[row['pmid']].get('project_accessions',[]):papers[row['pmid']].setdefault('project_accessions',[]).append(acc)
extra=json.loads((ROOT/'paper_linked_SRA_additional_metadata.json').read_text());group={}
for batch in extra:
 for row in batch['rows']:
  p=row.get('study_accession')
  if p:group.setdefault(p,[]).append(row)
for p,rows in group.items():dump(ROOT/'project_cache'/p/'ncbi_sra_link_subset.json',rows)
oldids={x['paper_id'] for x in json.loads((ROOT/'existing_articles_availability_audit.json').read_text())};linked=[];previous={x['pmid']:x for x in json.loads((ROOT/'new_associated_papers.json').read_text())}
for pmid,p in papers.items():
 pp=[x for x in associations if x['pmid']==pmid];allprojects=sorted(set([x for x in p.get('project_accessions',[]) if x.startswith('PRJ')]+[x['project'] for x in pp]))
 if not allprojects or p['paper_id'] in oldids:continue
 p.update(project_accessions=allprojects,project_link_evidence=pp or previous.get(pmid,{}).get('project_link_evidence') or [{'evidence':'官方PubMed记录直接出现项目编号','source_paths':p['source_paths']}],reading_level='官方关联元数据/已保存摘要，未声称全文方法核实',availability='由项目层另行核实；关联不证明数据类型/处理可用')
 linked.append(p)
dump(ROOT/'SRA_uid_project_resolution.json',resolved);dump(ROOT/'paper_SRA_project_associations.json',associations);dump(ROOT/'discovered_projects.json',list(reg.values()));dump(ROOT/'new_associated_papers.json',linked);print('resolved_uids',len(resolved),'associated_papers',len(linked),'new_associated_pmids',[x['pmid'] for x in linked],flush=True)
