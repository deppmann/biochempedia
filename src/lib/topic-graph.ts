/* The hop graph at build time.

   src/data/topic-graph.json says which IDEAS the site teaches and where. A concept ("osmosis") has
   a ladder: the lessons that teach it, lowest level first, each with a short note on what that
   level adds. It also lists lessons that lean on the idea, the films that show it, and sideways
   hops to neighbouring ideas. The file is written offline (scripts/topic-graph) and checked in CI
   (scripts/check-topic-graph.mjs); no model runs when someone visits.

   The file holds only ids and reader-facing notes. Titles, courses, levels and film details are
   joined here from the content collection, src/data/courses.ts, src/data/stages.ts and the film
   catalog, so the graph cannot drift from the lessons. The logic lives in topic-graph-core.mjs,
   which the offline tools and tests share.

   Rules for every consumer:
   - Concepts are optional. A lesson with no record gives [] from conceptsOf() and hops(); the
     page must be whole without them.
   - A gap is real. "No simpler version yet" and a ladder with a missing level are honest states;
     `jump`, `stepFromBelow` and ladderByLevel(id, true) exist so a design can say so.
   - `uses` rungs are "also comes up in": never draw them on a ladder (usedBy() returns them).
   - Never show an anchor's heading text as the name of a rung; show the note.

   Use, in an .astro frontmatter or an endpoint:
     import { hops, ladder, conceptsOf } from '../lib/topic-graph';
     const here = await hops(slug);            // per idea the lesson teaches: down, up, sideways
     const rungs = await ladder('osmosis');    // the whole ladder, joined */
import { getCollection } from 'astro:content';
import { COURSES } from '../data/courses';
import { STAGES, stageOf } from '../data/stages';
import { filmCatalog, filmKey } from './film-catalog';
import { makeTopicGraph, headingIds, searchConcepts as rank } from './topic-graph-core.mjs';
import raw from '../data/topic-graph.json';

// ------------------------------------------------------------------ the file's own shape

export type Role = 'core' | 'uses';

export interface Rung {
  lesson: string;
  role: Role;
  /** Core rungs: id of the `##` section that teaches the idea, when one section clearly does. */
  anchor?: string;
  /** Core rungs: what this level adds, in words for that level's reader (at most 14 words). */
  adds?: string;
}
export interface NearEdge {
  id: string;
  /** One sentence, written from the side of the reader who is on the first idea. */
  why: string;
}
export interface Concept {
  name: string;
  /** A display name of at most 26 characters, present when `name` is longer than 24. Show `short ?? name`. */
  short?: string;
  /** One plain sentence, readable at grade 7. */
  blurb: string;
  area: string;
  subject: string;
  /** Everyday phrases and school terms a person might type; each was checked to be this idea. */
  aliases: string[];
  rungs: Rung[];
  /** Film keys: the path under /explainers/ without ".mp4". */
  films: string[];
  near: NearEdge[];
}
export interface Area {
  id: string;
  name: string;
}
export interface TopicGraph {
  version: number;
  updated: string;
  about: string;
  areas: Area[];
  concepts: Record<string, Concept>;
  /** Reverse index: the concepts a lesson is on, MAIN IDEA FIRST (then its other core ideas, then
   *  the ideas it only uses), and the hash of the teaching text
   *  the record was written from. A live lesson may be absent. */
  lessons: Record<string, { hash: string; concepts: string[] }>;
}
export type ConceptWithId = Concept & { id: string };

// ------------------------------------------------------------------ the joined shapes

