from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
