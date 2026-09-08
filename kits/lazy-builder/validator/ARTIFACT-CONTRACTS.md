# Artifact Contracts

Every stage boundary must be stronger than “file exists and is non-empty”.

`artifact_validation.py` validates machine-readable contracts before a stage can become `PASS`.

## Canonical artifacts

```text
00-preflight/environment.json
10-reference/reference_front.png + manifest.json
19/20/21-shape-*/model.glb + manifest.json
30-blender/target.blend + target.json
40-minecraftize-primitives/blocks.json + report.json
41-minecraftize-model/blocks.json + report.json
45-preview/preview.svg + manifest.json
50-schematic/build.schem + manifest.json
60-axiom/runtime.json
```

## Preflight

Preflight is fail-closed. PASS requires more than declared strings:

```text
required runtime packages installed
Git + Blender executable paths available
installed generation API signatures compatible
actual imported hy3dgen checkout == pinned clean commit
required machine/Axiom/Paper facts populated
Axiom/AxiomPaper hashes syntactically valid
pinned source/model identities exact
```

No inference application is launched during this check.

## Text reference

The manifest binds:

```text
HunyuanDiTPipeline
exact HunyuanDiT model + revision
resolved prompt + deterministic parameters
reference_front.png SHA-256
```

Text reference is human-gated. It must transition:

```text
RUNNING → APPROVAL_REQUIRED → PASS
```

## Shape generation

Each shape manifest must bind:

```text
model ID + revision + subfolder
expected Hunyuan source repo/commit
actual imported clean source checkout path + commit
named input paths + SHA-256
explicit extraction settings
positive mesh vertex/face counts
output GLB SHA-256
```

Input files are re-hashed when the stage artifact is validated.

## Intentional case-input changes

Session initialization snapshots T1/I1/I2. Unexpected drift stops execution.

When a case input intentionally changes, use:

```text
refresh_case_input.py
→ validate changed source exists
→ replace only that authoritative case snapshot digest
→ invalidate its first owner + true downstream dependents
→ resume
```

Simply invalidating a stage does **not** silently redefine the original case snapshot.

## Blender

`target.json` binds source/target hashes, selected shape stage, Blender version, `LazyBuilderTarget`, target width, canonical orientation, cleanup notes, and finite positive world bounds.

NaN/Infinity, zero-size axes, inverted bounds, missing source GLB, or mutated `target.blend` are rejected.

## Minecraftize

`blocks.json` passes canonical block-model validation.

Representative V0 report must agree with canonical output:

```text
occupied_cells == block_count
grid_minecraft_axes == bounds.size
full_block == SUPPORTED
stair/slab == SKIPPED
```

Primitive report must bind its emitted blocks to the 5×5×5 true-interior proof and keep stair/slab `SKIPPED`.

## Preview

`preview.svg` derives from the exact canonical `blocks.json`. Validation recomputes source hash and requires preview manifest block count/bounds to equal actual source metadata.

Preview is also human-gated:

```text
RUNNING → APPROVAL_REQUIRED → PASS
```

Schematic export cannot unlock from an unapproved preview.

## Schematic

The writer reloads and checks **every source block state** after save.

To avoid duplicating production-size block data in the manifest, evidence records:

```text
round_trip_verified_block_count == source block_count
bounded deterministic diagnostic samples (max 64)
source hash / output hash / bounds / writer / version
```

Verification remains exhaustive even though diagnostic samples are bounded.

## Axiom/Paper/Minecraft

`write_runtime_evidence.py` creates `runtime.json` from actual observations and binds:

```text
exact build.schem path + SHA-256
exact environment.json path + SHA-256
import
clipboard
placement
minecraft_world
visual_state
```

PASS requires all five checks PASS. The session controller additionally requires runtime evidence hashes to equal the already-recorded PASS digests for that session’s schematic and preflight environment.

This prevents a different schematic/environment from being presented as acceptance evidence.

## Digest rule

Before a downstream stage starts:

```text
current input digest
== authoritative case snapshot or upstream PASS digest
```

A mismatch is `INPUT_DRIFT`, never a silent update.
