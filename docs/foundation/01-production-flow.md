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

Text input may first produce one canonical reviewable reference through the locked HunyuanDiT text-reference path. A generated text reference does not become authoritative until the required user review/approval gate passes.

## Flow 3 — shape generation

Use Hunyuan3D-2mv only. Run shape generation in its own environment and produce a GLB. Texture generation is not required for the Minecraft MVP.

The generated mesh is a geometric hypothesis. Preserve exact input/model/parameter provenance so later Blender/Minecraftize results can be traced to the source generation.

## Flow 4 — Blender preparation

Import GLB and perform only cleanup that materially improves downstream conversion: orientation, scale, severe floating/noisy geometry, and obvious structural distortion.

Normalize the target to the canonical LazyBuilder front/up and target-dimension contract before Minecraftize samples it. Keep the raw imported source recoverable and use a separate prepared target.

## Flow 5 — Minecraftize

Convert target mesh to Minecraft block placement incrementally:

```text
occupancy/full blocks
→ stairs
→ slabs
→ only then additional block families from proven use cases
```

Minecraftize owns geometry-to-block decisions. It emits one canonical deterministic block model used by both preview and schematic export.

Preview before export.

## Flow 6 — schematic / handoff

Serialize valid Minecraft BlockStates through the existing writer, load `.schem` in Axiom, and distinguish static/file validity from actual Axiom/Minecraft runtime proof.

The schematic writer serializes Minecraftize output; it does not repair conversion logic.

## Unified acceptance policy

Design and deterministic/static implementation may progress across Flow 2–6 before local runtime proof begins.

The first local runtime effort should be one prepared acceptance session rather than disconnected stage-by-stage experiments.

Before runtime execution, the test-readiness contract must define:

```text
fixed test cases
+ one run/session layout
+ stage inputs/outputs
+ artifact/manifests
+ human gates
+ acceptance criteria
+ failure ownership
+ resume semantics
+ final evidence report
```

Canonical detailed owner:

`../../kits/lazy-builder/validator/TEST-READINESS.md`

Static/CI checks may run before the local session, but they do not upgrade GPU, Blender, Axiom, Paper, or Minecraft claims to runtime PASS.

## Runtime session shape

The intended first local session covers the chain coherently:

```text
preflight once
→ text/single/multiview generation coverage
→ select representative GLB
→ Blender target preparation
→ Minecraftize primitive batch
→ representative Minecraftize conversion
→ schematic export
→ Axiom/Clipboard/Placement
→ Minecraft world verification
→ consolidated report
```

Successful upstream evidence is preserved. A failure resumes from the first invalidated Flow rather than restarting everything by default.

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

During the unified acceptance session, the same rule becomes resume behavior:

```text
record failure
→ fix first wrong owner
→ invalidate only dependent outputs
→ resume from first invalidated Flow
```
