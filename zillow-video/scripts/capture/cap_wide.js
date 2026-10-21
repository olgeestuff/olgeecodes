const { openApp, acceptIf } = require('./rec');
const A = process.argv[2], TMP = process.argv[3];
(async () => {
  const { browser, page } = await openApp({ width: 1600, height: 1000, mobile: false });
  await page.getByText('Modules', { exact: true }).last().click(); await page.waitForTimeout(4000);
  await page.mouse.click(604, 288); await page.waitForTimeout(5000); await acceptIf(page); await page.waitForTimeout(3000);
  await page.screenshot({ path: `${TMP}/desk_resi.png` });
  await page.mouse.click(212, 288); await page.waitForTimeout(6000); await acceptIf(page); await page.waitForTimeout(3000);
  await page.screenshot({ path: `${A}/wide_table.png` });
  // scroll horizontally to reveal more columns
  await page.mouse.move(800, 500);
  for (let i = 1; i <= 3; i++) { await page.mouse.wheel(1400, 0); await page.waitForTimeout(1200); await page.screenshot({ path: `${A}/wide_table_${i}.png` }); }
  await browser.close();
})();
