/* The front door's build-time data. Every number and every lesson name the homepage shows is
   counted or read here from the lessons, the catalog and the film library; nothing is typed.
   Draft lessons never reach the page: every read below filters `!data.draft`. */
import { existsSync } from 'node:fs';
import { getCollection, type CollectionEntry } from 'astro:content';
import { courseOf, unitsFor } from '../../data/courses';
import { STAGES, stageOf } from '../../data/stages';
import { courseCards } from '../../lib/catalog';
import { filmTotal } from '../../lib/film-catalog';
import { concept, conceptsOf, ladder, type LadderRung } from '../../lib/topic-graph';

type Lesson = CollectionEntry<'lessons'>;

export const fmt = (n: number) => n.toLocaleString('en-US');
const WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven'];
/** A small count as a word ("four levels"); larger ones stay digits. */
export const word = (n: number) => WORDS[n] ?? String(n);

/** One rung of an idea's ladder: a lesson, the level it is taught at, and what that level adds. */
export interface Rung {
  stage: string;
  stageTitle: string;
  href: string;
  title: string;
  /** What this level adds to the idea, from the hop graph. */
  note: string;
  /** Minutes of film in the lesson, all its chapters together, and how many chapters. */
  filmMin: number | null;
  filmParts: number;
}

/** Lowest level first, one rung per level (where a level has two lessons, the first stands for it). */
function byLevel(rungs: LadderRung[], lessons: Map<string, Lesson>): Rung[] {
  const seen = new Set<string>();
  return rungs
    .filter((r) => lessons.has(r.slug))
    .filter((r) => (seen.has(r.stage) ? false : (seen.add(r.stage), true)))
    .map((r) => {
      const d = lessons.get(r.slug)!.data;
      const secs = [d.explainer?.durationSec, ...(d.films ?? []).map((f) => f.durationSec)].filter((x): x is number => !!x);
      return {
        stage: r.stage,
        stageTitle: r.stageTitle,
        href: `/lessons/${r.slug}/`,
        title: r.title,
        note: r.adds ?? '',
        filmMin: secs.length ? Math.max(1, Math.round(secs.reduce((n, x) => n + x, 0) / 60)) : null,
        filmParts: secs.length,
      };
    });
}

/* The hand-checked activities the parents' door may show, one at a time. Each is done indoors in
   30 minutes or less with things from a kitchen or a grocery shop, and each guide was read for this
   list on 2026-11-20. `figure` is the guide's own set-up picture; its alt text is read from the guide. */
const HOME_ACTIVITIES = [
  { slug: 'thirsty-celery', figure: 'thirsty-celery-two-glasses.webp' },
  { slug: 'wake-up-a-seed', figure: 'wake-up-a-seed-two-bags.webp' },
  { slug: 'watershed-in-a-pan', figure: 'crumpled-paper-landscape.webp' },
];
const DAY = 24 * 60 * 60 * 1000;
const WEEK = 7 * DAY;
/* Day 0 of the clock was a Thursday; three days on puts the weekly change on a Monday (UTC), so the
   activity a parent shops for midweek is still the one on the page that weekend. */
const weekOf = (t: number) => Math.floor((t + 3 * DAY) / WEEK);
const SETTING: Record<string, string> = { indoors: 'indoors', outdoors: 'outdoors', either: 'indoors or out' };

