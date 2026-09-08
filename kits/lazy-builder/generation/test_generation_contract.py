from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from generate_text_reference import build_parser as build_text_parser, build_plan as build_text_plan
from generate_shape import build_parser as build_shape_parser, build_plan as build_shape_plan
from runtime_contract import (
    HUNYUAN3D_MODEL,
    HUNYUAN3D_MODEL_REVISION,
    HUNYUAN3D_SOURCE_COMMIT,
    HUNYUAN3D_SOURCE_REPO,
    HUNYUAN3D_SUBFOLDER,
    HUNYUANDIT_MODEL,
    HUNYUANDIT_MODEL_REVISION,
    HUNYUANDIT_PIPELINE,
    SHAPE_DEFAULTS,
    SHAPE_RUNTIME,
    TEXT_DEFAULTS,
    build_reference_prompt,
    normalize_text_prompt,
    require_pinned_hunyuan_source,
    validate_view_paths,
)


class GenerationContractTests(unittest.TestCase):
    def test_exact_model_ids_and_revisions(self) -> None:
        self.assertEqual(HUNYUANDIT_MODEL, "Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled")
        self.assertEqual(HUNYUANDIT_MODEL_REVISION, "527cf2ecce7c04021975938f8b0e44e35d2b1ed9")
        self.assertEqual(HUNYUANDIT_PIPELINE, "HunyuanDiTPipeline")
        self.assertEqual(TEXT_DEFAULTS["steps"], 25)
        self.assertEqual(HUNYUAN3D_MODEL, "tencent/Hunyuan3D-2mv")
        self.assertEqual(HUNYUAN3D_MODEL_REVISION, "08766051fa711c6ef5caf86b97e50304fdfcf0ef")
        self.assertEqual(HUNYUAN3D_SUBFOLDER, "hunyuan3d-dit-v2-mv")
        self.assertEqual(HUNYUAN3D_SOURCE_REPO, "Tencent-Hunyuan/Hunyuan3D-2")
        self.assertEqual(HUNYUAN3D_SOURCE_COMMIT, "f8db63096c8282cb27354314d896feba5ba6ff8a")

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
        self.assertEqual(SHAPE_RUNTIME["variant"], "fp16")
        self.assertEqual(SHAPE_RUNTIME["output_type"], "trimesh")

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
            self.assertEqual(plan["model_revision"], HUNYUANDIT_MODEL_REVISION)
            self.assertEqual(plan["pipeline"], "HunyuanDiTPipeline")
            self.assertNotIn("pag_scale", plan["params"])
            self.assertEqual(plan["params"]["steps"], 25)

    def test_shape_manifest_contract_records_source_model_and_extraction_pin(self) -> None:
        args = build_shape_parser().parse_args(
            ["--front", "/tmp/front.png", "--output-dir", "/tmp/shape", "--dry-run"]
        )
        plan = build_shape_plan(args, require_exists=False)
        self.assertEqual(Path(plan["outputs"]["manifest"]).name, "manifest.json")
        self.assertEqual(plan["model_revision"], HUNYUAN3D_MODEL_REVISION)
        self.assertEqual(plan["source_code"]["commit"], HUNYUAN3D_SOURCE_COMMIT)
        self.assertEqual(plan["runtime"], SHAPE_RUNTIME)

    @patch("runtime_contract.inspect_hunyuan_source_checkout")
    def test_hunyuan_source_identity_is_fail_closed(self, inspect) -> None:
        inspect.return_value = {"path": "/src", "commit": HUNYUAN3D_SOURCE_COMMIT, "dirty": False, "status_porcelain": ""}
        self.assertEqual(require_pinned_hunyuan_source("/src/hy3dgen/__init__.py")["commit"], HUNYUAN3D_SOURCE_COMMIT)
        inspect.return_value = {"path": "/src", "commit": "0" * 40, "dirty": False, "status_porcelain": ""}
        with self.assertRaisesRegex(RuntimeError, "source commit mismatch"):
            require_pinned_hunyuan_source("/src/hy3dgen/__init__.py")
        inspect.return_value = {"path": "/src", "commit": HUNYUAN3D_SOURCE_COMMIT, "dirty": True, "status_porcelain": " M file.py"}
        with self.assertRaisesRegex(RuntimeError, "local changes"):
            require_pinned_hunyuan_source("/src/hy3dgen/__init__.py")


if __name__ == "__main__":
    unittest.main()
