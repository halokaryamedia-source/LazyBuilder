from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MINECRAFTIZE = HERE.parent / "minecraftize"
if str(MINECRAFTIZE) not in sys.path:
    sys.path.insert(0, str(MINECRAFTIZE))

from block_model import build_payload, write_blocks_json
from export_blocks import export_blocks


class ExportBlocksTests(unittest.TestCase):
    def test_fixture_exports_and_round_trips(self) -> None:
        try:
            import mcschematic  # noqa: F401
        except ImportError:
            self.skipTest("mcschematic is not installed in this local contract environment")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            blocks_path = root / "blocks.json"
            payload = build_payload(
                [
                    {"x": 0, "y": 0, "z": 0, "block_state": "minecraft:stone_bricks"},
                    {
                        "x": 1,
                        "y": 0,
                        "z": 0,
                        "block_state": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
                    },
                    {"x": 2, "y": 0, "z": 0, "block_state": "minecraft:stone_slab[type=top,waterlogged=false]"},
                ]
            )
            write_blocks_json(blocks_path, payload)
            schem, manifest = export_blocks(blocks_path, root / "out")
            self.assertTrue(schem.is_file())
            self.assertTrue(manifest.is_file())


if __name__ == "__main__":
    unittest.main()
