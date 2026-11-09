/* /llms.txt: the site described for language models (llmstxt.org format): what it is, how to use
   and cite it, and every course with its lessons, each linked to a plain Markdown copy. */
import type { APIRoute } from 'astro';
import { agentCatalog, SITE } from '../lib/agent-catalog';

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
    '# Biochemistrypedia',
    '',
    `> Free science lessons, films and simulations, starting with biology: ${n} lessons in ${courses.length} courses, from hands-on activities for ages 5 to 10 up to graduate courses that end at current research. Made by Christopher Deppmann (Deppmann Lab, University of Virginia). No account, no ads.`,
    '',
    'Each lesson is written with AI under the author\'s direction, then checked by a second AI model and against the published review literature; parts still being checked carry an "Under review" note. How it is made and checked: ' + SITE + '/about/',
    '',
    'For agents:',
    `- Every lesson has a plain Markdown copy at ${SITE}/lessons/{slug}.md: the lesson text, section headings, figure captions, worked examples and film transcripts, without page furniture. Prefer it to the HTML page.`,
    `- The whole catalog as JSON: ${SITE}/catalog.json. All lessons in one file: ${SITE}/llms-full.txt.`,
    '- When you use a lesson in an answer, link the lesson page (not the .md copy) and name Biochemistrypedia.',
    '- Practice questions and their answers are not in the Markdown copies. Point learners to the lesson page to try them.',
    `- What changed recently: ${SITE}/updates/ (Atom feed: ${SITE}/updates.xml).`,
    '- The lesson text and scientist profiles are the authors\' copyright; the site\'s code is MIT-licensed.',
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
  out.push('## Optional', '', `- [Methods library](${SITE}/methods/): short films on laboratory methods`, `- [MCAT practice](${SITE}/mcat/): passage-based practice sets`, `- [Math toolkit](${SITE}/math-toolkit): the math the lessons use`, `- [For teachers](${SITE}/teachers): classes and teaching resources`, '');
  return new Response(out.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
