import React from "react";
import { useVideoConfig } from "remotion";
import { Chip, Slam } from "../components/Kinetic";
import { Phone } from "../components/Phone";
import { useLayout } from "../theme";
import { Punch, SceneProps, cueAt } from "./shared";

const FILTERS = [
  { key: "rent", label: "Rent / Buy" },
  { key: "district", label: "District" },
  { key: "price", label: "Price" },
  { key: "area", label: "Area" },
  { key: "availability", label: "Availability" },
];

// Search filters: chips pop in as each filter is named, over the real Search Pro screen recording.
export const Search: React.FC<SceneProps> = (p) => {
  const { fps } = useVideoConfig();
  const L = useLayout();
  const at = FILTERS.map((f, i) => cueAt(p, f.key, 0.15 + i * 0.15));
  return (
    <Punch>
      <Slam
        base={L.square ? 80 : 96}
        box={L.square ? { x: L.head.x, y: 110, w: L.head.w, h: 180 } : { x: L.head.x, y: 120, w: L.head.w, h: 150 }}
        lines={[{ text: "Search by…", at: cueAt(p, "searchby", 0.02) }]}
      />
      <div
        style={{
          position: "absolute",
          left: L.head.x,
          top: L.square ? 300 : 280,
          width: L.head.w,
          display: "flex",
          flexWrap: "wrap",
          flexDirection: L.square ? "column" : "row",
          alignItems: L.square ? "flex-start" : "center",
          justifyContent: "center",
          gap: L.square ? 18 : 16,
        }}
      >
        {FILTERS.map((f, i) => (
          <Chip key={f.key} label={f.label} at={at[i]} hot={i === FILTERS.length - 1} size={L.square ? 40 : 44} />
        ))}
      </div>
      <Phone media={{ kind: "clip", src: "app/clip_search.mp4", startFrom: Math.round(0.6 * fps), playbackRate: 1 }} />
    </Punch>
  );
};
