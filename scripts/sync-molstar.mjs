// Copies the prebuilt Mol* standalone viewer out of node_modules and into
// public/vendor/molstar/ so it can be loaded by a plain <script> tag.
//
// Why vendor a prebuilt bundle instead of importing `molstar` directly?
// The npm `molstar` package ships its compiled sources under lib/ with no
// package `exports` map, so a bare `import 'molstar'` does not resolve, and
// pulling the full plugin UI through Vite drags in React + SCSS. The package
// ALSO ships a self-contained UMD build (build/viewer/molstar.js) that exposes
// `window.molstar.Viewer` — exactly the rotatable viewer we want. We copy that
// build verbatim; nothing about the structure is generated or modified.
//
// The copied files are gitignored and regenerated on every `npm run dev` /
// `npm run build` (see the predev/prebuild hooks in package.json), so the repo
// stays small and the viewer version always tracks the installed dependency.
import { cp, mkdir, access } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const src = join(root, 'node_modules', 'molstar', 'build', 'viewer');
const dest = join(root, 'public', 'vendor', 'molstar');

const files = ['molstar.js', 'molstar.css', 'molstar.js.LICENSE.txt'];

try {
  await access(src);
} catch {
  console.error(
    '[sync-molstar] Could not find node_modules/molstar/build/viewer. ' +
      'Run `npm install` first.'
  );
  process.exit(1);
}

await mkdir(dest, { recursive: true });
for (const f of files) {
  await cp(join(src, f), join(dest, f));
}
console.log(`[sync-molstar] Copied Mol* viewer bundle → public/vendor/molstar/`);
