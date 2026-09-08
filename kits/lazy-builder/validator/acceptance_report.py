#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from session_contract import STAGE_DEFINITIONS, STAGE_ORDER, read_json, stage_map, utc_now, validate_session, write_json_atomic


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

    follow_up_owner = STAGE_DEFINITIONS[first_failed]["owner"] if first_failed else None
    runtime_metrics = {
        stage_id: stages[stage_id].get("metrics", {})
        for stage_id in STAGE_ORDER
        if stages[stage_id].get("metrics")
    }

    return {
        "schema_version": 1,
        "generated_at": utc_now(),
        "run_id": session["run_id"],
        "overall_status": overall,
        "first_failed_stage": first_failed,
        "passed_stages": passed,
        "failed_stages": failed,
        "blocked_stages": blocked,
        "skipped_required_stages": skipped_required,
        "selected_representative_artifact": session.get("artifacts", {}).get("selected_shape"),
        "runtime_metrics": runtime_metrics,
        "known_limitations": session.get("known_limitations", []),
        "follow_up_owner": follow_up_owner,
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
