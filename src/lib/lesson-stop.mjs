/* Which stop a lesson opens on ("How long have you got?", src/components/LessonTime.astro).

   One function, written in plain old JavaScript with no imports, because it is used twice: the
   lesson page pastes its source into a small inline script that runs before the first paint (so a
   reader who chose "Films" never sees the whole lesson flash first), and scripts/test-lesson-time.mjs
   imports it to test the rules. Keep it self-contained: no outer names, no modern syntax.

   The rules, in order:
     1. A link to a place in the text (a #hash, a search result, a notebook link) opens the whole
        lesson. Nothing is saved.
     2. ?time=<stop> in the address opens that stop for this visit. Nothing is saved. This is the
        link a teacher sends to open a lesson at one length.
     3. A device that has joined a class opens the whole lesson: a saved choice must not quietly
        shorten assigned work.
     4. An ages 5 to 10 activity guide ignores a choice saved on a science lesson.
     5. The saved choice (stemhop:prefs:v1 "time"), or, where there is none, the choice once saved for
        this one lesson by the old three-way switch (stemhop:side-hops:view:<slug>). If this lesson
        has no such stop, the skim opens and the page says why; the saved choice is left as it is.
     6. Otherwise the whole lesson.

   in:  { stops: ['skim','stories','films','lesson'] (the ones this lesson has),
          hash: location.hash, search: location.search,
          saved: prefs.time or null, legacy: the old per-lesson value ('films' | 'hops') or null,
          inClass: boolean, guide: boolean }
   out: { stop, why }   why is '' or one of: remembered, noStories, noFilm, deepLink, inClass */
export function chooseStop(i) {
  var stops = i.stops || ['lesson'];
  var has = function (v) { return stops.indexOf(v) > -1; };
  var out = function (stop, why) { return { stop: has(stop) ? stop : 'lesson', why: why || '' }; };

  var saved = typeof i.saved === 'string' ? i.saved : null;
  if (!saved && i.legacy === 'films') saved = 'films';
  if (!saved && i.legacy === 'hops') saved = 'stories';
  if (['skim', 'stories', 'films', 'lesson'].indexOf(saved) < 0) saved = null;

  var asked = null;
  var m = /[?&]time=([a-z]+)/.exec(i.search || '');
  if (m && has(m[1])) asked = m[1];

  // What would have opened without rules 1, 3 and 4: used only to decide whether to explain.
  var shorter = asked ? asked !== 'lesson' : !!saved && saved !== 'lesson';

  var hash = i.hash || '';
  var deep = (hash && hash !== '#' && hash !== '#top' && hash !== '#explainer') || /[?&]pagefind-highlight=/.test(i.search || '');
  if (deep) return out('lesson', shorter ? 'deepLink' : '');
  if (asked) return out(asked, '');
  if (i.inClass) return out('lesson', shorter ? 'inClass' : '');
  if (i.guide) return out('lesson', '');
  if (saved && saved !== 'lesson') {
    if (has(saved)) return out(saved, 'remembered');
    if (has('skim')) return out('skim', saved === 'stories' ? 'noStories' : saved === 'films' ? 'noFilm' : '');
  }
  return out('lesson', '');
}
