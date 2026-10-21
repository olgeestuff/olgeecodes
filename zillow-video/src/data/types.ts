// Shape of src/data/edit.json, produced by scripts/build_edit.py from the word-level transcript.
export type Word = { w: string; s: number; e: number };

export type Section = {
  id: "hook" | "ask" | "wrong" | "search" | "wall" | "twist" | "today";
  s: number;
  e: number;
};

export type Edit = {
  fps: number;
  // Length of the edited voice track in seconds (end card follows it).
  voice: number;
  endCard: number;
  words: Word[];
  sections: Section[];
  // Named moments (seconds on the edited timeline) that graphics sync to.
  cues: Record<string, number>;
};
