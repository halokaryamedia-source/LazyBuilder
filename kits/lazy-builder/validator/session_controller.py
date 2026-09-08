#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from session_contract import (
    ContractError,
    STAGE_DEFINITIONS,
    STAGE_ORDER,
    create_session,
    load_case,
    read_json,
    record_artifacts,
    record_inputs,
    refresh_ready,
    resolve_case_input,
    stage_map,
    utc_now,
    validate_session,
    write_json_atomic,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
SHAPE_STAGES = {"shape_text", "shape_single", "shape_multiview"}

ALLOWED_TRANSITIONS = {
    "READY": {"RUNNING", "BLOCKED", "SKIPPED"},
    "RUNNING": {"PASS", "FAIL", "BLOCKED", "APPROVAL_REQUIRED"},
    "APPROVAL_REQUIRED": {"PASS", "FAIL", "BLOCKED"},
    "FAIL": {"READY"},
    "BLOCKED": {"READY"},
}


def _session_path(args: argparse.Namespace) -> Path:
    return Path(args.session).expanduser().resolve()


def _load_session(path: Path) -> dict[str, Any]:
    return validate_session(read_json(path))


def _save_session(path: Path, session: dict[str, Any]) -> None:
    refresh_ready(session)
    validate_session(session)
    write_json_atomic(path, session)


def _stage(session: dict[str, Any], stage_id: str) -> dict[str, Any]:
    stages = stage_map(session)
    if stage_id not in stages:
        raise ContractError(f"unknown stage: {stage_id}")
    return stages[stage_id]


def _transition(
    session: dict[str, Any],
    stage_id: str,
    status: str,
    *,
    notes: str | None = None,
    failure_class: str | None = None,
) -> None:
    stage = _stage(session, stage_id)
    current = stage["status"]
    if status not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ContractError(f"invalid stage transition {stage_id}: {current} -> {status}")
    if status == "RUNNING":
        record_inputs(stage)
        stage["started_at"] = utc_now()
        stage["finished_at"] = None
        stage["failure_class"] = None
    elif status in {"PASS", "FAIL", "BLOCKED", "SKIPPED"}:
        stage["finished_at"] = utc_now()
    if status == "PASS":
        record_artifacts(stage)
    if failure_class:
        stage["failure_class"] = failure_class
    if notes:
        stage.setdefault("notes", []).append(notes)
    stage["status"] = status


def _snapshot_stage(stage: dict[str, Any]) -> dict[str, Any]:
    snapshot = copy.deepcopy(stage)
    snapshot.pop("history", None)
    snapshot["archived_at"] = utc_now()
    return snapshot


def _dependent_stages(stage_id: str) -> set[str]:
    affected = {stage_id}
    changed = True
    while changed:
        changed = False
        for candidate in STAGE_ORDER:
            if candidate in affected:
                continue
            dependencies = set(STAGE_DEFINITIONS[candidate]["dependencies"])
            if dependencies & affected:
                affected.add(candidate)
                changed = True
    return affected


def invalidate_from(session: dict[str, Any], stage_id: str, reason: str) -> None:
    if stage_id not in STAGE_ORDER:
        raise ContractError(f"unknown stage: {stage_id}")
    stages = stage_map(session)
    affected = _dependent_stages(stage_id)
    for current_id in STAGE_ORDER:
        if current_id not in affected:
            continue
        stage = stages[current_id]
        if stage["status"] != "PENDING" or stage.get("output_digests") or stage.get("notes"):
            stage.setdefault("history", []).append(_snapshot_stage(stage))
        stage["status"] = "PENDING"
        stage["input_digests"] = {}
        stage["output_digests"] = {}
        stage["parameters"] = {}
        stage["started_at"] = None
        stage["finished_at"] = None
        stage["metrics"] = {}
        stage["failure_class"] = None
        stage["notes"] = [f"invalidated: {reason}"] if current_id == stage_id else [f"invalidated because it depends on {stage_id}"]
    if session.get("selected_shape_stage") in affected:
        session["selected_shape_stage"] = None
        session.get("artifacts", {}).pop("selected_shape", None)
    refresh_ready(session)


