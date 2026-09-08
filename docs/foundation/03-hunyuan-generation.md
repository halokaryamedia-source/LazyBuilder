# Hunyuan3D-2mv Generation Policy

Flow 3 uses **Hunyuan3D-2mv as the only active 3D generation provider** for MVP.

## Input boundary

```text
T1 approved HunyuanDiT front reference ─┐
I1 one canonical image ─────────────────┼→ Hunyuan3D-2mv → shape-only GLB
I2 front/right/back/left ───────────────┘
```

Text input belongs to Flow 2 and first becomes one reviewable canonical front reference. HunyuanDiT is not a 3D provider.

## Reproducibility boundary

Generation runtime must use the exact upstream source/model revisions owned by:

`kits/lazy-builder/generation/ENVIRONMENT.md`

Manifests record those pins plus input/output SHA-256.

## First runtime baseline

```text
model: tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
texture: OFF
```

The profile is intentionally bounded for RTX 3070 8 GB first proof and is not yet a measured optimum.

Fast/Turbo are not automatically routed.

## Runtime boundary

- keep generation outside Blender Python;
- text-reference and shape processes are separate;
- shape-only generation;
- background removal by default;
- output `model.glb` + reproducibility `manifest.json`;
- do not claim CUDA/VRAM/quality success from static CI.

## Fidelity diagnosis order

1. reference consistency / missing geometry;
2. pinned generation environment/configuration;
3. bounded Blender cleanup vs regeneration;
4. whether the defect materially survives Minecraft discretization;
5. only then consider a measured variant experiment.

Do not add a second 3D provider merely because one generation is imperfect.
