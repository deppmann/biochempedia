/**
 * predicts — a lesson's Predict questions, collected at deploy time (2026-11-23).
 *
 * Lessons ask the reader to predict before a result is shown. In the MDX that is always one
 * paragraph that opens "**Predict.**" (or "**Predict 2.**"), then a <details> whose <summary> is
 * "Check your prediction" and whose body is the answer. predictsOf() reads the lesson body and
 * returns each such pair, rendered to HTML, so the lesson page and its Skim page can list them
 * once more near the end ("Try them again"), each answer folded shut.
 *
 * Kept strict, so the list never shows a half question:
 *   - the question is one paragraph (plus, at most, its numbered parts or a small table), and the
 *     <details> must come straight after it;
 *   - a pair that holds a component (<LessonFigure>, <EquationCard> …), an import or a {…}
 *     expression is left out: it cannot be rendered outside the lesson's MDX;
 *   - a Predict step inside a numbered list (the hands-on guides) is left out.
 * A Predict that is left out is still in the lesson where it always was. The lesson text is never
 * edited. The words go through the same Markdown settings as the lesson and the same subscript
 * rule (rehype-sub-sup), so E_K reads the same in both places.
 */
import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import rehypeSubSup from './rehype-sub-sup.mjs';

export interface PredictSource {
  /** "Predict" or "Predict 2", as the lesson numbers it. */
  label: string;
  /** Markdown of the question, without the bold label. */
  question: string;
  /** The lesson's own words on the fold ("Check your prediction"). */
  check: string;
  /** Markdown of the answer. */
  answer: string;
  /** Text of the ## heading the question sits under, when it has one. */
  heading: string | null;
}
export interface Predict extends Omit<PredictSource, 'question' | 'answer'> { questionHtml: string; answerHtml: string; sectionSlug: string | null }

const START = /^\*\*Predict(?: (\d+))?\.\*\*[ \t]*(.*)$/;
const UNSAFE = /<[A-Z]|[{}]|^\s*(import|export)\s/m;

/** The pairs in a lesson body, as Markdown. Pure text work: scripts/test-predicts.mjs covers it. */
export function predictSources(body: string): PredictSource[] {
  const lines = body.split(/\r?\n/);
  const out: PredictSource[] = [];
  let heading: string | null = null;
  let fence = false;
  for (let i = 0; i < lines.length; i++) {
    if (/^\s*(```|~~~)/.test(lines[i])) { fence = !fence; continue; }
    if (fence) continue;
    const h = /^##\s+(.+?)\s*#*\s*$/.exec(lines[i]);
    if (h) { heading = h[1]; continue; }
    const m = START.exec(lines[i]);
    if (!m) continue;
    // The question: this paragraph, plus at most two more short blocks (its numbered parts or a
    // small table), as long as the <details> comes straight after them.
    const q = [m[2]];
    let j = i + 1;
    let blocks = 1;
    for (; j < lines.length && lines[j].trim() !== '<details>'; j++) {
      const t = lines[j].trim();
      if (t === '') { if (lines[j + 1]?.trim() && lines[j + 1].trim() !== '<details>') blocks++; }
      else if (/^(<|#|\*\*[^*]+\.\*\*)/.test(t)) { blocks = 99; break; }             // a tag, a heading or the next labelled box
      q.push(lines[j]);
    }
    if (blocks > 3 || q.join(' ').split(/\s+/).length > 160) continue;
    if (j >= lines.length || lines[j].trim() !== '<details>') continue;
    j++;
    while (j < lines.length && lines[j].trim() === '') j++;
    const s = /^\s*<summary>([^<]+)<\/summary>\s*$/.exec(lines[j] ?? '');
    if (!s) continue;
    const a: string[] = [];
    let closed = false;
    for (j++; j < lines.length; j++) {
      const t = lines[j].trim();
      if (t === '</details>') { closed = true; break; }
      if (t === '<details>' || START.test(lines[j]) || /^##\s/.test(lines[j])) break;   // not the simple shape
      a.push(lines[j]);
    }
    const question = q.join('\n').trim();
    const answer = a.join('\n').trim();
    if (!closed || !question || !answer || UNSAFE.test(question) || UNSAFE.test(answer)) continue;
    out.push({ label: m[1] ? `Predict ${m[1]}` : 'Predict', question, check: s[1].trim(), answer, heading });
    i = j;
  }
  return out;
}

let processor: ReturnType<typeof createMarkdownProcessor> | undefined;

/** The pairs rendered to HTML, each with the anchor of its section on the lesson page. */
export async function predictsOf(body: string, headings: { depth: number; slug: string; text: string }[] = []): Promise<Predict[]> {
  const sources = predictSources(body);
  if (sources.length === 0) return [];
  processor ??= createMarkdownProcessor({ syntaxHighlight: false, rehypePlugins: [rehypeSubSup] });
  const md = await processor;
  const h2 = headings.filter((h) => h.depth === 2 && h.slug);
  // Astro's heading text is the rendered text; the source may carry Markdown marks. Compare loosely.
  // render() also applies smart quotes and dashes to heading text.
  const plain = (t: string) => t.replace(/<[^>]+>/g, '').replace(/[*_`\\'"‘’“”]/g, '').replace(/…/g, '...').replace(/[–—]/g, '-').replace(/-+/g, '-').replace(/\s+/g, ' ').trim().toLowerCase();
  return Promise.all(sources.map(async ({ question, answer, ...rest }) => ({
    ...rest,
    questionHtml: (await md.render(question)).code,
    answerHtml: (await md.render(answer)).code,
    sectionSlug: rest.heading ? h2.find((h) => plain(h.text) === plain(rest.heading!))?.slug ?? null : null,
  })));
}
