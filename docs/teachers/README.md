# /teachers: how the section is put together

Pages (all in `src/pages/teachers/`):

| URL | File | What it is |
|---|---|---|
| `/teachers` | `index.astro` | The hub that goes with the talk "Fast Tools, Slow Thinking" |
| `/teachers/do-it-yourself` | `do-it-yourself.astro` | Ten practical tips (uses `src/components/TeacherTip.astro`) |
| `/teachers/checklist` | `checklist.astro` | Printable one-page checklist (has a print stylesheet) |
| `/teachers/sources` | `sources.astro` | Every number with source and year (data in `src/data/teacher-sources.ts`) |
| `/teachers/demo` | `demo.astro` | Five-minute predict-then-reveal module |
| `/teachers/how-its-built` | `how-its-built.astro` | Renders `docs/teachers/HOW_ITS_BUILT.md` |
| `/teachers/life-science`, `/teachers/biology` | course pages for teachers | |
| `/teachers/talk/` | `public/teachers/talk/` | The embedded deck (static files, not an Astro page) |

Text and prompts live in `src/data/teachers.ts`. Rule for every page: a number needs a source and a
year in `teacher-sources.ts`, or it does not go on the page.

## The public talk deck

The talk is built in the workshop folder (`~/Dropbox/Chris/teaching/2026-10-24 AI teacher workshop/talk`,
see its README). The site carries a public copy: main path only, no speaker notes, no appendix.

To refresh it after the deck changes:

```bash
node scripts/refresh-teachers-deck.mjs            # copies the viewer, deck.json, images; moves the movies
python3 "<workshop folder>/talk/serve.py"         # in another terminal, port 8765 (skip if running)
python3 scripts/make-teachers-deck-pdf.py         # rebuilds public/teachers/Fast_Tools_Slow_Thinking.pdf
npm run build
```

- `public/teachers/talk/` holds the viewer (`index.html`, `viewer.js`, `viewer.css`), `deck.json`,
  fonts and images. There is no `notes.json`.
- The two movies and their caption files go in `public/explainers/talk-deck/`, so `scripts/upload-media.mjs`
  sends them to R2 and the edge worker answers byte-range requests (Safari needs those).
  **When deploying, run `node scripts/upload-media.mjs` so the files in that folder reach the bucket.**
  Until then the worker falls back to the copy in the build, so playback works either way.
- With no `/api/me`, the viewer falls back to audience mode. `p` does nothing, and `?presenter=1` says the
  notes could not be loaded.
