import { z } from 'astro:content';

/* =============================================================================
   Biochempedia lesson schema  (single source of truth for a lesson)
   -----------------------------------------------------------------------------
   Every lesson's frontmatter is validated against this at build time. Because
   Astro runs content-collection validation during `astro build`, ANY violation
   below FAILS THE BUILD — that is the enforcement mechanism for the project's
   content-integrity rules (see IMAGE_POLICY.md and LICENSING.md):

     • Structures may ONLY come from a real accession ID (RCSB PDB or PubChem).
       AI-drawn / hand-rolled geometry is impossible to express — there is no
       field for it. (CONTENT-INTEGRITY RULE #1)

     • An AI-generated image is allowed ONLY if it is flagged aiGenerated:true
       AND carries factCheckedBy:"<name>". An unreviewed AI image fails the
       build. (CONTENT-INTEGRITY RULE #2)

     • Every practice / MCAT question MUST carry a verified answer + rationale,
       and the answer index must point at a real choice. A question missing
       either fails the build. (QUESTIONS rule)

   The Sources & Integrity footer and the self-test quiz are generated FROM this
   data, so the schema is also the manifest the reader is shown.
   ============================================================================ */

/** A scientist card, grounded in the book. Quotes must be verbatim. */
const scientist = z.object({
  name: z.string().min(1),
  /** One-line statement of what they contributed to this concept. */
  contribution: z.string().min(1),
  /** Where in the source manuscript this profile lives (citation anchor). */
  profileSourceAnchor: z.string().min(1),
  /** VERBATIM quotes from the book / historical record — never paraphrased. */
  quotes: z.array(z.string().min(1)).default([]),
  /** Optional portrait years etc., for display only. */
  dates: z.string().optional(),
});

/** A technique, for the "how the technique works" quick-reference panel. */
const technique = z.object({
  name: z.string().min(1),
  blurb: z.string().min(1),
});

/** A live molecular structure — ONLY from a real accession ID. */
const structure = z.object({
  label: z.string().min(1),
  /** rcsb = macromolecule (PDB, data CC0); pubchem = small molecule. */
  source: z.enum(['rcsb', 'pubchem']),
  /** The accession ID: a PDB ID (e.g. "1LYZ") or a PubChem CID (e.g. "439174"). */
  id: z.string().min(1),
  caption: z.string().optional(),
  /** Optional: EC number / extra provenance shown in the integrity footer. */
  note: z.string().optional(),
});

/** Spotify podcast embed (show or episode). Embed-only, never rehosted. */
const podcast = z.object({
  platform: z.literal('spotify'),
  /** A canonical open.spotify.com URL (show or episode). */
  url: z.string().url(),
  title: z.string().optional(),
  note: z.string().optional(),
});

/** A YouTube embed. Embed-only (iframe), never rehosted. */
const video = z.object({
  title: z.string().min(1),
  /** The 11-char YouTube video id (NOT a full URL). */
  youtubeId: z.string().min(1),
  /** Why this video is here / who made it (curation + attribution). */
  sourceNote: z.string().min(1),
});

/* A simulation. NOTE: the original spec named this singular (`simulation`).
   It is widened to an array here because the definition-of-done requires a
   lesson to carry BOTH an original local sim AND a PhET embed. Each entry is:
     • type "phet"  → `ref` is the HTML5 iframe URL; `attribution` REQUIRED.
     • type "local" → `ref` is a registered component name (see the renderer);
                       `attribution` is the lesson's own credit line. */
const simulation = z
  .object({
    type: z.enum(['phet', 'local']),
    /** PhET: the HTML5 sim URL. Local: a component key the page knows how to mount. */
    ref: z.string().min(1),
    title: z.string().min(1),
    attribution: z.string().min(1),
    caption: z.string().optional(),
  })
  .superRefine((sim, ctx) => {
    if (sim.type === 'phet' && !/^https?:\/\//.test(sim.ref)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'A PhET simulation `ref` must be a full https:// iframe URL.',
        path: ['ref'],
      });
    }
    // PhET is CC BY 4.0 — the attribution must actually name PhET.
    if (sim.type === 'phet' && !/phet/i.test(sim.attribution)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message:
          'A PhET simulation must attribute PhET Interactive Simulations (CC BY 4.0).',
        path: ['attribution'],
      });
    }
  });

/** A multiple-choice question. Build FAILS without a valid answer + rationale. */
const question = z
  .object({
    stem: z.string().min(1),
    choices: z.array(z.string().min(1)).min(2, 'A question needs ≥2 choices.'),
    /** 0-based index of the correct choice. Required. */
    answer: z.number().int().nonnegative(),
    /** Why the answer is correct (and ideally why distractors are wrong). Required. */
    rationale: z.string().min(1, 'Every question must carry a rationale.'),
  })
  .superRefine((q, ctx) => {
    if (q.answer >= q.choices.length) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: `answer index ${q.answer} is out of range for ${q.choices.length} choices.`,
        path: ['answer'],
      });
    }
  });

/** An image. The integrity gate lives here. */
const image = z
  .object({
    src: z.string().min(1),
    alt: z.string().min(1, 'Every image needs descriptive alt text.'),
    /** Was this image produced by a generative model? */
    aiGenerated: z.boolean(),
    /** REQUIRED when aiGenerated is true: the human who fact-checked it. */
    factCheckedBy: z.string().nullable().default(null),
    /** Attribution / license for non-AI images (original or CC-with-attribution). */
    credit: z.string().optional(),
  })
  .superRefine((img, ctx) => {
    // RULE #2: an AI image with no human fact-checker fails the build.
    if (img.aiGenerated && (!img.factCheckedBy || img.factCheckedBy.trim() === '')) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message:
          'aiGenerated:true requires a non-empty factCheckedBy. Unreviewed AI images are not allowed.',
        path: ['factCheckedBy'],
      });
    }
    // A non-AI figure must declare where it came from (original or CC + attribution).
    if (!img.aiGenerated && (!img.credit || img.credit.trim() === '')) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message:
          'A non-AI image must carry `credit` (e.g. "Original — C. Deppmann" or a CC license + attribution).',
        path: ['credit'],
      });
    }
  });

/** The full lesson frontmatter schema. */
export const lessonSchema = z.object({
  title: z.string().min(1),
  /** URL slug (also the lesson folder name, by convention). */
  slug: z.string().min(1),
  /** The course slide-deck title this lesson maps to (e.g. "Mechanisms and Inhibitors"). */
  courseChapter: z.string().min(1),
  summary: z.string().min(1),

  scientists: z.array(scientist).default([]),
  techniques: z.array(technique).default([]),
  structures: z.array(structure).default([]),

  podcast: podcast.optional(),
  videos: z.array(video).default([]),
  simulations: z.array(simulation).default([]),

  practiceQuestions: z.array(question).default([]),
  /** MCAT-style — ORIGINAL items only, never real AAMC questions. */
  mcatQuestions: z.array(question).default([]),

  images: z.array(image).default([]),

  /** Reserved for the future RAG-grounded tutor. Not rendered yet. */
  corpusTags: z.array(z.string()).default([]),

  /** Optional ordering hint for the lesson index. */
  order: z.number().optional(),
  draft: z.boolean().default(false),
});

export type Lesson = z.infer<typeof lessonSchema>;
export type ScientistCard = z.infer<typeof scientist>;
export type StructureRef = z.infer<typeof structure>;
export type Question = z.infer<typeof question>;
export type SimulationRef = z.infer<typeof simulation>;
