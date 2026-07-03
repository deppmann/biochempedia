/* Tiny DOM helpers — no framework. Keeps the engine readable. */

type Attrs = Record<string, string | number | boolean | undefined | null | ((e: Event) => void)>;

/** el('button.foo.bar', { onclick, 'aria-label': '…' }, ...children) */
export function el(
  spec: string,
  attrs?: Attrs | null,
  ...children: Array<Node | string | null | undefined | false>
): HTMLElement {
  const [tag, ...classes] = spec.split('.');
  const node = document.createElement(tag || 'div');
  if (classes.length) node.className = classes.join(' ');
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === 'html') { node.innerHTML = String(v); continue; }
      if (k.startsWith('on') && typeof v === 'function') {
        node.addEventListener(k.slice(2).toLowerCase(), v as EventListener);
        continue;
      }
      if (typeof v === 'boolean') { if (v) node.setAttribute(k, ''); continue; }
      node.setAttribute(k, String(v));
    }
  }
  for (const c of children) {
    if (c == null || c === false) continue;
    node.append(typeof c === 'string' ? document.createTextNode(c) : c);
  }
  return node;
}

export function clear(node: HTMLElement): void {
  while (node.firstChild) node.removeChild(node.firstChild);
}

/** Fisher–Yates shuffle (returns a new array). Seedless — fine for a party game. */
export function shuffle<T>(arr: readonly T[]): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export const prefersReducedMotion = (): boolean =>
  typeof window !== 'undefined' &&
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches === true;
