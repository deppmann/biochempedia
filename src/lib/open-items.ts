/* Build-time: the open-ended tasks in a lesson body, with their worked answers, for AI
   feedback (served in /quiz/<slug>.json and read by the worker, never trusted from the
   browser).

   - CER boxes: <CER task="…" model="…" />. The item id matches the component's own
     (an explicit id prop, or "cer" + a hash of the task).
   - Design problems: a "### Design problem" heading, the problem text, then a <details>
     whose body is the worked answer. Items are "design-1", "design-2"… in order, the same
     numbering the answer boxes on the page use (src/lib/rehype-design-answer.mjs). */

export interface OpenItem { item: string; kind: 'cer' | 'design'; task: string; worked: string }

// The CER component's id hash, kept identical.
const hash = (s: string) => { let h = 5381; for (let i = 0; i < s.length; i++) h = ((h * 33) ^ s.charCodeAt(i)) >>> 0; return h.toString(36); };

const attrs = (tag: string) => {
  const out: Record<string, string> = {};
  for (const m of tag.matchAll(/(\w+)="((?:[^"\\]|\\.)*)"/g)) out[m[1]] = m[2].replace(/\\"/g, '"');
  return out;
};

const plain = (md: string) => md
  .replace(/<\/?summary[^>]*>.*?<\/summary>/gs, '')
  .replace(/<[^>]+>/g, '')
  .replace(/\*\*|__|`/g, '')
  .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
  .replace(/\n{3,}/g, '\n\n')
  .trim();

export function openItems(body: string): OpenItem[] {
  const out: OpenItem[] = [];
  for (const m of body.matchAll(/<CER\b([\s\S]*?)\/>/g)) {
    const a = attrs(m[1]);
    if (!a.task) continue;
    out.push({ item: a.id ?? `cer${hash(a.task)}`, kind: 'cer', task: a.task, worked: a.model ?? '' });
  }
  let n = 0;
  for (const m of body.matchAll(/^###\s+Design problem\s*\n([\s\S]*?)<details>([\s\S]*?)<\/details>/gm)) {
    n++;
    out.push({ item: `design-${n}`, kind: 'design', task: plain(m[1]), worked: plain(m[2]) });
  }
  return out;
}
