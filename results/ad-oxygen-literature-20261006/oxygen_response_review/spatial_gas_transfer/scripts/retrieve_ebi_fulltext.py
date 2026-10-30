import sys,json,xml.etree.ElementTree as E
sys.path.insert(0,'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/scripts')
from online_search import get,blocked
from prepare import T,read,dump
out=[]
for pmcid in ['PMC1317437','PMC7440799','PMC91616','PMC91175']:
 try:
  blocked.clear();b,path=get('https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmcid+'/fullTextXML',{},'EuropePMC',pmcid+'_fullTextXML')
  root=E.fromstring(b);body=root.find('.//body');parts=[]
  if body is not None:
   for sec in body.findall('sec'):parts.append({'id':sec.get('id'),'heading':sec.findtext('title'),'text':' '.join(''.join(sec.itertext()).split())})
  dest='evidence/'+pmcid+'_body_sections.json';dump(T/dest,parts);out.append({'pmcid':pmcid,'raw_path':path,'sections_path':dest,'has_body':body is not None,'sections':len(parts)})
 except Exception as e:out.append({'pmcid':pmcid,'status':'failed','error':str(e)})
 dump(T/'additional_fulltext_retrieval.json',out);print(out[-1],flush=True)
