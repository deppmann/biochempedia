/* Web Audio bleeps — synthesized on the fly, no audio files. Muted by default-off
   is a design choice: sound is opt-OUT (starts on) but persists the user's choice.
   Everything degrades silently if Web Audio is unavailable. */

let ctx: AudioContext | null = null;
let muted = false;

const MUTE_KEY = 'bcp-arcade:muted';

export function initSound(): void {
  try {
    muted = localStorage.getItem(MUTE_KEY) === '1';
  } catch {
    muted = false;
  }
}

export function isMuted(): boolean {
  return muted;
}

export function setMuted(m: boolean): void {
  muted = m;
  try {
    localStorage.setItem(MUTE_KEY, m ? '1' : '0');
  } catch {
    /* ignore */
  }
}

function ac(): AudioContext | null {
  if (muted) return null;
  try {
    if (!ctx) {
      const AC = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      ctx = new AC();
    }
    if (ctx.state === 'suspended') void ctx.resume();
    return ctx;
  } catch {
    return null;
  }
}

/** One tone. freq in Hz, dur in seconds. */
function tone(freq: number, dur: number, type: OscillatorType, when = 0, gain = 0.09): void {
  const c = ac();
  if (!c) return;
  const t0 = c.currentTime + when;
  const osc = c.createOscillator();
  const g = c.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, t0);
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.exponentialRampToValueAtTime(gain, t0 + 0.012);
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
  osc.connect(g).connect(c.destination);
  osc.start(t0);
  osc.stop(t0 + dur + 0.02);
}

/** A little melody: [freq, startOffset, dur]. */
function melody(notes: Array<[number, number, number]>, type: OscillatorType = 'triangle'): void {
  for (const [f, s, d] of notes) tone(f, d, type, s);
}

export const sfx = {
  place: () => tone(440, 0.08, 'sine', 0, 0.06),
  correct: () => melody([[523.25, 0, 0.1], [659.25, 0.08, 0.12]]),
  streak: () => melody([[523.25, 0, 0.08], [659.25, 0.07, 0.08], [783.99, 0.14, 0.14]]),
  wrong: () => melody([[196, 0, 0.16], [155.56, 0.1, 0.2]], 'sawtooth'),
  tick: () => tone(880, 0.03, 'square', 0, 0.03),
  select: () => tone(587.33, 0.06, 'triangle', 0, 0.05),
  win: () =>
    melody(
      [
        [523.25, 0, 0.12],
        [659.25, 0.12, 0.12],
        [783.99, 0.24, 0.12],
        [1046.5, 0.36, 0.28],
      ],
      'triangle',
    ),
  lose: () => melody([[329.63, 0, 0.18], [293.66, 0.16, 0.18], [220, 0.34, 0.4]], 'sawtooth'),
};
