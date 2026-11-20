/* The front door's build-time data. Every number and every lesson name the homepage shows is
   counted or read here from the lessons, the catalog and the film library; nothing is typed.
   Draft lessons never reach the page: every read below filters `!data.draft`. */
import { existsSync } from 'node:fs';
import { getCollection, type CollectionEntry } from 'astro:content';
import { courseOf, unitsFor } from '../../data/courses';
import { STAGES, stageOf } from '../../data/stages';
import { courseCards } from '../../lib/catalog';
import { filmTotal } from '../../lib/film-catalog';
import rewritten from '../../data/recently-rewritten.json';

type Lesson = CollectionEntry<'lessons'>;

export const fmt = (n: number) => n.toLocaleString('en-US');
const WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven'];
/** A small count as a word ("four levels"); larger ones stay digits. */
export const word = (n: number) => WORDS[n] ?? String(n);

/** One rung of an idea's ladder: a lesson, the level it is taught at, and a line about it. */
export interface Rung {
  stage: string;
  stageTitle: string;
  href: string;
  title: string;
  /** The lesson's own opening question (its `hook`). */
  note: string;
  /** Minutes of the lesson's first film, when it has one. */
  filmMin: number | null;
}

const stageKey = (l: Lesson) => stageOf(courseOf(l.data.course));
const rank = (key: string) => STAGES.findIndex((s) => s.key === key);
function rung(l: Lesson): Rung {
  const key = stageKey(l);
  const sec = l.data.explainer?.durationSec;
  return {
    stage: key,
    stageTitle: STAGES.find((s) => s.key === key)?.title ?? '',
    href: `/lessons/${l.data.slug}/`,
    title: l.data.title,
    note: l.data.hook ?? '',
    filmMin: sec ? Math.max(1, Math.round(sec / 60)) : null,
  };
}
/** Lowest level first, one rung per level (where a level has two lessons, the first listed stands for it). */
function byLevel(lessons: Lesson[]): Rung[] {
  const seen = new Set<string>();
  return lessons
    .map(rung)
    .filter((r) => (seen.has(r.stage) ? false : (seen.add(r.stage), true)))
    .sort((a, b) => rank(a.stage) - rank(b.stage));
}

/* The hand-checked activities the parents' door may show, one at a time. Each is done indoors in
   30 minutes or less with things from a kitchen or a grocery shop, and each guide was read for this
   list on 2026-11-20. `figure` is the guide's own set-up picture; its alt text is read from the guide. */
const HOME_ACTIVITIES = [
  { slug: 'thirsty-celery', figure: 'thirsty-celery-two-glasses.webp' },
  { slug: 'wake-up-a-seed', figure: 'wake-up-a-seed-two-bags.webp' },
  { slug: 'watershed-in-a-pan', figure: 'crumpled-paper-landscape.webp' },
];
const WEEK = 7 * 24 * 60 * 60 * 1000;
const SETTING: Record<string, string> = { indoors: 'indoors', outdoors: 'outdoors', either: 'indoors or out' };

export async function homeData(now = new Date()) {
  const { cards, lessonCount } = await courseCards();
  const sum = (k: 'sims' | 'questions') => cards.reduce((n, c) => n + c[k], 0);
  const liveLessons = await getCollection('lessons', ({ data }) => !data.draft);
  const live = new Map(liveLessons.map((l) => [l.data.slug, l]));
  const get = (slugs: string[] = []) => slugs.map((s) => live.get(s)).filter((l): l is Lesson => !!l);

  /* The levels, each with its courses and the first lesson of its first course, in that course's
     unit order (the order its course page lists). */
  const firstLesson = (slug: string) => {
    const first = unitsFor(courseOf(slug), liveLessons.filter((l) => l.data.course === slug))[0]?.entries[0]?.l;
    return first ? { slug: first.data.slug, title: first.data.title } : null;
  };
  const rows = STAGES.map((s) => ({ ...s, cards: cards.filter((k) => stageOf(k.c) === s.key) }))
    .filter((s) => s.cards.length > 0)
    .map((b) => ({ ...b, first: firstLesson(b.cards[0].c.slug) }));
  const lessonsIn = (slug: string) => cards.find((k) => k.c.slug === slug)?.lessons ?? 0;

  /**
   * One idea at every level it is taught, starting from a grade 7 lesson. Today the rungs are the
   * links authored in the lessons' own frontmatter (`ladder.biology`, `ladder.college`), the only
   * ladder data on main. When the hop graph is merged, this function is the one place to switch:
   * return the concept's rungs from the graph in the same `Rung` shape and the page follows.
   */
  const ladderFrom = (slug: string): Rung[] => {
    const start = live.get(slug);
    if (!start) return [];
    return byLevel([start, ...get(start.data.ladder?.biology), ...get(start.data.ladder?.college)]);
  };

  /** A Biology Together activity, then the grade 7 and high school lessons its own guide points up to. */
  const ladderFromActivity = (l: Lesson): Rung[] => {
    const up = get(l.data.activity?.stepUp).find((g) => get(g.data.ladder?.biology).length > 0);
    return up ? byLevel([l, up, get(up.data.ladder?.biology)[0]]) : [];
  };

  /* The parents' activity: one from the hand-checked list, changing once a week (the week of the day
     the site was last built). The build stops if a listed guide stops fitting the list's rule. */
  const pick = HOME_ACTIVITIES[Math.floor(now.getTime() / WEEK) % HOME_ACTIVITIES.length];
  const featured = HOME_ACTIVITIES.map((h) => {
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
      ladder: ladderFromActivity(l),
    };
  }).find((x) => x.slug === pick.slug)!;

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
    /* Lessons whose text was rewritten (an entry that lists only a new film is not a rewrite). */
    rewrittenCount: (rewritten as { slug: string; new?: string[] }[]).filter((r) => live.has(r.slug) && (!r.new?.length || r.new.includes('text'))).length,
    lessonsIn,
    ladderFrom,
    featured,
    standards: { lifeScience: standards('life-science', 'LS'), biology: standards('high-school-biology', 'BIO') },
  };
}
export type HomeData = Awaited<ReturnType<typeof homeData>>;
