"""Scene components + HyperFrames page builder for Batch 01 split-screen videos.
Top panel = animated visuals (per production card), bottom = talking-head footage,
captions = word-by-word highlight across the seam.
Every element with data-at="<sec>" animates in at that time (offset inside its scene).
"""
import json, html

W, H, TOP = 1080, 1920, 940          # top visual panel 0..TOP, footage TOP..H

# ------------------------------------------------------------------ icons (inline SVG)
def ic(name, size=64, color="currentColor"):
    p = {
        "building": '<rect x="14" y="10" width="36" height="46" rx="3"/><path d="M22 20h6M36 20h6M22 30h6M36 30h6M22 40h6M36 40h6M28 56v-8h8v8"/>',
        "phone": '<rect x="18" y="6" width="28" height="52" rx="5"/><path d="M28 50h8"/>',
        "sheet": '<rect x="8" y="12" width="48" height="40" rx="3"/><path d="M8 24h48M8 36h48M24 12v40M40 12v40"/>',
        "calendar": '<rect x="8" y="14" width="48" height="42" rx="4"/><path d="M8 26h48M20 8v12M44 8v12"/>',
        "bell": '<path d="M18 44V30a14 14 0 0 1 28 0v14l4 4H14z"/><path d="M27 54a5 5 0 0 0 10 0"/>',
        "check": '<path d="M14 33l12 12 24-26"/>',
        "x": '<path d="M18 18l28 28M46 18L18 46"/>',
        "user": '<circle cx="32" cy="22" r="10"/><path d="M12 56c2-12 10-18 20-18s18 6 20 18"/>',
        "clock": '<circle cx="32" cy="32" r="24"/><path d="M32 18v15l10 6"/>',
        "roof": '<path d="M8 32L32 12l24 20"/><path d="M14 28v26h36V28"/><path d="M40 36c0 4-3 6-3 9a3 3 0 0 0 6 0c0-3-3-5-3-9z"/>',
        "hand": '<path d="M6 34l10-10 10 4 8-6 10 2 14 12-10 12-8-6-8 6-10-8z"/>',
        "brain": '<path d="M24 12a9 9 0 0 0-12 8 9 9 0 0 0-2 16 9 9 0 0 0 12 12h2V12zM40 12a9 9 0 0 1 12 8 9 9 0 0 1 2 16 9 9 0 0 1-12 12h-2V12z"/>',
        "puzzle": '<path d="M10 22h14a6 6 0 1 1 12 0h14v14a6 6 0 1 0 0 12v8H10z"/>',
        "tag": '<path d="M8 32V10h22l26 26-22 22z"/><circle cx="20" cy="22" r="4"/>',
        "bolt": '<path d="M36 6L14 36h16l-4 22 24-32H34z"/>',
        "camera": '<rect x="8" y="18" width="48" height="34" rx="5"/><circle cx="32" cy="35" r="9"/><path d="M22 18l4-7h12l4 7"/>',
        "eye": '<path d="M4 32s10-18 28-18 28 18 28 18-10 18-28 18S4 32 4 32z"/><circle cx="32" cy="32" r="8"/>',
        "flow": '<rect x="6" y="8" width="18" height="14" rx="3"/><rect x="40" y="25" width="18" height="14" rx="3"/><rect x="6" y="42" width="18" height="14" rx="3"/><path d="M24 15h8v32h-8M32 32h8"/>',
        "chat": '<path d="M8 12h48v30H26l-12 10V42H8z"/>',
        "wrench": '<path d="M40 8a14 14 0 0 0-12 20L8 48l8 8 20-20A14 14 0 0 0 56 24l-8 6-8-2-2-8 8-8z"/>',
        "chart": '<path d="M10 54h44M18 46V30M30 46V20M42 46V34"/>',
    }[name]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none" stroke="{color}" '
            f'stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')

def e(s): return html.escape(s)

