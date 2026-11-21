/* /catalog.json: every course, unit and lesson, for AI agents and other programs. See src/lib/agent-catalog.ts. */
import type { APIRoute } from 'astro';
import { agentCatalog, SITE } from '../lib/agent-catalog';
import { PRIMARY_HOST } from '../lib/site-host.mjs';

export const GET: APIRoute = async () => {
  const courses = await agentCatalog();
  const body = {
    name: 'STEMhop',
    url: SITE,
    description: 'Free science lessons, films and simulations, starting with biology: ages 5 to graduate school.',
    llms: `${SITE}/llms.txt`,
    lessonMarkdown: `${SITE}/lessons/{slug}.md`,
    films: `${SITE}/films.json`,
    filmsInOrder: `${SITE}/films/play/{course}/`,
    // The hop graph: which ideas the site teaches and the lessons on each at every level (src/pages/graph.json.ts).
    ideas: `${SITE}/graph.json`,
    ideaLadders: `${SITE}/graph/all.json`,
    // For people: search the ideas, and one page per idea at ideaPage with {id} from ideas (src/pages/ideas/).
    ideaSearch: `${SITE}/ideas/`,
    ideaPage: `${SITE}/ideas/{id}/`,
    // Lesson titles, levels, Virginia standards codes and unit names, one row per lesson (src/pages/ideas/lessons.json.ts).
    ideaLessons: `${SITE}/ideas/lessons.json`,
    // Lesson text, the site's own figures and its films. The licence page lists what is not covered.
    license: 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    licenseName: 'CC BY-NC-SA 4.0',
    licenseDetails: `${SITE}/license/`,
    attribution: `STEMhop, Chris Deppmann, ${PRIMARY_HOST}`,
    generated: new Date().toISOString().slice(0, 10),
    courses,
  };
  return new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
