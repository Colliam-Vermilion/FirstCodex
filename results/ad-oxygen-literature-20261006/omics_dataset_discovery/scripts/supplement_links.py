from review_dependency import review_json
"""Complete bounded official publication backlinks and assembly checks; no read download."""
import json,re,time,xml.etree.ElementTree as ET
from common import ROOT,dump,now,fetch,getjson,url
from parse_discovery import txt
BASE='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def run():
 ass=json.loads((ROOT/'project_assessments.json').read_text());rel=json.loads((ROOT/'project_publication_relations.json').read_text());old=review_json('catalog.json');dm={x.get('doi','').lower():x['id'] for x in old if x.get('doi')};pm={str(x.get('pmid')):x['id'] for x in old if x.get('pmid')};existing={x['paper_id'] for x in json.loads((ROOT/'existing_articles_availability_audit.json').read_text())};papers={p['pmid']:p for p in json.loads((ROOT/'paper_discovery_candidates_enriched.json').read_text()) if p.get('pmid')};linked={p['paper_id']:p for p in json.loads((ROOT/'new_associated_papers.json').read_text())};logs=json.loads((ROOT/'search_log.json').read_text());checks=[]
 # Fetch twenty PRJNA records in one call; full response saved by fetch().
 ids=[a[5:] for a in ass if a.startswith('PRJNA') and ass[a].get('audit_batch')=='D004']
 b,m=fetch(url(BASE+'efetch.fcgi',db='bioproject',id=','.join(ids),retmode='xml'),'NCBI');time.sleep(.4)
 if b:
  for n in ET.fromstring(b).findall('.//DocumentSummary'):
   arch=n.find('./Project/ProjectID/ArchiveID')
   if arch is None:continue
   acc=arch.get('accession')
   for p in n.findall('.//Publication'):
    val=p.get('id','');kind='PMID' if val.isdigit() else 'DOI' if val.startswith('10.') else None
    if kind:
     v={'project':acc,'identifier_type':kind,'identifier':val,'evidence':'官方BioProject Publication字段','raw_source':m['raw_path']}
     if not any(x['project']==acc and x['identifier']==val for x in rel):rel.append(v)
 # A few targeted trace queries follow real project descriptions, not a fresh library rescreen.
 for qid,q in [('P05','"microaerophilic activated sludge"'),('P06','"Methane oxidation as a community function"'),('P07','"Transcriptome-SIP"'),('P08','"Intermittent Oxygen Supply" AND "Trichloroethene"')]:
  if any(x.get('query_id')==qid and x.get('complete') for x in logs):continue
  event={'query_id':qid,'database':'NCBI pubmed','query':q,'reason':'追踪已发现项目的关联论文','started_utc':now(),'pages':[],'fetch_batches':[],'complete':False};ids=[];off=0
  while True:
   j,meta=getjson(url(BASE+'esearch.fcgi',db='pubmed',term=q,retmode='json',retmax=1000,retstart=off),'NCBI');time.sleep(.4);event['pages'].append({'offset':off,'status':meta.get('status'),'raw_path':meta.get('raw_path')})
   if not j or 'esearchresult' not in j:break
   e=j['esearchresult'];ids+=e.get('idlist',[]);event['reported_count']=int(e['count']);event['query_translation']=e.get('querytranslation');event['warninglist']=e.get('warninglist')
   if len(ids)>=int(e['count']):event['complete']=True;break
   if not e.get('idlist'):break
   off+=1000
  event['id_count']=len(ids)
  for off in range(0,len(ids),100):
   data,meta=fetch(url(BASE+'efetch.fcgi',db='pubmed',id=','.join(ids[off:off+100]),retmode='xml'),'NCBI');time.sleep(.4);event['fetch_batches'].append({'offset':off,'uids':ids[off:off+100],'status':meta.get('status'),'raw_path':meta.get('raw_path')})
  event['finished_utc']=now();logs.append(event);dump(ROOT/'search_ids'/f'{qid}.json',ids)
 # Fetch linked PMIDs absent from all cached article metadata, then parse all new responses.
 missing=sorted({x['identifier'] for x in rel if x['identifier_type']=='PMID'}-set(papers));batches=[]
 for off in range(0,len(missing),100):
  b,m=fetch(url(BASE+'efetch.fcgi',db='pubmed',id=','.join(missing[off:off+100]),retmode='xml'),'NCBI');time.sleep(.4)
  if b:batches.append(m['raw_path'])
 batches += [v['raw_path'] for e in logs if e.get('query_id') in ['P05','P06','P07','P08'] for v in e.get('fetch_batches',[]) if v['status']==200]
 for raw in batches:
  for n in ET.fromstring((ROOT/raw).read_bytes()).findall('./PubmedArticle'):
   pmid=txt(n,'./MedlineCitation/PMID');doi=next((x.text for x in n.findall('./PubmedData/ArticleIdList/ArticleId') if x.get('IdType')=='doi'),'') or '';pid=pm.get(pmid) or dm.get(doi.lower()) or 'ODS-PMID'+pmid
   p=papers.setdefault(pmid,{'paper_id':pid,'pmid':pmid,'doi':doi,'title':txt(n,'./MedlineCitation/Article/ArticleTitle'),'year':txt(n,'./MedlineCitation/Article/Journal/JournalIssue/PubDate/Year'),'journal':txt(n,'./MedlineCitation/Article/Journal/Title'),'abstract':' '.join(' '.join(a.itertext()) for a in n.findall('.//Abstract/AbstractText')),'existing_literature_id':None if pid.startswith('ODS-') else pid,'newly_discovered_paper':pid.startswith('ODS-'),'source_paths':[raw],'source_queries':['project_trace_backlink'],'project_accessions':[],'reading_level':'官方元数据/摘要，非全文核实'})
   p['project_accessions']=sorted(set(p.get('project_accessions',[])+re.findall(r'PRJ(?:NA|EB|DB)\d+',ET.tostring(n,encoding='unicode'))))
 for p in papers.values():
  prs=[r for r in rel if (r['identifier_type']=='PMID' and r['identifier']==p['pmid']) or (r['identifier_type']=='DOI' and r['identifier'].lower()==p.get('doi','').lower())]
  pp=sorted(set([x for x in p.get('project_accessions',[]) if x.startswith('PRJ')]+[x['project'] for x in prs]))
  if pp and p['paper_id'] not in existing:
   p.update(project_accessions=pp,project_link_evidence=p.get('project_link_evidence',[])+[r for r in prs if r not in p.get('project_link_evidence',[])],availability='以官方项目审计为准；论文关联不等于目标类型或公开状态');linked[p['paper_id']]=p
 # Check whether three no-raw project records actually expose public assemblies.
 for acc in ['PRJNA301899','PRJNA818156','PRJNA1186224']:
  j,m=getjson(url(BASE+'esearch.fcgi',db='assembly',term=acc,retmode='json',retmax=1000),'NCBI');time.sleep(.4);e=(j or {}).get('esearchresult',{});ids=e.get('idlist',[]);item={'project_id':acc,'database':'NCBI Assembly','query':acc,'reported_count':int(e['count']) if e.get('count') else None,'returned_ids':ids,'raw_source':m.get('raw_path'),'complete':len(ids)==int(e.get('count',-1)),'assembly_records':[],'checked_utc':now()}
  for off in range(0,len(ids),100):
   s,meta=getjson(url(BASE+'esummary.fcgi',db='assembly',id=','.join(ids[off:off+100]),retmode='json'),'NCBI');time.sleep(.4)
   if s:item['assembly_records'] += [{'uid':u,'metadata':s.get('result',{}).get(u),'raw_source':meta['raw_path']} for u in s.get('result',{}).get('uids',[])]
  checks.append(item)
 dump(ROOT/'project_publication_relations.json',rel);dump(ROOT/'new_associated_papers.json',list(linked.values()));dump(ROOT/'paper_discovery_candidates_enriched.json',list(papers.values()));dump(ROOT/'search_log.json',logs);dump(ROOT/'assembly_status_checks.json',checks)
 print('association papers',len(linked),'new to old catalog',sum(p.get('newly_discovered_paper',False) for p in linked.values()),'assemblychecks',[(x['project_id'],x['reported_count']) for x in checks],flush=True)
if __name__=='__main__':run()
