/**
 * rehype-design-answer — put an answer box under every "Design problem" in a lesson.
 *
 * Lessons write a design problem as a "### Design problem" heading, the problem, then a
 * <details> fold with one worked answer. This inserts, just before that fold, a box
 * where the reader writes their own answer first. The box is plain HTML: without
 * JavaScript it is an ordinary text area; with it (DesignAnswer.astro on the lesson
 * page) the answer is kept in this browser, and a student in a teacher's class can
 * send it to the teacher and, if the class has AI feedback on, get feedback.
 *
 * Items are numbered design-1, design-2… in page order, the same numbering
 * src/lib/open-items.ts gives the worked answers. Lessons need no edits.
 */

const text = (n) => (n.type === 'text' ? n.value : (n.children || []).map(text).join(''));
const isDetails = (n) => (n.type === 'element' && n.tagName === 'details') || (n.type === 'mdxJsxFlowElement' && n.name === 'details');
const el = (tagName, properties, children = []) => ({ type: 'element', tagName, properties, children });
const t = (value) => ({ type: 'text', value });

function box(item) {
  const id = `da-${item}`;
  return el('div', { className: ['design-answer'], dataDesignItem: item }, [
    el('label', { className: ['da-label'], htmlFor: id }, [t('Your answer first. Write it before you open the worked answer.')]),
    el('textarea', { id, rows: 5, className: ['da-text'], dataDaText: '' }, []),
    el('p', { className: ['da-row'] }, [
      el('span', { className: ['da-saved'], dataDaSaved: '', hidden: true }, [t('Saved in this browser only.')]),
      el('button', { type: 'button', className: ['da-send'], dataDaSend: '', hidden: true }, [t('Send to my teacher')]),
      el('span', { className: ['da-note'], dataDaNote: '', role: 'status' }, []),
    ]),
    el('div', { className: ['da-feedback'], dataDaFeedback: '', hidden: true }, []),
  ]);
}

export default function rehypeDesignAnswer() {
  return (tree, file) => {
    const path = (file.path || (file.history && file.history[0]) || '').split('\\').join('/');
    if (!/lessons\/[^/]+\/lesson\.mdx$/.test(path)) return;
    const kids = tree.children;
    let n = 0;
    for (let i = 0; i < kids.length; i++) {
      const h = kids[i];
      if (h.type !== 'element' || h.tagName !== 'h3' || text(h).trim() !== 'Design problem') continue;
      // The worked-answer fold that follows, before the next heading.
      for (let j = i + 1; j < kids.length; j++) {
        const k = kids[j];
        if (k.type === 'element' && /^h[1-3]$/.test(k.tagName)) break;
        if (isDetails(k)) {
          n++;
          kids.splice(j, 0, box(`design-${n}`), t('\n'));
          i = j + 2;
          break;
        }
      }
    }
  };
}
