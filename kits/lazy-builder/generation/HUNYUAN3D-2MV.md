# Hunyuan Generation

## Role

This owner covers the executable input→3D handoff while preserving **Hunyuan3D-2mv as the only 3D provider**.

## Runtime files

```text
runtime_contract.py
→ shared exact model IDs/defaults/input validation

generate_text_reference.py
→ text → one reviewable front reference

generate_shape.py
→ 1–4 named images → shape-only model.glb

test_generation_contract.py
→ dependency-light static contract tests
```

Heavy ML dependencies are imported lazily so `--dry-run` and CI contract checks do not require CUDA/model weights.

## Text mode

Exact model:

```text
Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
```

First proof defaults:

```text
steps: 25
PAG scale: 1.3
size: 1024 × 1024
seed: 0
offload: model CPU offload
```

Example:

```bash
python generate_text_reference.py \
  --prompt "compact stone train station with a clock tower" \
  --output-dir workspace/active/demo/generated/text
```

Outputs:

```text
reference_front.png
text_reference.json
```

Hard boundary:

```text
reference_front.png
→ USER REVIEW / APPROVAL
→ only then generate_shape.py
```

Do not automatically generate 3D from text and do not independently generate four T2I views for MVP.

## Image / multiview mode

Accepted named inputs:

```text
front
right
back
left
```

At least one is required. Four consistent views are preferred.

Exact first-proof model:

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

Example single-view proof:

```bash
python generate_shape.py \
  --front workspace/active/demo/references/front.png \
  --output-dir workspace/active/demo/generated/shape
```

Example multiview proof:

```bash
python generate_shape.py \
  --front workspace/active/demo/references/front.png \
  --right workspace/active/demo/references/right.png \
  --back workspace/active/demo/references/back.png \
  --left workspace/active/demo/references/left.png \
  --output-dir workspace/active/demo/generated/shape
```

Outputs:

```text
model.glb
generation.json
```

The generation manifest records the exact model/subfolder, named views, input hashes, parameters, mesh counts, and output hash.

## 8 GB GPU boundary

Run text-reference and shape generation as separate processes. Exit the text process before starting Hunyuan3D so both models are not required in VRAM at the same time.

`num_chunks=8000` is an initial low-VRAM-oriented proof setting. Runtime measurement may justify adjustment; do not treat it as a permanent quality optimum.

## Variant boundary

Fast and Turbo exist upstream but are not automatically routed.

First prove standard:

```text
hunyuan3d-dit-v2-mv
```

Only compare Fast/Turbo if the standard baseline shows a measured quality/runtime problem. Compare with the same reference(s), and judge usefulness after Minecraft discretization rather than mesh appearance alone.

## Failure routing

If text reference is poor:

1. inspect semantic prompt/reference framing;
2. regenerate only the 2D reference;
3. do not enter 3D until approved.

If shape generation fails technically:

1. verify exact environment/model/subfolder;
2. verify input image validity;
3. record CUDA/PyTorch/VRAM failure;
4. reduce only the implicated runtime parameter before changing architecture.

If shape quality is poor:

1. verify view consistency;
2. compare single canonical view vs consistent multiview when useful;
3. decide whether bounded Blender cleanup is cheaper;
4. judge whether defect survives Minecraft discretization;
5. only then consider a Hunyuan variant experiment.

## Proof

Static CI proves runner/config contracts only. Actual local generation must record:

```text
GPU / VRAM
Python
PyTorch / CUDA
model/subfolder
parameters
runtime
peak VRAM
output files
GLB Blender import result
material geometry defects
```

No local generation = no runtime PASS.
