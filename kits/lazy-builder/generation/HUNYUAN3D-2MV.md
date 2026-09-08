# Hunyuan Generation

## Role

This owner covers executable input→3D handoff while preserving **Hunyuan3D-2mv as the only 3D provider**.

Detailed local environment authority: `ENVIRONMENT.md`.

## Runtime files

```text
runtime_contract.py
→ source/model pins, explicit runtime defaults, actual-source identity verification

generate_text_reference.py
→ T1 text → native pinned HunyuanDiT reference

generate_shape.py
→ approved T1 or I1/I2 images → pinned shape-only model.glb

test_generation_contract.py
→ dependency-light source/wrapper contract tests
```

Heavy ML imports remain lazy so dry-run/static CI does not launch models.

## Pinned identity

```text
HunyuanDiT
model: Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
revision: 527cf2ecce7c04021975938f8b0e44e35d2b1ed9
pipeline: HunyuanDiTPipeline

Hunyuan3D source
repository: Tencent-Hunyuan/Hunyuan3D-2
commit: f8db63096c8282cb27354314d896feba5ba6ff8a
required checkout state: clean

Hunyuan3D-2mv
model: tencent/Hunyuan3D-2mv
revision: 08766051fa711c6ef5caf86b97e50304fdfcf0ef
subfolder: hunyuan3d-dit-v2-mv
```

The runner verifies the **actual imported Hunyuan3D checkout** before inference. Expected identity written in code is not treated as runtime evidence by itself.

## T1 text mode

Baseline:

```text
native HunyuanDiTPipeline
steps: 25
guidance_scale: 7.5
size: 1024 × 1024
seed: 0
offload: model CPU offload
```

No custom PAG layer routing is part of the baseline. Add it only after measured same-prompt evidence proves downstream value.

Output:

```text
reference_front.png
manifest.json
```

Required human gate:

```text
reference_front.png
→ APPROVAL_REQUIRED
→ user visual approval
→ PASS
→ Hunyuan3D-2mv
```

The controller does not permit text reference `RUNNING → PASS` directly.

## I1 / I2 shape mode

Named views:

```text
front
right
back
left
```

I1 uses one canonical image. Controlled I2 uses a consistent front/right/back/left set.

Explicit Standard extraction profile:

```text
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
variant: fp16
use_safetensors: true
box_v: 1.01
mc_level: 0.0
mc_algo: null
output_type: trimesh
background removal: ON
texture: OFF
```

Outputs:

```text
model.glb
manifest.json
```

The shape manifest binds named input paths/hashes, exact model revision, actual clean source checkout, extraction settings, positive mesh counts, and GLB hash.

Zero/empty mesh output is a hard failure.

## Input/source change behavior

```text
intentional T1/I1/I2 file change
→ refresh_case_input.py
→ new authoritative input SHA-256
→ invalidate only true dependents

unexpected hash change
→ INPUT_DRIFT
→ STOP

Hunyuan source commit mismatch or dirty checkout
→ STOP before generation
```

Do not relabel changed source/input as the old evidence.

## 8 GB GPU boundary

Text and shape generation are separate processes. Exit/unload the text process before shape generation.

`num_chunks=8000` is a first-proof low-memory-oriented setting, not a permanent quality optimum.

## Variant boundary

Fast/Turbo exist upstream but are not automatically routed. Standard is proven first. Compare variants only after a measured quality/runtime issue, using the same reference and judging downstream Minecraft usefulness.

## Proof boundary

Static CI proves wrapper/API shape, pins, explicit parameters, command routing, and manifest validation only.

Actual GPU execution, VRAM behavior, output quality, and Blender import remain `LOCAL RUNTIME PROOF REQUIRED`.
