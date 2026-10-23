## How this site is built, in plain language

This is the supplement to the talk "Fast Tools, Slow Thinking." The talk is about teaching. This page is about the machinery, for anyone who wants to know what was used, what it cost, and how the passwords are kept. Every number below is either from the talk or from a file in the site's repository, and the file is named next to it. Where something was never measured, it says **not measured**. Nothing is estimated.

### The pipeline in brief: write, check, fix, install

Every lesson goes through the same four steps, and the check is done by something that did not write the lesson.

1. **Write.** A strong AI model drafts the lesson from a packet of source material (twenty years of lectures and, for some courses, research on the scientists involved). The writer is told what is in scope and what must not be invented.
2. **Check, independently.** A different AI agent, with web access, is told to assume the draft has at least three errors. It rules on every factual claim: confirmed, imprecise, wrong, or could not be checked. It proposes exact edits. Small scripts check what a script can check better than any model: that a protein structure ID points at the right molecule, and that the answer keys are not all in the same order.
3. **Fix.** A script applies the proposed edits, and the lesson checker runs again to make sure the edits did not break anything (for example, by making a section too long).
4. **Install, then a human reads it.** The lesson is added to the site. The build refuses to publish a lesson that fails its checks. An expert (here, the course author) reads it, which takes about 1 to 2 hours per lesson. That last step is the bottleneck, not the writing.

### What the checking found

