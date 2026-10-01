import type { RotatingTextConfig } from "../config";

export type Phase = "typing" | "holding" | "deleting" | "pausing";

export interface WordState {
  phase: Phase;
  word: string;
  visibleChars: number;
  wordIndex: number;
}

const msToFrames = (ms: number, fps: number) => Math.max(1, Math.round((ms / 1000) * fps));

interface Segment {
  word: string;
  wordIndex: number;
  typingFrames: number;
  holdFrames: number;
  deletingFrames: number;
  pauseFrames: number;
  total: number;
}

const buildSegments = (config: RotatingTextConfig, fps: number): Segment[] => {
  const charFramesTyping = msToFrames(config.typingSpeedMs, fps);
  const charFramesDeleting = msToFrames(config.deletingSpeedMs, fps);
  const holdFrames = msToFrames(config.holdMs, fps);
  const pauseFrames = msToFrames(config.pauseBeforeNextMs, fps);

  return config.words.map((word, wordIndex) => {
    const typingFrames = charFramesTyping * word.length;
    const deletingFrames = charFramesDeleting * word.length;
    return {
      word,
      wordIndex,
      typingFrames,
      holdFrames,
      deletingFrames,
      pauseFrames,
      total: typingFrames + holdFrames + deletingFrames + pauseFrames,
    };
  });
};

export const getTotalCycleFrames = (config: RotatingTextConfig, fps: number): number =>
  buildSegments(config, fps).reduce((sum, seg) => sum + seg.total, 0);

export const getWordState = (frame: number, config: RotatingTextConfig, fps: number): WordState => {
  const segments = buildSegments(config, fps);
  const totalCycle = segments.reduce((sum, seg) => sum + seg.total, 0);
  let localFrame = ((frame % totalCycle) + totalCycle) % totalCycle;

  for (const seg of segments) {
    if (localFrame < seg.typingFrames) {
      const charFrames = seg.typingFrames / seg.word.length;
      const visibleChars = Math.min(seg.word.length, Math.floor(localFrame / charFrames) + 1);
      return { phase: "typing", word: seg.word, visibleChars, wordIndex: seg.wordIndex };
    }
    localFrame -= seg.typingFrames;

    if (localFrame < seg.holdFrames) {
      return { phase: "holding", word: seg.word, visibleChars: seg.word.length, wordIndex: seg.wordIndex };
    }
    localFrame -= seg.holdFrames;

    if (localFrame < seg.deletingFrames) {
      const charFrames = seg.deletingFrames / seg.word.length;
      const deleted = Math.min(seg.word.length, Math.floor(localFrame / charFrames) + 1);
      return {
        phase: "deleting",
        word: seg.word,
        visibleChars: Math.max(0, seg.word.length - deleted),
        wordIndex: seg.wordIndex,
      };
    }
    localFrame -= seg.deletingFrames;

    if (localFrame < seg.pauseFrames) {
      return { phase: "pausing", word: seg.word, visibleChars: 0, wordIndex: seg.wordIndex };
    }
    localFrame -= seg.pauseFrames;
  }

  const last = segments[segments.length - 1];
  return { phase: "pausing", word: last.word, visibleChars: 0, wordIndex: last.wordIndex };
};
