# LazyBuilder Context

Status: `PRE_RUNTIME_SYSTEM_READY_RUNTIME_NOT_STARTED` / active R&D / pre-MVP  
Development branch: `develop`  
Verified integration baseline: `Local`  
Stable branch: `main`

This file is the stable orientation layer for new sessions and repository Development.

## Product

LazyBuilder turns text or non-Minecraft visual references into a Minecraft Java schematic through one intentionally narrow chain:

```text
T1 TEXT
→ Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
→ reference_front.png
→ review / approval
→ Hunyuan3D-2mv
→ model.glb

I1 SINGLE IMAGE ──────────────┐
I2 MULTIVIEW ─────────────────┼→ Hunyuan3D-2mv → model.glb
T1 approved reference ────────┘

three shape proofs
→ select representative GLB
→ Blender 5.2.x LTS
→ LazyBuilderTarget + target.json
→ Minecraftize V0
→ canonical blocks.json
├→ canonical preview.svg
└→ mcschematic==11.4.4
   → Sponge Schematic Version 2 / DataVersion 4189
   → Axiom 5.3.0
   → AxiomPaper 5.0.1+1.21.4 / Paper 1.21.4
   → Minecraft Java Edition 1.21.4
```

The product does not train a new 3D model. **Hunyuan3D-2mv remains the only 3D provider.** HunyuanDiT generates a reviewable 2D reference only for T1.

## Canonical production sequence

```text
Flow 1  Repository Boot & Project Memory
Flow 2  T1/I1/I2 Reference Intake
Flow 3  Hunyuan Shape Generation
Flow 4  Representative Selection + Blender Target Preparation
Flow 5  Minecraftize Conversion + Canonical Preview
Flow 6  Schematic Validation + Axiom/Minecraft Handoff
```

Agent work modes and product Flows are separate layers.

## Branch authority

```text
develop
→ active repository Development
→ working commits may be numerous

Local
→ verified integration / stable working baseline
→ exactly one squash commit per approved promoted update

main
→ stable repository history
→ receives explicit Local stable promotions
```

After `develop` → `Local` squash promotion, synchronize/reset `develop` to resulting `Local` HEAD. Stable `main` merge markers do not flow back into lower branches.

## Stable source authority

```text
current user instruction / text intent
+ approved build decisions
+ authoritative reference images / dimensions
→ approved generated T1 reference when text mode is used
→ Hunyuan3D mesh as generated geometric hypothesis
→ selected representative GLB
→ Blender LazyBuilderTarget
→ Minecraftize canonical block model
→ preview + .schem derived from the same blocks.json
→ Axiom/Minecraft runtime acceptance evidence
```

Generated references and downstream artifacts do not silently redefine upstream intent.

## Locked generation identity

HunyuanDiT:

```text
model: Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
revision: 527cf2ecce7c04021975938f8b0e44e35d2b1ed9
```

Hunyuan3D source:

```text
repository: Tencent-Hunyuan/Hunyuan3D-2
commit: f8db63096c8282cb27354314d896feba5ba6ff8a
```

Hunyuan3D-2mv Standard:

```text
model: tencent/Hunyuan3D-2mv
revision: 08766051fa711c6ef5caf86b97e50304fdfcf0ef
subfolder: hunyuan3d-dit-v2-mv
```

Runtime environment authority: `kits/lazy-builder/generation/ENVIRONMENT.md`.

## Current generation input contract

```text
T1 TEXT
→ pinned HunyuanDiT
→ one canonical front reference
→ USER REVIEW / APPROVAL
→ pinned Hunyuan3D-2mv

I1 SINGLE IMAGE
→ one canonical named image
→ pinned Hunyuan3D-2mv

I2 MULTIVIEW
front / right / back / left, same design
→ pinned Hunyuan3D-2mv
```

Do not independently generate four T2I views for MVP.

Text-reference and shape stages run as separate processes so the RTX 3070 8 GB development GPU does not need both models resident simultaneously.

Current first-proof shape baseline:

```text
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
texture: OFF
```

Fast/Turbo variants are inactive until measured same-reference evidence justifies comparison.

## Blender / Minecraftize boundary

Prepared Blender object name:

```text
LazyBuilderTarget
```

Canonical mapping:

```text
Minecraft X =  Blender X
Minecraft Y =  Blender Z
Minecraft Z = -Blender Y
```

`target.json` binds selected GLB, Blender version, target width/bounds, cleanup notes, orientation, and exact `target.blend` SHA-256.

Minecraftize V0 is implemented as Blender-native evaluated geometry + BVH full-block conversion. Runtime proof is still pending.

```text
full_block → SUPPORTED in V0 implementation
stair      → SKIPPED
slab       → SKIPPED
```

The prepared primitive suite includes a 3×2×2 boundary case and a 5×5×5 true-interior case so future Blender runtime evidence cannot pass only from near-surface occupancy.

## Canonical preview/export

```text
Minecraftize blocks.json
├→ build_preview.py → preview.svg
└→ export_blocks.py → build.schem
```

