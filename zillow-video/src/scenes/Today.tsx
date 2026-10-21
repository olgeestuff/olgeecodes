import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DirectoryIcon, GlobeIcon, SheetIcon } from "../components/Icons";
import { Slam } from "../components/Kinetic";
import { BODY, C, useLayout } from "../theme";
import { Punch, SceneProps, cueAt } from "./shared";

// Today: data -> Google Sheets -> your own directory.
export const Today: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const t = frame / fps;
  const nodes = [
    { label: "Web data", Icon: GlobeIcon, at: cueAt(p, "data2", 0.12) },
    { label: "Google Sheets", Icon: SheetIcon, at: cueAt(p, "sheets", 0.3) },
    { label: "Your directory", Icon: DirectoryIcon, at: cueAt(p, "directory", 0.62) },
  ];
  const nodeW = L.square ? 250 : 270;
  const arrowW = L.square ? 70 : 60;
  const rowY = L.square ? 380 : 700;
  return (
    <Punch>
      <Slam
        lines={[
          { text: "Today", at: cueAt(p, "today", 0.0), size: 1.5, color: C.accent },
          { text: "it's not an issue", at: cueAt(p, "notissue", 0.12), size: 0.6 },
        ]}
        box={L.square ? { x: 0, y: 70, w: L.W, h: 260 } : undefined}
        align="center"
      />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: rowY,
          display: "flex",
          justifyContent: "center",
          alignItems: "flex-start",
        }}
      >
        {nodes.map((n, i) => {
          const s = spring({ frame: frame - Math.round(n.at * fps), fps, config: { damping: 11, mass: 0.6 } });
          const visible = t >= n.at;
          const arrow = i > 0 ? interpolate(t, [n.at - 0.25, n.at], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
          return (
            <React.Fragment key={n.label}>
              {i > 0 && (
                <div style={{ width: arrowW, height: nodeW * 0.62, display: "flex", alignItems: "center" }}>
                  <div style={{ height: 8, width: "100%", background: C.accent, borderRadius: 4, transform: `scaleX(${arrow})`, transformOrigin: "0 50%", position: "relative" }}>
                    <div
                      style={{
                        position: "absolute",
                        right: -4,
                        top: -10,
                        width: 0,
                        height: 0,
                        borderTop: "14px solid transparent",
                        borderBottom: "14px solid transparent",
                        borderLeft: `20px solid ${C.accent}`,
                        opacity: arrow > 0.9 ? 1 : 0,
                      }}
                    />
                  </div>
                </div>
              )}
              <div
                style={{
                  width: nodeW,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 18,
                  opacity: visible ? interpolate(s, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }) : 0,
                  transform: `scale(${visible ? interpolate(s, [0, 1], [0.3, 1]) : 0.3})`,
                }}
              >
                <div
                  style={{
                    width: nodeW * 0.62,
                    height: nodeW * 0.62,
                    borderRadius: 36,
                    background: i === 2 ? C.accent : C.bg2,
                    border: `3px solid ${i === 2 ? C.accent : "rgba(255,255,255,0.14)"}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    boxShadow: i === 2 ? `0 0 70px ${C.accentSoft}` : "0 20px 50px rgba(0,0,0,0.5)",
                  }}
                >
                  <n.Icon size={nodeW * 0.36} color={i === 2 ? C.bg : C.accent} stroke={3.4} />
                </div>
                <div style={{ fontFamily: BODY, fontWeight: 800, fontSize: L.square ? 28 : 32, color: C.white, textAlign: "center", textTransform: "uppercase", letterSpacing: "0.04em" }}>
                  {n.label}
                </div>
              </div>
            </React.Fragment>
          );
        })}
      </div>
      <Slam
        box={L.square ? { x: 0, y: 700, w: L.W, h: 170 } : { x: 0, y: 1060, w: L.W, h: 260 }}
        align="center"
        base={L.square ? 84 : 104}
        lines={[
          { text: "Spin up your own", at: cueAt(p, "spin", 0.7) },
          { text: "property directory", at: cueAt(p, "spin", 0.7) + 0.2, accent: true },
        ]}
      />
    </Punch>
  );
};
