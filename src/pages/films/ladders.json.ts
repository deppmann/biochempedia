/* /films/ladders.json (2026-11-22): the ladders the film library can play, for "Play a ladder" on
   /films/ (src/lib/film-ladder.ts). Fetched once, the first time someone opens a ladder there.

   One entry per idea that has films at two or more levels (the ideas with "Play the ladder"):

     id, name, short   the idea, as the hop graph names it
     rungs             what the shared ladder drawing needs (src/lib/hop-ladder.mjs): one per lesson
                       that teaches the idea, { slug, title, href, rank, courseTitle, adds }
     films             what the ladder plays, simplest level first, each lesson's chapters in order:
                       [film key, title, film page, level 0..6, seconds, poster]

   The films are the lessons of the idea's run (runOf in src/lib/hop.ts), each with both of its
   chapters: a lesson film is a chapter pair, and the second chapter is where the lesson's second
   half is, so a ladder that plays the lesson plays both. A film key is the path under /explainers/
   without ".mp4", as in /films/list.json. Static, built with the site; nothing about visitors.
   Columns may be added at the end, never removed or reordered. */
import type { APIRoute } from 'astro';
import { filmLadders } from '../../lib/film-ladders';

export const GET: APIRoute = async () =>
  new Response(JSON.stringify({ v: 1, ladders: await filmLadders() }), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
