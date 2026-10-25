/* Teacher classes, browser side. A student who joined a class on this device has
   an HttpOnly cookie the page can't read, plus this small non-secret marker in
   localStorage so pages know to report answers. Everyone else: no requests at all.

   Reports are fire-and-forget. A failed report never interrupts the lesson. */

const KEY = 'biochempedia:class:v1';

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
    else window.localStorage.removeItem(KEY);
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

export type AnswerKind = 'quiz' | 'idea' | 'cer' | 'done' | 'stuck';

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
