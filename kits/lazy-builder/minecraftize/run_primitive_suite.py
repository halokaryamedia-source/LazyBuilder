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


def _make_box(bpy, *, dimensions):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.0))
    obj = bpy.context.active_object
    obj.name = DEFAULT_OBJECT_NAME
    obj.dimensions = dimensions
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def _run_box_case(bpy, *, dimensions, target_width_blocks: int, expected_size: dict[str, int], expected_blocks: int):
    _reset_scene(bpy)
    obj = _make_box(bpy, dimensions=dimensions)
    temp = tempfile.TemporaryDirectory(prefix="lazybuilder-primitive-")
    temp_path = Path(temp.name)
    payload, engine_report = convert_object(obj, target_width_blocks=target_width_blocks, output_dir=temp_path)
    if payload["bounds"]["size"] != expected_size:
        temp.cleanup()
        raise MinecraftizeError(f"full-block primitive bounds mismatch: {payload['bounds']['size']} != {expected_size}")
    if payload["block_count"] != expected_blocks:
        temp.cleanup()
        raise MinecraftizeError(f"full-block primitive expected {expected_blocks} blocks, got {payload['block_count']}")
    return temp, payload, engine_report


def main(argv: Sequence[str] | None = None) -> int:
    bpy = _blender_runtime()
    args = parse_args(_argv_after_double_dash(sys.argv) if argv is None else argv)
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    thin_temp, _thin_payload, thin_report = _run_box_case(
        bpy,
        dimensions=(3.0, 2.0, 2.0),
        target_width_blocks=3,
        expected_size={"x": 3, "y": 2, "z": 2},
        expected_blocks=12,
    )
    thin_temp.cleanup()

    solid_temp, solid_payload, solid_report = _run_box_case(
        bpy,
        dimensions=(5.0, 5.0, 5.0),
        target_width_blocks=5,
        expected_size={"x": 5, "y": 5, "z": 5},
        expected_blocks=125,
    )
    if solid_report["inside_vote_cells"] <= 0:
        solid_temp.cleanup()
        raise MinecraftizeError("5x5x5 primitive did not exercise BVH inside/parity evidence")
    if solid_report["near_surface_cells"] >= solid_payload["block_count"]:
        solid_temp.cleanup()
        raise MinecraftizeError("5x5x5 primitive is not a true-interior proof; every cell was near-surface")
    shutil.copy2(Path(solid_temp.name) / "blocks.json", output_dir / "blocks.json")
    solid_temp.cleanup()

    suite_report = {
        "schema_version": 1,
        "status": "PASS",
        "engine": solid_report["engine"],
        "cases": {
            "v0_full_block_box_3x2x2_boundary": {
                "status": "PASS",
                "expected_blocks": 12,
                "expected_bounds": {"x": 3, "y": 2, "z": 2},
                "inside_vote_cells": thin_report["inside_vote_cells"],
                "near_surface_cells": thin_report["near_surface_cells"],
            },
            "v0_full_block_box_5x5x5_interior": {
                "status": "PASS",
                "expected_blocks": 125,
                "expected_bounds": {"x": 5, "y": 5, "z": 5},
                "inside_vote_cells": solid_report["inside_vote_cells"],
                "near_surface_cells": solid_report["near_surface_cells"],
                "requires_non_surface_occupancy": True,
            },
            "stairs": {"status": "SKIPPED", "reason": "not implemented in V0"},
            "slabs": {"status": "SKIPPED", "reason": "not implemented in V0"},
        },
        "scope": "actual Blender engine path; boundary plus true-interior occupancy proof; no hand-authored blocks.json fixture",
    }
    (output_dir / "report.json").write_text(json.dumps(suite_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(suite_report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
