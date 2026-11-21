#!/usr/bin/env node
/**
 * The front door, checked in the built page (dist/index.html). Run after `npm run build`.
 *
 * It guards what older links and other pages rely on, and the promises the page makes:
 *  - the anchors old links point at (#stage, #courses, #lessons, #goals, #wip) and the three doors' addresses;
 *  - the role choice: three native radios in one group, Student checked by default, and the device key;
 *  - "Welcome back" present and hidden until the page's script fills it;
 *  - the hero search, the wordmark as the h1, and one link to the catalog in the page body;
 *  - no link to a feature that is switched off (the study planner, the AI syllabus page), and, while
 *    the calendar and the syllabus box are off, nothing of either on the page;
 *  - no count of what is left or due in the page or its script.
 */
import { readFile, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';

const FILE = 'dist/index.html';
if (!existsSync(FILE)) { console.error(`test-home: ${FILE} not found. Run "npm run build" first.`); process.exit(1); }
const html = await readFile(FILE, 'utf8');
const main = html.match(/<main[^>]*>([\s\S]*)<\/main>/)?.[1] ?? '';
const fails = [];
const ok = (cond, msg) => { if (!cond) fails.push(msg); };
const count = (re, s = main) => (s.match(re) ?? []).length;
const flags = await readFile('src/components/home/flags.ts', 'utf8');
const flagOn = (name) => new RegExp(`export const ${name} = true`).test(flags);

ok(main, 'the page has no <main>');
for (const id of ['stage', 'courses', 'lessons', 'goals', 'wip', 'students', 'parents', 'teachers']) {
  ok(count(new RegExp(`\\sid="${id}"`, 'g')) === 1, `anchor #${id} must appear exactly once in the page body`);
}
// The old anchors sit inside the students' door.
const students = main.match(/<section[^>]*id="students"[\s\S]*?<\/section>/)?.[0] ?? '';
for (const id of ['stage', 'courses', 'lessons', 'goals']) ok(students.includes(`id="${id}"`), `#${id} must be inside the students' door`);
ok(!students.includes('id="wip"'), '#wip must sit under every door, not inside one');

const radios = [...main.matchAll(/<input[^>]*type="radio"[^>]*>/g)].map((m) => m[0]).filter((r) => r.includes('name="home-role"'));
ok(radios.length === 3, `the role choice must be three radios named home-role (found ${radios.length})`);
ok(['student', 'parent', 'teacher'].every((v) => radios.some((r) => r.includes(`value="${v}"`))), 'the radios must be student, parent and teacher');
ok(radios.filter((r) => /\schecked/.test(r)).length === 1 && radios.some((r) => r.includes('value="student"') && /\schecked/.test(r)), 'Student must be the one radio checked by default');
ok(/<fieldset[^>]*>\s*<legend>I’m a<\/legend>/.test(main), 'the role choice must be a fieldset with the legend "I’m a"');
ok(main.includes("'stemhop:prefs:v1'"), 'the inline script must read the shared key stemhop:prefs:v1');
for (const role of ['student', 'parent', 'teacher']) ok(count(new RegExp(`data-door="${role}"`, 'g')) === 1, `there must be exactly one ${role} door`);

ok(/<p[^>]*data-resume[^>]*\shidden/.test(main), '"Welcome back" must be in the page and hidden until its script fills it');
ok(/<h1[^>]*id="home-h1"/.test(main) && /aria-label="STEMhop"|>STEMhop</.test(main.match(/<h1[\s\S]*?<\/h1>/)?.[0] ?? ''), 'the wordmark must be the page h1, named STEMhop');
ok(/role="search"[^>]*action="\/search\/"/.test(main) && main.includes('Search every lesson'), 'the hero must carry the search box, labelled "Search every lesson"');
ok(count(/href="\/courses\/"/g) === 1, `the page body must link the catalog (/courses/) exactly once (found ${count(/href="\/courses\/"/g)})`);
// Chris, 2026-11-21: his name is not on the homepage; the credit is on /contributors/ with everyone else.
ok(!main.includes('Deppmann') && main.includes('href="/contributors/"'), 'the homepage must not name its maker; it links /contributors/ instead');
for (const href of ['/play/', '/methods/', '/fun/']) ok(main.includes(`href="${href}"`), `Things to try must link ${href}`);
ok(/Open now/.test(main) && (main.match(/Coming</g) ?? []).length >= 4, 'Pick a subject must show Biology open and the coming subjects');

const site = await readFile('src/data/site-flags.ts', 'utf8');
const plannerOn = /export const PLANNER_TILE = true/.test(site);
for (const off of [...(plannerOn ? [] : ['/plan/']), '/teach/syllabus/', '/curious/']) ok(!main.includes(`href="${off}`), `the homepage must not link ${off} (off, or not what the page says it is)`);
if (!/export const IDEAS_LINK = true/.test(site)) ok(!html.includes('href="/ideas/"'), 'IDEAS_LINK is off, so no page chrome may link /ideas/');
// The choice is never written into the address by the page's own script when it could be saved instead.
ok(/autocomplete="off"/.test(radios.join('')), 'the role radios must not be restored by the browser (autocomplete="off")');
if (!flagOn('CALENDAR_LINK')) ok(!main.includes('/calendar/'), 'CALENDAR_LINK is off, so the page must not link the calendar');
if (!flagOn('SYLLABUS_BOX')) ok(!main.includes('<textarea'), 'SYLLABUS_BOX is off, so the page must not carry the syllabus box');
if (flagOn('SYLLABUS_BOX')) ok(!(await readFile('src/lib/syllabus-match.ts', 'utf8')).includes('return { ready: false }'), 'SYLLABUS_BOX is on but src/lib/syllabus-match.ts is still the unbuilt stub');

// Coming subjects are named, never links.
ok(!/href="\/(chemistry|physics|mathematics|psychology)/.test(main), 'a coming subject must not be a link');
// Calm: the homepage says what was done, never what is left or due.
const scripts = (await Promise.all((existsSync('dist/_astro') ? await readdir('dist/_astro') : [])
  .filter((f) => /^index\.astro.*\.js$|client.*\.js$/.test(f)).map((f) => readFile(`dist/_astro/${f}`, 'utf8')))).join('\n');
for (const [re, what] of [[/min left/, '"min left"'], [/questions? to review/, '"N questions to review"'], [/\bto go\b/, '"to go"']]) {
  ok(!re.test(main) && !re.test(scripts), `the homepage must not count what is left or due (${what})`);
}

if (fails.length) { console.error(`test-home: ${fails.length} problem(s)\n - ${fails.join('\n - ')}`); process.exit(1); }
console.log(`test-home: ok (3 doors, ${count(/<a\s/g)} links in the page body, old anchors in place).`);
