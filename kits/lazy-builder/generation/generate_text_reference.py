#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path

from runtime_contract import (
    HUNYUANDIT_MODEL,
    TEXT_DEFAULTS,
    TEXT_NEGATIVE_PROMPT,
    build_reference_prompt,
    write_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate one reviewable front reference image from text using HunyuanDiT."
    )
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", type=int, default=TEXT_DEFAULTS["seed"])
    parser.add_argument("--steps", type=int, default=TEXT_DEFAULTS["steps"])
    parser.add_argument("--pag-scale", type=float, default=TEXT_DEFAULTS["pag_scale"])
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


def build_plan(args: argparse.Namespace) -> dict:
    output_dir = Path(args.output_dir).expanduser()
    return {
        "stage": "text_reference",
        "model": HUNYUANDIT_MODEL,
        "prompt": args.prompt.strip(),
        "resolved_prompt": build_reference_prompt(args.prompt),
        "params": {
            "device": args.device,
            "seed": args.seed,
            "steps": args.steps,
            "pag_scale": args.pag_scale,
            "width": args.width,
            "height": args.height,
            "offload": args.offload,
        },
        "outputs": {
            "reference": str(output_dir / "reference_front.png"),
            "manifest": str(output_dir / "text_reference.json"),
        },
        "handoff": "USER_REVIEW_REQUIRED_BEFORE_3D",
    }


def run(args: argparse.Namespace) -> int:
    plan = build_plan(args)
    if args.dry_run:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    import torch
    from diffusers import AutoPipelineForText2Image

    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    reference_path = output_dir / "reference_front.png"
    manifest_path = output_dir / "text_reference.json"

    pipe = AutoPipelineForText2Image.from_pretrained(
        HUNYUANDIT_MODEL,
        torch_dtype=torch.float16,
        enable_pag=True,
        pag_applied_layers=["blocks.(16|17|18|19)"],
    )

    if args.offload == "model":
        pipe.enable_model_cpu_offload()
    elif args.offload == "sequential":
        pipe.enable_sequential_cpu_offload()
    else:
        pipe.to(args.device)

    generator_device = "cuda" if str(args.device).startswith("cuda") else "cpu"
    generator = torch.Generator(device=generator_device).manual_seed(args.seed)
    image = pipe(
        prompt=plan["resolved_prompt"],
        negative_prompt=TEXT_NEGATIVE_PROMPT,
        num_inference_steps=args.steps,
        pag_scale=args.pag_scale,
        width=args.width,
        height=args.height,
        generator=generator,
    ).images[0]
    image.save(reference_path)

    manifest = dict(plan)
    manifest["status"] = "GENERATED_REFERENCE_REVIEW_REQUIRED"
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
