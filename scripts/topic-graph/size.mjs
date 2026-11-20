#!/usr/bin/env node
/**
 * Hop graph: how big is /graph.json, and how big will it be when the graph is full?
 *
 * Prints the raw and gzipped size of the compact browser form of the current graph (built from
 * source, no site build needed): as one file, and as the site serves it (/graph.json index, one
 * file per area, /graph/all.json). Then an estimate for a larger graph. The estimate scales the three
 * parts separately, because they grow differently: text that belongs to a concept (name, blurb,
 * aliases, sideways hops) grows with the number of concepts; rung rows grow with the number of
 * lessons, not concepts; the lesson and film tables stop growing once every lesson is in.
 * The site should split the file by area if the full graph would pass about 150 KB gzipped.
 *
 *   node scripts/topic-graph/size.mjs [--concepts 600] [--graph <file>]
 */
import { gzipSync } from 'node:zlib';
import { readFileSync } from 'node:fs';
import { loadGraphSite, coreSite, makeTopicGraph, readGraph, GRAPH_FILE } from './lib.mjs';

const argv = process.argv.slice(2);
const opt = (f, d) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : d; };
const target = Number(opt('--concepts', 600));
const site = await loadGraphSite();
const graph = opt('--graph') ? JSON.parse(readFileSync(opt('--graph'), 'utf8')) : readGraph(GRAPH_FILE);
const client = makeTopicGraph(graph, coreSite(site)).clientGraph();
const bytes = (x) => Buffer.byteLength(JSON.stringify(x));
const gz = (x) => gzipSync(Buffer.from(JSON.stringify(x)), { level: 9 }).length;
const kb = (n) => `${(n / 1024).toFixed(1)} KB`;

const n = client.concepts.length;
const core = client.concepts.reduce((a, c) => a + c.r.filter((r) => r[1] === 0).length, 0);
const uses = client.concepts.reduce((a, c) => a + c.r.filter((r) => r[1] === 1).length, 0);
const rungBytes = bytes(client.concepts.map((c) => c.r));
const conceptBytes = bytes(client.concepts.map(({ r: _r, ...rest }) => rest));
const tableBytes = bytes({ lessons: client.lessons, films: client.films, courses: client.courses });
const total = bytes(client), totalGz = gz(client);
console.log(`now: ${n} concepts, ${core} core and ${uses} uses rungs, ${client.lessons.length} lessons, ${client.films.length} films`);
console.log(`     the whole graph as one file: ${kb(total)} raw, ${kb(totalGz)} gzipped (ratio ${(total / totalGz).toFixed(2)})`);
console.log(`     of the raw bytes: concept text ${kb(conceptBytes)}, rung rows ${kb(rungBytes)}, lesson and film tables ${kb(tableBytes)}`);

// the full graph: every live lesson in; about 1.6 core and 1 uses rung per lesson (the spec's 1 to 3 and 0 to 2)
const live = site.lessons.size, allFilms = site.films.size;
const perCore = rungBytes / Math.max(1, core + uses * 0.12);          // a uses row is a pair of numbers
const estCore = Math.round(live * 1.6), estUses = live;
const estRung = perCore * (estCore + estUses * 0.12);
const estConcept = (conceptBytes / n) * target;
const estTables = (bytes(client.lessons) / client.lessons.length) * live + (bytes(client.films) / client.films.length) * Math.min(allFilms, Math.round(estCore * (client.films.length / core))) + bytes(client.courses);
const estRaw = estConcept + estRung + estTables;
// Prose compresses a little better as a file grows; the ratio measured now is the cautious choice.
const ratio = total / totalGz;
console.log(`estimate for ${target} concepts over all ${live} lessons (${estCore} core, ${estUses} uses rungs):`);
console.log(`     ${kb(estRaw)} raw (concept text ${kb(estConcept)}, rung rows ${kb(estRung)}, tables ${kb(estTables)}), about ${kb(estRaw / ratio)} gzipped`);
console.log(`     ${estRaw / ratio > 150 * 1024 ? 'OVER' : 'under'} the 150 KB line for one file${estRaw / ratio > 150 * 1024 ? ', which is why the site serves an index and one file per area' : ''}`);

// what the site serves: the index, one file per area, and everything
const api = makeTopicGraph(graph, coreSite(site));
const index = api.clientIndex();
const areaSizes = graph.areas.map((a) => { const ids = Object.keys(graph.concepts).filter((id) => graph.concepts[id].area === a.id); const g = api.clientGraph(ids); return { id: a.id, n: ids.length, raw: bytes(g), gz: gz(g) }; });
const big = areaSizes.slice().sort((x, y) => y.gz - x.gz)[0];
console.log('served now:');
console.log(`     /graph.json (index)   ${kb(bytes(index))} raw, ${kb(gz(index))} gzipped`);
console.log(`     /graph/<area>.json    ${areaSizes.length} files, ${kb(areaSizes.reduce((x, y) => x + y.gz, 0))} gzipped in all; largest ${big.id} (${big.n} concepts) ${kb(big.raw)} raw, ${kb(big.gz)} gzipped`);
console.log(`     /graph/all.json       ${kb(total)} raw, ${kb(totalGz)} gzipped`);
const idxPer = (bytes(index.concepts) / n) * target + bytes(index.lessons) / Math.max(1, Object.keys(index.lessons).length) * live;
console.log(`estimate for ${target} concepts: index about ${kb(idxPer / (bytes(index) / gz(index)))} gzipped; a large area (a fifth of the graph) about ${kb(estRaw / ratio / 5 * 1.15)} gzipped`);
