"""Build one HyperFrames project per filmed card.  python3 make.py <key>"""
import sys, json, os, shutil, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

ROOT = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(ROOT)
FONTS = os.path.join(ROOT, "node_modules/@fontsource/poppins/files")

def fix_words(words, fixes):
    out = []
    i = 0
    while i < len(words):
        matched = False
        for src, dst in fixes:
            n = len(src)
            seq = [w["w"].strip().strip(",.?!").lower() for w in words[i:i+n]]
            if seq == [s.lower() for s in src]:
                trail = words[i+n-1]["w"].strip()[-1:] if words[i+n-1]["w"].strip()[-1:] in ",.?!" else ""
                for k, d in enumerate(dst):
                    w = dict(words[min(i+k, i+n-1)]); w["w"] = d + (trail if k == len(dst)-1 else "")
                    if k == len(dst)-1: w["e"] = words[i+n-1]["e"]
                    out.append(w)
                i += n; matched = True; break
        if not matched:
            out.append(words[i]); i += 1
    return out

SPECS = {
"B01-02": dict(src="2026_11_19_11_30_43", start=1.2, end=92.3, objpos="22%", bright=True,
  fixes=[(["an","own"],["and","own"]), (["thank","you","very","much","but"],["thank","you","very","much."])],
  scenes=[
    (1.2, price("$15,000", "just to get started with software, for 45 units", "Illustrative scenario")),
    (12.3, compare({"icon":"puzzle","title":"Option A","body":"Covers only part of the workflow","tag":"Gaps"},
                   {"icon":"building","title":"Option B","body":"Huge all-in-one system + onboarding costs","tag":"Bloat"},
                   right_at=6.5, foot="A difficult choice for a small portfolio")),
    (40.8, title("Your turn", "What would you advise him to do?", icon="chat", hl="advise")),
    (46.0, quote("The lesson isn't that every big platform is overpriced.", "Software should fit your operation.", hl="fit", at2=6.4)),
    (58.2, title("Sometimes the missing piece is", "a focused workflow app", sub="not another all-in-one system. One that grows and scales with you.", icon="flow", hl="focused workflow app")),
    (72.6, chips("That's where I come in", [("Google AppSheet","flow",0.8),("Google Sheets","sheet",1.4),("Apps Script","bolt",2.0)],
                 foot="Operate better now. Move smoothly to the next level.", foot_at=7.0)),
    (86.0, cta("Full platform, or fix the one workflow causing the most friction?")),
  ]),
"B01-03": dict(src="2026_11_19_11_40_09", start=0.5, end=83.3, objpos="28%",
  fixes=[(["meta"],["meter"]), (["App","Sheets"],["AppSheet"]), (["it's","free","to"],["is","for","you","to"]),
         (["it","could","be"],["I","could","be"])],
  scenes=[
    (0.5, chat("Every month, every unit", [("in","text","Hi! Here's this month's meter reading",0.6),
                                           ("in","meter","04527",5.3), ("out","text","Thanks, logging it now",7.2)])),
    (8.76, title("Step 1", "Identify the reading", sub="04527 kWh", icon="eye")),
    (11.78, sheet("Find the previous number. Enter the new one.", ["Unit","Month","Reading"],
                  [["4A","Oct","03112"],["4B","Oct","04398"],["5A","Oct","02870"]], hl_row=1, hl_at=0.5,
                  add_row=["4B","Nov","04527"], add_at=2.4)),
    (15.92, calc("Calculate the charge", [("04527 − 04398",0.2),("= 129 kWh × tariff",0.8)], "Charge calculated ✓", 1.4)),
    (17.78, months("Then repeat it next month", "None of these steps looks huge. Together they eat attention, and get missed.", 9.0)),
    (34.14, quote("Cost sometimes goes beyond money.", "It's attention and time.", hl="attention", at2=3.3)),
    (41.56, form("Capture it once, in one workflow", [("Property / Unit","Maple Court · 4B",0.8),("Meter photo","PHOTO",1.8),
                 ("Reading","04527 kWh",2.8),("Submitted","19 Nov · 09:42",3.8)], "Sent for review", 5.0)),
    (53.44, chips("Free tools in your Google account", [("Google Sheets","sheet",3.2),("Google AppSheet","flow",4.6),("Google Apps Script","bolt",5.6)])),
    (60.92, dashboard("Captured the same way, across your team", [("4B","Meter reading · submitted",0.5),("2A","Repair task · done",1.3),
                      ("7C","Meter reading · in review",2.1),("1","Consistent process",3.0)])),
    (72.66, cta("What recurring 10-minute admin task keeps coming back in your portfolio?")),
  ]),
"B01-04": dict(src="2026_11_19_15_04_08", start=5.38, end=74.4, objpos="30%",
  fixes=[(["least"],["lease"]), (["at","least","date"],["a","lease","date"]), (["app","sheet"],["AppSheet"]),
         (["google"],["Google"]), (["i"],["I"])],
  scenes=[
    (5.38, sheet("A lease date sits in a spreadsheet", ["Unit","Tenant","Lease end"],
                 [["2A","J. Okafor","31 Jan"],["3C","M. Diaz","14 Mar"],["4B","A. Chen","02 Dec"],["5D","R. Patel","19 Jun"]],
                 hl_row=2, hl_at=1.2)),
    (8.8, scattered("Important dates live in different places",
                    [("sheet","Spreadsheet","Lease end: 02 Dec","",0.2),("phone","Phone note","“Call A. Chen about renewal”","",1.0),
                     ("calendar","Calendar","Reminder never created","miss",2.4)],
                    "…or it only lives in someone's memory", 4.6)),
    (15.6, urgent("Renewal due in 6 days!", "Now the team is chasing a renewal that should have been on the radar weeks ago.", 2.0)),
    (28.0, quote("The problem isn't memory.", "It's visibility.", hl="visibility", at2=4.4)),
    (33.4, alert("One place, for every stakeholder", [("Unit","Maple Court · 4B",0.6),("Lease end","02 Dec 2026",1.4),
                 ("Responsible","Ada · Property Manager",2.4),("Next action","Send renewal offer",3.6)], "Renewal due in 60 days", 0)),
    (44.6, chips("Scattered information hurts", [("Property managers","building",3.0),("Inventory teams","sheet",5.0)],
                 foot="It's alarming.", foot_at=8.5)),
    (55.0, chips("The fix often already sits in your Google account", [("Google Sheets","sheet",2.8),("Google AppSheet","flow",5.0)],
                 foot="A system that shows your team what's coming, before it happens", foot_at=8.0)),
    (68.14, cta("Where do your lease renewal reminders live today?")),
  ]),
"B01-10": dict(src="2026_11_19_15_10_28", start=0.2, end=67.2, objpos="30%",
  transcript="transcripts",
  fixes=[(["Charles"],["Sholz"]), (["trap"],["track"]), (["for","the","UN","person"],["for","you"])],
  scenes=[
    (0.2, nots("Software won't…", [("Inspect a leaking roof","roof",3.0),("Build trust with a contractor","hand",8.0),
                                    ("Replace good judgment","brain",11.0)])),
    (13.7, title("Not even AI", "That part is ours.", sub="Human judgment stays human.", icon="user", hl="ours")),
    (15.9, checklist("But it can help you", [("Record requests",0.9),("Assign responsibility",3.0),
                                              ("Track progress",4.7),("Keep evidence together",6.4)])),
    (23.4, title("So you can focus on", "Building trust & making jobs easier", icon="hand", hl="trust")),
    (33.3, quote("The goal isn't to remove humans from property management.", "It's to stop you having to remember everything.",
                 hl="remember everything", at2=5.4)),
    (44.3, title("The result", "You stay in control.", icon="eye", hl="in control")),
    (47.6, cta("What should software handle, and what should always stay human?",
               line="I'm Sholz. I build systems with Google AppSheet for property & inventory management.")),
  ]),
}

