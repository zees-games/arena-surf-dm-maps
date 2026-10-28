#!/bin/bash
# stage_packs.sh OUT [id...] : one directory per map = maps/<id>/ plus worlds/<id>/, the layout a per-map CDN pack is published from.
# game-arena's ArenaBspMap.world_prefix reads a delivered map's world from <mount>/worlds/<id>/.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:?usage: stage_packs.sh OUT [id...]}"; shift
IDS=("$@"); [ ${#IDS[@]} -gt 0 ] || mapfile -t IDS < <(cd "$HERE/maps" && ls)
for id in "${IDS[@]}"; do
    [ -d "$HERE/worlds/$id" ] || { echo "no world for $id, skipped" >&2; continue; }
    rm -rf "${OUT:?}/$id"; mkdir -p "$OUT/$id/worlds"
    cp -r "$HERE/maps/$id/." "$OUT/$id/"
    cp -r "$HERE/worlds/$id" "$OUT/$id/worlds/$id"
done
