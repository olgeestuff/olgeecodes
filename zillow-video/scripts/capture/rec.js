// Shared capture helpers: open the AppSheet app with privacy blur + tap ripple, record CDP screencast clips.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const APP = 'https://www.appsheet.com/start/95b02b16-28ce-4268-8b17-1cdcb66e5b14';

// Runs in the page before any app script. CSS hides contact columns before first paint;
// the MutationObserver catches stray phone numbers / emails anywhere else.
const PRIVACY = `
(() => {
  const css = \`
    [data-testonly-column^="Contact"] .TextTypeDisplay__text,
    [data-testonly-column^="Contact"] .SlideshowPage__value,
    [data-testonly-column^="Contact"] .BaseTypeDisplay span,
    .__pii { filter: blur(9px) !important; color: #444 !important; user-select: none; }
    .__tap { position: fixed; width: 56px; height: 56px; margin: -28px 0 0 -28px; border-radius: 50%;
      background: rgba(255,90,31,0.35); border: 3px solid rgba(255,90,31,0.9); pointer-events: none; z-index: 2147483647;
      animation: __tap 650ms ease-out forwards; }
    @keyframes __tap { 0% { transform: scale(0.4); opacity: 1 } 100% { transform: scale(1.6); opacity: 0 } }
  \`;
  const addStyle = () => { if (!document.head) return false; const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s); return true; };
  if (!addStyle()) document.addEventListener('DOMContentLoaded', addStyle);
  const PII = /(\\+?\\d[\\d\\s-]{6,}\\d)|([\\w.+-]+@[\\w-]+\\.[\\w.]+)/;
  const scan = (root) => {
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) { const t = n.nodeValue; if (t && PII.test(t) && n.parentElement && !n.parentElement.closest('style,script')) n.parentElement.classList.add('__pii'); }
  };
  new MutationObserver(ms => { for (const m of ms) { if (m.type === 'characterData') { if (PII.test(m.target.nodeValue||'') && m.target.parentElement) m.target.parentElement.classList.add('__pii'); } else m.addedNodes.forEach(nd => { if (nd.nodeType === 1) scan(nd); else if (nd.nodeType === 3 && PII.test(nd.nodeValue||'') && nd.parentElement) nd.parentElement.classList.add('__pii'); }); } })
    .observe(document, { childList: true, subtree: true, characterData: true });
  window.addEventListener('pointerdown', e => { const d = document.createElement('div'); d.className = '__tap'; d.style.left = e.clientX + 'px'; d.style.top = e.clientY + 'px'; document.body.appendChild(d); setTimeout(() => d.remove(), 700); }, true);
})();
`;

async function openApp({ width = 430, height = 932, mobile = true } = {}) {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 2, isMobile: mobile, hasTouch: mobile,
    userAgent: mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined });
  await ctx.addInitScript({ content: PRIVACY });
  const page = await ctx.newPage();
  await page.goto(APP, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.getByText(/^accept$/i).first().click({ timeout: 60000 });
  await page.waitForTimeout(7000);
  return { browser, ctx, page };
}

async function acceptIf(page) {
  const acc = page.getByText(/^accept$/i);
  if (await acc.count() && await acc.first().isVisible()) { await acc.first().click(); await page.waitForTimeout(6000); }
}

// Smooth human-ish scroll inside the app's scroll container.
async function scroll(page, dy, ms = 1200, x = 215, y = 520) {
  await page.mouse.move(x, y);
  const steps = Math.max(1, Math.round(ms / 33));
  for (let i = 0; i < steps; i++) {
    const t0 = i / steps, t1 = (i + 1) / steps;
    const ease = t => 0.5 - 0.5 * Math.cos(Math.PI * t);
    await page.mouse.wheel(0, dy * (ease(t1) - ease(t0)));
    await page.waitForTimeout(33);
  }
}

async function startRec(page, dir) {
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const client = await page.context().newCDPSession(page);
  const frames = [];
  client.on('Page.screencastFrame', async ({ data, metadata, sessionId }) => {
    const f = path.join(dir, `f${String(frames.length).padStart(5, '0')}.jpg`);
    fs.writeFileSync(f, Buffer.from(data, 'base64'));
    frames.push({ f, t: metadata.timestamp });
    try { await client.send('Page.screencastFrameAck', { sessionId }); } catch {}
  });
  await client.send('Page.startScreencast', { format: 'jpeg', quality: 92, everyNthFrame: 1 });
  return { client, frames, dir, t0: Date.now() / 1000 };
}

// Stop and assemble a constant-30fps MP4 from the variable-rate frames.
async function stopRec(rec, outMp4) {
  const tEnd = Date.now() / 1000;
  await rec.client.send('Page.stopScreencast');
  const fr = rec.frames;
  const lines = [];
  for (let i = 0; i < fr.length; i++) {
    const next = i + 1 < fr.length ? fr[i + 1].t : tEnd;
    lines.push(`file '${fr[i].f}'`, `duration ${Math.max(0.001, next - fr[i].t).toFixed(4)}`);
  }
  lines.push(`file '${fr[fr.length - 1].f}'`);
  const list = path.join(rec.dir, 'list.txt'); fs.writeFileSync(list, lines.join('\n'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-vf', 'fps=30,scale=860:-2,format=yuv420p',
    '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', outMp4]);
  console.log('clip', outMp4, fr.length, 'frames', (tEnd - fr[0].t).toFixed(1) + 's');
}

module.exports = { openApp, acceptIf, scroll, startRec, stopRec };
