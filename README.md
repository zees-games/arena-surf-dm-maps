# arena-surf-dm-maps

The combat surf maps [game-arena](https://github.com/zees-games/game-arena) plays as a deathmatch, as a repository of their own: the imported maps in `maps/` and the list of them with their authors in `maps.json`.

These are maps from the surf genre that are not courses: small maps with buy zones, weapons on the floor and teleports back to a spawn, built to fight on. Each manifest says `"kind": "arena"`, and that is what game-arena looks for; a map that says otherwise is skipped.

Every map here is somebody else's work, made for the genre years ago and imported so it can be played again. Each one is credited below and on screen whenever a server changes to it. If you made one of these maps and want it credited differently or taken down, open an issue and it will be done.

## Why the maps are not in the game's repository

game-arena ships with its three built-in maps only. A server that wants these names them in its content configuration, and each map is its own signed pack, `gamemann/<map id>`, fetched when the server changes to it, so a player joining downloads the map that is running and not 170 MB of maps. Keeping them here means a map can be added, fixed or withdrawn without a release of the game.

## Layout

```
maps/<id>/<id>.json      what the importer produced: the map's manifest,
maps/<id>/<id>.bin       its geometry, lightmap and textures,
maps/<id>/textures/      with the .import markers beside them
maps.json                every map, its author and its source page
```

## Using it

For local development, game-arena's `maps/imported` is a link to this repository's `maps/` (dot-bootstrap makes it from the `# bootstrap-link:` line in the game's `.gitignore`). That is the path the `.import` markers were written against, so the game imports and tests these files without a copy. Without the link the game plays its built-in maps, which is supported.

**Releasing is a tag**: `git tag v1.x.y && git push --tags`. `.github/workflows/release.yml` calls dot-ci's `release-maps.yml`, which checks game-arena out beside this repository, links `maps/` in, imports, and attaches one `<map>-<version>-pack.zip` per map; the site publishes each as `gamemann/<map>@<version>` and signs it.

## Credits

| Map | Author | Source |
| --- | --- | --- |
| `surf_10x_final` | Wof- | https://gamebanana.com/mods/121522 |
| `surf_10x_reloaded_fixed` | Buck Nasty | https://gamebanana.com/mods/121524 |
| `surf_110b_austinpowers` | TheInvoker | https://gamebanana.com/mods/121530 |
| `surf_29_12_06` | matrix-hetman | https://gamebanana.com/mods/121540 |
| `surf_adverse` | target practice, Archangel | https://gamebanana.com/mods/137677 |
| `surf_akai_final` | akai | https://gamebanana.com/mods/121606 |
| `surf_bathroom_final` | smooth | https://gamebanana.com/mods/121698 |
| `surf_buck_wild` | buck nasty | https://gamebanana.com/mods/121787 |
| `surf_dust2_2008_final` | Matrix Hetman, Karatekäfer | https://gamebanana.com/mods/121962 |
| `surf_forbidden_ways_2nd` | krusty | https://gamebanana.com/mods/122075 |
| `surf_forbidden_ways_reloaded` | Krusty, sky by Karatekäfer | https://gamebanana.com/mods/122076 |
| `surf_fruits` | Sangre, Hellraisedsurfer, Robsonfire, Machine, Jaden, Komaokc, Icecreamlock, Shahzam, SKAR, JackTheStripper (copy-mark), Linus | https://gamebanana.com/mods/122092 |
| `surf_grave_reloaded` | xblah | https://gamebanana.com/mods/122151 |
| `surf_greatriver` | Ace Of Spades13 | https://gamebanana.com/mods/122158 |
| `surf_greatriver_v4` | BeNnY | https://gamebanana.com/mods/122202 |
| `surf_greatriver_xdre4m` | !Black, with Ace Of Spades13 and Junior | https://gamebanana.com/mods/122206 |
| `surf_i_hate_campers` | Snah | https://gamebanana.com/mods/122339 |
| `surf_japan_ptad` | ptad, monkeydie | https://gamebanana.com/mods/137687 |
| `surf_legends` | SintaxError | https://gamebanana.com/mods/122424 |
| `surf_machine2` | Z-machine | https://gamebanana.com/mods/122478 |
| `surf_machine_remix_final` | paper-cut, z-machine(original) | https://gamebanana.com/mods/122497 |
| `surf_mai_remix` | Krusty | https://gamebanana.com/mods/122505 |
| `surf_matrix_v8` | Flippi273 | https://gamebanana.com/mods/122520 |
| `surf_ny_advance` | faj | https://gamebanana.com/mods/122641 |
| `surf_ny_bigloop_2008a` | Paper-Cut, FAJ | https://gamebanana.com/mods/122644 |
| `surf_parrot_selector` | ptad | https://gamebanana.com/mods/122709 |
| `surf_pavilion` | Black Sheep | https://gamebanana.com/mods/122711 |
| `surf_pox` | Krusty, Pariah, Karatekäfer, Korr | https://gamebanana.com/mods/122741 |
| `surf_rebel_resistance_final3` | -)RR(-ArchAngel -)RR(-Lethalis | https://gamebanana.com/mods/122824 |
| `surf_ski_2` | Massive Boredom and Mario | https://gamebanana.com/mods/122953 |
| `surf_ski_2_source` | Korliki ''Angel | https://gamebanana.com/mods/122956 |
| `surf_skyworld` | Goerge | https://gamebanana.com/mods/122985 |
| `surf_snipers_island` | Loller Dan | https://gamebanana.com/mods/137698 |
| `surf_the_flow` | G-Flow, Karatekäfer (skybox), Stavros Xanthis | https://gamebanana.com/mods/137701 |
| `surf_the_gloaming` | Roosta, Teeth | https://gamebanana.com/mods/123134 |
| `surf_thriller` | buck nasty | https://gamebanana.com/mods/123141 |
| `surf_torque2` | Sangre Nueva | https://gamebanana.com/mods/123157 |
| `surf_velocity` | copy-mark, jack the stripper, sangre, hellraisedsurfer, target practice, jesuswashomeless, skar | https://gamebanana.com/mods/123224 |
| `surf_xiv_v2a` | smooth.nl | https://gamebanana.com/mods/123284 |

`surf_i_hate_campers` is listed on its page as CC BY-NC-ND 4.0 with redistribution marked "ask"; it is credited to Snah here and on screen, and if Snah or anyone speaking for them wants it removed or credited differently, open an issue and it will be done.

`surf_snipers_island` is listed on its page as CC BY-NC-ND 4.0 with redistribution marked "ask", and the page's text does not forbid sharing or porting (checked 2026-10-20); it is credited to Loller Dan here and on screen, and if Loller Dan or anyone speaking for them wants it removed or credited differently, open an issue and it will be done.

`surf_the_flow` is listed on its page as CC BY-NC-ND 4.0, and the page's text does not forbid sharing or porting (checked 2026-10-20); it is credited to G-Flow here and on screen, and if G-Flow or anyone speaking for them wants it removed or credited differently, open an issue and it will be done.
