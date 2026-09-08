# Hunyuan Generation

## Role

This owner covers executable input→3D handoff while preserving **Hunyuan3D-2mv as the only 3D provider**.

Detailed local environment authority: `ENVIRONMENT.md`.

## Runtime files

```text
runtime_contract.py
→ exact model/source pins + defaults + input validation

generate_text_reference.py
→ T1 text/prompt file → one reviewable front reference

generate_shape.py
→ approved T1 reference or I1/I2 named images → shape-only model.glb

test_generation_contract.py
→ dependency-light static contract tests
```

Heavy ML dependencies are imported lazily so `--dry-run` and CI do not require CUDA/model weights.

## Pinned identity

```text
HunyuanDiT
model: Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
revision: 527cf2ecce7c04021975938f8b0e44e35d2b1ed9

Hunyuan3D source
repository: Tencent-Hunyuan/Hunyuan3D-2
commit: f8db63096c8282cb27354314d896feba5ba6ff8a

Hunyuan3D-2mv
model: tencent/Hunyuan3D-2mv
revision: 08766051fa711c6ef5caf86b97e50304fdfcf0ef
subfolder: hunyuan3d-dit-v2-mv
```

The shape runner resolves the pinned Hugging Face snapshot explicitly before loading the upstream pipeline.

## T1 text mode

First-proof defaults:

```text
steps: 25
PAG scale: 1.3
size: 1024 × 1024
seed: 0
offload: model CPU offload
```

Output:

```text
reference_front.png
manifest.json
```

Hard gate:

```text
reference_front.png
→ USER REVIEW / APPROVAL
→ only then Hunyuan3D-2mv
```

The manifest binds model revision and output SHA-256.

## I1 / I2 shape mode

Accepted named views:

```text
front
right
back
left
```

I1 uses one canonical image. The controlled I2 path uses a consistent front/right/back/left set.

Initial bounded Standard profile:

```text
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
background removal: ON
texture: OFF
```

The `num_chunks=8000` profile is intentionally bounded for the RTX 3070 8 GB first proof. It is not claimed as the final quality/performance optimum.

Outputs per shape stage:

```text
model.glb
manifest.json
```

The manifest records exact model/source revisions, named-view hashes, parameters, mesh counts, and GLB hash.

## 8 GB GPU boundary

Text reference and shape generation are separate processes. Exit/unload the text process before shape generation so both large models are not required in VRAM simultaneously.

## Variant boundary

Fast/Turbo exist upstream but are not automatically routed. Standard is proven first. Variant comparison requires measured same-reference runtime/output evidence and downstream Minecraft usefulness.

## Failure routing

```text
text reference semantically wrong
→ text/reference owner

input hash changed
→ invalidate affected input owner; do not silently continue

shape startup / VRAM failure
→ generation environment/profile owner

shape geometry poor
→ verify reference consistency first
→ bounded Blender cleanup vs Minecraft discretization
→ only then consider a variant experiment
```

## Proof boundary

Static CI proves pins, command routing, serialization contracts and dry-run behavior only.

Actual local generation must still record GPU/VRAM, Python/PyTorch/CUDA, runtime, peak VRAM, exact output files, and Blender import result.

No local generation = no runtime PASS.
