/* Learner accounts, browser side. The server half is worker/learner.js.

   An account is optional. Everything still lives in this browser's localStorage
   first (the notebook, src/lib/notebook.ts, and progress, src/lib/progress.ts);
   signing in only copies it to the server and back so the learner's devices agree.

   Sync: syncNow() sends this device's notebook and progress, the server merges them
   with what it holds (rules in learner-merge.mjs), sends the merged state back, and
   that is merged into this device. One request does pull, merge and push.
   Auto-sync, when signed in: once on page load (at most every 5 minutes), and 5 s
   after the notebook or progress changes.

   Whether to try at all comes from a readable cookie, bp_signed_in=1, that the server
   sets beside the real (HttpOnly) session cookie. It holds no secret. Signed-out
   visitors therefore make no account requests at all. */

import { startRegistration, startAuthentication } from '@simplewebauthn/browser';
import { loadNotebook, mergeItems, NOTEBOOK_KEY, NOTEBOOK_EVENT } from './notebook';
import { load as loadProgress, STORAGE_KEY as PROGRESS_KEY, CHANGE_EVENT as PROGRESS_EVENT, type Progress } from './progress';
import { mergeProgress, sameJson } from './learner-merge.mjs';

const CACHE_KEY = 'biochempedia:learner:v1';
export const LEARNER_EVENT = 'bp-learner';
const AUTO_MS = 5 * 60 * 1000;
const DEBOUNCE_MS = 5000;
const MAX_BYTES = 1024 * 1024;

export interface Me {
  signedIn: boolean;
  googleAvailable?: boolean;
  name?: string;
  email?: string;
  methods?: ('google' | 'passkey')[];
  passkeys?: number;
  created?: number;
  lastSynced?: number | null;
}

interface Cache { name?: string; lastSync?: number }

function readCache(): Cache {
  try { return JSON.parse(window.localStorage.getItem(CACHE_KEY) || '{}') || {}; } catch { return {}; }
}
function writeCache(c: Cache | null) {
  try {
    if (c) window.localStorage.setItem(CACHE_KEY, JSON.stringify(c));
    else window.localStorage.removeItem(CACHE_KEY);
  } catch { /* storage blocked */ }
  window.dispatchEvent(new CustomEvent(LEARNER_EVENT));
}

/** True when the server said this browser is signed in (no request needed). */
export function signedInHint(): boolean {
  try { return /(?:^|;\s*)bp_signed_in=1(?:;|$)/.test(document.cookie); } catch { return false; }
}

/** The name to show in the header, from the last /me answer on this device. */
export const cachedName = (): string | undefined => readCache().name;
export const lastSyncAt = (): number | undefined => readCache().lastSync;

async function api(path: string, init: RequestInit = {}): Promise<{ status: number; data: any }> {
  const res = await fetch(`/api/learner${path}`, {
    credentials: 'same-origin',
    ...init,
    headers: { ...(init.body ? { 'Content-Type': 'application/json' } : {}), ...(init.headers || {}) },
  });
  let data: any = null;
  try { data = await res.json(); } catch { /* not JSON */ }
  return { status: res.status, data };
}
const post = (path: string, body: unknown = {}) => api(path, { method: 'POST', body: JSON.stringify(body) });

export async function getMe(): Promise<Me> {
  try {
    const { status, data } = await api('/me');
    if (status !== 200 || !data) return { signedIn: false, googleAvailable: false };
    if (data.signedIn) writeCache({ ...readCache(), name: data.name });
    else if (readCache().name) writeCache(null);
    return data as Me;
  } catch {
    return { signedIn: false, googleAvailable: false };
  }
}

// ---- sync --------------------------------------------------------------------------
let applying = false;   // true while we write merged data, so our own events don't re-trigger a sync
let inFlight: Promise<SyncResult> | null = null;

export type SyncResult = { ok: true; at: number; changed: boolean } | { ok: false; status: number; error: string };

function writeProgress(p: Progress) {
  try { window.localStorage.setItem(PROGRESS_KEY, JSON.stringify(p)); } catch { return; }
  window.dispatchEvent(new CustomEvent(PROGRESS_EVENT));
}

