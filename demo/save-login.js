// One-time login. Opens Chrome; sign in to Google + open your AppSheet app,
// then press Enter in this terminal. The login is kept in demo/.chrome-profile.
// Re-run whenever a recording lands on the Google sign-in page instead of your app.
//
//   node save-login.js https://www.appsheet.com/start/<your-app-id>
const readline = require('readline');
const { launch } = require('./browser');

(async () => {
  const url = process.argv[2] || 'https://www.appsheet.com/';
  const ctx = await launch();
  const page = ctx.pages()[0] || (await ctx.newPage());
  await page.goto(url);
  console.log('\nSign in with the Google account that owns the app (e.g. Office Geek).');
  console.log('When the app is open and working, come back here and press Enter.\n');
  await new Promise(r => readline.createInterface({ input: process.stdin }).once('line', r));
  await ctx.close();
  console.log('Saved. You can now run: node record-demo.js scripts/<name>.demo.yaml');
})();
