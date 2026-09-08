from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
MINECRAFTIZE_DIR = HERE.parent / "minecraftize"
GENERATION_DIR = HERE.parent / "generation"
for dependency_dir in (MINECRAFTIZE_DIR, GENERATION_DIR):
    if str(dependency_dir) not in sys.path:
        sys.path.insert(0, str(dependency_dir))

from block_model import BlockModelError, read_blocks_json
from runtime_contract import (
    HUNYUAN3D_MODEL,
    HUNYUAN3D_MODEL_REVISION,
    HUNYUAN3D_SOURCE_COMMIT,
    HUNYUAN3D_SOURCE_REPO,
    HUNYUAN3D_SUBFOLDER,
    HUNYUANDIT_MODEL,
    HUNYUANDIT_MODEL_REVISION,
    HUNYUANDIT_PIPELINE,
    SHAPE_RUNTIME,
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
MINECRAFT_VERSION = "1.21.4"
REQUIRED_RUNTIME_PACKAGES = {
    "torch", "diffusers", "transformers", "accelerate", "huggingface_hub", "Pillow", "hy3dgen", "mcschematic"
}
REQUIRED_RUNTIME_EXECUTABLES = {"git", "blender"}
REQUIRED_PREFLIGHT_DECLARED = {
    "blender_version",
    "gpu_name",
    "gpu_vram_gb",
    "cuda_driver",
    "cuda_runtime",
    "minecraft_client_version",
    "fabric_loader_version",
    "fabric_api_version",
    "axiom_client_version",
    "axiom_client_sha256",
    "paper_version_build",
    "axiompaper_version",
    "axiompaper_sha256",
    "permission_mode",
    "viaversion",
    "worldguard",
    "plotsquared",
    "coreprotect",
    "axiom_license_state",
    "hunyuan3d_source_commit",
    "hunyuan3d_model_revision",
    "hunyuandit_model_revision",
}


class ArtifactValidationError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactValidationError(f"cannot read JSON artifact {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ArtifactValidationError(f"JSON artifact root must be an object: {path}")
    return payload


def _require(payload: dict[str, Any], key: str, *, where: str) -> Any:
    if key not in payload:
        raise ArtifactValidationError(f"{where} missing required field: {key}")
    return payload[key]


def _require_string(payload: dict[str, Any], key: str, *, where: str) -> str:
    value = _require(payload, key, where=where)
    if not isinstance(value, str) or not value.strip():
        raise ArtifactValidationError(f"{where}.{key} must be a non-empty string")
    return value.strip()


def _require_sha(value: Any, *, where: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise ArtifactValidationError(f"{where} must be a lowercase SHA-256 hex digest")
    return value


def _check_file_hash(path: Path, expected: Any, *, where: str, require_exists: bool = True) -> None:
    if require_exists and (not path.is_file() or path.stat().st_size == 0):
        raise ArtifactValidationError(f"required artifact missing/empty: {path}")
    expected_sha = _require_sha(expected, where=where)
    if path.is_file():
        actual = sha256_file(path)
        if actual != expected_sha:
            raise ArtifactValidationError(f"artifact digest mismatch for {path}: {actual} != {expected_sha}")


def validate_preflight(environment_path: Path) -> None:
    payload = read_json(environment_path)
    if payload.get("schema_version") != 1 or payload.get("stage") != "preflight":
        raise ArtifactValidationError("environment.json must be preflight schema_version 1")
    if payload.get("status") != "PREFLIGHT_CAPTURED_RUNTIME_NOT_STARTED":
        raise ArtifactValidationError("environment.json has invalid preflight status")
    for key in ("system", "python", "packages", "executables", "declared", "hunyuan_source_checkout", "runtime_api_contract"):
        if not isinstance(payload.get(key), dict):
            raise ArtifactValidationError(f"environment.json.{key} must be an object")
    if payload.get("runtime_launched") is not False:
        raise ArtifactValidationError("preflight runtime_launched must be false")

    packages = payload["packages"]
    missing_packages = sorted(name for name in REQUIRED_RUNTIME_PACKAGES if not str(packages.get(name) or "").strip())
    if missing_packages:
        raise ArtifactValidationError(f"preflight runtime packages missing: {missing_packages}")
    executables = payload["executables"]
    missing_executables = sorted(name for name in REQUIRED_RUNTIME_EXECUTABLES if not str(executables.get(name) or "").strip())
    if missing_executables:
        raise ArtifactValidationError(f"preflight runtime executables missing from PATH: {missing_executables}")

    api_contract = payload["runtime_api_contract"]
    if api_contract.get("status") != "PASS":
        raise ArtifactValidationError(
            f"installed generation API contract is incompatible: {api_contract.get('error') or api_contract.get('missing')}"
        )

    source = payload["hunyuan_source_checkout"]
    if source.get("error") not in (None, ""):
        raise ArtifactValidationError(f"cannot verify installed Hunyuan source checkout: {source.get('error')}")
    if source.get("commit") != HUNYUAN3D_SOURCE_COMMIT:
        raise ArtifactValidationError("installed Hunyuan source commit does not match pinned source commit")
    if source.get("dirty") is not False:
        raise ArtifactValidationError("installed Hunyuan source checkout must be clean")
    _require_string(source, "path", where="environment.json.hunyuan_source_checkout")

    declared = payload["declared"]
    missing = sorted(REQUIRED_PREFLIGHT_DECLARED - set(declared))
    if missing:
        raise ArtifactValidationError(f"environment.json missing declared runtime fields: {missing}")
    unknown = [key for key in REQUIRED_PREFLIGHT_DECLARED if not str(declared.get(key, "")).strip()]
    if unknown:
        raise ArtifactValidationError(f"environment.json has empty declared runtime fields: {sorted(unknown)}")
    _require_sha(declared.get("axiom_client_sha256"), where="environment.json.declared.axiom_client_sha256")
    _require_sha(declared.get("axiompaper_sha256"), where="environment.json.declared.axiompaper_sha256")
    try:
        vram = float(declared.get("gpu_vram_gb"))
    except (TypeError, ValueError) as exc:
        raise ArtifactValidationError("environment.json.declared.gpu_vram_gb must be numeric") from exc
    if not math.isfinite(vram) or vram <= 0:
        raise ArtifactValidationError("environment.json.declared.gpu_vram_gb must be positive finite")
    expected_pins = {
        "hunyuan3d_source_commit": HUNYUAN3D_SOURCE_COMMIT,
        "hunyuan3d_model_revision": HUNYUAN3D_MODEL_REVISION,
        "hunyuandit_model_revision": HUNYUANDIT_MODEL_REVISION,
    }
    for key, expected in expected_pins.items():
        if declared.get(key) != expected:
            raise ArtifactValidationError(f"environment.json.declared.{key} must equal pinned {expected}")


def validate_text_reference(reference_path: Path, manifest_path: Path) -> None:
    payload = read_json(manifest_path)
    if payload.get("schema_version") != 1 or payload.get("stage") != "text_reference":
        raise ArtifactValidationError("text reference manifest schema/stage mismatch")
    if payload.get("status") != "GENERATED_REFERENCE_REVIEW_REQUIRED":
        raise ArtifactValidationError("text reference manifest status mismatch")
    if payload.get("pipeline") != HUNYUANDIT_PIPELINE:
        raise ArtifactValidationError("text reference pipeline identity mismatch")
    for key in ("model", "model_revision", "resolved_prompt"):
        _require_string(payload, key, where="text_reference manifest")
    if payload.get("model") != HUNYUANDIT_MODEL or payload.get("model_revision") != HUNYUANDIT_MODEL_REVISION:
        raise ArtifactValidationError("text reference manifest model identity does not match pinned contract")
    params = payload.get("params")
    if not isinstance(params, dict) or int(params.get("steps", 0)) <= 0:
        raise ArtifactValidationError("text reference manifest params invalid")
    _check_file_hash(reference_path, payload.get("output_sha256"), where="text_reference.output_sha256")


def validate_shape(glb_path: Path, manifest_path: Path) -> None:
    payload = read_json(manifest_path)
    if payload.get("schema_version") != 1 or payload.get("stage") != "shape":
        raise ArtifactValidationError("shape manifest schema/stage mismatch")
    if payload.get("status") != "GENERATED_GLB_RUNTIME_REVIEW_REQUIRED":
        raise ArtifactValidationError("shape manifest status mismatch")
    for key in ("model", "model_revision", "subfolder"):
        _require_string(payload, key, where="shape manifest")
    source_code = payload.get("source_code")
    resolved_source = payload.get("resolved_source_checkout")
    if not isinstance(source_code, dict) or not isinstance(resolved_source, dict):
        raise ArtifactValidationError("shape manifest source identity objects are required")
    if (
        payload.get("model") != HUNYUAN3D_MODEL
        or payload.get("model_revision") != HUNYUAN3D_MODEL_REVISION
        or payload.get("subfolder") != HUNYUAN3D_SUBFOLDER
        or source_code.get("repository") != HUNYUAN3D_SOURCE_REPO
        or source_code.get("commit") != HUNYUAN3D_SOURCE_COMMIT
        or resolved_source.get("commit") != HUNYUAN3D_SOURCE_COMMIT
        or resolved_source.get("dirty") is not False
    ):
        raise ArtifactValidationError("shape manifest source/model identity does not match clean pinned contract")
    _require_string(resolved_source, "path", where="shape manifest.resolved_source_checkout")
    runtime = payload.get("runtime")
    if not isinstance(runtime, dict) or runtime != SHAPE_RUNTIME:
        raise ArtifactValidationError("shape manifest runtime extraction settings drift")
    inputs = payload.get("inputs")
    if not isinstance(inputs, dict) or not inputs:
        raise ArtifactValidationError("shape manifest.inputs must contain hashed input views")
    for name, item in inputs.items():
        if name not in {"front", "right", "back", "left"} or not isinstance(item, dict):
            raise ArtifactValidationError(f"shape manifest.inputs.{name} is invalid")
        path = Path(_require_string(item, "path", where=f"shape manifest.inputs.{name}")).expanduser()
        _check_file_hash(path, item.get("sha256"), where=f"shape manifest.inputs.{name}.sha256")
    mesh = payload.get("mesh")
    if not isinstance(mesh, dict) or int(mesh.get("vertices", 0)) <= 0 or int(mesh.get("faces", 0)) <= 0:
        raise ArtifactValidationError("shape manifest mesh counts must be positive")
    _check_file_hash(glb_path, payload.get("output_sha256"), where="shape.output_sha256")


def validate_blender(target_blend: Path, target_json: Path) -> None:
    payload = read_json(target_json)
    if payload.get("schema_version") != 1 or payload.get("stage") != "blender":
        raise ArtifactValidationError("target.json must be blender schema_version 1")
    if payload.get("status") != "PREPARED_TARGET_RUNTIME_CONVERSION_PENDING":
        raise ArtifactValidationError("target.json status mismatch")
    source = payload.get("source")
    blender = payload.get("blender")
    target = payload.get("target")
    orientation = payload.get("orientation")
    cleanup = payload.get("cleanup")
    for name, item in (("source", source), ("blender", blender), ("target", target), ("orientation", orientation), ("cleanup", cleanup)):
        if not isinstance(item, dict):
            raise ArtifactValidationError(f"target.json.{name} must be an object")
    source_path = Path(_require_string(source, "path", where="target.json.source")).expanduser()
    _check_file_hash(source_path, source.get("sha256"), where="target.json.source.sha256")
    if source.get("selected_shape_stage") not in {"shape_text", "shape_single", "shape_multiview"}:
        raise ArtifactValidationError("target.json.source.selected_shape_stage is invalid")
    _require_string(blender, "version", where="target.json.blender")
    if blender.get("target_object_name") != "LazyBuilderTarget":
        raise ArtifactValidationError("target.json.blender.target_object_name must be LazyBuilderTarget")
    width = target.get("target_width_blocks")
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
        raise ArtifactValidationError("target.json.target.target_width_blocks must be a positive integer")
    bounds = target.get("bounds_world")
    if not isinstance(bounds, dict) or set(bounds) != {"min", "max"}:
        raise ArtifactValidationError("target.json.target.bounds_world must contain min/max")
    vectors = []
    for key in ("min", "max"):
        vec = bounds[key]
        if not isinstance(vec, list) or len(vec) != 3 or not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in vec):
            raise ArtifactValidationError(f"target.json.target.bounds_world.{key} must contain three finite numbers")
        vectors.append(vec)
    if any(vectors[1][axis] <= vectors[0][axis] for axis in range(3)):
        raise ArtifactValidationError("target.json target bounds must have positive extent on every axis")
    if orientation.get("minecraft_x") != "blender_x" or orientation.get("minecraft_y") != "blender_z" or orientation.get("minecraft_z") != "-blender_y":
        raise ArtifactValidationError("target.json orientation mapping drift")
    if not isinstance(cleanup.get("notes"), list):
        raise ArtifactValidationError("target.json.cleanup.notes must be an array")
    _check_file_hash(target_blend, payload.get("target_blend_sha256"), where="target.json.target_blend_sha256")


def validate_minecraftize(blocks_path: Path, report_path: Path, *, primitives: bool) -> None:
    try:
        blocks = read_blocks_json(blocks_path)
    except BlockModelError as exc:
        raise ArtifactValidationError(str(exc)) from exc
    report = read_json(report_path)
    if report.get("schema_version") != 1 or report.get("status") != "PASS":
        raise ArtifactValidationError("Minecraftize report must be schema_version 1 with PASS status")
    _require_string(report, "engine", where="Minecraftize report")
    if blocks.get("block_count", 0) <= 0:
        raise ArtifactValidationError("Minecraftize blocks.json must contain at least one block")
    if primitives:
        cases = report.get("cases")
        if not isinstance(cases, dict):
            raise ArtifactValidationError("primitive report.cases must be an object")
        interior = cases.get("v0_full_block_box_5x5x5_interior")
        if not isinstance(interior, dict) or interior.get("status") != "PASS":
            raise ArtifactValidationError("primitive suite must prove 5x5x5 interior occupancy case")
        if blocks["block_count"] != interior.get("expected_blocks") or blocks["bounds"]["size"] != interior.get("expected_bounds"):
            raise ArtifactValidationError("primitive blocks.json does not match reported 5x5x5 proof")
        for feature in ("stairs", "slabs"):
            item = cases.get(feature)
            if not isinstance(item, dict) or item.get("status") != "SKIPPED":
                raise ArtifactValidationError(f"primitive suite {feature} must remain SKIPPED in V0")
    else:
        features = report.get("features")
        if not isinstance(features, dict) or features.get("full_block") != "SUPPORTED":
            raise ArtifactValidationError("Minecraftize model report must support full_block")
        if features.get("stair") != "SKIPPED" or features.get("slab") != "SKIPPED":
            raise ArtifactValidationError("Minecraftize V0 stair/slab must remain SKIPPED")
        if report.get("occupied_cells") != blocks["block_count"]:
            raise ArtifactValidationError("Minecraftize report occupied_cells does not match canonical block_count")
        if report.get("grid_minecraft_axes") != blocks["bounds"]["size"]:
            raise ArtifactValidationError("Minecraftize report grid_minecraft_axes does not match block bounds")


def validate_preview(preview_path: Path, manifest_path: Path) -> None:
    payload = read_json(manifest_path)
    if payload.get("schema_version") != 1 or payload.get("stage") != "minecraft_preview":
        raise ArtifactValidationError("preview manifest schema/stage mismatch")
    if payload.get("status") != "PREVIEW_READY_FROM_CANONICAL_BLOCKS":
        raise ArtifactValidationError("preview manifest status mismatch")
    source_path = Path(_require_string(payload, "source_blocks", where="preview manifest")).expanduser()
    _check_file_hash(source_path, payload.get("source_sha256"), where="preview manifest.source_sha256")
    try:
        source = read_blocks_json(source_path)
    except BlockModelError as exc:
        raise ArtifactValidationError(str(exc)) from exc
    if payload.get("block_count") != source["block_count"] or payload.get("bounds") != source["bounds"]:
        raise ArtifactValidationError("preview manifest metadata does not match canonical source blocks")
    _check_file_hash(preview_path, payload.get("output_sha256"), where="preview manifest.output_sha256")


def validate_schematic(schem_path: Path, manifest_path: Path) -> None:
    payload = read_json(manifest_path)
    if payload.get("schema_version") != 1 or payload.get("stage") != "schematic":
        raise ArtifactValidationError("schematic manifest schema/stage mismatch")
    if payload.get("status") != "WRITER_ROUND_TRIP_PASS_RUNTIME_AXIOM_REQUIRED":
        raise ArtifactValidationError("schematic manifest status mismatch")
    if payload.get("writer") != "mcschematic==11.4.4" or payload.get("minecraft_version") != MINECRAFT_VERSION or payload.get("sponge_version") != 2 or payload.get("data_version") != 4189:
        raise ArtifactValidationError("schematic manifest version/writer contract mismatch")
    source_path = Path(_require_string(payload, "source_blocks", where="schematic manifest")).expanduser()
    _check_file_hash(source_path, payload.get("source_sha256"), where="schematic manifest.source_sha256")
    try:
        source = read_blocks_json(source_path)
    except BlockModelError as exc:
        raise ArtifactValidationError(str(exc)) from exc
    if payload.get("source_block_count") != source["block_count"] or payload.get("source_bounds") != source["bounds"]:
        raise ArtifactValidationError("schematic manifest source metadata does not match canonical blocks")
    if payload.get("round_trip_verified_block_count") != source["block_count"]:
        raise ArtifactValidationError("schematic round-trip verified count does not cover every source block")
    samples = payload.get("round_trip_samples")
    if not isinstance(samples, list) or len(samples) > 64:
        raise ArtifactValidationError("schematic round-trip samples must be a bounded array (max 64)")
    _check_file_hash(schem_path, payload.get("output_sha256"), where="schematic manifest.output_sha256")


def validate_axiom(runtime_path: Path) -> None:
    payload = read_json(runtime_path)
    if payload.get("schema_version") != 1 or payload.get("stage") != "axiom":
        raise ArtifactValidationError("runtime.json must be axiom schema_version 1")
    if payload.get("status") != "PASS":
        raise ArtifactValidationError("runtime.json can only validate as PASS after actual runtime proof")
    checks = payload.get("checks")
    if not isinstance(checks, dict):
        raise ArtifactValidationError("runtime.json.checks must be an object")
    required = {"import", "clipboard", "placement", "minecraft_world", "visual_state"}
    if set(checks) != required or any(checks[key] != "PASS" for key in required):
        raise ArtifactValidationError("runtime.json checks must all be PASS for exact runtime evidence")
    for name in ("schematic", "environment"):
        item = payload.get(name)
        if not isinstance(item, dict):
            raise ArtifactValidationError(f"runtime.json.{name} must be an object")
        path = Path(_require_string(item, "path", where=f"runtime.json.{name}")).expanduser()
        _check_file_hash(path, item.get("sha256"), where=f"runtime.json.{name}.sha256")
    notes = payload.get("notes", [])
    if not isinstance(notes, list) or any(not isinstance(note, str) for note in notes):
        raise ArtifactValidationError("runtime.json.notes must be an array of strings")


def validate_stage_artifacts(stage_id: str, output_paths: list[str]) -> None:
    paths = [Path(raw) for raw in output_paths]
    if stage_id == "preflight":
        validate_preflight(paths[0])
    elif stage_id == "text_reference":
        validate_text_reference(paths[0], paths[1])
    elif stage_id in {"shape_text", "shape_single", "shape_multiview"}:
        validate_shape(paths[0], paths[1])
    elif stage_id == "blender":
        validate_blender(paths[0], paths[1])
    elif stage_id == "minecraftize_primitives":
        validate_minecraftize(paths[0], paths[1], primitives=True)
    elif stage_id == "minecraftize_model":
        validate_minecraftize(paths[0], paths[1], primitives=False)
    elif stage_id == "minecraft_preview":
        validate_preview(paths[0], paths[1])
    elif stage_id == "schematic":
        validate_schematic(paths[0], paths[1])
    elif stage_id == "axiom":
        validate_axiom(paths[0])
    else:
        raise ArtifactValidationError(f"no artifact validator for stage: {stage_id}")
