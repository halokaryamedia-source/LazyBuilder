#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from session_contract import (
    ContractError,
    read_json,
    sha256_file,
    validate_session,
    write_json_atomic,
)
from session_controller import invalidate_from

OWNER_STAGE = {"T1": "text_reference", "I1": "shape_single", "I2": "shape_multiview"}


def _resolve(root: Path, raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def _entry(path: Path) -> dict[str, str]:
    if not path.is_file() or path.stat().st_size == 0:
        raise ContractError(f"refreshed input missing/empty: {path}")
    return {"path": str(path), "sha256": sha256_file(path)}


def refresh_input_snapshot(session: dict, input_id: str, reason: str) -> dict:
    if input_id not in OWNER_STAGE:
        raise ContractError(f"input must be one of {sorted(OWNER_STAGE)}")
    root = Path(session["case_root"]).expanduser().resolve()
    case = session["case"]
    if input_id == "T1":
        prompt = _resolve(root, case["inputs"]["T1"]["prompt_path"])
        entry = _entry(prompt)
        if not prompt.read_text(encoding="utf-8").strip():
            raise ContractError("T1 prompt must not be empty")
        session["inputs"]["T1"] = {"kind": "text", "prompt": entry}
    elif input_id == "I1":
        front = _resolve(root, case["inputs"]["I1"]["views"]["front"])
        session["inputs"]["I1"] = {"kind": "single", "views": {"front": _entry(front)}}
    else:
        session["inputs"]["I2"] = {
            "kind": "multiview",
            "views": {
                view: _entry(_resolve(root, case["inputs"]["I2"]["views"][view]))
                for view in ("front", "right", "back", "left")
            },
        }
    invalidate_from(session, OWNER_STAGE[input_id], f"case input {input_id} refreshed: {reason}")
    return session


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Explicitly accept a changed T1/I1/I2 case input, refresh its SHA-256 snapshot, and invalidate only true dependents."
    )
    parser.add_argument("--session", required=True)
    parser.add_argument("--input", required=True, choices=sorted(OWNER_STAGE))
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    path = Path(args.session).expanduser().resolve()
    session = validate_session(read_json(path))
    refresh_input_snapshot(session, args.input, args.reason)
    validate_session(session)
    write_json_atomic(path, session)
    print(json.dumps({"session": str(path), "refreshed_input": args.input, "invalidated_from": OWNER_STAGE[args.input]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
