# arena-surf-dm-maps

The combat surf maps game-arena plays, as their own repository. Read `../../CLAUDE.md`, `../game-arena/CLAUDE.md` and game-arena's `docs/imported-maps.md` first.

**Split out of g2gfast-maps on 2026-10-17.** These are the maps whose manifest says `"kind": "arena"`. game-g2gfast never played them (it kept them out of its rotation), and game-arena no longer comes with them: a server names them in dot-server-deploy's `cfg/content.yml`.

**Each map is its own signed pack, `gamemann/<map id>`, never one pack for all of them.** game-arena's `ArenaMaps.adopt_delivered` and `ArenaMapSession._mount_delivered` take one `<owner>/<id>@<version>` per map and mount a directory holding `<id>.json` directly. The pack ids are the ones these maps had in g2gfast-maps, so nothing that names them changes.

**`maps/` is linked at game-arena's `maps/imported`** (`# bootstrap-link: arena-surf-dm-maps/maps` in its `.gitignore`), the path the `.import` markers were written against. Never move them to another path in the game without re-importing.

**The importer is still game-g2gfast's.** A re-import or a new combat surf map is produced there (it writes the manifest, copying `"kind": "arena"` from the game's `maps/zones/<id>.json`, where the credits live too) and the map directory is then moved here. `maps.json` is the list with credits; keep it in step by hand when a map is added or removed, and add the README's credits row.

**Releasing is a tag**: `.github/workflows/release.yml` calls dot-ci's `release-maps.yml` with `game: zees-games/game-arena`. The repository needs the `DOT_DEPS_TOKEN` secret, like g2gfast-maps.

**Credits are mandatory**: every map in `maps.json` has an author and a source page, and the README's table says the same.

Plain git, no LFS: the largest file is well under GitHub's 100 MB limit.
