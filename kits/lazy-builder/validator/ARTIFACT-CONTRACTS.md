# Artifact Contracts

Every stage boundary must be stronger than “file exists and is non-empty”.

`artifact_validation.py` validates the machine-readable contract when a stage is marked `PASS`.

## Canonical stage artifacts

```text
00-preflight/
  environment.json

10-reference/
  reference_front.png
  manifest.json

19/20/21-shape-*/
  model.glb
  manifest.json

30-blender/
  target.blend
  target.json

40-minecraftize-primitives/
  blocks.json
  report.json

41-minecraftize-model/
  blocks.json
  report.json

45-preview/
  preview.svg
  manifest.json

50-schematic/
  build.schem
  manifest.json

60-axiom/
  runtime.json
```

## Validation rules

### Preflight

`environment.json` records automatic system/package discovery plus exact declared runtime facts. Required declared fields may not be silently omitted or guessed.

Pinned generation identities (`hunyuan3d_source_commit`, `hunyuan3d_model_revision`, `hunyuandit_model_revision`) are auto-recorded from the repository contract; machine-specific facts remain explicit.

### Text reference

The manifest records exact HunyuanDiT model ID + revision and the generated image SHA-256. Approval remains a separate human gate.

### Shape generation

Each shape manifest records:

```text
model ID
model revision
Hunyuan3D source repository + commit
named input views + SHA-256
parameters
mesh counts
output GLB SHA-256
```

### Blender

`target.json` binds the selected source GLB to the exact `target.blend` and records:

```text
source path + SHA-256 + selected shape stage
Blender version
LazyBuilderTarget object name
target_width_blocks
world bounds
canonical axis mapping
cleanup notes
target.blend SHA-256
```

### Minecraftize

`blocks.json` must pass the canonical block-model validator. V0 reports must explicitly keep stair/slab `SKIPPED`.

The primitive report must contain both:

```text
3×2×2 boundary case
5×5×5 true-interior case
```

The 5×5×5 case exists so the primitive suite cannot pass only from near-surface occupancy.

### Preview

`preview.svg` is derived from the exact canonical `blocks.json`. Its manifest binds source and output SHA-256. Preview is evidence; it is not a second converter.

### Schematic

The writer manifest binds the exact source blocks, output `.schem` SHA-256, Sponge V2, DataVersion 4189, and writer round-trip result.

### Axiom/Minecraft runtime

`runtime.json` may validate as `PASS` only after exact Axiom import, Clipboard, placement, Minecraft world placement, and visual-state checks all pass.

## Digest rule

The session records SHA-256 at every successful boundary.

Before a downstream stage starts:

```text
current input digest
== authoritative case snapshot or upstream PASS digest
```

A mismatch is `INPUT_DRIFT`; the owner must be invalidated explicitly rather than silently consuming changed data.
