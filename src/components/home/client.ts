/* The front door's script. Three small jobs, and the page is complete without any of them:
   1. old #tier-* links go to the catalog;
   2. the role choice: show that door, and keep the choice on this device when the visitor made it;
   3. "Welcome back": what this visitor was doing, from this device's own records. */
import { load, dueNow, onChange, lastLessonAt } from '../../lib/progress';
import { loadFilms, keepWatching, isWatched, onFilmsChange, resumeHref } from '../../lib/film-progress';
import { readPrefs, writePrefs, isRole, type Role } from '../../lib/prefs';
import { PATHS } from '../../data/paths';

// ---------------------------------------------------------------- 1. old anchors

/* The old homepage had #tier-* anchors. The catalog moved to /courses/, so send those hashes to
   the matching band there. */
const OLD_TIERS: Record<string, string> = {
  'tier-families': 'stage-ages-5-10',
  'tier-highschool': 'stage-grade-7',
  'tier-foundation': 'stage-starting-college',
  'tier-core': 'stage-college-core',
  'tier-elective': 'stage-college-further',
  'tier-advanced': 'research',
};
const oldTier = OLD_TIERS[location.hash.slice(1)];
if (oldTier) location.replace(`/courses/#${oldTier}`);

// ---------------------------------------------------------------- 2. the role choice

/* Which door an address asks for. A door's own address (#parents) wins; then an old link to an
   anchor inside the students' door; then ?role=. None of these is the visitor telling the site who
   they are, so none is saved: only a tap or a key press on the choice is. (The same order is in the
   small inline script in index.astro, which runs before the doors are drawn.) */
const DOOR: Record<string, Role> = { students: 'student', parents: 'parent', teachers: 'teacher' };
const STUDENT_ANCHORS = ['stage', 'courses', 'lessons', 'goals'];
const PLURAL: Record<Role, string> = { student: 'students', parent: 'parents', teacher: 'teachers' };
function asked(): Role | null {
  const h = location.hash.slice(1);
  if (DOOR[h]) return DOOR[h];
  if (STUDENT_ANCHORS.includes(h)) return 'student';
  try {
    const q = new URLSearchParams(location.search).get('role');
    if (isRole(q)) return q;
  } catch { /* no address to read */ }
  return null;
}

const radios = [...document.querySelectorAll<HTMLInputElement>('input[name="home-role"]')];
const doors = [...document.querySelectorAll<HTMLElement>('[data-door]')];
const said = document.querySelector<HTMLElement>('[data-home-said]');
const kept = document.querySelector<HTMLElement>('[data-home-kept]');

const current = (): Role => (radios.find((r) => r.checked)?.value as Role) ?? 'student';
function show(role: Role) {
  for (const r of radios) r.checked = r.value === role;
  // For browsers without :has(), where the stylesheet cannot hide the other two doors.
  for (const d of doors) d.hidden = d.dataset.door !== role;
}
show(asked() ?? readPrefs().role ?? current());

for (const r of radios) {
  r.addEventListener('change', () => {
    if (!r.checked) return;
    const role = r.value as Role;
    const first = !readPrefs().role;
    show(role);
    writePrefs({ role });
    try {
      const u = new URL(location.href);
      u.searchParams.set('role', role);
      u.hash = '';
      history.replaceState(null, '', u);
    } catch { /* the door still shows */ }
    /* Announced once per change; "Saved on this device" only the first time a choice is kept
       (and never when storage is blocked and nothing was). */
    const savedNow = first && readPrefs().role === role;
    if (said) said.textContent = `Showing the page for ${PLURAL[role]}.${savedNow ? ' Saved on this device.' : ''}`;
    if (kept) kept.hidden = !savedNow;
  });
}
addEventListener('hashchange', () => {
  const want = asked();
  if (!location.hash || !want || want === current()) return;
  show(want);
  document.getElementById(location.hash.slice(1))?.scrollIntoView();
});

// ---------------------------------------------------------------- 3. welcome back

/* The last lesson, an unfinished film or play-in-order queue, the review page and the chosen path,
   all from this device. Hidden on a first visit, without JavaScript, or with storage blocked. It says
   what the visitor was doing and never how much is left or due: those counts stay on /progress/ and
   /review/, the pages a person opens to see them. */
const box = document.querySelector<HTMLElement>('[data-resume]');
const text = document.querySelector<HTMLElement>('[data-resume-text]');
type Item = { at: number; label: string; href: string; meta?: string };
/* The newest unfinished film: a film stopped part-way, or a course's play-in-order queue. */
function filmItem(): Item | null {
  const r = loadFilms();
  const part = keepWatching(r);
  const q = Object.entries(r.q)
    .filter(([, x]) => x.title && !(isWatched(r, x.f) && x.t < 5))
    .sort((a, b) => b[1].at - a[1].at)[0];
  if (q && (!part || q[1].at >= part.at)) {
    const [course, x] = q;
    return { at: x.at, label: `Keep watching: ${x.title}`, href: `/films/play/${encodeURIComponent(course)}/`, meta: x.courseTitle ? `${x.courseTitle}, films in order` : 'films in order' };
  }
  if (!part) return null;
  return { at: part.at, label: `Keep watching: ${part.title}`, href: resumeHref(part), meta: part.course };
}
function draw() {
  if (!box || !text) return;
  const p = load();
  const due = dueNow(p).length;
  const path = PATHS.find((x) => x.id === p.path);
  const film = filmItem();
  text.textContent = '';
  if (!p.last && !path && !due && !film) { box.hidden = true; return; }
  box.hidden = false;
  let links = 0;
  const add = (it: Omit<Item, 'at'>) => {
    const a = document.createElement('a');
    a.href = it.href; a.textContent = it.label;
    if (links++) text.append(' · ');
    text.append(a);
    if (it.meta) text.append(Object.assign(document.createElement('span'), { className: 'home-resume-meta', textContent: ` (${it.meta})` }));
  };
  text.append('Welcome back. ');
  const recent: Item[] = [];
  if (p.last) recent.push({ at: lastLessonAt(p), label: 'Continue your last lesson', href: `/lessons/${p.last}/` });
  if (film) recent.push(film);
  recent.sort((a, b) => b.at - a.at).forEach(add);
  if (due) add({ label: 'Your review questions', href: '/review/' });
  if (path) add({ label: `Your path: ${path.label}`, href: `/paths/${path.id}/` });
}
onChange(draw);
onFilmsChange(draw);
