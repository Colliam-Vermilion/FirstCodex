"""Reproducible local supplemental discovery; no network and no old writes.

Online queries are separately queued, never reported as completed. This local
query searches the union of saved review and dataset-associated article records.
"""
import csv,datetime,hashlib,html,json,re,sqlite3,subprocess,unicodedata
from pathlib import Path
T=Path(__file__).resolve().parents[1];M=T.parent;P=M.parent;R=P.parents[1]
BASE='fcd0ad3119900af9f75c9b9220575b8ff79a0170'
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def read(p):return json.loads(p.read_text())
def doi(x):return re.sub(r'^https?://(?:dx\.)?doi.org/','',x or '',flags=re.I).strip().lower()
def title(x):return ''.join(c for c in unicodedata.normalize('NFKD',html.unescape(x or '')).casefold() if c.isalnum())
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
SEEDS=[
 ('S01','10.1128/aem.00563-24','Nondestructive and three-dimensional visualization by identifying elements using synchrotron radiation microscale X-ray CT reveals microbial and cavity distributions in anaerobic granular sludge'),
 ('S02','10.1128/AEM.01426-07','Layered Structure of Bacterial and Archaeal Communities and Their In Situ Activities in Anaerobic Granules'),
 ('S03','10.1007/s00253-012-4616-9','Interspecies distances between propionic acid degraders and methanogens in syntrophic consortia for optimal hydrogen transfer'),
 ('S04','10.1016/j.jenvman.2005.01.022','Size-dependent anaerobic digestion rates of flocculated activated sludge: role of intrafloc mass transfer resistance'),
 ('S05','10.1002/bit.260330612','Control of interspecies electron transfer flow during anaerobic digestion: Dynamic diffusion reaction models for hydrogen gas transfer in microbial flocs')]
