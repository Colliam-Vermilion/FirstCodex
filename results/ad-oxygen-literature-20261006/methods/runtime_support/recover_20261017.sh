#!/usr/bin/env bash
# Reconstruct pinned tools without changing upstream sources or global profiles.
set -euo pipefail
umask 077
support_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export UV_CACHE_DIR="${UV_CACHE_DIR:-/workspace/tools/.cache/uv}"
mkdir -p /workspace/tools
python3 - <<'PY'
import hashlib,json,pathlib,shutil,tarfile,urllib.request
specs=[('nature-skills','Yuan1z0825/nature-skills','b543e8b','b543e8b998eb2df1fd44641cc8b262c638c2b442','9af4866020c0d1fb302cd12d744e5e3313585022a22030d0e36b3048bb181874'),
 ('scansci-pdf','Rimagination/scansci-pdf','3df79f8211ec2fb542170d132e330fc7bb92ab96','3df79f8211ec2fb542170d132e330fc7bb92ab96','2828c13e761ed9d38ab247e7ce8e6e0c40d5a7b8f018cb5bc744ee603b6efdd6')]
for name,repo,ref,commit,expected in specs:
 dest=pathlib.Path('/workspace/tools')/name
 provenance=dest/'SOURCE_PROVENANCE.json'
 if dest.exists():
  if not provenance.is_file() or json.loads(provenance.read_text()).get('archive_sha256')!=expected:
   raise SystemExit(f'Preserve existing {dest}; source provenance differs')
  continue
 arc=pathlib.Path('/workspace/tools')/(name+'.tar.gz')
 with urllib.request.urlopen(f'https://codeload.github.com/{repo}/tar.gz/{ref}',timeout=120) as response,arc.open('wb') as stream:
  shutil.copyfileobj(response,stream)
 if hashlib.sha256(arc.read_bytes()).hexdigest()!=expected:
  raise SystemExit(f'Archive checksum mismatch for {name}; do not use it')
 with tarfile.open(arc) as archive:
  root=archive.getnames()[0];archive.extractall('/workspace/tools',filter='data')
 (dest.parent/root).rename(dest)
 provenance.write_text(json.dumps(dict(commit=commit,archive_sha256=expected,archive_ref=ref,transport='HTTPS codeload.github.com; TLS verification enabled'),indent=2)+'\n')
 arc.unlink()
PY
scansci_runtime=/workspace/tools/scansci-pdf-runtime
nature_runtime=/workspace/tools/nature-runtime
for runtime in "$scansci_runtime" "$nature_runtime"; do
  if [ ! -x "$runtime/venv/bin/python" ]; then uv venv "$runtime/venv"; fi
done
uv pip install --python "$scansci_runtime/venv/bin/python" -r "$support_dir/requirements.lock.txt"
uv pip install --python "$nature_runtime/venv/bin/python" -r "$support_dir/nature/dependencies.lock"
for asset in bootstrap.py launch.py init_config.py verify_mcp.py verify_transport.py requirements.lock.txt; do
  install -m 0600 "$support_dir/$asset" "$scansci_runtime/$asset"
done
for asset in configure.py launch_academic.py download.sh validate_node.mjs dependencies.lock; do
  install -m 0600 "$support_dir/nature/$asset" "$nature_runtime/$asset"
done
chmod 700 "$nature_runtime/download.sh"
# Contact comes from environment settings or previously created private config.
"$scansci_runtime/venv/bin/python" "$scansci_runtime/init_config.py"
"$nature_runtime/venv/bin/python" "$nature_runtime/configure.py"
node --use-env-proxy --version
node --check /workspace/tools/nature-skills/skills/nature-downloader/scripts/batch_download.mjs
uv pip check --python "$scansci_runtime/venv/bin/python"
uv pip check --python "$nature_runtime/venv/bin/python"
"$scansci_runtime/venv/bin/python" "$scansci_runtime/verify_transport.py"
"$scansci_runtime/venv/bin/python" "$scansci_runtime/verify_mcp.py"
"$nature_runtime/venv/bin/python" "$support_dir/verify_nature_20261017.py"
