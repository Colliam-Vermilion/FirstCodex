"""Reuse official public PMC pages; check body and keep scanned-only limitations."""
import json
from bs4 import BeautifulSoup
from online_search import get,blocked
from prepare import T,read,dump
out=read(T/'selected_fulltext_retrieval.json') if (T/'selected_fulltext_retrieval.json').exists() else []
a=read(T/'online_pubmed_reading_packet.json')
for n in [108,114,127,130,132,178]:
 r=a[n];rid=r['id']
 if any(x['id']==rid for x in out):continue
 try:
  blocked.clear();b,path=get('https://pmc.ncbi.nlm.nih.gov/articles/'+r['pmcid']+'/',{},'PMC',rid+'_public_html');soup=BeautifulSoup(b,'html.parser')
  parts=[]
  for sec in soup.select('section'):
   h=sec.find(['h2','h3'],recursive=False)
   if h and h.name=='h2' and h.get_text(' ',strip=True).upper() not in ['REFERENCES','ACKNOWLEDGMENTS','ACTIONS','RESOURCES']:
    parts.append({'id':sec.get('id'),'heading':h.get_text(' ',strip=True),'text':sec.get_text(' ',strip=True)})
  dest='evidence/'+rid+'_body_sections.json';dump(T/dest,parts)
  out.append({'id':rid,'pmcid':r['pmcid'],'raw_path':path,'sections_path':dest,'headings':[x['heading'] for x in parts],'status':'public page saved; sections require reading','has_methods_or_results_section':any('METHOD' in x['heading'].upper() or 'RESULT' in x['heading'].upper() for x in parts)})
 except Exception as e:out.append({'id':rid,'status':'failed','error':str(e)})
 dump(T/'selected_fulltext_retrieval.json',out);print(rid,out[-1].get('headings'),flush=True)
