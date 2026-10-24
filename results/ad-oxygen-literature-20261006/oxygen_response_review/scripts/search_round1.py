#!/usr/bin/env python3
"""Round-one retrieval. Cached raw responses, explicit source limits, no screening.

Run once for a NEW search round; continuation batches must not rerun discovery.
Public APIs; contact read from an environment variable or external runtime file.
"""
import argparse, csv, datetime as dt, hashlib, json, os, re, time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'raw'
DATE = '2026-10-24'

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8'); tmp.replace(path)

def request(qid, source, endpoint, params, tag='search', xml=False):
    dest = RAW / source / f'{qid}_{tag}.{"xml" if xml else "json"}'
    if dest.exists(): return dest.read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    cfg = Path('/workspace/tools/nature-runtime/config/contact.json')
    contact = os.environ.get('NATURE_CONTACT_EMAIL') or os.environ.get('PUBMED_EMAIL')
    if not contact and cfg.exists(): contact = json.loads(cfg.read_text()).get('contact_email')
    sent = dict(params)
    if contact and source in ('pubmed','crossref','openalex'):
        sent['email' if source == 'pubmed' else 'mailto'] = contact
    safe_url = endpoint+'?'+urlencode(params)
    for attempt in range(3):
        try:
            req = Request(endpoint+'?'+urlencode(sent), headers={'User-Agent':'OxygenResponseReview/1.0','Accept':'application/xml' if xml else 'application/json'})
            with urlopen(req,timeout=55) as resp: body=resp.read(); status=resp.status
            if xml: ET.fromstring(body)
            else: json.loads(body)
            dest.write_bytes(body)
            event={'query_id':qid,'source':source,'url_without_contact':safe_url,'status':status,'retrieved_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'path':str(dest.relative_to(ROOT)),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
            with (ROOT/'request_log.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(event,ensure_ascii=False)+'\n')
            time.sleep(.45 if source=='pubmed' else 1.0)
            return body
        except Exception as e:
            if attempt == 2: raise
            time.sleep(2*(attempt+1))

PUBMED = [
 ('P01','methanogen oxygen tolerance','methanogen* AND ("oxygen exposure" OR "oxygen stress" OR "oxygen tolerance" OR aerotolerance OR "oxygen shock")'),
 ('P02','oxygen detoxification enzymes','(anaerob* OR methanogen* OR Clostrid* OR Desulfovibrio) AND (rubrerythrin OR "superoxide reductase" OR flavodiiron) AND (oxygen OR oxidative)'),
 ('P03','gut anaerobe exposure','(Bacteroides OR "Faecalibacterium prausnitzii" OR "Clostridioides difficile") AND ("oxygen exposure" OR aerotolerance OR "oxygen tolerance" OR "oxygen detoxification")'),
 ('P04','syntrophic protection','(syntroph* OR "cross feeding" OR "cross-feeding" OR coculture OR "co-culture") AND (methanogen* OR anaerob*) AND (oxygen OR microoxic) AND (protect* OR scaveng* OR toleran*)'),
 ('P05','spatial protection','(anaerobic OR methanogenic) AND (granul* OR biofilm OR aggregat*) AND ("oxygen gradient" OR microelectrode OR "oxygen penetration" OR "oxygen diffusion")'),
 ('P06','sediment oxygen pulse','(sediment OR "waterlogged soil" OR "paddy soil") AND ("oxygen exposure" OR "oxygen pulse" OR reoxygenation OR "oxygen intrusion") AND (microb* OR methanogen* OR ferment*)'),
 ('P07','redox fluctuation peat wetland','(peat OR wetland OR "flooded soil") AND ("redox fluctuation" OR "redox oscillation" OR reoxygenation OR "oxygen exposure") AND (microb* OR methanogen* OR metabol*)'),
 ('P08','gut oxygen metabolic response','("gut microbiota" OR "intestinal bacteria" OR "gut anaerobes") AND ("oxygen exposure" OR microoxic OR "oxygen tolerance") AND (metaboli* OR physiolog* OR scaveng*)'),
 ('P09','rumen scavenging','rumen AND ("oxygen scavenging" OR "oxygen consumption" OR "oxygen exposure" OR aerotolerance OR "oxygen tolerance")'),
 ('P10','oxygen damage sensitive enzymes','(anaerob* OR methanogen*) AND (oxygen OR superoxide) AND ("iron-sulfur" OR "enzyme inactivation" OR "pyruvate formate lyase")'),
 ('P11','methanogen microoxia metabolism','methanogen* AND (microoxic OR microaerobic OR "oxygen limitation" OR "oxygen reduction") AND (metaboli* OR transcript* OR respir* OR physiolog*)'),
 ('P12','recovery repeated exposure','(anaerob* OR methanogen*) AND ("oxygen shock" OR "oxygen exposure" OR "oxygen pulse" OR "intermittent aeration") AND (recover* OR adapt* OR repeated)'),
 ('P13','AD mechanistic response','("anaerobic digestion" OR "methanogenic sludge") AND (microaeration OR "oxygen shock" OR "oxygen exposure") AND (microbial OR enzyme OR metabol* OR syntroph*)'),
 ('P14','fermenter metabolic switch','(Clostridium OR "fermentative bacteria" OR "strict anaerobes") AND (microoxic OR "oxygen exposure" OR "oxygen stress") AND (ferment* OR "electron flow" OR "redox balance")'),
]

def run():
    logs=[]
    old=ROOT/'search_log.json'
    if old.exists(): logs=json.loads(old.read_text())
    completed={x['query_id'] for x in logs if x.get('status')=='completed'}
    for qid,theme,query in PUBMED:
        if qid in completed: continue
        query=f'({query}) AND ("2012/01/01"[Date - Publication] : "2026/10/24"[Date - Publication])'
        entry={'query_id':qid,'database':'PubMed','date_utc':DATE,'theme':theme,'query':query,'field':'PubMed automatic term mapping; actual translation retained in raw ESearch','status':'started'}
        try:
            j=json.loads(request(qid,'pubmed','https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',{'db':'pubmed','term':query,'retmode':'json','retmax':9999,'sort':'pub date'}))['esearchresult']
            ids=j['idlist']; entry.update(reported_count=int(j['count']),returned_ids=len(ids),query_translation=j.get('querytranslation',''))
            if int(j['count'])>9999: raise ValueError('PubMed >9999 requires date split; not marked complete')
            n=0
            for off in range(0,len(ids),100):
                b=request(qid,'pubmed','https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',{'db':'pubmed','id':','.join(ids[off:off+100]),'retmode':'xml'},f'fetch_{off:05}',True)
                n+=len(ET.fromstring(b).findall('PubmedArticle'))+len(ET.fromstring(b).findall('PubmedBookArticle'))
            entry.update(retrieved_records=n,status='completed',limit='Complete IDs and all EFetch batches for this query')
        except Exception as e: entry.update(status='failed',error=str(e)[:350])
        logs=[x for x in logs if x['query_id']!=qid]+[entry]; save(old,logs)
        print(qid,entry.get('reported_count'),entry.get('retrieved_records'),entry['status'],flush=True)
    # Crossref is relevance ranked, NOT boolean. Retain every returned item and
    # explicitly retain the unvisited tail; do not present first100 as exhaustive.
    for i,query in enumerate(['methanogen oxygen exposure oxidative stress','anaerobic oxygen tolerance rubrerythrin','oxygen pulse sediment microbial recovery'],1):
        qid=f'C{i:02}'
        if qid in completed: continue
        e={'query_id':qid,'database':'Crossref','date_utc':DATE,'query':query,'field':'query.bibliographic','status':'started','limit':'First 100 relevance-ranked items; broader reported tail NOT retrieved (non-exhaustive complementary search)'}
        try:
            j=json.loads(request(qid,'crossref','https://api.crossref.org/works',{'query.bibliographic':query,'filter':f'from-pub-date:2012-01-01,until-pub-date:{DATE}','rows':100}))['message']
            e.update(reported_count=j['total-results'],retrieved_records=len(j['items']),status='completed',unretrieved_reported_tail=max(0,j['total-results']-len(j['items'])))
        except Exception as ex:e.update(status='failed',error=str(ex)[:350])
        logs=[x for x in logs if x['query_id']!=qid]+[e];save(old,logs);print(qid,e.get('retrieved_records'),e['status'],flush=True)
    for i,query in enumerate(['methanogen oxygen exposure','anaerobe rubrerythrin oxygen','syntrophic oxygen protection'],1):
        qid=f'O{i:02}'
        if qid in completed:continue
        e={'query_id':qid,'database':'OpenAlex','date_utc':DATE,'query':query,'field':'title_and_abstract.search','status':'started','limit':'Cursor pagination; maximum 1000 retrieved per query; stop at empty/exhausted or record explicit capped tail'}
        try:
            cursor='*';n=0;page=0
            while cursor and n<1000:
                j=json.loads(request(qid,'openalex','https://api.openalex.org/works',{'filter':f'from_publication_date:2012-01-01,to_publication_date:{DATE},title_and_abstract.search:{query}','per-page':200,'cursor':cursor},f'page_{page:03}'))
                e['reported_count']=j['meta']['count'];n+=len(j['results']);page+=1
                cursor=j['meta'].get('next_cursor') if j['results'] else None
            e.update(retrieved_records=n,pages=page,status='completed',termination='explicit_1000_cap' if cursor and n>=1000 else 'cursor_exhausted',next_cursor=cursor)
        except Exception as ex:e.update(status='failed',error=str(ex)[:350])
        logs=[x for x in logs if x['query_id']!=qid]+[e];save(old,logs);print(qid,e.get('reported_count'),e.get('retrieved_records'),e['status'],flush=True)

if __name__=='__main__':run()
