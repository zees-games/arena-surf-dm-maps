#!/bin/bash
# Store each map's source .bsp (credit from its licence.json) and rebuild its world through dot-map's global importer.
#   [SRC=dir] tools/regen_worlds.sh [map ids...]   default: every maps/<id> with a source .bsp; writes worlds/<id>/<id>.*
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$HERE/.."
SRC="${SRC:-$HOME/godot/inspirations/g2gfast}"
BSP="${DOTBSP_PATH:-$HERE/../../dot-map/tools/bsp}/bsp.py"
ids=("$@"); [ ${#ids[@]} -eq 0 ] && ids=($(ls "$ROOT/maps"))
rc=0
for m in "${ids[@]}"; do
    f="$(find "$SRC" -maxdepth 1 -iname "$m.bsp" | head -1)"
    [ -z "$f" ] && { echo "$m NO SOURCE"; rc=1; continue; }
    read -r author page < <(python3 -I -c 'import json,sys
for e in json.load(open(sys.argv[1])):
    if e.get("author") and e.get("source_url"): print(e["author"].replace(" ","_"), e["source_url"]); break' "$ROOT/maps/$m/licence.json")
    python3 -I "$BSP" store "$f" --game arena --author "${author//_/ }" --page "$page" --licence "none stated" --no-share-check "2026-10-28: credited with removal on request" > /dev/null 2>&1
    key="arena/$(basename "$f" .bsp)"
    mkdir -p "$ROOT/worlds/$m"
    heavy -- timeout 1800 python3 -I "$BSP" regen "$key" --out "$ROOT/worlds/$m/$m" --pbr-store "$ROOT/pbr-library" --model-store "$ROOT/model-library" > "${TMPDIR:-/tmp}/regen-$m.log" 2>&1 < /dev/null
    r=$?; [ $r -ne 0 ] && rc=1
    echo "$m exit $r"
done
exit $rc