# ------------------------------------------------------------------ scene components
def title(kicker, big, sub="", icon=None, note=None, hl=None):
    big_html = e(big)
    if hl: big_html = big_html.replace(e(hl), f'<span class="gold">{e(hl)}</span>')
    return f'''
    <div class="center col gap24">
      {f'<div class="iconbadge" data-at="0">{ic(icon, 92)}</div>' if icon else ''}
      <div class="kicker" data-at="0.1">{e(kicker)}</div>
      <div class="big" data-at="0.25">{big_html}</div>
      {f'<div class="sub" data-at="0.6">{e(sub)}</div>' if sub else ''}
      {f'<div class="note" data-at="0.9">{e(note)}</div>' if note else ''}
    </div>'''

def quote(line1, line2, hl=None, at2=0.8):
    l2 = e(line2)
    if hl: l2 = l2.replace(e(hl), f'<span class="gold under">{e(hl)}</span>')
    return f'''
    <div class="center col gap32">
      <div class="q1" data-at="0">{e(line1)}</div>
      <div class="q2" data-at="{at2}">{l2}</div>
    </div>'''

def steps(head, items, numbered=True, strike_at=None):
    rows = "".join(
        f'<div class="step" data-at="{at}"><div class="num">{i+1 if numbered else ic("check",34)}</div>'
        f'<div class="steptxt">{e(t)}</div></div>' for i, (t, at) in enumerate(items))
    return f'''<div class="center col gap20 w860">
      <div class="kicker" data-at="0">{e(head)}</div>{rows}</div>'''

def checklist(head, items):
    rows = "".join(
        f'<div class="step ok" data-at="{at}"><div class="num okc">{ic("check",36)}</div>'
        f'<div class="steptxt">{e(t)}</div></div>' for t, at in items)
    return f'''<div class="center col gap20 w860">
      <div class="kicker" data-at="0">{e(head)}</div>{rows}</div>'''

def nots(head, items):
    cards = "".join(
        f'''<div class="notcard" data-at="{at}"><div class="noticon">{ic(icon,76)}</div>
            <div class="nottxt">{e(t)}</div><div class="xbadge" data-at="{at+0.5}">{ic("x",34)}</div></div>'''
        for t, icon, at in items)
    return f'''<div class="center col gap28"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="row gap24">{cards}</div></div>'''

def compare(left, right, left_at=0, right_at=0.8, foot=None):
    def card(c, at, cls):
        return f'''<div class="cmp {cls}" data-at="{at}"><div class="cmpicon">{ic(c["icon"],70)}</div>
          <div class="cmph">{e(c["title"])}</div><div class="cmpb">{e(c["body"])}</div>
          <div class="cmptag">{e(c["tag"])}</div></div>'''
    return f'''<div class="center col gap28"><div class="row gap28">{card(left,left_at,"")}{card(right,right_at,"hot")}</div>
      {f'<div class="sub" data-at="{right_at+0.8}">{e(foot)}</div>' if foot else ''}</div>'''

def price(amount, label, note):
    return f'''<div class="center col gap24">
      <div class="building" data-at="0">{ic("building",150)}</div>
      <div class="pricetag" data-at="0.5">{ic("tag",54)}<span>{e(amount)}</span></div>
      <div class="sub" data-at="0.9">{e(label)}</div>
      <div class="note" data-at="1.2">{e(note)}</div></div>'''

def chat(head, msgs):
    bubbles = ""
    for side, kind, txt, at in msgs:
        if kind == "meter":
            inner = f'''<div class="meterpic"><div class="meterdial">
              {''.join(f'<span>{d}</span>' for d in txt)}</div><div class="meterlbl">kWh</div></div>'''
        else:
            inner = e(txt)
        bubbles += f'<div class="bubble {side}" data-at="{at}">{inner}</div>'
    return f'''<div class="center col gap20"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="phone" data-at="0"><div class="phonebar">Tenant · Unit 4B</div>
      <div class="chatlist">{bubbles}</div></div></div>'''

