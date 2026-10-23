#!/usr/bin/env node
/**
 * Refresh the PUBLIC copy of the "Fast Tools, Slow Thinking" talk deck that /teachers embeds.
 *
 *   node scripts/refresh-teachers-deck.mjs [TALK_DIR]
 *
 * TALK_DIR is the talk folder inside the workshop folder, the one that holds public/slides/talk/
 * (default: ~/Dropbox/Chris/teaching/2026-10-24 AI teacher workshop/talk). Build the deck there
 * first (see its README: tools/gen_v4_boards.py, then build.py).
 *
 * What it does, and why the public copy differs from the private deck:
 *   - Drops notes.json entirely. Speaker notes are private; nothing here ever fetches them.
 *   - Keeps only the main path: every step whose group is "Appendix" is removed (the deck.json
 *     meta counts are recomputed), and so are the images only those steps used.
 *   - Moves the movies out of public/teachers/ to public/explainers/talk-deck/, so that
 *     scripts/upload-media.mjs sends them to R2 and the edge worker answers byte ranges (Safari
 *     will not play video without them). deck.json points at them by absolute path.
 *   - Adds an English caption track to each movie, from the .vtt that sits next to the .mp4 in the
 *     workshop folder (the folder above TALK_DIR).
 *   - Copies the viewer as it is (index.html, viewer.js, viewer.css, fonts). The private browse.*
 *     files are not copied. With no /api/me the viewer falls back to audience mode, and
 *     ?presenter=1 shows "speaker notes could not be loaded" because there is no notes.json.
 *
 * What it does NOT do: build the PDF, or upload anything. The PDF is main-only screenshots of the
 * deck (see docs/teachers/README.md); upload the movies with `node scripts/upload-media.mjs`
 * only when deploying.
 */
import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync, copyFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, extname } from 'node:path';

const TALK = process.argv[2] || join(homedir(), 'Dropbox/Chris/teaching/2026-10-24 AI teacher workshop/talk');
const SRC = join(TALK, 'public/slides/talk');
const WORKSHOP = join(TALK, '..');
const OUT = join('public', 'teachers', 'talk');
const MOVIES = join('public', 'explainers', 'talk-deck');
const MOVIE_URL = '/explainers/talk-deck';
const MAX_MOVIE_MB = 8;

if (!existsSync(join(SRC, 'deck.json'))) {
  console.error(`No deck.json at ${SRC}. Build the deck first, or pass the talk folder as the first argument.`);
  process.exit(1);
}

const deck = JSON.parse(readFileSync(join(SRC, 'deck.json'), 'utf8'));
const steps = deck.steps.filter((s) => s.group !== 'Appendix');
const dropped = deck.steps.length - steps.length;

// Movies: rewrite src to an absolute path, add a captions track, and collect the files to copy.
const movies = new Map();   // file name -> source path
for (const s of steps) {
  s.html = s.html.replace(/<video\b([^>]*?)\bsrc="assets\/([^"]+\.mp4)"([^>]*)>([\s\S]*?)<\/video>/g, (_m, pre, file, post, inner) => {
    movies.set(file, join(SRC, 'assets', file));
    const stem = file.replace(/\.[0-9a-f]{8}\.mp4$/, '');       // sizzle_biochempedia_45s.9798c372.mp4 -> sizzle_biochempedia_45s
    const vtt = join(WORKSHOP, `${stem}.vtt`);
    let track = '';
    if (existsSync(vtt)) {
      const vttName = `${file.replace(/\.mp4$/, '')}.vtt`;
      movies.set(vttName, vtt);
      track = `<track kind="captions" srclang="en" label="English" src="${MOVIE_URL}/${vttName}">`;
    } else console.warn(`warning: no captions file at ${vtt}`);
    return `<video${pre}src="${MOVIE_URL}/${file}"${post}>${inner}${track}</video>`;
  });
}

// Keep only the images the remaining steps use.
const used = new Set();
for (const s of steps) for (const m of s.html.matchAll(/assets\/([\w.-]+\.(?:jpg|jpeg|png|webp|svg))/g)) used.add(m[1]);

const slides = new Set(steps.map((s) => s.slide));
deck.steps = steps;
deck.meta = {
  slides: slides.size,
  reveals: new Set(steps.filter((s) => s.step === 'a').map((s) => s.slide)).size,
  movies: steps.filter((s) => /<video\b/.test(s.html)).length,
};

// Write the public deck, starting clean so a removed slide's files do not linger.
rmSync(OUT, { recursive: true, force: true });
mkdirSync(join(OUT, 'assets'), { recursive: true });
for (const f of ['index.html', 'viewer.js', 'viewer.css']) copyFileSync(join(SRC, f), join(OUT, f));
cpSync(join(SRC, 'fonts'), join(OUT, 'fonts'), { recursive: true });
for (const f of used) {
  if (!existsSync(join(SRC, 'assets', f))) { console.error(`deck.json uses assets/${f}, which is not in ${SRC}/assets`); process.exit(1); }
  copyFileSync(join(SRC, 'assets', f), join(OUT, 'assets', f));
}
writeFileSync(join(OUT, 'deck.json'), JSON.stringify(deck) + '\n');

mkdirSync(MOVIES, { recursive: true });
for (const f of readdirSync(MOVIES)) rmSync(join(MOVIES, f), { force: true });
for (const [name, from] of movies) {
  if (extname(name) === '.mp4' && statSync(from).size > MAX_MOVIE_MB * 1e6) {
    console.error(`${name} is over ${MAX_MOVIE_MB} MB; re-encode it first.`);
    process.exit(1);
  }
  copyFileSync(from, join(MOVIES, name));
}

console.log(`main path only: ${steps.length} steps (${dropped} appendix steps dropped), ${slides.size} slides`);
console.log(`images kept: ${used.size}; movies and captions: ${[...movies.keys()].join(', ')}`);
console.log(`wrote ${OUT}/ and ${MOVIES}/ (no notes.json)`);
console.log('Next: node scripts/upload-media.mjs (when deploying) sends the files in public/explainers/talk-deck/ to R2.');
