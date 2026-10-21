const { openApp, acceptIf, scroll, startRec, stopRec } = require('./rec');
const A = process.argv[2], TMP = process.argv[3];
(async () => {
  const { browser, page } = await openApp();
  await page.getByText('Modules', { exact: true }).last().click(); await page.waitForTimeout(4000);
  await page.screenshot({ path: `${A}/modules.png` });
  // Residential -> Private Non Landed list
  await page.mouse.click(320, 190); await page.waitForTimeout(5000); await acceptIf(page); await page.waitForTimeout(3000);
  await page.screenshot({ path: `${A}/residential_tiles.png` });
  await page.mouse.click(105, 190); await page.waitForTimeout(6000); await acceptIf(page); await page.waitForTimeout(2000);
  await page.screenshot({ path: `${A}/listings_table.png` });
  const rec = await startRec(page, `${TMP}/rec_listings`);
  await page.waitForTimeout(1200);
  await scroll(page, 900, 2500); await page.waitForTimeout(600);
  await scroll(page, -900, 1500); await page.waitForTimeout(700);
  await page.mouse.click(150, 132); await page.waitForTimeout(2500);
  await scroll(page, 700, 2200); await page.waitForTimeout(900);
  await stopRec(rec, `${A}/clip_listings.mp4`);
  await scroll(page, -2000, 600); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${A}/detail_top.png` });
  await scroll(page, 560, 600); await page.waitForTimeout(1200);
  await page.screenshot({ path: `${A}/detail_mid.png` });
  await browser.close();
})();
