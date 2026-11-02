// Shared browser setup: real Google Chrome + a dedicated profile folder that stays signed in.
const path = require('path');
const { chromium } = require('playwright');

const PROFILE_DIR = path.join(__dirname, '.chrome-profile'); // gitignored — holds your login
// The demo fills the TOP HALF of a 1080x1920 video = 1080x960 px.
// We record a 1080x960 window and zoom the page 2x, so the app shows its phone/mobile layout
// (540 css px wide) but is captured at full sharpness. Playwright records at window size.
const WINDOW = { width: 1080, height: 960 };
const ZOOM = 2;

async function launch({ record = null, headless = false } = {}) {
  const opts = {
    channel: 'chrome',              // use installed Chrome: Google sign-in accepts it
    headless,
    viewport: WINDOW,
    deviceScaleFactor: 1,
    hasTouch: true,
    userAgent:
      'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 ' +
      '(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    ignoreDefaultArgs: ['--enable-automation'],
    args: ['--disable-blink-features=AutomationControlled'],
  };
  if (record) {
    opts.recordVideo = { dir: record, size: WINDOW };
  }
  try {
    return await chromium.launchPersistentContext(PROFILE_DIR, opts);
  } catch (e) {
    if (String(e).includes('chrome')) {
      console.log('Google Chrome not found — falling back to Playwright Chromium.');
      delete opts.channel;
      return chromium.launchPersistentContext(PROFILE_DIR, opts);
    }
    throw e;
  }
}

// Zooms every page so the app lays out like a phone screen.
const PAGE_ZOOM = `
  (() => { const z = () => { if (document.documentElement) document.documentElement.style.zoom = '${ZOOM}'; };
    z(); document.addEventListener('DOMContentLoaded', z); })();`;

// Shows a soft circle wherever the demo taps, so viewers can follow the clicks.
const TAP_INDICATOR = `
  window.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.textContent = '.__tap{position:fixed;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;' +
      'background:rgba(255,214,10,.55);border:3px solid rgba(255,214,10,.95);pointer-events:none;z-index:2147483647;' +
      'transition:transform .35s ease-out, opacity .35s ease-out}';
    document.head.appendChild(style);
    const show = (x, y) => {
      const d = document.createElement('div'); d.className = '__tap';
      const z = parseFloat(document.documentElement.style.zoom) || 1;
      d.style.left = x / z + 'px'; d.style.top = y / z + 'px'; document.body.appendChild(d);
      requestAnimationFrame(() => { d.style.transform = 'scale(1.6)'; d.style.opacity = '0'; });
      setTimeout(() => d.remove(), 450);
    };
    window.addEventListener('pointerdown', e => show(e.clientX, e.clientY), true);
    window.addEventListener('touchstart', e => { const t = e.touches[0]; if (t) show(t.clientX, t.clientY); }, true);
  });`;

module.exports = { launch, PROFILE_DIR, WINDOW, PAGE_ZOOM, TAP_INDICATOR };
