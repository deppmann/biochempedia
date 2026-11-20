/* /graph.json: the index of the hop graph, for browsers and other programs.

   The hop graph says which ideas the site teaches and where: each concept has a ladder of lessons
   across levels, the films that show it and sideways hops to neighbouring ideas
   (src/data/topic-graph.json, written offline and checked in CI; see src/lib/topic-graph.ts).

   This file is the small part every reader of the graph needs first: every idea's name, one-line
   description, everyday phrases and the levels it is taught at, plus which ideas each lesson
   teaches. It is enough to search for an idea. The ladders themselves are split by area so a phone
   fetches only the shelf it needs:
     /graph/<area>.json   one area's concepts with their rungs, notes, films and sideways hops
     /graph/all.json      everything in one file
   Static, built with the site; nothing about visitors. `covered` and `live` say how many lessons
   have a record so far: the graph fills in as lessons are added, and a lesson with no record is
   normal. Keys are short on purpose; clientIndex() in src/lib/topic-graph-core.mjs documents them.
   Fields may be added, never renamed or removed. */
import type { APIRoute } from 'astro';
import { clientIndex } from '../lib/topic-graph';

export const GET: APIRoute = async () =>
  new Response(JSON.stringify(await clientIndex()), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
