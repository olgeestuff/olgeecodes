// Montserrat Bold's average character width is roughly 0.6x its font size.
// Used to size text to fit a target pixel width without measuring the DOM
// (which isn't reliable across Remotion's per-frame headless renders).
const CHAR_WIDTH_RATIO = 0.6;

/**
 * Returns the largest font size (capped at maxFontSize) at which `text`
 * fits within `targetWidthPx`. Keeps long config edits (a longer word, a
 * longer prefix) from silently clipping off-canvas.
 */
export const fitFontSize = (text: string, maxFontSize: number, targetWidthPx: number): number => {
  const estimatedWidthAtMax = text.length * CHAR_WIDTH_RATIO * maxFontSize;
  if (estimatedWidthAtMax <= targetWidthPx) {
    return maxFontSize;
  }
  return Math.floor(targetWidthPx / (text.length * CHAR_WIDTH_RATIO));
};