For the Cell Signaling course (44 lessons), the checker ruled on 3,468 claims. It found 49 wrong, 453 imprecise, and 287 it could not verify, and 841 edits were made. (The talk says 3,468 claims, the repo's tally.) A separate cross-check of the Genetics course produced 80 corrections, for example a figure for the share of DNA in trisomy 21 corrected from 1.5% to 0.8%.

Earlier, on the first 11 Cell Signaling lessons, the checker found that most wrong claims came from the unpublished book the source packets drew on, not from the AI writer: a reversed anecdote, wrong dates, misattributed credit. No answer key was wrong in any of the 88 questions checked. Source: `docs/expansion/bakeoff-1/results.md`.

None of this replaces a person. An AI checker can be wrong, and it cannot tell you which of two defensible answers a teacher wants. Expert review is the scarce resource.

### Which models and tools are used for what

The site ran a head-to-head test ("bake-off") before choosing. The same two lessons were each written by three models and scored blind by two judges (source: `docs/expansion/bakeoff-1/results.md`).

| Job | Model or tool | Why |
|---|---|---|
| Lesson spec and source packet | Claude Opus, plus scripts | Judgment about scope and order |
| Lesson draft | Claude Opus, or Claude Sonnet where budget matters | Opus scored 8.7 of 10, Sonnet 8.0, Haiku 5.7. The ranking was the same for both lessons and both judges |
| Lesson prose from the smallest model (Haiku) | Not used | Questions scored 3 to 6 of 10 and it gave a wrong database ID |
| Fact-check with web access | Claude Sonnet | Sharper than Haiku and used fewer tokens |
| Second fact-check on important lessons | Claude Haiku or a different model | Caught two things the first checker missed |
| Outlines of lecture decks, simple key checks | Claude Haiku | Good enough and mechanical |
| Films and simulations | Claude Sonnet, after an Opus pilot | The first Sonnet films made to the revised brief were as good as the Opus pilot |

Other tools, from `explainers/README.md` and `explainers/_pipeline/`:

- **Manim** draws the animated explainers (the "3Blue1Brown style") in code.
- **faster-whisper** transcribes the narration so captions and animation timing come from the real speech.
- **Narration voices.** ElevenLabs (the voice "Sarah") narrates the biochemistry films and scientist profile films. Gemini text-to-speech (voice "Charon") narrates the Cell Signaling films. The free macOS built-in voice is used for drafts so no money is spent until the picture is right. The narration script has no default voice engine on purpose, after a test run spent 105 ElevenLabs characters by accident.
- **Lesson figures.** Up to five AI-generated illustrations per lesson, from OpenAI's image generator, with a model judge that checks each one and a disclosure on the page (`docs/expansion/figures/STATUS.md`, `IMAGE_POLICY.md`). No chemical structure is ever AI-drawn: molecules load live from the public RCSB and PubChem databases.
- **Hosting.** The site is static pages built with Astro, served by Cloudflare Workers. Large video files sit in a Cloudflare R2 storage bucket, and a small worker (`worker/index.js`) answers the video range requests Safari needs. A push to the `main` branch builds and deploys automatically. Analytics is Plausible, which uses no cookies.

### What it cost

Here is what the repository actually recorded. Tokens are the units AI models are billed in.

| Item | Recorded | Source |
|---|---|---|
| Writing plus fact-checking one Cell Signaling lesson | About 440,000 to 480,000 tokens | `bakeoff-1/results.md`, sections F and G |
| One fact-check pass on one lesson | About 250,000 to 313,000 tokens | same |
| One film, written by Sonnet | About 430,000 tokens (Opus pilot film: 411,000) | same, section H |
| One passage-writing test run | 106,000 to 130,000 tokens | `bakeoff-0/results.md` |
| Overhead of starting any agent call | About 60,000 tokens before it does any work | `PLAN.md`, `bakeoff-0/results.md` |
| Gemini narration of one film | Under 20 cents (about 15 to 17 cents) | `bakeoff-1/results.md`; `explainers/_pipeline/build_audio.py` |
| Building the whole 44-lesson Cell Signaling course in dollars | **Not measured** | The plan lists "cost per lesson" as a goal; the repo has token counts, not dollars |
| Dollars per lesson, for any course | **Not measured** | Token prices were not recorded |
| ElevenLabs narration in dollars | **Not measured** | It draws on a monthly quota; no per-film figure was recorded |
| Image generation in dollars | **Not measured** | |
| Cloudflare hosting in dollars | **Not measured** | |
| The author's own time | **Not measured**, except expert review at about 1 to 2 hours per lesson | `PLAN.md` |

For scale: the first 30 lessons took about 17 weeks (June 12 to October 10, 2026). The next 324 took 13 days (October 11 to 23). As of October 23, 2026 the site has 354 lessons, all live, in 11 courses, with 464 films (lesson explainers, scientist profile films and methods films). The newest course is grade 7 Life Science: 34 lessons in 8 units, following the Virginia Life Science Standards of Learning (LS.1 to LS.11), planned and released on October 23 (first commit 11:40 am, last lesson merged 6:34 pm ET). High school Biology, 33 lessons following BIO.1 to BIO.8, was released on October 20. Counts come from the repository's history and content on those dates. A grant request for $10,000 in July 2026 said $5,000 would buy three to five complete lessons. It was not selected, and the site was built anyway. The reason, from the project plan: a student's preparation should not depend on what the family can pay.

What these numbers do not say: fast is not finished. Writing got cheap; checking did not. Every lesson still needs an expert's read, at about 1 to 2 hours each, and the grade 7 and Biology courses are first editions with classroom testing just beginning. Dollars per lesson were **not measured** (see the table above).

### If you want to build with an AI model yourself

Start with the [Gemini API](https://ai.google.dev/gemini-api/docs). Its documentation walks through getting access and making a first request, and it has a free tier that is enough to try things out. Follow your district's rules on which AI tools may be used with student work.

### Do this on a teacher budget

You do not need any of the above to get the benefit. The part that matters most for a classroom is the pre-work, and it costs close to nothing.

- **Use free or district-approved tools.** Many AI tools have a free tier. The limits change often, so check the current terms, and use only what your district has approved for work involving students.
- **Start with one unit, not a course.** A realistic first step: pick one standard; use the "predict-then-reveal" prompt on the [Teachers page](/teachers#prompts) to draft about five items; check every item against your textbook yourself; give it to students as pre-work on a free form tool your district allows; read the answers; open class with the room's own anonymous words. The time this takes you was not measured. In class, expect one predict, argue, reveal cycle to take 8 to 10 minutes, not 4.
- **Check everything.** Whatever the tool drafts, you verify. An AI summary of one student's work once reported "no activity" for a student who had finished, which is why the human check comes before anything is sent.
- **Privacy.** Student work is protected (FERPA in the United States, and COPPA for children under 13). Remove names and IDs before pasting anything a student wrote. Do not store student audio. When in doubt, ask your district's technology office. This page is not legal advice.
- **You can also just use the finished courses.** They are free, need no account, and you may link to them.
- **Step-by-step versions** of the pre-work and the other classroom ideas are in the [do-it-yourself guide](/teachers/do-it-yourself). Every number in the talk, with its source and year, is on the [sources page](/teachers/sources).
