/**
 * rehype-sub-sup — render plain-text math notation as real subscripts and superscripts.
 *
 * Lessons write symbols the way a keyboard allows: I_ion, E_K, g_Na, P_open, l_x for a subscript and
 * 10^-6, h^2, cm^-2, I^A for a superscript (913 such uses in 93 lessons, 2026-11-05). Readers saw the
 * raw underscore and caret. This turns them into <sub> and <sup> in the rendered page, so the lesson
 * source stays easy to write. It changes no lesson.
 *
 * Rules, kept narrow so ordinary words are never touched:
 *   - a subscript is BASE_SUB where BASE is 1–5 letters/digits (or a Greek letter written as a word:
 *     pi, Psi, tau, Delta, lambda, mu, sigma, alpha, beta, gamma, theta, omega, which become the
 *     symbol) and SUB is 1–8 letters, digits or + −, or {anything} for longer subscripts;
 *   - a superscript is BASE^SUP with SUP an optional minus then 1–6 letters, digits or +, or {anything};
 *   - a parenthesised script, e^(−t/τ) or l_(x+1), is raised or lowered whole, without its brackets;
 *   - nothing inside code, pre, kbd, script, style, math or a link's text is changed, and a token
 *     that looks like a file name or a URL part is left alone.
 */

const GREEK = { pi: 'π', Pi: 'Π', psi: 'ψ', Psi: 'Ψ', tau: 'τ', Delta: 'Δ', delta: 'δ', lambda: 'λ', mu: 'μ', sigma: 'σ', Sigma: 'Σ', alpha: 'α', beta: 'β', gamma: 'γ', theta: 'θ', omega: 'ω' };
const SKIP = new Set(['code', 'pre', 'kbd', 'script', 'style', 'math', 'a', 'sub', 'sup', 'textarea']);

// One combined pattern: group 1 base, 2 op (_ or ^), 3 braced, 4 parenthesised, 5 plain.
const RE = /(?<![\p{L}\p{N}_/.\\`-])((?:pi|Pi|psi|Psi|tau|Delta|delta|lambda|mu|sigma|Sigma|alpha|beta|gamma|theta|omega)|[\p{L}\p{N}][\p{L}\p{N}]{0,4}|\))([_^])(?:\{([^{}]{1,24})\}|\(([^()]{1,24})\)|([−\-]?[\p{L}\p{N}+−]{1,8}))(?![\p{L}\p{N}_/])/gu;

const el = (tagName, children) => ({ type: 'element', tagName, properties: {}, children });
const txt = (value) => ({ type: 'text', value });

function convert(value) {
  RE.lastIndex = 0;
  if (!RE.test(value)) return null;
  RE.lastIndex = 0;
  const out = [];
  let last = 0;
  for (const m of value.matchAll(RE)) {
    const [whole, base, op, braced, paren, plain] = m;
    const script = braced ?? paren ?? plain;
    if (op === '_' && /^\d+$/.test(base) && /^\d+$/.test(script)) continue;      // 2_3 is not notation
    if (op === '^' && script.length > 6 && !braced && !paren) continue;
    if (plain && /^[−-]$/.test(plain)) continue;                                   // a lone minus is not a script
    if (/\.(mp4|vtt|webp|png|jpg|pdf|html|js|mjs|ts)$/i.test(whole)) continue;
    out.push(txt(value.slice(last, m.index)));
    out.push(txt(GREEK[base] ?? base));
    out.push(el(op === '_' ? 'sub' : 'sup', [txt(script.replace(/-/g, '−'))]));
    last = m.index + whole.length;
  }
  if (!out.length) return null;
  out.push(txt(value.slice(last)));
  return out.filter((n) => n.type !== 'text' || n.value !== '');
}

function walk(node) {
  if (!node.children) return;
  for (let i = 0; i < node.children.length; i++) {
    const c = node.children[i];
    if (c.type === 'text') {
      const parts = convert(c.value);
      if (parts) { node.children.splice(i, 1, ...parts); i += parts.length - 1; }
    } else if (c.type === 'element' && !SKIP.has(c.tagName)) {
      walk(c);
    } else if ((c.type === 'mdxJsxFlowElement' || c.type === 'mdxJsxTextElement') && !SKIP.has(c.name)) {
      walk(c);
    }
  }
}

export default function rehypeSubSup() {
  return (tree) => walk(tree);
}

export { convert as _convertForTest };
