/* /films/search.json (2026-11-22): what a film can be found by besides its card in /films/list.json:
   its field, the ideas its lesson teaches, the method it shows, its take-homes and rarer transcript
   words. Built by src/lib/film-search-data.ts; read by src/lib/film-search.mjs in the film library,
   the run page and the site search box. Fetched the first time someone searches. */
import type { APIRoute } from 'astro';
import { filmSearchData } from '../../lib/film-search-data';

export const GET: APIRoute = async () =>
  new Response(JSON.stringify(await filmSearchData()), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
