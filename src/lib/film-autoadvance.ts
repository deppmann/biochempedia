/* "Play all" on the film players (Chris, 2026-11-23/24: "Play all in playlist", "a next film button").
   One setting for the playlist run (/films/run/) and a course's play-in-order page (/films/play/<course>/):
   when it is on and a film the viewer started ends, the next one in the queue starts by itself. It is
   off until the viewer turns it on, and remembered on this device. Nothing starts until the viewer has
   pressed play once: the first film is never started by this setting, only the ones after it.
   Before this, the next film was always offered and never started by itself (ruling 2026-11-20); the
   offer is still what happens with the setting off, and when a browser refuses to start the next one. */

const KEY = 'biochempedia:films:playall:v1';

export function readPlayAll(): boolean {
  try { return localStorage.getItem(KEY) === '1'; } catch { return false; }
}

export function writePlayAll(on: boolean): void {
  try { if (on) localStorage.setItem(KEY, '1'); else localStorage.removeItem(KEY); } catch { /* storage blocked: this visit only */ }
}

/** Wire a checkbox to the setting; returns a getter for the current value. */
export function bindPlayAll(box: HTMLInputElement | null, onChange?: (on: boolean) => void): () => boolean {
  let on = readPlayAll();
  if (box) {
    box.checked = on;
    box.addEventListener('change', () => { on = box.checked; writePlayAll(on); onChange?.(on); });
  }
  // Another tab changed it.
  window.addEventListener('storage', (e) => { if (e.key === KEY) { on = readPlayAll(); if (box) box.checked = on; } });
  return () => on;
}
