// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

// Biochempedia — static-first Astro site. Islands only where interactive
// (the Mol* viewer and the Michaelis–Menten plotter ship JS; everything else
// renders to static HTML).
//
// Deployed as a Cloudflare Worker (Workers Builds, git-connected to main) whose
// origin is biochempedia.deppmann.workers.dev. `site` is the PUBLIC canonical
// host — every canonical link, OG url and sitemap entry derives from it — so it
// must name the domain actually bound to the Worker, not the origin.
export default defineConfig({
  site: 'https://biochemistrypedia.com',
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
});
