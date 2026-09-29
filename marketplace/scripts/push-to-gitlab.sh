#!/usr/bin/env bash
# Push marketplace/ as the root of a GitLab repo.
# Usage:
#   ./scripts/push-to-gitlab.sh https://oauth2:<TOKEN>@gitlab.com/myvibe-group/marketplacep2p.git
set -euo pipefail

REMOTE_URL="${1:-}"
if [[ -z "$REMOTE_URL" ]]; then
  echo "Usage: $0 <gitlab-repo-url>"
  echo "Example: $0 https://oauth2:<TOKEN>@gitlab.com/myvibe-group/marketplacep2p.git"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

echo "Preparing clean export from: $ROOT"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude '.git' "$ROOT/" "$TMP/"
else
  cp -a "$ROOT"/. "$TMP/"
  rm -rf "$TMP/.git"
fi

cd "$TMP"
git init -b main
git add .
git -c user.email="${GIT_AUTHOR_EMAIL:-dev@localhost}" \
    -c user.name="${GIT_AUTHOR_NAME:-p2p-market}" \
    commit -m "docs: initial P2P Market scaffold (stage 0)"
git remote add origin "$REMOTE_URL"
echo "Pushing to GitLab ..."
git push -u origin main
echo "Done. Protect main and invite your teammate."
