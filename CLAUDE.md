# fc-surf-dm-maps

The combat surf maps game-fatal-contact plays, as their own repository. Read `../../CLAUDE.md`, `../game-arena/CLAUDE.md` and game-fatal-contact's `docs/imported-maps.md` first.

**Split out of airdrift-maps on 2026-10-17.** These are the maps whose manifest says `"kind": "arena"`. game-airdrift never played them (it kept them out of its rotation), and game-fatal-contact no longer comes with them: a server names them in dot-server-deploy's `cfg/content.yml`.

**Each map is its own signed pack, `gamemann/arena-surf-dm-maps-<map id>` (the manifest id stays `<map id>`), never one pack for all of them.** game-fatal-contact's `ArenaMaps.adopt_delivered` and `ArenaMapSession._mount_delivered` take one `<owner>/<id>@<version>` per map and mount a directory holding `<id>.json` directly. Published at the repo version, so a server names `gamemann/arena-surf-dm-maps-<map id>`.

**`maps/` is linked at game-fatal-contact's `maps/imported`** (`# bootstrap-link: arena-surf-dm-maps/maps` in its `.gitignore`), the path the `.import` markers were written against. Never move them to another path in the game without re-importing.

**The importer is still game-airdrift's.** A re-import or a new combat surf map is produced there (it writes the manifest, copying `"kind": "arena"` from the game's `maps/zones/<id>.json`, where the credits live too) and the map directory is then moved here. `maps.json` is the list with credits; keep it in step by hand when a map is added or removed, and add the README's credits row.

**Releasing is a tag**: `.github/workflows/release.yml` calls dot-ci's `release-maps.yml` with `game: zees-games/game-fatal-contact`. The repository needs the `DOT_DEPS_TOKEN` secret, like airdrift-maps.

**Credits are mandatory**: every map in `maps.json` has an author and a source page, and the README's table says the same.

Plain git, no LFS: the largest file is well under GitHub's 100 MB limit.

**Each map folder carries a `provides.json`, which is what lists that map's pack in the Workshop** (kind `map`, the game it is for, one entry whose `scene` is the map document beside it). `tools/build_provides.py` writes them all and `--check` verifies them; rerun it when a map is added. The pack zip holds the folder's files at its root, so the file ships.

**`surf_conflux` was removed in v1.0.4** (CC BY-NC-ND, outside the art rules). Never re-add it; tags v1.0.0 to v1.0.3 still contain it.

**`worlds/<id>/` are the global importer's output** (`tools/regen_worlds.sh <id>...`: the source .bsp into `~/mapsrc/store` as `arena/<id>`, then dot-map's `bsp.py regen`), linked into game-fatal-contact at `/worlds` and drawn in place of the legacy `.json`/`.bin` meshes by `ArenaBspMap.draw_world`. `pbr-library/` and `model-library/` beside them are the shared art stores (ignored). All 39 maps have a world. `tools/stage_packs.sh OUT` lays each map's pack source out as `maps/<id>/` plus `worlds/<id>/`, which a delivered map draws from.

**Publish rule: no source-decoded textures in a pack (owner policy, 2026-11-07).** `maps/<id>/textures/` (and any `sky_*.png`) is the importer's decode of the textures in the source map's pakfile: third-party or Valve art that is mapped to nothing free. `tools/stage_packs.sh` never copies it; a pack draws from `worlds/<id>/textures` (`fb_*` = the CC0 PBR fallback tree, `gen_*` = generated), the baked `.bin` and our own lightmap. `tools/check_packs.py` (run by `stage_packs.sh` on everything it stages, and unit-tested by `tools/test_check_packs.py` in `.github/workflows/check.yml`) fails on a root `textures/` folder, on any file named like an entry of the world's coverage `textures_unmapped` / `textures_flat` / `nearest_photo`, on .vtf/.vmt/.mdl/.bsp/.vpk or sound files, and on a hollow pack. Publish only what `stage_packs.sh` staged, never `maps/<id>` directly.
