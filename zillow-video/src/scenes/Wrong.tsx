import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import {
  BuildingIcon,
  HdbIcon,
  IndustrialIcon,
  LandedIcon,
  NonLandedIcon,
  OfficeIcon,
  RetailIcon,
} from "../components/Icons";
import { Slam } from "../components/Kinetic";
import { Phone } from "../components/Phone";
import { BODY, C, HEAD, useLayout } from "../theme";
import { Punch, SceneProps, cueAt } from "./shared";

// In the order they're spoken.
const TILES = [
  { key: "nonlanded", label: "Non-landed", group: "Residential", Icon: NonLandedIcon },
  { key: "hdb", label: "HDB", group: "Residential", Icon: HdbIcon },
  { key: "landed", label: "Landed", group: "Residential", Icon: LandedIcon },
  { key: "retail", label: "Retail", group: "Commercial", Icon: RetailIcon },
  { key: "office", label: "Office", group: "Commercial", Icon: OfficeIcon },
  { key: "industrial", label: "Industrial", group: "Commercial", Icon: IndustrialIcon },
  { key: "buildings", label: "Whole buildings", group: "Commercial", Icon: BuildingIcon },
];

// Hero moment: "Residential / Commercial" -> "I was wrong" -> 7 property-type tiles burst out.
export const Wrong: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const t = frame / fps;
  const len = p.sec.e - p.sec.s;

  const tRes = cueAt(p, "residential", 0.05);
  const tCom = Math.max(cueAt(p, "commercial", 0.12), tRes + 0.2);
  const tWrong = cueAt(p, "wrong", 0.25);
  const tileAt = TILES.map((tile, i) => cueAt(p, tile.key, 0.4 + i * 0.045));
  const tBurst = Math.min(...tileAt);
  const tLast = Math.max(...tileAt);
  const tApp = p.cues.apptiles !== undefined ? cueAt(p, "apptiles", 1) : tLast + 1.4;
  const showApp = len - tApp > 1.8;

  // Stage geometry for the tile grid.
  const S = L.stage;
  const cols = L.square ? 4 : 2;
  const gap = L.square ? 22 : 30;
  const tw = (S.w - gap * (cols - 1)) / cols;
  const th = L.square ? 300 : 225;
  const rows = Math.ceil(TILES.length / cols);
  const gridH = rows * th + (rows - 1) * gap;
  const y0 = S.y + (S.h - gridH) / 2;
  const cx = L.W / 2;
  const cy = S.y + S.h / 2;
  const target = (i: number) => {
    const r = Math.floor(i / cols);
    const inRow = Math.min(cols, TILES.length - r * cols);
    const rowW = inRow * tw + (inRow - 1) * gap;
    const c = i - r * cols;
    return { x: (L.W - rowW) / 2 + c * (tw + gap), y: y0 + r * (th + gap) };
  };

  // Phase 1: the two words I thought were enough.
  const wordsOut = interpolate(t, [tBurst - 0.05, tBurst + 0.15], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const shake = t > tWrong && t < tBurst ? Math.sin(frame * 2.3) * interpolate(t, [tWrong, tWrong + 0.4], [16, 3], { extrapolateRight: "clamp" }) : 0;
  const word = (text: string, at: number) => {
    const s = spring({ frame: frame - Math.round(at * fps), fps, config: { damping: 12, mass: 0.6 } });
    if (t < at) return null;
    return (
      <div
        style={{
          fontFamily: HEAD,
          fontSize: L.square ? 150 : 170,
          lineHeight: 1,
          color: t > tWrong ? C.gray : C.white,
          textTransform: "uppercase",
          transform: `scale(${interpolate(s, [0, 1], [1.7, 1])})`,
          opacity: interpolate(s, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {text}
      </div>
    );
  };
  const stamp = spring({ frame: frame - Math.round(tWrong * fps), fps, config: { damping: 9, mass: 0.5 } });
  const flash = interpolate(t, [tBurst, tBurst + 0.35], [0.9, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ring = interpolate(t, [tBurst, tBurst + 0.7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const appIn = showApp ? interpolate(t, [tApp, tApp + 0.35], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;

  return (
    <Punch>
      {wordsOut > 0 && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: L.square ? 150 : 520,
            textAlign: "center",
            fontFamily: HEAD,
            fontSize: L.square ? 60 : 72,
            color: C.gray,
            textTransform: "uppercase",
            opacity: wordsOut * interpolate(t, [0, 0.25], [0, 1], { extrapolateRight: "clamp" }),
          }}
        >
          All I knew:
        </div>
      )}
      {wordsOut > 0 && (
        <AbsoluteFill
          style={{
            alignItems: "center",
            justifyContent: "center",
            opacity: wordsOut,
            transform: `translateX(${shake}px) scale(${interpolate(wordsOut, [0, 1], [1.5, 1])})`,
          }}
        >
          {word("Residential", tRes)}
          {t >= tCom && <div style={{ fontFamily: HEAD, fontSize: 90, color: C.accent, lineHeight: 1.1 }}>/</div>}
          {word("Commercial", tCom)}
          {t >= tWrong && (
            <div
              style={{
                position: "absolute",
                fontFamily: HEAD,
                fontSize: L.square ? 120 : 140,
                color: C.bg,
                background: C.accent,
                padding: "6px 34px 2px",
                textTransform: "uppercase",
                transform: `rotate(-8deg) scale(${interpolate(stamp, [0, 1], [2.4, 1])})`,
                opacity: interpolate(stamp, [0, 0.2], [0, 1], { extrapolateRight: "clamp" }),
                boxShadow: "0 30px 80px rgba(0,0,0,0.6)",
              }}
            >
              I was wrong
            </div>
          )}
        </AbsoluteFill>
      )}

      {t >= tBurst && (
        <>
          <div
            style={{
              position: "absolute",
              left: cx,
              top: cy,
              width: 10,
              height: 10,
              borderRadius: "50%",
              border: `${interpolate(ring, [0, 1], [30, 1])}px solid ${C.accent}`,
              transform: `translate(-50%,-50%) scale(${interpolate(ring, [0, 1], [1, 260])})`,
              opacity: 1 - ring,
            }}
          />
          <AbsoluteFill style={{ background: `radial-gradient(circle at 50% ${(cy / L.H) * 100}%, rgba(255,90,31,${flash}) 0%, rgba(0,0,0,0) 60%)` }} />
        </>
      )}

      <AbsoluteFill style={{ opacity: 1 - appIn * 0.82, filter: appIn > 0 ? `blur(${appIn * 6}px)` : undefined }}>
        {TILES.map((tile, i) => {
          const at = Math.max(tileAt[i], tBurst);
          if (t < at) return null;
          const s = spring({ frame: frame - Math.round(at * fps), fps, config: { damping: 12, mass: 0.7, stiffness: 140 } });
          const tg = target(i);
          const x = interpolate(s, [0, 1], [cx - tw / 2, tg.x]);
          const y = interpolate(s, [0, 1], [cy - th / 2, tg.y]);
          const rot = interpolate(s, [0, 1], [(i % 2 ? 1 : -1) * (25 + i * 6), 0]);
          const hot = interpolate(t, [at, at + 0.6], [1, 0], { extrapolateRight: "clamp" });
          return (
            <div
              key={tile.key}
              style={{
                position: "absolute",
                left: x,
                top: y,
                width: tw,
                height: th,
                borderRadius: 28,
                background: C.bg2,
                border: `3px solid ${hot > 0.05 ? C.accent : "rgba(255,255,255,0.12)"}`,
                boxShadow: `0 20px 50px rgba(0,0,0,0.55), 0 0 ${60 * hot}px rgba(255,90,31,${0.5 * hot})`,
                transform: `rotate(${rot}deg) scale(${interpolate(s, [0, 1], [0.2, 1])})`,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 10,
              }}
            >
              <tile.Icon size={th * 0.38} color={C.accent} stroke={3.2} />
              <div style={{ fontFamily: HEAD, fontSize: L.square ? 40 : 52, color: C.white, textTransform: "uppercase", lineHeight: 1, textAlign: "center" }}>
                {tile.label}
              </div>
              <div style={{ fontFamily: BODY, fontWeight: 700, fontSize: L.square ? 16 : 20, letterSpacing: "0.14em", color: C.gray, textTransform: "uppercase" }}>
                {tile.group}
              </div>
            </div>
          );
        })}
      </AbsoluteFill>

      {showApp && t >= tApp && (
        <>
          <Slam lines={[{ text: "7 types.", at: tApp }, { text: "One app.", at: tApp + 0.25, accent: true }]} />
          <Phone media={{ kind: "img", src: "app/commercial_tiles.png" }} enterDelay={Math.round(tApp * fps)} />
        </>
      )}
    </Punch>
  );
};
