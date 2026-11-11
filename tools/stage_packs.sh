#!/bin/bash
# stage_packs.sh OUT [id...] : one directory per map = maps/<id>/ plus worlds/<id>/ (with the library models it draws in models/), the layout a per-map CDN pack is published from.
# game-fatal-contact's ArenaBspMap.world_prefix reads a delivered map's world from <mount>/worlds/<id>/.
#
# PUBLISH RULE (owner policy: licensed textures must be mapped to free/open/own assets): maps/<id>/textures/ is the importer's
# decode of the textures in the SOURCE map's pakfile (third-party or Valve art, no mapping) and is NEVER copied into a pack.
# The pack draws from worlds/<id>/textures (fb_ = the CC0 PBR fallback tree, gen_ = generated), the baked .bin and our own
# lightmap. tools/check_packs.py then verifies every staged pack and the script fails if it finds a source texture.
# DOT_PY overrides the interpreter of the converter (default: python3 -P).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:?usage: stage_packs.sh OUT [id...]}"; shift
CONVERT="${DOT_MAP_CONVERT:-$HERE/../dot-map-convert}"
IDS=("$@"); [ ${#IDS[@]} -gt 0 ] || mapfile -t IDS < <(cd "$HERE/maps" && ls)
STAGED=()
for id in "${IDS[@]}"; do
    [ -d "$HERE/worlds/$id" ] || { echo "no world for $id, skipped" >&2; continue; }
    rm -rf "${OUT:?}/$id"; mkdir -p "$OUT/$id/worlds"
    [ -d "$HERE/maps/$id" ] && (cd "$HERE/maps/$id" && tar cf - --exclude=./textures .) | tar xf - -C "$OUT/$id"
    ${DOT_PY:-python3 -P} "$CONVERT/bsp.py" bundle "$HERE/worlds/$id" --out "$OUT/$id/worlds" --strict
    # An `.import` marker names the importing project's .godot cache, absent from a delivered pack: its texture would load null.
    find "$OUT/$id" -name '*.import' -delete
    STAGED+=("$id")
done
[ ${#STAGED[@]} -eq 0 ] || python3 -P "$HERE/tools/check_packs.py" "$OUT" "${STAGED[@]}"
# provides.json is what tools/build_provides.py writes; a hand edit would be overwritten by the next build, so say so first.
