import sys,json,os,urllib.parse,xml.etree.ElementTree as E,pathlib
sys.path.insert(0,'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/scripts')
from online_search import get,blocked
from prepare import T,read,dump,now
q=read(T/'online_query_queue.json');logs=read(T/'online_search_log.json')
# Standard page endpoint is tested once; no key creation or credential changes.
for n in [9,10,11]:
 row=logs[n]
 if row.get('status')=='completed':continue
 row['continuation_attempt_started_utc']=now(); blocked.clear()
 page=2 if n==9 else 1
 try:
  while True:
   b,path=get('https://api.openalex.org/works',{'search':q[n]['query_verbatim'],'filter':'to_publication_date:2026-10-30','per-page':200,'page':page},'OpenAlex',q[n]['query_id']+'_numbered_'+str(page))
   d=json.loads(b);items=d.get('results',[])
   row['pages'].append({'page':page,'records':len(items),'raw_path':path});row['reported_count']=d['meta']['count'];row['retrieved_records']+=len(items)
   if not items or page*200>=row['reported_count']:break
   page+=1
  row['status']='completed';row['pagination_note']='cursor continuation required API key; documented numbered-page endpoint accepted; entire result set fetched without key'
 except Exception as e:row['status']='failed_or_partial';row['continuation_error']=str(e)
 row['finished_utc']=now();dump(T/'online_search_log.json',logs)
 print(row['query_id'],row['status'],row['retrieved_records'],flush=True)
# Official PubMed DOI lookup and metadata/full text of all five seeds.
seedmeta=[]
for s in read(T/'seed_audit.json'):
 blocked.clear();doi=s['supplied_doi'];sid=s['seed_key']
 b,path=get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',{'db':'pubmed','term':doi+'[AID]','retmode':'json','retmax':100},'PubMed',sid+'_doi_lookup')
 ids=json.loads(b)['esearchresult']['idlist'];r={'seed_key':sid,'lookup_path':path,'pmids':ids}
 if ids:
  b,path=get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',{'db':'pubmed','id':','.join(ids),'retmode':'xml'},'PubMed',sid+'_metadata');r['metadata_path']=path
  root=E.fromstring(b)
  for a in root.findall('.//PubmedArticle'):
   ai={x.get('IdType'):x.text for x in a.findall('./PubmedData/ArticleIdList/ArticleId')}
   if ai.get('pmc'):
    r['pmcid']=ai['pmc'];b,path=get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',{'db':'pmc','id':ai['pmc'].replace('PMC',''),'retmode':'xml'},'PMC',sid+'_fulltext');r['fulltext_path']=path
 seedmeta.append(r);dump(T/'seed_pubmed_results.json',seedmeta)
print('seeds metadata/fulltext retrieval finished',flush=True)
