#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from session_contract import (
    STAGE_DEFINITIONS,
    STAGE_ORDER,
    read_json,
    stage_map,
    utc_now,
    validate_session,
    write_json_atomic,
)


def build_report(session: dict[str, Any]) -> dict[str, Any]:
    validate_session(session)
    stages = stage_map(session)
    passed = [stage_id for stage_id in STAGE_ORDER if stages[stage_id]["status"] == "PASS"]
    failed = [stage_id for stage_id in STAGE_ORDER if stages[stage_id]["status"] == "FAIL"]
    blocked = [stage_id for stage_id in STAGE_ORDER if stages[stage_id]["status"] == "BLOCKED"]
    skipped_required = [
        stage_id
        for stage_id in STAGE_ORDER
        if stages[stage_id]["status"] == "SKIPPED" and STAGE_DEFINITIONS[stage_id]["required"]
    ]

    if failed:
        overall = "FAIL"
    elif blocked:
        overall = "BLOCKED"
    elif len(passed) == len(STAGE_ORDER):
        overall = "PASS"
    else:
        overall = "PARTIAL"

    first_failed = None
    for stage_id in STAGE_ORDER:
        if stages[stage_id]["status"] in {"FAIL", "BLOCKED"}:
            first_failed = stage_id
            break

    stage_evidence = {}
    artifact_lineage = {}
    runtime_metrics = {}
    for stage_id in STAGE_ORDER:
        stage = stages[stage_id]
        stage_evidence[stage_id] = {
            "status": stage["status"],
            "owner": stage["owner"],
            "input_digests": dict(stage.get("input_digests", {})),
            "output_digests": dict(stage.get("output_digests", {})),
            "started_at": stage.get("started_at"),
            "finished_at": stage.get("finished_at"),
            "failure_class": stage.get("failure_class"),
            "notes": list(stage.get("notes", [])),
        }
        if stage.get("output_digests"):
            artifact_lineage[stage_id] = dict(stage["output_digests"])
        if stage.get("metrics"):
            runtime_metrics[stage_id] = stage["metrics"]

    return {
        "schema_version": 1,
        "generated_at": utc_now(),
        "run_id": session["run_id"],
        "case": {
            "case_id": session["case_id"],
            "minecraft_version": session["minecraft_version"],
            "target": session["case"].get("target", {}),
        },
        "overall_status": overall,
        "first_failed_stage": first_failed,
        "follow_up_owner": STAGE_DEFINITIONS[first_failed]["owner"] if first_failed else None,
        "passed_stages": passed,
        "failed_stages": failed,
        "blocked_stages": blocked,
        "skipped_required_stages": skipped_required,
        "input_snapshot": session.get("inputs", {}),
        "selected_representative_stage": session.get("selected_shape_stage"),
        "selected_representative_artifact": session.get("artifacts", {}).get("selected_shape"),
        "artifact_lineage": artifact_lineage,
        "stage_evidence": stage_evidence,
        "runtime_metrics": runtime_metrics,
        "known_limitations": session.get("known_limitations", []),
        "evidence_boundary": "PASS requires the exact declared runtime stages to have executed; pre-runtime/static checks never upgrade Hunyuan/Blender/Axiom/Minecraft runtime evidence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate one consolidated LazyBuilder acceptance report.")
    parser.add_argument("--session", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    session_path = Path(args.session).expanduser().resolve()
    session = validate_session(read_json(session_path))
    output = Path(args.output).expanduser().resolve() if args.output else session_path.parent / "acceptance-report.json"
    report = build_report(session)
    write_json_atomic(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
