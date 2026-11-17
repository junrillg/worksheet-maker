#!/usr/bin/env sh
# Requires ImageMagick 7 with SVG support and an installed sans-serif font.
# Set WORKSHEET_FONT to a font name or file to override the rendering font.
set -eu
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
font=${WORKSHEET_FONT:-sans-serif}
if [ -z "${WORKSHEET_FONT:-}" ] && [ -f /System/Library/Fonts/Supplemental/Arial.ttf ]; then
  font=/System/Library/Fonts/Supplemental/Arial.ttf
fi
magick -font "$font" -background none "$repo_dir/assets/social-preview.svg" \
  -strip "$repo_dir/assets/social-preview.png"
magick identify -format '%f: %wx%h, %b\n' "$repo_dir/assets/social-preview.png"
