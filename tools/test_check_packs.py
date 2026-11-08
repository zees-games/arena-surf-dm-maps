#!/usr/bin/env python3
"""Tests of the publish gate (tools/check_packs.py) and of stage_packs.sh never copying a source-decoded texture.

    python3 tools/test_check_packs.py        # stdlib only; runs in CI (.github/workflows/check.yml)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_packs  # noqa: E402

COVERAGE = {"lists": {"textures_unmapped": ["CS_ITALY/ORANGE", "COLOR/GOLDEN YELLOW"], "textures_flat": ["mustafar/blackbarrel"]},
            "textures": {"nearest_photo": ["props/cardboardbox001a"]}}


def put(path, data=b"x"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode())


def make_pack(root, pid="m1"):
    for rel in ("%s.json", "%s.bin", "%s_lightmap.png"):
        put(os.path.join(root, rel % pid))
    put(os.path.join(root, "provides.json"), "{}")
    put(os.path.join(root, "licence.json"), "{}")
    put(os.path.join(root, "worlds", pid, pid + ".json"), "{}")
    put(os.path.join(root, "worlds", pid, pid + ".coverage.json"), json.dumps(COVERAGE))
    put(os.path.join(root, "worlds", pid, "textures", "fb_Concrete044D.webp"))
    put(os.path.join(root, "worlds", pid, "textures", "gen_flat.png"))
    put(os.path.join(root, "worlds", pid, "models", "polyhaven", "clock", "textures", "cs_italy_orange.jpg"))  # library name, not a source map


class CheckPacks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "m1")
        make_pack(self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_clean_pack_passes(self):
        self.assertEqual(check_packs.check_pack(self.root, "m1"), [])

    def test_legacy_textures_tree_fails(self):
        put(os.path.join(self.root, "textures", "sky_up.png"))
        self.assertTrue(any("legacy textures/" in b for b in check_packs.check_pack(self.root, "m1")))

    def test_unmapped_name_fails_anywhere(self):
        put(os.path.join(self.root, "cs_italy_orange.png"))
        put(os.path.join(self.root, "worlds", "m1", "color_golden_yellow.png.import"))
        put(os.path.join(self.root, "props_cardboardbox001a.PNG"))
        bad = check_packs.check_pack(self.root, "m1")
        self.assertEqual(len([b for b in bad if "unmapped source texture" in b]), 3, bad)

    def test_fallback_names_pass_even_if_unmapped_name_is_inside(self):
        put(os.path.join(self.root, "worlds", "m1", "textures", "fb_cs_italy_orange.webp"))
        self.assertEqual(check_packs.check_pack(self.root, "m1"), [])

    def test_source_engine_and_sound_files_fail(self):
        put(os.path.join(self.root, "worlds", "m1", "x.vtf"))
        put(os.path.join(self.root, "boom.wav"))
        self.assertEqual(len(check_packs.check_pack(self.root, "m1")), 2)

    def test_hollow_pack_fails(self):
        os.remove(os.path.join(self.root, "m1.bin"))
        self.assertTrue(any("hollow" in b for b in check_packs.check_pack(self.root, "m1")))


class StagePacks(unittest.TestCase):
    """stage_packs.sh against a fake repository and a stub converter: the source-decoded textures/ never reach the pack."""

    def test_stage_drops_textures_and_gate_passes(self):
        tmp = tempfile.mkdtemp()
        try:
            repo = os.path.join(tmp, "repo")
            os.makedirs(os.path.join(repo, "tools"))
            shutil.copy(os.path.join(HERE, "stage_packs.sh"), os.path.join(repo, "tools"))
            shutil.copy(os.path.join(HERE, "check_packs.py"), os.path.join(repo, "tools"))
            for rel in ("m1.json", "m1.bin", "m1_lightmap.png", "provides.json", "licence.json"):
                put(os.path.join(repo, "maps", "m1", rel))
            put(os.path.join(repo, "maps", "m1", "textures", "cs_italy_orange.png"))
            put(os.path.join(repo, "maps", "m1", "textures", "sky_up.png.import"))
            put(os.path.join(repo, "worlds", "m1", "m1.json"), "{}")
            put(os.path.join(repo, "worlds", "m1", "m1.coverage.json"), json.dumps(COVERAGE))
            put(os.path.join(repo, "worlds", "m1", "textures", "fb_Grass004.webp"))
            conv = os.path.join(tmp, "convert")  # stub of dot-map-convert: `bsp.py bundle WORLD --out OUT --strict` copies the folder
            put(os.path.join(conv, "bsp.py"),
                "import shutil, sys, os\nw = sys.argv[2]\nout = sys.argv[sys.argv.index('--out') + 1]\n"
                "shutil.copytree(w, os.path.join(out, os.path.basename(w)))\n")
            out = os.path.join(tmp, "out")
            env = dict(os.environ, DOT_MAP_CONVERT=conv, DOT_PY=sys.executable)
            r = subprocess.run(["bash", os.path.join(repo, "tools", "stage_packs.sh"), out, "m1"], env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertFalse(os.path.exists(os.path.join(out, "m1", "textures")))
            self.assertTrue(os.path.isfile(os.path.join(out, "m1", "m1.bin")))
            self.assertTrue(os.path.isfile(os.path.join(out, "m1", "worlds", "m1", "textures", "fb_Grass004.webp")))
            self.assertEqual(check_packs.check_pack(os.path.join(out, "m1"), "m1"), [])
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main(verbosity=1)