def sheet(head, cols, rows, hl_row=None, hl_at=1.0, add_row=None, add_at=None, foot=None, foot_at=None):
    th = "".join(f"<th>{e(c)}</th>" for c in cols)
    trs = ""
    for i, r in enumerate(rows):
        cls = ' class="hl"' if i == hl_row else ""
        trs += f"<tr{cls}>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>"
    if add_row:
        trs += f'<tr class="new" data-at="{add_at}">' + "".join(f"<td>{e(c)}</td>" for c in add_row) + "</tr>"
    hl = f'<div class="hlbox" data-at="{hl_at}" style="top:{78 + hl_row * 64}px"></div>' if hl_row is not None else ""
    return f'''<div class="center col gap24"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="sheetwrap" data-at="0.1"><div class="sheetbar">{ic("sheet",30)} Property_Tracker.xlsx</div>
      <div class="tbl"><table><tr>{th}</tr>{trs}</table>{hl}</div></div>
      {f'<div class="sub" data-at="{foot_at}">{e(foot)}</div>' if foot else ''}</div>'''

def calc(head, lines, result, at_result):
    ls = "".join(f'<div class="calcline" data-at="{at}">{e(t)}</div>' for t, at in lines)
    return f'''<div class="center col gap24"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="calcbox" data-at="0.1">{ls}<div class="calcres" data-at="{at_result}">{e(result)}</div></div></div>'''

def months(head, sub, sub_at):
    ms = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
    tiles = "".join(f'<div class="mtile" data-at="{0.3 + i*0.22:.2f}"><b>{m}</b><span>10 min</span></div>'
                    for i, m in enumerate(ms))
    return f'''<div class="center col gap28"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="mgrid">{tiles}</div><div class="sub" data-at="{sub_at}">{e(sub)}</div></div>'''

def form(head, fields, status, status_at, title_txt="Meter Reading"):
    fs = "".join(f'''<div class="field" data-at="{at}"><div class="flbl">{e(k)}</div>
        <div class="fval">{('<div class="thumb">'+ic("camera",34)+' meter_4B.jpg</div>') if v=="PHOTO" else e(v)}</div></div>'''
        for k, v, at in fields)
    return f'''<div class="center col gap20"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="phone app" data-at="0"><div class="appbar">{ic("flow",30)} {e(title_txt)}</div>
      <div class="fields">{fs}</div><div class="status" data-at="{status_at}">{ic("check",30)} {e(status)}</div></div></div>'''

def alert(head, rows, badge, badge_at):
    rs = "".join(f'<div class="arow" data-at="{at}"><span>{e(k)}</span><b>{e(v)}</b></div>' for k, v, at in rows)
    return f'''<div class="center col gap24"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="alertcard" data-at="0.1"><div class="alerthead">{ic("bell",44)}<span>{e(badge)}</span></div>
      {rs}</div></div>'''

def scattered(head, items, foot, foot_at):
    t = "".join(f'''<div class="scat {cls}" data-at="{at}">{ic(icon,70)}<div class="scath">{e(h)}</div>
        <div class="scatb">{e(b)}</div></div>''' for icon, h, b, cls, at in items)
    return f'''<div class="center col gap28"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="row gap24">{t}</div><div class="sub" data-at="{foot_at}">{e(foot)}</div></div>'''

def urgent(big, sub, sub_at=0.8):
    return f'''<div class="center col gap24"><div class="urgentbadge pulse" data-at="0">{ic("bell",80)}</div>
      <div class="big red" data-at="0.2">{e(big)}</div><div class="sub" data-at="{sub_at}">{e(sub)}</div></div>'''

def chips(head, items, foot=None, foot_at=None):
    c = "".join(f'<div class="chip" data-at="{at}">{ic(icon,44)}<span>{e(t)}</span></div>' for t, icon, at in items)
    return f'''<div class="center col gap28"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="col gap20">{c}</div>{f'<div class="sub" data-at="{foot_at}">{e(foot)}</div>' if foot else ''}</div>'''

def dashboard(head, tiles, foot=None, foot_at=None):
    ts = "".join(f'<div class="dtile" data-at="{at}"><div class="dnum">{e(n)}</div><div class="dlbl">{e(l)}</div></div>'
                 for n, l, at in tiles)
    return f'''<div class="center col gap24"><div class="kicker" data-at="0">{e(head)}</div>
      <div class="dash" data-at="0.1"><div class="dashbar">{ic("chart",30)} Operations · One view</div>
      <div class="dgrid">{ts}</div></div>{f'<div class="sub" data-at="{foot_at}">{e(foot)}</div>' if foot else ''}</div>'''

