# Rotating Text — Remotion project

A looping "I am a [rotating word]" typewriter animation for automationwithsholz.com, rendered to MP4 and GIF at both 1920x1080 and 1080x1080.

## Edit the animation

Everything you'd want to tweak lives in **`config.ts`** at the project root — word list, colors, font, and all timing (typing speed, hold time, deleting speed, cursor blink). No need to touch anything in `src/`.

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
# MP4s (both sizes)
npm run render:mp4

# GIFs from the rendered MP4s (optimized, auto-capped under 2MB)
npm run render:gif

# Everything in one go
npm run render:all
```

Output lands in `out/`:
- `rotating-text-1920x1080.mp4` / `.gif`
- `rotating-text-1080x1080.mp4` / `.gif`

The GIF step (`scripts/render-gifs.sh`) uses ffmpeg's two-pass palette workflow and automatically backs off fps/resolution/colors if a GIF comes out over 2MB.

## Font

The heading font couldn't be pulled from automationwithsholz.com automatically (network-restricted sandbox), so `config.ts` ships with a safe system-font fallback (`Helvetica Neue, Arial, sans-serif`). To match the site exactly, update `fontFamily`/`fontWeight` in `config.ts` — see the comment above those fields for how to load a Google Font if needed.
