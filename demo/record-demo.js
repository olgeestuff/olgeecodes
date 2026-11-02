// Record a mobile-layout demo (1080x960, fills the top half of the final video) of an AppSheet app from a step script.
//
//   node record-demo.js scripts/video5.demo.yaml
//
// Output: "AI video editors/raw footage/<output>.webm" (e.g. "video 5 demo.webm").
// Step types (see scripts/example.demo.yaml):
//   goto: <url>                       open a page
//   tap: <visible text>               tap a button/row/tab showing that text
//   tap_selector: <css or role=...>   tap an exact element (copy from `npx playwright codegen`)
//   type: {into: <label/placeholder>, text: <what to type>}
//   scroll: <pixels>                  scroll the view (negative = up)
//   wait: <seconds>                   hold still (let the viewer read)
//   wait_for: <visible text>          wait until something appears
// Every step also accepts `hold: <seconds>` = pause after the step (default from settings.hold).
const fs = require('fs');
const path = require('path');
const YAML = require('yaml');
const { launch, PAGE_ZOOM, TAP_INDICATOR } = require('./browser');

const RAW = path.resolve(__dirname, '..', 'AI video editors', 'raw footage');

async function tapText(page, text) {
  const candidates = [
    page.getByRole('button', { name: text, exact: false }),
    page.getByRole('tab', { name: text, exact: false }),
    page.getByRole('link', { name: text, exact: false }),
    page.getByText(text, { exact: true }),
    page.getByText(text, { exact: false }),
  ];
  for (const loc of candidates) {
    const first = loc.first();
    if (await first.isVisible().catch(() => false)) {
      await first.scrollIntoViewIfNeeded().catch(() => {});
      return first.tap().catch(() => first.click());
    }
  }
  throw new Error(`Could not find anything showing "${text}" on screen`);
}

async function typeInto(page, into, text) {
  const loc = [page.getByLabel(into), page.getByPlaceholder(into), page.locator(into)];
  for (const l of loc) {
    const f = l.first();
    if (await f.isVisible().catch(() => false)) {
      await f.click();
      return f.pressSequentially(String(text), { delay: 70 }); // visible typing
    }
  }
  throw new Error(`Could not find an input for "${into}"`);
}

async function runStep(page, step, defHold) {
  const [kind] = Object.keys(step).filter(k => k !== 'hold' && k !== 'say');
  const v = step[kind];
  if (step.say) console.log(`   [${step.say}]`);
  switch (kind) {
    case 'goto': await page.goto(v, { waitUntil: 'networkidle' }).catch(() => {}); break;
    case 'tap': await tapText(page, v); break;
    case 'tap_selector': await page.locator(v).first().tap().catch(() => page.locator(v).first().click()); break;
    case 'type': await typeInto(page, v.into, v.text); break;
    case 'scroll': await page.mouse.wheel(0, Number(v)); break;
    case 'wait': await page.waitForTimeout(Number(v) * 1000); break;
    case 'wait_for': await page.getByText(v).first().waitFor({ timeout: 30000 }); break;
    default: throw new Error(`Unknown step: ${JSON.stringify(step)}`);
  }
  const hold = step.hold ?? (kind === 'wait' ? 0 : defHold);
  if (hold) await page.waitForTimeout(hold * 1000);
}

(async () => {
  const file = process.argv[2];
  if (!file) { console.log('Usage: node record-demo.js scripts/<name>.demo.yaml'); process.exit(1); }
  const spec = YAML.parse(fs.readFileSync(file, 'utf8'));
  const s = spec.settings || {};
  const tmp = path.join(__dirname, '.videos');
  fs.mkdirSync(tmp, { recursive: true });
  fs.mkdirSync(RAW, { recursive: true });

  // Load the app first WITHOUT recording, so the video starts on a ready screen.
  if (s.app_url) {
    const warm = await launch({ headless: false });
    const p = warm.pages()[0] || (await warm.newPage());
    await p.goto(s.app_url, { waitUntil: 'networkidle' }).catch(() => {});
    if (/accounts\.google\.com/.test(p.url())) {
      console.log('Not signed in — run: node save-login.js ' + s.app_url);
      await warm.close(); process.exit(1);
    }
    await warm.close();
  }

  const ctx = await launch({ record: tmp });
  await ctx.addInitScript(PAGE_ZOOM);
  await ctx.addInitScript(TAP_INDICATOR);
  const page = ctx.pages()[0] || (await ctx.newPage());
  const t0 = Date.now();
  if (s.app_url) {
    await page.goto(s.app_url, { waitUntil: 'networkidle' }).catch(() => {});
    await page.waitForTimeout((s.start_hold ?? 1.5) * 1000);
  }
  let ok = true;
  for (const [i, step] of (spec.steps || []).entries()) {
    try {
      console.log(`step ${i + 1}: ${JSON.stringify(step)}`);
      await runStep(page, step, s.hold ?? 1.2);
    } catch (e) {
      ok = false;
      console.error(`  ✗ step ${i + 1} failed: ${e.message}`);
      await page.screenshot({ path: path.join(tmp, `failed-step-${i + 1}.png`) });
      break;
    }
  }
  await page.waitForTimeout((s.end_hold ?? 1.5) * 1000);
  const secs = ((Date.now() - t0) / 1000).toFixed(1);
  const video = page.video();
  await ctx.close();
  const out = path.join(RAW, `${spec.output || path.basename(file, '.demo.yaml') + ' demo'}.webm`);
  fs.renameSync(await video.path(), out);
  console.log(`\n${ok ? '✓' : '⚠ partial'} demo saved: ${out}  (${secs}s)`);
  if (s.target_seconds) {
    console.log(`  narration length target: ${s.target_seconds}s — the editor speeds/holds the demo to fit.`);
  }
  if (!ok) process.exit(2);
})();
