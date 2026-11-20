/* The hop graph: the words used to ask a model, in one place.

   The first fill (many readers, each given a batch of lessons) and the later single-lesson top-up
   (scripts/topic-graph/assign.mjs) use the same rules, the same examples and the same answer
   shapes, and every answer goes through the same validator (ingest.mjs). Each function returns a
   complete, self-contained prompt as a string.

     proposePrompt(digest, registry)        stage 1, one lesson: which ideas does it teach?
     proposeBatchPrompt(digests, registry)  stage 1 for a batch of lessons from one course
     canonicalizePrompt(proposals, registry) stage 2: one id per idea across all levels
     nearPrompt(area, registry)             stage 2b: sideways hops between ideas
     assignPrompt(digest, registry)         the top-up for one new or rewritten lesson
     verifyPrompt(concept, digests)         the blind check by a reader who did not write it

   Nothing here calls a model. */
import { digestText } from './digest.mjs';
import { AREAS, LIMITS } from './lib.mjs';

// ------------------------------------------------------------------ shared blocks

const SITE = `STEMhop (stemhop.com) is a free biology site. Its lessons run across seven levels:
  0 ages-5-10        hands-on activities; the page is written for the GROWN-UP who runs them with a child
  1 grade-7          middle school Life Science
  2 high-school      high school Biology
  3 starting-college the first college course
  4 college-core     the core courses of a biology degree
  5 college-further  one subject taken further
  6 graduate         courses built around current research

The site's main promise is "hopping": a learner on any lesson can go one level down to a simpler lesson on
the SAME IDEA, one level up to a deeper one, or sideways to a neighbouring idea. That needs one shared
graph of CONCEPTS. A concept is an idea a learner could ask for by name: "osmosis", "the action potential",
"natural selection". Its LADDER is the lessons that teach it, in level order; each rung carries a short note
on what that level adds. A wrong rung is worse than a missing one: a reader who hops down a level and lands
on a lesson about something else stops trusting the hop.`;

const ROLE_RULES = `ROLES. For each lesson and concept there are exactly three possibilities.

core   The lesson is a place to LEARN this idea at its level. The test, and it is strict:
       (a) the lesson has a section (a ## heading) whose subject is the idea itself, and
       (b) a reader arriving from the rung below would learn more ABOUT THAT IDEA there.
       The anchor is the test. If you cannot point at the section, it is not core.
uses   The lesson leans on the idea to teach something else, and you can name the section that leans on it.
       It does not re-teach it. Listed as "also comes up in", never shown on a ladder.
       At most ${LIMITS.usesPerProposal} per lesson. Most lessons have none or one. When in doubt, leave it out.
(none) Everything else, including PREREQUISITES. A lesson a student needs BEFORE an idea neither teaches
       that idea nor leans on it. "The resting membrane" comes before the action potential; it is not a rung
       of the action potential in either role. The site already has "before this" links for prerequisites.

Three cases come up again and again. Decide them this way.
- The specialised case. A graduate lesson on a division rigged to give two different daughter cells IS a
  core rung of "cell division": it has a section on the division itself and a reader coming up from the
  mitosis lesson learns something new about the same idea. A lesson that only mentions that cells divide is not.
- The lesson named "X and Y". It is two concepts with two anchors and usually two films. Do not invent a
  concept called "X and Y".
- The partner lesson (a lesson about the RELATION between two ideas). Make it core for the idea it adds
  something to, uses for the other, and mention the relation in "relations".

How many: 1 to ${LIMITS.corePerLesson} core concepts for a lesson. One or two is normal. A lesson that seems to be "about" five
things has not been read closely: find the one or two ideas its sections are built around.
College and graduate lessons are often built around a question or an experiment; ask "which idea would a
student one level below already know by name, and learn more about here?" If the honest answer is "none,
this idea is first taught here", then it is a new concept and that is fine: a ladder can be one rung, and
"no simpler version yet" is a true and useful thing for the site to say.`;

