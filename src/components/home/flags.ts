/* Two parts of the front door are written but switched OFF, because what they lead to is not
   on the site yet. Turn one on only when its other half is merged and live.

   SYLLABUS_BOX   The teachers' "paste your syllabus" box (SyllabusBox.astro). It needs the matcher
                  that runs in the browser on the hop graph (src/lib/syllabus-match.ts is the seam,
                  and today it answers "not built"). Until that lands the teachers' door leads with
                  the standards maps. Do NOT point teachers at /teach/syllabus/ or /plan/ instead:
                  both are switched off on the live site, and the first sends a syllabus to an AI
                  model, which the box's own privacy sentence says never happens.

   CALENDAR_LINK  The parents' link to /calendar/. That page is being built in another pull request;
                  with the flag on before it exists, check-assets fails the build (a dead link). */
export const SYLLABUS_BOX = false;
export const CALENDAR_LINK = false;
