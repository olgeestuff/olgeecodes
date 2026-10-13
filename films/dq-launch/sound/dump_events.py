#!/usr/bin/env python3
"""dump_events.py — the comp's __events() → sound/events.json, so a retimed beat takes its sound with it."""
import asyncio, json, pathlib, sys
from playwright.async_api import async_playwright
comp = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "comp.html").resolve()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await pg.goto(comp.as_uri()); await pg.evaluate("window.__ready")
        ev = await pg.evaluate("window.__events()"); await b.close()
    out = comp.parent / "sound" / "events.json"; out.write_text(json.dumps(ev, indent=1)); print(out, len(ev["events"]), "events")
asyncio.run(main())
