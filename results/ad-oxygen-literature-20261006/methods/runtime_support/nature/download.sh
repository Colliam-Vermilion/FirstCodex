#!/usr/bin/env bash
# Pass only an existing definite DOI/title/URL list; this wrapper does not select papers.
set -euo pipefail
nature_runtime_dir="${NATURE_RUNTIME_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
nature_source_dir="${NATURE_SOURCE_DIR:-$(dirname "$nature_runtime_dir")/nature-skills}"
export LIT_DL_CONFIG_DIR="${LIT_DL_CONFIG_DIR:-$nature_runtime_dir/config/lit-dl}"
export NODE_USE_ENV_PROXY=1
export PATH="$nature_runtime_dir/venv/bin:$PATH"
exec node "$nature_source_dir/skills/nature-downloader/scripts/batch_download.mjs" "$@"
