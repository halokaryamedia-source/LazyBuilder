# Validation and Handoff

## Proof layers

```text
0 Pre-Runtime Verification (static/contracts only)
1 generation/runtime environment capture
2 conversion primitive correctness
3 representative Minecraftize + canonical preview
4 schematic writer / schema compatibility
5 Axiom client import + Clipboard
6 AxiomPaper handshake / placement permission
7 Minecraft world placement + visual fidelity
```

A lower layer never proves a higher layer.

## Current audited runtime target

```text
Minecraft Java Edition 1.21.4

CLIENT
Fabric
Axiom 5.3.0
Axiom API family 9

SERVER
Paper 1.21.4
AxiomPaper 5.0.1+1.21.4
Axiom API family 9

SCHEMATIC
Sponge Version 2
DataVersion 4189
```

Do not use supplied AxiomPaper 4.0.4 for this baseline; it is API family 8.

AxiomPaper 5.0.4+1.21.4 remains only a conditional upgrade candidate for a measured matching issue or explicit user decision.

## Current evidence boundary

```text
Pre-Runtime repository/contracts      → PASS only when CI is green
M1 writer / BlockState round-trip      → PASS
Axiom binary integration audit         → PASS (research/static)
Hunyuan runtime                        → LOCAL RUNTIME PROOF REQUIRED
Blender/Minecraftize runtime           → LOCAL RUNTIME PROOF REQUIRED
Axiom import / Clipboard               → LOCAL RUNTIME PROOF REQUIRED
Paper handshake / placement            → LOCAL RUNTIME PROOF REQUIRED
Minecraft placement / visual fidelity  → LOCAL RUNTIME PROOF REQUIRED
```

## Preflight capture

Before future runtime, use:

```bash
python kits/lazy-builder/validator/collect_environment.py \
  --output <run>/00-preflight/environment.json \
  --record key=value \
  ...
```

The session action reports the exact required record keys. They cover:

```text
Blender version
GPU / VRAM / CUDA driver/runtime
Minecraft client version
Fabric Loader / Fabric API
Axiom client version + SHA-256
Paper version/build
AxiomPaper version + SHA-256
permission mode
ViaVersion / WorldGuard / PlotSquared / CoreProtect state
Axiom license/whitelist state as applicable
```

The collector itself does not launch Hunyuan, Blender, Axiom, or Minecraft.

Pinned generation identities (`hunyuan3d_source_commit`, `hunyuan3d_model_revision`, `hunyuandit_model_revision`) are auto-recorded from the repository contract; machine-specific facts remain explicit.

A preflight stage becomes PASS only after `artifact_validation.py` confirms required fields are present.

## Generation acceptance

T1/I1/I2 generation must use the exact source/model pins in `../generation/ENVIRONMENT.md`.

Every generation output must preserve manifest + SHA-256 lineage.

T1 additionally requires explicit user approval of `reference_front.png` before shape generation.

## Blender acceptance

Selected representative GLB:

```text
→ manual Blender preparation
→ LazyBuilderTarget
→ target.blend
→ target.json via write_target_metadata.py
```

`target.json` must bind source/target hashes, Blender version, target width/bounds, orientation, and cleanup notes.

## Minecraftize acceptance

Primitive runtime uses the actual Blender V0 converter and includes:

```text
3×2×2 boundary case
5×5×5 true-interior case
```

The interior case must not be satisfiable entirely by near-surface occupancy.

V0 feature status remains:

```text
full_block → SUPPORTED
stair      → SKIPPED
slab       → SKIPPED
```

Representative conversion then emits canonical `blocks.json` + report.

## Canonical preview

Before schematic export, generate:

```text
41-minecraftize-model/blocks.json
→ build_preview.py
→ 45-preview/preview.svg + manifest.json
```

This preview consumes the exact block model used by export. It is not a second conversion path.

Human inspection may compare the preview against the prepared mesh/reference, but static preview generation alone is not visual-fidelity PASS.

## Schematic writer acceptance

```text
canonical blocks.json
→ mcschematic==11.4.4
→ Sponge V2 / DataVersion 4189 build.schem
→ reload same file
→ exact BlockState round-trip
```

If `blocks.json` is correct and `.schem` is wrong, fix the exporter. If `blocks.json` is wrong, fix Minecraftize.

## Axiom session preflight

For the first controlled multiplayer proof use either OP or the expected Axiom permission setup. After changing permission/OP state, reconnect as required by the plugin behavior.

If Axiom is not active:

```text
/whynoaxiom
/axiomhandshake
```

The import menu requires the server-provided `CAN_IMPORT_BLOCKS` capability / `axiom.can_import_blocks` permission.

Do not change exporter/model versions before identifying the first failing owner.

## Exact Axiom/Paper/Minecraft runtime checks

For the exact generated `build.schem`:

1. import in Axiom 5.3.0 with no unknown-format/version error;
2. verify Clipboard content;
3. create Placement without first-proof rotation/scale/flip;
4. verify server accepts placement through AxiomPaper/Paper;
5. verify expected world structure and block states;
6. compare Minecraft result to canonical preview/prepared target/reference;
7. write `runtime.json` only from actual observations.

`runtime.json` can validate as PASS only when these checks are all PASS:

```text
import
clipboard
placement
minecraft_world
visual_state
```

## Failure routing

```text
Import Schematic disabled
→ permission/session: axiom.can_import_blocks / handshake

unknown format / unsupported Sponge Version
→ schematic compatibility

file imports but Clipboard wrong
→ client parsing/content compatibility

Clipboard correct but Placement cannot start
→ BUILD_SECTION permission / client restrictions

Placement starts but server rejects/does nothing
→ AxiomPaper handshake/world/region/transport

block/state/orientation wrong with correct blocks.json
→ exporter / BlockState owner

blocks.json already wrong
→ Minecraftize owner

preview wrong but blocks.json correct
→ preview owner

slow updates with correct permissions
→ measure first, then evaluate AxiomPaper 5.0.4+1.21.4
```

## Server policy/config boundary

Do not pre-tune packet/rate limits. Check existing world/region/disallowed-block policy only after an observed failure.

Do not enable broad payload settings merely to make a first proof pass.

## Later scope

NBT/entities, broad block families, production-scale benchmarking, Fast/Turbo, and Axiom automation remain outside V0 until evidence requires them.

## Evidence language

Use `LOCAL RUNTIME PROOF REQUIRED` whenever the repository is prepared but the exact application execution has not happened.

Do not claim runtime PASS from CI, binary inspection, a hand-altered screenshot, or a manually substituted artifact.
