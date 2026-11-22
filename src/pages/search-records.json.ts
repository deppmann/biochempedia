/* /search-records.json (2026-11-22): the typed search records, for the build only.

   Everything worth finding that is not a lesson page, as records (src/lib/search-records.mjs says
   what a record is): every film with its whole narration, every method, every Side Hop story and
   audio segment, every flashcard deck and every simulation. scripts/build-search-index.mjs adds them
   to the Pagefind index after `astro build` and then deletes this file from dist/, so it is never
   served: the browser only ever loads the Pagefind chunks a query needs. */
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
import { lessonHop, allIdeas, runOf } from '../lib/hop';
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
    out.push({
      type: 'film',
      url: f.href,
      title: f.title,
      lead: f.lessonTitle && f.lessonTitle !== f.title ? f.lessonTitle : f.description,
      kicker: kindBadge(f),
      ...lessonBits(f.lesson),
      poster: f.poster,
      dur: Math.round(f.durationSec),
      filmKey: filmKey(f.src),
      parts: [
        ...(f.takeaways?.length ? [{ id: 'take-homes', h: 'Take-homes', text: f.takeaways.join(' '), w: 2 }] : []),
        ...runs,
      ],
    });
  }

  /* Ladders: one idea at every level it is taught, played on /films/ (?ladder=<id>). The same
     ladders as the films-page picker: an idea with films at two or more levels, each film on a
     level the idea has a rung at (filmLadders() in src/lib/film-ladders.ts keeps the same rule). */
  const catalog = await filmCatalog();
  const lessonFilms = new Map<string, typeof catalog>();
  for (const f of catalog) {
    if (!f.lesson || !f.href.startsWith('/watch/') || !['first', 'second', 'series'].includes(f.kind)) continue;
    if (!lessonFilms.has(f.lesson)) lessonFilms.set(f.lesson, []);
    lessonFilms.get(f.lesson)!.push(f);
  }
  for (const i of await allIdeas()) {
    if (!i.play) continue;
    const slugs: string[] = [];
    for (const f of runOf(i.films)) if (!slugs.includes(f.lesson)) slugs.push(f.lesson);
    const ranks = new Set(i.rungs.map((r) => r.rank));
    const films = slugs.flatMap((slug) => {
      const rank = i.films.find((f) => f.lesson === slug)?.rank;
      return (lessonFilms.get(slug) ?? []).map((f) => ({ f, rank }));
    });
    if (films.length < 2 || films.some((x) => x.rank == null || !ranks.has(x.rank))) continue;
    const levels = new Set(films.map((x) => x.rank)).size;
    out.push({
      type: 'ladder',
      url: `/films/?ladder=${encodeURIComponent(i.id)}`,
      title: i.name,
      lead: i.blurb,
      kicker: `Ladder · ${films.length} films · ${levels} levels`,
      courseTitle: i.areaName,
      courses: [...new Set(films.map((x) => x.f.course).filter((c): c is string => !!c))],
      poster: films[0].f.poster,
      dur: Math.round(films.reduce((t, x) => t + x.f.durationSec, 0)),
      films: films.length,
      parts: [
        ...(i.aliases?.length ? [{ text: `Also called ${i.aliases.join(', ')}.`, w: 3 }] : []),
        { id: 'films', h: 'Films on this ladder', text: films.map((x) => x.f.title).join(' · '), w: 2 },
        { id: 'lessons', h: 'Lessons on this ladder', text: i.rungs.map((r) => `${r.title} (${r.courseTitle})`).join(' · '), w: 2 },
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

  /* Side Hops: each story is its own record, and so is the audio segment's script. */
  for (const { default: d } of Object.values(HOPS)) {
    if (!live.has(d.slug)) continue;
    const bits = lessonBits(d.slug);
    d.hops.forEach((h, i) => {
      out.push({
        type: 'sidehop',
        url: `/lessons/${d.slug}/#sh-${i + 1}`,
        title: h.title,
        kicker: `Side Hop · ${KIND_LOOK[h.kind]?.label ?? 'Story'}`,
        ...bits,
        ...(h.image ? { poster: `/${h.image.file}` } : {}),
        parts: [{ text: h.text }, ...(h.image?.caption ? [{ text: h.image.caption, w: 2 }] : [])],
      });
    });
    if (d.audio?.transcript) {
      out.push({
        type: 'sidehop',
        url: `/lessons/${d.slug}/#sh-panel-h`,
        title: d.audio.title,
        kicker: 'Side Hops · Audio',
        ...bits,
        dur: Math.round(d.audio.durationSec),
        parts: d.audio.transcript.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean).map((text) => ({ text })),
      });
    }
  }

  /* Flashcards: one record per deck, every card's front, back and why. */
  for (const { default: deck } of Object.values(DECKS)) {
    if (!deck.cards?.length || !live.has(deck.slug)) continue;
    out.push({
      type: 'flashcards',
      url: `/lessons/${deck.slug}/#flashcards`,
      title: `Flashcards: ${live.get(deck.slug)!.title}`,
      kicker: `${deck.cards.length} flashcards`,
      ...lessonBits(deck.slug),
      parts: deck.cards.map((c) => ({ text: [clozeText(c.front), clozeText(c.back), c.why ?? ''].filter(Boolean).join(' — ') })),
    });
  }

  /* Simulations: the ones a lesson lists, by title and caption. */
  for (const l of lessons) {
    const d = l.data;
    (d.simulations ?? []).forEach((s: { type: string; title: string; caption?: string }) => {
      out.push({
        type: 'sim',
        url: `/lessons/${d.slug}/`,
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
