from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping

HUNYUAN3D_MODEL = "tencent/Hunyuan3D-2mv"
HUNYUAN3D_SUBFOLDER = "hunyuan3d-dit-v2-mv"
HUNYUAN3D_MODEL_REVISION = "08766051fa711c6ef5caf86b97e50304fdfcf0ef"
HUNYUAN3D_SOURCE_REPO = "Tencent-Hunyuan/Hunyuan3D-2"
HUNYUAN3D_SOURCE_COMMIT = "f8db63096c8282cb27354314d896feba5ba6ff8a"

HUNYUANDIT_MODEL = "Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled"
HUNYUANDIT_MODEL_REVISION = "527cf2ecce7c04021975938f8b0e44e35d2b1ed9"

VIEW_NAMES = ("front", "right", "back", "left")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}

SHAPE_DEFAULTS = {
    "steps": 30,
    "guidance_scale": 7.5,
    "octree_resolution": 256,
    "num_chunks": 8000,
    "seed": 12345,
}

TEXT_DEFAULTS = {
    "steps": 25,
    "pag_scale": 1.3,
    "width": 1024,
    "height": 1024,
    "seed": 0,
    "offload": "model",
}

REFERENCE_PROMPT_SUFFIX = (
    "front view, full object visible, centered, isolated on a white background, "
    "3D asset reference, no people, no surrounding scene"
)
TEXT_NEGATIVE_PROMPT = (
    "text, watermark, cropped, out of frame, blurry, low quality, distorted, "
    "duplicate object, extra object, people, surrounding scenery"
)


def normalize_text_prompt(prompt: str) -> str:
    prompt = " ".join(prompt.strip().split())
    if not prompt:
        raise ValueError("text prompt must not be empty")
    return prompt


def build_reference_prompt(prompt: str) -> str:
    base = normalize_text_prompt(prompt).rstrip(" .")
    return f"{base}, {REFERENCE_PROMPT_SUFFIX}"


def validate_view_paths(
    views: Mapping[str, str | Path | None], *, require_exists: bool = True
) -> dict[str, Path]:
    normalized: dict[str, Path] = {}
    for view in VIEW_NAMES:
        raw = views.get(view)
        if raw is None:
            continue
        path = Path(raw).expanduser()
        if path.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError(f"unsupported {view} image extension: {path.suffix or '<none>'}")
        if require_exists and not path.is_file():
            raise ValueError(f"{view} image does not exist: {path}")
        normalized[view] = path
    if not normalized:
        raise ValueError("at least one of front/right/back/left is required")
    return normalized


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
