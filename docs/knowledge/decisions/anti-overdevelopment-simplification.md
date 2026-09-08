# Anti-Overdevelopment Simplification Decision

Status: current

## Context

LazyBuilder research exposed many possible components: multiple 3D providers, MCP, semantic scene graphs, custom renderers, inverse-meshing optimizers, learned Minecraft priors, palette systems, and direct game integration. Building them before proving the basic pipeline would create complexity without a validated result.

## Decision

Prefer the simplest chain that produces falsifiable progress:

```text
reference
→ Hunyuan3D-2mv
→ Blender
→ Minecraftize
→ mcschematic
→ Axiom
```

### Keep for MVP

- one generation provider;
- one Blender workbench;
- one custom conversion core;
- one schematic writer;
- one final Axiom handoff;
- full-block → stair → slab progression;
- targeted primitive/build tests;
- minimum repository/promotion verification.

### Do not expand into

- provider routers/fallback orchestration;
- MCP automation before manual workflow works;
- custom ML/foundation model training;
- generic dependency/registry frameworks;
- custom renderer before preview need is proven;
- custom NBT/schematic serializer while existing writer works;
- every possible Minecraft block family up front;
- speculative compatibility layers;
- more CI/proof layers merely because they are possible.

A new subsystem requires at least one of:

1. a reproduced defect current stack cannot solve simply;
2. a measured quality bottleneck;
3. a measured performance bottleneck;
4. an approved next milestone that directly requires it.

## Proof rule

Use the cheapest check that can falsify the current boundary. Once evidence is sufficient, stop.

`No change required` is a valid and preferred result when remaining risk is theoretical.
