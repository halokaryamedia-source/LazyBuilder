#!/usr/bin/env python3
"""Generate and self-check the LazyBuilder M1 schematic handoff fixture.

This proves the mcschematic writer can serialize and reload a small structure with
Minecraft BlockStates. It does not prove Axiom import or Minecraft placement.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mcschematic

DEFAULT_VERSION = "JE_1_21_4"
DEFAULT_NAME = "lazybuilder_m1_smoke"

SMOKE_BLOCKS: dict[tuple[int, int, int], str] = {
    (0, 0, 0): "minecraft:stone_bricks",
    (1, 0, 0): "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    (2, 0, 0): "minecraft:stone_slab[type=top,waterlogged=false]",
}


def resolve_version(name: str):
    try:
        return getattr(mcschematic.Version, name)
    except AttributeError as exc:
        available = sorted(member for member in dir(mcschematic.Version) if member.startswith("JE_"))
        tail = ", ".join(available[-8:])
        raise SystemExit(f"Unsupported mcschematic version enum {name!r}. Recent values: {tail}") from exc


def build_fixture(output_dir: Path, name: str, version_name: str) -> tuple[Path, Path]:
    version = resolve_version(version_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    schematic = mcschematic.MCSchematic()
    for position, block_state in SMOKE_BLOCKS.items():
        schematic.setBlock(position, block_state)

    schematic.save(str(output_dir), name, version)
    schem_path = output_dir / f"{name}.schem"
    if not schem_path.is_file() or schem_path.stat().st_size <= 0:
        raise RuntimeError(f"Expected non-empty schematic was not produced: {schem_path}")

    reloaded = mcschematic.MCSchematic(str(schem_path))
    observed: dict[str, str] = {}
    for position, expected in SMOKE_BLOCKS.items():
        actual = reloaded.getBlockStateAt(position)
        observed[str(position)] = actual
        if actual != expected:
            raise AssertionError(
                f"BlockState mismatch at {position}: expected {expected!r}, got {actual!r}"
            )

    manifest_path = output_dir / f"{name}.json"
    manifest_path.write_text(
        json.dumps(
            {
                "milestone": "M1",
                "minecraft_version_enum": version_name,
                "schematic": schem_path.name,
                "blocks": observed,
                "proof": "mcschematic save + reload BlockState equality",
                "runtime_required": ["Axiom import", "Minecraft Java placement"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    return schem_path, manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/m1"))
    parser.add_argument("--name", default=DEFAULT_NAME)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    schem_path, manifest_path = build_fixture(args.output_dir, args.name, args.version)
    print(f"M1 writer smoke PASS: {schem_path} ({schem_path.stat().st_size} bytes)")
    print(f"Manifest: {manifest_path}")
    print("Next proof: import this exact .schem into Axiom and place it in Minecraft Java.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
