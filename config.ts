/**
 * Single source of truth for the rotating-text animation.
 * Edit anything here — words, colors, timing, fonts — without touching animation code.
 */

export const config = {
  // --- Text content ---
  prefix: "I am a",
  words: [
    "partner",
    "developer",
    "Google AppSheet expert",
    "technical support",
    "technical partner",
  ],

  // --- Colors ---
  colors: {
    background: "#FFFFFF",
    text: "#000000",
    cursor: "#000000",
  },

  // --- Typography ---
  // Montserrat Bold, self-hosted from public/fonts/montserrat-700.woff2
  // (via @fontsource/montserrat) and loaded in src/RotatingText.tsx.
  // Fallbacks after it only kick in if the font file is ever missing.
  // To use a different weight, copy the matching file from
  // node_modules/@fontsource/montserrat/files/ into public/fonts/,
  // update the @font-face src in src/RotatingText.tsx, and set
  // fontWeight below to match.
  fontFamily: "'Montserrat', 'Helvetica Neue', Arial, sans-serif",
  fontWeight: 700,
  fontSizeLandscape: 100, // px, for the 1920x1080 composition
  fontSizeSquare: 80, // px, for the 1080x1080 composition

  // --- Timing ---
  fps: 30,
  typingSpeedMs: 60, // ms per character while typing in
  deletingSpeedMs: 40, // ms per character while deleting
  holdMs: 1000, // ms to hold the fully-typed word before deleting
  pauseBeforeNextMs: 300, // ms of empty pause after deleting, before next word types in
  cursorBlinkMs: 500, // ms per blink half-cycle (on/off)
};

export type RotatingTextConfig = typeof config;
