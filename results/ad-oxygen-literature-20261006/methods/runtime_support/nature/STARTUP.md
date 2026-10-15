Use the existing isolated task checkout; do not create a Git worktree unless the user asks.

Restore tools only when missing by running this directory's `install.sh`. It pins the
full Nature Skills repository to `b543e8b998eb2df1fd44641cc8b262c638c2b442` and
retains all files in `nature-academic-search`, `nature-downloader`, and `nature-shared`.
The runtime defaults to `/workspace/tools/nature-runtime`, with source under
`/workspace/tools/nature-skills`. `NATURE_SOURCE_DIR` and `NATURE_RUNTIME_DIR`
can select other writable directories. It preserves an existing checkout at
another revision instead of replacing it. It never modifies the research repository.

Set the authorized nonsecret `NATURE_CONTACT_EMAIL` in environment settings or
use the already configured private `config/contact.json` outside Git. PubMed
and Crossref contact configuration and `LIT_DL_CONFIG_DIR` are initialized there.
Existing contact/settings and injected proxy/CA variables are preserved; no API
key or institutional session is assumed. No secrets belong in these support files.

The verified runtime is Python 3.12 and Node 24.19.0. Upstream requires Node 22+;
this proxy-backed deployment additionally checks support for `--use-env-proxy`.
`download.sh` sets the supported `NODE_USE_ENV_PROXY=1` and inherits the current
platform proxy and TLS trust. Do not replace these with old proxy addresses.

Check local readiness with:

```bash
/workspace/tools/nature-runtime/venv/bin/python /workspace/tools/nature-runtime/validate.py --offline-only
```

The MCP is a stdio server, not an HTTP service or persistent background process:

```bash
/workspace/tools/nature-runtime/venv/bin/python /workspace/tools/nature-runtime/launch_academic.py
```

Use an MCP SDK client to launch and call it. The current chat has no dynamically
registered Nature MCP tools; the SDK initialization and 16 advertised tools were
tested directly. Do not describe tool listing as an API or PDF download success.
Use `validate.py --known-doi <existing-project-DOI>` only for an intentional,
exact known-record API check. It never invokes a topical literature search.

Use `/workspace/tools/nature-runtime/download.sh` with a definite existing record
list and explicit `--si` because the user already requested supplements. Give
each record ID/source attempt a separate output directory, check existing
originals/SHA first, respect provider pacing, and retain manifests for resume.
Do not use `--topic`, redo searches, change classifications, or process excluded
records. `batch_download.mjs --help` is unsupported in this pinned version;
consult the full README/SKILL and script argument parser instead.

The fixed version's direct PDF URL route writes SI `not_found` without checking
the landing page. Bare DOI SI needs a live CDP browser service. Independently
inspect official landing-page/attachment metadata for PDF, Word, spreadsheet,
CSV, archive and other supplements, and label inaccessible/unassessed SI
separately. Do not infer absence from that direct-route `not_found` value.
The upstream OA label is not license proof, and same-title files can overwrite;
separate record directories and verify identity/version and lawful source.

After a CONNECT 403, record the destination and continue other sources. Retry
only after a meaningful route/policy change. Keep authenticated school access
separate and never request passwords. Current-instance files and saved setup
configuration are not a file backup. Require original-file persistence, user
download, and an independent subsequent-task readback before bulk retrieval.
