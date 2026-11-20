/* =============================================================================
   What the calendar pages are built from. Runs when the site is built, never in
   the browser, and calls no model. Everything is read from what the site already
   knows: the course order (courses.ts), each lesson's own frontmatter, the
   Biology Together activity blocks and safety notes, the MCAT path (paths.ts)
   and the passage sets. Nothing here is about a visitor.
   ============================================================================ */
import { getCollection } from 'astro:content';
import { COURSES, unitsFor } from '../../data/courses';
import { STAGES, stageOf } from '../../data/stages';
import { PATHS, MCAT_SCOPE_NOTE } from '../../data/paths';
import { SETS, DIAGNOSTIC_LENGTH } from '../mcat';
import { lessonMinutes } from '../reading-time';
import { watchHref } from '../films';
import type { Activity, CourseData, Lesson, McatData } from './engine';

type Entry = Awaited<ReturnType<typeof getCollection<'lessons'>>>[number];

let cache: Promise<Entry[]> | undefined;
const published = () => (cache ??= getCollection('lessons', ({ data }) => !data.draft));

/**
 * The calendar's one use of the site's lesson-time recipe. Minutes to read (or the class
 * period, for a school lesson) come from src/lib/reading-time.ts; film time is the sum of the
 * lesson's film lengths. If the site's minutes recipe changes, change it here and nowhere else
 * in the calendar.
 */
export function calendarMinutes(l: Entry): { read: number; filmSec: number; films: number } {
  const films = [...(l.data.explainer ? [l.data.explainer] : []), ...l.data.films];
  return {
    read: lessonMinutes(l)?.core ?? l.data.estMinutes ?? 20,
    filmSec: Math.round(films.reduce((a, f) => a + (f.durationSec ?? 0), 0)),
    films: films.length,
  };
}

const one = (s: string) => s.replace(/\s+/g, ' ').trim();
const firstSentence = (s: string) => one(s).split(/(?<=[.?!])\s+/)[0];

/** The guide's safety notes, each bullet word for word (line breaks inside a bullet closed up). */
function safetyOf(body: string | undefined): string[] {
  const m = body?.match(/<SafetyNote[^>]*>([\s\S]*?)<\/SafetyNote>/);
  if (!m) return [];
  return m[1].trim().split(/\n(?=- )/).map((s) => one(s.replace(/^\s*-\s*/, ''))).filter(Boolean);
}

export async function activities(): Promise<Activity[]> {
  const all = await published();
  const bt = COURSES.find((c) => c.slug === 'biology-together')!;
  const out: Activity[] = [];
  unitsFor(bt, all.filter((l) => l.data.course === bt.slug)).forEach((unit, u) => {
    for (const { l } of unit.entries) {
      const d = l.data;
      const a = d.activity;
      if (!a) continue;
      const safety = safetyOf(l.body);
      if (!safety.length) throw new Error(`calendar: no safety notes found in the guide "${d.slug}". The calendar shows them word for word and will not ship a guide without them.`);
      out.push({
        s: d.slug, t: d.title, hook: one(d.hook ?? firstSentence(d.summary)), unit: unit.name, u,
        min: a.minutes, follow: a.followUp, setting: a.setting, adult: a.adult, materials: a.materials, safety,
        poster: d.explainer?.poster,
        film: d.explainer ? { sec: Math.round(d.explainer.durationSec), href: watchHref(d.slug) } : undefined,
      });
    }
  });
  return out;
}

const LEVEL_WORDS: Record<string, string> = { 'grade-7': 'grade 7', 'high-school': 'high school' };

