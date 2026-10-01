#!/usr/bin/env bash
# Renders both compositions and converts them straight to optimized, looping
# GIFs under 2MB — GIF is the only deliverable, so the intermediate MP4s are
# rendered to a temp dir and discarded. Uses ffmpeg's two-pass palette
# workflow for best quality-per-byte, backing off fps/width/colors
# automatically if a result is still too big.
set -euo pipefail

# Target a safety margin below the real 2MB cap so encoder variance never
# tips a result over the line.
MAX_BYTES=$((1900 * 1024))
OUT_DIR="out"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$OUT_DIR"

convert_one () {
  local input="$1"
  local output="$2"
  shift 2
  local attempts=("$@")

  for attempt in "${attempts[@]}"; do
    read -r fps w colors <<< "$attempt"
    local palette
    palette="$(mktemp --suffix=.png)"

    ffmpeg -y -i "$input" \
      -vf "fps=${fps},scale=${w}:-1:flags=lanczos,palettegen=max_colors=${colors}" \
      "$palette" -loglevel error

    ffmpeg -y -i "$input" -i "$palette" \
      -lavfi "fps=${fps},scale=${w}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer" \
      -loop 0 \
      "$output" -loglevel error

    rm -f "$palette"

    local size
    size=$(stat -c%s "$output")
    echo "  tried fps=${fps} width=${w} colors=${colors} -> $(numfmt --to=iec-i --suffix=B "$size")"

    if [ "$size" -le "$MAX_BYTES" ]; then
      echo "  OK: ${output} is under 2MB"
      return 0
    fi
  done

  echo "  WARNING: ${output} is still over 2MB after all quality reductions." >&2
  return 1
}

render_and_convert () {
  local comp_id="$1"
  local gif_name="$2"
  shift 2
  local attempts=("$@")

  local mp4_tmp="$TMP_DIR/${comp_id}.mp4"
  echo "Rendering ${comp_id}..."
  npx remotion render src/index.ts "$comp_id" "$mp4_tmp" --log=error

  echo "Converting ${comp_id} to GIF..."
  convert_one "$mp4_tmp" "$OUT_DIR/$gif_name" "${attempts[@]}"
}

render_and_convert "RotatingText-Landscape" "rotating-text-1920x100.gif" \
  "20 1920 160" "15 1920 128" "15 1280 96" "12 960 64"

render_and_convert "RotatingText-Square" "rotating-text-1080x1080.gif" \
  "15 720 128" "12 540 96" "10 360 64" "8 270 64"