LOCAL=[
 ('L01','空间与三维', [r'anaerob|methanogen|syntroph|sludge',r'granul|floc|biofilm|aggregat',r'spatial|layer|imag|confocal|microelectrod|diffus|poros|three.?dimension|tomograph|micro.?ct']),
 ('L02','传质与互营',[r'anaerob|methanogen|syntroph',r'mass transfer|diffus|boundary layer|interspecies distance|hydrogen transfer|formate transfer']),
 ('L03','ORP控制',[r'\bORP\b|oxidation.reduction potential|redox potential',r'micro.?aerat|oxygen|aeration',r'digest|methanogen|biogas']),
 ('L04','DO控制或记录',[r'dissolved oxygen|\bDO\b',r'control|feedback|setpoint|uptake|mass transfer',r'anaerob|digest']),
 ('L05','可借鉴的氧传递',[r'sediment|biofilm',r'oxygen',r'mass transfer|penetration|gradient|diffus']),
 ('L06','距离及中间产物交换',[r'syntroph|co.?cultur',r'hydrogen|formate',r'distance|spatial|aggregate|floc']),
]
ONLINE=[
 ('Q01','PubMed','((anaerobic granule*[Title/Abstract] OR methanogenic granule*[Title/Abstract]) AND (three-dimensional[Title/Abstract] OR tomography[Title/Abstract] OR confocal[Title/Abstract] OR micro-CT[Title/Abstract]))'),
 ('Q02','PubMed','((anaerobic granule*[Title/Abstract] OR anaerobic biofilm*[Title/Abstract]) AND (spatial distribution[Title/Abstract] OR FISH[Title/Abstract] OR CLSM[Title/Abstract] OR pore*[Title/Abstract] OR channel*[Title/Abstract]))'),
 ('Q03','PubMed','((anaerobic sludge[Title/Abstract] OR methanogenic sludge[Title/Abstract] OR sludge floc*[Title/Abstract]) AND (effective diffusivity[Title/Abstract] OR diffusion coefficient[Title/Abstract] OR mass transfer resistance[Title/Abstract] OR liquid film[Title/Abstract]))'),
 ('Q04','PubMed','((syntroph*[Title/Abstract] OR methanogen*[Title/Abstract]) AND (interspecies distance*[Title/Abstract] OR interspecies hydrogen transfer[Title/Abstract] OR formate transfer[Title/Abstract]))'),
 ('Q05','PubMed','((interfloc[Title/Abstract] OR inter-floc[Title/Abstract] OR intrafloc[Title/Abstract] OR intra-floc[Title/Abstract]) AND (hydrogen[Title/Abstract] OR methane[Title/Abstract] OR diffusion[Title/Abstract] OR anaerobic[Title/Abstract]))'),
 ('Q06','PubMed','((anaerobic digest*[Title/Abstract] OR biogas[Title/Abstract]) AND (ORP[Title/Abstract] OR redox feedback[Title/Abstract] OR oxidation reduction potential[Title/Abstract]) AND (oxygen[Title/Abstract] OR aeration[Title/Abstract]))'),
 ('Q07','PubMed','((anaerobic digest*[Title/Abstract] OR methanogenic[Title/Abstract]) AND (oxygen uptake rate[Title/Abstract] OR oxygen transfer rate[Title/Abstract] OR DO control[Title/Abstract] OR dissolved oxygen control[Title/Abstract]))'),
 ('Q08','PubMed','((anaerobic granule*[Title/Abstract] OR methanogenic biofilm*[Title/Abstract]) AND (microsensor*[Title/Abstract] OR microprofile*[Title/Abstract] OR penetration depth[Title/Abstract]) AND (hydrogen[Title/Abstract] OR methane[Title/Abstract] OR sulfide[Title/Abstract] OR oxygen[Title/Abstract]))'),
 ('Q09','OpenAlex','anaerobic granular sludge three dimensional tomography porosity'),
 ('Q10','OpenAlex','methanogenic floc hydrogen diffusion reaction model'),
 ('Q11','OpenAlex','anaerobic granules effective diffusivity methane hydrogen'),
 ('Q12','OpenAlex','microaeration ORP control dissolved oxygen transfer'),
]
def main():
 sources=[(M/'catalog.json','id'),(P/'omics_dataset_discovery/paper_discovery_candidates_enriched.json','paper_id')]
 catalog={};indexes={};inputs=[];conflicts=[]
 for f,idkey in sources:
  for item in read(f):
   rid=item[idkey];keys=[('doi',doi(item.get('doi'))),('pmid',str(item.get('pmid') or '')),('title',title(item.get('title')))]
   matches=set()
   for k,v in keys:
    if not v or (k,v) not in indexes:continue
    existing=indexes[k,v]
    if k=='title' and catalog[existing].get('doi') and doi(item.get('doi')) and catalog[existing]['doi']!=doi(item['doi']):
     conflicts.append({'incoming':rid,'candidate':existing,'reason':'规范化题名相同但DOI不同，保留版本/身份疑点，不按题名合并'});continue
    matches.add(existing)
   target=next(iter(matches)) if len(matches)==1 else rid
   if len(matches)>1:conflicts.append({'incoming':rid,'candidates':sorted(matches),'action':'保持原ID，待核实，不自动合并'})
   c=catalog.setdefault(target,{'id':target,'source_links':[],'aliases':[],'doi':doi(item.get('doi')),'pmid':str(item.get('pmid') or ''),'title':item['title'],'year':item.get('year'),'journal':item.get('journal'),'authors':item.get('authors',[]),'abstract':item.get('abstract','')})
   if not c.get('abstract') and item.get('abstract'):c['abstract']=item['abstract']
   if rid!=target and rid not in c['aliases']:c['aliases'].append(rid)
   c['source_links'].append({'path':str(f.relative_to(R)),'id':rid,'identity_field':idkey})
   for k,v in keys:
    if v:indexes.setdefault((k,v),target)
   inputs.append({'source':str(f.relative_to(R)),'source_id':rid,'assigned_id':target,'match_keys':[k for k,v in keys if v and indexes.get((k,v))==target]})
 logs=[];hitids=set()
 for qid,theme,patterns in LOCAL:
  hits=[]
  for c in catalog.values():
   text=c['title']+'\n'+c.get('abstract','')
   if all(re.search(p,text,re.I) for p in patterns):hits.append(c);hitids.add(c['id'])
  path=T/'raw/local'/f'{qid}.json';dump(path,hits)
  logs.append({'query_id':qid,'database':'已保存官方/旧库记录的本地并集；不是新外部数据库查询','theme':theme,'fields':['title','abstract'],'query_verbatim':' AND '.join('REGEX('+p+')' for p in patterns),'case_insensitive':True,'time_filter':'无新时间过滤；覆盖受先前保存材料限制','date_utc':now(),'pagination':'完整本地遍历，无截断','returned_records':len(hits),'raw_path':str(path.relative_to(T)),'execution_state':'completed_local'})
 exact_ids=['OR-8E58C5BBDB53','OR-06716459121E','OR-9AE95458315B','OR-6A3D9B1E5D73','R01414','R03161','R13833']
 exact=[catalog[rid] for rid in exact_ids];hitids.update(exact_ids);dump(T/'raw/local/L07.json',exact)
 logs.append({'query_id':'L07','database':'已保存记录精确ID取回','theme':'用户指定记录与已保存全文索引/导读线索','query_verbatim':exact_ids,'fields':['id'],'date_utc':now(),'pagination':'7个指定ID，完整返回','returned_records':len(exact),'raw_path':'raw/local/L07.json','execution_state':'completed_local'})
 seedrows=[]
 for sid,d,t in SEEDS:
  match=indexes.get(('doi',doi(d)));c=catalog.get(match)
  if c:hitids.add(match)
  seedrows.append({'seed_key':sid,'supplied_title':t,'supplied_doi':d,'assigned_existing_id':match,'verified_title':c['title'] if c else None,'verified_doi':c['doi'] if c else None,'verification_basis':'此前保存的官方元数据；本轮尚未联网重新核对' if c else '仅用户提供线索，尚未独立核实','title_normalized_matches':title(t)==title(c['title']) if c else None,'external_verification_state':'blocked_proxy_CONNECT_403','fulltext_state':'尚未获取／核实，不以摘要代全文'})
 dump(T/'seed_audit.json',seedrows)
 # The four user seed identities lacking an independently saved record remain
 # seed tasks, not invented bibliographic records or RIS entries.
 dump(T/'local_identity_conflicts.json',conflicts);dump(T/'local_input_mapping.json',inputs)
 dump(T/'local_identity_registry.json',[{'id':c['id'],'doi':c['doi'],'pmid':c['pmid'],'title':c['title'],'aliases':c['aliases'],'source_links':c['source_links']} for c in catalog.values()])
 dump(T/'candidate_records.json',[catalog[i] for i in sorted(hitids)])
 dump(T/'search_log.json',logs)
 dump(T/'online_query_queue.json',[{'query_id':qid,'database':db,'query_verbatim':q,'date_end':'2026-10-30','date_start':None,'state':'not_executed_network_policy_block','planned_pagination':'PubMed: count then full ID pages, EFetch batches100; OpenAlex: cursor/per-page200 until end, no arbitrary result cap','note':'OpenAlex为普通文本相关检索，不把空格当严格Boolean AND；若过宽按对象/概念拆分，保存每页'} for qid,db,q in ONLINE])
 dump(T/'raw/preflight/observations.json',{'observed_date_Asia_Shanghai':'2026-10-30','exact_request_timestamp_not_saved':True,'requests':[{'host':h,'purpose':'exact seed DOI metadata preflight','outcome':'URLError: Tunnel connection failed: 403 Forbidden','upstream_response_obtained':False} for h in ['www.ebi.ac.uk','api.crossref.org','eutils.ncbi.nlm.nih.gov','api.openalex.org']],'tool_inventory':'Nature academic-search installed b543e8b998eb2df1fd44641cc8b262c638c2b442; no callable academic tool mounted in chat; stdio validation initialized process but did not return and was terminated; not claimed ready','configuration':'Existing academic domain draft preserved; journals.asm.org added; save confirmed, requires_publish=true; not runtime application','new_external_discovery_records':0})
 dump(T/'baseline.json',{'commit':BASE,'branch':'review/oxygen-response-mechanisms','created_utc':now(),'original_review_records':len(read(M/'catalog.json')),'raw_local_input_rows':len(inputs),'local_union_identities':len(catalog),'topical_local_candidates':len(hitids),'local_queries_completed':len(logs),'external_queries_completed':0,'seed_metadata_reused':sum(bool(x['assigned_existing_id']) for x in seedrows),'seed_external_metadata_pending':sum(not x['assigned_existing_id'] for x in seedrows),'source_dedupe_policy':'DOI/PMID/规范化题名精确关联，优先原review ID；多身份冲突保留且不强并','no_new_verified_bibliographic_id':True})
 print(json.dumps(read(T/'baseline.json'),ensure_ascii=False))
if __name__=='__main__':main()
