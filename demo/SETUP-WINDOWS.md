# Demo recorder: Windows setup

Records your AppSheet app being clicked through, sized to fill the top half of the video
(1080×960, AppSheet's mobile layout, sharp). Each run takes about 15 minutes to set up once.

## 1. Install (once)
Open **PowerShell**:
```
winget install OpenJS.NodeJS.LTS
winget install Git.Git
```
Close and reopen PowerShell, then:
```
git clone https://github.com/olgeestuff/olgeecodes.git
cd olgeecodes\demo
npm install
```
It uses your installed **Google Chrome** (Google sign-in blocks other automated browsers).

## 2. Sign in (once, then whenever Google logs you out)
```
node save-login.js https://www.appsheet.com/start/YOUR-APP-ID
```
Chrome opens. Sign in with the account that owns the app (e.g. Office Geek) and wait until the app loads.
Then press **Enter** in PowerShell. The login is saved in `demo\.chrome-profile` (private and never committed).
Close any other Chrome window that uses this profile before recording.

## 3. Write the demo steps
Copy `scripts\example.demo.yaml` to `scripts\video5.demo.yaml` and edit:
- `output: video 5 demo` pairs it with `video 5 narration`
- `app_url:` your app link
- `steps:` one line per tap or type, in the order the narration talks about them. Use `hold:` to stay on a
  screen while you're still talking about it.

Not sure what a button is called? Run this and click around. It prints each element's name:
```
npx playwright codegen --channel chrome --viewport-size=540,480 https://www.appsheet.com/start/YOUR-APP-ID
```

## 4. Record
```
node record-demo.js scripts\video5.demo.yaml
```
→ `AI video editors\raw footage\video 5 demo.webm`. Upload it to the Drive folder next to the narration.
If a step fails, the recorder saves a screenshot in `demo\.videos\failed-step-N.png` showing what was on screen.

Timing doesn't have to be perfect. The editor speeds the demo up (max 2×) or holds the last frame to match the narration length.
