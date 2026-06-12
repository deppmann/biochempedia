import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { lessonSchema } from './schema';

// Astro 5 Content Layer. Each lesson lives in its own folder under
// src/content/lessons/<slug>/lesson.mdx (one folder per lesson — copy a folder
// to start a new one; see CONTRIBUTING.md). The schema in src/schema.ts is the
// integrity gate: a lesson that violates it fails `astro build`.
const lessons = defineCollection({
  loader: glob({
    pattern: '**/lesson.mdx',
    base: './src/content/lessons',
  }),
  schema: lessonSchema,
});

export const collections = { lessons };
