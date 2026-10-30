// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import rehypeMethodLinks from './src/lib/rehype-method-links.mjs';
import rehypeDesignAnswer from './src/lib/rehype-design-answer.mjs';
import { METHODS } from './src/data/methods.ts';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { join, normalize, extname, sep } from 'node:path';

// Full-text search index. Pagefind reads the built HTML, so it runs once the build has written
// dist/ and puts its files in dist/pagefind/ (config: pagefind.yml). It is an integration, not a
// package.json step, so the index exists however the build is started: `npm run build`,
// `astro build`, or a CI/Cloudflare command that calls astro directly. If Pagefind itself fails the
// build fails; a site with no /pagefind/ would quietly fall back to title search, which is the
// regression this is here to prevent.
/** @returns {import('astro').AstroIntegration} */
const pagefindIndex = () => ({
  name: 'pagefind-index',
  hooks: {
    'astro:build:done': ({ dir, logger }) => {
      const site = fileURLToPath(dir);
      logger.info('indexing lesson text with Pagefind');
      const r = spawnSync('npx', ['--no-install', 'pagefind', '--site', site], { stdio: 'inherit', cwd: process.cwd() });
      if (r.status !== 0) throw new Error('Pagefind failed to build the search index (see output above).');
    },
  },
});

// `astro dev` has no search index of its own: Pagefind indexes built HTML, so the full-text
// index exists only after `npm run build` (or `npm run build:fast`). So that dev can still try
// full-text search, this serves the last build's dist/pagefind/ at /pagefind/. It is a
// convenience: the index is as old as the last build, and with no build the search falls back
// to titles and headings. Production does not use this (Cloudflare serves dist/ itself).
/** @type {Record<string, string>} */
const PF_TYPES = { '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.wasm': 'application/wasm' };
/** @returns {import('vite').Plugin} */
const devPagefind = () => ({
  name: 'dev-pagefind',
  apply: 'serve',
  configureServer(server) {
    const root = join(process.cwd(), 'dist', 'pagefind');
    server.middlewares.use('/pagefind', (req, res, next) => {
      const file = normalize(join(root, decodeURIComponent((req.url || '/').split('?')[0])));
      if (!file.startsWith(root + sep) || !existsSync(file) || !statSync(file).isFile()) return next();
      res.setHeader('Content-Type', PF_TYPES[extname(file)] || 'application/octet-stream');
      createReadStream(file).pipe(res);
    });
  },
});

// Biochemistrypedia — static-first Astro site. Islands only where interactive
// (the Mol* viewer and the Michaelis–Menten plotter ship JS; everything else
// renders to static HTML).
//
// Deployed as a Cloudflare Worker (Workers Builds, git-connected to main) whose
// origin is biochempedia.deppmann.workers.dev. `site` is the PUBLIC canonical
// host — every canonical link, OG url and sitemap entry derives from it — so it
// must name the domain actually bound to the Worker, not the origin.
export default defineConfig({
  site: 'https://biochemistrypedia.com',
  // Method names in lesson prose link to the methods library (first mention per section).
  integrations: [mdx({ rehypePlugins: [[rehypeMethodLinks, { methods: METHODS }], rehypeDesignAnswer] }), pagefindIndex()],
  vite: {
    plugins: [tailwindcss(), devPagefind()],
  },
});
