import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { BODY, C, HEAD, useLayout } from "../theme";

const LEAD = "If you built your own property directory,";
const ASK = "what would you search by first?";
const IDEAS = ["Price", "District", "MRT", "Size", "Tenure"];

// Closing question + channel name. No logo, text only.
export const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const lead = LEAD.split(" ");
  const ask = ASK.split(" ");
  const word = (w: string, i: number, delay: number, style: React.CSSProperties) => {
    const s = spring({ frame: frame - delay - i * 2, fps, config: { damping: 13, mass: 0.5 } });
    return (
      <span
        key={`${w}${i}`}
        style={{
          display: "inline-block",
          marginRight: "0.22em",
          opacity: interpolate(s, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
          transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px)`,
          ...style,
        }}
      >
        {w}
      </span>
    );
  };
  const askDelay = 6 + lead.length * 2 + 4;
  const ideasAt = askDelay + ask.length * 2 + 8;
  const brand = spring({ frame: frame - (ideasAt + 10), fps, config: { damping: 15 } });
  const idea = Math.floor(Math.max(0, frame - ideasAt) / 9) % IDEAS.length;
  return (
    <AbsoluteFill style={{ background: C.bg, alignItems: "center", justifyContent: "center", padding: L.square ? 70 : 80 }}>
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 42%, rgba(255,90,31,0.22) 0%, rgba(0,0,0,0) 55%)` }} />
      <div style={{ width: "100%", textAlign: "center", marginTop: L.square ? -60 : -160 }}>
        <div style={{ fontFamily: HEAD, fontSize: L.square ? 68 : 84, lineHeight: 1.08, color: C.white, textTransform: "uppercase" }}>
          {lead.map((w, i) => word(w, i, 6, {}))}
        </div>
        <div style={{ marginTop: 20, fontFamily: HEAD, fontSize: L.square ? 96 : 128, lineHeight: 1.02, color: C.accent, textTransform: "uppercase" }}>
          {ask.map((w, i) => word(w, i, askDelay, {}))}
        </div>
        {frame >= ideasAt && (
          <div style={{ marginTop: L.square ? 34 : 60, display: "flex", justifyContent: "center", gap: 14, flexWrap: "wrap" }}>
            {IDEAS.map((s, i) => (
              <div
                key={s}
                style={{
                  fontFamily: BODY,
                  fontWeight: 800,
                  fontSize: L.square ? 26 : 34,
                  textTransform: "uppercase",
                  letterSpacing: "0.06em",
                  padding: "10px 22px",
                  borderRadius: 999,
                  color: i === idea ? C.bg : C.white,
                  background: i === idea ? C.accent : "rgba(255,255,255,0.06)",
                  border: `2px solid ${i === idea ? C.accent : "rgba(255,255,255,0.16)"}`,
                }}
              >
                {s}?
              </div>
            ))}
          </div>
        )}
        {frame >= ideasAt && (
          <div style={{ marginTop: 26, fontFamily: BODY, fontWeight: 700, fontSize: L.square ? 24 : 30, color: C.gray, letterSpacing: "0.1em", textTransform: "uppercase" }}>
            Tell me in the comments ↓
          </div>
        )}
      </div>
      <div
        style={{
          position: "absolute",
          bottom: L.square ? 60 : 260,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          opacity: brand,
          transform: `translateY(${interpolate(brand, [0, 1], [30, 0])}px)`,
        }}
      >
        <div style={{ fontFamily: BODY, fontWeight: 900, fontSize: L.square ? 40 : 52, color: C.white, letterSpacing: "0.02em" }}>
          Automation With Sholz
        </div>
        <div style={{ marginTop: 12, height: 6, width: interpolate(brand, [0, 1], [0, L.square ? 260 : 340]), background: C.accent, borderRadius: 3 }} />
      </div>
    </AbsoluteFill>
  );
};