const CONCEPT_RULES = `WHAT COUNTS AS A CONCEPT.
- An idea with a name a learner could type: a process, a principle, a structure-and-what-it-does, a kind of
  evidence. Not a course topic ("cell biology"), not a skill ("reading graphs"), not a single fact, not one
  experiment (the experiment belongs in the note).
- The grain: about the size of one lesson section to one lesson at grade 7. "Osmosis" and "diffusion" are two
  concepts; "membrane transport" is too broad to be one; "aquaporins" is too narrow unless a whole lesson
  teaches it.
- An idea that SPLITS as it goes up (grade 7 teaches the cell cycle and mitosis together; college has one
  lesson for each) stays ONE concept while the lower rungs teach it together. The upper lessons sit on the
  same rung with different notes.
- Two ideas that young learners meet separately stay separate even if they merge higher up. "Adaptations"
  (ages 5 to 10 and grade 7) and "natural selection" are two concepts joined by a sideways hop, because a
  child who asks "why do birds have different beaks" should land on adaptations.
- REUSE. If the idea is already in the registry below, use that id exactly. A new id for an idea that
  already has one breaks the ladder in two. Create a new concept only when no registry concept is this idea.
- A new concept needs: an id (kebab-case, the plainest name of the idea, for example "nitrogen-cycle"),
  a name (as a learner would say it; a technical term may follow in brackets), a blurb, an area, and aliases.`;

const BLURB_RULES = `THE BLURB (new concepts only) is one sentence of at most ${LIMITS.blurbWords} words that says what the idea IS, in words a
grade 7 reader knows. Example: "Water moves across a membrane toward the side with more dissolved stuff."
It states the idea; it does not describe the lessons.`;

const NOTE_RULES = `THE NOTE ("adds") on every core rung is reader-facing copy: it tells a reader deciding whether to hop what
THIS lesson adds at THIS level.
- At most ${LIMITS.addsWords} words.
- It names the lesson's own case, experiment or number. Good notes: "Water drifts to the saltier side: weigh
  cucumber slices and see." "Fast across a cell, hopeless across a body: time grows with distance squared."
  "The test: add NGF, take it away, and count which neurons live."
- It must NOT be writable from the title alone. "Covers osmosis in more detail", "An introduction to
  diffusion", "Explores the action potential" are failures and are rejected by the checker.
- Pitch the words at that rung's own reader: plain verbs for a twelve-year-old, the real terms ("Km and
  Vmax") at college.
- For an ages-5-10 activity the reader is the grown-up, so the note describes the activity: "Stand celery in
  blue water and watch the colour climb to the leaves."
- When two lessons teach the same idea at the same level, each note says what that lesson adds that the
  other does not.
- Every number or name in a note must be in the lesson. If the digest does not show it, open the lesson.`;

const ANCHOR_RULES = `THE ANCHOR on a core rung is the id of the ## section that teaches the idea, copied exactly from the square
brackets in the digest. One anchor, the section where a reader should land. Use null only when the idea is
truly spread across the whole lesson. On ages-5-10 activities every page has the same eight headings and the
only useful anchor is "the-big-idea". Prefer an id made of plain ASCII letters.`;

const FILM_RULES = `FILMS are chosen per concept, not inherited from the lesson. List only the films of this lesson that SHOW
this idea, judged by the film's title and take-homes. A lesson cut into six films usually has one or two
that show a given concept; a second film often belongs to the lesson's other concept. An ages-5-10 "Set Up"
film shows the grown-up how to run the activity: list it for the activity's core concept. A uses rung has
no films. Copy film keys exactly.`;

const ALIAS_RULES = `ALIASES (new concepts need ${LIMITS.aliasMin} to ${LIMITS.aliasMax}) are what a person would really type when this idea is the answer.
Two kinds are both wanted: the everyday question ("where does the wood in a tree come from") and the school
term or other name ("Punnett squares", "apoptosis").
- Every alias must be FACTUALLY this idea. Check each one. "Why do my fingers wrinkle in the bath" sounds
  like osmosis and is not (it is a nerve response), so it is not an osmosis alias. A wrong alias sends a
  curious reader to the wrong page, and no word check will catch it.
- Not another concept's name, and not a phrase that fits another concept as well as this one.
- Lower case unless it is a proper name or an abbreviation. No question mark. At most ${LIMITS.aliasWords} words.
- Never a request for medical advice (no doses, symptoms, treatments, "should I"), never a brand or product.`;

const VOICE = `VOICE for every string a reader will see (names, blurbs, notes, aliases, reasons): plain, concrete and
calm, the way a good teacher talks to one student. No hype ("amazing", "fascinating"). No dashes used as
punctuation (no em-dash, no en-dash): use a colon, a comma or a second sentence. No emojis. No brand,
product, company, exam or test-preparation names. Nothing phrased as medical advice. No analogy formulas
("X is like Y", "mirrors", "parallels", "by contrast", "the same logic as"): say what happens, or name a real
case. Follow the spelling of the lesson you are describing.`;

