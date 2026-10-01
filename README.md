# Rotating Text — Remotion project

A looping "I'm your [rotating word]" typewriter animation for automationwithsholz.com, exported as GIF at two sizes:
- **1920x100** — a thin banner strip (for embedding on the site)
- **1080x1080** — square, for social (prefix on its own line above the rotating word, since the longer phrases don't fit one line at a readable size on a 1:1 canvas)

## Edit the animation

Everything you'd want to tweak lives in **`config.ts`** at the project root — word list, colors, font, and all timing (typing speed, hold time, deleting speed, cursor blink). No need to touch anything in `src/`.

Font sizes in `config.ts` are caps, not fixed values — `src/fit.ts` automatically shrinks the rendered size if your longest word wouldn't fit the canvas width, so editing the word list never clips text off-screen.

## Setup

```bash
npm install
```

## Preview in the browser

```bash
npm run dev
```

Opens the Remotion Studio, where you can scrub both compositions (`RotatingText-Landscape`, `RotatingText-Square`) live as you edit `config.ts`.

## Render

```bash
npm run render
```

Renders both compositions and converts them straight to GIF — MP4 is only an intermediate step and is discarded. Output lands in `out/`:
- `rotating-text-1920x100.gif`
- `rotating-text-1080x1080.gif`

`scripts/render-gifs.sh` uses ffmpeg's two-pass palette workflow and automatically backs off fps/resolution/colors until each GIF is safely under 2MB.

## Font

Montserrat Bold, matching automationwithsholz.com — self-hosted from `public/fonts/montserrat-700.woff2` so rendering never depends on fetching from Google's font CDN.
