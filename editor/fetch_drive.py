"""Pull new videos + script .txt files from a Google Drive folder into "raw footage".

Works anywhere (cloud session or laptop) without Drive for desktop.
One-time setup (5 minutes):
  1. Drive folder -> Share -> General access: "Anyone with the link" (Viewer).
  2. Google Cloud console -> APIs & Services -> enable "Google Drive API" ->
     Credentials -> Create credentials -> API key. Restrict it to the Drive API.
  3. Set the key:  Windows:  setx GOOGLE_API_KEY "AIza..."   (new terminal after)
                   cloud:    add GOOGLE_API_KEY to the environment's variables

Usage:
  python editor/fetch_drive.py                  (uses the default folder below)
  python editor/fetch_drive.py <folder id or url>
Already-downloaded files (same name + size) are skipped.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from common import RAW

# "teleprompter vids on office geek"
DEFAULT_FOLDER = "1LhPhwC0Cp2SDOovu-IbxVY5xoCDdTzdb"
API = "https://www.googleapis.com/drive/v3/files"
WANTED = re.compile(r"\.(mp4|mov|m4v|webm|mkv|txt)$", re.I)


def _get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def list_folder(folder: str, key: str) -> list[dict]:
    files, token = [], None
    while True:
        q = {"q": f"'{folder}' in parents and trashed = false", "key": key, "pageSize": 1000,
             "fields": "nextPageToken, files(id, name, size, mimeType)"}
        if token:
            q["pageToken"] = token
        data = json.loads(_get(f"{API}?{urllib.parse.urlencode(q)}"))
        files += data.get("files", [])
        token = data.get("nextPageToken")
        if not token:
            return files


def download(file: dict, dest: Path, key: str) -> None:
    url = f"{API}/{file['id']}?alt=media&key={key}"
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=300) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    tmp.replace(dest)


def main() -> None:
    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit(__doc__)
    folder = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FOLDER
    m = re.search(r"folders/([\w-]+)", folder)
    folder = m.group(1) if m else folder
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / "scripts").mkdir(exist_ok=True)
    for f in list_folder(folder, key):
        if not WANTED.search(f["name"]):
            continue
        dest = (RAW / "scripts" if f["name"].lower().endswith(".txt") else RAW) / f["name"]
        if dest.exists() and str(dest.stat().st_size) == f.get("size"):
            continue
        print(f"  downloading {f['name']} ({int(f.get('size', 0)) / 1e6:.1f} MB)")
        download(f, dest, key)
    print("done.")


if __name__ == "__main__":
    main()
