/* What the study helpers (worker/helper.js) know about a lesson, worked out at build time from the
   lesson source. Dependency-free, so the build endpoint (src/pages/helper-data/[slug].json.ts), the
   Worker's tests and the evaluation script all use the same code.

   The helpers are for learner accounts (13 and older). They are never offered on Biology Together
   (ages 5 to 10, written for the adult) or on grade 7 Life Science: no data file is built for those
   lessons, so the Worker refuses them even if a page asked. */

/** Course tiers and ladder steps the helpers are offered on. */
export function helperAllowed(course) {
  if (!course) return false;
  if (course.tier === 'families') return false;
  if (course.tier === 'highschool' && (course.ladderStep ?? 2) === 1) return false;   // grade 7 Life Science
  return true;
}

/** The level the lesson is written at, in words the model can aim for. */
export function levelLabel(course) {
  switch (course?.tier) {
    case 'highschool': return 'high school biology (grades 9 to 10)';
    case 'foundation': return 'first-year college biology';
    case 'core': return 'second-year college biology';
    case 'elective': return 'upper-level college course';
    case 'advanced': return 'advanced undergraduate or beginning graduate course';
    default: return 'college course';
  }
}

/** The id CER.astro gives a box with no id prop: the same hash of its task. Keep the two in step. */
export function cerUid(task, id) {
  if (id) return id;
  let h = 5381;
  for (let i = 0; i < task.length; i++) h = ((h * 33) ^ task.charCodeAt(i)) >>> 0;
  return `cer${h.toString(36)}`;
}

const attr = (tag, name) => {
  const m = new RegExp(`\\s${name}="([^"]*)"`).exec(tag);
  return m ? m[1] : undefined;
};

/** Every <CER .../> in a lesson body, with its id, task and model answer. Boxes without a model answer are left out. */
export function parseCers(body) {
  const out = [];
  for (const m of String(body ?? '').matchAll(/<CER\b([\s\S]*?)\/>/g)) {
    const tag = m[1];
    const task = attr(tag, 'task');
    const model = attr(tag, 'model');
    if (!task || !model) continue;
    out.push({ id: cerUid(task, attr(tag, 'id')), task, model });
  }
  return out;
}
