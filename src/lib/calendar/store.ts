/* The calendar's one storage key, and the way to clear it. Kept apart from the page's own
   script so that "Clear everything" on /progress/ and the account page's "remove from this
   device" can clear the calendar without loading it. */

export const CAL_KEY = 'stemhop:calendar:v1';
/** Fired on `window` after the calendar's record is cleared in this tab. */
export const CAL_EVENT = 'stemhop:calendar';

/** Forget everything the calendar keeps on this device: every plan, tick and done mark. */
export function clearCalendar(): void {
  try { window.localStorage.removeItem(CAL_KEY); } catch { /* nothing stored, or storage blocked */ }
  try { window.dispatchEvent(new CustomEvent(CAL_EVENT)); } catch { /* no window events */ }
}
