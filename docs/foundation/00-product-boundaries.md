# Product Boundaries

LazyBuilder has one product goal:

> Convert non-Minecraft visual references into a Minecraft Java `.schem` that can be loaded in Axiom, while progressively using Minecraft-native block shapes instead of remaining a full-cube voxelizer.

## In scope for MVP

```text
multi-view images
→ Hunyuan3D-2mv
→ GLB
→ Blender
→ Minecraftize
→ .schem
→ Axiom
```

Active tool boundary:

- one 3D provider: Hunyuan3D-2mv;
- Blender 5.2.x LTS as 3D workbench;
- custom `Minecraftize` conversion core;
- `mcschematic` as file writer while sufficient;
- Axiom as external final import/edit/placement tool;
- Minecraft Java Edition target.

## Minecraftize growth boundary

```text
V0 → full blocks
V1 → stairs
V1 → slabs
later → wall / fence / glass pane only from real use cases
later → additional decorative/partial blocks only from demonstrated need
```

Rule-based geometry comes before a complex optimizer or ML solver.

## Explicitly out of MVP

- MCP automation;
- multi-model routing;
- Tripo / TRELLIS / Pixal3D as parallel providers;
- custom foundation model training;
- direct Axiom automation;
- direct Minecraft world injection;
- custom schematic/NBT format;
- modded-block support;
- broad architecture-semantic engine;
- speculative compatibility frameworks.

A future capability enters scope only when a demonstrated product defect, measured bottleneck, or approved milestone requires it.

## Authority boundary

Reference images and current user decisions remain upstream authority. Hunyuan meshes, Blender targets, Minecraft previews, schematics, and Axiom placements are downstream representations/evidence.

A downstream artifact never silently repairs or redefines upstream intent.
