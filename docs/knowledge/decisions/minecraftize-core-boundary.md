# Minecraftize Core Boundary Decision

Status: current

## Context

Image/multi-view to 3D and schematic writing already have existing tools. The unsolved product value is turning Blender target geometry into a Minecraft-native structure rather than a crude full-cube voxel model.

## Decision

Custom product development concentrates on **Minecraftize**.

```text
Hunyuan3D-2mv   → reuse
Blender          → reuse as workbench
Minecraftize     → custom core
mcschematic      → reuse as writer while sufficient
Axiom            → reuse as final external editor/placement tool
```

Minecraftize grows incrementally:

```text
full-block occupancy
→ stair fitting
→ slab fitting
→ extra block families only from demonstrated build needs
```

Begin rule-based. A scoring optimizer, semantic architecture system, or ML solver is introduced only when actual tests prove simple rules insufficient.

## Why

This puts engineering effort at the exact gap existing tools do not solve well while preserving a short path to a real `.schem` result.

## Not chosen

- custom 3D editor;
- custom schematic/NBT implementation by default;
- direct Axiom automation;
- broad block database/framework before basic conversion works;
- architecture-generation framework before first real building proof.

## Evidence boundary

The first success criterion is end-to-end functionality, not theoretical solver completeness.

## Follow-up owner

`kits/lazy-builder/minecraftize/CONTRACT.md` and the future addon source once implemented.
