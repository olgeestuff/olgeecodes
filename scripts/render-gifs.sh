#!/usr/bin/env bash
# Converts the rendered MP4s into optimized, looping GIFs under 2MB.
# Uses ffmpeg's two-pass palette workflow for best quality-per-byte, then
# backs off fps/width/colors automatically if the result is still too big.
set -euo pipefail

MAX_BYTES=$((2 * 1024 * 1024))
OUT_DIR="out"

convert_one () {
  local input="$1"
  local output="$2"
  local width="$3"

  local attempts=(
    "15 ${width} 128"
    "12 ${width} 96"
    "10 $((width * 2 / 3)) 64"
    "8 $((width / 2)) 64"
  )

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

mkdir -p "$OUT_DIR"

echo "Converting landscape GIF..."
convert_one "$OUT_DIR/rotating-text-1920x1080.mp4" "$OUT_DIR/rotating-text-1920x1080.gif" 720

echo "Converting square GIF..."
convert_one "$OUT_DIR/rotating-text-1080x1080.mp4" "$OUT_DIR/rotating-text-1080x1080.gif" 540
