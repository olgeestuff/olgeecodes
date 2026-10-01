import React from "react";
import { Composition } from "remotion";
import { config } from "../config";
import { RotatingText } from "./RotatingText";
import { getTotalCycleFrames } from "./timing";

export const RemotionRoot: React.FC = () => {
  const { fps } = config;
  const durationInFrames = getTotalCycleFrames(config, fps);

  return (
    <>
      <Composition
        id="RotatingText-Landscape"
        component={RotatingText}
        durationInFrames={durationInFrames}
        fps={fps}
        width={1920}
        height={1080}
        defaultProps={{ fontSize: config.fontSizeLandscape }}
      />
      <Composition
        id="RotatingText-Square"
        component={RotatingText}
        durationInFrames={durationInFrames}
        fps={fps}
        width={1080}
        height={1080}
        defaultProps={{ fontSize: config.fontSizeSquare }}
      />
    </>
  );
};
