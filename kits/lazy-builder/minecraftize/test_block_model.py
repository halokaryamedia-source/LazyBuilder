from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from block_model import (
    BlockModelError,
    blender_to_minecraft,
    build_payload,
    canonical_block_state,
    read_blocks_json,
    validate_payload,
    write_blocks_json,
)
from build_primitive_fixture import build_fixture, load_cases


class BlockModelTests(unittest.TestCase):
    def test_blender_to_minecraft_axis_contract(self) -> None:
        self.assertEqual(blender_to_minecraft(2, -3, 5), (2, 5, 3))

    def test_block_state_properties_are_canonicalized(self) -> None:
        raw = "minecraft:stone_brick_stairs[shape=straight,waterlogged=false,half=bottom,facing=north]"
        self.assertEqual(
            canonical_block_state(raw),
            "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        )

    def test_duplicate_coordinate_is_rejected(self) -> None:
        with self.assertRaises(BlockModelError):
            build_payload(
                [
                    {"x": 0, "y": 0, "z": 0, "block_state": "minecraft:stone"},
                    {"x": 0, "y": 0, "z": 0, "block_state": "minecraft:dirt"},
                ]
            )

    def test_payload_is_deterministic_and_self_consistent(self) -> None:
        blocks = [
            {"x": 2, "y": 0, "z": 0, "block_state": "minecraft:stone_slab[waterlogged=false,type=top]"},
            {"x": 0, "y": 0, "z": 0, "block_state": "minecraft:stone_bricks"},
        ]
        first = build_payload(blocks)
        second = build_payload(reversed(blocks))
        self.assertEqual(first, second)
        self.assertEqual(first["bounds"]["size"], {"x": 3, "y": 1, "z": 1})
        self.assertEqual(first["block_count"], 2)
        validate_payload(first)

    def test_round_trip_blocks_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "blocks.json"
            payload = build_payload([
                {"x": 0, "y": 0, "z": 0, "block_state": "minecraft:stone_bricks", "source_reason": "test"}
            ])
            write_blocks_json(path, payload)
            self.assertEqual(read_blocks_json(path), payload)

    def test_primitive_fixture_covers_locked_families(self) -> None:
        cases_path = Path(__file__).with_name("fixtures") / "primitive_cases.json"
        cases = load_cases(cases_path)
        families = {case["family"] for case in cases}
        self.assertTrue({"full", "stair", "stair_corner", "slab"}.issubset(families))
        blocks, report = build_fixture(cases)
        validate_payload(blocks)
        self.assertFalse(report["engine_runtime_proven"])
        self.assertEqual(blocks["block_count"], len(cases))


if __name__ == "__main__":
    unittest.main()
