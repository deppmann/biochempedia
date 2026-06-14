// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

import cloudflare from "@astrojs/cloudflare";

// Biochempedia — static-first Astro site. Islands only where interactive
// (the Mol* viewer and the Michaelis–Menten plotter ship JS; everything else
// renders to static HTML). Deployed to Cloudflare Pages at
// biochempedia.deppmannlab.com.
export default defineConfig({
  site: 'https://biochempedia.deppmannlab.com',
  integrations: [mdx()],

  vite: {
    plugins: [tailwindcss()],
  },

  adapter: cloudflare()
});