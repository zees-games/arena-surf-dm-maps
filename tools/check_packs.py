#!/usr/bin/env python3
"""Publish gate: a staged pack may carry no texture that was decoded from a source map's pakfile.

    check_packs.py PACKS_DIR [id...]     PACKS_DIR holds one staged pack per map (tools/stage_packs.sh OUT)

A pack's art must be mapped to free, open or own assets: the fallback tree `worlds/<id>/textures/fb_*` (CC0 PBR library),
`gen_*` (generated), the lightmap (our own bake) and the library models. The importer also decodes every texture the
source map's pakfile carries into `textures/<source_name>.png` at the pack root (and sky faces `sky_*.png`); that is third
party or Valve art with no mapping, so it must never be published. The rules, all deterministic:

  1. no `textures/` directory at the pack root, and no .vtf/.vmt/.mdl/.vtx/.vvd/.bsp/.vpk/.wav/.mp3/.ogg anywhere;
  2. no file anywhere whose normalised name equals an entry of the world's coverage lists `textures_unmapped`,
     `textures_flat` or `textures.nearest_photo` (`CS_ITALY/ORANGE` -> `cs_italy_orange`), unless it is an fb_/gen_ file;
  3. the pack is not hollow: <id>.json, <id>.bin, provides.json, licence.json and worlds/<id>/<id>.json all exist;
  4. no `.import` marker: a marker redirects every `load()` of its source to `res://.godot/imported/<hash>.ctex`, which a
     published pack does not carry (the importing project's cache), so the texture loads as null and the surface draws as a
     flat colour (crackhouse 1.0.4 on prod, 2026-11-08). A pack ships raw .webp/.png, which `Image.load_from_file` reads;
  5. every material resolves: each `pbr:` / `generated` key the world's surfaces draw has a row in the manifest's
     `licence.textures` whose pack file (`fallback_file` for a PBR set, `file` for a generated one) is in the pack, because
     a shared PBR store is not mounted for a delivered pack and that file is all the surface has; a key with no such file
     draws as a flat colour.

Exit 1 with one line per offence. Standard library only.
"""
import json
import os
import re
import sys

BANNED_EXT = {".vtf", ".vmt", ".mdl", ".vtx", ".vvd", ".bsp", ".vpk", ".wav", ".mp3", ".ogg"}
IMAGE_EXT = (".png", ".webp", ".jpg", ".jpeg", ".tga", ".bmp", ".dds", ".exr", ".hdr")
OWN_PREFIX = ("fb_", "gen_")  # the free fallback tree and the generated surfaces
REQUIRED = ("{id}.json", "{id}.bin", "provides.json", "licence.json", "worlds/{id}/{id}.json")


def norm(name):
    """Source material name or file stem, lower case, every run of non-alphanumerics one underscore."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def unmapped_names(coverage):
    lists = coverage.get("lists", {})
    names = list(lists.get("textures_unmapped", [])) + list(lists.get("textures_flat", []))
    names += list(coverage.get("textures", {}).get("nearest_photo", []))
    return {norm(n) for n in names if norm(n)}


def stem(fname):
    s = fname
    for _ in range(3):
        base, ext = os.path.splitext(s)
        if ext.lower() in IMAGE_EXT or ext.lower() == ".import":
            s = base
        else:
            break
    return s


def material_offences(root, pid):
    """Rule 5: the surfaces of worlds/<id>/<id>.json whose texture file the pack does not carry (a flat colour in game)."""
    path = os.path.join(root, "worlds", pid, pid + ".json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as f:
        world = json.load(f)
    base = os.path.dirname(path)
    rows = {}
    for t in world.get("licence", {}).get("textures", []):
        rows[str(t.get("key", ""))] = t
    bad = []
    seen = set()
    for rec in world.get("surfaces", []):
        for field in ("free", "free2"):
            key = str(rec.get(field, "") or "")
            if key in seen or not (key.startswith("pbr:") or key in rows):
                continue  # a plain kind name ("concrete") is drawn from the game's own surfaces folder
            seen.add(key)
            row = rows.get(key)
            if row is None:
                bad.append("%s: surface texture %s has no row in licence.textures (draws flat)" % (pid, key))
                continue
            rel = row.get("fallback_file") if row.get("kind") == "pbr" else row.get("file")
            if not rel or not os.path.isfile(os.path.join(base, rel)):
                bad.append("%s: surface texture %s: file %s is not in the pack (draws flat)" % (pid, key, rel))
    return bad


def check_pack(root, pid):
    """Offences (list of strings) for the staged pack at root."""
    bad = []
    for req in REQUIRED:
        rel = req.format(id=pid)
        if not os.path.isfile(os.path.join(root, rel)):
            bad.append("%s: hollow pack, %s is missing" % (pid, rel))
    if os.path.isdir(os.path.join(root, "textures")):
        n = sum(len(fs) for _, _, fs in os.walk(os.path.join(root, "textures")))
        bad.append("%s: legacy textures/ tree at the pack root (%d files decoded from the source map's pakfile)" % (pid, n))
    unmapped = set()
    cov = os.path.join(root, "worlds", pid, pid + ".coverage.json")
    if os.path.isfile(cov):
        with open(cov, encoding="utf-8") as f:
            unmapped = unmapped_names(json.load(f))
    bad += material_offences(root, pid)
    for d, _, files in os.walk(root):
        for fn in files:
            rel = os.path.relpath(os.path.join(d, fn), root)
            if fn.endswith(".import"):
                bad.append("%s: %s is an import marker; its .ctex is not in the pack, so the texture would load as null" % (pid, rel))
            if os.path.splitext(fn)[1].lower() in BANNED_EXT:
                bad.append("%s: %s is a source-engine or sound file" % (pid, rel))
                continue
            if fn.startswith(OWN_PREFIX) or not fn.lower().replace(".import", "").endswith(IMAGE_EXT):
                continue
            if "/models/" in "/" + rel.replace(os.sep, "/"):
                continue  # library model textures are named by the library, not by a source map
            if norm(stem(fn)) in unmapped:
                bad.append("%s: %s matches an unmapped source texture of the coverage report" % (pid, rel))
    return bad


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    out = argv[0]
    ids = argv[1:] or sorted(n for n in os.listdir(out) if os.path.isdir(os.path.join(out, n)))
    bad = []
    for pid in ids:
        bad += check_pack(os.path.join(out, pid), pid)
    for b in bad:
        print("check_packs: " + b, file=sys.stderr)
    print("check_packs: %d pack(s), %s" % (len(ids), "%d offence(s)" % len(bad) if bad else "clean"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
