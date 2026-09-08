#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CHECK_NAMES = ("import", "clipboard", "placement", "minecraft_world", "visual_state")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_payload(*, schematic: Path, environment: Path, checks: dict[str, str], notes: list[str]) -> dict:
    for path in (schematic, environment):
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"required runtime evidence input missing/empty: {path}")
    if set(checks) != set(CHECK_NAMES):
        raise ValueError(f"runtime checks must be exactly {CHECK_NAMES}")
    if any(value not in {"PASS", "FAIL"} for value in checks.values()):
        raise ValueError("runtime checks must be PASS or FAIL")
    overall = "PASS" if all(checks[name] == "PASS" for name in CHECK_NAMES) else "FAIL"
    return {
        "schema_version": 1,
        "stage": "axiom",
        "status": overall,
        "recorded_at": utc_now(),
        "schematic": {"path": str(schematic.resolve()), "sha256": sha256_file(schematic)},
        "environment": {"path": str(environment.resolve()), "sha256": sha256_file(environment)},
        "checks": {name: checks[name] for name in CHECK_NAMES},
        "notes": list(notes),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Record exact Axiom/Paper/Minecraft runtime evidence with artifact lineage.")
    parser.add_argument("--schematic", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--output", required=True)
    for name in CHECK_NAMES:
        parser.add_argument(f"--{name.replace('_', '-')}", required=True, choices=("PASS", "FAIL"))
    parser.add_argument("--note", action="append", default=[])
    args = parser.parse_args()
    checks = {name: getattr(args, name) for name in CHECK_NAMES}
    try:
        payload = build_payload(
            schematic=Path(args.schematic).expanduser().resolve(),
            environment=Path(args.environment).expanduser().resolve(),
            checks=checks,
            notes=args.note,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
