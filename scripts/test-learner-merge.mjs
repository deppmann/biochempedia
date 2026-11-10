// Checks the learner sync merge rules (src/lib/learner-merge.mjs), which the worker and the
// browser share. Offline, no build needed: `node scripts/test-learner-merge.mjs`.
// The cases are the ones a signed-in learner can hit: undo a "done" tick, change or clear the
// path, and reset progress, each on one device while another device or the server holds the old state.
import assert from 'node:assert/strict';
import { mergeProgress } from '../src/lib/learner-merge.mjs';

const P = (x = {}) => ({ v: 1, lessons: {}, items: {}, ...x });
let n = 0;
const check = (name, fn) => { fn(); n++; console.log('  ok  ' + name); };
// The server merges (stored, incoming); the browser then merges (server reply, local). Run both.
const sync = (server, device) => { const s = mergeProgress(server, device); return { server: s, device: mergeProgress(s, device) }; };

check('a done mark still syncs up', () => {
  const r = sync(P(), P({ lessons: { a: { v: 10, d: 20 } } }));
  assert.equal(r.server.lessons.a.d, 20);
});
check('unticking done is not put back by the server', () => {
  const r = sync(P({ lessons: { a: { v: 10, d: 20 } } }), P({ lessons: { a: { v: 10, u: 30 } } }));
  assert.equal(r.server.lessons.a.d, undefined);
  assert.equal(r.device.lessons.a.d, undefined);
  assert.equal(r.server.lessons.a.u, 30);
});
check('ticking done again after an undo wins', () => {
  const r = sync(P({ lessons: { a: { v: 10, u: 30 } } }), P({ lessons: { a: { v: 10, d: 40 } } }));
  assert.equal(r.server.lessons.a.d, 40);
  assert.equal(r.server.lessons.a.u, undefined);
});
check('an older undo on another device does not remove a newer done mark', () => {
  const r = sync(P({ lessons: { a: { v: 10, d: 40 } } }), P({ lessons: { a: { v: 10, u: 30 } } }));
  assert.equal(r.device.lessons.a.d, 40);
});
check('records written before this change merge as they did', () => {
  const r = mergeProgress(P({ path: 'mcat', last: 'a', lessons: { a: { v: 10 } } }), P({ lessons: { a: { v: 5, d: 9 } }, items: { q: { l: 'a', n: 1, c: 1, t: 7 } } }));
  assert.deepEqual(r, { v: 1, path: 'mcat', last: 'a', lessons: { a: { v: 5, d: 9 } }, items: { q: { l: 'a', n: 1, c: 1, t: 7 } } });
  assert.equal(mergeProgress(P({ path: 'mcat' }), P({ path: 'degree' })).path, 'degree');
});
check('clearing the path is not put back by the server', () => {
  const r = sync(P({ path: 'mcat' }), P({ pathAt: 50 }));
  assert.equal(r.server.path, undefined);
  assert.equal(r.device.path, undefined);
});
check('the later path choice wins, whichever side holds it', () => {
  assert.equal(mergeProgress(P({ path: 'mcat', pathAt: 60 }), P({ path: 'degree', pathAt: 50 })).path, 'mcat');
  assert.equal(mergeProgress(P({ path: 'mcat', pathAt: 40 }), P({ path: 'degree', pathAt: 50 })).path, 'degree');
});
check('reset progress clears the synced copy and stays cleared', () => {
  const old = P({ path: 'mcat', last: 'a', lessons: { a: { v: 10, d: 20 }, b: { v: 15 } }, items: { q: { l: 'a', n: 2, c: 1, t: 25, s: 0, due: 99 } } });
  const r = sync(old, P({ reset: 100 }));
  assert.deepEqual(r.server, { v: 1, reset: 100, lessons: {}, items: {} });
  assert.deepEqual(r.device, { v: 1, reset: 100, lessons: {}, items: {} });
  // A second device that never heard of the reset syncs its old copy: still cleared.
  assert.deepEqual(sync(r.server, old).device, { v: 1, reset: 100, lessons: {}, items: {} });
});
check('work done after a reset is kept', () => {
  const r = sync(P({ reset: 100, lessons: { a: { v: 10, d: 20 } } }),
    P({ reset: 100, path: 'degree', pathAt: 120, last: 'c', lessons: { c: { v: 110, d: 130 } }, items: { q: { l: 'c', n: 1, c: 0, t: 125, s: 0, due: 999 } } }));
  assert.deepEqual(Object.keys(r.server.lessons), ['c']);
  assert.equal(r.server.path, 'degree');
  assert.equal(r.server.last, 'c');
  assert.ok(r.server.items.q);
});
check('merging is stable: a second pass changes nothing', () => {
  const a = P({ reset: 100, path: 'x', pathAt: 150, lessons: { a: { v: 110, u: 140 }, b: { v: 90, d: 160 } }, items: { q: { l: 'a', n: 1, c: 1, t: 130 } } });
  const b = P({ lessons: { a: { v: 105, d: 120 }, z: { v: 50, d: 60 } }, path: 'old' });
  const once = mergeProgress(a, b);
  assert.deepEqual(mergeProgress(once, b), once);
  assert.deepEqual(mergeProgress(a, once), once);
});
console.log(`${n} passed`);
