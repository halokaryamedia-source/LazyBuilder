#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.metadata
import inspect
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
    inspect_hunyuan_source_checkout,
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
    "hy3dgen",
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


def hunyuan_source_checkout() -> dict[str, object]:
    try:
        import hy3dgen

        if not getattr(hy3dgen, "__file__", None):
            raise RuntimeError("hy3dgen.__file__ is unavailable")
        identity = inspect_hunyuan_source_checkout(Path(hy3dgen.__file__))
        identity["error"] = None
        return identity
    except Exception as exc:
        return {
            "path": None,
            "commit": None,
            "dirty": None,
            "status_porcelain": None,
            "error": str(exc),
        }


def runtime_api_contract() -> dict[str, object]:
    try:
        from diffusers import HunyuanDiTPipeline
        from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

        text_call = set(inspect.signature(HunyuanDiTPipeline.__call__).parameters)
        required_text = {
            "prompt", "height", "width", "num_inference_steps", "guidance_scale",
            "negative_prompt", "generator",
        }
        shape_load = set(inspect.signature(Hunyuan3DDiTFlowMatchingPipeline.from_pretrained).parameters)
        required_shape_load = {"model_path", "device", "use_safetensors", "variant", "subfolder"}
        shape_call = set(inspect.signature(Hunyuan3DDiTFlowMatchingPipeline.__call__).parameters)
        required_shape_call = {
            "image", "num_inference_steps", "guidance_scale", "generator", "box_v",
            "octree_resolution", "mc_level", "mc_algo", "num_chunks", "output_type",
        }
        missing = {
            "text_call": sorted(required_text - text_call),
            "shape_from_pretrained": sorted(required_shape_load - shape_load),
            "shape_call": sorted(required_shape_call - shape_call),
        }
        if not callable(getattr(HunyuanDiTPipeline, "enable_model_cpu_offload", None)):
            missing["text_offload"] = ["enable_model_cpu_offload"]
        if not callable(getattr(HunyuanDiTPipeline, "enable_sequential_cpu_offload", None)):
            missing["text_sequential_offload"] = ["enable_sequential_cpu_offload"]
        failures = {key: value for key, value in missing.items() if value}
        return {
            "status": "PASS" if not failures else "FAIL",
            "missing": failures,
            "error": None,
        }
    except Exception as exc:
        return {"status": "FAIL", "missing": {}, "error": str(exc)}


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
            "git": shutil.which("git"),
            "blender": shutil.which("blender"),
            "java": shutil.which("java"),
        },
        "hunyuan_source_checkout": hunyuan_source_checkout(),
        "runtime_api_contract": runtime_api_contract(),
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
    output.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
