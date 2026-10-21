import React from "react";
import { Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, useLayout } from "../theme";

type Media =
  | { kind: "img"; src: string }
  | { kind: "clip"; src: string; startFrom?: number; playbackRate?: number };

// iPhone-style mockup holding an app screenshot or screen recording.
// Slides up on entry; `zoom` lets a scene push in on part of the screen.
export const Phone: React.FC<{
  media: Media;
  enterDelay?: number;
  zoom?: { scale: number; originY: number };
  tilt?: number;
}> = ({ media, enterDelay = 0, zoom, tilt = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const p = spring({ frame: frame - enterDelay, fps, config: { damping: 16, mass: 0.8 } });
  const y = interpolate(p, [0, 1], [L.H * 0.35, 0]);
  const bezel = Math.round(L.phone.w * 0.045);
  const radius = L.phone.w * 0.13;
  const w = L.phone.w + bezel * 2;
  const h = L.phone.h + bezel * 2;
  const floatY = Math.sin(frame / 22) * 5;
  return (
    <div
      style={{
        position: "absolute",
        left: L.phone.cx - w / 2,
        top: L.phone.top - bezel,
        width: w,
        height: h,
        transform: `translateY(${y + floatY}px) rotate(${tilt}deg)`,
        opacity: interpolate(p, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }),
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: -40,
          borderRadius: radius + 40,
          background: `radial-gradient(ellipse at center, ${C.accentSoft} 0%, rgba(0,0,0,0) 70%)`,
          filter: "blur(20px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: radius,
          background: "linear-gradient(145deg, #2A2D33 0%, #121418 60%, #23262B 100%)",
          boxShadow: "0 40px 90px rgba(0,0,0,0.7), inset 0 0 0 2px rgba(255,255,255,0.08)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: bezel,
          top: bezel,
          width: L.phone.w,
          height: L.phone.h,
          borderRadius: radius - bezel,
          overflow: "hidden",
          background: "#fff",
        }}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            transform: zoom ? `scale(${zoom.scale})` : undefined,
            transformOrigin: zoom ? `50% ${zoom.originY * 100}%` : undefined,
          }}
        >
          {media.kind === "img" ? (
            <Img src={staticFile(media.src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          ) : (
            <OffthreadVideo
              src={staticFile(media.src)}
              startFrom={media.startFrom ?? 0}
              playbackRate={media.playbackRate ?? 1}
              muted
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          )}
        </div>
      </div>
    </div>
  );
};
