#!/usr/bin/env node
/**
 * Film end-card guard (source-level; needs no build, reads no video).
 *
 * The end card is a short silent card. On 2026-11-16 a film was found whose closing narration ran for
 * 21 s over its end card (the card came up while the narrator was still talking). For every film
 * (explainers/<slug>[/<chapter>]/script.json beside a scenes.py) this check FAILS when:
 *   - the last scene is spoken (non-empty `tts` or `narration`) while its class in scenes.py is an
 *     EndCard (directly or through another class, including the shared pipeline classes): the closing
 *     narration belongs to its own scene before the card;
 *   - a scene whose class is an EndCard is spoken anywhere in the film;
 *   - an EndCard scene is longer than MAX_CARD_S (its `silent` length plus render.py's 0.4 s tail).
 * A film that closes on a spoken scene that is not an EndCard (e.g. teachers-fast-tools-slow-thinking)
 * passes: that is a design choice, not a card with narration over it.
 *
 * Run: node scripts/check-film-scripts.mjs   (also run by CI on every push)
 */
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(new URL('.', import.meta.url)), '..');
const EXP = join(ROOT, 'explainers');
const PIPE = join(EXP, '_pipeline');
const TAIL = 0.4;          // render.py / kx_manim.py: stillness after the scene's audio
// A standard card is 3.5 s + tail = 3.9 s. The limit allows the two longest deliberate cards on main
// (bio-vitalism-louis-pasteur 6.4 s, bio-vitalism-berzelius 6.9 s) and still catches narration-length cards.
const MAX_CARD_S = 7.0;

const camel = (id) => id.split(/[_\-\s]+/).filter(Boolean).map((p) => p[0].toUpperCase() + p.slice(1)).join('');
const spoken = (s) => Boolean((s.tts && String(s.tts).trim()) || (s.narration && String(s.narration).trim()));

// class name -> list of base names, from one Python source
function classBases(src) {
  const out = new Map();
  for (const m of src.matchAll(/^class\s+(\w+)\s*(?:\(([^)]*)\))?\s*:/gm)) {
    out.set(m[1], (m[2] || '').split(',').map((b) => b.trim().split('.').pop()).filter(Boolean));
  }
  return out;
}

// shared classes from the pipeline (EndCard, SetupEnd, and the setup template's S05End)
const shared = new Map();
for (const f of readdirSync(PIPE).filter((x) => x.endsWith('.py'))) {
  for (const [k, v] of classBases(readFileSync(join(PIPE, f), 'utf8'))) if (!shared.has(k)) shared.set(k, v);
}

function isEndCard(name, local, seen = new Set()) {
  if (name === 'EndCard') return true;
  if (seen.has(name)) return false;
  seen.add(name);
  const bases = local.get(name) ?? shared.get(name) ?? [];
  return bases.some((b) => isEndCard(b, local, seen));
}

function filmDirs(dir, depth = 0, acc = []) {
  for (const e of readdirSync(dir)) {
    if (e.startsWith('.') || e.startsWith('_')) continue;
    const p = join(dir, e);
    if (!statSync(p).isDirectory()) continue;
    if (existsSync(join(p, 'script.json')) && existsSync(join(p, 'scenes.py'))) acc.push(p);
    if (depth < 1) filmDirs(p, depth + 1, acc);
  }
  return acc;
}

const failures = [];
let films = 0, cards = 0;
for (const d of filmDirs(EXP)) {
  const rel = relative(ROOT, d);
  let script;
  try { script = JSON.parse(readFileSync(join(d, 'script.json'), 'utf8')); } catch (e) {
    failures.push(`${rel}/script.json: not valid JSON (${e.message})`);
    continue;
  }
  const scenes = Array.isArray(script.scenes) ? script.scenes : [];
  if (!scenes.length) continue;
  films++;
  const local = classBases(readFileSync(join(d, 'scenes.py'), 'utf8'));
  const known = (n) => local.has(n) || shared.has(n);
  scenes.forEach((s, i) => {
    const cls = [s.id, camel(String(s.id))].find(known);
    if (!cls || !isEndCard(cls, local)) return;
    cards++;
    const last = i === scenes.length - 1;
    if (spoken(s)) {
      failures.push(`${rel}: ${last ? 'the last scene' : 'scene'} "${s.id}" (${cls}) is an EndCard but has narration. `
        + 'The end-card scene is silent: no tts. Closing narration belongs to the scene before it.');
      return;
    }
    const len = (Number(s.silent) || 0) + TAIL;
    if (len > MAX_CARD_S) {
      failures.push(`${rel}: end card "${s.id}" lasts about ${len.toFixed(1)} s (silent ${s.silent} + ${TAIL} s tail); `
        + `keep end cards at or under ${MAX_CARD_S} s (standard: silent 3.5).`);
    }
  });
}

if (failures.length) {
  for (const f of failures) console.log(`FAIL  ${f}`);
  console.log(`\n${failures.length} problem(s) in ${films} films.`);
  process.exit(1);
}
console.log(`ok  ${films} films, ${cards} end-card scenes: all silent and at most ${MAX_CARD_S} s`);
