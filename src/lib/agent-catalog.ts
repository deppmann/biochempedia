/* The site's catalog in a form AI agents can read: courses, units and lessons, with a one-line
   summary and two links per lesson (the page, and its plain Markdown copy, /lessons/<slug>.md,
   written after the build by scripts/agent-markdown.mjs). Feeds /catalog.json and /llms.txt. */
import { getCollection } from 'astro:content';
import { COURSES, unitsFor, courseHref } from '../data/courses';
import { lessonMinutes } from './reading-time';
import REWRITTEN from '../data/recently-rewritten.json';
import LINKS from '../data/lesson-links.json';

export const SITE = 'https://biochemistrypedia.com';

const TIER_LEVEL: Record<string, string> = {
  families: 'ages 5–10, with a parent or teacher',
  highschool: 'grades 7–12',
  foundation: 'first- and second-year university',
  core: 'core university (third year)',
  elective: 'university elective',
  advanced: 'advanced university and graduate',
};

const rewritten = new Map((REWRITTEN as { slug: string; date: string }[]).map((r) => [r.slug, r.date]));
/** "Before this" and "After this" from src/data/lesson-links.json (drafted offline by a model, then checked). */
const links = LINKS.lessons as Record<string, { before: { slug: string }[]; after: { slug: string }[] }>;

export interface AgentLesson {
  slug: string; title: string; summary: string; url: string; markdown: string;
  minutes?: number; objectives: string[]; rewritten?: string;
  /** Lessons to review first and to study next, by slug. */
  reviewFirst?: string[]; studyNext?: string[];
}
export interface AgentCourse {
  slug: string; title: string; tagline: string; tier: string; level: string; mcat: boolean; url: string;
  units: { name: string; lessons: AgentLesson[] }[];
}

export async function agentCatalog(): Promise<AgentCourse[]> {
  const all = (await getCollection('lessons')).filter((l) => !l.data.draft);
  const live = new Set(all.map((l) => l.data.slug));
  const slugs = (xs?: { slug: string }[]) => { const out = (xs ?? []).map((x) => x.slug).filter((s) => live.has(s)); return out.length ? out : undefined; };
  return COURSES.map((c) => {
    const mine = all.filter((l) => l.data.course === c.slug);
    return {
      slug: c.slug, title: c.title, tagline: c.tagline, tier: c.tier, level: TIER_LEVEL[c.tier] ?? c.tier,
      mcat: !!c.mcat, url: SITE + courseHref(c.slug),
      units: unitsFor(c, mine).map((u) => ({
        name: u.name,
        lessons: u.entries.map(({ l }) => ({
          slug: l.data.slug,
          title: l.data.title,
          summary: l.data.summary,
          url: `${SITE}/lessons/${l.data.slug}/`,
          markdown: `${SITE}/lessons/${l.data.slug}.md`,
          minutes: lessonMinutes(l)?.core,
          objectives: l.data.objectives ?? [],
          rewritten: rewritten.get(l.data.slug),
          reviewFirst: slugs(links[l.data.slug]?.before),
          studyNext: slugs(links[l.data.slug]?.after),
        })),
      })),
    };
  }).filter((c) => c.units.length > 0);
}