def build_action(session: dict[str, Any], stage_id: str) -> dict[str, Any]:
    run_dir = Path(session["run_dir"])
    case = session["case"]
    output_dir = run_dir / STAGE_DEFINITIONS[stage_id]["folder"]
    common = {
        "stage": stage_id,
        "status": _stage(session, stage_id)["status"],
        "owner": STAGE_DEFINITIONS[stage_id]["owner"],
        "output_dir": str(output_dir),
        "expected_outputs": _stage(session, stage_id)["output_paths"],
    }
    if stage_id == "preflight":
        return {**common, "kind": "manual_record", "instruction": "Record exact runtime environment into environment.json without changing packages or server policy."}
    if stage_id == "text_reference":
        prompt = resolve_case_input(session, case["inputs"]["T1"]["prompt_path"])
        return {**common, "kind": "command", "argv": ["python", str(REPO_ROOT / "kits/lazy-builder/generation/generate_text_reference.py"), "--prompt-file", str(prompt), "--output-dir", str(output_dir)], "completion": "mark APPROVAL_REQUIRED after generation; approve only after visual review"}
    if stage_id == "shape_text":
        return {**common, "kind": "command", "argv": ["python", str(REPO_ROOT / "kits/lazy-builder/generation/generate_shape.py"), "--front", str(run_dir / "10-reference/reference_front.png"), "--output-dir", str(output_dir)]}
    if stage_id == "shape_single":
        front = resolve_case_input(session, case["inputs"]["I1"]["views"]["front"])
        return {**common, "kind": "command", "argv": ["python", str(REPO_ROOT / "kits/lazy-builder/generation/generate_shape.py"), "--front", str(front), "--output-dir", str(output_dir)]}
    if stage_id == "shape_multiview":
        argv = ["python", str(REPO_ROOT / "kits/lazy-builder/generation/generate_shape.py")]
        for view in ("front", "right", "back", "left"):
            path = resolve_case_input(session, case["inputs"]["I2"]["views"][view])
            argv.extend([f"--{view}", str(path)])
        argv.extend(["--output-dir", str(output_dir)])
        return {**common, "kind": "command", "argv": argv}
    if stage_id == "blender":
        selected = session.get("selected_shape_stage")
        if selected not in SHAPE_STAGES:
            return {**common, "kind": "blocked", "blocker": "SELECT_REPRESENTATIVE_SHAPE_FIRST"}
        source = Path(_stage(session, selected)["output_paths"][0])
        return {**common, "kind": "manual_application", "source_glb": str(source), "target_width_blocks": case["target"]["target_width_blocks"], "target_object_name": "LazyBuilderTarget", "instruction": "Open the selected GLB in Blender 5.2.x LTS, normalize per TARGET-MODEL.md, preserve raw source separately, name the prepared mesh LazyBuilderTarget, then save target.blend and target.json."}
    if stage_id == "minecraftize_primitives":
        return {**common, "kind": "command", "argv": ["blender", "--background", "--python", str(REPO_ROOT / "kits/lazy-builder/minecraftize/run_primitive_suite.py"), "--", "--output-dir", str(output_dir)], "completion": "V0 full-block primitive must PASS; stair/slab remain SKIPPED until implemented"}
    if stage_id == "minecraftize_model":
        return {**common, "kind": "command", "argv": ["blender", str(run_dir / "30-blender/target.blend"), "--background", "--python", str(REPO_ROOT / "kits/lazy-builder/minecraftize/minecraftize_v0.py"), "--", "--object-name", "LazyBuilderTarget", "--target-width-blocks", str(case["target"]["target_width_blocks"]), "--output-dir", str(output_dir)]}
    if stage_id == "schematic":
        blocks_path = run_dir / "41-minecraftize-model/blocks.json"
        return {**common, "kind": "command", "argv": ["python", str(REPO_ROOT / "kits/lazy-builder/schematic/export_blocks.py"), "--blocks", str(blocks_path), "--output-dir", str(output_dir)]}
    if stage_id == "axiom":
        return {**common, "kind": "manual_application", "schematic": str(run_dir / "50-schematic/build.schem"), "instruction": "Use VALIDATION.md: import exact build.schem in Axiom, verify Clipboard, place through AxiomPaper/Paper, and record runtime.json."}
    raise ContractError(f"no action definition for stage: {stage_id}")


