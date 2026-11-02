#!/bin/bash
# stage_packs.sh OUT [id...] : one directory per map = maps/<id>/ plus worlds/<id>/ (with the library models it draws in models/), the layout a per-map CDN pack is published from.
# game-arena's ArenaBspMap.world_prefix reads a delivered map's world from <mount>/worlds/<id>/.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:?usage: stage_packs.sh OUT [id...]}"; shift
CONVERT="${DOT_MAP_CONVERT:-$HERE/../dot-map-convert}"
IDS=("$@"); [ ${#IDS[@]} -gt 0 ] || mapfile -t IDS < <(cd "$HERE/maps" && ls)
for id in "${IDS[@]}"; do
    [ -d "$HERE/worlds/$id" ] || { echo "no world for $id, skipped" >&2; continue; }
    rm -rf "${OUT:?}/$id"; mkdir -p "$OUT/$id/worlds"
    cp -r "$HERE/maps/$id/." "$OUT/$id/"
    python3 -I "$CONVERT/bsp.py" bundle "$HERE/worlds/$id" --out "$OUT/$id/worlds" --strict
done
