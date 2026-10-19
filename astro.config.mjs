// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import rehypeMethodLinks from './src/lib/rehype-method-links.mjs';
import { METHODS } from './src/data/methods.ts';

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
  integrations: [mdx({ rehypePlugins: [[rehypeMethodLinks, { methods: METHODS }]] })],
  vite: {
    plugins: [tailwindcss()],
  },
});