def cmd_init(args: argparse.Namespace) -> int:
    case_path = Path(args.case).expanduser().resolve()
    case, case_root = load_case(case_path, require_files=not args.allow_missing_inputs)
    runs_dir = Path(args.runs_dir).expanduser().resolve()
    run_dir = runs_dir / args.run_id
    session_path = run_dir / "session.json"
    if session_path.exists():
        raise ContractError(f"session already exists: {session_path}")
    for stage_id in STAGE_ORDER:
        (run_dir / STAGE_DEFINITIONS[stage_id]["folder"]).mkdir(parents=True, exist_ok=True)
    session = create_session(case=case, case_root=case_root, run_id=args.run_id, run_dir=run_dir)
    _save_session(session_path, session)
    print(session_path)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    session = _load_session(_session_path(args))
    summary = {"run_id": session["run_id"], "status": session["status"], "active_stage": session["active_stage"], "selected_shape_stage": session.get("selected_shape_stage"), "stages": [{"id": s["id"], "status": s["status"]} for s in session["stages"]]}
    print(json.dumps(summary, indent=2))
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    session = _load_session(_session_path(args))
    refresh_ready(session)
    active = session.get("active_stage")
    if active is None:
        print(json.dumps({"status": "NO_READY_STAGE"}, indent=2))
        return 0
    print(json.dumps(build_action(session, active), indent=2, sort_keys=True))
    return 0


def cmd_mark(args: argparse.Namespace) -> int:
    path = _session_path(args)
    session = _load_session(path)
    _transition(session, args.stage, args.status, notes=args.notes, failure_class=args.failure_class)
    _save_session(path, session)
    return 0


def cmd_select(args: argparse.Namespace) -> int:
    path = _session_path(args)
    session = _load_session(path)
    if args.stage not in SHAPE_STAGES:
        raise ContractError(f"selected shape must be one of {sorted(SHAPE_STAGES)}")
    stage = _stage(session, args.stage)
    if stage["status"] != "PASS":
        raise ContractError(f"cannot select {args.stage}; status is {stage['status']}")
    session["selected_shape_stage"] = args.stage
    session.setdefault("artifacts", {})["selected_shape"] = stage["output_paths"][0]
    blender = _stage(session, "blender")
    blender["input_paths"] = [stage["output_paths"][0], stage["output_paths"][1]]
    _save_session(path, session)
    return 0


def cmd_invalidate(args: argparse.Namespace) -> int:
    path = _session_path(args)
    session = _load_session(path)
    invalidate_from(session, args.stage, args.reason)
    _save_session(path, session)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage one LazyBuilder end-to-end acceptance session.")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="Create run directories and session.json from a case manifest.")
    init.add_argument("--case", required=True)
    init.add_argument("--run-id", required=True)
    init.add_argument("--runs-dir", required=True)
    init.add_argument("--allow-missing-inputs", action="store_true")
    init.set_defaults(func=cmd_init)
    for name, func in (("status", cmd_status), ("next", cmd_next)):
        item = sub.add_parser(name)
        item.add_argument("--session", required=True)
        item.set_defaults(func=func)
    mark = sub.add_parser("mark")
    mark.add_argument("--session", required=True)
    mark.add_argument("--stage", required=True, choices=STAGE_ORDER)
    mark.add_argument("--status", required=True, choices=("RUNNING", "APPROVAL_REQUIRED", "PASS", "FAIL", "BLOCKED", "SKIPPED", "READY"))
    mark.add_argument("--notes")
    mark.add_argument("--failure-class")
    mark.set_defaults(func=cmd_mark)
    select = sub.add_parser("select-shape")
    select.add_argument("--session", required=True)
    select.add_argument("--stage", required=True, choices=sorted(SHAPE_STAGES))
    select.set_defaults(func=cmd_select)
    invalidate = sub.add_parser("invalidate")
    invalidate.add_argument("--session", required=True)
    invalidate.add_argument("--stage", required=True, choices=STAGE_ORDER)
    invalidate.add_argument("--reason", required=True)
    invalidate.set_defaults(func=cmd_invalidate)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        return args.func(args)
    except ContractError as exc:
        raise SystemExit(f"error: {exc}") from exc

if __name__ == "__main__":
    raise SystemExit(main())
