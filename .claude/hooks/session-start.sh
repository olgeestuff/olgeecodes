#!/bin/bash
# Installs the Python packages the onetake skill (.claude/skills/onetake) needs
# to render videos. ffmpeg, node and Chromium are already in the cloud image.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# playwright is pinned to 1.56.0 because it drives the pre-installed
# /opt/pw-browsers/chromium-1194; a newer playwright looks for a newer Chromium.
python3 -m pip install -q --break-system-packages --root-user-action=ignore \
  "playwright==1.56.0" numpy scipy Pillow matplotlib fonttools brotli opencv-python-headless
