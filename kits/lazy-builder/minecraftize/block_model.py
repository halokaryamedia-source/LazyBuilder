from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 1
MINECRAFT_VERSION = "1.21.4"
BLOCK_ID_RE = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_/.-]+$")
PROPERTY_RE = re.compile(r"^[a-z0-9_]+=[a-z0-9_./-]+$")


class BlockModelError(ValueError):
    pass


def canonical_block_state(raw: str) -> str:
    if not isinstance(raw, str):
        raise BlockModelError("block_state must be a string")
    raw = raw.strip()
    if not raw:
        raise BlockModelError("block_state must not be empty")
    if "[" not in raw:
        if not BLOCK_ID_RE.fullmatch(raw):
            raise BlockModelError(f"invalid block id: {raw}")
        return raw
    if not raw.endswith("]") or raw.count("[") != 1:
        raise BlockModelError(f"invalid block state syntax: {raw}")
    block_id, properties_raw = raw[:-1].split("[", 1)
    if not BLOCK_ID_RE.fullmatch(block_id):
        raise BlockModelError(f"invalid block id: {block_id}")
    if not properties_raw:
        raise BlockModelError("block state property list must not be empty")
    properties: dict[str, str] = {}
    for item in properties_raw.split(","):
        item = item.strip()
        if not PROPERTY_RE.fullmatch(item):
            raise BlockModelError(f"invalid block state property: {item}")
        key, value = item.split("=", 1)
        if key in properties:
            raise BlockModelError(f"duplicate block state property: {key}")
        properties[key] = value
    ordered = ",".join(f"{key}={properties[key]}" for key in sorted(properties))
    return f"{block_id}[{ordered}]"


@dataclass(frozen=True, order=True)
class Block:
    x: int
    y: int
    z: int
    block_state: str
    source_reason: str | None = None

    @classmethod
    def from_mapping(cls, payload: dict[str, Any]) -> "Block":
        coords = []
        for key in ("x", "y", "z"):
            value = payload.get(key)
            if not isinstance(value, int) or isinstance(value, bool):
                raise BlockModelError(f"block.{key} must be an integer")
            coords.append(value)
        state = canonical_block_state(payload.get("block_state"))
        reason = payload.get("source_reason")
        if reason is not None and (not isinstance(reason, str) or not reason.strip()):
            raise BlockModelError("block.source_reason must be null or non-empty string")
        return cls(coords[0], coords[1], coords[2], state, reason.strip() if isinstance(reason, str) else None)

    def to_mapping(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "block_state": self.block_state,
        }
        if self.source_reason is not None:
            payload["source_reason"] = self.source_reason
        return payload


def blender_to_minecraft(x: float, y: float, z: float) -> tuple[float, float, float]:
    """Canonical axis mapping: Minecraft X=Blender X, Y=Blender Z, Z=-Blender Y."""
    return x, z, -y


def _bounds(blocks: list[Block]) -> dict[str, Any]:
    if not blocks:
        return {"min": None, "max": None, "size": {"x": 0, "y": 0, "z": 0}}
    min_x = min(block.x for block in blocks)
    min_y = min(block.y for block in blocks)
    min_z = min(block.z for block in blocks)
    max_x = max(block.x for block in blocks)
    max_y = max(block.y for block in blocks)
    max_z = max(block.z for block in blocks)
    return {
        "min": {"x": min_x, "y": min_y, "z": min_z},
        "max": {"x": max_x, "y": max_y, "z": max_z},
        "size": {"x": max_x - min_x + 1, "y": max_y - min_y + 1, "z": max_z - min_z + 1},
    }


def normalize_blocks(blocks: Iterable[Block | dict[str, Any]]) -> list[Block]:
    normalized: list[Block] = []
    seen: dict[tuple[int, int, int], str] = {}
    for raw in blocks:
        block = raw if isinstance(raw, Block) else Block.from_mapping(raw)
        coordinate = (block.x, block.y, block.z)
        previous = seen.get(coordinate)
        if previous is not None:
            if previous == block.block_state:
                raise BlockModelError(f"duplicate coordinate repeated with same state: {coordinate}")
            raise BlockModelError(
                f"duplicate coordinate with conflicting states: {coordinate}: {previous} vs {block.block_state}"
            )
        seen[coordinate] = block.block_state
        normalized.append(block)
    return sorted(normalized, key=lambda block: (block.y, block.z, block.x, block.block_state))


def build_payload(
    blocks: Iterable[Block | dict[str, Any]],
    *,
    source: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    normalized = normalize_blocks(blocks)
    counts: dict[str, int] = {}
    for block in normalized:
        block_id = block.block_state.split("[", 1)[0]
        counts[block_id] = counts.get(block_id, 0) + 1
    return {
        "schema_version": SCHEMA_VERSION,
        "minecraft_version": MINECRAFT_VERSION,
        "coordinate_contract": {
            "minecraft_x": "blender_x",
            "minecraft_y": "blender_z",
            "minecraft_z": "-blender_y",
        },
        "source": source or {},
        "metadata": metadata or {},
        "bounds": _bounds(normalized),
        "block_count": len(normalized),
        "counts_by_block": dict(sorted(counts.items())),
        "blocks": [block.to_mapping() for block in normalized],
    }


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise BlockModelError(f"schema_version must be {SCHEMA_VERSION}")
    if payload.get("minecraft_version") != MINECRAFT_VERSION:
        raise BlockModelError(f"minecraft_version must be {MINECRAFT_VERSION}")
    raw_blocks = payload.get("blocks")
    if not isinstance(raw_blocks, list):
        raise BlockModelError("blocks must be an array")
    rebuilt = build_payload(raw_blocks, source=payload.get("source") or {}, metadata=payload.get("metadata") or {})
    if payload.get("block_count") != rebuilt["block_count"]:
        raise BlockModelError("block_count does not match blocks")
    if payload.get("bounds") != rebuilt["bounds"]:
        raise BlockModelError("bounds do not match blocks")
    if payload.get("counts_by_block") != rebuilt["counts_by_block"]:
        raise BlockModelError("counts_by_block do not match blocks")
    if payload.get("coordinate_contract") != rebuilt["coordinate_contract"]:
        raise BlockModelError("coordinate_contract drift")
    if payload.get("blocks") != rebuilt["blocks"]:
        raise BlockModelError("blocks are not in canonical order/state form")
    return rebuilt


def write_blocks_json(path: Path, payload: dict[str, Any]) -> None:
    validate_payload(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_blocks_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BlockModelError(f"cannot read blocks.json {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise BlockModelError("blocks.json root must be an object")
    return validate_payload(payload)
