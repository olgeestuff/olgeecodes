import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import type { Section } from "../data/types";

export type SceneProps = {
  sec: Section;
  cues: Record<string, number>;
};

// Cue time relative to the section start; falls back to a fraction of the section when the cue is missing.
export const cueAt = (p: SceneProps, name: string, fallbackFrac: number): number => {
  const c = p.cues[name];
  const len = p.sec.e - p.sec.s;
  return c !== undefined ? c - p.sec.s : len * fallbackFrac;
};

// Quick punch-in on every cut so hard cuts feel intentional.
export const Punch: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 7], [1.07, 1], { extrapolateRight: "clamp" });
  const b = interpolate(frame, [0, 5], [10, 0], { extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ transform: `scale(${s})`, filter: b > 0.1 ? `blur(${b}px)` : undefined }}>{children}</AbsoluteFill>;
};
