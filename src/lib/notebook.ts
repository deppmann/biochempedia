/* Browser-only highlights and notes. No account needed, no server.

   Everything lives in one localStorage entry on this device. The accounts code
   (src/lib/learner.ts) reads and merges this same entry to sync it between
   devices, so the shape below is a shared contract: change it only together.

     { v: 1, items: { <id>: NotebookItem } }

   kind "highlight"  a passage of a lesson, found again by its quote plus a few
                     characters of text on either side (prefix / suffix).
   kind "note"       a note on the whole lesson, with no quote.

   Deleting keeps the item as a tombstone (deleted: true, updated bumped), so a
   sync can delete it on every device. The UI hides deleted items. Tombstones
   older than 90 days are pruned when the notebook is saved.

   Storage may be blocked (private windows, strict settings). Every read and
   write is wrapped; a failure means "nothing remembered", never an error. */

export const NOTEBOOK_KEY = 'biochempedia:notebook:v1';
export const NOTEBOOK_EVENT = 'bp-notebook';

export type HighlightColor = 'yellow' | 'green' | 'blue';
export const COLORS: HighlightColor[] = ['yellow', 'green', 'blue'];

export interface NotebookItem {
  id: string;
  kind: 'highlight' | 'note';
  slug: string;
  title: string;
  section: string;
  anchorId: string;
  quote: string;
  prefix: string;
  suffix: string;
  color: HighlightColor;
  note: string;
  created: number;
  updated: number;
  deleted: boolean;
}

export interface Notebook {
  v: 1;
  items: Record<string, NotebookItem>;
}

const TOMBSTONE_MS = 90 * 86_400_000;

const empty = (): Notebook => ({ v: 1, items: {} });

function validItem(x: unknown): x is NotebookItem {
  const i = x as NotebookItem;
  return !!i && typeof i === 'object' && typeof i.id === 'string' && typeof i.slug === 'string'
    && (i.kind === 'highlight' || i.kind === 'note') && typeof i.updated === 'number';
}

/** Fill in any missing fields so older or partial records never break the UI. */
function clean(i: NotebookItem): NotebookItem {
  return {
    id: i.id,
    kind: i.kind,
    slug: i.slug,
    title: typeof i.title === 'string' ? i.title : '',
    section: typeof i.section === 'string' ? i.section : '',
    anchorId: typeof i.anchorId === 'string' ? i.anchorId : '',
    quote: typeof i.quote === 'string' ? i.quote : '',
    prefix: typeof i.prefix === 'string' ? i.prefix : '',
    suffix: typeof i.suffix === 'string' ? i.suffix : '',
    color: COLORS.includes(i.color) ? i.color : 'yellow',
    note: typeof i.note === 'string' ? i.note : '',
    created: typeof i.created === 'number' ? i.created : i.updated,
    updated: i.updated,
    deleted: i.deleted === true,
  };
}

export function loadNotebook(): Notebook {
  try {
    const raw = window.localStorage.getItem(NOTEBOOK_KEY);
    if (!raw) return empty();
    const p = JSON.parse(raw);
    if (!p || typeof p !== 'object' || p.v !== 1 || !p.items || typeof p.items !== 'object') return empty();
    const items: Record<string, NotebookItem> = {};
    for (const [id, it] of Object.entries(p.items)) if (validItem(it) && it.id === id) items[id] = clean(it);
    return { v: 1, items };
  } catch {
    return empty();
  }
}

/** Write the notebook and tell the page. Returns false when storage is blocked. */
export function saveNotebook(nb: Notebook): boolean {
  const now = Date.now();
  for (const [id, it] of Object.entries(nb.items)) {
    if (it.deleted && now - it.updated > TOMBSTONE_MS) delete nb.items[id];
  }
  let ok = true;
  try {
    window.localStorage.setItem(NOTEBOOK_KEY, JSON.stringify(nb));
  } catch {
    ok = false;
  }
  try { window.dispatchEvent(new CustomEvent(NOTEBOOK_EVENT)); } catch { /* no window */ }
  return ok;
}

/** True when this browser lets the site save anything. */
export function storageWorks(): boolean {
  try {
    const k = `${NOTEBOOK_KEY}:probe`;
    window.localStorage.setItem(k, '1');
    window.localStorage.removeItem(k);
    return true;
  } catch {
    return false;
  }
}

/** "h_" + 12 random lowercase letters and digits. */
export function newId(): string {
  const abc = 'abcdefghijklmnopqrstuvwxyz0123456789';
  const bytes = new Uint8Array(12);
  try { crypto.getRandomValues(bytes); } catch { for (let i = 0; i < 12; i++) bytes[i] = Math.floor(Math.random() * 256); }
  let s = 'h_';
  for (const b of bytes) s += abc[b % abc.length];
  return s;
}

/** Add or replace one item. `updated` is set to now (and `created` if missing). */
export function upsertItem(item: Partial<NotebookItem> & Pick<NotebookItem, 'slug' | 'kind'>): NotebookItem {
  const nb = loadNotebook();
  const now = Date.now();
  const prev = item.id ? nb.items[item.id] : undefined;
  const next = clean({
    ...(prev ?? {}),
    ...item,
    id: item.id ?? prev?.id ?? newId(),
    created: prev?.created ?? item.created ?? now,
    updated: Math.max(now, (prev?.updated ?? 0) + 1),
    deleted: item.deleted ?? false,
  } as NotebookItem);
  nb.items[next.id] = next;
  saveNotebook(nb);
  return next;
}

/** Mark an item deleted (a tombstone) so a sync removes it everywhere. */
export function deleteItem(id: string): boolean {
  const nb = loadNotebook();
  const it = nb.items[id];
  if (!it) return false;
  nb.items[id] = { ...it, deleted: true, updated: Math.max(Date.now(), it.updated + 1) };
  saveNotebook(nb);
  return true;
}

/** Every item that is not deleted. */
export function allItems(): NotebookItem[] {
  return Object.values(loadNotebook().items).filter((i) => !i.deleted);
}

/** Merge items from another device: per id, the record with the larger
 *  `updated` wins (tombstones included). Saves and returns true if anything
 *  here changed. */
export function mergeItems(remoteItems: Record<string, unknown> | unknown[] | null | undefined): boolean {
  if (!remoteItems || typeof remoteItems !== 'object') return false;
  const list = Array.isArray(remoteItems) ? remoteItems : Object.values(remoteItems);
  const nb = loadNotebook();
  let changed = false;
  for (const r of list) {
    if (!validItem(r)) continue;
    const mine = nb.items[r.id];
    if (!mine || r.updated > mine.updated) {
      nb.items[r.id] = clean(r);
      changed = true;
    }
  }
  if (changed) saveNotebook(nb);
  return changed;
}
