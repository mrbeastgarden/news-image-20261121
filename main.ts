// The World in One Day — Saturday 21 November 2026.
//
// The front page is pre-rendered at build time (see draw.py in this repo:
// 45 verified stories, masthead, three leads, region list, world map and
// UTC timeline, drawn once with PIL into entry.png). This program only
// copies the finished image to the output directory, as the kit's
// RULES.txt suggests for a pre-rendered entry.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
// A copy is byte-identical by construction; the stat is only a sanity
// check that the file we shipped is the one that landed.
const { size } = statSync(dst);
console.log(`wrote ${dst} (${size} bytes)`);