export interface LessonInfo {
  slug: string;
  title: string;
  course: string;
  courseTitle: string;
  /** Stage key from src/data/stages.ts. */
  stage: string;
  stageTitle: string;
  /** 0 (ages 5 to 10) … 6 (graduate). */
  rank: number;
  /** Position in its course. */
  order: number;
  hook: string;
}
export interface JoinedFilm {
  key: string;
  title: string;
  lesson: string;
  lessonTitle: string;
  course: string;
  stage: string;
  stageTitle: string;
  rank: number;
  /** Film id within the lesson; null for the lesson's first film. */
  id: string | null;
  /** The film's own page (/watch/…). */
  href: string;
  poster: string;
  durationSec: number;
  /** 'activity' for an ages 5 to 10 film, which shows the grown-up how to run the activity. */
  kind: string;
}
export interface JoinedRung extends LessonInfo {
  lesson: string;
  role: Role;
  anchor?: string;
  adds?: string;
  /** The lesson page, at the section that teaches the idea when the anchor still exists. */
  href: string;
  /** The concept's films that belong to this lesson. */
  films: JoinedFilm[];
}
export interface LadderRung extends JoinedRung {
  /** Levels between this rung and the nearest lower one: 1 = the next level up, 3 = two levels
   *  have no lesson in between. null on the lowest level. */
  stepFromBelow: number | null;
  /** The same, looking up. null on the highest level. */
  stepToAbove: number | null;
}
export interface HopRung extends LadderRung {
  /** Levels moved from the reader's lesson: 1 = next door. For a sideways target it may be 0 or negative. */
  jump: number;
}
export interface LevelRow {
  stage: string;
  stageTitle: string;
  rank: number;
  rungs: LadderRung[];
  /** True for an empty level that lies between two levels that have a lesson. */
  gap: boolean;
}
export interface LessonConcept {
  id: string;
  name: string;
  /** `short ?? name`: what to show where space is tight. */
  label: string;
  area: string;
  role: Role;
  anchor?: string;
  adds?: string;
}
export interface Hop {
  id: string;
  name: string;
  label: string;
  area: string;
  anchor?: string;
  adds?: string;
  /** The first lesson on this idea at the nearest lower level; absent when there is no simpler version yet. */
  down?: HopRung;
  downAll: HopRung[];
  /** The first lesson at the nearest higher level; absent at the top of the ladder. */
  up?: HopRung;
  upAll: HopRung[];
  /** Other lessons on this idea at the reader's own level. */
  beside: LadderRung[];
  /** Neighbouring ideas, each with the reason and the lesson on it nearest the reader's level. */
  sideways: { id: string; name: string; label: string; blurb: string; area: string; why: string; to?: HopRung }[];
}
export interface SearchRow {
  id: string;
  name: string;
  label: string;
  blurb: string;
  area: string;
  areaName: string;
  /** Folded for matching: the name, then each alias. */
  terms: string[];
  aliases: string[];
  /** Stage keys that have a core lesson, lowest first. */
  levels: string[];
  films: number;
}
/** /graph/all.json and /graph/<area>.json: see clientGraph() in topic-graph-core.mjs for the key to each column. */
export interface ClientGraph {
  v: number;
  updated: string;
  stages: [key: string, title: string][];
  areas: [id: string, name: string][];
  courses: [slug: string, title: string, stage: number][];
  lessons: [slug: string, title: string, course: number][];
  films: [key: string, title: string, lesson: number, seconds: number, id: string | 0][];
  concepts: {
    id: string;
    n: string;
    h?: string;
    b: string;
    a: number;
    s?: string;
    q: string[];
    r: ([lesson: number, role: 0, adds: string, anchor?: string] | [lesson: number, role: 1])[];
    f: number[];
    x: [concept: number | string, why: string][];
  }[];
}

/** /graph.json: the small index. See clientIndex() in topic-graph-core.mjs. */
export interface ClientIndex {
  v: number;
  updated: string;
  /** Live lessons that have a record so far, and how many live lessons there are. */
  covered: number;
  live: number;
  files: { area: string; all: string };
  stages: [key: string, title: string][];
  areas: [id: string, name: string, concepts: number][];
  concepts: { id: string; n: string; h?: string; a: number; l: number; b: string; q: string[]; f: number }[];
  lessons: Record<string, number[]>;
}

interface Api {
  concepts: ConceptWithId[];
  concept(id: string): ConceptWithId | undefined;
  conceptsOf(slug: string): LessonConcept[];
  ladder(id: string): LadderRung[];
  usedBy(id: string): JoinedRung[];
  ladderByLevel(id: string, withGaps?: boolean): LevelRow[];
  span(id: string): { levels: string[]; lowest: string | null; highest: string | null; gaps: string[] };
  hops(slug: string): Hop[];
  filmsFor(id: string): JoinedFilm[];
  searchIndex(): SearchRow[];
  clientGraph(only?: string[]): ClientGraph;
  clientIndex(): ClientIndex;
}

// ------------------------------------------------------------------ data that needs no join

export const graph = raw as TopicGraph;
export const areas: Area[] = graph.areas;
export const areaName = (id: string): string => areas.find((a) => a.id === id)?.name ?? id;
/** Every concept with its id, in the file's order (by area, then id). */
export const concepts: ConceptWithId[] = Object.entries(graph.concepts).map(([id, c]) => ({ id, ...c }));
export const concept = (id: string): ConceptWithId | undefined => (graph.concepts[id] ? { id, ...graph.concepts[id] } : undefined);
/** True when the lesson has a record. A lesson without one is normal. */
export const hasRecord = (slug: string): boolean => !!graph.lessons[slug];

/** Level keys in ladder order: ages-5-10 … graduate. */
export const STAGE_KEYS: string[] = STAGES.map((s) => s.key);
export const stageRank = (key: string): number => STAGE_KEYS.indexOf(key);
export const stageTitle = (key: string): string => STAGES.find((s) => s.key === key)?.title ?? key;

