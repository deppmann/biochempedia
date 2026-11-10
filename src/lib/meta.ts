/** A meta description: one line, at most `max` characters, cut at a word with an ellipsis. */
export function metaDescription(text: string, max = 155): string {
  const t = text.replace(/\s+/g, ' ').trim();
  if (t.length <= max) return t;
  const cut = t.slice(0, max - 1);
  const atWord = cut.lastIndexOf(' ');
  return `${(atWord > max * 0.6 ? cut.slice(0, atWord) : cut).replace(/[\s,;:.\u2014-]+$/, '')}\u2026`;
}
