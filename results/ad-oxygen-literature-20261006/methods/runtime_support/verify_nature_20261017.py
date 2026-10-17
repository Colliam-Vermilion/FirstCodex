"""Exercise actual Nature stdio tools without a literature search."""
import asyncio, json, os
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    source=Path('/workspace/tools/nature-skills')
    runtime=Path('/workspace/tools/nature-runtime')
    report={'source':json.loads((source/'SOURCE_PROVENANCE.json').read_text()),
            'full_directories':{n:sum(p.is_file() for p in (source/'skills'/n).rglob('*') if '__pycache__' not in p.parts) for n in ['nature-academic-search','nature-downloader','nature-shared']},
            'new_literature_search_executed':False,'tls_verification_disabled':False}
    params=StdioServerParameters(command=str(runtime/'venv/bin/python'),args=[str(runtime/'launch_academic.py')],env=dict(os.environ))
    with (runtime/'mcp_stderr.log').open('w') as err:
        async with stdio_client(params,errlog=err) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                names=[t.name for t in (await session.list_tools()).tools]
                result=await session.call_tool('get_paper_by_id',{'id':'invalid-recovery-id','id_type':'auto'})
                report.update(mcp_initialized=True,tool_count=len(names),tools=names,
                    actual_tool_call_validated='Cannot detect ID type' in '\n'.join(getattr(c,'text','') for c in result.content))
    (runtime/'validation_20261017.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
    assert report['actual_tool_call_validated'] and all(report['full_directories'].values())

asyncio.run(main())
