/**
 * People who helped make STEMhop better, shown on /contributors/.
 *
 * Rules (Chris, 2026-11-20):
 *  - A person appears on the built page only when `confirmed` is true. Set it only after the person
 *    has said, in their own words, that they are happy to be listed and how.
 *  - `role` says what they did here, plainly, in one or two sentences. No ranks, no counts.
 *  - `link` is optional and only ever something the person chose to share.
 *  - Never name or allude to commercial test prep. Never imply a real exam: the MCAT-style questions
 *    were all written for this site.
 *  - No emails, photos or years of study.
 *
 * To add someone: append an object below, in the order they joined.
 */
export interface Contributor {
  name: string;
  /** What they did here, one or two plain sentences. */
  role: string;
  /** Optional page the person chose to share. */
  link?: { href: string; label: string };
  /** Month and year they started helping, as 'YYYY-MM'. */
  since: string;
  /** Short labels for the kind of work, for example 'MCAT-style questions'. */
  areas: string[];
  /** Kept out of the built page until permission is confirmed. */
  confirmed: boolean;
}

export const CONTRIBUTORS: Contributor[] = [
  {
    // Placeholder. Chris confirms the first real entry with the person before this is replaced.
    name: 'First contributor',
    role: 'A sentence or two about what this person did on the site.',
    since: '2026-11',
    areas: ['Area of work'],
    confirmed: false,
  },
];

export const confirmedContributors = (): Contributor[] => CONTRIBUTORS.filter((c) => c.confirmed);

export const sinceLabel = (since: string): string =>
  new Date(`${since}-15T12:00:00Z`).toLocaleDateString('en-US', { month: 'long', year: 'numeric', timeZone: 'UTC' });
