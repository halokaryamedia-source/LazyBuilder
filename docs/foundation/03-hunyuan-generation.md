# Hunyuan3D-2mv Generation Policy

Flow 3 uses **Hunyuan3D-2mv as the only active 3D generation provider** for MVP.

## Input boundary

Flow 3 receives images only:

```text
front / right / back / left
→ Hunyuan3D-2mv
→ shape-only GLB
```

At least one named view is required; four consistent views are preferred when available.

Text input belongs to Flow 2 and is first converted into a reviewable canonical front reference with `Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled`. HunyuanDiT is not a 3D provider.

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

The initial `num_chunks=8000` profile is intentionally bounded for RTX 3070 8 GB proof. It is not yet a proven quality/performance optimum.

Fast/Turbo subfolders are not automatically routed. First prove the standard baseline; compare variants only if measured runtime/output evidence justifies it.

## Runtime boundary

- keep generation outside Blender Python;
- text-reference and shape stages run as separate processes;
- use shape-only generation;
- remove background by default using the Hunyuan helper unless the source already has a deliberate usable alpha/background;
- output is `model.glb` plus a reproducibility manifest.

## Fidelity rule

If output is poor, diagnose in this order before adding another model provider:

1. reference consistency / missing geometry;
2. generation runtime/configuration;
3. whether bounded Blender cleanup is cheaper than regeneration;
4. whether the defect materially survives Minecraft discretization.

Do not introduce another 3D provider or automatic model router merely because one generation is imperfect.

## Evidence

Repository/CI checks prove configuration/routing only. CUDA compatibility, VRAM use, mesh quality, and GLB compatibility require actual `local` runtime proof.

Detailed procedure: `kits/lazy-builder/generation/HUNYUAN3D-2MV.md`.
