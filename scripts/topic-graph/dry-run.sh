#!/bin/sh
# Hop graph: run a whole fill end to end with stand-in answers, to prove the plumbing before real
# readers spend effort. Writes only inside the staging folder given (default .graph-staging/dryrun),
# never to src/data. Some stand-in answers are broken on purpose, so the report must show rejected
# items and removed rungs; the run fails only if a step crashes or the merged graph breaks a rule.
#   sh scripts/topic-graph/dry-run.sh [staging-folder]
set -e
D=${1:-.graph-staging/dryrun}
rm -rf "$D"; mkdir -p "$D"; touch "$D/MOCK"
E="node scripts/topic-graph/emit.mjs"
I="node scripts/topic-graph/ingest.mjs --staging $D --out $D/topic-graph.json --quiet"
step() { echo; echo "== $1"; }
step "0 digests";            node scripts/topic-graph/digest.mjs --out "$D/digests" | tail -1
step "1 propose: prompts";   $E propose --staging "$D" | tail -1
step "1 propose: answers";   $E mock propose --staging "$D"
step "1 propose: ingest";    $I --no-canonical --no-near --no-verify | tail -1
step "2 canonicalize: prompts"; $E canonicalize --staging "$D" | tail -1
step "2 canonicalize: answers"; $E mock canonicalize --staging "$D"
step "2 across areas";       $E canonicalize --cross --staging "$D"; $E mock cross --staging "$D"
step "2b near: prompts";     $E near --staging "$D" | tail -1
step "2b near: answers";     $E mock near --staging "$D"
step "3 ingest";             $I --no-verify | tail -1
step "4 verify: prompts";    $E verify --staging "$D" | tail -1
step "4 verify: answers";    $E mock verify --staging "$D"
step "5 ingest with verdicts"; $I | tail -1
cp "$D/topic-graph.json" "$D/first.json"
step "5 again (the result must not change)"; $I | tail -1
cmp "$D/topic-graph.json" "$D/first.json" && echo "same bytes on a second run"
step "6 report"
sed -n '1,12p' "$D/reports/ingest.txt"
grep -E '^(CHANGES APPLIED|REJECTED ITEMS|NOTES|CHECK)' "$D/reports/ingest.txt"
node scripts/topic-graph/emit.mjs status --staging "$D"
echo; echo "dry run finished: full report in $D/reports/ingest.txt"
