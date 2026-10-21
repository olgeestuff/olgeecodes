import React from "react";
import { useVideoConfig } from "remotion";
import { Slam } from "../components/Kinetic";
import { Phone } from "../components/Phone";
import { Punch, SceneProps, cueAt } from "./shared";

// "Manage properties ... and let people search them."
export const Ask: React.FC<SceneProps> = (p) => {
  const { fps } = useVideoConfig();
  return (
    <Punch>
      <Slam
        lines={[
          { text: "Manage properties", at: cueAt(p, "manage", 0.1) },
          { text: "+ let people search", at: cueAt(p, "search", 0.5), accent: true },
        ]}
      />
      <Phone media={{ kind: "clip", src: "app/clip_listings.mp4", startFrom: Math.round(0.8 * fps), playbackRate: 1 }} />
    </Punch>
  );
};
