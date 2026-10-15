#!/usr/bin/env bash
# Rebuild only the missing tool installation, outside the result checkout.
set -euo pipefail
umask 077
assets_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
runtime_dir="${SCANSCI_RUNTIME_DIR:-/workspace/tools/scansci-pdf-runtime}"
upstream_sha='3df79f8211ec2fb542170d132e330fc7bb92ab96'
mkdir -p "$runtime_dir"
if [ ! -x "$runtime_dir/venv/bin/python" ]; then
    python3 -m venv "$runtime_dir/venv"
fi
"$runtime_dir/venv/bin/python" -m pip install --quiet --no-cache-dir --no-input --disable-pip-version-check --requirement "$assets_dir/requirements.lock.txt"
if [ ! -d "$runtime_dir/upstream/.git" ]; then
    git clone --no-checkout --filter=blob:none https://github.com/Rimagination/scansci-pdf.git "$runtime_dir/upstream"
    git -C "$runtime_dir/upstream" checkout --detach "$upstream_sha"
fi
if [ -n "$(git -C "$runtime_dir/upstream" status --porcelain)" ]; then
    echo 'Upstream checkout has local modifications; preserving them and stopping.' >&2
    exit 1
fi
if ! git -C "$runtime_dir/upstream" cat-file -e "$upstream_sha^{commit}"; then
    git -C "$runtime_dir/upstream" fetch origin "$upstream_sha"
fi
if [ "$(git -C "$runtime_dir/upstream" rev-parse HEAD)" != "$upstream_sha" ]; then
    git -C "$runtime_dir/upstream" checkout --detach "$upstream_sha"
fi
[ "$(git -C "$runtime_dir/upstream" rev-parse HEAD)" = "$upstream_sha" ]
for asset in bootstrap.py launch.py init_config.py verify_mcp.py verify_transport.py requirements.lock.txt; do
    if [ "$assets_dir/$asset" != "$runtime_dir/$asset" ]; then
        install -m 0644 "$assets_dir/$asset" "$runtime_dir/$asset"
    fi
done
"$runtime_dir/venv/bin/python" "$runtime_dir/init_config.py"
"$runtime_dir/venv/bin/python" -m pip check
"$runtime_dir/venv/bin/python" "$runtime_dir/verify_transport.py"
"$runtime_dir/venv/bin/python" "$runtime_dir/verify_mcp.py"
