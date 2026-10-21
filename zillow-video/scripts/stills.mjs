// Render preview stills at given seconds for both compositions: node scripts/stills.mjs out/stills 3 12.5 ...
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
import fs from "node:fs";

const [outDir, ...secs] = process.argv.slice(2);
const comps = (process.env.COMPS ?? "Vertical,Square").split(",");
fs.mkdirSync(outDir, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const browserExecutable = process.env.REMOTION_BROWSER ?? null;
for (const id of comps) {
  const composition = await selectComposition({ serveUrl, id, browserExecutable });
  for (const s of secs) {
    const frame = Math.min(composition.durationInFrames - 1, Math.round(Number(s) * composition.fps));
    const output = path.join(outDir, `${id}_${String(s).replace(".", "_")}.jpg`);
    await renderStill({ serveUrl, composition, frame, output, imageFormat: "jpeg", jpegQuality: 85, browserExecutable });
    console.log(output);
  }
}
