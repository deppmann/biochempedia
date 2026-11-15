/* /robots.txt. Built rather than kept in public/ so its two addresses follow the site's address
   (src/lib/site-host.mjs). With the address unchanged the file is byte-for-byte what it was. */
import type { APIRoute } from 'astro';
import { SITE_ORIGIN } from '../lib/site-host.mjs';

const body = `# Biochemistrypedia: free science lessons. People and well-behaved agents are welcome.
#
# Content signals (https://contentsignals.org): yes to search indexing, and yes to AI
# systems reading pages to answer a person's question (please link the lesson you used).
#
# For AI agents: start at ${SITE_ORIGIN}/llms.txt. Every lesson has a plain
# Markdown copy at /lessons/<slug>.md, and the whole catalog is at /catalog.json.

User-agent: *
Content-Signal: search=yes, ai-input=yes
Allow: /

Sitemap: ${SITE_ORIGIN}/sitemap.xml
`;

export const GET: APIRoute = () => new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
