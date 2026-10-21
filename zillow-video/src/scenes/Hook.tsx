import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Slam } from "../components/Kinetic";
import { BODY, C, useLayout } from "../theme";
import { Punch, SceneProps, cueAt } from "./shared";

// "Making a Zillow alternative for a Singaporean client. Back in 2023, somebody reached out..."
export const Hook: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const tZillow = cueAt(p, "zillow", 0.08);
  const tSg = cueAt(p, "singapore", 0.35);
  const tBack = cueAt(p, "back", 0.55);
  const t = frame / fps;
  const tag = spring({ frame, fps, config: { damping: 15 } });
  return (
    <Punch>
      <div
        style={{
          position: "absolute",
          top: L.square ? 36 : 80,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          opacity: tag,
          transform: `translateY(${interpolate(tag, [0, 1], [-30, 0])}px)`,
        }}
      >
        <div
          style={{
            fontFamily: BODY,
            fontWeight: 800,
            fontSize: L.square ? 26 : 32,
            letterSpacing: "0.08em",
            color: C.white,
            padding: "10px 22px",
            border: `2px solid ${C.accent}`,
            borderRadius: 999,
            textTransform: "uppercase",
          }}
        >
          My failed attempt at Zillow <span style={{ color: C.accent }}>— without AI</span>
        </div>
      </div>
      {t < tBack ? (
        <Slam
          box={L.stage}
          align="center"
          base={L.square ? 110 : 140}
          lines={[
            { text: "Making a", at: 0.05, size: 0.55, color: C.gray },
            { text: "Zillow", at: tZillow, size: 2.0 },
            { text: "alternative", at: cueAt(p, "alternative", 0.15), size: 0.9 },
            { text: "for Singapore", at: tSg, accent: true, size: 0.9 },
          ]}
        />
      ) : (
        <Slam
          box={L.stage}
          align="center"
          base={L.square ? 110 : 140}
          lines={[
            { text: "Back in", at: tBack, size: 0.55, color: C.gray },
            { text: "2023", at: cueAt(p, "2023", 0.65), size: 2.1, color: C.accent },
            { text: "a client", at: cueAt(p, "client", 0.75) },
            { text: "reached out", at: cueAt(p, "client", 0.75) + 0.25 },
          ]}
        />
      )}
    </Punch>
  );
};
