import sys,json
sys.path.insert(0,'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/scripts')
from online_search import get,blocked
from prepare import T,read,dump
from bs4 import BeautifulSoup
out=[]
for rid,pmcid in [('SG-25234D8276BD','PMC91616'),('SG-2DE3F410358B','PMC91175')]:
 blocked.clear()
 try:
  b,path=get('https://pmc.ncbi.nlm.nih.gov/articles/'+pmcid+'/',{},'PMC',rid+'_public_html');soup=BeautifulSoup(b,'html.parser');parts=[]
  for sec in soup.select('section'):
   h=sec.find(['h2','h3'],recursive=False)
   if h and h.name=='h2' and h.get_text(' ',strip=True).upper() not in ['REFERENCES','ACKNOWLEDGMENTS','ACTIONS','RESOURCES']:
    parts.append({'id':sec.get('id'),'heading':h.get_text(' ',strip=True),'text':sec.get_text(' ',strip=True)})
  dest='evidence/'+rid+'_body_sections.json';dump(T/dest,parts);out.append({'id':rid,'pmcid':pmcid,'raw_path':path,'sections_path':dest,'has_body_methods_results':any('METHOD' in x['heading'].upper() for x in parts) and any('RESULT' in x['heading'].upper() for x in parts),'headings':[x['heading'] for x in parts],'page_title':soup.title.get_text() if soup.title else None})
 except Exception as e:out.append({'id':rid,'status':'failed','error':str(e)})
 dump(T/'classic_1999_fulltext_retrieval.json',out);print(out[-1],flush=True)
