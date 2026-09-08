# Hunyuan Generation

## Role

This owner covers the executable input→3D handoff while preserving **Hunyuan3D-2mv as the only 3D provider**.

## Runtime files

```text
runtime_contract.py
→ exact model IDs/defaults/input validation

generate_text_reference.py
→ text/prompt file → one reviewable front reference

generate_shape.py
→ 1–4 named images → shape-only model.glb

test_generation_contract.py
→ dependency-light static contract tests
```

Heavy ML dependencies are imported lazily so `--dry-run` and CI do not require CUDA/model weights.

## Text mode

Exact model:

```text
Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
```

First-proof defaults:

```text
steps: 25
PAG scale: 1.3
size: 1024 × 1024
seed: 0
offload: model CPU offload
```

For standalone use:

```bash
python generate_text_reference.py \
  --prompt "compact stone train station with a clock tower" \
  --output-dir <run>/10-reference
```

For the unified acceptance case:

```bash
python generate_text_reference.py \
  --prompt-file <case>/inputs/text/prompt.txt \
  --output-dir <run>/10-reference
```

Outputs:

```text
reference_front.png
manifest.json
```

Hard boundary:

```text
reference_front.png
→ USER REVIEW / APPROVAL
→ only then may it enter Hunyuan3D-2mv
```

The unified acceptance session proves the complete text-origin path by using the approved reference as:

```text
10-reference/reference_front.png
→ 19-shape-text/model.glb
```

Do not independently generate four T2I views for MVP.

## Image / multiview mode

Accepted named views:

```text
front
right
back
left
```

At least one is required. Four consistent views are preferred.

Exact first-proof shape model:

```text
model: tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
```

Initial bounded profile:

```text
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
background removal: ON
texture: OFF
```

Outputs per shape stage:

```text
model.glb
manifest.json
```

The manifest records exact model/subfolder, named views, input hashes, parameters, mesh counts, and output hash.

Unified acceptance paths:

```text
T1 approved reference → 19-shape-text/
I1 front image        → 20-shape-single/
I2 four views         → 21-shape-multiview/
```

All three are generated with the same Standard Hunyuan3D-2mv baseline before a representative GLB is selected for Blender.

## 8 GB GPU boundary

Text-reference and shape generation run as separate processes. Exit/unload the text process before shape generation so both large models are not required in VRAM simultaneously.

`num_chunks=8000` is the initial low-VRAM-oriented proof setting, not a permanent quality optimum.

## Variant boundary

Fast and Turbo exist upstream but are not automatically routed.

First prove:

```text
hunyuan3d-dit-v2-mv
```

Only compare variants after a measured quality/runtime problem, using the same references and judging downstream Minecraft usefulness rather than mesh appearance alone.

## Failure routing

```text
text reference semantically wrong
→ text/reference owner; regenerate only T1

shape model startup / VRAM failure
→ generation environment/profile owner

one view path fails while others pass
→ preserve independent successful paths; invalidate only true dependents

shape geometry poor
→ verify references/view consistency first
→ judge whether bounded Blender cleanup or Minecraft discretization makes the defect irrelevant
→ only then consider a variant experiment
```

## Proof boundary

Static CI proves runner/config/session contracts only.

Actual local generation must still record GPU/VRAM, Python/PyTorch/CUDA, exact model parameters, runtime, peak VRAM, output files, and Blender import result.

No local generation = no runtime PASS.