const AREA_LIST = `AREAS. Each concept sits on exactly one shelf (for browsing; the sideways hops carry the crossings):
${AREAS.map((a) => `  ${a.id.padEnd(18)} ${a.name}`).join('\n')}
Hard calls: put an idea where a learner would look for it first. Cell death sits in cells; immunity has its
own shelf; a method or a kind of evidence ("how we know") goes in methods only when the idea IS the method.`;

const EXAMPLES = `THREE WORKED EXAMPLES (real lessons, real answers).

Example 1, a school idea. Lesson diffusion-and-osmosis (grade 7, "Diffusion and Osmosis").
The title names two ideas, the lesson has one "Explain" section for each, and it has two films.
  { "id": "diffusion", "role": "core", "anchor": "explain-particles-spread-from-more-to-less",
    "adds": "Random moves add up to a one-way drift from crowded to empty.",
    "films": ["diffusion-and-osmosis/explainer"] }
  { "id": "osmosis", "role": "core", "anchor": "explain-water-crosses-a-choosy-membrane",
    "adds": "Water drifts to the saltier side: weigh cucumber slices and see.",
    "films": ["diffusion-and-osmosis/chapter-2"] }
Each film went to the concept its take-homes are about. The objectives mention homeostasis in passing; no
section teaches it or leans on it, so it is not listed at all.
A trap next door: the ages-5-10 activity thirsty-celery has a hand-written link up to this lesson, but the
activity shows water climbing a stem, which is a different idea (how water moves through a plant). It is NOT
a rung of osmosis. Hand-written ladder links are hints about the neighbourhood, not proof of "same idea".

Example 2, a body-and-brain idea. Lesson action-potential (college-further, "The Action Potential and Conduction").
The whole lesson is this one idea, so it has one core concept. It has six films; two show the idea as a whole.
  { "id": "action-potential", "role": "core", "anchor": "how-three-gates-make-one-spike",
    "adds": "Sodium in, potassium out: how three gates make one spike.",
    "films": ["action-potential/explainer", "action-potential/three-gates"] }
Around it: resting-membrane-passive is what a student needs first. It neither teaches the spike nor leans on
it, so it gets NO rung for this concept. synaptic-transmission starts from an arriving spike to teach release
at the synapse: uses. myelination (graduate) has a section "Why wrap an axon" on how the wrap makes the
signal jump, and a reader coming up from this lesson learns more about the spike there: core (the
specialised case), with the note "Why wrapping an axon makes the signal jump, and who decides the wrap."
This ladder starts at high school and has no rung below it. That is true, so it stays that way.

Example 3, an idea at one level only. Lesson neurotrophic-hypothesis (graduate, "The Neurotrophic Hypothesis Tested").
  { "id": "nerve-growth-factor", "role": "core", "anchor": "add-it-take-it-away",
    "adds": "The test: add NGF, take it away, and count which neurons live.",
    "films": ["neurotrophic-hypothesis/explainer"] }
Three graduate lessons in two courses teach this idea (the discovery, the test, the receptors) and nothing
below graduate level does. It is still a concept: a learner can ask for it by name, and its three notes say
what each lesson adds that the others do not. naturally-occurring-death teaches why embryos make too many
neurons and leans on the survival signal to explain who lives: core for cell-death, uses for nerve-growth-factor.`;

const READING = `HOW TO READ. Each lesson comes as a DIGEST: where it sits, its hook, summary and objectives, every ##
section with its anchor id, how the section opens and the sentences that carry its numbers, the lesson
explained at other levels, each film's key, title and take-homes, and the links already on the page.
The digest is enough for most lessons. OPEN THE LESSON FILE (its path is in the digest) when:
- the digest says to ("Open the full text before deciding");
- you cannot tell from the section openings whether a section teaches an idea or only leans on it;
- you need a case, an experiment or a number for a note and the digest does not show one;
- you are about to create a new concept (read the section first).
Do not guess. If after reading you are still unsure a rung is core, it is not core.`;

// ------------------------------------------------------------------ the registry as text

