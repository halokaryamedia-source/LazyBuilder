from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA_VERSION = 1
MINECRAFT_VERSION = "1.21.4"

ALLOWED_STAGE_STATUSES = {
    "PENDING",
    "READY",
    "RUNNING",
    "APPROVAL_REQUIRED",
    "PASS",
    "FAIL",
    "BLOCKED",
    "SKIPPED",
}

STAGE_ORDER = (
    "preflight",
    "text_reference",
    "shape_text",
    "shape_single",
    "shape_multiview",
    "blender",
    "minecraftize_primitives",
    "minecraftize_model",
    "schematic",
    "axiom",
)

STAGE_DEFINITIONS: dict[str, dict[str, Any]] = {
    "preflight": {
        "folder": "00-preflight",
        "owner": "environment/bootstrap",
        "dependencies": (),
        "required": True,
        "outputs": ("environment.json",),
    },
    "text_reference": {
        "folder": "10-reference",
        "owner": "intake/generation",
        "dependencies": ("preflight",),
        "required": True,
        "outputs": ("reference_front.png", "manifest.json"),
    },
    "shape_text": {
        "folder": "19-shape-text",
        "owner": "generation",
        "dependencies": ("text_reference",),
        "required": True,
        "outputs": ("model.glb", "manifest.json"),
    },
    "shape_single": {
        "folder": "20-shape-single",
        "owner": "generation",
        "dependencies": ("preflight",),
        "required": True,
        "outputs": ("model.glb", "manifest.json"),
    },
    "shape_multiview": {
        "folder": "21-shape-multiview",
        "owner": "generation",
        "dependencies": ("preflight",),
        "required": True,
        "outputs": ("model.glb", "manifest.json"),
    },
    "blender": {
        "folder": "30-blender",
        "owner": "blender target",
        "dependencies": ("shape_text", "shape_single", "shape_multiview"),
        "required": True,
        "outputs": ("target.blend", "target.json"),
    },
    "minecraftize_primitives": {
        "folder": "40-minecraftize-primitives",
        "owner": "minecraftize primitive",
        "dependencies": ("blender",),
        "required": True,
        "outputs": ("blocks.json", "report.json"),
    },
    "minecraftize_model": {
        "folder": "41-minecraftize-model",
        "owner": "minecraftize conversion",
        "dependencies": ("minecraftize_primitives", "blender"),
        "required": True,
        "outputs": ("blocks.json", "report.json"),
    },
    "schematic": {
        "folder": "50-schematic",
        "owner": "schematic exporter",
        "dependencies": ("minecraftize_model",),
        "required": True,
        "outputs": ("build.schem", "manifest.json"),
    },
    "axiom": {
        "folder": "60-axiom",
        "owner": "axiom/paper/minecraft runtime",
        "dependencies": ("schematic",),
        "required": True,
        "outputs": ("runtime.json",),
    },
}

RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


class ContractError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
        raise ContractError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ContractError(f"JSON root must be an object: {path}")
    return payload


