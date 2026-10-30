"""One minimal request per official API. Inherited proxy/TLS; no credentials logged."""
import json,time,re
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from urllib.parse import urlsplit
import requests

OUT=Path(__file__).resolve().parents[1]/'raw/preflight/20261030_retest'
QUERIES=[
 ('crossref','https://api.crossref.org/works/10.1128/AEM.01426-07'),
 ('pubmed','https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=10.1128%2FAEM.01426-07%5Bdoi%5D&retmode=json&retmax=1'),
 ('openalex','https://api.openalex.org/works/https://doi.org/10.1128/AEM.01426-07'),
 ('europepmc','https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1128%2FAEM.01426-07&format=json&pageSize=1')]
def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 for name,url in QUERIES:
  t=datetime.now(timezone.utc);start=time.monotonic()
  row={'source':name,'url':url,'hostname':urlsplit(url).hostname,'started_utc':t.isoformat(),'started_Asia_Shanghai':t.astimezone(ZoneInfo('Asia/Shanghai')).isoformat(),'attempts':1,'proxy_inherited':True,'TLS_verification':True,'target_http_status':None,'valid_target_JSON_XML':False}
  try:
   r=requests.get(url,timeout=(15,30),headers={'User-Agent':'FirstCodex-literature-connectivity-diagnostic/1.0'},allow_redirects=False)
   row.update(target_http_status=r.status_code,response_content_type=r.headers.get('Content-Type'),retry_after=r.headers.get('Retry-After'),response_bytes=len(r.content))
   (OUT/(name+'.body')).write_bytes(r.content)
   try:
    data=r.json()
    valid={'crossref':lambda d:d.get('status')=='ok' and bool(d.get('message',{}).get('DOI')),'pubmed':lambda d:'esearchresult' in d,'openalex':lambda d:bool(d.get('id')) and 'title' in d,'europepmc':lambda d:'resultList' in d and 'hitCount' in d}[name](data)
    row['valid_target_JSON_XML']=bool(r.ok and valid)
   except (ValueError,TypeError,AttributeError):pass
   row['failure_layer']='none' if row['valid_target_JSON_XML'] else 'target_http' if r.status_code in (403,429) else 'http_response_not_validated'
  except requests.exceptions.ProxyError as e:
   match=re.search(r'Tunnel connection failed: (\d+) ([^\r\n\"\)]+)',str(e))
   row.update(failure_layer='proxy_CONNECT' if match else 'proxy_connection',proxy_connect_status=int(match.group(1)) if match else None,error='Tunnel connection failed: '+match.group(1)+' '+match.group(2).strip(" '\\") if match else 'Proxy connection exception; credential-bearing exception text intentionally omitted')
  except requests.exceptions.SSLError:row.update(failure_layer='TLS',error='TLS verification failed')
  except requests.exceptions.Timeout:row.update(failure_layer='timeout',error='Connection/read timeout')
  except requests.exceptions.RequestException as e:row.update(failure_layer='transport',error=type(e).__name__)
  row['elapsed_seconds']=round(time.monotonic()-start,3);row['finished_utc']=datetime.now(timezone.utc).isoformat();rows.append(row)
  (OUT/'requests.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps(row,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
