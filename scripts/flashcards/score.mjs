#!/usr/bin/env node
/* Unblind and tabulate a pilot: node scripts/flashcards/score.mjs <pilotDir>
   Reads judges/<j>/verdict.json + judges/<j>.key.json, gate/gate.json + gate/cards.key.json,
   goaltest/<k>/choice.json + goaltest/key.json, tokens.jsonl. Writes results.json and prints tables. */
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
const P = process.argv[2];
const J = (f) => JSON.parse(readFileSync(join(P, f), 'utf8'));
const DIMS = ['accuracy', 'usefulness', 'coverage', 'non_redundancy', 'ladder', 'craft', 'goal_tags', 'overall'];
const out = { judges: {}, arms: {}, formats: {}, gate: null, goaltest: {}, tokens: [] };

const judges = readdirSync(join(P, 'judges')).filter((f) => f.endsWith('.key.json')).map((f) => f.slice(0, -9));
for (const j of judges) {
  const vf = join('judges', j, 'verdict.json');
  if (!existsSync(join(P, vf))) { console.log(`(no verdict yet: ${j})`); continue; }
  const v = J(vf); const key = J(`judges/${j}.key.json`);
  const arms = {};
  for (const [L, s] of Object.entries(v.decks)) arms[key[L]] = s;
  const rank = (v.rank ?? []).map((L) => key[L]);
  const errors = (v.errors ?? []).map((e) => ({ ...e, arm: key[e.id?.[0]] }));
  const worst = (v.worst ?? []).map((e) => ({ ...e, arm: key[e.id?.[0]] }));
  out.judges[j] = { arms, rank, errors, worst, format_value: v.format_value };
}
const armNames = [...new Set(Object.values(out.judges).flatMap((x) => Object.keys(x.arms)))].sort();
for (const a of armNames) {
  const rows = Object.values(out.judges).map((x) => x.arms[a]).filter(Boolean);
  const mean = (d) => +(rows.reduce((s, r) => s + Number(r[d] ?? 0), 0) / rows.length).toFixed(2);
  out.arms[a] = {
    ...Object.fromEntries(DIMS.map((d) => [d, mean(d)])),
    would_assign: rows.filter((r) => String(r.would_assign).toLowerCase().startsWith('y')).length + '/' + rows.length,
    first_place: Object.values(out.judges).filter((x) => x.rank[0] === a).length,
    mean_rank: +(Object.values(out.judges).reduce((s, x) => s + (x.rank.indexOf(a) + 1), 0) / Object.keys(out.judges).length).toFixed(2),
    judge_must: Object.values(out.judges).flatMap((x) => x.errors).filter((e) => e.arm === a && e.severity === 'must').length,
    judge_minor: Object.values(out.judges).flatMap((x) => x.errors).filter((e) => e.arm === a && e.severity !== 'must').length,
    worst_flags: Object.values(out.judges).flatMap((x) => x.worst).filter((e) => e.arm === a).length,
  };
}
for (const t of ['cloze', 'qa', 'predict', 'experiment', 'calc']) {
  const vals = Object.values(out.judges).map((x) => Number(x.format_value?.[t])).filter((n) => !Number.isNaN(n));
  out.formats[t] = vals.length ? +(vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(2) : null;
}
if (existsSync(join(P, 'gate/gate.json'))) {
  const g = J('gate/gate.json'); const key = J('gate/cards.key.json');
  const per = {};
  for (const c of g.cards) {
    const k = key[c.id]; if (!k) continue;
    per[k.arm] ??= { cards: 0, ok: 0, minor: 0, must: 0, must_items: [] };
    per[k.arm].cards++; per[k.arm][c.verdict] = (per[k.arm][c.verdict] ?? 0) + 1;
    if (c.verdict === 'must') per[k.arm].must_items.push({ card: k.id, problem: c.problem });
  }
  out.gate = per;
}
if (existsSync(join(P, 'goaltest/key.json'))) {
  const key = J('goaltest/key.json');
  for (const k of Object.keys(key)) {
    const f = `goaltest/${k}/choice.json`;
    if (!existsSync(join(P, f))) continue;
    const c = J(f);
    out.goaltest[k] = { chose: key[k][c.choice], strength: c.strength, treatment: c.scores[key[k].P === 'treatment' ? 'P' : 'Q'], control: c.scores[key[k].P === 'control' ? 'P' : 'Q'], why: c.why, missing: c.missing };
  }
}
if (existsSync(join(P, 'tokens.jsonl'))) out.tokens = readFileSync(join(P, 'tokens.jsonl'), 'utf8').trim().split('\n').map((l) => JSON.parse(l));
writeFileSync(join(P, 'results.json'), JSON.stringify(out, null, 1));
console.table(out.arms);
console.log('formats', out.formats);
if (out.gate) console.table(Object.fromEntries(Object.entries(out.gate).map(([a, v]) => [a, { cards: v.cards, ok: v.ok, minor: v.minor, must: v.must }])));
console.log(JSON.stringify(out.goaltest, null, 1));
