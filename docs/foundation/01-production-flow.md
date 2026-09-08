# Production Flow

LazyBuilder product Flow is separate from agent work modes (Plan / Production Execution / Development / Maintenance).

## Canonical sequence

```text
Flow 1  Repository Boot & Project Memory
Flow 2  Reference Intake & Multi-view Recovery
Flow 3  Hunyuan3D-2mv Shape Generation
Flow 4  Blender Target Preparation
Flow 5  Minecraftize Conversion
Flow 6  Schematic Validation & Axiom Handoff
```

## Flow 1 — repository/project continuity

Recover current repository rules and active project state before repeating questions or restarting completed work.

## Flow 2 — reference intake

Establish the actual reference set, intended object/build, known dimensions/scale constraints, and material conflicts. Prefer consistent front/right/back/left views when available.

## Flow 3 — shape generation

Use Hunyuan3D-2mv only. Run shape generation in its own environment and produce a GLB. Texture generation is not required for the Minecraft MVP.

## Flow 4 — Blender preparation

Import GLB and perform only cleanup that materially improves downstream conversion: orientation, scale, severe floating/noisy geometry, and obvious structural distortion.

## Flow 5 — Minecraftize

Convert target mesh to Minecraft block placement incrementally:

```text
occupancy/full blocks
→ stairs
→ slabs
→ only then additional block families from proven use cases
```

Preview before export.

## Flow 6 — schematic / handoff

Serialize valid Minecraft BlockStates through the existing writer, load `.schem` in Axiom, and distinguish static/file validity from actual Axiom/Minecraft runtime proof.

## Revision rule

A bounded change returns to the **first affected Flow owner**, then reruns only downstream work actually invalidated by that change.

Examples:

```text
new reference dimension only
→ Flow 2
→ regenerate affected downstream target/output

GLB correct, Blender orientation wrong
→ Flow 4

Blender target correct, roof still cube-stepped
→ Flow 5

Minecraft block model correct, file won't open in Axiom
→ Flow 6
```

Do not restart from Flow 2 for a bounded downstream defect.
