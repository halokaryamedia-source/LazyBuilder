# Single Hunyuan Provider Decision

Status: current

## Context

Several image-to-3D models were researched. Multi-provider routing would increase setup, GPU/runtime branching, maintenance, and debugging before the Minecraft conversion path has even been proven.

The development device is an RTX 3070 8 GB and the target use case prioritizes multi-view shape consistency over texture generation.

## Decision

Use **Hunyuan3D-2mv as the only active 3D generation provider for MVP**.

```text
front / right / back / left
→ Hunyuan3D-2mv
→ shape-only GLB
→ Blender
```

Texture generation is not required for the Minecraft MVP. Use low-VRAM mode when required by the local environment.

## Why

- multi-view input directly matches the desired precision goal;
- one provider keeps runtime setup and debugging bounded;
- Minecraft material/block selection will replace AI texture anyway;
- the project should prove Minecraft conversion before optimizing model-provider choice.

## Not chosen

- Tripo;
- TRELLIS/TRELLIS.2;
- Pixal3D;
- model router/fallback chain;
- custom 3D foundation model training.

These are not active backlog simply because they exist. Reassessment requires a demonstrated Hunyuan failure that cannot be handled more simply.

## Evidence boundary

Repository policy does not prove local Hunyuan runtime or generation quality. Those require actual GPU execution.

## Follow-up owner

`kits/lazy-builder/generation/HUNYUAN3D-2MV.md`.
