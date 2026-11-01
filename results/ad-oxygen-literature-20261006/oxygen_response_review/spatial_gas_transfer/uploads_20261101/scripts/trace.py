import requests,json,datetime
from pathlib import Path
R=Path('/workspace/FirstCodex');P=R/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer/uploads_20261101';S=requests.Session();log=[]
for key,d in [('Wessel','10.1128/mbio.00992-14'),('Berg','10.1002/bit.27522')]:
 try:
  u='https://api.openalex.org/works/https://doi.org/'+d;r=S.get(u,timeout=25);(P/'raw'/f'{key}_identity.json').write_text(r.text);r.raise_for_status();w=r.json();u='https://api.openalex.org/works';params={'filter':'cites:'+w['id'].split('/')[-1],'per-page':200,'page':1};r=S.get(u,params=params,timeout=30);(P/'raw'/f'{key}_citing_page1.json').write_text(r.text);r.raise_for_status();j=r.json();log.append({'seed':d,'source':'OpenAlex official API','direction':'forward','params':params,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':j['meta']['count'],'returned':len(j['results']),'complete':j['meta']['count']<=200,'reading_status':'元数据取回；不计已筛或纳入','raw_path':str((P/'raw'/f'{key}_citing_page1.json').relative_to(R))})
 except Exception as e:log.append({'seed':d,'error':str(e),'complete':False})
(P/'citation_trace_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2));print(log)
