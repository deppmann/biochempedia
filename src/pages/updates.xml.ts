/* Atom feed of /updates/: one entry per milestone, in its plain-words sentence. Built at deploy time
   from src/data/updates.ts, so it costs nothing to run and works in any feed reader or email-digest service. */
import type { APIRoute } from 'astro';
import { MILESTONES, KIND_LABEL } from '../data/updates';
import { milestoneId } from '../lib/updates-feed';

const SITE = 'https://biochemistrypedia.com';
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const stamp = (d: string) => `${d}T12:00:00Z`;

export const GET: APIRoute = () => {
  const items = [...MILESTONES].sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
  const updated = stamp(items[0].date);
  const entries = items.map((m) => {
    const id = milestoneId(m);
    return `  <entry>
    <id>tag:biochemistrypedia.com,2026:updates/${id}</id>
    <title>${esc(m.title)}</title>
    <link rel="alternate" type="text/html" href="${SITE}/updates/#${id}"/>
    <updated>${stamp(m.date)}</updated>
    <published>${stamp(m.date)}</published>
    <category term="${m.kind}" label="${esc(KIND_LABEL[m.kind])}"/>
    <summary type="text">${esc(m.text)}</summary>
  </entry>`;
  }).join('\n');
  const xml = `<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <id>tag:biochemistrypedia.com,2026:updates</id>
  <title>Biochemistrypedia: what’s new</title>
  <subtitle>New courses, learning tools and fixes on Biochemistrypedia, a free site for learning science.</subtitle>
  <link rel="self" type="application/atom+xml" href="${SITE}/updates.xml"/>
  <link rel="alternate" type="text/html" href="${SITE}/updates/"/>
  <updated>${updated}</updated>
  <author><name>Christopher Deppmann</name></author>
  <icon>${SITE}/favicon.svg</icon>
${entries}
</feed>
`;
  return new Response(xml, { headers: { 'Content-Type': 'application/atom+xml; charset=utf-8' } });
};
