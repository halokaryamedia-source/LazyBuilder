#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare a LazyBuilder acceptance-case workspace without running any runtime stage.")
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--target-width-blocks", type=int, default=64)
    parser.add_argument("--prompt")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.target_width_blocks <= 0:
        raise SystemExit("target width must be positive")
    root = args.workspace.expanduser().resolve()
    case_path = root / "case.json"
    if case_path.exists():
        raise SystemExit(f"refusing to overwrite existing case: {case_path}")

    for folder in ("inputs/text", "inputs/single", "inputs/multiview", "runs"):
        (root / folder).mkdir(parents=True, exist_ok=True)
    prompt_path = root / "inputs/text/prompt.txt"
    prompt_path.write_text((args.prompt or "REPLACE WITH THE APPROVED TEST PROMPT") + "\n", encoding="utf-8")

    payload = {
        "schema_version": 1,
        "case_id": args.case_id,
        "minecraft_version": "1.21.4",
        "inputs": {
            "T1": {"kind": "text", "prompt_path": "inputs/text/prompt.txt"},
            "I1": {"kind": "single", "views": {"front": "inputs/single/front.png"}},
            "I2": {"kind": "multiview", "views": {
                "front": "inputs/multiview/front.png",
                "right": "inputs/multiview/right.png",
                "back": "inputs/multiview/back.png",
                "left": "inputs/multiview/left.png",
            }},
        },
        "target": {"target_width_blocks": args.target_width_blocks},
        "notes": ["Runtime remains deferred until all referenced images are populated and reviewed."],
    }
    case_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "case": str(case_path),
        "status": "CASE_SCAFFOLD_CREATED_RUNTIME_NOT_STARTED",
        "required_user_files": [
            "inputs/single/front.png",
            "inputs/multiview/front.png",
            "inputs/multiview/right.png",
            "inputs/multiview/back.png",
            "inputs/multiview/left.png",
        ],
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