def main(key):
    sp = SPECS[key]
    proj = os.path.join(ROOT, key); os.makedirs(os.path.join(proj, "assets/fonts"), exist_ok=True)
    for f in os.listdir(FONTS):
        if f.startswith("poppins-latin-") and f.endswith("-normal.woff2") and f.split("-")[2] in ("400","600","700","800"):
            shutil.copy(os.path.join(FONTS, f), os.path.join(proj, "assets/fonts", f))
    s0, s1 = sp["start"], sp["end"]
    D = round(s1 - s0, 2)
    talk = os.path.join(proj, "assets/talk.mp4")
    if not os.path.exists(talk):
        vf = "scale=720:1280,setsar=1" + (",eq=brightness=0.05:gamma=1.45:saturation=1.1" if sp.get("bright") else "")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(s0), "-to", str(s1),
                        "-i", os.path.join(B, "raw", sp["src"] + ".mp4"), "-vf", vf, "-r", "30",
                        "-c:v", "libx264", "-crf", "18", "-g", "30", "-pix_fmt", "yuv420p",
                        "-af", "highpass=f=80,loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "48000",
                        "-c:a", "aac", "-b:a", "192k", talk], check=True)
    words = json.load(open(os.path.join(B, sp.get("transcript", "transcripts_med"), sp["src"] + ".words.json")))
    words = fix_words(words, sp["fixes"])
    words = [dict(w, s=round(w["s"] - s0, 2), e=round(w["e"] - s0, 2)) for w in words if w["s"] >= s0 - 0.05 and w["e"] <= s1 + 0.3]
    for w in words: w["s"] = max(w["s"], 0)
    spec = {"card": key, "duration": D, "objpos": sp["objpos"],
            "scenes": [{"t": max(round(t - s0, 2), 0), "html": h} for t, h in sp["scenes"]]}
    build(spec, words, os.path.join(proj, "index.html"))
    json.dump(words, open(os.path.join(proj, "captions.json"), "w"), indent=0)
    for f in ("hyperframes.json", "meta.json"):
        if not os.path.exists(os.path.join(proj, f)):
            shutil.copy(os.path.join(ROOT, "test", f), os.path.join(proj, f))
    print(key, "built, duration", D, "words", len(words))

if __name__ == "__main__":
    for k in sys.argv[1:]: main(k)