/** The registry block: one line per concept. `full` adds aliases. */
export function registryText(registry, { full = false } = {}) {
  if (!registry.length) return '(the registry is empty)';
  const byArea = new Map();
  for (const c of registry) (byArea.get(c.area) ?? byArea.set(c.area, []).get(c.area)).push(c);
  const L = [];
  for (const a of AREAS) {
    const mine = (byArea.get(a.id) ?? []).slice().sort((x, y) => x.id.localeCompare(y.id));
    if (!mine.length) continue;
    L.push(`[${a.id}] ${a.name}`);
    for (const c of mine) {
      L.push(`  ${c.id} | ${c.name} | ${c.blurb} | taught at: ${c.levels.length ? c.levels.join(', ') : 'nowhere yet'}${c.lessons?.length ? ` (${c.lessons.join(', ')})` : ''}`);
      if (full && c.aliases?.length) L.push(`      also asked as: ${c.aliases.join('; ')}`);
    }
  }
  return L.join('\n');
}

const existingText = (existing) => {
  if (!existing?.length) return '';
  return `THIS LESSON ALREADY HAS A RECORD in the graph:
${existing.map((e) => `  ${JSON.stringify(e)}`).join('\n')}
Return these entries unchanged unless reading the lesson shows one is wrong (then leave it out or correct it,
and say why in "notes"). Then add any idea the lesson teaches that the record misses.`;
};

// ------------------------------------------------------------------ stage 1: propose

const PROPOSAL_SHAPE = `{
  "lesson": "<slug>",
  "hash": "<the content hash printed on the digest's first line, copied exactly>",
  "opened_lesson": true or false,
  "concepts": [
    {
      "id": "<registry id, or a new kebab-case id>",
      "new": { "name": "...", "blurb": "...", "area": "<area id>", "aliases": ["...", "..."] },
      "role": "core" or "uses",
      "anchor": "<section id>" or null,
      "adds": "<the note, at most ${LIMITS.addsWords} words>",
      "films": ["<film key>", ...],
      "aliases": ["<optional: 0 to 2 more everyday phrases for an EXISTING concept that this lesson suggests>"],
      "why": "<one sentence for the checker, not for readers: which section teaches or leans on it>"
    }
  ],
  "relations": [ { "a": "<concept id>", "b": "<concept id>", "note": "<how this lesson ties the two ideas>" } ],
  "notes": "<anything the next reader should know: a record you changed and why, an idea with no clean home>"
}
Rules of the shape:
- "new" appears ONLY when the id is not in the registry, and then it is required in full. Define a new
  concept once, in the first lesson that needs it; later lessons in your batch reuse the id without "new".
- core entries carry "anchor" (or null), "adds" and "films" (possibly empty). uses entries carry none of the three.
- "relations" and "notes" may be empty ([] and ""). "concepts" may be empty only for a page that teaches no
  idea at all (say why in "notes").
- Return JSON only: no commentary before or after, no trailing commas, straight double quotes.`;

/** Stage 1 for one lesson. `opts.existing` is the lesson's current record as proposal entries. */
export function proposePrompt(digest, registry, opts = {}) {
  return `You are reading one lesson of STEMhop to decide which ideas it teaches, so the site can connect it to the
lessons on the same ideas at other levels.

${SITE}

${ROLE_RULES}

${CONCEPT_RULES}

${BLURB_RULES}

${NOTE_RULES}

${ANCHOR_RULES}

${FILM_RULES}

${ALIAS_RULES}

${AREA_LIST}

${VOICE}

${EXAMPLES}

${READING}

THE REGISTRY (concepts that already exist: id | name | what it is | where it is taught). Reuse these ids.
${registryText(registry)}

${existingText(opts.existing)}

THE LESSON
${digestText(digest)}

YOUR ANSWER is one JSON object of exactly this shape:
${PROPOSAL_SHAPE}
`.replace(/\n{3,}/g, '\n\n');
}

/**
 * Stage 1 for a batch of lessons from one course, read by one reader who keeps the course in mind.
 * opts: { existingBySlug, courseMap (text: every lesson of the course, one line each), answerDir, batch }
 */
