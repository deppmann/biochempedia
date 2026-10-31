import { readFileSync } from 'node:fs';
import { join, normalize } from 'node:path';

/**
 * A film's caption file (WebVTT, in public/) as readable paragraphs, for the "Read the transcript"
 * section beside each film. The transcript is real page text: it is searchable (Pagefind indexes it,
 * see src/lib/lesson-search.ts) and it helps anyone who cannot play the film.
 *
 * Runs at build time only. A missing or unreadable file returns null and the page simply shows no
 * transcript; it never fails the build.
 */

const ENTITIES: Record<string, string> = { '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&nbsp;': ' ', '&lrm;': '', '&rlm;': '' };

const clock = (s: string): number => {
  const p = s.trim().split(':').map(Number);
  return p.length === 3 ? p[0] * 3600 + p[1] * 60 + p[2] : p[0] * 60 + p[1];
};

/** Parses WebVTT text into paragraphs: cue numbers, timings, notes and tags dropped; cues joined
 *  into sentences; a new paragraph at a pause of a second and a half or more once the current one
 *  is a few sentences long, and never longer than about 650 characters. */
export function paragraphsFromVtt(vtt: string): string[] {
  const cues: { start: number; end: number; text: string }[] = [];
  for (const block of vtt.replace(/\r/g, '').split(/\n{2,}/)) {
    const lines = block.split('\n').map((l) => l.trim()).filter(Boolean);
    if (!lines.length || /^(WEBVTT|NOTE|STYLE|REGION)\b/.test(lines[0])) continue;
    const ti = lines.findIndex((l) => l.includes('-->'));
    if (ti === -1) continue;
    const [a, b] = lines[ti].split('-->');
    const text = lines.slice(ti + 1).join(' ')
      .replace(/<[^>]+>/g, '')
      .replace(/&(?:amp|lt|gt|quot|#39|nbsp|lrm|rlm);/g, (m) => ENTITIES[m] ?? m)
      .replace(/\s+/g, ' ').trim();
    if (text) cues.push({ start: clock(a), end: clock(b.trim().split(/\s+/)[0]), text });
  }
  const out: string[] = [];
  let cur = '';
  let prevEnd = 0;
  for (const c of cues) {
    const pause = c.start - prevEnd;
    const ended = /[.?!…]["”')\]]*$/.test(cur);
    if (cur && ended && ((pause >= 1.5 && cur.length >= 220) || cur.length >= 650)) { out.push(cur); cur = ''; }
    cur = cur ? `${cur} ${c.text}` : c.text;
    prevEnd = c.end;
  }
  if (cur) out.push(cur);
  return out;
}

/** Reads the transcript for a captions path as written in a lesson's frontmatter, e.g.
 *  "/explainers/sleep-or-travel/explainer.vtt". Null if there is none to show. */
export function transcriptFor(captions: string | undefined): string[] | null {
  try {
    if (!captions || !/^\/explainers\/[a-z0-9/._-]+\.vtt$/i.test(captions) || captions.includes('..')) return null;
    const file = normalize(join(process.cwd(), 'public', captions));
    const paras = paragraphsFromVtt(readFileSync(file, 'utf8'));
    return paras.length ? paras : null;
  } catch {
    return null;
  }
}
