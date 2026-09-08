# Next Action

## Current Status

`M2_INPUT_TO_3D_IMPLEMENTATION_READY_LOCAL_RUNTIME_REQUIRED`

The repository operating system, Astra6 profile, execution-mode routing, M1 writer/Axiom research baseline, and the image/text→3D implementation contract are now established.

The user explicitly advanced Flow 2/3 generation implementation while the exact M1 Axiom/Paper/Minecraft runtime proof remains pending. This does **not** mark M1 PASS.

Branch state:

```text
develop → active Development continuation
Local   → verified integration milestone
main    → stable repository history
```

## Locked input-to-3D architecture

```text
IMAGE / MULTIVIEW
front / right / back / left
→ Hunyuan3D-2mv
→ model.glb

TEXT
→ Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
→ reference_front.png
→ USER REVIEW / APPROVAL
→ Hunyuan3D-2mv
→ model.glb
```

Hunyuan3D-2mv remains the **only 3D provider**. HunyuanDiT is only an auxiliary 2D reference generator.

The temporary/unverified `HunyuanDiT v1.2 Distilled Lite` label is retired from the active contract.

## Implemented repository runners

```text
kits/lazy-builder/generation/runtime_contract.py
kits/lazy-builder/generation/generate_text_reference.py
kits/lazy-builder/generation/generate_shape.py
kits/lazy-builder/generation/test_generation_contract.py
```

Text and shape are separate processes so the 8 GB GPU does not need both models resident simultaneously.

## First-proof text baseline

```text
model: Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
steps: 25
PAG scale: 1.3
size: 1024 × 1024
seed: 0
offload: model CPU offload
output: reference_front.png
handoff: USER_REVIEW_REQUIRED_BEFORE_3D
```

## First-proof shape baseline

```text
model: tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
background removal: ON
texture: OFF
output: model.glb
```

Fast/Turbo variants are not routed automatically. Standard is proven first.

## Next Step — local generation runtime proof

Use `local` mode. Repository/CI proof is not GPU runtime proof.

### 1. Environment preflight

Record:

```text
OS
GPU + exact VRAM
NVIDIA driver
Python
PyTorch
CUDA
system RAM
free disk
```

### 2. Text-reference proof

Run one bounded prompt:

```bash
python kits/lazy-builder/generation/generate_text_reference.py \
  --prompt "<test object/building>" \
  --output-dir workspace/active/generation-proof/generated/text
```

Record:

```text
reference generated yes/no
runtime
peak VRAM
major visual defects
```

### 3. Approval gate

Inspect `reference_front.png` before shape generation.

```text
APPROVED
→ continue

REJECTED
→ fix/regenerate only the text-reference stage
```

Do not silently continue from a poor text-generated reference.

### 4. Single-view shape proof

Use the approved front image:

```bash
python kits/lazy-builder/generation/generate_shape.py \
  --front workspace/active/generation-proof/generated/text/reference_front.png \
  --output-dir workspace/active/generation-proof/generated/shape-single
```

Record:

```text
model/subfolder
parameters
runtime
peak VRAM
model.glb generated
mesh defects
```

### 5. Multiview shape proof

When a consistent source set is available, repeat with front/right/back/left and compare against the single-view result.

Do not change provider/variant during the first controlled proof.

### 6. Blender compatibility proof

Open the exact generated `model.glb` in Blender 5.2.x LTS and record:

```text
import success
orientation
scale sanity
mesh integrity
major floating/noisy geometry
```

Only after a usable GLB is proven should Minecraftize runtime implementation begin.

## Failure routing

```text
text model fails to start
→ HunyuanDiT environment / PyTorch / CUDA / offload

text image runs but concept is wrong
→ text/reference stage only

shape model fails to start
→ Hunyuan3D environment / extension / PyTorch / CUDA / VRAM

single view works, multiview fails
→ named-view consistency / multiview runtime

GLB generated but Blender rejects it
→ generation/export compatibility

mesh looks imperfect
→ determine whether defect matters after Minecraft discretization before changing variants/providers
```

## M1 runtime remains pending

Still required before M1 can be called end-to-end PASS:

```text
Axiom 5.3.0 import
Clipboard
AxiomPaper 5.0.1 handshake/placement
Minecraft BlockState verification
```

## Stop Boundary

Do not automatically:

- add Tripo / TRELLIS / Pixal3D / another 3D provider;
- add Hunyuan3D-2 base as a parallel path;
- add Fast/Turbo routing;
- generate four independent T2I views;
- enable Hunyuan texture generation;
- combine Hunyuan runtime with Blender Python;
- implement Minecraftize runtime before first usable GLB proof;
- add MCP/API-server orchestration;
- promote `develop` to `Local` or `Local` to `main`.
