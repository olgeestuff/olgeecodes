import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Slam } from "../components/Kinetic";
import { Phone } from "../components/Phone";
import { BODY, C, useLayout } from "../theme";
import { Punch, SceneProps, cueAt } from "./shared";

// "2023. A client reached out ... a Zillow alternative for Singapore."
export const Hook: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const tZillow = cueAt(p, "zillow", 0.5);
  const tSg = cueAt(p, "singapore", 0.7);
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
      {t < tZillow ? (
        <Slam
          box={L.stage}
          align="center"
          base={L.square ? 120 : 150}
          lines={[
            { text: "2023", at: cueAt(p, "2023", 0.02), size: 2.1, color: C.accent },
            { text: "A client", at: cueAt(p, "client", 0.15) },
            { text: "reached out", at: cueAt(p, "reached", 0.22) },
          ]}
        />
      ) : (
        <>
          <Slam
            lines={[
              { text: "A Zillow alternative", at: tZillow },
              { text: "for Singapore", at: tSg, accent: true },
            ]}
          />
          <Phone media={{ kind: "img", src: "app/modules.png" }} enterDelay={Math.round(tZillow * fps)} />
        </>
      )}
    </Punch>
  );
};
