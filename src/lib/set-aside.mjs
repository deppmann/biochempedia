/* Keeping two accounts' notes apart on one browser, without deleting anything.

   The notebook and progress live in this browser first and are synced to whichever learner
   account is signed in. When a DIFFERENT account signs in on the same browser (a family laptop, a
   shared computer, one person with two accounts), the server refuses to merge the first account's
   copy into the second (worker/learner.js, PUT /sync, 409). What happens to that copy is decided
   here, and the rule is: never delete it.

     - The two synced entries (notebook and progress) are MOVED to one set-aside entry, filed under
       the outgoing account's tag. AT MOST THREE accounts' notes are kept aside: when a fourth is
       set aside, the oldest of them is dropped for good. (The account page says so.) That is the
       one place where this file lets go of anything, and it bounds how much of other people's
       work a shared browser holds.
     - If the account now signed in has a set-aside copy of its own from an earlier visit, that copy
       is put back, so its unsynced work returns the moment it signs in here again.
     - Nothing else on the device is touched. The calendar's plan and the preferences belong to the
       device, not to an account, and stay exactly as they are.

   If the copy cannot be set aside (storage full or blocked), nothing is moved and nothing is
   removed, and the caller must not sync: the data stays where it is until the person signs out.

   Plain functions over a Storage-like object (in the browser, window.localStorage), so they run
   in the browser and in a Node test. */

export const ASIDE_KEY = 'stemhop:set-aside:v1';
export const ASIDE_MAX = 3;

/** { tag: { at, items: { key: stored text } } }, or {} when there is none or it is damaged. */
/** Remove everything set aside. For "clear this device": sign-out with that box ticked, "Clear everything", account deletion. */
export function clearAside(storage) {
  try { storage.removeItem(ASIDE_KEY); } catch { /* nothing stored, or storage blocked */ }
}

export function readAside(storage) {
  try {
    const o = JSON.parse(storage.getItem(ASIDE_KEY) ?? 'null');
    return o && typeof o === 'object' && !Array.isArray(o) ? o : {};
  } catch { return {}; }
}

/** True when this browser holds set-aside notes of an account other than `currentTag`. */
export function hasSetAside(storage, currentTag) {
  return Object.keys(readAside(storage)).some((tag) => tag !== currentTag);
}

/**
 * The account changed from `fromTag` to `toTag`. Move `keys` (the synced entries) out under `fromTag`
 * and put back whatever was set aside for `toTag`. Returns true when it is safe to sync as `toTag`;
 * false when nothing could be moved, in which case nothing was changed.
 */
export function switchAccount(storage, fromTag, toTag, keys, now = Date.now()) {
  let aside, items = {};
  try {
    aside = readAside(storage);
    for (const k of keys) { const v = storage.getItem(k); if (v !== null) items[k] = v; }
  } catch { return false; }
  const next = { ...aside };
  if (Object.keys(items).length) {
    // An earlier set-aside copy under the same tag is kept beside the new one, never overwritten.
    let tag = fromTag;
    for (let i = 2; next[tag]; i++) tag = `${fromTag}#${i}`;
    next[tag] = { at: now, items };
  }
  const coming = next[toTag];
  delete next[toTag];
  // Keep the newest few. The incoming account's own copy has just been taken out to be restored.
  const kept = Object.entries(next).sort((a, b) => (b[1]?.at ?? 0) - (a[1]?.at ?? 0)).slice(0, ASIDE_MAX);
  try {
    if (kept.length) storage.setItem(ASIDE_KEY, JSON.stringify(Object.fromEntries(kept)));
    else storage.removeItem(ASIDE_KEY);
  } catch { return false; }   // could not be set aside: leave everything where it is
  try {
    for (const k of keys) {
      const back = coming?.items?.[k];
      if (typeof back === 'string') storage.setItem(k, back); else storage.removeItem(k);
    }
  } catch {
    // Half-way is not acceptable: put the outgoing copy back and report failure.
    try { for (const [k, v] of Object.entries(items)) storage.setItem(k, v); storage.setItem(ASIDE_KEY, JSON.stringify(aside)); } catch { /* storage is failing; nothing more can be done */ }
    return false;
  }
  return true;
}
