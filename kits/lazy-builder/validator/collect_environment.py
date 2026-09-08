#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATION_DIR = HERE.parent / "generation"
if str(GENERATION_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATION_DIR))

from runtime_contract import (
    HUNYUAN3D_MODEL_REVISION,
    HUNYUAN3D_SOURCE_COMMIT,
    HUNYUANDIT_MODEL_REVISION,
)

AUTO_DECLARED = {
    "hunyuan3d_source_commit": HUNYUAN3D_SOURCE_COMMIT,
    "hunyuan3d_model_revision": HUNYUAN3D_MODEL_REVISION,
    "hunyuandit_model_revision": HUNYUANDIT_MODEL_REVISION,
}

PACKAGE_NAMES = (
    "torch",
    "diffusers",
    "transformers",
    "accelerate",
    "huggingface_hub",
    "Pillow",
    "mcschematic",
)


def package_versions() -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    for name in PACKAGE_NAMES:
        try:
            result[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            result[name] = None
    return result


def parse_records(values: list[str]) -> dict[str, str]:
    records: dict[str, str] = {}
    for raw in values:
        if "=" not in raw:
            raise ValueError(f"--record must use key=value: {raw}")
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError(f"--record must contain non-empty key/value: {raw}")
        records[key] = value
    return records


def build_payload(records: dict[str, str]) -> dict:
    return {
        "schema_version": 1,
        "stage": "preflight",
        "status": "PREFLIGHT_CAPTURED_RUNTIME_NOT_STARTED",
        "system": {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "python": {
            "version": platform.python_version(),
            "executable": sys.executable,
        },
        "packages": package_versions(),
        "executables": {
            "blender": shutil.which("blender"),
            "java": shutil.which("java"),
        },
        "declared": dict(sorted({**AUTO_DECLARED, **records}.items())),
        "runtime_launched": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture LazyBuilder preflight environment metadata without launching Hunyuan/Blender/Axiom/Minecraft runtime."
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--record", action="append", default=[], help="Exact environment fact as key=value; repeat as needed.")
    args = parser.parse_args()
    try:
        records = parse_records(args.record)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    payload = build_payload(records)
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