export function proposeBatchPrompt(digests, registry, opts = {}) {
  const slugs = digests.map((d) => d.slug);
  return `You are reading ${digests.length} lesson(s) of one STEMhop course to decide which ideas each one teaches, so the
site can connect each lesson to the lessons on the same ideas at other levels. Do them one at a time, in the
order given, and keep the whole course in mind so the same idea gets the same id in every lesson.

${SITE}

${ROLE_RULES}

${CONCEPT_RULES}

${BLURB_RULES}

${NOTE_RULES}

${ANCHOR_RULES}

${FILM_RULES}

${ALIAS_RULES}

${AREA_LIST}

${VOICE}

${EXAMPLES}

${READING}
${opts.root ? `Lesson file paths are relative to ${opts.root}. ` : ''}Read only: change no file except your answer files.

THE REGISTRY (concepts that already exist: id | name | what it is | where it is taught). Reuse these ids.
Other readers are working on other courses at the same moment and cannot see your new ids, so name a new
concept by the plainest name of the idea (another reader who meets the same idea should arrive at the same
id). A later step merges duplicates.
${registryText(registry)}

${opts.courseMap ? `THE WHOLE COURSE, for orientation (you are answering only for the lessons listed after it):\n${opts.courseMap}\n` : ''}
YOUR ANSWER: for EACH lesson write one file ${opts.answerDir ?? '<staging>/proposals'}/<slug>.json holding one JSON object of exactly this shape:
${PROPOSAL_SHAPE}
Write exactly these files and nothing else: ${slugs.map((s) => `${s}.json`).join(', ')}.
When all are written, reply with one line per lesson: the slug, its core ids, its uses ids, and whether you opened the file.

THE LESSONS
${digests.map((d) => `${'='.repeat(100)}\n${existingText(opts.existingBySlug?.[d.slug])}\n${digestText(d)}`).join('\n\n')}
`.replace(/\n{3,}/g, '\n\n');
}

// ------------------------------------------------------------------ stage 2: canonicalize

const CANONICAL_SHAPE = `{
  "area": "<the area id you were given>",
  "concepts": [
    {
      "id": "<the one id for this idea: an existing registry id when the idea is already there, else the plainest kebab-case name>",
      "merge": ["<every proposed id that is this idea, including the id itself when it was proposed>"],
      "name": "...", "blurb": "...", "area": "<area id>", "aliases": ["...", "..."]
    }
  ],
  "drop": [ { "id": "<proposed id>", "why": "<one sentence: not an idea a learner could ask for by name, or too broad, or a single fact>" } ],
  "rungs": [ { "id": "<final concept id>", "lesson": "<slug>", "role": "uses" or "drop", "adds": "<a replacement note>", "why": "<one sentence>" } ],
  "notes": "<calls you were unsure of, for the person who reads the report>"
}
Rules of the shape:
- EVERY new id listed under "PROPOSALS" must appear exactly once: in one concept's "merge" list, or in "drop".
  An id you keep as it is still needs an entry: { "id": "x", "merge": ["x"] }.
- For a concept whose id is already in the registry, give "name", "blurb", "area" and "aliases" ONLY if you
  mean to change them; leave them out to keep what is there. For a new id all four are required.
- "rungs" is for the few rungs that the merge makes wrong or unclear. Give "role": "uses" to demote a rung
  that leans on the merged idea but does not teach it, "role": "drop" to remove one, or only "adds" to
  replace a note (when two lessons at one level now sit on the same rung and their notes blur). Leave it
  empty when the proposals stand.
- Return JSON only.`;

/**
 * Stage 2 for one area. `areaProposals` = { area, proposed: [{ id, defs: [{ name, blurb, area, aliases, by }], rungs: [{ lesson, title, stage, rank, role, adds, anchor, why }] }], existing: [...same shape for registry concepts that received rungs] }
 */
