#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path

from runtime_contract import (
    HUNYUANDIT_MODEL,
    HUNYUANDIT_MODEL_REVISION,
    HUNYUANDIT_PIPELINE,
    TEXT_DEFAULTS,
    TEXT_NEGATIVE_PROMPT,
    build_reference_prompt,
    sha256_file,
    write_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate one reviewable front reference image from text using HunyuanDiT."
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", type=int, default=TEXT_DEFAULTS["seed"])
    parser.add_argument("--steps", type=int, default=TEXT_DEFAULTS["steps"])
    parser.add_argument(
        "--guidance-scale", type=float, default=TEXT_DEFAULTS["guidance_scale"]
    )
    parser.add_argument("--width", type=int, default=TEXT_DEFAULTS["width"])
    parser.add_argument("--height", type=int, default=TEXT_DEFAULTS["height"])
    parser.add_argument(
        "--offload",
        choices=("model", "sequential", "none"),
        default=TEXT_DEFAULTS["offload"],
        help="VRAM strategy. 'model' is the default for the 8 GB development GPU.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


def resolve_prompt(args: argparse.Namespace, *, require_exists: bool) -> tuple[str, str | None]:
    if args.prompt is not None:
        return args.prompt, None
    path = Path(args.prompt_file).expanduser()
    if require_exists and not path.is_file():
        raise ValueError(f"prompt file does not exist: {path}")
    if path.is_file():
        return path.read_text(encoding="utf-8"), str(path.resolve())
    if require_exists:
        raise ValueError(f"prompt file does not exist: {path}")
    return f"<prompt from {path}>", str(path)


def build_plan(args: argparse.Namespace, *, require_exists: bool = True) -> dict:
    prompt, prompt_file = resolve_prompt(args, require_exists=require_exists)
    output_dir = Path(args.output_dir).expanduser()
    if args.steps <= 0:
        raise ValueError("steps must be positive")
    if args.guidance_scale < 0:
        raise ValueError("guidance scale must be non-negative")
    if args.width <= 0 or args.height <= 0:
        raise ValueError("image width/height must be positive")
    return {
        "schema_version": 1,
        "stage": "text_reference",
        "pipeline": HUNYUANDIT_PIPELINE,
        "model": HUNYUANDIT_MODEL,
        "model_revision": HUNYUANDIT_MODEL_REVISION,
        "prompt": prompt.strip(),
        "prompt_file": prompt_file,
        "resolved_prompt": build_reference_prompt(prompt),
        "params": {
            "device": args.device,
            "seed": args.seed,
            "steps": args.steps,
            "guidance_scale": args.guidance_scale,
            "width": args.width,
            "height": args.height,
            "offload": args.offload,
        },
        "outputs": {
            "reference": str(output_dir / "reference_front.png"),
            "manifest": str(output_dir / "manifest.json"),
        },
        "handoff": "USER_REVIEW_REQUIRED_BEFORE_3D",
    }


def run(args: argparse.Namespace) -> int:
    plan = build_plan(args, require_exists=not args.dry_run)
    if args.dry_run:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    import torch
    from diffusers import HunyuanDiTPipeline

    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    reference_path = output_dir / "reference_front.png"
    manifest_path = output_dir / "manifest.json"

    pipe = HunyuanDiTPipeline.from_pretrained(
        HUNYUANDIT_MODEL,
        revision=HUNYUANDIT_MODEL_REVISION,
        torch_dtype=torch.float16,
    )

    if args.offload == "model":
        pipe.enable_model_cpu_offload(device=args.device)
    elif args.offload == "sequential":
        pipe.enable_sequential_cpu_offload(device=args.device)
    else:
        pipe.to(args.device)

    generator_device = str(args.device) if str(args.device).startswith("cuda") else "cpu"
    generator = torch.Generator(device=generator_device).manual_seed(args.seed)
    image = pipe(
        prompt=plan["resolved_prompt"],
        negative_prompt=TEXT_NEGATIVE_PROMPT,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance_scale,
        width=args.width,
        height=args.height,
        generator=generator,
    ).images[0]
    image.save(reference_path)

    manifest = dict(plan)
    manifest["status"] = "GENERATED_REFERENCE_REVIEW_REQUIRED"
    manifest["output_sha256"] = sha256_file(reference_path)
    write_json(manifest_path, manifest)

    del image
    del pipe
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    print(reference_path)
    return 0


def main() -> int:
    return run(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