/** Every course a learner or a class can follow, in the site's order, with its lessons in order. */
export async function courses(): Promise<CourseData[]> {
  const all = await published();
  const bySlug = new Map(all.map((l) => [l.data.slug, l]));
  const stageKey = (slug: string) => { const c = COURSES.find((x) => x.slug === slug); return c ? stageOf(c) : ''; };

  /* An authored lower rung. A high school lesson names its grade 7 lessons (ladder.grade7).
     A college lesson is named by the school lessons that point up to it (ladder.college);
     the high school one is preferred, as the nearer rung. Nothing is inferred. */
  const downOf = new Map<string, { s: string; t: string; level: string }>();
  for (const l of all) {
    const key = stageKey(l.data.course);
    for (const up of l.data.ladder?.college ?? []) {
      const had = downOf.get(up);
      if (!LEVEL_WORDS[key] || (had && had.level === 'high school')) continue;
      downOf.set(up, { s: l.data.slug, t: l.data.title, level: LEVEL_WORDS[key] });
    }
  }
  for (const l of all) {
    const g7 = (l.data.ladder?.grade7 ?? []).map((s) => bySlug.get(s)).find(Boolean);
    if (g7) downOf.set(l.data.slug, { s: g7.data.slug, t: g7.data.title, level: 'grade 7' });
  }

  const out: CourseData[] = [];
  for (const course of COURSES) {
    const mine = all.filter((l) => l.data.course === course.slug);
    if (!mine.length) continue;
    const units = unitsFor(course, mine);
    const lessons: Lesson[] = [];
    units.forEach((unit, u) => {
      for (const { l, n } of unit.entries) {
        const d = l.data;
        const min = calendarMinutes(l);
        const sol = (d.ladder?.sol ?? d.activity?.sol ?? []).join(', ');
        lessons.push({
          s: d.slug, t: d.title, u, n, m: min.read, fs: min.filmSec, fc: min.films,
          ...(min.films ? { watch: watchHref(d.slug) } : {}),
          ...(d.hook || d.ladder?.essentialQuestion ? { hook: one(d.hook ?? d.ladder!.essentialQuestion) } : {}),
          ...(sol ? { sol } : {}),
          ...(downOf.has(d.slug) && course.tier !== 'families' ? { down: downOf.get(d.slug) } : {}),
        });
      }
    });
    const stage = stageOf(course);
    /* One level up, for school courses only: grade 7 to high school, high school to the first college course. */
    const nextStage = stage === 'grade-7' ? 'high-school' : stage === 'high-school' ? 'starting-college' : '';
    const upCourse = nextStage ? COURSES.find((c) => stageOf(c) === nextStage && all.some((l) => l.data.course === c.slug)) : undefined;
    out.push({
      ...(upCourse ? { up: { s: upCourse.slug, t: upCourse.title } } : {}),
      s: course.slug, t: course.title, level: STAGES.find((s) => s.key === stage)?.title ?? '',
      school: course.tier === 'highschool' || course.tier === 'families', units: units.map((u) => u.name), lessons,
    });
  }
  return out;
}

/** Courses a learner can follow. The activity guides are a grown-up's, so they are not here. */
export const learnerCourses = async () => (await courses()).filter((c) => c.s !== 'biology-together');

/** Courses the class-plan sample offers. Biology Together is left out: its guides are hands-on
 *  activities whose safety notes must travel with them, and a dated list of titles would not carry them. */
export const teacherCourses = learnerCourses;

export async function mcat(): Promise<McatData> {
  const all = await courses();
  const path = PATHS.find((p) => p.id === 'mcat')!;
  return {
    steps: path.steps
      .map((st) => ({ st, c: all.find((c) => c.s === st.course) }))
      .filter((x): x is { st: typeof x.st; c: CourseData } => !!x.c)
      .map(({ st, c }) => ({ s: c.s, t: c.t, why: st.why, optional: !!st.optional, lessons: c.lessons.map(({ down: _down, hook: _hook, sol: _sol, ...l }) => l) })),
    sets: SETS.map((s) => ({ id: s.id, title: s.title, lessons: [...new Set(s.lessons.map((x) => x.slug))] })),
    scope: MCAT_SCOPE_NOTE,
    links: path.notes?.flatMap((n) => n.links ?? []) ?? [],
    diagnostic: DIAGNOSTIC_LENGTH,
  };
}

/** Lesson slug -> course slug, for "the course you were last in". */
export async function lessonCourse(): Promise<Record<string, string>> {
  const out: Record<string, string> = {};
  for (const c of await learnerCourses()) for (const l of c.lessons) out[l.s] = c.s;
  return out;
}
