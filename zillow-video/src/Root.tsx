import "@fontsource/anton/400.css";
import "@fontsource/inter/700.css";
import "@fontsource/inter/800.css";
import "@fontsource/inter/900.css";
import React, { useEffect, useState } from "react";
import { Composition, continueRender, delayRender } from "remotion";
import edit from "./data/edit.json";
import type { Edit } from "./data/types";
import { Video } from "./Video";

const E = edit as Edit;
const FPS = E.fps;
const DURATION = Math.ceil((E.voice + E.endCard) * FPS);

// Hold rendering until the web fonts are ready so the first frames don't flash a fallback font.
const FontGate: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [handle] = useState(() => delayRender("fonts"));
  useEffect(() => {
    Promise.all(["400 100px Anton", "700 100px Inter", "800 100px Inter", "900 100px Inter"].map((f) => document.fonts.load(f)))
      .then(() => continueRender(handle))
      .catch(() => continueRender(handle));
  }, [handle]);
  return <>{children}</>;
};

const Main: React.FC = () => (
  <FontGate>
    <Video edit={E} />
  </FontGate>
);

export const Root: React.FC = () => (
  <>
    <Composition id="Vertical" component={Main} durationInFrames={DURATION} fps={FPS} width={1080} height={1920} />
    <Composition id="Square" component={Main} durationInFrames={DURATION} fps={FPS} width={1080} height={1080} />
  </>
);
