"""Optional serial exact-DOI jobs against an already installed ScanSci PDF MCP.
No topic queries. Keeps tool output as candidates; register after manual review.
ScanSci may still race internal sources; strict per-host scheduling is provided by
download_local.py, not by this wrapper. No credentials are printed or copied.
"""
from pathlib import Path
import argparse,asyncio,json,os
from audit_library import dump,read_csv,sha
from download_local import validate_file


def decode(result):
    for c in result.content:
        if getattr(c,'type','')=='text':
            try:return json.loads(c.text)
            except ValueError:continue
    return {}


async def run(args):
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    params=StdioServerParameters(command=args.command,args=args.server_arg or [],env=dict(os.environ));args.root.mkdir(parents=True,exist_ok=True)
    statefile=args.root/'intake/scansci_jobs.json';state=json.loads(statefile.read_text()) if statefile.exists() else {}
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize();tools=await session.list_tools();tool=next(t for t in tools.tools if t.name=='scansci_pdf_download')
            for key,wanted in [('download_strategy','legal_only'),('scihub_enabled',False)]:
                cfg=decode(await session.call_tool('scansci_pdf_config',{'key':key}))
                if cfg.get('value')!=wanted:raise ValueError('Configure '+key+' in your private ScanSci runtime before local jobs')
            probe={'stdio_initialized':True,'tool_count':len(tools.tools),'download_si_argument_present':'download_si' in (getattr(tool,'inputSchema',None) or getattr(tool,'input_schema',{})).get('properties',{}),'explicit_download_si_used_for_jobs':True,'credentials_exported':False,'actual_downloads_in_probe':0}
            print(json.dumps(probe),flush=True)
            if args.probe_only:return
            rows=read_csv(args.queue);count=0
            for row in rows:
                id=row['record_id'];meta=json.loads((args.project/'papers'/id/'metadata.json').read_text())
                if not meta['included_for_download'] or not row.get('doi'):continue
                old=state.get(id,{})
                if old.get('status')=='downloaded_pending_review' and Path(old.get('file','')).is_file() and sha(old['file'])==old.get('sha256'):continue
                if old.get('status') and not args.retry_failed:continue
                out=args.root/'intake'/id/'scansci';out.mkdir(parents=True,exist_ok=True)
                call={'identifier':row['doi'],'output_dir':str(out.resolve()),'strategy':'legal_only','scihub_enabled':False,'use_tor':False,'use_vpnsci':False,'download_si':True,'markdown':False}
                event={'record_id':id,'doi':row['doi'],'download_si_explicit':True,'status':'failed_or_access_restricted','identity_verified':False,'version_verified':False}
                try:
                    result=decode(await session.call_tool('scansci_pdf_download',call));file=Path(result.get('file') or '/nonexistent')
                    if result.get('success') and file.is_file():
                        check=validate_file(file,'main');event.update(status='downloaded_pending_review',file=str(file),sha256=sha(file),size_bytes=file.stat().st_size,format_checks=check)
                    event['tool_error_type']=result.get('error_type') or result.get('error')
                    event['candidate_files']=[{'path':str(f),'sha256':sha(f),'bytes':f.stat().st_size} for f in out.rglob('*') if f.is_file()]
                    event['SI_completeness_not_inferred_from_tool_result']=True
                except Exception as exc:event['error_type']=type(exc).__name__
                state[id]=event;dump(statefile,state);print(json.dumps(event,ensure_ascii=False),flush=True);count+=1
                if count>=args.limit:break
                await asyncio.sleep(args.delay)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--project',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--root',type=Path,required=True);ap.add_argument('--queue',type=Path);ap.add_argument('--command',required=True);ap.add_argument('--server-arg',action='append');ap.add_argument('--probe-only',action='store_true');ap.add_argument('--retry-failed',action='store_true');ap.add_argument('--limit',type=int,default=5);ap.add_argument('--delay',type=float,default=10)
    args=ap.parse_args()
    if not args.queue:args.queue=args.project/'windows/main_records_current_utf8.csv'
    if args.delay<5:ap.error('--delay must be >=5 seconds')
    asyncio.run(run(args))
