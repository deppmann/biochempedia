/* "Where are you starting?" The stage bands shared by the homepage chooser and the
   /courses/ catalog. A band is a plain-language name for one or more existing course
   `tier` values (see courses.ts), so adding a course to a tier needs no change here.
   `ladderStep` splits the grades 7-12 tier into grade 7 and high school. */
import type { Course } from './courses';

export interface Stage {
  key: string;
  /** Short name used as the heading. */
  title: string;
  /** "Start here if..." line, in the reader's terms. */
  here: string;
  /** Longer note shown above the cards on /courses/. */
  note: string;
}

export const STAGES: Stage[] = [
  { key: 'ages-5-10', title: 'Ages 5–10, with a grown-up', here: 'You’re a parent or teacher with a young child. You run the activity together, away from the screen.', note: 'Hands-on activities a grown-up runs with children, away from the screen. Aligned to Virginia’s kindergarten to grade 4 science standards.' },
  { key: 'grade-7', title: 'Grade 7', here: 'You’re about 12, or you want biology from its first page.', note: 'Middle school Life Science, aligned to the Virginia Standards of Learning.' },
  { key: 'high-school', title: 'High school', here: 'You’re in high school, or you want the full high school course.', note: 'The full high school Biology course, aligned to the Virginia Standards of Learning.' },
  { key: 'starting-college', title: 'Starting college', here: 'You’re starting college biology, or coming back to it after years away.', note: 'The first college course. It is the only one in this band so far; chemistry, statistics and physics are not built yet.' },
  { key: 'college-core', title: 'College: the core', here: 'You know the basics and want what a biology degree covers.', note: 'The three subjects every biology degree requires. Each course also stands on its own.' },
  { key: 'college-further', title: 'College: going further', here: 'You have the core and want one subject in depth.', note: 'One subject taken further, for students who have the core behind them.' },
  { key: 'graduate', title: 'Graduate school and beyond', here: 'You want to read the current research and see the open questions.', note: 'Courses that go all the way to current research.' },
];

/** The band a course belongs to, derived from its tier. */
export function stageOf(c: Pick<Course, 'tier' | 'ladderStep'>): string {
  switch (c.tier) {
    case 'families': return 'ages-5-10';
    case 'highschool': return c.ladderStep === 1 ? 'grade-7' : 'high-school';
    case 'foundation': return 'starting-college';
    case 'core': return 'college-core';
    case 'elective': return 'college-further';
    case 'advanced': return 'graduate';
  }
}
