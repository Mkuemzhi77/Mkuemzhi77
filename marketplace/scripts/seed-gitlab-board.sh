#!/usr/bin/env bash
# Create labels + starter issues on GitLab (needs token with api / issues write).
# Usage:
#   export GITLAB_TOKEN=glpat-...
#   export GITLAB_PROJECT=myvibe-group/marketplacep2p
#   ./scripts/seed-gitlab-board.sh
set -euo pipefail

TOKEN="${GITLAB_TOKEN:?Set GITLAB_TOKEN}"
PROJECT="${GITLAB_PROJECT:-myvibe-group/marketplacep2p}"
API="https://gitlab.com/api/v4"
ENC="$(python3 -c "import urllib.parse; print(urllib.parse.quote('$PROJECT', safe=''))")"

auth=(-H "PRIVATE-TOKEN: $TOKEN" -H "Content-Type: application/json")

create_label() {
  local name="$1" color="$2"
  curl -sS -o /tmp/gl_label.json -w "%{http_code}" -X POST "$API/projects/$ENC/labels" \
    "${auth[@]}" \
    -d "{\"name\":\"$name\",\"color\":\"$color\"}" >/tmp/gl_label_code
  code=$(cat /tmp/gl_label_code)
  if [[ "$code" == "201" || "$code" == "409" ]]; then
    echo "label ok: $name ($code)"
  else
    echo "label fail: $name → $code $(cat /tmp/gl_label.json)"
  fi
}

create_issue() {
  local title="$1" labels="$2" desc="$3"
  curl -sS -o /tmp/gl_issue.json -w "%{http_code}" -X POST "$API/projects/$ENC/issues" \
    "${auth[@]}" \
    --data-binary @- <<EOF >/tmp/gl_issue_code
{"title":$(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$title"),"labels":"$labels","description":$(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$desc")}
EOF
  code=$(cat /tmp/gl_issue_code)
  if [[ "$code" == "201" ]]; then
    iid=$(python3 -c "import json; print(json.load(open('/tmp/gl_issue.json'))['iid'])")
    echo "issue #$iid: $title"
  else
    echo "issue fail: $title → $code $(head -c 200 /tmp/gl_issue.json)"
  fi
}

echo "Seeding labels for $PROJECT ..."
create_label "role::backend" "#1D4ED8"
create_label "role::frontend" "#7C3AED"
create_label "role::shared" "#64748B"
create_label "stage::0" "#0F766E"
create_label "stage::1" "#0F766E"
create_label "stage::2" "#0F766E"
create_label "stage::3" "#0F766E"
create_label "stage::4" "#0F766E"
create_label "size::S" "#F59E0B"
create_label "size::M" "#F59E0B"
create_label "size::L" "#F59E0B"
create_label "status::todo" "#94A3B8"
create_label "status::doing" "#EAB308"
create_label "status::blocked" "#DC2626"

echo "Seeding issues ..."
create_issue "T0-2: Protect main + MR rules" "role::shared,stage::0,size::S,status::todo" "Settings → Repository → Protected branches. Require MR. Assignee: Backend."
create_issue "T0-3: Agree ERD users/items/inventory/wallet" "role::shared,stage::1,size::M,status::todo" "Together. Update docs/domain.md. Blocks backend models."
create_issue "T0-4: Draft OpenAPI auth + health" "role::shared,stage::1,size::M,status::todo" "Together. Contract for frontend mocks."
create_issue "T1-A1: FastAPI skeleton health/settings/logging" "role::backend,stage::1,size::M,status::todo" "Backend. See ROADMAP stage 1."
create_issue "T1-A2: Docker Compose api + postgres" "role::backend,stage::1,size::M,status::todo" "Backend."
create_issue "T1-A3: Alembic + users migration" "role::backend,stage::1,size::M,status::todo" "Backend. After T0-3."
create_issue "T1-A4: JWT register/login/me" "role::backend,stage::1,size::L,status::todo" "Backend."
create_issue "T1-B1: Scaffold React/TS + routing" "role::frontend,stage::1,size::M,status::todo" "Frontend."
create_issue "T1-B2: Login/Register pages + JWT storage" "role::frontend,stage::1,size::M,status::todo" "Frontend. Can mock until T1-A4."
create_issue "T1-B3: Layout + API client" "role::frontend,stage::1,size::M,status::todo" "Frontend."
create_issue "T2-A1: Models items/inventories/wallets + seed" "role::backend,stage::2,size::L,status::todo" "Backend."
create_issue "T2-A2: Inventory API + create/cancel listing" "role::backend,stage::2,size::L,status::todo" "Backend."
create_issue "T2-B1: Catalog page from API" "role::frontend,stage::2,size::M,status::todo" "Frontend."
create_issue "T2-B2: User inventory page" "role::frontend,stage::2,size::M,status::todo" "Frontend."
create_issue "T2-B3: Create/cancel listing form" "role::frontend,stage::2,size::M,status::todo" "Frontend."
create_issue "T3-A1: Buy Now atomic transaction + ledger" "role::backend,stage::3,size::L,status::todo" "Backend core."
create_issue "T3-A2: Parallel buy race integration test" "role::backend,stage::3,size::M,status::todo" "Backend. Required for merge."
create_issue "T3-B1: Buy button loading/error states" "role::frontend,stage::3,size::M,status::todo" "Frontend."
create_issue "T3-B2: Trades history page" "role::frontend,stage::3,size::S,status::todo" "Frontend."

echo "Done. Open: https://gitlab.com/$PROJECT/-/issues"
echo "Then create Board: Plan → Issue boards → columns by status::*"
