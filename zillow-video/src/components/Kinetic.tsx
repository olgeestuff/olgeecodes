import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { C, HEAD, useLayout } from "../theme";

export type Line = {
  text: string;
  at: number; // seconds, relative to the enclosing Sequence
  accent?: boolean; // filled accent box behind the text
  size?: number; // multiplier on the base headline size
  color?: string;
};

export type Box = { x: number; y: number; w: number; h: number };

// Big condensed headline lines that slam in one after another.
export const Slam: React.FC<{ lines: Line[]; out?: number; box?: Box; align?: "center" | "left"; base?: number }> = ({
  lines,
  out,
  box,
  align,
  base,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const size = base ?? (L.square ? 84 : 112);
  const t = frame / fps;
  const exit = out !== undefined ? interpolate(t, [out, out + 0.2], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
  if (exit <= 0) return null;
  const b = box ?? L.head;
  const al = align ?? L.head.align;
  return (
    <div
      style={{
        position: "absolute",
        left: b.x,
        top: b.y,
        width: b.w,
        height: b.h,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: al === "center" ? "center" : "flex-start",
        gap: size * 0.08,
        opacity: exit,
        transform: `scale(${interpolate(exit, [0, 1], [0.92, 1])})`,
      }}
    >
      {lines.map((l, i) => {
        const p = spring({ frame: frame - Math.round(l.at * fps), fps, config: { damping: 13, mass: 0.6, stiffness: 160 } });
        if (frame < l.at * fps) return null;
        const fs = size * (l.size ?? 1);
        return (
          <div
            key={i}
            style={{
              fontFamily: HEAD,
              fontSize: fs,
              lineHeight: l.accent ? 1.12 : 1.0,
              textTransform: "uppercase",
              color: l.accent ? C.bg : l.color ?? C.white,
              transform: `scale(${interpolate(p, [0, 1], [1.6, 1])}) rotate(${interpolate(p, [0, 1], [i % 2 ? 3 : -3, 0])}deg)`,
              opacity: interpolate(p, [0, 0.25], [0, 1], { extrapolateRight: "clamp" }),
              filter: `blur(${interpolate(p, [0, 0.6], [10, 0], { extrapolateRight: "clamp" })}px)`,
              textAlign: al,
              textShadow: l.accent ? "none" : "0 8px 30px rgba(0,0,0,0.6)",
            }}
          >
            {/* Inline span + cloned box decoration keeps the accent box hugging each wrapped line. */}
            <span
              style={{
                background: l.accent ? C.accent : "transparent",
                padding: l.accent ? `${fs * 0.03}px ${fs * 0.14}px 0` : 0,
                boxDecorationBreak: "clone",
                WebkitBoxDecorationBreak: "clone",
              }}
            >
              {l.text}
            </span>
          </div>
        );
      })}
    </div>
  );
};

// Small rounded label used for filter chips and tags.
export const Chip: React.FC<{ label: string; at: number; icon?: React.ReactNode; hot?: boolean; size?: number }> = ({
  label,
  at,
  icon,
  hot,
  size = 40,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = spring({ frame: frame - Math.round(at * fps), fps, config: { damping: 11, mass: 0.5 } });
  if (frame < at * fps) return <div style={{ visibility: "hidden", fontSize: size, padding: `${size * 0.3}px ${size * 0.55}px` }}>{label}</div>;
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: size * 0.3,
        padding: `${size * 0.3}px ${size * 0.55}px`,
        borderRadius: 999,
        fontFamily: HEAD,
        fontSize: size,
        letterSpacing: "0.02em",
        textTransform: "uppercase",
        color: hot ? C.bg : C.white,
        background: hot ? C.accent : "rgba(255,255,255,0.06)",
        border: `3px solid ${hot ? C.accent : "rgba(255,255,255,0.18)"}`,
        transform: `scale(${interpolate(p, [0, 1], [0.3, 1])})`,
        opacity: interpolate(p, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }),
        boxShadow: hot ? `0 0 40px ${C.accentSoft}` : "none",
      }}
    >
      {icon}
      {label}
    </div>
  );
};
