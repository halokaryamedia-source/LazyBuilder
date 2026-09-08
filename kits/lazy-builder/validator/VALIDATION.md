# Validation and Handoff

## Proof layers

```text
0 Pre-Runtime Verification (static/source/contracts)
1 validated runtime environment capture
2 generation + Blender/Minecraftize primitive runtime
3 representative Minecraftize + approved canonical preview
4 schematic writer / schema compatibility
5 Axiom client import + Clipboard
6 AxiomPaper handshake / placement
7 Minecraft world placement + visual fidelity
```

A lower layer never proves a higher layer.

## Current runtime target

```text
Minecraft Java 1.21.4
Fabric client
Axiom 5.3.0 / API family 9
Paper 1.21.4
AxiomPaper 5.0.1+1.21.4 / API family 9
Sponge Schematic V2 / DataVersion 4189
```

AxiomPaper 4.0.4 is outside this baseline. AxiomPaper 5.0.4+1.21.4 remains only a conditional upgrade candidate after measured evidence.

## Preflight capture is fail-closed

Before future runtime, run the session-provided `collect_environment.py` command and supply all required declared facts.

The collector does **not** launch inference or Blender. It records:

```text
OS / Python
installed runtime package versions
Git / Blender / Java executable paths
actual imported hy3dgen checkout path / commit / dirty state
installed generation API signature compatibility
Blender/GPU/VRAM/CUDA facts
Minecraft/Fabric/Axiom/Paper/AxiomPaper facts + hashes
integration/plugin state
pinned model/source identities
```

A preflight can become PASS only if required packages/executables exist, generation APIs match wrapper expectations, and the actual imported Hunyuan checkout is the clean pinned source commit.

If package, driver, Blender, Hunyuan source, or Axiom/Paper environment changes after preflight, invalidate and capture preflight again.

## Generation acceptance

T1 uses the pinned distilled HunyuanDiT with native `HunyuanDiTPipeline` and 25-step baseline. Text reference requires:

```text
RUNNING → APPROVAL_REQUIRED → PASS
```

T1/I1/I2 shape generation requires the exact Hunyuan3D source/model pins and explicit extraction settings in `generation/ENVIRONMENT.md`.

The shape runner rejects source commit mismatch, dirty source checkout, missing/empty mesh, and records actual source/input/output lineage.

Intentional case-input changes must use `refresh_case_input.py`; unexpected changes remain `INPUT_DRIFT`.

## Blender acceptance

Selected GLB:

```text
→ Blender preparation
→ LazyBuilderTarget
→ target.blend
→ target.json via write_target_metadata.py
```

`target.json` must bind source/target hashes, Blender version, target width, finite positive world bounds, canonical orientation, and cleanup notes.

## Minecraftize acceptance

Primitive runtime executes the real Blender V0 converter:

```text
3×2×2 boundary
5×5×5 true interior
```

Representative V0 must agree across report and canonical `blocks.json`:

```text
occupied cell count
grid/bounds size
full block support
stair/slab SKIPPED
```

## Canonical preview approval

```text
blocks.json
→ build_preview.py
→ preview.svg + manifest.json
```

Preview metadata is validated against the exact source blocks. The preview stage must transition:

```text
RUNNING → APPROVAL_REQUIRED → PASS
```

Schematic export remains locked until that preview is approved.

## Schematic writer acceptance

```text
canonical blocks.json
→ mcschematic==11.4.4
→ build.schem
→ reload same file
→ verify every source coordinate + BlockState
```

The manifest stores total verified count plus at most 64 deterministic diagnostic samples, avoiding an unnecessary O(N) duplicate of a production block model while retaining exhaustive verification.

## Exact Axiom/Paper/Minecraft evidence

Use the exact session outputs. After actual observations, create runtime evidence with:

```bash
python kits/lazy-builder/validator/write_runtime_evidence.py \
  --schematic <run>/50-schematic/build.schem \
  --environment <run>/00-preflight/environment.json \
  --output <run>/60-axiom/runtime.json \
  --import PASS \
  --clipboard PASS \
  --placement PASS \
  --minecraft-world PASS \
  --visual-state PASS
```

Use `FAIL` for any failed observation. The helper sets overall PASS only when all checks pass.

`runtime.json` records SHA-256 for the exact schematic and environment. When the Axiom stage is marked PASS, the session controller compares both hashes with the already-recorded session PASS digests. Evidence from another build/environment is rejected.

## Axiom diagnosis

For the first controlled multiplayer proof use the expected OP/permission setup. Reconnect after permission changes when required.

If Axiom is inactive:

```text
/whynoaxiom
/axiomhandshake
```

Import requires the server-provided import capability / `axiom.can_import_blocks` permission.

Failure routing:

```text
Import menu disabled → permission/session/handshake
unknown schematic → schematic compatibility
Clipboard wrong → client parsing/content
Placement blocked → Axiom permission/restriction
server placement rejected → AxiomPaper/world/region/transport
blocks.json wrong → Minecraftize
preview wrong with correct blocks.json → preview owner
.schem wrong with correct blocks.json → exporter
slow placement → measure first, then consider plugin/tuning changes
```

## Evidence boundary

Use `LOCAL RUNTIME PROOF REQUIRED` until exact Hunyuan/Blender/Axiom/Paper/Minecraft execution occurs.

Do not claim runtime PASS from CI, source inspection, static binary research, a manually altered result, or a substituted artifact.
