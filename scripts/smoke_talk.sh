#!/usr/bin/env bash
# Smoke check: health + one NPC talk (server must be running).
set -euo pipefail
BASE="${AI_SERVER_URL:-http://127.0.0.1:8000}"
curl -sf "$BASE/health" | tee /dev/stderr
echo
curl -sf -X POST "$BASE/npc/npc-1/talk" \
  -H 'Content-Type: application/json' \
  -d '{"message":"Bonjour, résumé trésorerie"}'
echo
