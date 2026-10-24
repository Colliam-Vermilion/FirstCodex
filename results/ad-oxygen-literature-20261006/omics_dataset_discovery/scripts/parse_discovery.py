import json,re,xml.etree.ElementTree as ET
from common import ROOT,dump

def txt(e,path):
 n=e.find(path);return ' '.join(' '.join(n.itertext()).split()) if n is not None else ''
def run():
 logs=json.loads((ROOT/'search_log.json').read_text());register={x['accession']:x for x in json.loads((ROOT/'discovered_projects.json').read_text())};bioproject=[];papers={};oldcat=json.loads((ROOT.parent/'oxygen_response_review/catalog.json').read_text());dmap={x.get('doi','').lower():x['id'] for x in oldcat if x.get('doi')};pmap={x.get('pmid'):x['id'] for x in oldcat if x.get('pmid')};existingpapers={x['paper_id'] for x in json.loads((ROOT/'existing_articles_availability_audit.json').read_text())}
 for log in logs:
  qid=log['query_id']
  if not qid.startswith(('N','P')):continue
  for b in log.get('fetch_batches',[]):
   if b['status']!=200:continue
   tree=ET.fromstring((ROOT/b['raw_path']).read_bytes())
   if qid.startswith('N'):
    for node in tree.findall('.//DocumentSummary'):
     x=node.find('./Project/ProjectID/ArchiveID')
     if x is None:continue
     acc=x.get('accession');title=txt(node,'./Project/ProjectDescr/Title');desc=txt(node,'./Project/ProjectDescr/Description');pub=[{'tag':n.tag,'attributes':n.attrib,'text':' '.join(n.itertext())} for n in node.iter() if any(k in n.tag.lower() for k in ['publication','pubmed','pmid','doi'])];v=register.setdefault(acc,{'accession':acc,'source_queries':[],'study_title':title,'run_accessions_discovered':[],'raw_source_paths':[]})
     v['project_description']=desc;v['NCBI_project_uid']=node.get('uid');v['publication_fields']=pub
     if qid not in v['source_queries']:v['source_queries'].append(qid)
     if b['raw_path'] not in v['raw_source_paths']:v['raw_source_paths'].append(b['raw_path'])
     bioproject.append({'accession':acc,'uid':node.get('uid'),'title':title,'description':desc,'publication_fields':pub,'query_id':qid,'raw_source_path':b['raw_path'],'raw_project_XML':ET.tostring(node,encoding='unicode')})
   else:
    for article in tree.findall('.//PubmedArticle'):
     pmid=txt(article,'./MedlineCitation/PMID');doi=next((x.text for x in article.findall('./PubmedData/ArticleIdList/ArticleId') if x.get('IdType')=='doi'),'') or '';pmcid=next((x.text for x in article.findall('./PubmedData/ArticleIdList/ArticleId') if x.get('IdType')=='pmc'),'') or '';pid=pmap.get(pmid) or dmap.get(doi.lower()) or 'ODS-PMID'+pmid;ab=' '.join(' '.join(n.itertext()) for n in article.findall('.//Abstract/AbstractText'));title=txt(article,'./MedlineCitation/Article/ArticleTitle');year=txt(article,'./MedlineCitation/Article/Journal/JournalIssue/PubDate/Year') or txt(article,'./MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate')[:4];authors=[txt(a,'LastName')+', '+txt(a,'ForeName') for a in article.findall('.//AuthorList/Author')];acc=sorted(set(re.findall(r'PRJ(?:NA|EB|DB)\d+|SRP\d+|ERP\d+|CRA\d{6,}',ET.tostring(article,encoding='unicode'))));r=papers.setdefault(pmid,{'paper_id':pid,'pmid':pmid,'pmcid':pmcid,'title':title,'year':year,'journal':txt(article,'./MedlineCitation/Article/Journal/Title'),'doi':doi,'authors':authors,'abstract':ab,'existing_literature_id':pid if not pid.startswith('ODS-') else None,'newly_discovered_paper':pid.startswith('ODS-'),'project_accessions':acc,'source_queries':[],'source_paths':[],'review_status':'未开始项目关联/方法筛查','reading_level':'官方PubMed元数据/摘要已保存，未因此声称已语义审阅或全文核实'})
     if qid not in r['source_queries']:r['source_queries'].append(qid)
     if b['raw_path'] not in r['source_paths']:r['source_paths'].append(b['raw_path'])
 dump(ROOT/'NCBI_BioProject_discovery_records.json',bioproject);dump(ROOT/'discovered_projects.json',list(register.values()));dump(ROOT/'paper_discovery_candidates.json',list(papers.values()));print('project_candidates',len(register),'BioProject_records',len(bioproject),'paper_candidates',len(papers))
if __name__=='__main__':run()