def cta(question, line="I build simple work apps with Google AppSheet, Sheets & Apps Script"):
    return f'''<div class="center col gap28">
      <div class="brand" data-at="0"><div class="logo">A</div><div>Automation With Sholz</div></div>
      <div class="sub" data-at="0.4">{e(line)}</div>
      <div class="question" data-at="1.0">{ic("chat",64)}<span>{e(question)}</span></div>
      <div class="note" data-at="1.6">Comment below, or DM me “WORKFLOW”</div></div>'''

# ------------------------------------------------------------------ captions
def chunk_words(words, max_words=4, gap=0.45):
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["s"] - cur[-1]["e"] > gap or cur[-1]["w"].strip()[-1:] in ".?!,"):
            chunks.append(cur); cur = []
        cur.append(w)
    if cur: chunks.append(cur)
    return chunks

# ------------------------------------------------------------------ page
def build(spec, words, out_path):
    D = spec["duration"]
    scenes_html, at_js = [], []
    for i, sc in enumerate(spec["scenes"]):
        t0 = sc["t"]; t1 = spec["scenes"][i + 1]["t"] if i + 1 < len(spec["scenes"]) else D
        body = sc["html"]
        # convert relative data-at -> absolute
        import re
        body = re.sub(r'data-at="([\d.]+)"', lambda m: f'data-at="{t0 + float(m.group(1)):.2f}"', body)
        scenes_html.append(
            f'<div id="sc{i}" class="clip scene" data-start="{t0:.2f}" data-duration="{t1 - t0:.2f}" '
            f'data-track-index="1">{body}</div>')

    caps = []
    chs = chunk_words(words)
    for j, ch in enumerate(chs):
        s = ch[0]["s"]; nxt_end = ch[-1]["e"] + 0.25
        if j + 1 < len(chs): nxt_end = min(nxt_end, chs[j + 1][0]["s"] - 0.01)
        spans = "".join(f'<span class="w" data-ws="{w["s"]:.2f}">{e(w["w"].strip())}</span> ' for w in ch)
        caps.append(f'<div class="clip cap" data-start="{s:.2f}" data-duration="{max(nxt_end - s, 0.3):.2f}" '
                    f'data-track-index="3"><div class="capin">{spans}</div></div>')

    page = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family: Pop; font-weight: 400; src: url(assets/fonts/poppins-latin-400-normal.woff2); }}
