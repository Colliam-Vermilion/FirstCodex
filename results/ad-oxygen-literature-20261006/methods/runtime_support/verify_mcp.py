"""Verify the stdio MCP server without network searches or credential output."""
import asyncio,json,os
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

BASE=Path(__file__).resolve().parent
async def main():
    params=StdioServerParameters(command=str(BASE/'venv/bin/python'),args=[str(BASE/'launch.py'),'run'],env=dict(os.environ))
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            listed=await session.list_tools()
            names=sorted(t.name for t in listed.tools)
            def decoded(result):
                return json.loads(next(c.text for c in result.content if getattr(c,'type','')=='text'))
            legal=decoded(await session.call_tool('scansci_pdf_config',{'key':'download_strategy'}))
            grey=decoded(await session.call_tool('scansci_pdf_config',{'key':'scihub_enabled'}))
            email=decoded(await session.call_tool('scansci_pdf_config',{'key':'email'}))
            result={'version':'1.18.0','upstream_snapshot':'3df79f8211ec2fb542170d132e330fc7bb92ab96','mcp_stdio_initialize':True,'tools_count':len(names),'tool_names':names,'legal_only_read_through_actual_mcp':legal.get('value')=='legal_only','grey_sources_disabled_read_through_actual_mcp':grey.get('value') is False,'authorized_email_read_matches':email.get('value')==json.loads((Path(os.environ.get('SCANSCI_PDF_DATA_DIR',str(BASE/'data')))/'config.json').read_text())['email'],'email_value_not_exported':True,'current_chat_tool_registration_claimed':False}
            (BASE/'mcp_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
            print(json.dumps(result,ensure_ascii=False))
asyncio.run(main())
