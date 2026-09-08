#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path

from runtime_contract import (
    HUNYUAN3D_MODEL,
    HUNYUAN3D_SUBFOLDER,
    SHAPE_DEFAULTS,
    VIEW_NAMES,
    sha256_file,
    validate_view_paths,
    write_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a shape-only GLB from one to four named views using Hunyuan3D-2mv."
    )
    for view in VIEW_NAMES:
        parser.add_argument(f"--{view}")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", type=int, default=SHAPE_DEFAULTS["seed"])
    parser.add_argument("--steps", type=int, default=SHAPE_DEFAULTS["steps"])
    parser.add_argument(
        "--guidance-scale", type=float, default=SHAPE_DEFAULTS["guidance_scale"]
    )
    parser.add_argument(
        "--octree-resolution", type=int, default=SHAPE_DEFAULTS["octree_resolution"]
    )
    parser.add_argument("--num-chunks", type=int, default=SHAPE_DEFAULTS["num_chunks"])
    parser.add_argument(
        "--keep-background",
        action="store_true",
        help="Skip the official Hunyuan background remover.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


def build_plan(args: argparse.Namespace, *, require_exists: bool) -> dict:
    views = validate_view_paths(
        {view: getattr(args, view) for view in VIEW_NAMES}, require_exists=require_exists
    )
    output_dir = Path(args.output_dir).expanduser()
    return {
        "stage": "shape",
        "model": HUNYUAN3D_MODEL,
        "subfolder": HUNYUAN3D_SUBFOLDER,
        "views": {name: str(path) for name, path in views.items()},
        "params": {
            "device": args.device,
            "seed": args.seed,
            "steps": args.steps,
            "guidance_scale": args.guidance_scale,
            "octree_resolution": args.octree_resolution,
            "num_chunks": args.num_chunks,
            "remove_background": not args.keep_background,
            "texture": False,
        },
        "outputs": {
            "glb": str(output_dir / "model.glb"),
            "manifest": str(output_dir / "manifest.json"),
        },
        "handoff": "GENERATED_GLB_RUNTIME_REVIEW_REQUIRED",
    }


def run(args: argparse.Namespace) -> int:
    plan = build_plan(args, require_exists=not args.dry_run)
    if args.dry_run:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    import torch
    from PIL import Image
    from hy3dgen.rembg import BackgroundRemover
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline

    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    glb_path = output_dir / "model.glb"
    manifest_path = output_dir / "manifest.json"

    prepared_images = {}
    remover = None if args.keep_background else BackgroundRemover()
    for name, raw_path in plan["views"].items():
        image = Image.open(raw_path).convert("RGBA")
        if remover is not None:
            image = remover(image)
        prepared_images[name] = image

    pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
        HUNYUAN3D_MODEL,
        subfolder=HUNYUAN3D_SUBFOLDER,
        use_safetensors=True,
        device=args.device,
    )

    generator_device = "cuda" if str(args.device).startswith("cuda") else "cpu"
    generator = torch.Generator(device=generator_device).manual_seed(args.seed)
    mesh = pipeline(
        image=prepared_images,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance_scale,
        octree_resolution=args.octree_resolution,
        num_chunks=args.num_chunks,
        generator=generator,
        output_type="trimesh",
    )[0]
    mesh.export(glb_path)

    manifest = dict(plan)
    manifest["status"] = "GENERATED_GLB_RUNTIME_REVIEW_REQUIRED"
    manifest["inputs"] = {
        name: {"path": raw_path, "sha256": sha256_file(Path(raw_path))}
        for name, raw_path in plan["views"].items()
    }
    manifest["mesh"] = {
        "vertices": int(len(mesh.vertices)),
        "faces": int(len(mesh.faces)),
    }
    manifest["output_sha256"] = sha256_file(glb_path)
    write_json(manifest_path, manifest)

    for image in prepared_images.values():
        image.close()
    del mesh
    del pipeline
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    print(glb_path)
    return 0


def main() -> int:
    return run(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
