import React from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/fonts";
import { config } from "../config";
import { getWordState } from "./timing";

void loadFont({
  family: "Montserrat",
  url: staticFile("fonts/montserrat-700.woff2"),
  weight: "700",
  style: "normal",
});

export interface RotatingTextProps {
  fontSize?: number;
}

const msToFrames = (ms: number, fps: number) => Math.max(1, Math.round((ms / 1000) * fps));

export const RotatingText: React.FC<RotatingTextProps> = ({ fontSize = config.fontSizeLandscape }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const { word, visibleChars } = getWordState(frame, config, fps);
  const typedPart = word.slice(0, visibleChars);

  const cursorBlinkFrames = msToFrames(config.cursorBlinkMs, fps);
  const cursorVisible = Math.floor(frame / cursorBlinkFrames) % 2 === 0;

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
          fontSize,
          color: config.colors.text,
          whiteSpace: "pre",
        }}
      >
        <span>{config.prefix}&nbsp;</span>
        <span>{typedPart}</span>
        <span
          style={{
            color: config.colors.cursor,
            opacity: cursorVisible ? 1 : 0,
            marginLeft: Math.round(fontSize * 0.04),
          }}
        >
          |
        </span>
      </div>
    </AbsoluteFill>
  );
};
