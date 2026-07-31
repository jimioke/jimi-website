#!/usr/bin/env bash
# Pull publications from Zotero and regenerate content/publications/.
#
# One-time setup: create a gitignored .env.zotero next to this script with:
#     export ZOTERO_API_KEY=your-key-here
# (get a read-only key at https://www.zotero.org/settings/keys)
#
# Usage:
#   ./sync-pubs.sh --dry-run              # preview; writes nothing
#   ./sync-pubs.sh --overwrite --prune    # full sync (apply updates + remove orphans)
#   ./sync-pubs.sh --overwrite --prune && hugo   # sync, then rebuild the site
set -euo pipefail
cd "$(dirname "$0")"

# Non-secret library config (safe to commit).
export ZOTERO_LIBRARY_ID=6356012
export ZOTERO_LIBRARY_TYPE=user
export ZOTERO_COLLECTION_KEY=GJZPZ3V3

# Load the API key from the gitignored file.
if [ -f .env.zotero ]; then
    source .env.zotero
fi
if [ -z "${ZOTERO_API_KEY:-}" ]; then
    echo "ZOTERO_API_KEY not set. Create .env.zotero with: export ZOTERO_API_KEY=..." >&2
    exit 1
fi

python3 zotero_sync.py "$@"
