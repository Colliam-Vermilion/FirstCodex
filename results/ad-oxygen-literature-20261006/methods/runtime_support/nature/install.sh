#!/usr/bin/env bash
# Reconstruct the approved Nature tools outside the research checkout.
set -euo pipefail
umask 077
nature_asset_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
nature_source_dir="${NATURE_SOURCE_DIR:-/workspace/tools/nature-skills}"
nature_runtime_dir="${NATURE_RUNTIME_DIR:-/workspace/tools/nature-runtime}"
nature_revision=b543e8b998eb2df1fd44641cc8b262c638c2b442
mkdir -p "$(dirname "$nature_source_dir")" "$nature_runtime_dir"
# The fixed skill needs Node 22+, while the current proxy route additionally
# needs Node's supported --use-env-proxy capability (verified with 24.19.0).
node --use-env-proxy --version >/dev/null
if [ ! -d "$nature_source_dir/.git" ]; then
  git clone --no-checkout https://github.com/Yuan1z0825/nature-skills.git "$nature_source_dir"
  git -C "$nature_source_dir" checkout --detach "$nature_revision"
fi
if [ "$(git -C "$nature_source_dir" rev-parse HEAD)" != "$nature_revision" ]; then
  echo 'Existing Nature checkout has a different revision; preserve it and choose a separate NATURE_SOURCE_DIR.' >&2
  exit 1
fi
for nature_skill in nature-academic-search nature-downloader nature-shared; do
  test -f "$nature_source_dir/skills/$nature_skill/SKILL.md"
  test -f "$nature_source_dir/skills/$nature_skill/README.md"
done
test -f "$nature_source_dir/skills/nature-academic-search/mcp-server/academic_search_server.py"
test -f "$nature_source_dir/skills/nature-downloader/scripts/batch_download.mjs"
if [ ! -x "$nature_runtime_dir/venv/bin/python" ]; then
  python3 -m venv --system-site-packages "$nature_runtime_dir/venv"
fi
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-$nature_runtime_dir/cache/pip}"
"$nature_runtime_dir/venv/bin/python" -m pip install --disable-pip-version-check -r "$nature_asset_dir/dependencies.lock"
"$nature_runtime_dir/venv/bin/python" -m pip check
for nature_helper in configure.py launch_academic.py download.sh validate.py validate_node.mjs dependencies.lock; do
  if [ "$nature_asset_dir/$nature_helper" != "$nature_runtime_dir/$nature_helper" ]; then
    cp "$nature_asset_dir/$nature_helper" "$nature_runtime_dir/$nature_helper"
  fi
done
chmod 700 "$nature_runtime_dir/download.sh"
export NATURE_SOURCE_DIR="$nature_source_dir"
export NATURE_RUNTIME_DIR="$nature_runtime_dir"
"$nature_runtime_dir/venv/bin/python" "$nature_runtime_dir/configure.py"
node --check "$nature_source_dir/skills/nature-downloader/scripts/batch_download.mjs"
"$nature_runtime_dir/venv/bin/python" "$nature_runtime_dir/validate.py" --offline-only
