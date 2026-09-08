from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from generate_text_reference import build_parser as build_text_parser, build_plan as build_text_plan
from generate_shape import build_parser as build_shape_parser, build_plan as build_shape_plan
from runtime_contract import (
    HUNYUAN3D_MODEL,
    HUNYUAN3D_SUBFOLDER,
    HUNYUANDIT_MODEL,
    SHAPE_DEFAULTS,
    build_reference_prompt,
    normalize_text_prompt,
    validate_view_paths,
)


class GenerationContractTests(unittest.TestCase):
    def test_exact_model_ids(self) -> None:
        self.assertEqual(HUNYUANDIT_MODEL, "Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled")
        self.assertEqual(HUNYUAN3D_MODEL, "tencent/Hunyuan3D-2mv")
        self.assertEqual(HUNYUAN3D_SUBFOLDER, "hunyuan3d-dit-v2-mv")

    def test_text_prompt_is_preserved_and_canonicalized(self) -> None:
        prompt = "  Victorian   station with a clock tower  "
        resolved = build_reference_prompt(prompt)
        self.assertTrue(resolved.startswith("Victorian station with a clock tower,"))
        self.assertIn("front view", resolved)
        self.assertIn("isolated on a white background", resolved)

    def test_empty_text_prompt_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_text_prompt("   ")

    def test_named_view_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            front = root / "front.png"
            right = root / "right.jpg"
            front.write_bytes(b"front")
            right.write_bytes(b"right")
            result = validate_view_paths({"front": front, "right": right})
            self.assertEqual(set(result), {"front", "right"})

    def test_missing_views_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_view_paths({}, require_exists=False)

    def test_unsupported_extension_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_view_paths({"front": "front.txt"}, require_exists=False)

    def test_initial_8gb_shape_defaults_are_bounded(self) -> None:
        self.assertEqual(SHAPE_DEFAULTS["steps"], 30)
        self.assertEqual(SHAPE_DEFAULTS["octree_resolution"], 256)
        self.assertEqual(SHAPE_DEFAULTS["num_chunks"], 8000)
        self.assertEqual(SHAPE_DEFAULTS["seed"], 12345)

    def test_prompt_file_and_stage_manifest_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prompt_file = root / "prompt.txt"
            prompt_file.write_text("compact stone station", encoding="utf-8")
            args = build_text_parser().parse_args(
                ["--prompt-file", str(prompt_file), "--output-dir", str(root / "out")]
            )
            plan = build_text_plan(args)
            self.assertEqual(Path(plan["outputs"]["manifest"]).name, "manifest.json")
            self.assertEqual(plan["prompt"], "compact stone station")

    def test_shape_manifest_contract(self) -> None:
        args = build_shape_parser().parse_args(
            ["--front", "/tmp/front.png", "--output-dir", "/tmp/shape", "--dry-run"]
        )
        plan = build_shape_plan(args, require_exists=False)
        self.assertEqual(Path(plan["outputs"]["manifest"]).name, "manifest.json")


if __name__ == "__main__":
    unittest.main()
