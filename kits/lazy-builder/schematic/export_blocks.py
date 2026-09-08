#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MINECRAFTIZE_DIR = REPO_ROOT / "kits" / "lazy-builder" / "minecraftize"
if MINECRAFTIZE_DIR.is_dir() and str(MINECRAFTIZE_DIR) not in sys.path:
    sys.path.insert(0, str(MINECRAFTIZE_DIR))
else:
    sibling = Path(__file__).resolve().parents[1] / "minecraftize"
    if sibling.is_dir() and str(sibling) not in sys.path:
        sys.path.insert(0, str(sibling))

from block_model import read_blocks_json

MCSCHEMATIC_VERSION = "JE_1_21_4"
DATA_VERSION = 4189


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def export_blocks(blocks_path: Path, output_dir: Path, *, name: str = "build") -> tuple[Path, Path]:
    import mcschematic

    payload = read_blocks_json(blocks_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    schematic = mcschematic.MCSchematic()
    for block in payload["blocks"]:
        schematic.setBlock((block["x"], block["y"], block["z"]), block["block_state"])

    version = getattr(mcschematic.Version, MCSCHEMATIC_VERSION)
    schematic.save(str(output_dir), name, version)
    schem_path = output_dir / f"{name}.schem"
    if not schem_path.is_file() or schem_path.stat().st_size == 0:
        raise RuntimeError(f"schematic was not produced: {schem_path}")

    reloaded = mcschematic.MCSchematic(str(schem_path))
    sampled = []
    for block in payload["blocks"]:
        coordinate = (block["x"], block["y"], block["z"])
        actual = reloaded.getBlockStateAt(coordinate)
        if actual != block["block_state"]:
            raise RuntimeError(
                f"BlockState round-trip mismatch at {coordinate}: expected {block['block_state']}, got {actual}"
            )
        sampled.append({"coordinate": list(coordinate), "block_state": actual})

    manifest = {
        "schema_version": 1,
        "stage": "schematic",
        "writer": "mcschematic==11.4.4",
        "minecraft_version": "1.21.4",
        "mcschematic_version": MCSCHEMATIC_VERSION,
        "sponge_version": 2,
        "data_version": DATA_VERSION,
        "source_blocks": str(blocks_path.resolve()),
        "source_block_count": payload["block_count"],
        "source_bounds": payload["bounds"],
        "output": str(schem_path.resolve()),
        "output_sha256": sha256_file(schem_path),
        "round_trip_samples": sampled,
        "status": "WRITER_ROUND_TRIP_PASS_RUNTIME_AXIOM_REQUIRED",
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return schem_path, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export canonical LazyBuilder blocks.json to Sponge V2 .schem.")
    parser.add_argument("--blocks", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--name", default="build")
    args = parser.parse_args()

    schem, _manifest = export_blocks(
        Path(args.blocks).expanduser().resolve(),
        Path(args.output_dir).expanduser().resolve(),
        name=args.name,
    )
    print(schem)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
