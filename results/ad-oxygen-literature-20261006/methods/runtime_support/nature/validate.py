#!/usr/bin/env python3
"""Check real stdio MCP startup; optional exact DOI fetch never runs a search."""
from __future__ import annotations
import argparse
import asyncio
from datetime import datetime, timezone
from importlib import metadata
import json
import os
from pathlib import Path
import subprocess
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

parser = argparse.ArgumentParser()
parser.add_argument("--offline-only", action="store_true")
parser.add_argument("--known-doi")
args = parser.parse_args()
runtime = Path(os.environ.get("NATURE_RUNTIME_DIR", Path(__file__).resolve().parent))
source = Path(os.environ.get("NATURE_SOURCE_DIR", runtime.parent / "nature-skills"))
required = ["nature-academic-search", "nature-downloader", "nature-shared"]
report = {
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "source_commit": subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip(),
    "full_directories": {name: len([p for p in (source / "skills" / name).rglob("*") if p.is_file() and "__pycache__" not in p.parts]) for name in required},
    "dependencies": {name: metadata.version(name) for name in ["mcp", "requests", "toml", "lxml", "pybliometrics", "defusedxml", "pdfplumber", "pypdf", "PyYAML", "jsonschema"]},
    "node_version": subprocess.check_output(["node", "--version"], text=True).strip(),
    "credential_variable_presence": {name: bool(os.environ.get(name)) for name in ["NCBI_API_KEY", "ELSEVIER_API_KEY", "SPRINGER_API_KEY", "IEEE_API_KEY"]},
    "tls_verification_disabled": False,
    "proxy_inherited": bool(os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")),
    "ca_variables_present": {name: bool(os.environ.get(name)) for name in ["REQUESTS_CA_BUNDLE", "SSL_CERT_FILE", "NODE_EXTRA_CA_CERTS"]},
    "chat_tool_registration": "not registered in current chat; directly tested with MCP SDK stdio client",
    "exact_doi_fetch": {"state": "not_requested"},
}

async def main():
    env = os.environ.copy()
    env["NATURE_RUNTIME_DIR"] = str(runtime)
    env["NATURE_SOURCE_DIR"] = str(source)
    http_audit = runtime / "http_audit.jsonl"
    if args.known_doi and not args.offline_only:
        http_audit.write_text("")
        os.chmod(http_audit, 0o600)
        env["NATURE_HTTP_AUDIT_FILE"] = str(http_audit)
    params = StdioServerParameters(command=sys.executable, args=[str(runtime / "launch_academic.py")], env=env, cwd=str(runtime))
    # Keep any upstream messages out of the shared report; no credentials are read.
    with (runtime / "mcp_stderr.log").open("w", encoding="utf-8") as err:
        os.chmod(runtime / "mcp_stderr.log", 0o600)
        async with stdio_client(params, errlog=err) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                tools = await session.list_tools()
                names = sorted(t.name for t in tools.tools)
                report["mcp_initialized"] = True
                report["mcp_tool_count"] = len(names)
                report["mcp_tools"] = names
                invalid = await session.call_tool("get_paper_by_id", {"id": "invalid-onboarding-id", "id_type": "auto"})
                invalid_text = "\n".join(getattr(block, "text", "") for block in invalid.content)
                report["offline_input_validation_passed"] = "Cannot detect ID type" in invalid_text
                if args.known_doi and not args.offline_only:
                    result = await session.call_tool("get_paper_by_id", {"id": args.known_doi, "id_type": "doi"})
                    result_text = "\n".join(getattr(block, "text", "") for block in result.content)
                    try:
                        payload = json.loads(result_text)
                    except ValueError:
                        payload = {"error": "non-JSON response"}
                    error = str(payload.get("error", ""))
                    blocked = "Tunnel connection failed: 403" in error or "CONNECT" in error and "403" in error
                    report["exact_doi_fetch"] = {
                        "doi": args.known_doi,
                        "tool": "get_paper_by_id",
                        "endpoint": "api.crossref.org/works/<exact DOI>",
                        "search_executed": False,
                        "attempts": 1,
                        "state": "blocked_connect_403" if blocked else "failed" if error else "metadata_received",
                        "doi_matches": str(payload.get("doi", "")).lower() == args.known_doi.lower(),
                        "returned_title": payload.get("title", ""),
                        "metadata_received": not bool(error),
                        "error_class": "proxy_connect_denied" if blocked else "upstream_error" if error else None,
                    }
    if args.known_doi and not args.offline_only:
        report["http_transport_observations"] = [json.loads(line) for line in http_audit.read_text().splitlines() if line.strip()]
    output = runtime / ("validation_offline.json" if args.offline_only else "validation.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    assert report["mcp_initialized"] and report["offline_input_validation_passed"]

asyncio.run(main())
