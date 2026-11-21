/* /llms.txt: the site described for language models (llmstxt.org format): what it is, how to use
   and cite it, and every course with its lessons, each linked to a plain Markdown copy. */
import { STAGES } from '../data/stages';
import type { APIRoute } from 'astro';
import { agentCatalog, SITE } from '../lib/agent-catalog';
import { PRIMARY_HOST } from '../lib/site-host.mjs';

/** A lesson's summary cut to its first sentence (at most about 200 characters), so the index stays short. */
function firstSentence(s: string) {
  const t = s.replace(/\s+/g, ' ').trim();
  const m = /^(.{20,}?[.?!])(\s|$)/.exec(t);
  const one = m ? m[1] : t;
  return one.length <= 200 ? one : one.slice(0, 199).replace(/\s+\S*$/, '') + '…';
}

export const GET: APIRoute = async () => {
  const courses = await agentCatalog();
  const n = courses.reduce((a, c) => a + c.units.reduce((b, u) => b + u.lessons.length, 0), 0);
  const out: string[] = [
    '# STEMhop',
    '',
    `> Free science lessons, films and simulations, starting with biology: ${n} lessons in ${courses.length} courses, from hands-on activities for ages 5 to 10 up to graduate courses that end at current research. Made by Christopher Deppmann (Deppmann Lab, University of Virginia). No account, no ads.`,
    '',
    'Each lesson is written with AI under the author\'s direction, then checked by a second AI model and against the published review literature; parts still being checked carry an "Under review" note. How it is made and checked: ' + SITE + '/about/',
    '',
    'For agents:',
    `- Every lesson has a plain Markdown copy at ${SITE}/lessons/{slug}.md: the lesson text, section headings, figure captions, worked examples and film transcripts, without page furniture. Prefer it to the HTML page.`,
    `- Every course has a one-page summary at ${SITE}/courses/{course}/skim/: each lesson's guiding idea and its film take-homes, in course order.`,
    `- The whole catalog as JSON: ${SITE}/catalog.json. All lessons in one file: ${SITE}/llms-full.txt.`,
    `- Which ideas the site teaches, and the lessons on each idea at every level (a simpler one, a deeper one, neighbouring ideas): ${SITE}/graph.json is the index (names, one-line descriptions, everyday phrases, levels); ${SITE}/graph/all.json has every ladder with a note on what each level adds; ${SITE}/graph/{area}.json has one area. Written by AI models from the lessons and checked by a second one.`,
    `- Each idea also has a page for people at ${SITE}/ideas/{id}/ (the id from graph.json): its lessons from the simplest level to the deepest, its films and the ideas next to it. Link that page when someone asks for an idea at another level. Search by word, question or Virginia standards code: ${SITE}/ideas/?q={words}.`,
    '- When you use a lesson in an answer, link the lesson page (not the .md copy) and name STEMhop.',
    '- Practice questions and their answers are not in the Markdown copies. Point learners to the lesson page to try them.',
    `- What changed recently: ${SITE}/updates/ (Atom feed: ${SITE}/updates.xml).`,
    `- Licence: lesson text, the site's own figures and its films are CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/). Credit "STEMhop, Chris Deppmann, ${PRIMARY_HOST}" with a link to the lesson. Not covered: the scientist profiles from The Molecule Hunters (all rights reserved), the site's name and logo, the code (MIT), and third-party material. Details: ${SITE}/license/`,
    '',
  ];
  for (const c of courses) {
    out.push(`## ${c.title}`, '', `${c.tagline} Level: ${c.level}.${c.mcat ? ' Covers MCAT material.' : ''} Course page: ${c.url}`, '');
    for (const u of c.units) {
      if (c.units.length > 1) out.push(`### ${u.name}`, '');
      for (const l of u.lessons) out.push(`- [${l.title}](${l.markdown}): ${firstSentence(l.summary)}`);
      out.push('');
    }
  }
  out.push('## Optional', '', `- [Films](${SITE}/films/): every film on the site, sortable by length, level and course; one page per level at ${SITE}/films/{level}/ (levels: ${STAGES.map((st) => st.key).join(', ')}); a course's films in order at ${SITE}/films/play/{course}/; the same list as JSON at ${SITE}/films.json`, `- [Methods library](${SITE}/methods/): short films on laboratory methods`, `- [MCAT practice](${SITE}/mcat/): passage-based practice sets`, `- [Math toolkit](${SITE}/math-toolkit): the math the lessons use`, `- [For teachers](${SITE}/teachers): classes and teaching resources`, '');
  return new Response(out.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
