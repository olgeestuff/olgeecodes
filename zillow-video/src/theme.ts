import { useVideoConfig } from "remotion";

export const C = {
  bg: "#0A0B0D",
  bg2: "#15171C",
  line: "rgba(255,255,255,0.06)",
  accent: "#FF5A1F",
  accentSoft: "rgba(255,90,31,0.18)",
  white: "#F6F5F1",
  gray: "#8B9099",
  dim: "#4A4F58",
};

export const HEAD = "Anton, Impact, sans-serif";
export const BODY = "Inter, Arial, sans-serif";

// App screenshots/clips are 860x1864 (430x932 @2x).
export const SCREEN_RATIO = 860 / 1864;

export type Layout = {
  W: number;
  H: number;
  square: boolean;
  // Phone mockup screen rect (outer bezel added around it).
  phone: { cx: number; top: number; h: number; w: number };
  // Area for big kinetic headlines.
  head: { x: number; y: number; w: number; h: number; align: "center" | "left" };
  // Vertical centre of burned-in captions.
  capY: number;
  capSize: number;
  // Full stage for graphics-only scenes.
  stage: { x: number; y: number; w: number; h: number };
};

export const useLayout = (): Layout => {
  const { width: W, height: H } = useVideoConfig();
  const square = Math.abs(W - H) < 10;
  if (square) {
    const h = 840;
    return {
      W,
      H,
      square,
      phone: { cx: 790, top: 110, h, w: h * SCREEN_RATIO },
      head: { x: 60, y: 120, w: 520, h: 640, align: "left" },
      capY: 975,
      capSize: 54,
      stage: { x: 50, y: 120, w: W - 100, h: 760 },
    };
  }
  const h = 1010;
  return {
    W,
    H,
    square,
    phone: { cx: W / 2, top: 560, h, w: h * SCREEN_RATIO },
    head: { x: 60, y: 150, w: W - 120, h: 380, align: "center" },
    capY: 1470,
    capSize: 66,
    stage: { x: 60, y: 300, w: W - 120, h: 1100 },
  };
};
