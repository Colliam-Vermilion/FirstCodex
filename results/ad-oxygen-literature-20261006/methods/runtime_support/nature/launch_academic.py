#!/usr/bin/env python3
"""Run the unchanged Nature MCP source with private, external contact settings."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import time
from urllib.parse import urlsplit

runtime = Path(os.environ.get("NATURE_RUNTIME_DIR", Path(__file__).resolve().parent))
source = Path(os.environ.get("NATURE_SOURCE_DIR", runtime.parent / "nature-skills"))
server_dir = source / "skills" / "nature-academic-search" / "mcp-server"
contact_file = runtime / "config" / "contact.json"
settings = json.loads(contact_file.read_text()) if contact_file.exists() else {}
email = os.environ.get("NATURE_CONTACT_EMAIL") or os.environ.get("PUBMED_EMAIL") or settings.get("contact_email", "")
if not email:
    raise SystemExit("Configure NATURE_CONTACT_EMAIL or the private runtime config/contact.json first")
os.environ.setdefault("PUBMED_EMAIL", email)
os.environ.setdefault("OPENALEX_MAILTO", email)
os.environ.setdefault("CROSSREF_MAILTO", email)
os.environ.setdefault("LIT_DL_CONFIG_DIR", str(runtime / "config" / "lit-dl"))
# Optional, non-invasive transport evidence. No URL query, headers, body,
# credential, or proxy address is recorded. This does not change TLS/proxy use.
audit_file = os.environ.get("NATURE_HTTP_AUDIT_FILE")
if audit_file:
    import requests
    original_send = requests.Session.send
    def audited_send(session, request, **kwargs):
        url = urlsplit(request.url)
        observed = {"method": request.method, "scheme": url.scheme,
                    "host": url.hostname, "path": url.path,
                    "local_cache": False, "session_trust_env": session.trust_env,
                    "proxy_route_present": bool(kwargs.get("proxies")),
                    "tls_verification_enabled": kwargs.get("verify", session.verify) is not False,
                    "started_unix": time.time()}
        try:
            response = original_send(session, request, **kwargs)
            observed.update({"http_status": response.status_code,
                             "response_host": urlsplit(response.url).hostname,
                             "content_type": response.headers.get("content-type", ""),
                             "response_date": response.headers.get("date", ""),
                             "response_bytes": len(response.content)})
            return response
        except Exception as exc:
            observed["exception_class"] = type(exc).__name__
            raise
        finally:
            observed["finished_unix"] = time.time()
            with open(audit_file, "a", encoding="utf-8") as audit:
                audit.write(json.dumps(observed) + "\n")
    requests.Session.send = audited_send
sys.path.insert(0, str(server_dir))
from utils import config as config_module
config_module._config = config_module.Config(server_dir / "config.toml")
config_module._config._config.setdefault("crossref", {})["mailto"] = os.environ.get("CROSSREF_MAILTO", email)
from academic_search_server import mcp
mcp.run(transport="stdio")
