/**
 * rehype-method-links — link method names in lesson prose to the methods library.
 *
 * For each lesson (src/content/lessons/<slug>/lesson.mdx) it takes the methods whose `lessons`
 * list names that lesson (src/data/methods.ts) and links the FIRST mention of each method in
 * each section (a section starts at an <h2>) to /methods/<method>/. The link carries
 * data-method, which the lesson page's pop-out player (MethodPopout.astro) uses to open the
 * film in place; without JavaScript it is an ordinary link to the method page.
 *
 * It never links inside headings, links, code, buttons, figures or MDX components (figures,
 * films, simulations), and only in lessons the inventory ties to the method, so a common word
 * in an unrelated lesson is never touched. Runs at build time: lessons need no edits.
 */

const SKIP_TAGS = new Set(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'code', 'pre', 'kbd', 'samp', 'script', 'style',
  'svg', 'math', 'button', 'figure', 'figcaption', 'summary', 'sup', 'sub', 'cite', 'abbr', 'table']);
const isJsx = (n) => typeof n.type === 'string' && n.type.startsWith('mdx');

const escape = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** One regex per term. Lowercase terms match any case; terms with a capital match that case.
 *  A plural "s" is allowed after a term that ends in a letter. */
function compile(term) {
  const plural = /[a-z]$/i.test(term) ? '(?:e?s)?' : '';
  const flags = term === term.toLowerCase() ? 'i' : '';
  return new RegExp(`(?<![\\w-])${escape(term)}${plural}(?![\\w-])`, flags);
}

export default function rehypeMethodLinks({ methods = [] } = {}) {
  const compiled = methods
    .filter((m) => m.terms && m.terms.length)
    .map((m) => ({ slug: m.slug, lessons: new Set(m.lessons), res: m.terms.map(compile), name: m.name }));

  return (tree, file) => {
    const path = (file.path || (file.history && file.history[0]) || '').split('\\').join('/');
    const hit = /lessons\/([^/]+)\/lesson\.mdx$/.exec(path);
    if (!hit) return;
    const mine = compiled.filter((m) => m.lessons.has(hit[1]));
    if (mine.length === 0) return;

    let linked = new Set();

    /** The earliest match in `text` among methods not yet linked in this section. */
    const firstMatch = (text) => {
      let best = null;
      for (const m of mine) {
        if (linked.has(m.slug)) continue;
        for (const re of m.res) {
          const r = re.exec(text);
          if (r && (!best || r.index < best.index || (r.index === best.index && r[0].length > best.len))) {
            best = { index: r.index, len: r[0].length, slug: m.slug, name: m.name };
          }
        }
      }
      return best;
    };

    const linkText = (node) => {
      const out = [];
      let rest = node.value;
      for (;;) {
        const m = firstMatch(rest);
        if (!m) break;
        linked.add(m.slug);
        if (m.index > 0) out.push({ type: 'text', value: rest.slice(0, m.index) });
        out.push({
          type: 'element',
          tagName: 'a',
          properties: { href: `/methods/${m.slug}/`, className: ['method-link'], dataMethod: m.slug, title: `Method: ${m.name}` },
          children: [{ type: 'text', value: rest.slice(m.index, m.index + m.len) }],
        });
        rest = rest.slice(m.index + m.len);
      }
      if (out.length === 0) return null;
      if (rest) out.push({ type: 'text', value: rest });
      return out;
    };

    const walk = (node) => {
      if (!node.children) return;
      const next = [];
      for (const child of node.children) {
        if (child.type === 'text') {
          const parts = linkText(child);
          if (parts) next.push(...parts);
          else next.push(child);
          continue;
        }
        if (child.type === 'element' && !SKIP_TAGS.has(child.tagName)) walk(child);
        // MDX components (figures, films, simulations) and skipped tags are left as they are.
        next.push(child);
      }
      node.children = next;
    };

    for (const child of tree.children) {
      if (child.type === 'element' && child.tagName === 'h2') {
        linked = new Set();
        continue;
      }
      if (isJsx(child)) continue;
      if (child.type === 'element' && !SKIP_TAGS.has(child.tagName)) walk({ children: [child] });
    }
  };
}
