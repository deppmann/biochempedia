/* Two parts of the front door are written but switched OFF, because what they lead to is not
   on the site yet. Turn one on only when its other half is merged and live.

   SYLLABUS_BOX   The teachers' "paste your syllabus" box (SyllabusBox.astro). It needs the matcher
                  that runs in the browser on the hop graph (src/lib/syllabus-match.ts is the seam,
                  and today it answers "not built"). Until that lands the teachers' door leads with
                  the standards maps. Do NOT point teachers at /teach/syllabus/ or /plan/ instead:
                  both are switched off on the live site, and the first sends a syllabus to an AI
                  model, which the box's own privacy sentence says never happens.

   CALENDAR_LINK  The parents' link to /calendar/parent/. The calendar was built in another pull
                  request while this page was; the link stays off until someone has read the two
                  together. With the flag on and the page missing, check-assets fails the build. */
export const SYLLABUS_BOX = false;
export const CALENDAR_LINK = false;
