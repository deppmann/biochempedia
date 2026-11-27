/* /search-records.json (2026-11-22): the typed search records, for the build only.

   Everything worth finding that is not a lesson page, as records (src/lib/search-records.mjs says
   what a record is): every film with its whole narration, every method, every Side Hop story and
   audio segment, every ladder, every flashcard deck and every simulation. scripts/build-search-index.mjs adds them
   to the Pagefind index after `astro build` and then deletes this file from dist/, so it is never
   served: the browser only ever loads the Pagefind chunks a query needs.

   Every record needs a URL of its own, apart from the hash: Pagefind keeps one entry per URL, so a
   record at /lessons/<slug>/ would replace the lesson page itself. Records on a lesson page carry a
   small query (?hop=1, ?cards=1, ?sim=1) that the page ignores. */
import type { APIRoute } from 'astro';
import { readFileSync } from 'node:fs';
import { join, normalize } from 'node:path';
import { getCollection } from 'astro:content';
import { filmCatalog, filmKey, kindBadge } from '../lib/film-catalog';
import { METHODS, methodHref } from '../data/methods';
import { COURSES, courseOf } from '../data/courses';
import { STAGES, stageOf } from '../data/stages';
import { KIND_LOOK, type SideHopsData } from '../lib/side-hops';
import type { Deck } from '../lib/flashcards';
import { lessonHop, allIdeas } from '../lib/hop';
import { filmLadders } from '../lib/film-ladders';
import { runsFromVtt, timeId, clock, clozeText } from '../lib/search-records.mjs';

type Rec = {
  type: string; url: string; title: string; lead?: string; kicker?: string; courses?: string[]; courseTitle?: string;
  level?: string; levelTitle?: string; lesson?: string; ladder?: string; poster?: string; dur?: number; filmKey?: string; films?: number;
  parts: { id?: string; h?: string; text: string; w?: number }[];
};

const HOPS = import.meta.glob<{ default: SideHopsData }>('../data/side-hops/*.json', { eager: true });
const DECKS = import.meta.glob<{ default: Deck }>('../data/flashcards/*.json', { eager: true });

/** The narration of a film as timed runs, from its caption file in public/. Empty if it has none. */
function narration(captions: string | undefined): { id: string; h: string; text: string }[] {
  if (!captions || !/^\/explainers\/[a-z0-9/._-]+\.vtt$/i.test(captions) || captions.includes('..')) return [];
  try {
    const vtt = readFileSync(normalize(join(process.cwd(), 'public', captions)), 'utf8');
    return runsFromVtt(vtt).map((r) => ({ id: timeId(r.start), h: clock(r.start), text: r.text }));
  } catch {
    return [];
  }
}