@font-face {{ font-family: Pop; font-weight: 600; src: url(assets/fonts/poppins-latin-600-normal.woff2); }}
@font-face {{ font-family: Pop; font-weight: 700; src: url(assets/fonts/poppins-latin-700-normal.woff2); }}
@font-face {{ font-family: Pop; font-weight: 800; src: url(assets/fonts/poppins-latin-800-normal.woff2); }}
:root {{ --navy:#0a1224; --panel:#13203b; --line:#24365c; --gold:#f5b82e; --orange:#ff8a1f;
        --ink:#ffffff; --muted:#a9b8d6; --red:#ff5a5f; --green:#3ddc84; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:var(--navy); }}
#root {{ position:relative; width:100%; height:100%; font-family:Pop, sans-serif; color:var(--ink); }}
.top {{ position:absolute; left:0; top:0; width:{W}px; height:{TOP}px; overflow:hidden;
       background: radial-gradient(120% 90% at 50% 0%, #1b2d55 0%, #0d1830 55%, #0a1224 100%); }}
.grid {{ position:absolute; inset:0; opacity:.18;
        background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg, var(--line) 1px, transparent 1px);
        background-size: 54px 54px; }}
.hdr {{ position:absolute; left:44px; right:44px; top:40px; display:flex; justify-content:space-between; align-items:center; z-index:5; }}
.brandmini {{ display:flex; align-items:center; gap:14px; font-weight:600; font-size:30px; }}
.logo {{ width:52px; height:52px; border-radius:14px; background:linear-gradient(135deg,var(--orange),var(--gold));
        color:#0a1224; font-weight:800; font-size:34px; display:flex; align-items:center; justify-content:center; }}
.cardid {{ font-size:24px; font-weight:600; color:var(--gold); border:2px solid var(--gold); padding:6px 16px; border-radius:40px; }}
.scene {{ position:absolute; left:0; top:110px; width:{W}px; height:{TOP - 150}px; display:flex; align-items:center; justify-content:center; }}
.center {{ display:flex; align-items:center; justify-content:center; text-align:center; }}
.col {{ flex-direction:column; }} .row {{ display:flex; flex-direction:row; align-items:stretch; }}
.gap20 {{ gap:20px; }} .gap24 {{ gap:24px; }} .gap28 {{ gap:28px; }} .gap32 {{ gap:32px; }} .w860 {{ width:860px; }}
.kicker {{ font-size:30px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--gold); }}
.big {{ font-size:84px; line-height:1.06; font-weight:800; max-width:960px; letter-spacing:-.02em; }}
.big.red {{ color:var(--red); }}
.sub {{ font-size:38px; line-height:1.3; color:var(--muted); max-width:900px; font-weight:400; }}
.note {{ font-size:24px; color:#7f90b3; font-style:italic; }}
.gold {{ color:var(--gold); }} .under {{ text-decoration: underline; text-decoration-color: var(--red); text-underline-offset: 14px; }}
.iconbadge, .urgentbadge {{ width:150px; height:150px; border-radius:40px; background:var(--panel); border:2px solid var(--line);
        display:flex; align-items:center; justify-content:center; color:var(--gold); }}
.urgentbadge {{ color:var(--red); border-color:var(--red); }}
.q1 {{ font-size:56px; font-weight:600; color:var(--muted); max-width:920px; line-height:1.2; }}
.q2 {{ font-size:84px; font-weight:800; max-width:960px; line-height:1.1; }}
.step {{ display:flex; align-items:center; gap:26px; width:100%; background:var(--panel); border:2px solid var(--line);
        border-radius:22px; padding:22px 28px; text-align:left; }}
.num {{ flex:none; width:64px; height:64px; border-radius:18px; background:var(--gold); color:#0a1224; font-weight:800; font-size:34px;
       display:flex; align-items:center; justify-content:center; }}
.num.okc {{ background:var(--green); }}
.steptxt {{ font-size:40px; font-weight:600; }}
.notcard {{ position:relative; width:300px; padding:36px 22px; background:var(--panel); border:2px solid var(--line); border-radius:28px;
           display:flex; flex-direction:column; align-items:center; gap:20px; }}
.noticon {{ color:var(--muted); }} .nottxt {{ font-size:32px; font-weight:600; line-height:1.2; }}
.xbadge {{ position:absolute; top:-18px; right:-18px; width:64px; height:64px; border-radius:50%; background:var(--red);
          color:white; display:flex; align-items:center; justify-content:center; }}
.cmp {{ width:440px; padding:40px 30px; background:var(--panel); border:2px solid var(--line); border-radius:30px;
       display:flex; flex-direction:column; align-items:center; gap:18px; }}
.cmp.hot {{ border-color:var(--gold); }} .cmpicon {{ color:var(--gold); }}
.cmph {{ font-size:40px; font-weight:700; }} .cmpb {{ font-size:30px; color:var(--muted); line-height:1.3; }}
.cmptag {{ font-size:24px; font-weight:600; background:#0a1224; padding:8px 18px; border-radius:30px; color:var(--gold); }}
.building {{ color:var(--muted); }}
.pricetag {{ display:flex; align-items:center; gap:20px; background:var(--gold); color:#0a1224; font-weight:800; font-size:96px;
            padding:16px 46px; border-radius:26px; transform:rotate(-3deg); }}
.phone {{ width:520px; height:640px; border-radius:46px; background:#0d1626; border:6px solid #2a3a5e; overflow:hidden;
         display:flex; flex-direction:column; text-align:left; }}
.phonebar, .appbar {{ padding:20px 26px; font-size:26px; font-weight:600; background:#16243f; color:var(--muted); display:flex; gap:12px; align-items:center; }}
.appbar {{ color:var(--ink); background:#1a6bd6; }}
.chatlist {{ display:flex; flex-direction:column; gap:18px; padding:26px; }}
.bubble {{ max-width:80%; font-size:28px; padding:16px 22px; border-radius:24px; line-height:1.3; }}
.bubble.in {{ background:#22314f; align-self:flex-start; border-bottom-left-radius:6px; }}
.bubble.out {{ background:#1f7a4d; align-self:flex-end; border-bottom-right-radius:6px; }}
.meterpic {{ background:#ddd5c4; border-radius:16px; padding:22px; display:flex; flex-direction:column; align-items:center; gap:8px; color:#333; }}
.meterdial {{ display:flex; gap:6px; }} .meterdial span {{ background:#111; color:#fff; font-size:46px; font-weight:700; width:48px; text-align:center; border-radius:6px; font-family:monospace; }}
.meterlbl {{ font-size:22px; font-weight:600; }}
.sheetwrap {{ width:940px; background:#ffffff; border-radius:20px; overflow:hidden; color:#1f2937; }}
.sheetbar {{ background:#1e7b45; color:white; font-size:26px; font-weight:600; padding:12px 20px; display:flex; gap:12px; align-items:center; }}
.tbl {{ position:relative; }}
table {{ width:100%; border-collapse:collapse; font-size:28px; }}
th {{ background:#eef2f7; font-weight:700; height:66px; border:1px solid #d6dde8; }}
td {{ height:64px; border:1px solid #e3e8ef; padding:0 12px; }}
tr.new td {{ background:#fff4d6; font-weight:700; }}
.hlbox {{ position:absolute; left:4px; right:4px; height:64px; border:5px solid var(--gold); border-radius:8px; box-shadow:0 0 0 9999px rgba(10,18,36,.25); }}
.calcbox {{ width:820px; background:var(--panel); border:2px solid var(--line); border-radius:28px; padding:36px 40px; display:flex; flex-direction:column; gap:18px; text-align:left; }}
.calcline {{ font-size:44px; font-weight:600; font-family:Pop; }}
.calcres {{ font-size:54px; font-weight:800; color:var(--gold); border-top:3px dashed var(--line); padding-top:18px; }}
.mgrid {{ display:grid; grid-template-columns:repeat(4, 200px); gap:18px; }}
.mtile {{ background:var(--panel); border:2px solid var(--line); border-radius:20px; padding:18px 10px; display:flex; flex-direction:column; gap:6px; }}
.mtile b {{ font-size:32px; }} .mtile span {{ font-size:24px; color:var(--orange); font-weight:600; }}
.phone.app {{ height:660px; background:#f4f7fb; color:#0f172a; border-color:#1a6bd6; }}
.fields {{ display:flex; flex-direction:column; gap:14px; padding:22px; }}
.field {{ background:white; border-radius:16px; padding:12px 18px; box-shadow:0 2px 6px rgba(0,0,0,.08); }}
.flbl {{ font-size:20px; color:#64748b; font-weight:600; }} .fval {{ font-size:30px; font-weight:700; }}
.thumb {{ display:flex; align-items:center; gap:10px; font-size:24px; color:#1a6bd6; }}
.status {{ margin:6px 22px; background:var(--green); color:#06301a; font-weight:700; font-size:28px; border-radius:16px; padding:14px; display:flex; gap:10px; align-items:center; justify-content:center; }}
.alertcard {{ width:860px; background:var(--panel); border:3px solid var(--gold); border-radius:30px; padding:30px 36px; display:flex; flex-direction:column; gap:14px; }}
.alerthead {{ display:flex; align-items:center; gap:18px; color:var(--gold); font-size:46px; font-weight:800; padding-bottom:12px; border-bottom:2px solid var(--line); }}
.arow {{ display:flex; justify-content:space-between; font-size:34px; }} .arow span {{ color:var(--muted); }}
.scat {{ width:300px; padding:30px 20px; background:var(--panel); border:3px dashed var(--line); border-radius:26px; display:flex; flex-direction:column; align-items:center; gap:14px; color:var(--muted); }}
.scat.miss {{ border-color:var(--red); color:var(--red); }}
.scath {{ font-size:32px; font-weight:700; color:var(--ink); }} .scatb {{ font-size:26px; line-height:1.3; }}
.chip {{ display:flex; align-items:center; gap:20px; background:var(--panel); border:2px solid var(--line); border-radius:24px; padding:20px 34px; font-size:42px; font-weight:700; color:var(--gold); }}
.chip span {{ color:var(--ink); }}
.dash {{ width:900px; background:#f4f7fb; border-radius:26px; overflow:hidden; color:#0f172a; }}
.dashbar {{ background:#1a6bd6; color:white; font-size:26px; font-weight:600; padding:14px 22px; display:flex; gap:12px; align-items:center; }}
.dgrid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:18px; padding:24px; }}
.dtile {{ background:white; border-radius:18px; padding:22px; box-shadow:0 2px 6px rgba(0,0,0,.08); text-align:left; }}
.dnum {{ font-size:58px; font-weight:800; color:#1a6bd6; }} .dlbl {{ font-size:26px; color:#475569; font-weight:600; }}
.brand {{ display:flex; align-items:center; gap:22px; font-size:52px; font-weight:800; }}
.brand .logo {{ width:96px; height:96px; font-size:62px; border-radius:26px; }}
.question {{ display:flex; align-items:center; gap:22px; max-width:920px; background:var(--gold); color:#0a1224; font-size:40px; font-weight:700;
            padding:26px 34px; border-radius:28px; text-align:left; line-height:1.25; }}
.foot {{ position:absolute; left:0; top:{TOP}px; width:{W}px; height:{H - TOP}px; overflow:hidden; background:#000; }}
.foot video {{ width:100%; height:100%; object-fit:cover; object-position:50% {{OBJPOS}}; }}
.seam {{ position:absolute; left:0; top:{TOP - 4}px; width:{W}px; height:8px; background:linear-gradient(90deg,var(--orange),var(--gold)); z-index:6; }}
.cap {{ position:absolute; left:0; top:{TOP - 52}px; width:{W}px; display:flex; justify-content:center; z-index:8; }}
.capin {{ max-width:960px; text-align:center; font-size:56px; font-weight:800; line-height:1.15; padding:14px 26px; border-radius:20px;
         background:rgba(10,18,36,.82); color:#fff; letter-spacing:-.01em; }}
.capin .w {{ color:#ffffff; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D:.2f}" data-width="{W}" data-height="{H}">
  <div class="top"><div class="grid"></div>
    <div class="hdr"><div class="brandmini"><div class="logo">A</div>Automation With Sholz</div><div class="cardid">{e(spec["card"])}</div></div>
  </div>
  {"".join(scenes_html)}
  <div class="foot"><video id="talk" class="clip" src="assets/talk.mp4" data-start="0" data-duration="{D:.2f}" data-media-start="0"
       data-has-audio="true" data-track-index="0" playsinline></video></div>
  <div class="seam"></div>
  {"".join(caps)}
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  document.querySelectorAll(".scene").forEach(sc => {{
    tl.fromTo(sc, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, +sc.dataset.start);
  }});
  document.querySelectorAll("[data-at]").forEach(el => {{
    tl.fromTo(el, {{ opacity: 0, y: 36, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, +el.dataset.at);
  }});
  document.querySelectorAll(".pulse").forEach(el => {{
    tl.to(el, {{ scale: 1.08, duration: 0.45, yoyo: true, repeat: 7, ease: "sine.inOut" }}, +el.dataset.at + 0.5);
  }});
  document.querySelectorAll(".capin .w").forEach(w => {{
    tl.set(w, {{ color: "#f5b82e" }}, +w.dataset.ws);
  }});
  document.querySelectorAll(".cap").forEach(c => {{
    tl.fromTo(c, {{ y: 14, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.12 }}, +c.dataset.start);
  }});
  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
</body>
</html>'''
    page = page.replace("{OBJPOS}", spec.get("objpos", "30%"))
    open(out_path, "w").write(page)
