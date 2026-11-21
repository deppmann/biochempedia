/* The mini syllabus: from the ideas a question matched, a short path of films and lessons at one
   level, with the same idea one level simpler and one level deeper beside it.

   Pure JavaScript (no Astro, no Node, no network): the page (src/lib/start-page.ts) and
   scripts/test-syllabus.mjs run this file. The rules it keeps:
   - Honest minutes. A film counts its own length; a skim and a whole lesson count the figure the
     lesson page itself prints. The total is the sum of the steps and nothing else.
   - The three lengths are the lesson page's own stops: skim, films, lesson.
   - A path is two to five steps where the lessons allow it, and never padded.
   - When the reader's level has no lesson on the idea, the path uses the nearest level and says so.
   - Nothing is counted, scored or queued: the path is a list of links. */
import { LEVEL_SHORT } from './hop-words.mjs';
import { pickRungs, defaultLevel } from './syllabus-match.mjs';

export const TIMES = ['skim', 'films', 'lesson'];
export const MAX_STEPS = 5;

/** A saved "How long have you got?" choice as one of this page's three; 'films' when there is none. */
export const timeFrom = (saved) => (saved === 'skim' || saved === 'lesson' ? saved : saved === 'films' || saved === 'stories' ? 'films' : 'films');

/**
 * Turn one concept of /graph/<area>.json into rungs with their films.
 * @param {any} g the area file
 * @param {string} id concept id
 * @param {Record<string, [number, number, string[]]>} minutes /start/lessons.json `lessons`
 */
export function ideaFromArea(g, id, minutes = {}) {
  const c = g.concepts.find((x) => x.id === id);
  if (!c) return null;
  const rankOf = (li) => g.courses[g.lessons[li][2]][2];
  const films = new Map();
  for (const fi of c.f) {
    const [, title, li, sec, fid] = g.films[fi];
    const slug = g.lessons[li][0];
    if (!films.has(li)) films.set(li, []);
    films.get(li).push({ title, sec, href: `/watch/${slug}/${fid ? `${fid}/` : ''}` });
  }
  const rungs = c.r.filter((r) => r[1] === 0).map((r) => {
    const [slug, title, ci] = g.lessons[r[0]];
    const m = minutes[slug] ?? [0, 0];
    return {
      slug, title, rank: rankOf(r[0]), courseTitle: g.courses[ci][1], adds: r[2] || '', anchor: r[3] || '',
      href: `/lessons/${slug}/`, whole: m[0] || 0, skim: m[1] || 0, films: films.get(r[0]) ?? [],
      ...(films.get(r[0])?.[0] ? { film: { href: films.get(r[0])[0].href, seconds: films.get(r[0])[0].sec, title: films.get(r[0])[0].title } } : {}),
      ...(m[0] ? { minutes: m[0] } : {}),
    };
  });
  return { id, name: c.n, label: c.h ?? c.n, blurb: c.b, rungs, near: c.x.map(([nid, why]) => ({ id: nid, why })) };
}

/** Which level a path is built at: the reader's own if the idea has a lesson there, else the nearest (simpler first). */
export function levelFor(rungs, asked) {
  if (!rungs.length) return { rank: -1, moved: false };
  if (asked === null || asked === undefined || asked < 0) return { rank: defaultLevel(rungs), moved: false };
  if (rungs.some((r) => r.rank === asked)) return { rank: asked, moved: false };
  const below = rungs.filter((r) => r.rank < asked).map((r) => r.rank);
  const above = rungs.filter((r) => r.rank > asked).map((r) => r.rank);
  // An activity for young children is not offered to an older reader as "the nearest level" when something deeper exists.
  const down = below.length ? Math.max(...below) : -1;
  const up = above.length ? Math.min(...above) : -1;
  const rank = down >= 1 || up < 0 ? (down >= 0 ? down : up) : up;
  return { rank, moved: true };
}

const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.round(s) % 60).padStart(2, '0')}`;

function stepsFor(rung, time, room) {
  const steps = [];
  const guide = rung.rank === 0;
  const film = (f) => ({ kind: 'film', title: f.title, href: f.href, sec: f.sec, length: mmss(f.sec) });
  const whole = { kind: guide ? 'activity' : 'lesson', title: rung.title, href: `/lessons/${rung.slug}/?time=lesson`, sec: rung.whole * 60, length: `${rung.whole} min`, slug: rung.slug, ...(rung.anchor && !guide ? { part: `/lessons/${rung.slug}/#${rung.anchor}` } : {}) };
  const skim = rung.skim ? { kind: 'skim', title: rung.title, href: `/lessons/${rung.slug}/?time=skim`, sec: rung.skim * 60, length: `${rung.skim} min`, slug: rung.slug } : null;
  if (time === 'lesson' || (!skim && !rung.films.length)) return rung.whole ? [whole] : [];
  // An activity guide has no skim: its short version is its set-up film alone.
  if (guide) return rung.films.slice(0, 1).map(film);
  const n = time === 'skim' ? 1 : Math.max(1, room - 1);
  for (const f of rung.films.slice(0, n)) steps.push(film(f));
  if (skim) steps.push(skim);
  return steps.slice(0, room);
}

/**
 * @param {{ id: string, name: string, label: string, rungs: any[] }[]} ideas the matched ideas, main one first (one or two)
 * @param {{ level?: number | null, time?: 'skim' | 'films' | 'lesson', prefer?: (string | undefined)[] }} o
 */
export function buildPath(ideas, o = {}) {
  const time = TIMES.includes(o.time) ? o.time : 'films';
  const main = ideas[0];
  if (!main) return null;
  const at = levelFor(main.rungs, o.level);
  const make = (t) => {
    const steps = [];
    const used = new Set();
    ideas.slice(0, 2).forEach((it, k) => {
      const lv = k === 0 ? at.rank : levelFor(it.rungs, at.rank).rank;
      const rung = pickRungs(it.rungs, lv, o.prefer?.[k]).at.find((r) => !used.has(r.slug));
      if (!rung) return;
      used.add(rung.slug);
      const room = Math.max(1, Math.floor((MAX_STEPS - steps.length) / (ideas.slice(0, 2).length - k)));
      for (const s of stepsFor(rung, t, room)) steps.push({ ...s, idea: it.id, rank: rung.rank, adds: s.kind === 'film' ? '' : rung.adds });
    });
    const sec = steps.reduce((n, s) => n + s.sec, 0);
    return { steps, minutes: Math.max(1, Math.round(sec / 60)) };
  };
  const paths = Object.fromEntries(TIMES.map((t) => [t, make(t)]));
  const beside = pickRungs(main.rungs, at.rank);
  const side = (r) => (r ? { slug: r.slug, title: r.title, rank: r.rank, level: LEVEL_SHORT[r.rank], adds: r.adds, href: `/lessons/${r.slug}/`, minutes: r.whole, film: r.films[0] ? { href: r.films[0].href, length: mmss(r.films[0].sec), title: r.films[0].title } : null } : null);
  return {
    time, rank: at.rank, level: LEVEL_SHORT[at.rank] ?? '', moved: at.moved, asked: o.level ?? null,
    steps: paths[time].steps, minutes: paths[time].minutes,
    stops: Object.fromEntries(TIMES.map((t) => [t, paths[t].minutes])),
    down: side(beside.down[0]), up: side(beside.up[0]),
  };
}
