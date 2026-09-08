# Hunyuan3D-2mv Generation Policy

Flow 3 uses **Hunyuan3D-2mv as the only active 3D generation provider** for the MVP.

## Purpose

Hunyuan creates a geometric draft/hypothesis from multi-view reference images. It does not produce the final Minecraft representation.

## Runtime boundary

- run Hunyuan in an environment separate from Blender's Python;
- use shape generation as the required path;
- texture generation is optional and normally off for Minecraft conversion;
- `low_vram_mode` may be used when needed on the target RTX 3070 8 GB development device;
- output is a GLB/trimesh-compatible mesh imported into Blender.

## Fidelity rule

If output is poor, diagnose in this order before adding another model provider:

1. reference inconsistency/missing geometry;
2. generation setup/parameters;
3. bounded Blender cleanup feasibility;
4. whether the failure actually matters after Minecraft discretization.

Do not introduce a parallel model router merely because a generation is imperfect.

## Evidence

Repository docs cannot prove Hunyuan runtime success or geometry quality. Those require local generation evidence.

Detailed procedure: `kits/lazy-builder/generation/HUNYUAN3D-2MV.md`.
