# Minecraftize Conversion Policy

Flow 5 is LazyBuilder's custom technical core.

## Objective

Convert Blender target geometry into Minecraft Java block placement while progressively using Minecraft-native geometry rather than full-cube voxelization only.

## Incremental contract

### V0 — full-block baseline

Prove mesh sampling, Minecraft grid scale, occupancy, preview, and schematic export end-to-end.

### V1 — stairs

Use valid stair BlockStates where the target surface is better represented by a stair than a full cube.

Minimum state vocabulary:

```text
facing=north|south|east|west
half=top|bottom
shape=straight|inner_left|inner_right|outer_left|outer_right
```

### V1 — slabs

Use top/bottom slab states for half-height/shallow contour cases.

```text
type=top|bottom|double
```

### Later block families

`wall`, `fence`, `glass pane`, `trapdoor`, `iron bars`, doors, and decorative blocks are added only when a real test build proves that full/stair/slab cannot represent the required geometry satisfactorily.

## Development rule

Begin rule-based:

```text
solid/interior cell  → full block
45°-like surface     → stair candidate
half-height contour  → slab candidate
```

Add scoring/optimizer complexity only after primitive and real-building tests expose a concrete failure class.

## Preview rule

Before export, support enough preview to compare:

```text
Original Mesh
Minecraft Preview
Original + Minecraft Overlay
```

## Source-of-truth rule

When validating LazyBuilder, fix conversion logic rather than hand-patching the exported `.schem` in Axiom. Axiom polish is downstream user work, not an engine fix.

Detailed owner: `kits/lazy-builder/minecraftize/CONTRACT.md`.
