#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from minecraftize_v0 import DEFAULT_OBJECT_NAME, MinecraftizeError, convert_object


def _blender_runtime():
    try:
        import bpy  # type: ignore
    except Exception as exc:
        raise MinecraftizeError("primitive suite must execute inside Blender Python") from exc
    return bpy


def _argv_after_double_dash(argv: Sequence[str]) -> list[str]:
    return list(argv[argv.index("--") + 1 :]) if "--" in argv else list(argv[1:])


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minecraftize V0 primitive acceptance suite")
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args(argv)


def _reset_scene(bpy):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def _make_box(bpy, *, dimensions=(3.0, 2.0, 2.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.0))
    obj = bpy.context.active_object
    obj.name = DEFAULT_OBJECT_NAME
    obj.dimensions = dimensions
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def main(argv: Sequence[str] | None = None) -> int:
    bpy = _blender_runtime()
    args = parse_args(_argv_after_double_dash(sys.argv) if argv is None else argv)
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    _reset_scene(bpy)
    obj = _make_box(bpy)
    with tempfile.TemporaryDirectory(prefix="lazybuilder-primitive-") as temp_name:
        temp = Path(temp_name)
        payload, engine_report = convert_object(obj, target_width_blocks=3, output_dir=temp)
        expected_size = {"x": 3, "y": 2, "z": 2}
        if payload["bounds"]["size"] != expected_size:
            raise MinecraftizeError(
                f"full-block primitive bounds mismatch: {payload['bounds']['size']} != {expected_size}"
            )
        if payload["block_count"] != 12:
            raise MinecraftizeError(f"full-block primitive expected 12 blocks, got {payload['block_count']}")
        shutil.copy2(temp / "blocks.json", output_dir / "blocks.json")

    suite_report = {
        "schema_version": 1,
        "status": "PASS",
        "engine": engine_report["engine"],
        "cases": {
            "v0_full_block_box_3x2x2": {
                "status": "PASS",
                "expected_blocks": 12,
                "expected_bounds": expected_size,
            },
            "stairs": {"status": "SKIPPED", "reason": "not implemented in V0"},
            "slabs": {"status": "SKIPPED", "reason": "not implemented in V0"},
        },
        "scope": "actual engine path; no hand-authored blocks.json fixture",
    }
    (output_dir / "report.json").write_text(json.dumps(suite_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(suite_report, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
