import { readRecord } from '../../scripts/production-record.mjs';

interface LessonRecord {
  slug: string;
  levelUp?: { shipped?: string };
  sideHops?: { updated: string };
  films: { id: string; durationSec: number | null }[];
}

const rows: LessonRecord[] = readRecord(process.cwd());
const records = new Map(rows.map((row) => [row.slug, row]));

export const recordFor = (slug: string) => records.get(slug);
