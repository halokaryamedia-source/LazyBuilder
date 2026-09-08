#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from block_model import read_blocks_json


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _projection(blocks: list[dict], axes: tuple[str, str]) -> set[tuple[int, int]]:
    return {(int(block[axes[0]]), int(block[axes[1]])) for block in blocks}


def _panel(label: str, points: set[tuple[int, int]], *, x_offset: float, panel_width: float = 320.0, panel_height: float = 320.0) -> tuple[str, dict]:
    if not points:
        return "", {"points": 0, "bounds": None}
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    cell = min((panel_width - 24) / max(width, 1), (panel_height - 48) / max(height, 1), 12.0)
    draw_w = width * cell
    draw_h = height * cell
    origin_x = x_offset + (panel_width - draw_w) / 2
    origin_y = 36 + (panel_height - 48 - draw_h) / 2
    rects = []
    for x, y in sorted(points, key=lambda item: (item[1], item[0])):
        sx = origin_x + (x - min_x) * cell
        sy = origin_y + (max_y - y) * cell
        rects.append(
            f'<rect x="{sx:.3f}" y="{sy:.3f}" width="{cell:.3f}" height="{cell:.3f}" class="block"/>'
        )
    panel = (
        f'<g><text x="{x_offset + panel_width / 2:.1f}" y="22" text-anchor="middle" class="label">{html.escape(label)}</text>'
        + "".join(rects)
        + f'<rect x="{x_offset + 4:.1f}" y="30" width="{panel_width - 8:.1f}" height="{panel_height - 34:.1f}" class="frame"/></g>'
    )
    return panel, {
        "points": len(points),
        "bounds": {"min": [min_x, min_y], "max": [max_x, max_y], "size": [width, height]},
    }


def build_preview(blocks_path: Path, output_dir: Path) -> tuple[Path, Path]:
    payload = read_blocks_json(blocks_path)
    blocks = payload["blocks"]
    projections = [
        ("TOP X/Z", _projection(blocks, ("x", "z"))),
        ("FRONT X/Y", _projection(blocks, ("x", "y"))),
        ("RIGHT Z/Y", _projection(blocks, ("z", "y"))),
    ]
    panels = []
    metrics = {}
    for index, (label, points) in enumerate(projections):
        panel, data = _panel(label, points, x_offset=index * 320.0)
        panels.append(panel)
        metrics[label] = data
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 320" role="img" aria-label="LazyBuilder canonical block preview">
<style>
.block {{ fill: #171717; stroke: #ffffff; stroke-width: 0.08; }}
.frame {{ fill: none; stroke: #777777; stroke-width: 1; }}
.label {{ font: 14px sans-serif; fill: #171717; }}
</style>
<rect width="960" height="320" fill="#ffffff"/>
{''.join(panels)}
</svg>\n'''
    output_dir.mkdir(parents=True, exist_ok=True)
    preview_path = output_dir / "preview.svg"
    preview_path.write_text(svg, encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "stage": "minecraft_preview",
        "status": "PREVIEW_READY_FROM_CANONICAL_BLOCKS",
        "source_blocks": str(blocks_path.resolve()),
        "source_sha256": sha256_file(blocks_path),
        "block_count": payload["block_count"],
        "bounds": payload["bounds"],
        "projections": metrics,
        "output": str(preview_path.resolve()),
        "output_sha256": sha256_file(preview_path),
        "runtime_apps_launched": False,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return preview_path, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic SVG preview from canonical LazyBuilder blocks.json.")
    parser.add_argument("--blocks", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    preview, _manifest = build_preview(
        Path(args.blocks).expanduser().resolve(),
        Path(args.output_dir).expanduser().resolve(),
    )
    print(preview)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
