/* /films/idea/<id>.json (2026-11-21): one idea's films from the simplest level to the deepest, for
   /films/run/?idea=<id> ("play this idea at every level"). One small file per idea, so a phone
   fetches only the idea it plays. Built from the hop graph (src/lib/topic-graph.ts); only ideas
   whose films span two or more levels get a file. Film keys are those of /films/list.json. */
import type { APIRoute } from 'astro';
import { concepts } from '../../../lib/topic-graph';
import { ideaFilms } from '../../../lib/film-hops';

export async function getStaticPaths() {
  const out = [];
  for (const c of concepts) {
    const films = await ideaFilms(c.id);
    if (new Set(films.map((f) => f.stage)).size >= 2) out.push({ params: { id: c.id }, props: { name: c.name, films: films.map((f) => f.key) } });
  }
  return out;
}

export const GET: APIRoute = ({ props }) =>
  new Response(JSON.stringify({ name: props.name, films: props.films }), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
