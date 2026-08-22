#!/usr/bin/env node
/**
 * Scoped-CSS / runtime-DOM guard (source-level; needs no build).
 *
 * Astro scopes a component's <style> by stamping data-astro-cid-* on the
 * elements in its TEMPLATE. Elements the component's <script> creates at
 * runtime (createElement, innerHTML) never get the stamp, so scoped rules
 * that target them silently never apply. On 2026-08-13 this was live on 14
 * islands — JS-built chips, cards, rungs and bars rendered as raw unstyled
 * text while their scripts dutifully toggled classes nobody could see.
 *
 * This finds the pattern statically: a class assigned to a runtime-created
 * element that is also targeted by a scoped (non-is:global) rule without a
 * :global() wrapper. The fix is `<style is:global>` with every selector
 * anchored to the component's prefix, or :global() on the affected rules.
 *
 * Run: node scripts/check-scoped-styles.mjs   (also run by CI on every push)
 */
import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';

const DIR = join(process.cwd(), 'src', 'components');
const esc = (s) => s.replace(/[-]/g, '\\-');
const failures = [];

for (const f of (await readdir(DIR)).filter((x) => x.endsWith('.astro')).sort()) {
  const t = await readFile(join(DIR, f), 'utf8');
  const scoped = [...t.matchAll(/<style([^>]*)>([\s\S]*?)<\/style>/g)]
    .filter((m) => !/is:global/.test(m[1])).map((m) => m[2]).join('\n');
  const script = [...t.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
  if (!scoped || !script) continue;

  // Classes that land on runtime-created elements.
  const created = new Set();
  const vars = [...script.matchAll(/(?:const|let|var)\s+(\w+)\s*=\s*document\.createElement(?:NS)?\(/g)].map((m) => m[1]);
  for (const v of vars) {
    for (const m of script.matchAll(new RegExp(`\\b${v}\\.className\\s*=\\s*[\`'"]([^\`'"]+)`, 'g'))) m[1].split(/\s+/).forEach((c) => created.add(c));
    for (const m of script.matchAll(new RegExp(`\\b${v}\\.classList\\.(?:add|toggle)\\(\\s*['"]([^'"]+)`, 'g'))) created.add(m[1]);
    for (const m of script.matchAll(new RegExp(`\\b${v}\\.setAttribute\\(\\s*['"]class['"]\\s*,\\s*[\`'"]([^\`'"]+)`, 'g'))) m[1].split(/\s+/).forEach((c) => created.add(c));
  }
  // innerHTML-built markup: every class="…" inside it is on an unstamped node.
  for (const m of script.matchAll(/innerHTML\s*=\s*`([\s\S]*?)`/g)) {
    for (const c of m[1].matchAll(/class="([^"]+)"/g)) c[1].split(/\s+/).forEach((x) => created.add(x));
  }
  // Helper factories like el('div', { class: 'foo' }) used with createElement.
  if (/createElement(?:NS)?\(/.test(script)) {
    for (const m of script.matchAll(/\bclass:\s*[`'"]([^`'"]+)/g)) m[1].split(/\s+/).forEach((c) => created.add(c));
  }

  const hits = [];
  for (const c of created) {
    if (!c || /\$\{/.test(c)) continue;
    const styled = new RegExp(`\\.${esc(c)}(?![\\w-])`).test(scoped);
    const globalized = new RegExp(`:global\\(\\.${esc(c)}(?![\\w-])`).test(t);
    if (styled && !globalized) hits.push(c);
  }
  if (hits.length) failures.push(`${f}: scoped CSS targets runtime-created class${hits.length > 1 ? 'es' : ''} .${hits.join(' .')}`);
}

if (failures.length) {
  console.error(`\n✗ check-scoped-styles: ${failures.length} component(s) style JS-created elements with scoped CSS that can never reach them:\n`);
  for (const x of failures) console.error(`  ${x}`);
  console.error(`\n  Fix: make the block <style is:global> (every selector anchored to the component prefix), or wrap the affected rules in :global().\n`);
  process.exit(1);
}
console.log('✓ check-scoped-styles: no scoped rule targets a runtime-created element.');