def write_json_atomic(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        Path(temporary_name).replace(path)
    finally:
        temporary = Path(temporary_name)
        if temporary.exists():
            temporary.unlink()


def _require_nonempty_string(payload: Mapping[str, Any], key: str, where: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{where}.{key} must be a non-empty string")
    return value.strip()


def _resolve_input(case_root: Path, raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = case_root / path
    return path.resolve()


def validate_case(
    payload: Mapping[str, Any], *, case_root: Path | None = None, require_files: bool = False
) -> dict[str, Any]:
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ContractError(f"case.schema_version must be {SCHEMA_VERSION}")
    case_id = _require_nonempty_string(payload, "case_id", "case")
    minecraft_version = _require_nonempty_string(payload, "minecraft_version", "case")
    if minecraft_version != MINECRAFT_VERSION:
        raise ContractError(
            f"case.minecraft_version must be {MINECRAFT_VERSION}, got {minecraft_version}"
        )

    inputs = payload.get("inputs")
    if not isinstance(inputs, dict):
        raise ContractError("case.inputs must be an object")

    for case_name, expected_kind in (("T1", "text"), ("I1", "single"), ("I2", "multiview")):
        item = inputs.get(case_name)
        if not isinstance(item, dict):
            raise ContractError(f"case.inputs.{case_name} must be an object")
        if item.get("kind") != expected_kind:
            raise ContractError(f"case.inputs.{case_name}.kind must be {expected_kind}")

    prompt_path = _require_nonempty_string(inputs["T1"], "prompt_path", "case.inputs.T1")
    single_views = inputs["I1"].get("views")
    if not isinstance(single_views, dict) or set(single_views) != {"front"}:
        raise ContractError("case.inputs.I1.views must contain exactly front")
    _require_nonempty_string(single_views, "front", "case.inputs.I1.views")

    multiview_views = inputs["I2"].get("views")
    required_views = {"front", "right", "back", "left"}
    if not isinstance(multiview_views, dict) or set(multiview_views) != required_views:
        raise ContractError("case.inputs.I2.views must contain front/right/back/left exactly")
    for view in sorted(required_views):
        _require_nonempty_string(multiview_views, view, "case.inputs.I2.views")

    target = payload.get("target")
    if not isinstance(target, dict):
        raise ContractError("case.target must be an object")
    width = target.get("target_width_blocks")
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
        raise ContractError("case.target.target_width_blocks must be a positive integer")

    normalized = copy.deepcopy(dict(payload))
    normalized["case_id"] = case_id
    normalized["minecraft_version"] = minecraft_version

    if require_files:
        if case_root is None:
            raise ContractError("case_root is required when require_files=True")
        expected_files = [prompt_path, single_views["front"], *multiview_views.values()]
        for raw in expected_files:
            resolved = _resolve_input(case_root, raw)
            if not resolved.is_file():
                raise ContractError(f"required case input does not exist: {resolved}")
        prompt = _resolve_input(case_root, prompt_path).read_text(encoding="utf-8").strip()
        if not prompt:
            raise ContractError("T1 prompt file must not be empty")

    return normalized


def load_case(path: Path, *, require_files: bool = False) -> tuple[dict[str, Any], Path]:
    path = path.expanduser().resolve()
    payload = read_json(path)
    return validate_case(payload, case_root=path.parent, require_files=require_files), path.parent


def validate_run_id(run_id: str) -> str:
    run_id = run_id.strip()
    if not RUN_ID_RE.fullmatch(run_id):
        raise ContractError(
            "run_id must be 1-64 characters using letters, digits, dot, underscore, or hyphen"
        )
    return run_id


def stage_folder(run_dir: Path, stage_id: str) -> Path:
    try:
        folder = STAGE_DEFINITIONS[stage_id]["folder"]
    except KeyError as exc:
        raise ContractError(f"unknown stage: {stage_id}") from exc
    return run_dir / folder


def _case_input_snapshot(case: Mapping[str, Any], case_root: Path) -> dict[str, Any]:
    def entry(raw: str) -> dict[str, Any]:
        path = _resolve_input(case_root, raw)
        return {
            "path": str(path),
            "sha256": sha256_file(path) if path.is_file() else None,
        }

    return {
        "T1": {
            "kind": "text",
            "prompt": entry(case["inputs"]["T1"]["prompt_path"]),
        },
        "I1": {
            "kind": "single",
            "views": {
                "front": entry(case["inputs"]["I1"]["views"]["front"]),
            },
        },
        "I2": {
            "kind": "multiview",
            "views": {
                view: entry(case["inputs"]["I2"]["views"][view])
                for view in ("front", "right", "back", "left")
            },
        },
    }


def create_session(
    *, case: Mapping[str, Any], case_root: Path, run_id: str, run_dir: Path
) -> dict[str, Any]:
    case = validate_case(case)
    run_id = validate_run_id(run_id)
    run_dir = run_dir.expanduser().resolve()
    now = utc_now()
    input_snapshot = _case_input_snapshot(case, case_root)
    expected = {stage_id: [str((run_dir / STAGE_DEFINITIONS[stage_id]["folder"] / name).resolve()) for name in STAGE_DEFINITIONS[stage_id]["outputs"]] for stage_id in STAGE_ORDER}
    stage_inputs = {
        "preflight": [],
        "text_reference": [input_snapshot["T1"]["prompt"]["path"]],
        "shape_text": [expected["text_reference"][0]],
        "shape_single": [input_snapshot["I1"]["views"]["front"]["path"]],
        "shape_multiview": [input_snapshot["I2"]["views"][view]["path"] for view in ("front", "right", "back", "left")],
        "blender": [],
        "minecraftize_primitives": [expected["blender"][0], expected["blender"][1]],
        "minecraftize_model": [expected["blender"][0], expected["blender"][1]],
        "schematic": [expected["minecraftize_model"][0]],
        "axiom": [expected["schematic"][0], expected["schematic"][1]],
    }
    stages = []
    for stage_id in STAGE_ORDER:
        definition = STAGE_DEFINITIONS[stage_id]
        stages.append(
            {
                "id": stage_id,
                "status": "PENDING",
                "required": definition["required"],
                "owner": definition["owner"],
                "input_paths": stage_inputs[stage_id],
                "input_digests": {},
                "output_paths": expected[stage_id],
                "output_digests": {},
                "parameters": {},
                "started_at": None,
                "finished_at": None,
                "metrics": {},
                "notes": [],
                "failure_class": None,
                "history": [],
            }
        )

    session: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at": now,
        "updated_at": now,
        "minecraft_version": case["minecraft_version"],
        "case_id": case["case_id"],
        "case_root": str(case_root.expanduser().resolve()),
        "run_dir": str(run_dir),
        "stage_order": list(STAGE_ORDER),
        "active_stage": None,
        "status": "PARTIAL",
        "case": copy.deepcopy(dict(case)),
        "inputs": input_snapshot,
        "artifacts": {},
        "selected_shape_stage": None,
        "known_limitations": [],
        "stages": stages,
    }
    refresh_ready(session)
    validate_session(session)
    return session


def stage_map(session: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    stages = session.get("stages")
    if not isinstance(stages, list):
        raise ContractError("session.stages must be an array")
    result: dict[str, dict[str, Any]] = {}
    for stage in stages:
        if not isinstance(stage, dict):
            raise ContractError("each session stage must be an object")
        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or stage_id in result:
            raise ContractError(f"invalid or duplicate stage id: {stage_id!r}")
        result[stage_id] = stage
    return result


def compute_session_status(session: Mapping[str, Any]) -> str:
    stages = stage_map(session)
    if any(stage["status"] == "FAIL" for stage in stages.values()):
        return "FAIL"
    if any(stage["status"] == "BLOCKED" for stage in stages.values()):
        return "BLOCKED"
    required = [stage_id for stage_id in STAGE_ORDER if STAGE_DEFINITIONS[stage_id]["required"]]
    if all(stages[stage_id]["status"] == "PASS" for stage_id in required):
        return "PASS"
    return "PARTIAL"


def refresh_ready(session: dict[str, Any]) -> None:
    stages = stage_map(session)
    selected_shape = session.get("selected_shape_stage")
    for stage_id in STAGE_ORDER:
        stage = stages[stage_id]
        if stage["status"] != "PENDING":
            continue
        definition = STAGE_DEFINITIONS[stage_id]
        dependencies = definition["dependencies"]
        dependencies_pass = all(stages[dep]["status"] in {"PASS", "SKIPPED"} for dep in dependencies)
        if stage_id == "blender":
            dependencies_pass = dependencies_pass and selected_shape in {
                "shape_text",
                "shape_single",
                "shape_multiview",
            }
        if dependencies_pass:
            stage["status"] = "READY"

    active = None
    for stage_id in STAGE_ORDER:
        if stages[stage_id]["status"] in {"RUNNING", "APPROVAL_REQUIRED"}:
            active = stage_id
            break
    if active is None:
        for stage_id in STAGE_ORDER:
            if stages[stage_id]["status"] == "READY":
                active = stage_id
                break
    session["active_stage"] = active
    session["status"] = compute_session_status(session)
    session["updated_at"] = utc_now()


def validate_session(payload: Mapping[str, Any]) -> dict[str, Any]:
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ContractError(f"session.schema_version must be {SCHEMA_VERSION}")
    validate_run_id(_require_nonempty_string(payload, "run_id", "session"))
    if payload.get("minecraft_version") != MINECRAFT_VERSION:
        raise ContractError(f"session.minecraft_version must be {MINECRAFT_VERSION}")
    if tuple(payload.get("stage_order", ())) != STAGE_ORDER:
        raise ContractError("session.stage_order does not match canonical stage order")
    stages = stage_map(payload)
    if tuple(stages) != STAGE_ORDER:
        raise ContractError("session.stages must contain canonical stages in canonical order")
    for stage_id, stage in stages.items():
        status = stage.get("status")
        if status not in ALLOWED_STAGE_STATUSES:
            raise ContractError(f"invalid stage status for {stage_id}: {status}")
        if stage.get("owner") != STAGE_DEFINITIONS[stage_id]["owner"]:
            raise ContractError(f"stage owner drift for {stage_id}")
    active = payload.get("active_stage")
    if active is not None and active not in STAGE_ORDER:
        raise ContractError(f"unknown active_stage: {active}")
    selected = payload.get("selected_shape_stage")
    if selected is not None and selected not in {"shape_text", "shape_single", "shape_multiview"}:
        raise ContractError(f"invalid selected_shape_stage: {selected}")
    return copy.deepcopy(dict(payload))


def resolve_case_input(session: Mapping[str, Any], raw: str) -> Path:
    root = Path(_require_nonempty_string(session, "case_root", "session"))
    return _resolve_input(root, raw)


def record_inputs(stage: dict[str, Any]) -> None:
    digests: dict[str, str] = {}
    missing = []
    for raw in stage.get("input_paths", []):
        path = Path(raw)
        if not path.is_file():
            missing.append(str(path))
        else:
            digests[str(path)] = sha256_file(path)
    if missing:
        raise ContractError(f"required stage inputs are missing: {missing}")
    stage["input_digests"] = digests


def record_artifacts(stage: dict[str, Any]) -> None:
    digests: dict[str, str] = {}
    missing = []
    empty = []
    for raw in stage.get("output_paths", []):
        path = Path(raw)
        if not path.is_file():
            missing.append(str(path))
        elif path.stat().st_size == 0:
            empty.append(str(path))
        else:
            digests[str(path)] = sha256_file(path)
    if missing:
        raise ContractError(f"expected stage outputs are missing: {missing}")
    if empty:
        raise ContractError(f"expected stage outputs are empty: {empty}")
    stage["output_digests"] = digests
