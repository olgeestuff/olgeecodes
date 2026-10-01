import React from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/fonts";
import { config } from "../config";
import { getWordState } from "./timing";
import { fitFontSize } from "./fit";

void loadFont({
  family: "Montserrat",
  url: staticFile("fonts/montserrat-700.woff2"),
  weight: "700",
  style: "normal",
});

export interface RotatingTextProps {
  fontSize?: number;
  // "inline": prefix and word share one centered line (the landscape banner).
  // "stacked": prefix sits above the word on its own line, each auto-sized
  // to fit — used for the square export, where the longer phrases in
  // config.words don't fit one line at a readable size on a 1:1 canvas.
  layout?: "inline" | "stacked";
}

const msToFrames = (ms: number, fps: number) => Math.max(1, Math.round((ms / 1000) * fps));

// Leaves ~4% margin on each side so text never touches the canvas edge.
const MARGIN_FRACTION = 0.92;

export const RotatingText: React.FC<RotatingTextProps> = ({
  fontSize = config.fontSizeLandscape,
  layout = "inline",
}) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();

  const { word, visibleChars } = getWordState(frame, config, fps);
  const typedPart = word.slice(0, visibleChars);

  const cursorBlinkFrames = msToFrames(config.cursorBlinkMs, fps);
  const cursorVisible = Math.floor(frame / cursorBlinkFrames) % 2 === 0;

  const targetWidthPx = width * MARGIN_FRACTION;
  // Longest string any word in the loop can produce — used by the "stacked"
  // (square) layout so its font size stays constant across the whole loop
  // instead of jumping per word.
  const longestWord = config.words.reduce((a, b) => (b.length > a.length ? b : a), "");

  const cursor = (
    <span
      style={{
        color: config.colors.cursor,
        opacity: cursorVisible ? 1 : 0,
      }}
    >
      |
    </span>
  );

  if (layout === "stacked") {
    const wordFontSize = fitFontSize(`${longestWord}__`, fontSize, targetWidthPx);
    const prefixFontSize = Math.round(wordFontSize * 0.55);

    return (
      <AbsoluteFill
        style={{
          backgroundColor: config.colors.background,
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <div
          style={{
            fontFamily: config.fontFamily,
            fontWeight: config.fontWeight,
            fontSize: prefixFontSize,
            color: config.colors.text,
            marginBottom: Math.round(wordFontSize * 0.25),
          }}
        >
          {config.prefix}
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            fontFamily: config.fontFamily,
            fontWeight: config.fontWeight,
            fontSize: wordFontSize,
            color: config.colors.text,
            whiteSpace: "pre",
          }}
        >
          <span>{typedPart}</span>
          <span style={{ marginLeft: Math.round(wordFontSize * 0.04) }}>{cursor}</span>
        </div>
      </AbsoluteFill>
    );
  }

  // Fit to the CURRENT word rather than the longest in the list, so on a
  // narrow banner width most words render large and only the one longest
  // phrase shrinks to fit — sizing is still constant for a given word's
  // whole type/hold/delete cycle (it only changes between words, during the
  // blank pause when nothing is drawn), so there's no mid-word jitter.
  const fittedFontSize = fitFontSize(`${config.prefix} ${word}__`, fontSize, targetWidthPx);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: config.colors.background,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "baseline",
          fontFamily: config.fontFamily,
          fontWeight: config.fontWeight,
          fontSize: fittedFontSize,
          color: config.colors.text,
          whiteSpace: "pre",
        }}
      >
        <span>{config.prefix}&nbsp;</span>
        <span>{typedPart}</span>
        <span style={{ marginLeft: Math.round(fittedFontSize * 0.04) }}>{cursor}</span>
      </div>
    </AbsoluteFill>
  );
};
