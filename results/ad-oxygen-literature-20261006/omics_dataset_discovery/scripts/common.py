import datetime as dt,hashlib,json,time,urllib.request,urllib.error,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(p)
def url(base,**params):return base+'?'+urllib.parse.urlencode(params)
def fetch(u,source='official',cache=True,timeout=45):
 key=hashlib.sha256(u.encode()).hexdigest();dest=ROOT/'raw'/source/(key+'.body');side=dest.with_suffix('.meta.json')
 if cache and side.exists() and dest.exists():
  m=json.loads(side.read_text());return (dest.read_bytes() if m.get('status')==200 else None),m
 start=time.monotonic();m={'url':u,'source':source,'started_utc':now(),'raw_path':str(dest.relative_to(ROOT))}
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'OmicsDatasetDiscovery/1.0','Accept':'*/*'})
  with urllib.request.urlopen(req,timeout=timeout) as r:b=r.read();m.update(status=r.status,content_type=r.headers.get('content-type'),final_url=r.url)
 except urllib.error.HTTPError as e:b=e.read();m.update(status=e.code,error=str(e))
 except Exception as e:b=str(e).encode();m.update(status=None,error=type(e).__name__+': '+str(e))
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);m.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),finished_utc=now(),measured_wall_seconds=round(time.monotonic()-start,3));dump(side,m)
 with (ROOT/'request_log.jsonl').open('a') as f:f.write(json.dumps(m,ensure_ascii=False)+'\n')
 return (b if m.get('status')==200 else None),m
def getjson(u,source='official'):
 b,m=fetch(u,source)
 if b is None:return None,m
 try:return json.loads(b),m
 except Exception as e:return None,{**m,'parse_error':str(e)}
