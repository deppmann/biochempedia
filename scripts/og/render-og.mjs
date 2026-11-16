#!/usr/bin/env node
/* Render public/og.png (the share image, 1200 x 630) from scripts/og/og.html with a headless browser.
   No image generation: the card is HTML, with the wordmark from src/lib/wordmark.ts and its styles from
   src/styles/global.css. Playwright is not a dependency of the site; point PLAYWRIGHT at an installed
   copy (a package directory), and the system Chrome is used:
     PLAYWRIGHT=/path/to/node_modules/playwright node scripts/og/render-og.mjs
   Needs Node 22.18+ (it imports the .ts file) and network access for the two Google fonts. */
import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createRequire } from 'node:module';
import { wordmarkHtml } from '../../src/lib/wordmark.ts';

const root = new URL('../../', import.meta.url).pathname;
const css = readFileSync(join(root, 'src/styles/global.css'), 'utf8');
const start = css.indexOf('The STEMhop wordmark (markup in src/lib/wordmark.ts)');
if (start < 0) throw new Error('render-og: the wordmark block is missing from src/styles/global.css');
const block = css.slice(css.lastIndexOf('/*', start));
const html = readFileSync(join(root, 'scripts/og/og.html'), 'utf8')
  .replace('{{WORDMARK_CSS}}', block)
  .replace('{{WORDMARK}}', wordmarkHtml({ size: 168, hop: true }));
const dir = mkdtempSync(join(tmpdir(), 'og-'));
const page = join(dir, 'og.html');
writeFileSync(page, html);

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || 'chrome' });
const p = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1, colorScheme: 'light' });
await p.goto('file://' + page, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
const fonts = await p.evaluate(() => [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family));
if (!fonts.some((f) => /Playfair/.test(f))) throw new Error('render-og: Playfair Display did not load (offline?)');
await p.screenshot({ path: join(root, 'public/og.png'), clip: { x: 0, y: 0, width: 1200, height: 630 } });
await browser.close();
console.log('render-og: wrote public/og.png');
