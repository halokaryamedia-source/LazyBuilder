# Minecraftize Conversion Policy

Flow 5 is LazyBuilder's custom deterministic conversion core.

## Objective

Convert a prepared Blender target into one canonical Minecraft Java block model while adding Minecraft-native geometry only when simpler evidence has been proven first.

## Incremental contract

### V0 — full-block baseline — implemented, runtime proof pending

```text
LazyBuilderTarget
→ Blender evaluated geometry + BVH occupancy
→ full-block baseline
→ canonical blocks.json
```

V0 must prove scale, axes, occupancy, tight bounds, determinism, preview lineage, and schematic handoff before block-family refinement begins.

Current feature status:

```text
full_block → SUPPORTED by implementation
stair      → SKIPPED
slab       → SKIPPED
```

### V1 — stairs — future after V0 runtime evidence

Use valid stair BlockStates where a prepared surface is materially better represented by stairs than full cubes.

Minimum vocabulary when implemented:

```text
facing=north|south|east|west
half=top|bottom
shape=straight|inner_left|inner_right|outer_left|outer_right
```

Do not implement or claim stair support before V0 Runtime Acceptance establishes the full-block baseline.

### V2 — slabs — future after stable stairs/full blocks

Use top/bottom slab states for proven half-height/shallow-contour cases.

```text
type=top|bottom|double
```

### Later block families

`wall`, `fence`, `glass pane`, `trapdoor`, `iron bars`, doors, decorative blocks, NBT/block entities, and other families are added only when representative runtime evidence demonstrates a concrete need and a deterministic primitive contract can define correctness.

## Primitive proof rule

The prepared V0 Blender runtime suite contains:

```text
3×2×2 boundary box
5×5×5 true-interior box
```

The second case requires non-surface/interior occupancy evidence. This prevents a primitive PASS that is satisfied only by the converter's near-surface band.

Static CI may compile the suite but cannot mark Blender execution PASS.

## Canonical preview rule

Preview is derived from the exact final block model:

```text
blocks.json
→ build_preview.py
→ preview.svg + manifest.json
```

Current deterministic preview provides top/front/right block projections and binds the source/output SHA-256.

```text
                  blocks.json
                   /       \
             preview.svg   build.schem
```

Preview is **not** a second approximate conversion path. If preview coordinates disagree with `blocks.json`, the preview owner is wrong.

A richer prepared-mesh overlay may be added later only if representative runtime diagnosis proves it materially useful; it is not required to make V0 pre-runtime-ready.

## Source-of-truth rule

Do not hand-patch an exported `.schem` in Axiom to hide a conversion defect.

```text
wrong blocks.json → Minecraftize owner
correct blocks.json + wrong preview → preview owner
correct blocks.json + wrong .schem → exporter owner
```

Axiom polish remains downstream user work, not an engine correction.

Detailed owner: `kits/lazy-builder/minecraftize/CONTRACT.md`.
