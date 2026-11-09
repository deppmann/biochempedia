/* Teacher classes, browser side. A student who joined a class on this device has
   an HttpOnly cookie the page can't read, plus this small non-secret marker in
   localStorage so pages know to report answers. Everyone else: no requests at all.

   Reports are fire-and-forget. A failed report never interrupts the lesson. */

const KEY = 'biochempedia:class:v1';
// Running "Again" counts per flashcard, kept only for a student in a class, only for lessons
// the teacher assigned with flashcards on: { "<lesson slug>": { "<card id>": n } }.
const CARDS_KEY = 'biochempedia:class-cards:v1';

export interface ClassMarker { className: string; nickname: string; teacherName?: string }

export function enrolled(): ClassMarker | null {
  try {
    const m = JSON.parse(window.localStorage.getItem(KEY) || 'null');
    return m && typeof m.className === 'string' ? m : null;
  } catch { return null; }
}

export function setEnrolled(m: ClassMarker | null) {
  try {
    if (m) window.localStorage.setItem(KEY, JSON.stringify(m));
    else { window.localStorage.removeItem(KEY); window.localStorage.removeItem(CARDS_KEY); }
  } catch { /* storage blocked: the cookie still works, the page just won't know */ }
  window.dispatchEvent(new CustomEvent('bp-class'));
}

export async function api<T = unknown>(path: string, body?: unknown, method = body === undefined ? 'GET' : 'POST'): Promise<{ ok: boolean; status: number; data: T & { error?: string } }> {
  try {
    const r = await fetch(path, {
      method,
      credentials: 'same-origin',
      // Anything but GET goes as JSON: the API refuses other state-changing requests.
      headers: method === 'GET' ? {} : { 'Content-Type': 'application/json' },
      body: method === 'GET' ? undefined : JSON.stringify(body ?? {}),
    });
    const data = await r.json().catch(() => ({}));
    return { ok: r.ok, status: r.status, data };
  } catch {
    return { ok: false, status: 0, data: { error: 'Could not reach the site. Check your connection.' } as T & { error?: string } };
  }
}

/** Today's date where the reader is (YYYY-MM-DD), for due dates. `toISOString()` gives the UTC date,
 *  which is already tomorrow by early evening in the Americas. */
export function localToday(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

export type AnswerKind = 'quiz' | 'idea' | 'cer' | 'done' | 'stuck' | 'cards';

/** Send one answer for the current student, if they are in a class. */
export function report(lesson: string, kind: AnswerKind, fields: Record<string, unknown>) {
  if (!enrolled()) return;
  fetch('/api/student/answer', {
    method: 'POST',
    credentials: 'same-origin',
    keepalive: true,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lesson, kind, ...fields }),
  }).then((r) => { if (r.status === 401) setEnrolled(null); }).catch(() => { /* offline: skip */ });
}

// ---- AI feedback and teacher notes (only for a student in a class) ------------------
export interface StudentMe { nickname: string; className: string; teacherName: string; pending: boolean; ai?: boolean; assignments: { slug: string; due: string | null; flashcards?: boolean }[]; done: string[]; stuck?: string }
export interface FeedbackItem { id: number; lesson: string; kind: string; item: string; text: string; source: 'ai' | 'teacher'; at: number }

let meCache: Promise<StudentMe | null> | null = null;
/** The student's class view, fetched once per page (null when not in a class). */
export function studentMe(lesson?: string): Promise<StudentMe | null> {
  if (!enrolled()) return Promise.resolve(null);
  meCache ??= api<StudentMe>(`/api/student/me${lesson ? `?lesson=${encodeURIComponent(lesson)}` : ''}`).then((r) => {
    if (r.status === 401) setEnrolled(null);
    return r.ok ? r.data : null;
  });
  return meCache;
}

/** A flashcard marked "Again". Counted only when this student's class assigned the lesson with
 *  flashcards on; the lesson's running counts go with the usual report (no AI, nothing for anyone else). */
export function markAgain(lesson: string, cardId: string) {
  if (!enrolled()) return;
  studentMe(lesson).then((me) => {
    if (!me || me.pending || !me.assignments.some((a) => a.slug === lesson && a.flashcards)) return;
    let all: Record<string, Record<string, number>> = {};
    try { all = JSON.parse(window.localStorage.getItem(CARDS_KEY) || '{}') || {}; } catch { /* start empty */ }
    const mine = (all[lesson] ??= {});
    mine[cardId] = Math.min(999, (mine[cardId] ?? 0) + 1);
    try { window.localStorage.setItem(CARDS_KEY, JSON.stringify(all)); } catch { /* still sent this time */ }
    report(lesson, 'cards', { cards: mine });
  });
}

let fbCache: Promise<FeedbackItem[]> | null = null;
/** Released feedback and teacher notes for this lesson. */
export function lessonFeedback(lesson: string): Promise<FeedbackItem[]> {
  if (!enrolled()) return Promise.resolve([]);
  fbCache ??= api<{ feedback: FeedbackItem[] }>(`/api/student/feedback?lesson=${encodeURIComponent(lesson)}`).then((r) => (r.ok ? r.data.feedback : []));
  return fbCache;
}

/** Ask for AI feedback on a written answer. */
export async function askFeedback(lesson: string, item: string, fields: Record<string, string>) {
  return api<{ status: 'released' | 'held'; text?: string }>('/api/student/feedback', { lesson, item, ...fields });
}

/** Fill a feedback box (static element) with one piece of feedback. */
export function showFeedback(box: HTMLElement, text: string, source: 'ai' | 'teacher' | 'held') {
  box.hidden = false;
  box.textContent = '';
  const head = document.createElement('p');
  head.className = 'fb-head';
  head.textContent = source === 'held' ? 'Sent. Your teacher will read your answer and the feedback, then send it to you.'
    : source === 'teacher' ? 'Feedback from your teacher' : 'AI feedback (your teacher can see it)';
  box.append(head);
  if (source !== 'held') {
    for (const para of text.split(/\n{2,}/)) {
      const p = document.createElement('p');
      p.className = 'fb-text';
      p.textContent = para;
      box.append(p);
    }
  }
}
