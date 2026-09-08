#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from block_model import build_payload, canonical_block_state, write_blocks_json


def load_cases(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or payload.get("minecraft_version") != "1.21.4":
        raise ValueError("primitive fixture contract version mismatch")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("primitive fixture must contain cases")
    seen = set()
    normalized = []
    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise ValueError(f"invalid/duplicate primitive case id: {case_id!r}")
        seen.add(case_id)
        normalized.append({**case, "expected_state": canonical_block_state(case["expected_state"])})
    return normalized


def build_fixture(cases: list[dict]) -> tuple[dict, dict]:
    blocks = []
    results = []
    for index, case in enumerate(cases):
        blocks.append(
            {
                "x": index,
                "y": 0,
                "z": 0,
                "block_state": case["expected_state"],
                "source_reason": f"fixture:{case['id']}",
            }
        )
        results.append(
            {
                "id": case["id"],
                "family": case["family"],
                "engine_milestone": case["engine_milestone"],
                "expected_state": case["expected_state"],
                "status": "EXPECTED_FIXTURE_ONLY",
            }
        )
    payload = build_payload(
        blocks,
        source={"kind": "primitive_contract_fixture"},
        metadata={"warning": "This fixture validates the block-model contract; it is not Minecraftize classifier runtime proof."},
    )
    report = {
        "schema_version": 1,
        "status": "STATIC_FIXTURE_READY",
        "case_count": len(cases),
        "cases": results,
        "engine_runtime_proven": False,
    }
    return payload, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Minecraftize primitive contract fixtures.")
    parser.add_argument(
        "--cases",
        default=str(Path(__file__).with_name("fixtures") / "primitive_cases.json"),
    )
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    cases = load_cases(Path(args.cases).expanduser().resolve())
    blocks, report = build_fixture(cases)
    write_blocks_json(output_dir / "blocks.json", blocks)
    (output_dir / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output_dir / "blocks.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
