from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MINECRAFTIZE_DIR = HERE.parent / "minecraftize"
if str(MINECRAFTIZE_DIR) not in sys.path:
    sys.path.insert(0, str(MINECRAFTIZE_DIR))

from collect_environment import build_payload as build_environment_payload
from artifact_validation import (
    ArtifactValidationError,
    REQUIRED_PREFLIGHT_DECLARED,
    validate_blender,
    validate_preflight,
    validate_preview,
)
from block_model import Block, build_payload, write_blocks_json
from build_preview import build_preview


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ArtifactValidationTests(unittest.TestCase):
    def test_collector_auto_records_generation_pins(self) -> None:
        payload = build_environment_payload({"gpu_name": "RTX 3070"})
        declared = payload["declared"]
        self.assertEqual(declared["hunyuan3d_source_commit"], "f8db63096c8282cb27354314d896feba5ba6ff8a")
        self.assertEqual(declared["hunyuan3d_model_revision"], "08766051fa711c6ef5caf86b97e50304fdfcf0ef")
        self.assertEqual(declared["hunyuandit_model_revision"], "527cf2ecce7c04021975938f8b0e44e35d2b1ed9")
        self.assertFalse(payload["runtime_launched"])

    def test_preflight_requires_all_declared_runtime_facts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "environment.json"
            declared = {key: ("a" * 64 if key in {"axiom_client_sha256", "axiompaper_sha256"} else "8" if key == "gpu_vram_gb" else "known") for key in REQUIRED_PREFLIGHT_DECLARED}
            declared.update({
                "hunyuan3d_source_commit": "f8db63096c8282cb27354314d896feba5ba6ff8a",
                "hunyuan3d_model_revision": "08766051fa711c6ef5caf86b97e50304fdfcf0ef",
                "hunyuandit_model_revision": "527cf2ecce7c04021975938f8b0e44e35d2b1ed9",
            })
            payload = {
                "schema_version": 1,
                "stage": "preflight",
                "status": "PREFLIGHT_CAPTURED_RUNTIME_NOT_STARTED",
                "system": {},
                "python": {},
                "packages": {},
                "executables": {},
                "declared": declared,
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            validate_preflight(path)
            del payload["declared"]["gpu_name"]
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ArtifactValidationError):
                validate_preflight(path)

    def test_blender_target_digest_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "model.glb"
            target = root / "target.blend"
            meta = root / "target.json"
            source.write_bytes(b"glb")
            target.write_bytes(b"blend")
            payload = {
                "schema_version": 1,
                "stage": "blender",
                "status": "PREPARED_TARGET_RUNTIME_CONVERSION_PENDING",
                "source": {"path": str(source), "sha256": sha(source), "selected_shape_stage": "shape_single"},
                "blender": {"version": "5.2.x", "target_object_name": "LazyBuilderTarget"},
                "target": {"target_width_blocks": 64, "bounds_world": {"min": [0, 0, 0], "max": [1, 1, 1]}},
                "orientation": {"minecraft_x": "blender_x", "minecraft_y": "blender_z", "minecraft_z": "-blender_y"},
                "cleanup": {"notes": []},
                "target_blend_sha256": sha(target),
            }
            meta.write_text(json.dumps(payload), encoding="utf-8")
            validate_blender(target, meta)
            target.write_bytes(b"changed")
            with self.assertRaises(ArtifactValidationError):
                validate_blender(target, meta)

    def test_preview_is_derived_from_exact_canonical_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            blocks_path = root / "blocks.json"
            payload = build_payload([
                Block(0, 0, 0, "minecraft:stone_bricks"),
                Block(1, 0, 0, "minecraft:stone_bricks"),
                Block(0, 1, 0, "minecraft:stone_bricks"),
            ])
            write_blocks_json(blocks_path, payload)
            preview, manifest = build_preview(blocks_path, root / "preview")
            validate_preview(preview, manifest)
            self.assertIn("TOP X/Z", preview.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
