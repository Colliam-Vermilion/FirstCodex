#!/usr/bin/env python3
"""Bulk metadata enrichment: reuse cached works and never requery the prior20."""
import datetime as dt,hashlib,json,os,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'all_pool'
TZ=dt.timezone(dt.timedelta(hours=8))
def now():return dt.datetime.now(TZ).isoformat()
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def doi(x):return (x or '').lower().split('doi.org/')[-1].strip()
def run():
 start=time.monotonic();began=now();OUT.mkdir(exist_ok=True)
 if not (OUT/'baseline_catalog.json').exists():
  for name in ['catalog.json','screening.json','remaining_queue.json','processing_order.json','summary.json']:(OUT/('baseline_'+name)).write_bytes((ROOT/name).read_bytes())
  dump(OUT/'baseline.json',{'source_commit':'625dac5eb84d06fb15e5ff7d884f475730f9af06','started_Asia_Shanghai':began,'pool':1536,'screened':20,'remaining':1516,'original20_evaluations_sha256':hashlib.sha256((ROOT/'reading_priority/evaluations.json').read_bytes()).hexdigest()})
 cat=json.loads((OUT/'baseline_catalog.json').read_text());cache={};orig20=set()
 paths=list((ROOT/'raw/openalex').glob('*.json'))+list((OUT/'raw').glob('*.json'))+[ROOT/'reading_priority/raw/openalex_citations_20.json']
 for p in paths:
  try:j=json.loads(p.read_text())
  except Exception:continue
  for w in j.get('results',[]):
   d=doi(w.get('doi'))
   if d:cache[d]={'work':w,'source_path':str(p.relative_to(ROOT)),'query_date':'2026-10-24','reused':not str(p).startswith(str(OUT))}
   if p.name=='openalex_citations_20.json' and d:orig20.add(d)
 need=sorted({r['doi'] for r in cat if r.get('doi') and r['doi'] not in cache});batch_requests=[]
 contact=os.environ.get('OPENALEX_MAILTO') or os.environ.get('NATURE_CONTACT_EMAIL')
 cfg=Path('/workspace/tools/nature-runtime/config/contact.json')
 if not contact and cfg.exists():contact=json.loads(cfg.read_text()).get('contact_email')
 print('pool',len(cat),'cached_work_DOIs',len(cache),'prior20_reused',len(orig20),'uncached_DOIs',len(need),flush=True)
 for i in range(0,len(need),45):
  ds=need[i:i+45];key=hashlib.sha256('|'.join(ds).encode()).hexdigest()[:14];dest=OUT/'raw'/f'openalex_{key}.json';params={'filter':'doi:'+'|'.join('https://doi.org/'+d for d in ds),'per-page':100,'select':'id,doi,title,publication_date,publication_year,cited_by_count,primary_location,ids,abstract_inverted_index,type'}
  event={'batch':i//45+1,'dois':ds,'started_Asia_Shanghai':now(),'endpoint':'https://api.openalex.org/works','params_without_contact':params,'path':str(dest.relative_to(ROOT))}
  if set(ds)&orig20:raise ValueError('Do not requery prior20')
  try:
   if dest.exists():j=json.loads(dest.read_text());event['cache_hit']=True
   else:
    sent=dict(params)
    if contact:sent['mailto']=contact
    with urlopen(Request('https://api.openalex.org/works?'+urlencode(sent),headers={'User-Agent':'OxygenResponseWholePool/1.0'}),timeout=40) as r:body=r.read();event['status']=r.status
    j=json.loads(body);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body);event['bytes']=len(body);event['sha256']=hashlib.sha256(body).hexdigest()
    time.sleep(1.1)
   event['returned']=len(j.get('results',[]))
   for w in j.get('results',[]):
    d=doi(w.get('doi'))
    if d in ds:cache[d]={'work':w,'source_path':str(dest.relative_to(ROOT)),'query_date':'2026-10-24','reused':False}
  except Exception as e:
   event['error']=type(e).__name__+': '+str(e)[:150];event['returned']=0
  event['finished_Asia_Shanghai']=now();batch_requests.append(event);dump(OUT/'metadata_requests.json',batch_requests)
  print('metadata',i//45+1,'requested',len(ds),'returned',event['returned'],'error',event.get('error',''),flush=True)
  # A source/credential/quota failure does not block screening; do not retry
  # the same batch endlessly or individually chase missing impact metrics.
  if '429' in event.get('error',''):break
 dump(OUT/'openalex_work_cache.json',cache)
 enrich=[]
 for r in cat:
  c=cache.get(r.get('doi',''));w=c['work'] if c else {};inv=w.get('abstract_inverted_index') or {};pos={i:word for word,ii in inv.items() for i in ii};source=(w.get('primary_location') or {}).get('source') or {}
  enrich.append({'id':r['id'],'doi':r.get('doi',''),'title':r['title'],'year':r.get('year',''),'journal':r.get('journal',''),'openalex_id':w.get('id') or r.get('openalex_id'),'citation_count':w.get('cited_by_count'),'citation_source':'OpenAlex' if c else None,'citation_query_date':c['query_date'] if c else None,'citation_raw_path':c['source_path'] if c else None,'citation_cache_reused':c['reused'] if c else False,'publication_date_for_age':w.get('publication_date'),'journal_source_name':source.get('display_name'),'issn_l':source.get('issn_l'),'issns':source.get('issn') or [],'abstract_enriched':r.get('abstract') or ' '.join(pos[k] for k in sorted(pos)),'abstract_from':'existing' if r.get('abstract') else ('OpenAlex inverted index' if pos else 'missing'),'openalex_type':w.get('type'),'metric_missing_reason':None if c else ('no DOI; bulk identity lookup deferred' if not r.get('doi') else 'not matched/temporarily unavailable; left blank, not zero')})
 dump(OUT/'metadata_enrichment.json',enrich)
 result={'stage':'metadata','started_Asia_Shanghai':began,'finished_Asia_Shanghai':now(),'measured_wall_seconds':round(time.monotonic()-start,3),'pool':len(cat),'citations_available':sum(x['citation_count'] is not None for x in enrich),'prior20_not_requeried':len(orig20),'new_bulk_requests':sum(not x.get('cache_hit') for x in batch_requests),'missing_citations':sum(x['citation_count'] is None for x in enrich),'abstracts_available':sum(bool(x['abstract_enriched']) for x in enrich),'missing_values_not_zero':True}
 dump(OUT/'metadata_stage.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':run()
