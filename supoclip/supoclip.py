#!/usr/bin/env python3
"""SupoClip connector: turn long-form videos into short clips via the SupoClip API.

No installs needed (Python 3.8+ standard library only).

Auth: set SUPOCLIP_API_KEY in your environment or in a .env file next to this
script (see .env.example). Never hard-code the key in this file.

Usage:
    python supoclip.py check                       # verify key + show plan/quota
    python supoclip.py clip <video_url> [options]  # create clips, wait, list them
    python supoclip.py status <task_id>
    python supoclip.py clips <task_id>
    python supoclip.py download <task_id> [clip_id ...]   # all clips if none given

API reference: https://github.com/FujiwaraChoki/supoclip/blob/main/docs/api-reference.md
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_API_URL = "https://api.supoclip.com"
TERMINAL_STATES = {"completed", "error", "cancelled"}
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_dotenv():
    """Load KEY=VALUE lines from .env (script dir, then cwd) without overriding real env vars."""
    for path in (os.path.join(SCRIPT_DIR, ".env"), os.path.join(os.getcwd(), ".env")):
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


class SupoClipError(Exception):
    pass


class SupoClip:
    def __init__(self, api_key, api_url=DEFAULT_API_URL, timeout=60):
        if not api_key:
            raise SupoClipError(
                "SUPOCLIP_API_KEY is not set. Put it in supoclip/.env or your environment."
            )
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method, path, body=None, params=None, timeout=None):
        url = self.api_url + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        # Unredirected: the key is never forwarded if the API redirects to storage (e.g. S3).
        req.add_unredirected_header("Authorization", f"Bearer {self.api_key}")
        try:
            return urllib.request.urlopen(req, timeout=timeout or self.timeout)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            try:
                detail = json.loads(detail).get("detail", detail)
            except (ValueError, AttributeError):
                pass
            hint = {
                401: " (API key invalid or revoked)",
                402: " (plan/quota limit reached; run `check`)",
                403: " (forbidden; verify your email on SupoClip)",
                404: " (not found)",
            }.get(e.code, "")
            raise SupoClipError(f"HTTP {e.code}{hint}: {detail}") from None
        except urllib.error.URLError as e:
            raise SupoClipError(f"Cannot reach {self.api_url}: {e.reason}") from None

    def _json(self, method, path, body=None, params=None):
        with self._request(method, path, body, params) as resp:
            return json.loads(resp.read().decode("utf-8") or "{}")

    def billing_summary(self):
        return self._json("GET", "/tasks/billing/summary")

    def create_task(self, url, title="", processing_mode="fast", output_format="vertical",
                    caption_template="default", add_subtitles=True, include_broll=False):
        source = {"url": url}
        if title:
            source["title"] = title
        body = {
            "source": source,
            "processing_mode": processing_mode,
            "output_format": output_format,
            "caption_template": caption_template,
            "add_subtitles": add_subtitles,
            "include_broll": include_broll,
        }
        return self._json("POST", "/tasks/", body)

    def get_task(self, task_id):
        return self._json("GET", f"/tasks/{task_id}")

    def list_clips(self, task_id):
        return self._json("GET", f"/tasks/{task_id}/clips").get("clips", [])

    def wait_for_task(self, task_id, timeout_seconds=1800, poll_seconds=10):
        deadline = time.monotonic() + timeout_seconds
        last_line = ""
        while True:
            task = self.get_task(task_id)
            status = task.get("status", "unknown")
            line = f"  {status} {task.get('progress', 0)}% {task.get('progress_message') or ''}".rstrip()
            if line != last_line:
                print(line, flush=True)
                last_line = line
            if status in TERMINAL_STATES:
                return task
            if time.monotonic() >= deadline:
                raise SupoClipError(
                    f"Still '{status}' after {timeout_seconds}s. Check later: "
                    f"python supoclip.py status {task_id}"
                )
            time.sleep(poll_seconds)

    def download_clip(self, task_id, clip_id, out_dir, filename=None):
        os.makedirs(out_dir, exist_ok=True)
        name = re.sub(r"[^A-Za-z0-9._-]", "_", filename or f"clip_{clip_id}")
        if not name.lower().endswith(".mp4"):
            name += ".mp4"
        path = os.path.join(out_dir, name)
        with self._request("GET", f"/tasks/{task_id}/clips/{clip_id}/file", timeout=600) as resp, \
                open(path, "wb") as f:
            while chunk := resp.read(1024 * 256):
                f.write(chunk)
        return path


def print_clips(clips):
    if not clips:
        print("No clips yet.")
        return
    for i, c in enumerate(clips, 1):
        score = c.get("virality_score")
        print(f"{i:>2}. clip_id={c.get('id')}  {c.get('start_time')} -> {c.get('end_time')}"
              f"{f'  virality={score}' if score is not None else ''}")
        if c.get("text"):
            print(f"    \"{c['text'][:120]}{'...' if len(c['text']) > 120 else ''}\"")


def download_all(client, task_id, clips, out_dir, only_ids=None):
    # Number files by the clip's position in the full list so names stay stable.
    for i, c in enumerate(clips, 1):
        if only_ids and str(c.get("id")) not in only_ids:
            continue
        path = client.download_clip(task_id, c["id"], out_dir, f"{task_id[:8]}_{i:02d}_{c['id']}")
        print(f"  saved {path}")


def main(argv=None):
    load_dotenv()
    p = argparse.ArgumentParser(description="SupoClip API connector")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="Verify API key and show plan/quota")

    c = sub.add_parser("clip", help="Create clips from a video URL")
    c.add_argument("url", help="YouTube or direct video URL")
    c.add_argument("--title", default="")
    c.add_argument("--mode", default="fast", choices=["fast", "balanced", "quality"])
    c.add_argument("--format", default="vertical",
                   choices=["vertical", "vertical_pan", "vertical_split", "original"])
    c.add_argument("--captions", default="default", help="Caption template, e.g. default, hormozi, mrbeast")
    c.add_argument("--no-subtitles", action="store_true")
    c.add_argument("--broll", action="store_true", help="Add B-roll overlays")
    c.add_argument("--no-wait", action="store_true", help="Return the task_id without waiting")
    c.add_argument("--download", action="store_true", help="Download all clips when done")

    s = sub.add_parser("status", help="Show a task's status")
    s.add_argument("task_id")

    l = sub.add_parser("clips", help="List a task's clips")
    l.add_argument("task_id")

    d = sub.add_parser("download", help="Download clips (all if no clip ids given)")
    d.add_argument("task_id")
    d.add_argument("clip_ids", nargs="*")

    args = p.parse_args(argv)
    out_dir = os.environ.get("SUPOCLIP_DOWNLOAD_DIR", os.path.join(os.getcwd(), "supoclip-downloads"))

    try:
        client = SupoClip(os.environ.get("SUPOCLIP_API_KEY", ""),
                          os.environ.get("SUPOCLIP_API_URL", DEFAULT_API_URL))

        if args.cmd == "check":
            summary = client.billing_summary()
            print("Connected. Account summary:")
            print(json.dumps(summary, indent=2))

        elif args.cmd == "clip":
            created = client.create_task(
                args.url, args.title, args.mode, args.format, args.captions,
                add_subtitles=not args.no_subtitles, include_broll=args.broll,
            )
            task_id = created["task_id"]
            print(f"Task created: {task_id}")
            if args.no_wait:
                return 0
            task = client.wait_for_task(task_id)
            if task.get("status") != "completed":
                raise SupoClipError(f"Task ended as '{task.get('status')}': {task.get('progress_message') or ''}")
            clips = client.list_clips(task_id)
            print_clips(clips)
            if args.download:
                download_all(client, task_id, clips, out_dir)

        elif args.cmd == "status":
            task = client.get_task(args.task_id)
            print(f"{task.get('status')} {task.get('progress', 0)}% {task.get('progress_message') or ''}")

        elif args.cmd == "clips":
            print_clips(client.list_clips(args.task_id))

        elif args.cmd == "download":
            clips = client.list_clips(args.task_id)
            wanted = set(args.clip_ids)
            if wanted and not any(str(c.get("id")) in wanted for c in clips):
                raise SupoClipError("None of those clip ids belong to this task.")
            download_all(client, args.task_id, clips, out_dir, wanted)

    except SupoClipError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