export function canonicalizePrompt(areaProposals, registry, opts = {}) {
  const cross = areaProposals.area === '_cross';
  const block = (p) => {
    const L = [`${p.id}${p.inRegistry ? '   (already in the registry)' : ''}`];
    for (const d of p.defs ?? []) L.push(`    defined as: "${d.name}" | ${d.blurb} | area ${d.area} | aliases: ${(d.aliases ?? []).join('; ')}${d.by ? `   [from ${d.by}]` : ''}`);
    for (const r of p.rungs ?? []) L.push(`    ${r.role === 'core' ? 'CORE' : 'uses'}  ${r.stage.padEnd(16)} ${r.lesson} ("${r.title}")${r.role === 'core' ? `  [#${r.anchor ?? '-'}]  note: ${r.adds}` : ''}${r.why ? `   why: ${r.why}` : ''}`);
    return L.join('\n');
  };
  return `You are merging proposals into STEMhop's graph of ideas. Readers went through the lessons course by course and,
for each lesson, named the ideas it teaches. Each reader saw the registry but not the other readers' new ids,
so the same idea may have arrived under several ids, at several levels. Your job${cross ? ' in this pass is to look ACROSS all areas' : ` for the area "${areaProposals.area}"`} is to give
each idea exactly one id, and to keep different ideas apart.

${SITE}

${CONCEPT_RULES}

MERGE when two proposed ids are one idea a learner would ask for by one name, even if the levels are far apart
and the words differ ("why leaves are green" at ages 5 to 10 and "light-harvesting pigments" at college can
be one concept if the lower lesson really teaches that idea). Merging is what builds a ladder across levels:
look hardest at proposals from DIFFERENT levels.
KEEP APART when a learner would see two questions. Ideas that are neighbours, a part and its whole, or a
cause and its effect are two concepts joined later by a sideways hop. "Adaptations" and "natural selection"
stay two; "diffusion" and "osmosis" stay two; "what counts as alive" at three levels turned out to be three
different questions and stayed three.
An idea that splits as it goes up stays one concept while the lower rungs teach it together.
DROP a proposal that is not a concept: a course topic, a skill, a single fact, one experiment.
A concept taught by a single lesson is allowed and common. Do not merge just to make ladders longer:
a wrong rung is worse than a missing one.
${cross ? 'In this pass every id below is already a concept. Look only for the SAME idea filed under two ids in different areas (for example a signal filed once under signaling and once under development). Most ids need no change: list ONLY the concepts you merge; ids you do not mention are kept as they are (the "every id must appear" rule does not apply to this pass).' : `If a proposal clearly belongs on another shelf, set its "area" to that area; it stays in your answer.`}

When you write or change a name, blurb or alias:
${BLURB_RULES}

${ALIAS_RULES}

${AREA_LIST}

${VOICE}

THE REGISTRY (every concept that already exists, all areas):
${registryText(registry)}

${cross ? 'Every concept is in the registry above; there is no separate list for this pass.' : `PROPOSALS filed under "${areaProposals.area}" (each NEW id, how its proposers defined it, and the lessons proposed for it, lowest level first):
${areaProposals.proposed.map(block).join('\n\n') || '(none)'}

ALREADY IN THE REGISTRY on this shelf, with the lessons now on each (these are the first places to look for a
merge target; you may also fix one of their rungs under "rungs"; they need no entry of their own otherwise):
${(areaProposals.existing ?? []).map(block).join('\n\n') || '(none)'}`}

${opts.digestDir ? `If you need to see a lesson to decide, its digest is at ${opts.digestDir}/<slug>.json.\n` : ''}
YOUR ANSWER is one JSON object of exactly this shape${opts.answerFile ? `, written to ${opts.answerFile}` : ''}:
${CANONICAL_SHAPE}
`.replace(/\n{3,}/g, '\n\n');
}

// ------------------------------------------------------------------ stage 2b: sideways hops

const NEAR_SHAPE = `{
  "area": "<the area id you were given>",
  "near": {
    "<concept id>": [ { "id": "<another concept's id>", "why": "<one sentence, at most ${LIMITS.whyWords} words>" } ]
  }
}
Rules of the shape:
- One entry for EVERY concept listed under "CONCEPTS TO WRITE FOR", each with 1 to ${LIMITS.nearMax} hops (2 or 3 is usual).
- A concept that already has hops is shown with them: return them unchanged unless one is wrong, and add
  only if a clearly better neighbour now exists.
- Ids copied exactly from the registry. Never a hop to itself. Return JSON only.`;

/** Stage 2b for one area: `concepts` = registry rows to write for (with `.near` when they have some), `hints` = relations noted by lesson readers. */
export function nearPrompt(area, concepts, registry, opts = {}) {
  return `You are writing the SIDEWAYS HOPS of STEMhop's graph of ideas: from one idea, the one to four neighbouring
ideas a curious reader would want next, each with a one-sentence reason.

${SITE}

A SIDEWAYS HOP goes from the idea the reader is on to a DIFFERENT idea. Write the reason from the reader's
side: "you are on osmosis; why go to diffusion?" So the hop from A to B and the hop from B to A have different
sentences; write both when both are worth having, but symmetry is not required.
- The reason names a shared mechanism or a real case. Good: "The same random motion, without the membrane's
  rule about who may cross." (osmosis to diffusion) "A synapse is a gap narrow enough for diffusion to be fast."
  (diffusion to synapse) "Rebuilding a body means removing old cells as well as adding new ones."
  (metamorphosis to cell death).
- No analogy formulas: not "is like", "mirrors", "parallels", "by contrast", "the same logic as". The natural
  sentence from immunity to natural selection is a comparison; the right one names a real case, antibiotic
  resistance.
- Not a prerequisite chain and not "is related to". If you cannot say what joins the two in one concrete
  sentence, it is not a hop.
- Hops may and should cross areas: about half of the good ones do. Look through the WHOLE registry.
- One sentence, at most ${LIMITS.whyWords} words, in words a reader at the concept's LOWEST level understands.

${VOICE}

THE REGISTRY (every concept; hop only to ids in this list):
${registryText(registry)}

${opts.hints?.length ? `RELATIONS noticed by the readers of the lessons (hints, not all worth a hop):\n${opts.hints.map((h) => `  ${h.a} <-> ${h.b}: ${h.note}   [${h.by}]`).join('\n')}\n` : ''}
CONCEPTS TO WRITE FOR (area "${area}"):
${concepts.map((c) => `  ${c.id} | ${c.name} | ${c.blurb} | taught at: ${c.levels.join(', ')}${c.near?.length ? `\n      has: ${c.near.map((n) => `${n.id} ("${n.why}")`).join('; ')}` : ''}`).join('\n')}

YOUR ANSWER is one JSON object of exactly this shape${opts.answerFile ? `, written to ${opts.answerFile}` : ''}:
${NEAR_SHAPE}
`.replace(/\n{3,}/g, '\n\n');
}

// ------------------------------------------------------------------ the single-lesson top-up

/** The top-up for one new or rewritten lesson: the same rules as stage 1, with the full registry. */
export function assignPrompt(digest, registry, opts = {}) {
  return `A lesson of STEMhop is new or was rewritten. Decide which ideas it teaches so it joins the site's graph of
ideas. The registry below is the whole graph: almost every idea this lesson teaches is already in it.

${SITE}

${ROLE_RULES}

${CONCEPT_RULES}
For this top-up there is no later merging step: a new concept you create goes into the graph as you wrote
it. Create one only when you have read the registry's lines for that area and no concept there is this idea.

${BLURB_RULES}

${NOTE_RULES}
Look at the notes already on the concept's other rungs (shown below when the lesson joins an existing
ladder): yours must say what THIS lesson adds that they do not.

${ANCHOR_RULES}

${FILM_RULES}

${ALIAS_RULES}

${AREA_LIST}

${VOICE}

${EXAMPLES}

${READING}

THE REGISTRY (id | name | what it is | where it is taught). Reuse these ids.
${registryText(registry, { full: true })}

${opts.ladders?.length ? `LADDERS THIS LESSON MAY JOIN (the notes already written, lowest level first):\n${opts.ladders.map((c) => `  ${c.id}:\n${c.rungs.map((r) => `      ${r.stage.padEnd(16)} ${r.lesson}: ${r.adds}`).join('\n')}`).join('\n')}\n` : ''}
${existingText(opts.existing)}

THE LESSON
${digestText(digest)}
${opts.body ? `\nTHE LESSON TEXT\n${opts.body}\n` : ''}
YOUR ANSWER is one JSON object of exactly this shape:
${PROPOSAL_SHAPE}
One addition for this top-up. If you created a NEW concept, add a top-level field
  "near": { "<the new id>": [ { "id": "<an existing concept's id>", "why": "<one sentence, at most ${LIMITS.whyWords} words>" } ] }
with 1 to 3 sideways hops: the neighbouring ideas a curious reader would want next. Write each reason from
the reader's side ("you are on this idea; why go there?"), naming a shared mechanism or a real case, never an
analogy formula and never "is related to".
`.replace(/\n{3,}/g, '\n\n');
}

// ------------------------------------------------------------------ the blind check

const VERIFY_SHAPE = `{
  "concept": "<the concept id>",
  "ticket": "<the ticket printed above, copied exactly>",
  "same_idea": true or false,
  "rungs": [
    { "lesson": "<slug>", "verdict": "ok" },
    { "lesson": "<slug>", "verdict": "note", "adds": "<your replacement note, at most ${LIMITS.addsWords} words>", "why": "<what was wrong with the note>" },
    { "lesson": "<slug>", "verdict": "not-core", "why": "<one sentence>" },
    { "lesson": "<slug>", "verdict": "wrong", "why": "<one sentence>" }
  ],
  "bad_anchors": ["<slug of a core rung whose anchor section is not where the idea is taught>"],
  "bad_films": [ { "film": "<film key>", "why": "<one sentence>" } ],
  "bad_aliases": [ { "alias": "<the phrase>", "why": "<one sentence: what it really is>" } ],
  "notes": "<anything else the person reading the report should know>"
}
Rules of the shape:
- One entry in "rungs" for EVERY core rung listed, with exactly one verdict:
    ok        the lesson has a section on this idea and a reader from the rung below learns more about it there
    note      the rung is right but its note is wrong, vague, or could be written from the title; you supply a better one
    not-core  the lesson leans on the idea but does not teach it (it becomes "also comes up in")
    wrong     the lesson is about a different idea, or is only a prerequisite; the rung is removed
- "same_idea" is false when the rungs do not all teach one idea; then mark the rungs that do not belong "wrong".
- The lists may be empty. Return JSON only.`;

/**
 * The blind check of one concept. `concept` = { id, name, blurb, aliases, ticket, rungs: [{ lesson, role, stage, title, anchor, adds }], films: [{ key, title, lesson }] }.
 * `digests` = Map or object of slug -> digest for every core rung's lesson.
 */
export function verifyPrompt(concept, digests, opts = {}) {
  const get = (slug) => (digests instanceof Map ? digests.get(slug) : digests[slug]);
  const core = concept.rungs.filter((r) => r.role === 'core');
  return `You are checking one entry of STEMhop's graph of ideas. You did not write it. Someone claims that the lessons
below all teach ONE idea, at different levels, and that each is a place to learn it. Readers will follow these
links to hop down to a simpler lesson or up to a deeper one, so a wrong link costs their trust: a wrong rung
is worse than a missing one. Judge from the lessons, not from the claim. Do not be generous.

${SITE}

${ROLE_RULES}

Expect to disagree most often on the specialised case. Apply the rule as written: core if the lesson has a
section whose subject is the idea itself AND a reader arriving from the rung below would learn more about
that idea there. A section on a special form of the idea passes; a lesson that only assumes the idea does not.

${NOTE_RULES}

${ALIAS_RULES}

${FILM_RULES}

${VOICE}

THE CLAIM
Concept: ${concept.id}   (ticket ${concept.ticket})
Name: ${concept.name}
What it is: ${concept.blurb}
Also asked as: ${(concept.aliases ?? []).join('; ') || '(none)'}
Core rungs, lowest level first (lesson | level | anchor | note):
${core.map((r) => `  ${r.lesson} | ${r.stage} | ${r.anchor ? `#${r.anchor}` : '(no anchor)'} | ${r.adds}`).join('\n')}
Films said to show the idea: ${(concept.films ?? []).map((f) => `${f.key} ("${f.title}")`).join('; ') || '(none)'}

FOR EACH CORE RUNG, in order:
1. Find the anchor's section in the lesson's digest. Is its subject this idea?
2. Would a reader who knows the rung below learn more about THIS idea here? (For the lowest rung: is it a
   place to meet the idea for the first time?)
3. Is the note true to the lesson (its case, experiment or number is really there), specific to this lesson,
   and pitched at this level's reader?
When the digest does not settle it, open the lesson file named in the digest${opts.root ? ` (paths are relative to ${opts.root})` : ''}. Then check each alias as a
fact ("is this phrase really this idea?") and each film against its title and take-homes.

THE LESSONS (digests; they hold nothing from the graph)
${core.map((r) => { const d = get(r.lesson); return `${'='.repeat(100)}\n${d ? digestText(d) : `LESSON ${r.lesson}: no digest available; open src/content/lessons/${r.lesson}/lesson.mdx`}`; }).join('\n\n')}

YOUR ANSWER is one JSON object of exactly this shape${opts.answerFile ? `, written to ${opts.answerFile}` : ''}:
${VERIFY_SHAPE}
`.replace(/\n{3,}/g, '\n\n');
}
