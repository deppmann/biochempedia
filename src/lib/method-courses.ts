import { COURSES } from '../data/courses';
import { METHODS } from '../data/methods';

/** Methods has a page only for courses whose visible lessons use at least one method, so no course page is empty. */
export function methodCourses(lessons: readonly { id?: string; slug?: string; data: { course: string } }[]) {
  const used = new Set(METHODS.flatMap((m) => m.lessons ?? []));
  const withMethods = new Set(
    lessons.filter((l) => used.has(String(l.slug ?? l.id ?? '').replace(/\/lesson(\.mdx?)?$/, ''))).map(({ data }) => data.course),
  );
  return COURSES.filter((course) => withMethods.has(course.slug));
}
