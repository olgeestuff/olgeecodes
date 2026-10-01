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
  // TODO: automationwithsholz.com could not be reached from this sandbox
  // (blocked by network policy). This is a safe system-font fallback that
  // needs no network access to render reliably.
  //
  // To match your site exactly, replace fontFamily below with your heading
  // font (and fontWeight with its weight), e.g.:
  //   fontFamily: "'Poppins', sans-serif", fontWeight: 700
  // If it's a Google Font, also install it so it loads at render time:
  //   npm install @remotion/google-fonts
  // then in src/RotatingText.tsx:
  //   import {loadFont} from "@remotion/google-fonts/Poppins";
  //   loadFont();
  // (Loading a Google Font requires fetching it from Google's font CDN at
  // render time, which only works where that network access is allowed —
  // it will work fine on your own machine.)
  fontFamily: "'Helvetica Neue', Arial, sans-serif",
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