export function syncNow(): Promise<SyncResult> {
  if (inFlight) return inFlight;
  inFlight = (async (): Promise<SyncResult> => {
    const localItems = loadNotebook().items;
    const localProgress = loadProgress();
    const body = JSON.stringify({ notebook: { items: localItems }, progress: localProgress });
    if (body.length > MAX_BYTES) return { ok: false, status: 413, error: 'Your notebook is too big to sync (over 1 MB).' };
    let r;
    try { r = await api('/sync', { method: 'PUT', body }); } catch { return { ok: false, status: 0, error: 'No connection. Your work is saved on this device.' }; }
    if (r.status === 401) { writeCache(null); return { ok: false, status: 401, error: 'Not signed in.' }; }
    if (r.status !== 200 || !r.data) return { ok: false, status: r.status, error: r.data?.error || 'Sync failed. Your work is saved on this device.' };

    // Merge the server's merged state into this device (another device may have added things).
    let changed = false;
    applying = true;
    try {
      changed = mergeItems(r.data.notebook?.items) || changed;
      const merged = mergeProgress(r.data.progress, loadProgress());   // this device's path/last win
      if (!sameJson(merged, loadProgress())) { writeProgress(merged as Progress); changed = true; }
    } finally { applying = false; }
    const at = Date.now();
    writeCache({ ...readCache(), lastSync: at });
    return { ok: true, at, changed };
  })();
  inFlight.finally(() => { inFlight = null; });
  return inFlight;
}

let started = false;
/** Called once per page by the header. Does nothing when signed out. */
export function startAutoSync() {
  if (started || !signedInHint()) return;
  started = true;
  if (!cachedName()) getMe();
  const last = lastSyncAt() ?? 0;
  if (Date.now() - last > AUTO_MS) syncNow();
  let timer: number | undefined;
  const soon = () => {
    if (applying || !signedInHint()) return;
    window.clearTimeout(timer);
    timer = window.setTimeout(() => { syncNow(); }, DEBOUNCE_MS);
  };
  window.addEventListener(NOTEBOOK_EVENT, soon);
  window.addEventListener(PROGRESS_EVENT, soon);
}

// ---- sign-in ------------------------------------------------------------------------
export type Outcome = { ok: true; name?: string } | { ok: false; error: string };

function passkeyError(e: unknown): string {
  const name = (e as { name?: string })?.name;
  if (name === 'NotAllowedError' || name === 'AbortError') return 'Cancelled, or the passkey prompt timed out.';
  if (name === 'InvalidStateError') return 'This device already has a passkey for this account.';
  if (name === 'NotSupportedError') return 'This browser cannot use passkeys.';
  return 'The passkey did not work. Please try again.';
}

export const passkeysSupported = () => typeof window !== 'undefined' && typeof window.PublicKeyCredential === 'function';

/** Make a passkey. Signed out: creates a new account with `displayName`. Signed in: adds one. */
export async function registerPasskey(displayName?: string, age13?: boolean): Promise<Outcome> {
  const o = await post('/passkey/register/options', { displayName, age13 });
  if (o.status !== 200) return { ok: false, error: o.data?.error || 'Could not start. Please try again.' };
  let response;
  try { response = await startRegistration({ optionsJSON: o.data.options }); } catch (e) { return { ok: false, error: passkeyError(e) }; }
  const v = await post('/passkey/register/verify', { response });
  if (v.status !== 200) return { ok: false, error: v.data?.error || 'The passkey could not be saved.' };
  writeCache({ ...readCache(), name: v.data.name });
  return { ok: true, name: v.data.name };
}

export async function signInWithPasskey(): Promise<Outcome> {
  const o = await post('/passkey/login/options');
  if (o.status !== 200) return { ok: false, error: o.data?.error || 'Could not start. Please try again.' };
  let response;
  try { response = await startAuthentication({ optionsJSON: o.data.options }); } catch (e) { return { ok: false, error: passkeyError(e) }; }
  const v = await post('/passkey/login/verify', { response });
  if (v.status !== 200) return { ok: false, error: v.data?.error || 'Sign-in failed.' };
  writeCache({ name: v.data.name });
  return { ok: true, name: v.data.name };
}

export const googleStartUrl = (ret = '/account/', age13 = false) =>
  `/api/learner/google/start?${new URLSearchParams({ return: ret, ...(age13 ? { age: '1' } : {}) })}`;

export const EXPORT_URL = '/api/learner/export';

/** Remove this device's own copy of the notebook and progress. */
export function clearDevice() {
  try { window.localStorage.removeItem(NOTEBOOK_KEY); window.localStorage.removeItem(PROGRESS_KEY); } catch { /* blocked */ }
  window.dispatchEvent(new CustomEvent(NOTEBOOK_EVENT));
  window.dispatchEvent(new CustomEvent(PROGRESS_EVENT));
}

export async function signOut(clearThisDevice = false): Promise<void> {
  try { await post('/logout'); } catch { /* offline: the cookie stays until next time */ }
  writeCache(null);
  if (clearThisDevice) clearDevice();
}

export async function deleteAccount(confirm: string): Promise<Outcome> {
  const r = await post('/delete', { confirm });
  if (r.status !== 200) return { ok: false, error: r.data?.error || 'Could not delete. Please try again.' };
  writeCache(null);
  return { ok: true };
}
