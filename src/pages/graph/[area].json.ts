/* /graph/<area>.json and /graph/all.json: the hop graph's ladders, for browsers and other programs.

   One file per area (the ids are in /graph.json), and `all` for everything at once. Each holds
   concepts with their rungs (lesson, core or uses, the note on what that level adds, the section
   anchor), film links and sideways hops. A lesson's title, course and level are written once, in
   tables the rungs point into; clientGraph() in src/lib/topic-graph-core.mjs documents every
   column and expandClientGraph() there turns a file back into readable objects.
   An area with no concept yet still has a file, so the address never 404s. */
import type { APIRoute, GetStaticPaths } from 'astro';
import { areas, clientArea, clientGraph } from '../../lib/topic-graph';

export const getStaticPaths: GetStaticPaths = () => [{ params: { area: 'all' } }, ...areas.map((a) => ({ params: { area: a.id } }))];

export const GET: APIRoute = async ({ params }) => {
  const body = params.area === 'all' ? await clientGraph() : await clientArea(params.area!);
  return new Response(JSON.stringify(body), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
