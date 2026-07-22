// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

// Biochempedia — static-first Astro site. Islands only where interactive
// (the Mol* viewer and the Michaelis–Menten plotter ship JS; everything else
// renders to static HTML). Served from Cloudflare at its own apex domain,
// biochemistrypedia.com (registered on Cloudflare, so the zone is already
// there — no dependency on the pending deppmannlab.com DNS migration).
// `site` drives canonical URLs, og:url, and the sitemap, so it must match the
// domain actually attached to the Cloudflare project.
export default defineConfig({
  site: 'https://biochemistrypedia.com',
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
});
