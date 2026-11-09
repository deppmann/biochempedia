/* The site's catalog in a form AI agents can read: courses, units and lessons, with a one-line
   summary and two links per lesson (the page, and its plain Markdown copy, /lessons/<slug>.md,
   written after the build by scripts/agent-markdown.mjs). Feeds /catalog.json and /llms.txt. */
import { getCollection } from 'astro:content';
import { COURSES, unitsFor, courseHref } from '../data/courses';
import { lessonMinutes } from './reading-time';
import REWRITTEN from '../data/recently-rewritten.json';

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

export interface AgentLesson {
  slug: string; title: string; summary: string; url: string; markdown: string;
  minutes?: number; objectives: string[]; rewritten?: string;
}
export interface AgentCourse {
  slug: string; title: string; tagline: string; tier: string; level: string; mcat: boolean; url: string;
  units: { name: string; lessons: AgentLesson[] }[];
}

export async function agentCatalog(): Promise<AgentCourse[]> {
  const all = (await getCollection('lessons')).filter((l) => !l.data.draft);
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
        })),
      })),
    };
  }).filter((c) => c.units.length > 0);
}
