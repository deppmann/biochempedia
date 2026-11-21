/* Links in the site chrome that are written but switched OFF, because what they lead to is not on
   the site yet (check-assets fails the build on a dead link). Flip one only when its page is live.

   IDEAS_LINK    "Find an idea" (/ideas/) in the menu, the footer's Learn list, and one line on the
                 search box's no-result state. ON since the ladder work merged (2026-11-21); the
                 search page carries its own line to the same place.

   PLANNER_TILE  A "Study planner" tile (/plan/) in the homepage's "Things to try". The planner has
                 been live on the real site since 2026-11-21; whether the tile comes back is Chris's call. */
export const IDEAS_LINK = true;
export const PLANNER_TILE = false;
