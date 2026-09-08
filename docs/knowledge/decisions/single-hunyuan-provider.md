# Single Hunyuan Provider Decision

Status: current

## Context

Multi-provider 3D routing would increase setup, GPU/runtime branching, maintenance, and debugging before the Minecraft conversion path is proven. The target development device is an RTX 3070 8 GB and the use case prioritizes shape consistency over AI texture.

The product now accepts either image references or text intent. Text input does not change the one-provider 3D decision.

## Decision

Use **Hunyuan3D-2mv as the only active 3D generation provider for MVP**.

Image path:

```text
front / right / back / left
→ Hunyuan3D-2mv
→ shape-only GLB
→ Blender
```

Text path:

```text
text intent
→ Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
→ one reviewable front reference
→ user approval
→ Hunyuan3D-2mv
→ shape-only GLB
→ Blender
```

HunyuanDiT is an auxiliary **2D reference generator**, not a second 3D provider.

## Why

- Hunyuan3D-2mv directly supports named multiview shape conditioning;
- one 3D provider keeps runtime setup/debugging bounded;
- text intent can enter the same shape path through a reviewable 2D hypothesis;
- Minecraft material/block selection replaces AI texture anyway;
- the project should prove conversion and runtime quality before optimizing provider/variant choice.

## Variant boundary

The Hunyuan3D-2mv repository also provides Fast and Turbo subfolders. They are variants of the same provider, but MVP does not auto-route them.

Start with:

```text
tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
```

Reassess Fast/Turbo only from controlled same-reference evidence and downstream Minecraft usefulness.

## Not chosen

- Tripo;
- TRELLIS/TRELLIS.2;
- Pixal3D;
- Hunyuan3D-2 base as a parallel provider;
- model router/fallback chain;
- independently generated four-view T2I routing;
- custom 3D foundation model training;
- Hunyuan texture generation for MVP.

These are not active backlog merely because they exist.

## Hardware boundary

Text-reference and shape generation run as separate processes. The system must not require HunyuanDiT and Hunyuan3D-2mv to remain resident in the RTX 3070 8 GB VRAM simultaneously.

## Evidence boundary

Repository policy and CI can prove model IDs, input routing, and static defaults. Local GPU execution is required to prove CUDA compatibility, VRAM use, generation quality, runtime, and GLB usability.

## Follow-up owners

- `docs/knowledge/decisions/text-image-to-3d-input-contract.md`
- `kits/lazy-builder/generation/HUNYUAN3D-2MV.md`
