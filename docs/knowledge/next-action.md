# Next Action

## Current Status

`M2_GENERATION_CONTRACT_IMPLEMENTED_LOCAL_RUNTIME_REQUIRED`

The repository operating system, Astra6 profile, execution modes, M1 writer/Axiom research baseline, and the image/text→3D generation contract are established.

The user explicitly advanced Flow 3 implementation work while the exact M1 Axiom/Paper/Minecraft runtime proof remains pending. This does **not** convert M1 to PASS; it only allows generation scaffolding/research to proceed in parallel.

Branch state:

```text
develop → active Development continuation
Local   → verified operating-system milestone
main    → stable repository history
```

## Locked generation architecture

```text
MULTIVIEW (preferred)
front / right / back / left
→ Hunyuan3D-2mv
→ model.glb

SINGLE CANONICAL IMAGE
front OR right OR back OR left
→ Hunyuan3D-2mv
→ model.glb

TEXT
→ HunyuanDiT v1.2 Distilled Lite
→ reference_front.png
→ USER REVIEW / APPROVAL
→ Hunyuan3D-2mv
→ model.glb
```

Hunyuan3D-2mv remains the **only 3D provider**. HunyuanDiT is an auxiliary 2D reference generator used only for text input.

Do not independently generate four T2I views for text mode.

## Implemented repository runners

```text
kits/lazy-builder/generation/generate_text_reference.py
kits/lazy-builder/generation/generate_shape.py
```

Text and shape are separate processes so the 8 GB GPU does not need both models resident at the same time.

Current shape baseline:

```text
model_path: tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
steps: 30
guidance: 7.5
octree_resolution: 256
num_chunks: 20000
seed: 12345
texture: OFF
```

Current text-reference baseline:

```text
model: Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers-Distilled
official Lite runner
seed: 42
steps: 50
guidance: 6
```

## Next Step — local generation runtime proof

Use `local` mode. Do not claim runtime success from repository CI.

### 1. Local preflight

Record:

```text
OS
GPU / VRAM
NVIDIA driver
Python version(s)
CUDA/PyTorch versions
free system RAM/disk
```

### 2. Prove text-reference stage

Set up/use the official Tencent-Hunyuan/HunyuanDiT Lite environment.

Run one bounded prompt through:

```text
generate_text_reference.py
→ reference_front.png
```

Record peak VRAM and verify the image is usable as a front reference.

### 3. Review gate

Do not continue to 3D automatically. Inspect/approve the generated reference first.

### 4. Prove Hunyuan3D-2mv shape stage

Set up/use the official Hunyuan3D-2 environment separately from Blender Python.

First test:

```text
one approved front image
→ generate_shape.py
→ model.glb
```

Then test a consistent multiview set when available.

Record:

```text
model/subfolder
parameters
peak VRAM
runtime
GLB opens correctly
major geometry defects
```

### 5. Compare only what matters

Do not tune variants/providers yet. First answer:

```text
Does the standard Hunyuan3D-2mv baseline run reliably on RTX 3070 8 GB?
Does the generated geometry preserve the reference well enough for Minecraft discretization?
```

## M1 runtime remains pending

Still required before M1 can be called end-to-end PASS:

```text
Axiom 5.3.0 import
Clipboard
AxiomPaper 5.0.1 handshake/placement
Minecraft BlockState verification
```

This pending proof remains visible; do not silently mark it complete.

## Stop Boundary

Do not automatically:

- add Hunyuan3D-2 base / Tripo / TRELLIS / Pixal3D;
- add Fast/Turbo model routing;
- auto-generate four text views;
- enable texture generation;
- integrate Hunyuan into Blender Python;
- implement Minecraftize before the first local GLB proof;
- add MCP/API-server orchestration;
- promote `develop` to `Local` or `Local` to `main`.