Preview and export share the exact same canonical block model. The schematic writer does not repair conversion logic.

## Current Axiom integration baseline

Current research/static baseline is:

```text
CLIENT
Minecraft Java 1.21.4
Fabric
Axiom 5.3.0
Axiom API family 9

SERVER
Paper 1.21.4
AxiomPaper 5.0.1+1.21.4
Axiom API family 9

SCHEMATIC
Sponge Schematic Version 2
DataVersion 4189
```

Supplied AxiomPaper 4.0.4 remains outside baseline because it uses API family 8. AxiomPaper 5.0.4+1.21.4 remains only a conditional upgrade candidate for a measured matching problem or explicit user decision.

Canonical architecture:

```text
LazyBuilder / mcschematic
→ .schem
→ Axiom 5.3.0 CLIENT parses the file
→ Clipboard / Placement
→ client block buffer
→ AxiomPaper validates multiplayer session / permission / region / transport
→ Paper world modification
```

LazyBuilder therefore does not need an Axiom protocol implementation, Paper-side schematic parser, Axiom automation/MCP, or Blueprint `.bp` output for MVP.

## Pre-Runtime Verification vs Runtime Acceptance

**Pre-Runtime Verification** proves only repository/system preparation:

```text
source/model pins
command routing
session dependency graph
input/upstream digest locks
artifact schemas
target metadata contract
pure/static converter contracts
canonical preview path
schematic writer round-trip
acceptance evidence structure
```

It does **not** launch or prove Hunyuan, Blender conversion, Axiom, Paper, or Minecraft.

**Runtime Acceptance** begins only after explicit user instruction and uses one resumable session with real fixture content.

## Session integrity

- case inputs are SHA-256 snapshotted;
- downstream stages verify current files against authoritative input/upstream PASS digests;
- changed inputs require explicit invalidation;
- changing representative GLB invalidates Blender and true downstream stages;
- `minecraftize_primitives` is independent of the representative Blender target and is preserved when appropriate;
- stage PASS additionally requires artifact-schema validation.

## Development operator profile

Preferred repository Development model: **GPT Astra 6 — ExtraHigh**.

```text
Astra6 reasons about meaning / architecture / diagnosis
→ deterministic code owns computation/invariants
→ matching runtime proves runtime behavior
```

The repository remains model-portable; private reasoning history is not product authority.

## Explicitly inactive scope

Do not add by default:

- Tripo, TRELLIS, Pixal3D, Hunyuan3D-2 base, or multi-3D-model routing;
- automatic four-view T2I generation;
- automatic Fast/Turbo routing;
- Hunyuan texture generation;
- custom foundation model training;
- custom schematic/NBT format;
- entity/NBT support without a concrete requirement/test;
- direct Minecraft world injection;
- direct Axiom automation/protocol implementation;
- Paper-side schematic parsing;
- Axiom Blueprint `.bp` output;
- packet/rate tuning before observed scale evidence;
- MCP orchestration without a demonstrated workflow need;
- complex optimizer/ML solver before rule-based conversion proves insufficient;
- broad Minecraft block-family support before representative runtime evidence requires it.

## Product package boundary

`kits/lazy-builder/` is the single procedure/implementation owner for Flow 2–6.

```text
intake/        T1/I1/I2 intake + approval
generation/    pinned text-reference + shape runners/environment
blender/       target preparation + metadata contract
minecraftize/  deterministic conversion + canonical preview
schematic/     export contract
validator/     preflight, session, artifact, proof/handoff contract
```

## Project-data boundary

The public repository owns the system, not live project data. `workspace/active/` and `workspace/archive/` remain local/external conventions.

Do not commit private references, generated images/GLBs, `.blend`, output schematics, model weights, credentials, Axiom JARs, or Minecraft worlds unless an explicit visibility/licensing decision permits it.

## Operating direction

- recover context before repeating questions;
- use the smallest canonical owner;
- keep Hunyuan3D-2mv as the single 3D provider until evidence proves otherwise;
- keep generation source/model identity pinned;
- treat T1 generated references as hypotheses until approval;
- keep input/artifact digests authoritative;
- use deterministic code for repeated transforms/state/file mechanics;
- keep Minecraftize V0 full-block runtime proof visibly pending until actual Blender execution;
- do not implement stairs/slabs before V0 runtime evidence;
- do not promote `develop` to `Local` without explicit approved promotion;
- stop before runtime while the user has not requested Runtime Acceptance.

## Repository map

```text
AGENTS.md            routing / continuity / model-execution rules
GITHUB_RULES.md      GitHub execution / history / proof discipline
CONTEXT.md           stable product/repository orientation
docs/foundation/     durable Flow policy
docs/knowledge/      continuation / decisions / evidence / operations
.agents/skills/      small reusable semantic skills
kits/lazy-builder/   Flow 2–6 procedure + implementation
workspace/           ignored local/external project data
tools/               deterministic verification
.github/             CI / promotion gates
```

## Continuation

Read `docs/knowledge/next-action.md` after this file. If continuation disagrees with actual implementation state, reconcile the stale owner before proceeding.
