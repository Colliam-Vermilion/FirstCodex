#!/usr/bin/env python3
"""Targeted metadata/claim checks for reading priorities, not discovery reruns."""
import datetime as dt,hashlib,json,os,time,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reading_priority';RAW=OUT/'raw'
def dump(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def fetch(name,endpoint,params,xml=False):
 path=RAW/(name+('.xml' if xml else '.json'));path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():return path.read_bytes()
 query=dict(params);contact=os.environ.get('NATURE_CONTACT_EMAIL') or os.environ.get('PUBMED_EMAIL')
 cfg=Path('/workspace/tools/nature-runtime/config/contact.json')
 if not contact and cfg.exists():contact=json.loads(cfg.read_text()).get('contact_email')
 if contact and 'openalex' in endpoint:query['mailto']=contact
 if contact and 'eutils' in endpoint:query['email']=contact
 for attempt in range(3):
  try:
   with urlopen(Request(endpoint+'?'+urlencode(query),headers={'User-Agent':'OxygenMechanismPriorityAudit/1.0'}),timeout=45) as r:body=r.read();status=r.status
   ET.fromstring(body) if xml else json.loads(body)
   path.write_bytes(body)
   e={'name':name,'url_without_contact':endpoint+'?'+urlencode(params),'status':status,'queried_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'queried_Asia_Shanghai':dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(),'path':str(path.relative_to(ROOT)),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
   with (OUT/'request_log.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(e,ensure_ascii=False)+'\n')
   time.sleep(.5);return body
  except Exception as exc:
   if attempt==2:raise
   time.sleep(2*(attempt+1))
def run():
 cat={r['id']:r for r in json.loads((ROOT/'catalog.json').read_text())};sel=json.loads((ROOT/'screening.json').read_text())
 dois=[cat[r['id']]['doi'] for r in sel]
 try:
  j=json.loads(fetch('openalex_citations_20','https://api.openalex.org/works',{'filter':'doi:'+'|'.join('https://doi.org/'+d for d in dois),'per-page':50}))
  print('OpenAlex citation records',len(j.get('results',[])),flush=True)
 except Exception as e:dump(OUT/'citation_failure.json',{'status':'failed','error':str(e)[:180],'missing_is_not_zero':True});print('citation error',type(e).__name__,flush=True)
 # Already retrieved candidates/reference PMIDs only; focused checks, no broad
 # keyword queries and no advancing the main screening queue.
 support=['23093671','32900801','39547298','14749831','11260473','18161989','29559534','8226748']
 selected=[r['pmid'] for r in sel]
 b=fetch('pubmed_selected_and_support','https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',{'db':'pubmed','id':','.join(selected+support),'retmode':'xml'},True)
 root=ET.fromstring(b);print('targeted PubMed records',len(root.findall('PubmedArticle')),flush=True)
 for a in root.findall('PubmedArticle'):
  pm=a.findtext('MedlineCitation/PMID');ids={x.get('IdType'):''.join(x.itertext()) for x in a.findall('PubmedData/ArticleIdList/ArticleId')}
  if pm in ['23093671','32900801','29559534'] and ids.get('pmc'):
   try:
    data=fetch('PMC_'+pm,'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',{'db':'pmc','id':ids['pmc'].replace('PMC',''),'retmode':'xml'},True);rr=ET.fromstring(data);print(pm,'body_paragraphs',len(rr.findall('.//body//p')),flush=True)
   except Exception as e:print(pm,type(e).__name__,flush=True)
if __name__=='__main__':run()
