import React from "react";
import { AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Background } from "./components/Background";
import { Captions } from "./components/Captions";
import type { Edit, Section } from "./data/types";
import { Ask } from "./scenes/Ask";
import { EndCard } from "./scenes/EndCard";
import { Hook } from "./scenes/Hook";
import { Search } from "./scenes/Search";
import type { SceneProps } from "./scenes/shared";
import { Today } from "./scenes/Today";
import { Twist } from "./scenes/Twist";
import { Wall } from "./scenes/Wall";
import { Wrong } from "./scenes/Wrong";
import { C } from "./theme";

const SCENES: Record<Section["id"], React.FC<SceneProps>> = {
  hook: Hook,
  ask: Ask,
  wrong: Wrong,
  search: Search,
  wall: Wall,
  twist: Twist,
  today: Today,
};

const Progress: React.FC<{ total: number }> = ({ total }) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        top: 0,
        height: 8,
        width: `${interpolate(frame, [0, total], [0, 100], { extrapolateRight: "clamp" })}%`,
        background: C.accent,
      }}
    />
  );
};

export const Video: React.FC<{ edit: Edit }> = ({ edit }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const voiceEnd = Math.round(edit.voice * fps);
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      <Background />
      <Audio src={staticFile("audio/voice.wav")} />
      {edit.sections.map((sec) => {
        const Scene = SCENES[sec.id];
        const from = Math.round(sec.s * fps);
        return (
          <Sequence key={sec.id} from={from} durationInFrames={Math.round(sec.e * fps) - from} name={sec.id}>
            <Scene sec={sec} cues={edit.cues} />
          </Sequence>
        );
      })}
      <Sequence from={voiceEnd} name="end card">
        <EndCard />
      </Sequence>
      <Captions words={edit.words} until={edit.voice} />
      <Progress total={durationInFrames} />
    </AbsoluteFill>
  );
};