// ------------------------------------------------------------------ joins made at build time

let apiCache: Promise<Api> | undefined;
function api(): Promise<Api> {
  apiCache ??= (async () => {
    const byCourse = new Map(COURSES.map((c) => [c.slug, c]));
    const entries = await getCollection('lessons', ({ data }) => !data.draft);
    const lessons = new Map<string, LessonInfo & { headingIds?: Set<string> }>();
    // Position in the course, as the course page counts it.
    const order = new Map<string, number>();
    for (const c of COURSES) {
      entries.filter((l) => l.data.course === c.slug)
        .sort((a, b) => (a.data.order ?? 999) - (b.data.order ?? 999) || a.data.slug.localeCompare(b.data.slug))
        .forEach((l, i) => order.set(l.data.slug, i + 1));
    }
    for (const l of entries) {
      const d = l.data;
      const c = byCourse.get(d.course);
      if (!c) continue;
      const stage = stageOf(c);
      // Section ids as the page will have them, so a rung whose heading was reworded falls back
      // to the top of the lesson instead of pointing at nothing.
      const ids = l.body ? new Set(headingIds(l.body).filter((h) => h.depth === 2).map((h) => h.id)) : undefined;
      lessons.set(d.slug, {
        slug: d.slug, title: d.title, course: c.slug, courseTitle: c.title, stage, stageTitle: stageTitle(stage), rank: stageRank(stage),
        order: order.get(d.slug) ?? 0, hook: d.hook ?? '', ...(ids ? { headingIds: ids } : {}),
      });
    }
    const films = new Map(
      (await filmCatalog())
        .filter((f) => f.lesson && (f.kind === 'first' || f.kind === 'second' || f.kind === 'series' || f.kind === 'activity'))
        .map((f) => [filmKey(f.src), { key: filmKey(f.src), title: f.title, lesson: f.lesson!, id: f.id.split(':')[2] ?? null, durationSec: f.durationSec, href: f.href, poster: f.poster, kind: f.kind }]),
    );
    const courses = COURSES.map((c) => ({ slug: c.slug, title: c.title, stage: stageOf(c) }));
    return makeTopicGraph(graph, { stages: STAGES.map((s) => ({ key: s.key, title: s.title })), lessons, films, courses }) as unknown as Api;
  })();
  return apiCache;
}

/** The display name of a concept: its short name when it has one. */
export const labelOf = (id: string): string => graph.concepts[id]?.short ?? graph.concepts[id]?.name ?? id;

/** The concepts a lesson is on, with its role in each: the lesson's main idea first, then its other core ideas, then what it uses. [] for a lesson with no record. */
export const conceptsOf = async (slug: string): Promise<LessonConcept[]> => (await api()).conceptsOf(slug);

/** A concept's ladder: its core rungs, lowest level first, with titles, courses, levels, the
 *  concept's films from each lesson and the size of each step. */
export const ladder = async (id: string): Promise<LadderRung[]> => (await api()).ladder(id);

/** Lessons that lean on the idea without teaching it ("also comes up in"), lowest level first. */
export const usedBy = async (id: string): Promise<JoinedRung[]> => (await api()).usedBy(id);

/** The ladder as one row per level; with `withGaps`, empty levels are included so a hole can be drawn. */
export const ladderByLevel = async (id: string, withGaps = false): Promise<LevelRow[]> => (await api()).ladderByLevel(id, withGaps);

/** Where a concept's ladder starts and stops, and the levels missing in between. */
export const span = async (id: string) => (await api()).span(id);

/** From one lesson, for each idea it teaches: one level down, one level up and sideways. */
export const hops = async (slug: string): Promise<Hop[]> => (await api()).hops(slug);

/** A concept's films joined with the catalog, lowest level first. */
export const filmsFor = async (id: string): Promise<JoinedFilm[]> => (await api()).filmsFor(id);

/** One row per concept for search over names and everyday phrases. */
export const searchIndex = async (): Promise<SearchRow[]> => (await api()).searchIndex();

/** Concept ids for a typed query, best first (folds case, accents and British or American spelling). */
export const searchConcepts = async (query: string, limit = 8): Promise<string[]> => rank(await searchIndex(), query, limit);

/** The compact graph for browsers: everything (/graph/all.json), or only the concepts named. */
export const clientGraph = async (only?: string[]): Promise<ClientGraph> => (await api()).clientGraph(only);

/** One area's share of the graph (/graph/<area>.json). */
export const clientArea = async (area: string): Promise<ClientGraph> => (await api()).clientGraph(concepts.filter((c) => c.area === area).map((c) => c.id));

/** The small index /graph.json serves: every idea's name, phrases and levels, and where the rest is. */
export const clientIndex = async (): Promise<ClientIndex> => (await api()).clientIndex();
