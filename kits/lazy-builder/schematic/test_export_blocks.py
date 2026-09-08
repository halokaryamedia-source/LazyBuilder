from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MINECRAFTIZE = HERE.parent / "minecraftize"
if str(MINECRAFTIZE) not in sys.path:
    sys.path.insert(0, str(MINECRAFTIZE))

from block_model import build_payload, write_blocks_json
from export_blocks import ROUND_TRIP_SAMPLE_LIMIT, _sample_indexes, export_blocks


class ExportBlocksTests(unittest.TestCase):
    def test_sample_indexes_are_bounded_but_cover_small_outputs(self) -> None:
        self.assertEqual(_sample_indexes(3), {0, 1, 2})
        sampled = _sample_indexes(1000)
        self.assertEqual(len(sampled), ROUND_TRIP_SAMPLE_LIMIT)
        self.assertIn(0, sampled)
        self.assertIn(999, sampled)

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
            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(data["round_trip_verified_block_count"], payload["block_count"])
            self.assertEqual(len(data["round_trip_samples"]), payload["block_count"])


if __name__ == "__main__":
    unittest.main()
