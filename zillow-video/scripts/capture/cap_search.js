const { openApp, acceptIf, scroll, startRec, stopRec } = require('./rec');
const A = process.argv[2], TMP = process.argv[3];
async function typeInto(page, label, text) {
  const lab = page.locator(`text="${label}" >> visible=true`).first();
  const box = await lab.boundingBox(); if (!box) { console.log('no label', label); return; }
  await page.mouse.click(250, box.y + box.height / 2); await page.waitForTimeout(400);
  await page.keyboard.press('Control+A'); await page.keyboard.type(text, { delay: 120 }); await page.waitForTimeout(300);
}
(async () => {
  const { browser, page } = await openApp();
  const rec = await startRec(page, `${TMP}/rec_search`);
  await page.waitForTimeout(1200);
  await page.mouse.click(347, 260); await page.waitForTimeout(1100);   // Sale
  await page.mouse.click(214, 260); await page.waitForTimeout(1100);   // back to Rent
  await page.mouse.click(280, 406); await page.waitForTimeout(1300);   // Private Non Landed
  await scroll(page, 600, 1400); await page.waitForTimeout(600);
  const nl = page.locator('text="Non Landed Property Type" >> visible=true').first();
  const nb = await nl.boundingBox();
  await page.mouse.click(300, nb.y + nb.height / 2); await page.waitForTimeout(1300);
  await page.mouse.click(115, 85); await page.waitForTimeout(800);     // Condominium
  await page.mouse.click(368, 878); await page.waitForTimeout(1200);   // Done
  const dd = page.locator('text=District >> visible=true').first();
  const box = await dd.boundingBox();
  await page.mouse.click(300, box.y + box.height / 2); await page.waitForTimeout(1500);
  await page.mouse.click(150, 180); await page.waitForTimeout(900);    // D1
  await page.mouse.click(352, 878); await page.waitForTimeout(1300);   // Done
  await scroll(page, 120, 500); await page.waitForTimeout(400);
  await typeInto(page, 'Price Starts From', '2000');
  await typeInto(page, 'Price Ends At', '15000');
  await page.mouse.click(400, 120); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${A}/search_price.png` });
  await scroll(page, 1500, 2600); await page.waitForTimeout(1500);
  await page.screenshot({ path: `${A}/search_results.png` });
  await stopRec(rec, `${A}/clip_search.mp4`);
  console.log('TEXT', (await page.evaluate(() => document.body.innerText)).slice(-900));
  await browser.close();
})();
