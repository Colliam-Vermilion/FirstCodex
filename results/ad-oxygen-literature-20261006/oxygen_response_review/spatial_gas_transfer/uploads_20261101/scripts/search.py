import asyncio,json,os,datetime
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
R=Path('/workspace/FirstCodex');T=R/'results/ad-oxygen-literature-20261006/oxygen_response_review/spatial_gas_transfer';P=T/'uploads_20261101';O=P/'raw';O.mkdir(exist_ok=True)
M=json.load(open(T/'literature_master.json'));tasks=[]
for rid in ['SG-66E719E38CD9','SG-6E33DBD11D46','SG-47E08464D7E8']:
 r=next(x for x in M if x['id']==rid);tasks.append((rid,'get_paper_by_id',{'id':r.get('pmid')or r['doi'],'id_type':'pmid' if r.get('pmid')else 'doi'},'现有候选补摘要'))
for i,d in enumerate(['10.1002/bit.20862','10.1128/JB.185.5.1485-1491.2003','10.1128/jb.178.24.7322-7325.1996','10.1016/j.ces.2005.02.063']):tasks.append(('REF'+str(i),'get_paper_by_id',{'id':d,'id_type':'doi'},'上传正文参考文献追溯：Berg或Wessel或Sabra'))
queries=['((biofilm[Title/Abstract] OR granule*[Title/Abstract]) AND ("diffusive permeability"[Title/Abstract] OR "diffusion relaxation"[Title/Abstract]))','(("activated sludge"[Title/Abstract]) AND ("oxygen penetration"[Title/Abstract] OR "microelectrode"[Title/Abstract]) AND (EPS[Title/Abstract] OR "extracellular polymeric"[Title/Abstract]))']
for i,q in enumerate(queries):tasks.append(('Q'+str(i+1),'search_papers',{'query':q,'sources':['pubmed'],'rows':100},'针对水扩散/渗透性与EPS因果缺口；不设起始年'))
async def main():
 log=[]
 async with stdio_client(StdioServerParameters(command='/workspace/academic-search-runtime/venv/bin/python',args=['/workspace/academic-search-runtime/launch.py'],env=dict(os.environ)))as(r,w):
  async with ClientSession(r,w)as s:
   await s.initialize()
   for key,tool,args,why in tasks:
    l={'key':key,'tool':tool,'arguments':args,'purpose':why,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'date_range':'无起始下限；执行日2026-11-01；出版日需逐条核实','source':'nature-academic-search local MCP'}
    try:
     z=await asyncio.wait_for(s.call_tool(tool,args),45);f=O/(key+'.json');f.write_text(json.dumps(z.model_dump(),ensure_ascii=False,indent=2));l.update(raw_path=str(f.relative_to(R)),status='error'if z.isError else 'returned');print(key,l['status'],flush=True)
    except Exception as e:l.update(status='failed',error=type(e).__name__);print(key,l,flush=True)
    log.append(l);(P/'search_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
asyncio.run(main())
