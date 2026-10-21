import React, { useMemo } from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { Word } from "../data/types";
import { BODY, C, useLayout } from "../theme";

type Page = { words: Word[]; s: number; e: number };

const clean = (w: string) => w.trim().replace(/[.,;:]+$/g, "").replace(/^["“]|["”]$/g, "").toUpperCase();

// Group words into short caption pages: break on sentence ends, pauses, or length.
const paginate = (words: Word[], maxWords: number, maxChars: number): Page[] => {
  const pages: Page[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) pages.push({ words: cur, s: cur[0].s, e: cur[cur.length - 1].e });
    cur = [];
  };
  words.forEach((w, i) => {
    const prev = words[i - 1];
    const chars = cur.reduce((n, x) => n + clean(x.w).length + 1, 0) + clean(w.w).length;
    if (cur.length && (cur.length >= maxWords || chars > maxChars || (prev && w.s - prev.e > 0.45))) flush();
    cur.push(w);
    if (/[.?!]$/.test(w.w.trim())) flush();
  });
  flush();
  // Hold each page until the next one starts (short gaps) so captions don't flicker.
  pages.forEach((p, i) => {
    const next = pages[i + 1];
    p.e = next && next.s - p.e < 0.6 ? next.s : p.e + 0.3;
  });
  return pages;
};

export const Captions: React.FC<{ words: Word[]; until: number }> = ({ words, until }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const L = useLayout();
  const t = frame / fps;
  const pages = useMemo(() => paginate(words, L.square ? 4 : 3, L.square ? 22 : 16), [words, L.square]);
  if (t >= until) return null;
  const page = pages.find((p) => t >= p.s && t < p.e);
  if (!page) return null;
  const enter = spring({ frame: frame - Math.round(page.s * fps), fps, config: { damping: 14, mass: 0.5 } });
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        top: L.capY,
        display: "flex",
        justifyContent: "center",
        transform: `translateY(-50%) scale(${interpolate(enter, [0, 1], [0.86, 1])})`,
        opacity: interpolate(enter, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
      }}
    >
      <div
        style={{
          maxWidth: L.W - 120,
          padding: `${L.capSize * 0.22}px ${L.capSize * 0.45}px`,
          borderRadius: L.capSize * 0.35,
          background: "rgba(10,11,13,0.88)",
          boxShadow: "0 18px 40px rgba(0,0,0,0.45)",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: `0 ${L.capSize * 0.42}px`,
          fontFamily: BODY,
          fontWeight: 900,
          fontSize: L.capSize,
          lineHeight: 1.12,
          letterSpacing: "-0.01em",
        }}
      >
        {page.words.map((w, i) => {
          const next = page.words[i + 1];
          const active = t >= w.s && (next ? t < next.s : true);
          const spoken = t >= w.s;
          const pop = spring({ frame: frame - Math.round(w.s * fps), fps, config: { damping: 12, mass: 0.4 } });
          return (
            <span
              key={i}
              style={{
                color: active ? C.accent : spoken ? C.white : "rgba(246,245,241,0.55)",
                transform: active ? `scale(${interpolate(pop, [0, 1], [1.06, 1.02])})` : "scale(1)",
                display: "inline-block",
              }}
            >
              {clean(w.w)}
            </span>
          );
        })}
      </div>
    </div>
  );
};
