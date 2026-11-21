/* /ideas/film-runs.json: "Play the ladder". For every idea with films at two or more levels, its
   films in order from the simplest level to the deepest, so a player can run them as one finite
   set that says how many films and minutes it holds and where it ends.

     link    the address a run is opened with ({id} is the idea's id); null until the run page reads it
     runs    { <idea id>: { name, seconds, films: [[film key, title, film page, level 0..6, seconds, lesson slug]] } }

   A film key is the path under /explainers/ without ".mp4", as in /films.json and /graph/all.json.
   Static, built with the site; nothing about visitors. Columns may be added at the end, never
   removed or reordered. */
import type { APIRoute } from 'astro';
import { allIdeas, PLAY_LADDER } from '../../lib/hop';

export const GET: APIRoute = async () => {
  const runs: Record<string, unknown> = {};
  for (const i of await allIdeas()) {
    if (new Set(i.films.map((f) => f.rank)).size < 2) continue;
    runs[i.id] = {
      name: i.name,
      seconds: Math.round(i.films.reduce((t, f) => t + f.durationSec, 0)),
      films: i.films.map((f) => [f.key, f.title, f.href, f.rank, Math.round(f.durationSec), f.lesson]),
    };
  }
  return new Response(JSON.stringify({ v: 1, link: PLAY_LADDER ? '/films/run/?idea={id}' : null, runs }), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