export async function homeData(now = new Date()) {
  const { cards, lessonCount } = await courseCards();
  const sum = (k: 'sims' | 'questions') => cards.reduce((n, c) => n + c[k], 0);
  const liveLessons = await getCollection('lessons', ({ data }) => !data.draft);
  const live = new Map(liveLessons.map((l) => [l.data.slug, l]));

  /* The levels, each with its courses and the first lesson of its first course, in that course's
     unit order (the order its course page lists). */
  const firstLesson = (slug: string) => {
    const first = unitsFor(courseOf(slug), liveLessons.filter((l) => l.data.course === slug))[0]?.entries[0]?.l;
    return first ? { slug: first.data.slug, title: first.data.title } : null;
  };
  const rows = STAGES.map((s) => ({ ...s, cards: cards.filter((k) => stageOf(k.c) === s.key) }))
    .filter((s) => s.cards.length > 0)
    .map((b) => ({
      ...b,
      first: firstLesson(b.cards[0].c.slug),
      /* On a row with more than one course, each course's own first lesson (2026-11-23): a reader who
         came for the second course can see where it starts. A course with no live lesson is left out. */
      starts: b.cards.length > 1
        ? b.cards.map((k) => ({ course: k.c.title, first: firstLesson(k.c.slug) })).filter((x): x is { course: string; first: { slug: string; title: string } } => !!x.first)
        : [],
    }));
  const lessonsIn = (slug: string) => cards.find((k) => k.c.slug === slug)?.lessons ?? 0;

  /** One idea at every level it is taught, from the hop graph (src/data/topic-graph.json). */
  const ladderOf = async (id: string): Promise<{ name: string; rungs: Rung[] }> => {
    const c = concept(id);
    if (!c) throw new Error(`Homepage: the hop graph has no idea called "${id}".`);
    return { name: c.name, rungs: byLevel(await ladder(id), live) };
  };

  /**
   * Where an activity's idea is taught again, from the hop graph: the idea the activity is a core
   * lesson of, and that idea's lessons at later levels. Null when the graph has no later lesson
   * for it, and then the page says nothing about "later" for that activity.
   */
  const laterFrom = async (slug: string): Promise<{ name: string; rungs: Rung[] } | null> => {
    for (const c of (await conceptsOf(slug)).filter((x) => x.role === 'core')) {
      const all = await ladder(c.id);
      const here = all.find((r) => r.slug === slug);
      const later = byLevel(all.filter((r) => here && r.rank > here.rank && r.role === 'core'), live);
      if (later.length) return { name: c.name, rungs: later };
    }
    return null;
  };

  /* The parents' activity: one from the hand-checked list, changing once a week (the week of the day
     the site was last built). The build stops if a listed guide stops fitting the list's rule. */
  const week = weekOf(now.getTime());
  const pick = HOME_ACTIVITIES[week % HOME_ACTIVITIES.length];
  const before = HOME_ACTIVITIES[(week - 1 + HOME_ACTIVITIES.length) % HOME_ACTIVITIES.length];
  const checked = HOME_ACTIVITIES.map((h) => {
    const l = live.get(h.slug);
    const a = l?.data.activity;
    const body = l?.body ?? '';
    const src = `/figures/${h.slug}/${h.figure}`;
    const alt = body.match(new RegExp(`src="${src}"[^>]*?alt="AI-generated illustration: ([^"]+)"`))?.[1];
    const safety = body.indexOf('<SafetyNote');
    const steps = body.indexOf('## What to do');
    if (!l || !a) throw new Error(`Homepage: "${h.slug}" is not a published Biology Together activity.`);
    if (a.setting !== 'indoors' || a.minutes > 30) throw new Error(`Homepage: "${h.slug}" is no longer an indoor activity of 30 minutes or less.`);
    if (!alt || !existsSync(`public${src}`)) throw new Error(`Homepage: "${h.slug}" no longer has the AI-labelled figure ${src}.`);
    if (safety < 0 || steps < 0 || safety > steps) throw new Error(`Homepage: "${h.slug}" no longer has its safety notes before its steps, which the parents' door says it does.`);
    return {
      slug: h.slug,
      title: l.data.title,
      hook: l.data.hook ?? '',
      minutes: a.minutes,
      setting: SETTING[a.setting] ?? a.setting,
      followUp: a.followUp,
      adult: a.adult,
      /* "the printed observation sheet below" points down the guide's own page; from here it is "in the guide". */
      materials: a.materials.map((m) => ({ text: m.replace(/\s*\(optional\)\s*$/, '').replace(/observation sheet below$/, 'observation sheet in the guide'), optional: /\(optional\)\s*$/.test(m) })),
      figure: { src, alt: alt.charAt(0).toUpperCase() + alt.slice(1) },
      underReview: l.data.underReview.length > 0,
    };
  });
  const chosen = checked.find((x) => x.slug === pick.slug)!;
  const featured = { ...chosen, later: await laterFrom(chosen.slug), lastWeek: checked.find((x) => x.slug === before.slug)! };

  /* The Virginia standards each school course's lessons carry, as a range ("LS.1 to LS.11"). */
  const standards = (course: string, prefix: string) => {
    const nums = liveLessons
      .filter((l) => l.data.course === course)
      .flatMap((l) => [...(l.data.ladder?.sol ?? []), ...(l.data.ladder?.practices ?? [])])
      .map((c) => c.match(new RegExp(`^${prefix}\\.(\\d+)`))?.[1])
      .filter(Boolean)
      .map(Number);
    if (!nums.length) throw new Error(`Homepage: no ${prefix} standards found on the ${course} lessons.`);
    return `${prefix}.${Math.min(...nums)} to ${prefix}.${Math.max(...nums)}`;
  };

  return {
    cards,
    rows,
    lessonCount,
    courseCount: cards.length,
    films: await filmTotal(),
    sims: sum('sims'),
    questions: sum('questions'),
    lessonsIn,
    ladderOf,
    featured,
    standards: { lifeScience: standards('life-science', 'LS'), biology: standards('high-school-biology', 'BIO') },
    /** A lesson's first Virginia standard, for the teachers' one worked example. */
    standardOf: (slug: string) => live.get(slug)?.data.ladder?.sol[0] ?? null,
  };
}
export type HomeData = Awaited<ReturnType<typeof homeData>>;
