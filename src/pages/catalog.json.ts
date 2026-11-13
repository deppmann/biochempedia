/* /catalog.json: every course, unit and lesson, for AI agents and other programs. See src/lib/agent-catalog.ts. */
import type { APIRoute } from 'astro';
import { agentCatalog, SITE } from '../lib/agent-catalog';

export const GET: APIRoute = async () => {
  const courses = await agentCatalog();
  const body = {
    name: 'Biochemistrypedia',
    url: SITE,
    description: 'Free science lessons, films and simulations, starting with biology: ages 5 to graduate school.',
    llms: `${SITE}/llms.txt`,
    lessonMarkdown: `${SITE}/lessons/{slug}.md`,
    films: `${SITE}/films.json`,
    // Lesson text, the site's own figures and its films. The licence page lists what is not covered.
    license: 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
    licenseName: 'CC BY-NC-SA 4.0',
    licenseDetails: `${SITE}/license/`,
    attribution: 'Biochemistrypedia, Chris Deppmann, biochemistrypedia.com',
    generated: new Date().toISOString().slice(0, 10),
    courses,
  };
  return new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
