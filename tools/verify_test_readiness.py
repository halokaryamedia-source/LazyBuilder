#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "kits/lazy-builder/validator/TEST-READINESS.md",
    "kits/lazy-builder/validator/FIXTURE-PACK.md",
    "kits/lazy-builder/validator/case.template.json",
    "kits/lazy-builder/validator/prepare_case.py",
    "kits/lazy-builder/validator/session_contract.py",
    "kits/lazy-builder/validator/session_controller.py",
    "kits/lazy-builder/validator/dry_run_readiness.py",
    "kits/lazy-builder/validator/acceptance_report.py",
    "kits/lazy-builder/validator/test_test_readiness.py",
    "kits/lazy-builder/minecraftize/block_model.py",
    "kits/lazy-builder/minecraftize/minecraftize_v0.py",
    "kits/lazy-builder/minecraftize/run_primitive_suite.py",
    "kits/lazy-builder/minecraftize/test_minecraftize_v0.py",
    "kits/lazy-builder/schematic/export_blocks.py",
    "kits/lazy-builder/schematic/test_export_blocks.py",
    ".github/workflows/test-readiness-verify.yml",
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing readiness owner: {rel}")

    markers = {
        "kits/lazy-builder/validator/session_contract.py": [
            '"shape_text"', '"shape_single"', '"shape_multiview"',
            'MINECRAFT_VERSION = "1.21.4"', '"APPROVAL_REQUIRED"',
        ],
        "kits/lazy-builder/validator/session_controller.py": [
            "run_primitive_suite.py", "minecraftize_v0.py", "LazyBuilderTarget", "select-shape", "invalidate",
        ],
        "kits/lazy-builder/minecraftize/minecraftize_v0.py": [
            'ENGINE_VERSION = "v0-full-block-bvh-1"', 'DEFAULT_OBJECT_NAME = "LazyBuilderTarget"',
            "BVHTree", "target_width_blocks", "blocks.json", "report.json",
            '"stair": "SKIPPED"', '"slab": "SKIPPED"',
        ],
        "kits/lazy-builder/minecraftize/block_model.py": [
            '"minecraft_x": "blender_x"', '"minecraft_y": "blender_z"', '"minecraft_z": "-blender_y"',
        ],
        "kits/lazy-builder/schematic/export_blocks.py": [
            'MCSCHEMATIC_VERSION = "JE_1_21_4"', "mcschematic==11.4.4", '"sponge_version": 2',
        ],
        "kits/lazy-builder/validator/TEST-READINESS.md": [
            "E2E_HARNESS_IMPLEMENTED_FIXTURE_PACK_REQUIRED", "Blender-native BVH", "STATIC_DRY_RUN_PASS_RUNTIME_DEFERRED",
        ],
    }
    for rel, expected in markers.items():
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in expected:
            if marker not in text:
                errors.append(f"{rel} missing readiness marker: {marker}")

    template = ROOT / "kits/lazy-builder/validator/case.template.json"
    if template.is_file():
        try:
            payload = json.loads(template.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid case template JSON: {exc}")
        else:
            inputs = payload.get("inputs", {})
            if set(inputs) != {"T1", "I1", "I2"}:
                errors.append("case template must contain exactly T1/I1/I2")

    if errors:
        print("Test-readiness verification FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Test-readiness verification PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
