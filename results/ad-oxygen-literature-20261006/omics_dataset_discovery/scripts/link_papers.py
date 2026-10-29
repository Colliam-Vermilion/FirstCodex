from review_dependency import review_json
"""Project-publication and PubMed-SRA links, retaining exact official evidence."""
import json,re,time,xml.etree.ElementTree as ET,urllib.parse
from common import ROOT,dump,now,fetch,getjson,url
from collect_projects import parse_sra
BASE='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def txt(e,path):
 n=e.find(path);return ' '.join(' '.join(n.itertext()).split()) if n is not None else ''
def run():
 candidates=json.loads((ROOT/'paper_discovery_candidates.json').read_text());links=json.loads((ROOT/'existing_project_links.json').read_text());cmap={x['pmid']:x for x in candidates};oldcat=review_json('catalog.json');dmap={x.get('doi','').lower():x['id'] for x in oldcat if x.get('doi')};pmap={x.get('pmid'):x['id'] for x in oldcat if x.get('pmid')};existingids={x['paper_id'] for x in json.loads((ROOT/'existing_articles_availability_audit.json').read_text())};registered=json.loads((ROOT/'NCBI_BioProject_discovery_records.json').read_text());relationships=[];project_meta=[];pmid_needed=set()
 for folder in sorted((ROOT/'project_cache').iterdir()):
  acc=folder.name;previous=[x for x in registered if x['accession']==acc];b=None;m={}
  if previous:
   for row in previous:
    for pub in row['publication_fields']:
     val=pub['attributes'].get('id','');kind='PMID' if val.isdigit() else ('DOI' if val.startswith('10.') else None)
     if kind:relationships.append({'project':acc,'identifier_type':kind,'identifier':val,'evidence':'官方BioProject Publication字段','raw_source':row['raw_source_path']});pmid_needed.update([val] if kind=='PMID' else [])
   continue
  uid=None
  if acc.startswith('PRJNA'):uid=acc[5:]
  else:
   j,m=getjson(url(BASE+'esearch.fcgi',db='bioproject',term=acc,retmode='json',retmax=20),'NCBI');ids=(j or {}).get('esearchresult',{}).get('idlist',[])
   if len(ids)==1:uid=ids[0]
   time.sleep(.4)
  if uid:
   b,m=fetch(url(BASE+'efetch.fcgi',db='bioproject',id=uid,retmode='xml'),'NCBI');time.sleep(.4)
  if not b:continue
  tree=ET.fromstring(b)
  for node in tree.findall('.//DocumentSummary'):
   arch=node.find('./Project/ProjectID/ArchiveID')
   if arch is None or arch.get('accession')!=acc:continue
   project_meta.append({'accession':acc,'title':txt(node,'./Project/ProjectDescr/Title'),'description':txt(node,'./Project/ProjectDescr/Description'),'raw_source':m['raw_path'],'raw_project_XML':ET.tostring(node,encoding='unicode')})
   for pub in node.findall('.//Publication'):
    val=pub.get('id','');kind='PMID' if val.isdigit() else ('DOI' if val.startswith('10.') else None)
    if kind:relationships.append({'project':acc,'identifier_type':kind,'identifier':val,'evidence':'官方BioProject Publication字段','raw_source':m['raw_path']});pmid_needed.update([val] if kind=='PMID' else [])
 dump(ROOT/'project_publication_relations.json',relationships);dump(ROOT/'additional_BioProject_descriptions.json',project_meta)
 # Paper→SRA links use repeated id parameters to preserve the PMID per LinkSet.
 elinks=[];uids_to_pmids={}
 for off in range(0,len(candidates),50):
  ids=[x['pmid'] for x in candidates[off:off+50]];u=BASE+'elink.fcgi?'+urllib.parse.urlencode([('dbfrom','pubmed'),('db','sra'),('retmode','xml')]+[('id',i) for i in ids]);b,m=fetch(u,'NCBI');time.sleep(.4)
  if not b:continue
  for node in ET.fromstring(b).findall('./LinkSet'):
   pmids=[x.text for x in node.findall('./IdList/Id')];sra=[x.text for l in node.findall('./LinkSetDb') if l.findtext('DbTo')=='sra' for x in l.findall('./Link/Id')]
   for p in pmids:
    elinks.append({'pmid':p,'SRA_uids':sra,'official_source':m['raw_path'],'link':'PubMed→SRA'})
    for uid in sra:uids_to_pmids.setdefault(uid,[]).append(p)
 dump(ROOT/'paper_to_SRA_links.json',elinks)
 already={uid for p in (ROOT/'project_cache').glob('*/ncbi_sra_uids.json') for uid in json.loads(p.read_text())};newuids=sorted(set(uids_to_pmids)-already);packets=[]
 for off in range(0,len(newuids),100):
  b,m=fetch(url(BASE+'efetch.fcgi',db='sra',id=','.join(newuids[off:off+100]),retmode='xml'),'NCBI');time.sleep(.4)
  if b:packets.append({'uid_batch':newuids[off:off+100],'rows':parse_sra(b),'source':m['raw_path']})
 dump(ROOT/'paper_linked_SRA_additional_metadata.json',packets)
 # Resolve linked SRA uids using parsed package EXPERIMENT accession→UID.
 uid_run={}
 for p in (ROOT/'project_cache').glob('*/ncbi_sra_packages.json'):
  uids=json.loads((p.parent/'ncbi_sra_uids.json').read_text())
  # No order-based association. Cross-link uid by NCBI search only in XML below.
 for log in (ROOT/'raw/NCBI').glob('*.body'):
  try:
   tree=ET.fromstring(log.read_bytes())
  except Exception:continue
  for pkg in tree.findall('.//EXPERIMENT_PACKAGE'):
   study=pkg.find('STUDY');ex=pkg.find('EXPERIMENT')
   if study is None or ex is None:continue
   project=next((x.text for x in study.findall('./IDENTIFIERS/EXTERNAL_ID') if x.get('namespace')=='BioProject'),None)
   if not project:continue
   # SRA uid is explicit EXPERIMENT/IDENTIFIERS/PRIMARY_ID? That's SRX, not numeric.
   # Instead map each PMID's linked uid to an efetch record from a one-uid request
   # only when needed later. Do not infer numeric uid order from XML record order.
 # PubMed metadata: fetch missing official linked PMIDs, reuse cached candidates first.
 missing=sorted(pmid_needed-set(cmap))
 for off in range(0,len(missing),100):
  b,m=fetch(url(BASE+'efetch.fcgi',db='pubmed',id=','.join(missing[off:off+100]),retmode='xml'),'NCBI');time.sleep(.4)
  if not b:continue
  for node in ET.fromstring(b).findall('./PubmedArticle'):
   pmid=txt(node,'./MedlineCitation/PMID');doi=next((x.text for x in node.findall('./PubmedData/ArticleIdList/ArticleId') if x.get('IdType')=='doi'),'') or '';pmcid=next((x.text for x in node.findall('./PubmedData/ArticleIdList/ArticleId') if x.get('IdType')=='pmc'),'') or '';pid=pmap.get(pmid) or dmap.get(doi.lower()) or 'ODS-PMID'+pmid;cmap[pmid]={'paper_id':pid,'pmid':pmid,'pmcid':pmcid,'title':txt(node,'./MedlineCitation/Article/ArticleTitle'),'doi':doi,'year':txt(node,'./MedlineCitation/Article/Journal/JournalIssue/PubDate/Year'),'journal':txt(node,'./MedlineCitation/Article/Journal/Title'),'abstract':' '.join(' '.join(x.itertext()) for x in node.findall('.//Abstract/AbstractText')),'project_accessions':[],'existing_literature_id':pid if not pid.startswith('ODS-') else None,'newly_discovered_paper':pid.startswith('ODS-'),'source_paths':[m['raw_path']],'source_queries':['official_project_publication_backlink']}
 linked=[]
 for p in cmap.values():
  pp=[x for x in relationships if x['identifier_type']=='PMID' and x['identifier']==p['pmid'] or x['identifier_type']=='DOI' and x['identifier'].lower()==p.get('doi','').lower()]
  rawacc=[a for a in p.get('project_accessions',[]) if a.startswith('PRJ')];projectacc=sorted(set(rawacc+[x['project'] for x in pp]))
  if not projectacc or p['paper_id'] in existingids:continue
  p.update(project_accessions=projectacc,project_link_evidence=pp or [{'evidence':'官方PubMed记录中明确项目编号；具体字段/读深须核','source_paths':p['source_paths']}],reading_level='关联元数据/摘要；未据此声称完整方法已核实',availability='随官方项目状态，不由论文摘要推断公开性');linked.append(p)
 dump(ROOT/'new_associated_papers.json',linked);dump(ROOT/'paper_discovery_candidates_enriched.json',list(cmap.values()));print('project_publication_relations',len(relationships),'PMID-SRA linked',sum(bool(x['SRA_uids']) for x in elinks),'additional_SRAuids',len(newuids),'linked_papers',len(linked),flush=True)
if __name__=='__main__':run()
