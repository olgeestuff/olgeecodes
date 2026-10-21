import React from "react";
import { Sequence, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Phone } from "../components/Phone";
import { C, HEAD, useLayout } from "../theme";
import { Punch, SceneProps, cueAt } from "./shared";

// "FAILED?" gets crossed out and replaced by "USED BY HIS TEAM".
export const Twist: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const t = frame / fps;
  const len = p.sec.e - p.sec.s;
  const tFailed = cueAt(p, "failure", 0.03);
  const tCross = cueAt(p, "notfailure", 0.3);
  const tTeam = cueAt(p, "team", 0.5);
  // After the reveal, lift the text to the top and bring the app in underneath.
  const tLift = Math.min(tTeam + 1.6, len - 1.5);
  const lift = spring({ frame: frame - Math.round(tLift * fps), fps, config: { damping: 16 } });
  const liftOn = len - tLift > 1.2;

  const f = spring({ frame: frame - Math.round(tFailed * fps), fps, config: { damping: 11, mass: 0.6 } });
  const strike = interpolate(t, [tCross, tCross + 0.28], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const used = spring({ frame: frame - Math.round(tTeam * fps), fps, config: { damping: 10, mass: 0.6 } });

  const bigY = L.square ? 260 : 620;
  const topY = L.square ? 130 : 150;
  const y = liftOn ? interpolate(lift, [0, 1], [bigY, topY]) : bigY;
  const scale = liftOn ? interpolate(lift, [0, 1], [1, L.square ? 0.62 : 0.55]) : 1;
  const failSize = L.square ? 210 : 250;

  return (
    <Punch>
      <div
        style={{
          position: "absolute",
          left: L.square && liftOn ? interpolate(lift, [0, 1], [0, -230]) : 0,
          right: 0,
          top: y,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `scale(${scale})`,
          transformOrigin: "50% 0%",
        }}
      >
        <div style={{ position: "relative", display: "inline-block" }}>
          <div
            style={{
              fontFamily: HEAD,
              fontSize: failSize,
              lineHeight: 1,
              color: strike > 0 ? C.dim : C.white,
              transform: `scale(${interpolate(f, [0, 1], [1.8, 1])})`,
              opacity: interpolate(f, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }),
              textTransform: "uppercase",
            }}
          >
            Failed?
          </div>
          <div
            style={{
              position: "absolute",
              left: "-6%",
              top: "48%",
              height: failSize * 0.11,
              width: "112%",
              background: C.accent,
              borderRadius: 999,
              transform: `rotate(-6deg) scaleX(${strike})`,
              transformOrigin: "0% 50%",
              boxShadow: `0 0 40px ${C.accentSoft}`,
            }}
          />
        </div>
        {t >= tTeam && (
          <div
            style={{
              marginTop: 30,
              fontFamily: HEAD,
              fontSize: L.square ? 108 : 124,
              lineHeight: 1,
              color: C.bg,
              background: C.accent,
              padding: "10px 30px 4px",
              textTransform: "uppercase",
              textAlign: "center",
              transform: `scale(${interpolate(used, [0, 1], [2, 1])}) rotate(${interpolate(used, [0, 1], [6, -2])}deg)`,
              opacity: interpolate(used, [0, 0.2], [0, 1], { extrapolateRight: "clamp" }),
              boxShadow: "0 30px 80px rgba(0,0,0,0.5)",
            }}
          >
            Used by his team
          </div>
        )}
      </div>
      {liftOn && (
        <Sequence from={Math.round(tLift * fps)} layout="none">
          <Phone media={{ kind: "clip", src: "app/clip_listings.mp4", startFrom: Math.round(12.5 * fps) }} />
        </Sequence>
      )}
    </Punch>
  );
};
