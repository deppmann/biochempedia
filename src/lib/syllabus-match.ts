/* The seam for the teachers' syllabus matcher (the homepage's SyllabusBox.astro, switched OFF in
   src/components/home/flags.ts).

   The matcher is NOT BUILT. It is meant to run in the browser on the hop graph (topic to idea to
   lessons), with no server and no AI, so that "nothing you paste leaves this device" stays literally
   true. Until it exists, matchSyllabus() answers `ready: false` and the box says so. Whoever builds
   it replaces the body of matchSyllabus() and keeps these shapes; it must fetch only fixed static
   files (never a URL that depends on the words typed). */

export interface MatchedLesson {
  slug: string;
  title: string;
  course: string;
  /** The Virginia standard the lesson teaches, when the data holds one ("BIO.3d"). */
  standard?: string;
}
export interface TopicMatch {
  /** The teacher's own line, as typed. */
  topic: string;
  lessons: MatchedLesson[];
  /** Set when nothing matched at the class's level and the nearest lessons are a level away. */
  hop?: { direction: 'down' | 'up'; levelTitle: string };
}
export type MatchResult = { ready: false } | { ready: true; levelTitle: string; topics: TopicMatch[] };

export async function matchSyllabus(_text: string, _level: string): Promise<MatchResult> {
  return { ready: false };
}
