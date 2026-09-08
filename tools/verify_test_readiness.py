#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "kits/lazy-builder/validator/TEST-READINESS.md",
    "kits/lazy-builder/validator/FIXTURE-PACK.md",
    "kits/lazy-builder/validator/ARTIFACT-CONTRACTS.md",
    "kits/lazy-builder/validator/VALIDATION.md",
    "kits/lazy-builder/validator/case.template.json",
    "kits/lazy-builder/validator/prepare_case.py",
    "kits/lazy-builder/validator/collect_environment.py",
    "kits/lazy-builder/validator/artifact_validation.py",
    "kits/lazy-builder/validator/session_contract.py",
    "kits/lazy-builder/validator/session_controller.py",
    "kits/lazy-builder/validator/refresh_case_input.py",
    "kits/lazy-builder/validator/write_runtime_evidence.py",
    "kits/lazy-builder/validator/dry_run_readiness.py",
    "kits/lazy-builder/validator/acceptance_report.py",
    "kits/lazy-builder/validator/test_test_readiness.py",
    "kits/lazy-builder/validator/test_artifact_validation.py",
    "kits/lazy-builder/generation/ENVIRONMENT.md",
    "kits/lazy-builder/generation/runtime_contract.py",
    "kits/lazy-builder/blender/TARGET-MODEL.md",
    "kits/lazy-builder/blender/write_target_metadata.py",
    "kits/lazy-builder/minecraftize/block_model.py",
    "kits/lazy-builder/minecraftize/minecraftize_v0.py",
    "kits/lazy-builder/minecraftize/run_primitive_suite.py",
    "kits/lazy-builder/minecraftize/build_preview.py",
    "kits/lazy-builder/minecraftize/test_minecraftize_v0.py",
    "kits/lazy-builder/schematic/export_blocks.py",
    "kits/lazy-builder/schematic/test_export_blocks.py",
    ".github/workflows/test-readiness-verify.yml",
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing pre-runtime owner: {rel}")

    markers = {
        "kits/lazy-builder/generation/runtime_contract.py": [
            'HUNYUAN3D_MODEL_REVISION = "08766051fa711c6ef5caf86b97e50304fdfcf0ef"',
            'HUNYUANDIT_MODEL_REVISION = "527cf2ecce7c04021975938f8b0e44e35d2b1ed9"',
            'HUNYUAN3D_SOURCE_COMMIT = "f8db63096c8282cb27354314d896feba5ba6ff8a"',
            'HUNYUANDIT_PIPELINE = "HunyuanDiTPipeline"',
            "require_pinned_hunyuan_source",
            '"mc_level": 0.0',
        ],
        "kits/lazy-builder/generation/generate_shape.py": [
            "resolved_source_checkout", "require_pinned_hunyuan_source", "SHAPE_RUNTIME", "returned no mesh",
        ],
        "kits/lazy-builder/generation/generate_text_reference.py": [
            "HunyuanDiTPipeline", "guidance_scale", "num_inference_steps",
        ],
        "kits/lazy-builder/validator/collect_environment.py": [
            "runtime_api_contract", "hunyuan_source_checkout", "inspect.signature",
        ],
        "kits/lazy-builder/validator/session_contract.py": [
            '"shape_text"', '"shape_single"', '"shape_multiview"', '"minecraft_preview"',
            '"minecraftize_primitives"', '"dependencies": ("preflight",)',
            'MINECRAFT_VERSION = "1.21.4"', "input drift detected",
        ],
        "kits/lazy-builder/validator/session_controller.py": [
            "APPROVAL_GATED_STAGES", "write_runtime_evidence.py", "runtime.json schematic digest",
            "collect_environment.py", "write_target_metadata.py", "run_primitive_suite.py", "build_preview.py",
        ],
        "kits/lazy-builder/validator/refresh_case_input.py": [
            "refresh_input_snapshot", "OWNER_STAGE", "invalidate_from",
        ],
        "kits/lazy-builder/validator/write_runtime_evidence.py": [
            '"schematic"', '"environment"', '"visual_state"', '"recorded_at"',
        ],
        "kits/lazy-builder/validator/artifact_validation.py": [
            "REQUIRED_RUNTIME_PACKAGES", "REQUIRED_RUNTIME_EXECUTABLES", "runtime_api_contract",
            "resolved_source_checkout", "round_trip_verified_block_count", "validate_axiom",
        ],
        "kits/lazy-builder/schematic/export_blocks.py": [
            "ROUND_TRIP_SAMPLE_LIMIT = 64", "round_trip_verified_block_count", 'MCSCHEMATIC_VERSION = "JE_1_21_4"',
        ],
        "kits/lazy-builder/minecraftize/run_primitive_suite.py": [
            "v0_full_block_box_3x2x2_boundary", "v0_full_block_box_5x5x5_interior", "requires_non_surface_occupancy",
        ],
        "kits/lazy-builder/minecraftize/build_preview.py": [
            "PREVIEW_READY_FROM_CANONICAL_BLOCKS", "TOP X/Z", "FRONT X/Y", "RIGHT Z/Y",
        ],
        "kits/lazy-builder/validator/TEST-READINESS.md": [
            "PRE_RUNTIME_SYSTEM_READY_RUNTIME_NOT_STARTED", "fail-closed", "Runtime Acceptance",
            "STATIC_PRE_RUNTIME_DRY_RUN_PASS_RUNTIME_NOT_STARTED",
        ],
        "docs/knowledge/next-action.md": [
            "PRE_RUNTIME_SYSTEM_READY_RUNTIME_NOT_STARTED", "Do not start runtime",
        ],
        "README.md": ["T1 TEXT", "I1 SINGLE IMAGE", "I2 MULTIVIEW", "Pre-Runtime Verification"],
    }
    for rel, expected in markers.items():
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in expected:
            if marker not in text:
                errors.append(f"{rel} missing pre-runtime marker: {marker}")

    forbidden = {
        "kits/lazy-builder/generation/generate_text_reference.py": ["enable_pag", "pag_applied_layers", "pag_scale"],
        "kits/lazy-builder/generation/runtime_contract.py": ["pag_scale"],
        "kits/lazy-builder/intake/REFERENCE-INTAKE.md": ["text_reference.json"],
        "kits/lazy-builder/README.md": ["future implementation"],
        "CONTEXT.md": ["prove the first local GLB before implementing Minecraftize runtime code"],
    }
    for rel, markers_ in forbidden.items():
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers_:
            if marker in text:
                errors.append(f"{rel} contains forbidden/stale marker: {marker}")

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
        print("Pre-runtime verification FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Pre-runtime verification PASS; runtime not started")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