export const GET: APIRoute = async () => {
  const lessons = await getCollection('lessons', ({ data }) => !data.draft);
  const live = new Map(lessons.map((l) => [l.data.slug, l.data]));
  const stageTitle = (k: string) => STAGES.find((s) => s.key === k)?.title ?? k;
  const where = (slug: string) => {
    const d = live.get(slug)!;
    const c = courseOf(d.course);
    const stage = stageOf(c);
    return { courses: [c.slug], courseTitle: c.title, level: stage, levelTitle: stageTitle(stage), lesson: d.title };
  };
  /* The idea (hop ladder) a lesson teaches first, when the graph knows it. */
  const ladders = new Map<string, string>();
  for (const slug of live.keys()) {
    try {
      const h = await lessonHop(slug);
      if (h?.ideas[0]) ladders.set(slug, h.ideas[0].name);
    } catch { /* no ladder: fine */ }
  }
  const lessonBits = (slug: string) => ({ ...where(slug), ...(ladders.has(slug) ? { ladder: ladders.get(slug) } : {}) });

  const out: Rec[] = [];

  /* Films: every lesson, activity and profile film, with its take-homes and whole narration. Method
     films are the methods' records below. */
  for (const f of await filmCatalog()) {
    if (f.kind === 'method' || !f.lesson || !live.has(f.lesson)) continue;
    const runs = narration(f.captions);
    // A scientist profile film opens in a pop-up on its lesson page (/lessons/x/#lb-sci-0): a query of
    // its own keeps its URL apart from the lesson's (see the header).
    const profile = f.href.startsWith('/lessons/');
    out.push({
      type: 'film',
      url: profile ? f.href.replace('#', `?profile=${encodeURIComponent(filmKey(f.src))}#`) : f.href,
      title: f.title,
      lead: f.lessonTitle && f.lessonTitle !== f.title ? f.lessonTitle : f.description,
      kicker: kindBadge(f),
      ...lessonBits(f.lesson),
      poster: f.poster,
      dur: Math.round(f.durationSec),
      ...(profile ? {} : { filmKey: filmKey(f.src) }),
      parts: [
        ...(f.takeaways?.length ? [{ id: 'take-homes', h: 'Take-homes', text: f.takeaways.join(' '), w: 2 }] : []),
        ...runs,
      ],
    });
  }

  /* Ladders: one idea at every level it is taught, played on /films/ (?ladder=<id>): exactly the
     ladders of the films-page picker (filmLadders, src/lib/film-ladders.ts). Found by the idea's name,
     its blurb and other names, and the titles of the films and lessons on it. */
  const ideas = new Map((await allIdeas()).map((i) => [i.id, i]));
  const filmBySrcKey = new Map((await filmCatalog()).map((f) => [filmKey(f.src), f]));
  for (const l of await filmLadders()) {
    const i = ideas.get(l.id);
    const seconds = l.films.reduce((t, f) => t + f[4], 0);
    out.push({
      type: 'ladder',
      url: `/films/?ladder=${encodeURIComponent(l.id)}`,
      title: l.name,
      lead: i?.blurb,
      kicker: `Ladder · ${l.films.length} films · ${new Set(l.films.map((f) => f[3])).size} levels`,
      courseTitle: l.area,
      courses: [...new Set(l.films.map((f) => filmBySrcKey.get(f[0])?.course).filter((c): c is string => !!c))],
      poster: l.films[0]?.[5],
      dur: Math.round(seconds),
      films: l.films.length,
      parts: [
        ...(i?.aliases?.length ? [{ text: `Also called ${i.aliases.join(', ')}.`, w: 3 }] : []),
        { id: 'films', h: 'Films on this ladder', text: l.films.map((f) => f[1]).join(' · '), w: 2 },
        { id: 'lessons', h: 'Lessons on this ladder', text: l.rungs.map((r) => `${r.title} (${r.courseTitle})`).join(' · '), w: 2 },
      ],
    });
  }

  /* Methods: every method page, with its own film's narration when it has one. */
  for (const m of METHODS) {
    const courses = [...new Set(m.lessons.filter((s) => live.has(s)).map((s) => live.get(s)!.course))];
    const own = m.film && !m.film.from ? m.film : undefined;
    out.push({
      type: 'method',
      url: methodHref(m.slug),
      title: m.name,
      lead: m.summary,
      kicker: m.film ? 'Method with a film' : 'Method',
      courses,
      ...(m.film ? { poster: m.film.poster, dur: Math.round(m.film.durationSec), filmKey: filmKey(m.film.src) } : {}),
      parts: [
        ...(m.aka?.length ? [{ text: `Also called ${m.aka.join(', ')}.`, w: 3 }] : []),
        ...(m.unlocked?.length ? [{ id: 'unlocked', h: 'What it unlocked', text: m.unlocked.map((u) => u.text).join(' ') }] : []),
        ...(own ? narration(own.captions) : []),
      ],
    });
  }

  /* Side Hops: one record per card. */
  for (const { default: d } of Object.values(HOPS)) {
    if (!live.has(d.slug)) continue;
    const bits = lessonBits(d.slug);
    d.hops.forEach((h, i) => {
      out.push({
        type: 'sidehop',
        url: `/lessons/${d.slug}/?hop=${i + 1}#sh-${i + 1}`,
        title: h.title,
        kicker: `Side Hop · ${KIND_LOOK[h.kind]?.label ?? 'Story'}`,
        ...bits,
        ...(h.image ? { poster: `/${h.image.file}` } : {}),
        parts: [{ text: h.text }, ...(h.image?.caption ? [{ text: h.image.caption, w: 2 }] : [])],
      });
    });
  }

  /* Flashcards: one record per deck, every card's front, back and why. */
  for (const { default: deck } of Object.values(DECKS)) {
    if (!deck.cards?.length || !live.has(deck.slug)) continue;
    out.push({
      type: 'flashcards',
      url: `/lessons/${deck.slug}/?cards=1#flashcards`,
      title: `Flashcards: ${live.get(deck.slug)!.title}`,
      kicker: `${deck.cards.length} flashcards`,
      ...lessonBits(deck.slug),
      parts: deck.cards.map((c) => ({ text: [clozeText(c.front), clozeText(c.back), c.why ?? ''].filter(Boolean).join(' — ') })),
    });
  }

  /* Simulations: the ones a lesson lists, by title and caption. */
  for (const l of lessons) {
    const d = l.data;
    (d.simulations ?? []).forEach((s: { type: string; title: string; caption?: string }, n: number) => {
      out.push({
        type: 'sim',
        url: `/lessons/${d.slug}/?sim=${n + 1}`,
        title: s.title,
        kicker: s.type === 'phet' ? 'PhET simulation' : 'Interactive',
        ...lessonBits(d.slug),
        parts: s.caption ? [{ text: s.caption }] : [],
      });
    });
  }

  const courseTitles = Object.fromEntries(COURSES.map((c) => [c.slug, c.title]));
  return new Response(JSON.stringify({ count: out.length, courseTitles, records: out }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};
