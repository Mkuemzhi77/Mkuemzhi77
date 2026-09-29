#!/usr/bin/env bash
# Push marketplace/ as the root of a new GitLab repo.
# Usage:
#   ./scripts/push-to-gitlab.sh git@gitlab.com:<group>/<project>.git
set -euo pipefail

REMOTE_URL="${1:-}"
if [[ -z "$REMOTE_URL" ]]; then
  echo "Usage: $0 <gitlab-repo-url>"
  echo "Example: $0 git@gitlab.com:mygroup/p2p-market.git"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

echo "Preparing clean export from: $ROOT"
rsync -a --exclude '.git' "$ROOT/" "$TMP/"
cd "$TMP"
git init -b main
git add .
git commit -m "docs: initial P2P Market scaffold (stage 0)"
git remote add origin "$REMOTE_URL"
echo "Pushing to $REMOTE_URL ..."
git push -u origin main
echo "Done. Open the GitLab project and protect main + enable CI."
