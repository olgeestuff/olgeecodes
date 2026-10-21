import React from "react";
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Slam } from "../components/Kinetic";
import { BODY, C, HEAD, useLayout } from "../theme";
import { Punch, SceneProps, cueAt } from "./shared";

const STRIP = ["app/wide_table.png", "app/wide_table_1.png", "app/wide_table_2.png", "app/wide_table_3.png"];

// The wall: the listing data didn't exist in a usable form — it had to be scraped (URA).
export const Wall: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const t = frame / fps;
  const len = p.sec.e - p.sec.s;
  const tScraped = cueAt(p, "scraped", 0.3);
  const tUra = cueAt(p, "ura", 0.65);
  const imgH = L.square ? 640 : 1000;
  const imgW = imgH * 1.6;
  const pan = interpolate(t, [0, len], [0, -imgW * 2.2]);
  const ura = spring({ frame: frame - Math.round(tUra * fps), fps, config: { damping: 10, mass: 0.6 } });
  const jolt = t > tScraped ? Math.sin((t - tScraped) * 60) * interpolate(t, [tScraped, tScraped + 0.3], [14, 0], { extrapolateRight: "clamp" }) : 0;
  return (
    <Punch>
      <AbsoluteFill style={{ perspective: 1800, overflow: "hidden" }}>
        <div
          style={{
            position: "absolute",
            left: L.W * 0.1,
            top: L.square ? 300 : 620,
            display: "flex",
            gap: 0,
            transform: `rotateX(28deg) rotateZ(-10deg) translateX(${pan}px) translateY(${jolt}px)`,
            transformOrigin: "0 0",
            filter: "saturate(0.6) brightness(0.8)",
            opacity: 0.75,
          }}
        >
          {STRIP.map((s) => (
            <Img key={s} src={staticFile(s)} style={{ width: imgW, height: imgH, objectFit: "cover", borderRadius: 18 }} />
          ))}
        </div>
        <AbsoluteFill
          style={{
            background: `linear-gradient(180deg, ${C.bg} 0%, rgba(10,11,13,0.92) 26%, rgba(10,11,13,0.35) 55%, rgba(10,11,13,0.85) 100%)`,
          }}
        />
      </AbsoluteFill>
      <Slam
        lines={[
          { text: "The data?", at: cueAt(p, "data", 0.05) },
          { text: "Had to be scraped", at: tScraped, accent: true },
        ]}
      />
      {t >= tUra && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: L.square ? 640 : 820,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            transform: `scale(${interpolate(ura, [0, 1], [2, 1])}) rotate(${interpolate(ura, [0, 1], [-10, -3])}deg)`,
            opacity: interpolate(ura, [0, 0.25], [0, 1], { extrapolateRight: "clamp" }),
          }}
        >
          <div
            style={{
              fontFamily: HEAD,
              fontSize: L.square ? 150 : 210,
              lineHeight: 1,
              color: C.white,
              border: `8px solid ${C.accent}`,
              padding: "10px 40px 0",
              borderRadius: 24,
              background: "rgba(10,11,13,0.8)",
            }}
          >
            URA
          </div>
          <div style={{ marginTop: 16, fontFamily: BODY, fontWeight: 800, fontSize: L.square ? 22 : 30, letterSpacing: "0.12em", color: C.gray, textTransform: "uppercase" }}>
            Urban Redevelopment Authority
          </div>
        </div>
      )}
    </Punch>
  );
};
