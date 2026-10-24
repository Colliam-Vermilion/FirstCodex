"""Official BioProject/PubMed grouped discovery, complete ID pagination."""
import json,xml.etree.ElementTree as ET,time,re,hashlib
from common import ROOT,dump,now,fetch,getjson,url
BASE='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
Q=[('N01','bioproject','(microaeration OR microaerobic OR microoxic) AND (metagenom* OR metatranscriptom*)'),('N02','bioproject','("oxygen exposure" OR "oxygen shock" OR "oxygen pulse" OR "oxygen intrusion" OR reoxygenation) AND (anaerob* OR methanogen* OR syntroph* OR sediment OR fermentation) AND (metagenom* OR metatranscriptom*)'),('N03','bioproject','("redox fluctuation" OR "redox oscillation" OR "intermittent aeration" OR "side-stream aeration") AND (metagenom* OR metatranscriptom*)'),('N04','bioproject','oxygen AND ("anaerobic digestion" OR methanogenic OR syntrophic) AND (metatranscriptom* OR "RNA-Seq")'),('P01','pubmed','(microaerat*[Title/Abstract] OR microaerob*[Title/Abstract] OR microoxic[Title/Abstract]) AND (anaerob*[Title/Abstract] OR methanogen*[Title/Abstract] OR syntroph*[Title/Abstract] OR digester*[Title/Abstract] OR fermentation[Title/Abstract]) AND (metagenom*[Title/Abstract] OR metatranscriptom*[Title/Abstract] OR shotgun[Title/Abstract])'),('P02','pubmed','("oxygen exposure" OR "oxygen shock" OR "oxygen pulse" OR "oxygen intrusion" OR "oxygen stress" OR reoxygenation) AND (anaerob* OR methanogen* OR sediment* OR ferment*) AND (metagenom* OR metatranscriptom* OR "RNA-Seq")'),('P03','pubmed','("redox fluctuation" OR "redox oscillation" OR "intermittent aeration" OR "side-stream aeration") AND (anaerob* OR soil OR sediment OR digester) AND (metagenom* OR metatranscriptom*)'),('P04','pubmed','oxygen AND (sediment OR wetland OR peat) AND metatranscriptom*')]
def run():
 for qid,db,query in Q:
  logs=json.loads((ROOT/'search_log.json').read_text()) if (ROOT/'search_log.json').exists() else []
  if any(x.get('query_id')==qid and x.get('complete') for x in logs):continue
  event={'query_id':qid,'database':'NCBI '+db,'query':query,'started_utc':now(),'pages':[],'id_count':None,'complete':False};allids=[];offset=0;count=None
  while True:
   j,m=getjson(url(BASE+'esearch.fcgi',db=db,term=query,retmode='json',retmax=1000,retstart=offset),'NCBI');event['pages'].append({'offset':offset,'status':m.get('status'),'raw_path':m.get('raw_path'),'error':m.get('error')})
   if not j or 'esearchresult' not in j:event['error']='search failed';break
   e=j['esearchresult'];count=int(e['count']);ids=e.get('idlist',[]);event['reported_count']=count;event['query_translation']=e.get('querytranslation');event['warninglist']=e.get('warninglist');event['errorlist']=e.get('errorlist');allids+=ids
   if len(allids)>=count:event['complete']=True;break
   if not ids:event['error']='early empty page';break
   offset+=1000;time.sleep(.4)
  event['id_count']=len(allids);event['fetch_batches']=[]
  for off in range(0,len(allids),100):
   b,m=fetch(url(BASE+'efetch.fcgi',db=db,id=','.join(allids[off:off+100]),retmode='xml'),'NCBI');event['fetch_batches'].append({'offset':off,'uids':allids[off:off+100],'status':m.get('status'),'raw_path':m.get('raw_path')});time.sleep(.4)
  event['all_fetch_batches_succeeded']=all(x['status']==200 for x in event['fetch_batches']);event['finished_utc']=now();dump(ROOT/'search_ids'/f'{qid}.json',allids);logs=json.loads((ROOT/'search_log.json').read_text()) if (ROOT/'search_log.json').exists() else [];logs=[x for x in logs if x.get('query_id')!=qid]+[event];dump(ROOT/'search_log.json',logs);print(qid,'count',count,'IDs',len(allids),'complete',event['complete'],'fetch',event['all_fetch_batches_succeeded'],flush=True);time.sleep(.5)
if __name__=='__main__':run()
