const segmenter = new Intl.Segmenter('en', { granularity: 'sentence' });
const oneLine = (text: string) => text.replace(/\s+/g, ' ').trim();
const sentences = (text: string) => Array.from(segmenter.segment(oneLine(text)), ({ segment }) => segment.trim());

/** Prefer complete sentences from the summary used by Skim, or the first sentence of the hook. */
export function metaDescription(summary: string, hook = ''): string {
  const min = 120;
  const max = 160;
  const parts = summary.trim() ? sentences(summary) : sentences(hook).slice(0, 1);
  for (let start = 0; start < parts.length; start++) {
    let candidate = '';
    for (const sentence of parts.slice(start)) {
      candidate = candidate ? `${candidate} ${sentence}` : sentence;
      if (candidate.length > max) break;
      if (candidate.length >= min) return candidate;
    }
  }
  const text = parts.join(' ');
  if (text.length <= max) return text;
  const end = text.lastIndexOf(' ', max - 1);
  return `${text.slice(0, end === -1 ? max - 1 : end).replace(/[,;:.\u2014-]+$/, '')}…`;
}

/** The film's own takeaway, with the title to distinguish films that share a takeaway. */
export function filmDescription(film: { title: string; takeaways?: string[] }, lessonSummary: string): string {
  const title = /[.!?]$/.test(film.title) ? film.title : `${film.title}.`;
  return oneLine(`${title} ${film.takeaways?.[0] ?? metaDescription(lessonSummary)}`);
}
