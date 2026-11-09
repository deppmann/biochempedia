/* Shared by /updates/ (anchors) and /updates.xml (the Atom feed): a stable id for each milestone,
   from its date and title, so a feed entry links to its place on the page and never changes id. */
import type { Milestone } from '../data/updates';

export const milestoneId = (m: Pick<Milestone, 'date' | 'title'>) =>
  `${m.date}-${m.title.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')}`;
