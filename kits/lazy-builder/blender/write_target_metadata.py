#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_bounds(minimum: list[float], maximum: list[float]) -> None:
    if len(minimum) != 3 or len(maximum) != 3:
        raise SystemExit("bounds must contain exactly three axes")
    if not all(math.isfinite(value) for value in (*minimum, *maximum)):
        raise SystemExit("bounds must contain only finite numbers")
    extents = [maximum[i] - minimum[i] for i in range(3)]
    if any(extent <= 0 for extent in extents):
        raise SystemExit(f"bounds must have positive extent on every axis, got {extents}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Write canonical LazyBuilder target.json after manual Blender preparation.")
    parser.add_argument("--source-glb", required=True)
    parser.add_argument("--source-stage", required=True, choices=("shape_text", "shape_single", "shape_multiview"))
    parser.add_argument("--target-blend", required=True)
    parser.add_argument("--blender-version", required=True)
    parser.add_argument("--target-width-blocks", required=True, type=int)
    parser.add_argument("--bounds-min", nargs=3, required=True, type=float, metavar=("X", "Y", "Z"))
    parser.add_argument("--bounds-max", nargs=3, required=True, type=float, metavar=("X", "Y", "Z"))
    parser.add_argument("--cleanup-note", action="append", default=[])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.target_width_blocks <= 0:
        raise SystemExit("target width must be positive")
    _validate_bounds(args.bounds_min, args.bounds_max)
    source = Path(args.source_glb).expanduser().resolve()
    target = Path(args.target_blend).expanduser().resolve()
    for path in (source, target):
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"required file missing/empty: {path}")
    payload = {
        "schema_version": 1,
        "stage": "blender",
        "status": "PREPARED_TARGET_RUNTIME_CONVERSION_PENDING",
        "source": {
            "path": str(source),
            "sha256": sha256_file(source),
            "selected_shape_stage": args.source_stage,
        },
        "blender": {
            "version": args.blender_version,
            "target_object_name": "LazyBuilderTarget",
        },
        "target": {
            "target_width_blocks": args.target_width_blocks,
            "bounds_world": {"min": args.bounds_min, "max": args.bounds_max},
        },
        "orientation": {
            "minecraft_x": "blender_x",
            "minecraft_y": "blender_z",
            "minecraft_z": "-blender_y",
        },
        "cleanup": {"notes": args.cleanup_note},
        "target_blend_sha256": sha256_file(target),
    }
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
