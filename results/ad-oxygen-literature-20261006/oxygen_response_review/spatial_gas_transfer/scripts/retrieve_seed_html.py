import sys,json
sys.path.insert(0,'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/scripts')
from online_search import get
from prepare import T,read,dump
from bs4 import BeautifulSoup
out=[]
for s in read(T/'seed_pubmed_results.json')[:2]:
 b,path=get('https://pmc.ncbi.nlm.nih.gov/articles/'+s['pmcid']+'/',{},'PMC',s['seed_key']+'_public_html')
 soup=BeautifulSoup(b,'html.parser')
 for x in soup(['script','style','nav']):x.decompose()
 text=soup.get_text(' ',strip=True)
 dest=T/'evidence'/(s['seed_key']+'_official_fulltext.txt');dest.write_text(text)
 out.append({'seed_key':s['seed_key'],'raw_path':path,'text_path':str(dest.relative_to(T)),'characters':len(text),'xml_note':'EUtilities response has front matter only, publisher disallows full-text XML download; not counted as full text','reading_state':'public HTML obtained; verify body before counting'})
dump(T/'seed_fulltext_retrieval.json',out)
