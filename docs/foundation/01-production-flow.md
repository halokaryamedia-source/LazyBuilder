# Production Flow

LazyBuilder product Flow is separate from agent work modes (Plan / Production Execution / Development / Maintenance).

## Canonical sequence

```text
Flow 1  Repository Boot & Project Memory
Flow 2  T1/I1/I2 Reference Intake
Flow 3  Hunyuan Shape Generation
Flow 4  Representative Selection + Blender Target Preparation
Flow 5  Minecraftize Conversion + Canonical Preview
Flow 6  Schematic Validation + Axiom/Minecraft Handoff
```

## Flow 1 — repository/project continuity

Recover current repository rules and active project state before repeating questions or restarting completed work.

## Flow 2 — reference intake

Three explicit input paths:

```text
T1 TEXT
I1 SINGLE IMAGE
I2 MULTIVIEW front/right/back/left
```

T1 first produces one canonical reviewable front reference through the pinned HunyuanDiT path. It becomes usable for shape generation only after approval.

Case inputs are SHA-256 snapshotted before a runtime acceptance session. Changed inputs require explicit invalidation rather than silent replacement.

## Flow 3 — shape generation

Use pinned Hunyuan3D-2mv only. Each T1/I1/I2 shape path produces:

```text
model.glb
manifest.json
```

The manifest binds source/model revision, named-view hashes, parameters, mesh counts, and output hash.

Generated meshes are geometric hypotheses, not final product authority.

## Flow 4 — representative selection + Blender

Compare the three shape paths and select exactly one representative GLB for downstream conversion.

Prepare:

```text
LazyBuilderTarget
target.blend
target.json
```

`target.json` binds selected source digest, Blender version, orientation, target scale/bounds, cleanup notes, and exact target file digest.

Changing the selected GLB invalidates Blender and its true downstream stages.

## Flow 5 — Minecraftize + preview

Minecraftize owns geometry-to-block decisions.

V0:

```text
prepared mesh
→ occupancy/full blocks
→ canonical blocks.json
```

Stairs/slabs remain `SKIPPED` until V0 runtime evidence justifies the next implementation step.

Canonical preview is derived from the exact block model:

```text
blocks.json
→ preview.svg
```

Preview is evidence, not a second conversion path.

## Flow 6 — schematic / handoff

```text
blocks.json
→ mcschematic==11.4.4
→ Sponge V2 / DataVersion 4189 build.schem
→ Axiom client import / Clipboard / Placement
→ AxiomPaper / Paper
→ Minecraft Java
```

The schematic writer serializes Minecraftize output; it does not repair geometry.

## Pre-Runtime Verification

Before any controlled runtime acceptance test, the repository verifies:

```text
source/model pins
session dependency/resume graph
input and upstream artifact digest locks
artifact schemas
Blender target metadata schema
Minecraftize pure/static contracts
primitive suite definition
canonical preview generation from blocks.json
schematic writer round-trip
acceptance evidence structure
```

Pre-Runtime Verification does not launch Hunyuan GPU generation, Blender conversion, Axiom, Paper, or Minecraft.

## Runtime Acceptance session

When the user explicitly starts testing:

```text
preflight once
→ T1/I1/I2 generation
→ representative selection
→ Blender target
→ prepared primitive runtime suite
→ representative Minecraftize conversion
→ canonical preview
→ schematic export
→ Axiom/Clipboard/Placement
→ Minecraft verification
→ consolidated report
```

A failure resumes from the first invalidated owner rather than restarting independent upstream work.

## True dependency rule

Dependencies must reflect actual ownership.

Example:

```text
minecraftize_primitives
→ depends on preflight/runtime environment
→ does NOT depend on representative target.blend
```

Therefore changing the representative GLB must not throw away an independent valid primitive proof.

## Revision rule

```text
reference/input changed
→ Flow 2

generation wrong with unchanged references
→ Flow 3

representative selection / Blender target wrong
→ Flow 4

block model wrong
→ Flow 5

blocks.json correct but preview wrong
→ Flow 5 preview owner

blocks.json correct but .schem wrong
→ Flow 6 exporter

Axiom/Paper/Minecraft runtime problem
→ Flow 6 runtime owner
```

Invalidate only true dependents.
