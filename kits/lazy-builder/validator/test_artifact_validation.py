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
    REQUIRED_RUNTIME_EXECUTABLES,
    REQUIRED_RUNTIME_PACKAGES,
    validate_axiom,
    validate_blender,
    validate_preflight,
    validate_preview,
)
from block_model import Block, build_payload, write_blocks_json
from build_preview import build_preview
from write_runtime_evidence import build_payload as build_runtime_payload


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def declared_runtime_facts() -> dict[str, str]:
    result = {
        key: ("a" * 64 if key in {"axiom_client_sha256", "axiompaper_sha256"} else "8" if key == "gpu_vram_gb" else "known")
        for key in REQUIRED_PREFLIGHT_DECLARED
    }
    result.update({
        "hunyuan3d_source_commit": "f8db63096c8282cb27354314d896feba5ba6ff8a",
        "hunyuan3d_model_revision": "08766051fa711c6ef5caf86b97e50304fdfcf0ef",
        "hunyuandit_model_revision": "527cf2ecce7c04021975938f8b0e44e35d2b1ed9",
    })
    return result


def valid_preflight_payload() -> dict:
    return {
        "schema_version": 1,
        "stage": "preflight",
        "status": "PREFLIGHT_CAPTURED_RUNTIME_NOT_STARTED",
        "system": {},
        "python": {},
        "packages": {name: "1.0" for name in REQUIRED_RUNTIME_PACKAGES},
        "executables": {name: f"/bin/{name}" for name in REQUIRED_RUNTIME_EXECUTABLES},
        "hunyuan_source_checkout": {
            "path": "/src/Hunyuan3D-2",
            "commit": "f8db63096c8282cb27354314d896feba5ba6ff8a",
            "dirty": False,
            "status_porcelain": "",
            "error": None,
        },
        "runtime_api_contract": {"status": "PASS", "missing": {}, "error": None},
        "declared": declared_runtime_facts(),
        "runtime_launched": False,
    }


class ArtifactValidationTests(unittest.TestCase):
    def test_collector_auto_records_generation_pins(self) -> None:
        payload = build_environment_payload({"gpu_name": "RTX 3070"})
        declared = payload["declared"]
        self.assertEqual(declared["hunyuan3d_source_commit"], "f8db63096c8282cb27354314d896feba5ba6ff8a")
        self.assertEqual(declared["hunyuan3d_model_revision"], "08766051fa711c6ef5caf86b97e50304fdfcf0ef")
        self.assertEqual(declared["hunyuandit_model_revision"], "527cf2ecce7c04021975938f8b0e44e35d2b1ed9")
        self.assertFalse(payload["runtime_launched"])
        self.assertIn("hunyuan_source_checkout", payload)
        self.assertIn("runtime_api_contract", payload)

    def test_preflight_requires_actual_packages_executables_and_clean_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "environment.json"
            payload = valid_preflight_payload()
            path.write_text(json.dumps(payload), encoding="utf-8")
            validate_preflight(path)

            payload["packages"]["torch"] = None
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ArtifactValidationError, "packages missing"):
                validate_preflight(path)
            payload = valid_preflight_payload()
            payload["executables"]["blender"] = None
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ArtifactValidationError, "executables missing"):
                validate_preflight(path)
            payload = valid_preflight_payload()
            payload["hunyuan_source_checkout"]["dirty"] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ArtifactValidationError, "must be clean"):
                validate_preflight(path)
            payload = valid_preflight_payload()
            payload["runtime_api_contract"]["status"] = "FAIL"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ArtifactValidationError, "API contract is incompatible"):
                validate_preflight(path)

    def test_blender_target_digest_and_finite_positive_bounds_are_enforced(self) -> None:
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
            payload["target"]["bounds_world"]["max"][0] = 0
            meta.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ArtifactValidationError, "positive extent"):
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
            data = json.loads(manifest.read_text())
            data["block_count"] = 999
            manifest.write_text(json.dumps(data))
            with self.assertRaisesRegex(ArtifactValidationError, "metadata does not match"):
                validate_preview(preview, manifest)

    def test_runtime_evidence_binds_exact_schematic_and_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            schem = root / "build.schem"
            environment = root / "environment.json"
            runtime = root / "runtime.json"
            schem.write_bytes(b"schem")
            environment.write_bytes(b"env")
            checks = {name: "PASS" for name in ("import", "clipboard", "placement", "minecraft_world", "visual_state")}
            payload = build_runtime_payload(schematic=schem, environment=environment, checks=checks, notes=[])
            runtime.write_text(json.dumps(payload))
            validate_axiom(runtime)
            schem.write_bytes(b"changed")
            with self.assertRaisesRegex(ArtifactValidationError, "digest mismatch"):
                validate_axiom(runtime)


if __name__ == "__main__":
    unittest.main()
