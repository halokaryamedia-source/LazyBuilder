#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from block_model import Block, build_payload, canonical_block_state, write_blocks_json

ENGINE_VERSION = "v0-full-block-bvh-1"
DEFAULT_OBJECT_NAME = "LazyBuilderTarget"
DEFAULT_BLOCK_STATE = "minecraft:stone_bricks"
DEFAULT_SURFACE_BAND = 0.72

class MinecraftizeError(RuntimeError):
    pass

@dataclass(frozen=True)
class GridSpec:
    pitch: float
    nx: int
    ny: int
    nz: int


def positive_target_width(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise MinecraftizeError("target_width_blocks must be a positive integer")
    return value


def grid_spec_from_bounds(minimum: Sequence[float], maximum: Sequence[float], target_width_blocks: int) -> GridSpec:
    positive_target_width(target_width_blocks)
    if len(minimum) != 3 or len(maximum) != 3:
        raise MinecraftizeError("bounds must contain exactly three axes")
    extents = [float(maximum[i]) - float(minimum[i]) for i in range(3)]
    if any((not math.isfinite(v)) or v <= 0 for v in extents):
        raise MinecraftizeError(f"mesh bounds must have positive finite extents, got {extents}")
    pitch = extents[0] / target_width_blocks
    if not math.isfinite(pitch) or pitch <= 0:
        raise MinecraftizeError("derived block pitch is invalid")
    return GridSpec(
        pitch=pitch,
        nx=target_width_blocks,
        ny=max(1, math.ceil(extents[1] / pitch)),
        nz=max(1, math.ceil(extents[2] / pitch)),
    )


def index_to_minecraft(ix: int, iy: int, iz: int, spec: GridSpec) -> tuple[int, int, int]:
    if not (0 <= ix < spec.nx and 0 <= iy < spec.ny and 0 <= iz < spec.nz):
        raise MinecraftizeError("voxel index outside grid")
    return ix, iz, (spec.ny - 1) - iy


def blocks_from_occupied(
    occupied: Iterable[tuple[int, int, int]],
    spec: GridSpec,
    *,
    block_state: str = DEFAULT_BLOCK_STATE,
) -> list[Block]:
    state = canonical_block_state(block_state)
    blocks: list[Block] = []
    seen: set[tuple[int, int, int]] = set()
    for index in occupied:
        if index in seen:
            raise MinecraftizeError(f"duplicate occupied voxel index: {index}")
        seen.add(index)
        x, y, z = index_to_minecraft(*index, spec)
        blocks.append(Block(x, y, z, state, "v0_occupied_cell"))
    return blocks


def _blender_runtime():
    try:
        import bpy  # type: ignore
        from mathutils import Vector  # type: ignore
        from mathutils.bvhtree import BVHTree  # type: ignore
    except Exception as exc:
        raise MinecraftizeError(
            "minecraftize_v0.py must execute inside Blender Python for mesh conversion"
        ) from exc
    return bpy, Vector, BVHTree


def _mesh_world_geometry(obj, depsgraph, Vector, BVHTree):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    try:
        matrix = evaluated.matrix_world
        vertices = [matrix @ vertex.co for vertex in mesh.vertices]
        polygons = [tuple(poly.vertices) for poly in mesh.polygons]
        if not vertices or not polygons:
            raise MinecraftizeError("prepared target contains no mesh geometry")
        bvh = BVHTree.FromPolygons(vertices, polygons, all_triangles=False)
        if bvh is None:
            raise MinecraftizeError("Blender could not build BVH for prepared target")
        minimum = [min(vertex[i] for vertex in vertices) for i in range(3)]
        maximum = [max(vertex[i] for vertex in vertices) for i in range(3)]
        return bvh, minimum, maximum
    finally:
        evaluated.to_mesh_clear()


def _ray_parity(bvh, origin, direction, max_distance: float, epsilon: float, Vector) -> bool:
    current = Vector(origin)
    travelled = 0.0
    hits = 0
    for _ in range(4096):
        location, _normal, _index, distance = bvh.ray_cast(current, direction, max_distance - travelled)
        if location is None or distance is None:
            break
        hits += 1
        step = float(distance) + epsilon
        travelled += step
        if travelled >= max_distance:
            break
        current = location + direction * epsilon
    else:
        raise MinecraftizeError("BVH parity ray exceeded safety hit limit")
    return (hits % 2) == 1


def _occupied_cell(bvh, center, pitch: float, diagonal: float, surface_band: float, Vector):
    nearest = bvh.find_nearest(center)
    surface_distance = float(nearest[3]) if nearest and nearest[0] is not None and nearest[3] is not None else math.inf
    near_surface = surface_distance <= pitch * surface_band

    directions = [
        Vector((1.0, 0.173, 0.071)).normalized(),
        Vector((0.113, 1.0, 0.193)).normalized(),
        Vector((0.151, 0.097, 1.0)).normalized(),
    ]
    epsilon = max(pitch * 1e-5, 1e-7)
    max_distance = diagonal * 3.0 + pitch
    inside_votes = sum(
        1 for direction in directions if _ray_parity(bvh, center, direction, max_distance, epsilon, Vector)
    )
    return (inside_votes >= 2) or near_surface, inside_votes, surface_distance


def convert_object(
    obj,
    *,
    target_width_blocks: int,
    output_dir: Path,
    block_state: str = DEFAULT_BLOCK_STATE,
    surface_band: float = DEFAULT_SURFACE_BAND,
):
    if not math.isfinite(surface_band) or surface_band < 0:
        raise MinecraftizeError("surface_band must be a finite non-negative number")
    bpy, Vector, BVHTree = _blender_runtime()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bvh, minimum, maximum = _mesh_world_geometry(obj, depsgraph, Vector, BVHTree)
    spec = grid_spec_from_bounds(minimum, maximum, target_width_blocks)
    diagonal = math.dist(minimum, maximum)

    occupied: list[tuple[int, int, int]] = []
    inside_cells = 0
    surface_cells = 0
    for iz in range(spec.nz):
        z = minimum[2] + (iz + 0.5) * spec.pitch
        for iy in range(spec.ny):
            y = minimum[1] + (iy + 0.5) * spec.pitch
            for ix in range(spec.nx):
                x = minimum[0] + (ix + 0.5) * spec.pitch
                is_occupied, inside_votes, distance = _occupied_cell(
                    bvh, Vector((x, y, z)), spec.pitch, diagonal, surface_band, Vector
                )
                if not is_occupied:
                    continue
                occupied.append((ix, iy, iz))
                if inside_votes >= 2:
                    inside_cells += 1
                if distance <= spec.pitch * surface_band:
                    surface_cells += 1

    if not occupied:
        raise MinecraftizeError("V0 produced zero occupied cells; target/pitch contract must be inspected")

    blocks = blocks_from_occupied(occupied, spec, block_state=block_state)
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = build_payload(
        blocks,
        source={"engine": ENGINE_VERSION, "blender_object": obj.name},
        metadata={
            "target_width_blocks": target_width_blocks,
            "pitch_blender_units_per_block": spec.pitch,
            "surface_band": surface_band,
            "grid_blender_axes": {"x": spec.nx, "y": spec.ny, "z": spec.nz},
            "supported_block_families": ["full_block"],
        },
    )
    write_blocks_json(output_dir / "blocks.json", payload)
    report = {
        "schema_version": 1,
        "engine": ENGINE_VERSION,
        "status": "PASS",
        "object_name": obj.name,
        "input_bounds_world": {"min": minimum, "max": maximum},
        "grid_blender_axes": {"x": spec.nx, "y": spec.ny, "z": spec.nz},
        "grid_minecraft_axes": payload["bounds"]["size"],
        "pitch_blender_units_per_block": spec.pitch,
        "target_width_blocks": target_width_blocks,
        "block_state": canonical_block_state(block_state),
        "occupied_cells": len(occupied),
        "inside_vote_cells": inside_cells,
        "near_surface_cells": surface_cells,
        "surface_band": surface_band,
        "features": {"full_block": "SUPPORTED", "stair": "SKIPPED", "slab": "SKIPPED"},
        "limitations": [
            "V0 uses full blocks only",
            "thin features below active block pitch may disappear",
            "non-watertight or noisy geometry may require Blender cleanup before conversion",
        ],
    }
    (output_dir / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload, report


def _resolve_target_object(bpy, object_name: str):
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        raise MinecraftizeError(f"prepared target object not found: {object_name}")
    if obj.type != "MESH":
        raise MinecraftizeError(f"prepared target object must be MESH, got {obj.type}")
    return obj


def _argv_after_double_dash(argv: Sequence[str]) -> list[str]:
    return list(argv[argv.index("--") + 1 :]) if "--" in argv else list(argv[1:])


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minecraftize V0 Blender-native full-block converter")
    parser.add_argument("--object-name", default=DEFAULT_OBJECT_NAME)
    parser.add_argument("--target-width-blocks", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--block-state", default=DEFAULT_BLOCK_STATE)
    parser.add_argument("--surface-band", type=float, default=DEFAULT_SURFACE_BAND)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    bpy, _Vector, _BVHTree = _blender_runtime()
    args = parse_args(_argv_after_double_dash(sys.argv) if argv is None else argv)
    positive_target_width(args.target_width_blocks)
    obj = _resolve_target_object(bpy, args.object_name)
    payload, report = convert_object(
        obj,
        target_width_blocks=args.target_width_blocks,
        output_dir=args.output_dir.expanduser().resolve(),
        block_state=args.block_state,
        surface_band=args.surface_band,
    )
    print(json.dumps({"blocks": payload["block_count"], "report": report["status"]}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
