/* Build-time: link each quiz question to the lesson section that teaches it.

   A lesson's sections are its ## and ### headings; Astro gives each one an id,
   so /lessons/<slug>/#<id> is a stable anchor. For every question we score each
   section by the distinctive words it shares with the question (stem, correct
   answer and rationale), weighting rarer words more (inverse document frequency
   across that lesson's sections), and keep the best section if the match is
   clear enough. No model, nothing to maintain: it re-runs on every build, so an
   edited lesson re-links itself.

   Used for "Read this again" after a missed question and in the review queue.
   A question with no clear match gets no link rather than a wrong one. */

import type { Question } from '../schema';

export interface Anchor { id: string; text: string }
interface Heading { depth: number; slug: string; text: string }

const STOP = new Set(('about above after again against also among another because been before being below between both '
  + 'cannot could does doing down during each from further have having here into itself just more most much must only '
  + 'other over same should some such than that their them then there these they this those through under until very '
  + 'were what when where which while whom will with would your answer correct choice choices question statement '
  + 'lesson following true false best explains explain describes describe likely most least option options').split(' '));

const words = (t: string) =>
  t.toLowerCase().replace(/<[^>]+>/g, ' ').replace(/[^a-z0-9α-ω₀-₉+\- ]/g, ' ')
    .split(/\s+/).filter((w) => w.length >= 4 && !STOP.has(w) && !/^\d+$/.test(w));

/** Split the MDX body into the text under each ## / ### heading, in order. */
function sectionTexts(body: string): { text: string; heading: string }[] {
  const lines = body.split('\n');
  const out: { text: string; heading: string }[] = [];
  let fence = false;
  let cur: { text: string; heading: string } | null = null;
  for (const line of lines) {
    if (/^\s*```/.test(line)) fence = !fence;
    const m = !fence && /^(#{2,3})\s+(.+?)\s*$/.exec(line);
    if (m) { cur = { heading: m[2], text: m[2] + '\n' }; out.push(cur); continue; }
    if (cur) cur.text += line + '\n';
  }
  return out;
}

const norm = (t: string) => t.toLowerCase().replace(/[`*_]/g, '').replace(/\s+/g, ' ').trim();

export function anchorsFor(body: string, headings: Heading[], questions: Question[]): (Anchor | null)[] {
  const hs = headings.filter((h) => h.depth === 2 || h.depth === 3);
  const secs = sectionTexts(body);
  // Pair parsed sections with Astro's headings: by position when the counts agree,
  // otherwise by heading text.
  const paired = secs.map((s, i) => {
    const h = secs.length === hs.length ? hs[i] : hs.find((x) => norm(x.text) === norm(s.heading));
    return h ? { id: h.slug, text: h.text, bag: new Set(words(s.text)) } : null;
  }).filter((x): x is { id: string; text: string; bag: Set<string> } => !!x && x.bag.size > 0);
  if (paired.length === 0) return questions.map(() => null);

  const df = new Map<string, number>();
  for (const s of paired) for (const w of s.bag) df.set(w, (df.get(w) ?? 0) + 1);
  const idf = (w: string) => Math.log(1 + paired.length / (df.get(w) ?? paired.length));

  return questions.map((q) => {
    const qw = new Set(words(`${q.stem} ${q.choices[q.answer] ?? ''} ${q.rationale}`));
    let best: (typeof paired)[number] | null = null;
    let bestScore = 0;
    let second = 0;
    for (const s of paired) {
      let score = 0;
      for (const w of qw) if (s.bag.has(w)) score += idf(w);
      if (score > bestScore) { second = bestScore; bestScore = score; best = s; }
      else if (score > second) second = score;
    }
    // Clear enough: a few distinctive shared words, and ahead of the runner-up
    // (a one-section lesson only needs the first test).
    const clear = bestScore >= 2.0 && (paired.length === 1 || bestScore >= second * 1.15);
    return best && clear ? { id: best.id, text: best.text } : null;
  });
}
