import { Config } from "@remotion/cli/config";
import fs from "node:fs";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

// Use the Chromium that's already installed in this environment instead of
// letting Remotion download its own headless browser (useful in sandboxes
// with restricted network access). Safe to leave in place on a normal
// machine too — it's a no-op if the path doesn't exist.
const preinstalledChromium = "/opt/pw-browsers/chromium";
if (fs.existsSync(preinstalledChromium)) {
  Config.setBrowserExecutable(preinstalledChromium);
  // Our preinstalled binary is a full Chromium build (new headless mode
  // only), not Remotion's "headless-shell" build — tell it to launch
  // accordingly.
  Config.setChromeMode("chrome-for-testing");
}
