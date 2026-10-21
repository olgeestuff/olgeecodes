const { openApp, acceptIf, scroll, startRec, stopRec } = require('./rec');
const A = process.argv[2], TMP = process.argv[3];
(async () => {
  { const { browser, page } = await openApp();
    await page.getByText('Modules', { exact: true }).last().click(); await page.waitForTimeout(4000);
    await page.mouse.click(105, 190); await page.waitForTimeout(4000); await acceptIf(page); await page.waitForTimeout(4000);
    await page.screenshot({ path: `${A}/commercial_tiles.png` });
    await browser.close(); }
  { const { browser, page } = await openApp({ width: 1600, height: 1000, mobile: false });
    await page.screenshot({ path: `${TMP}/desk_home.png` });
    await page.getByText('Modules', { exact: true }).last().click(); await page.waitForTimeout(4000);
    await page.screenshot({ path: `${TMP}/desk_modules.png` });
    console.log((await page.evaluate(() => document.body.innerText)).slice(0, 400));
    await browser.close(); }
})();
