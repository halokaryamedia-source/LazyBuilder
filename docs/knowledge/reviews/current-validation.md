# Current Validation Status

Updated: 2026-09-08

## Current system state

```text
status: PRE_RUNTIME_SYSTEM_READY_RUNTIME_NOT_STARTED
working branch: develop
verified integration baseline: Local
stable branch: main
product maturity: pre-MVP
```

LazyBuilder's repository/system preparation is now coherent enough for a future controlled Runtime Acceptance session, but **no new Hunyuan/Blender/Axiom/Minecraft runtime proof is claimed**.

## Canonical product chain

```text
T1 TEXT
→ pinned HunyuanDiT
→ reference_front.png
→ user approval
→ pinned Hunyuan3D-2mv
→ model.glb

I1 SINGLE IMAGE ──────────────┐
I2 MULTIVIEW ─────────────────┼→ pinned Hunyuan3D-2mv → model.glb
T1 approved reference ────────┘

three GLBs
→ select representative GLB
→ Blender LazyBuilderTarget + target.json
→ Minecraftize V0 full-block conversion
→ canonical blocks.json
├→ preview.svg
└→ mcschematic==11.4.4 → Sponge V2 / DataVersion 4189 .schem
→ Axiom 5.3.0
→ AxiomPaper 5.0.1+1.21.4 / Paper 1.21.4
→ Minecraft Java 1.21.4
```

## Latest pre-runtime hardening evidence

Hardening delivery:

```text
9c7d83faeac730bce83b645679344b2efca51e01
feat(readiness): harden pre-runtime pipeline contracts
```

Checks on that exact commit:

```text
Generation Contract Verify   run 34258306317 → PASS
Repository Verify            run 34258306328 → PASS
M1 Schematic Smoke           run 34258306357 → PASS
Pre-Runtime Verify           run 34258306388 → PASS
```

Pre-Runtime Verify covers repository/source synchronization, generation contracts, session/artifact tests, static session dry-run, Minecraftize pure tests, runtime-entrypoint compilation **without launching applications**, canonical preview generation, and schematic writer round-trip.

Expected static marker:

```text
STATIC_PRE_RUNTIME_DRY_RUN_PASS_RUNTIME_NOT_STARTED
```

## Generation reproducibility status

Pinned authority:

```text
HunyuanDiT
model: Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
revision: 527cf2ecce7c04021975938f8b0e44e35d2b1ed9

Hunyuan3D source
repository: Tencent-Hunyuan/Hunyuan3D-2
commit: f8db63096c8282cb27354314d896feba5ba6ff8a

Hunyuan3D-2mv
model: tencent/Hunyuan3D-2mv
revision: 08766051fa711c6ef5caf86b97e50304fdfcf0ef
subfolder: hunyuan3d-dit-v2-mv
```

`kits/lazy-builder/generation/ENVIRONMENT.md` owns the local setup contract. Exact target-machine Python/PyTorch/CUDA/driver values remain runtime preflight facts and are not guessed from CI.

## Session / evidence integrity status

Repository-owned session behavior now enforces:

```text
case input SHA-256 snapshot
→ stage input digest verification
→ upstream PASS artifact digest verification
→ explicit invalidation on source change
→ true dependency resume
→ semantic artifact validation before PASS
```

Changing the selected representative GLB invalidates Blender and its true downstream stages while preserving independent Minecraftize primitive evidence.

`minecraftize_primitives` depends on preflight/runtime environment, not on representative `target.blend`.

## Blender preparation status

Prepared-target contract is implemented but not runtime-proven.

Canonical outputs:

```text
target.blend
target.json
```

`target.json` binds:

```text
selected source path + SHA-256 + stage
Blender version
LazyBuilderTarget object name
target_width_blocks
world bounds
canonical axis mapping
cleanup notes
target.blend SHA-256
```

Helper: `kits/lazy-builder/blender/write_target_metadata.py`.

## Minecraftize V0 status

V0 runtime entrypoint is implemented using Blender evaluated geometry + BVH occupancy.

```text
full_block → SUPPORTED by implementation
stair      → SKIPPED
slab       → SKIPPED
```

Static/pure logic checks are PASS. Actual Blender execution is still `LOCAL RUNTIME PROOF REQUIRED`.

The prepared runtime primitive suite contains:

```text
3×2×2 boundary box
5×5×5 true-interior box
```

The second case requires non-surface/interior evidence so future runtime proof cannot pass only from the near-surface band.

## Canonical preview status

Preview now has one source of truth:

```text
Minecraftize blocks.json
→ build_preview.py
→ preview.svg + manifest.json
```

The preview manifest binds the exact source/output SHA-256. Preview and schematic export consume the same canonical `blocks.json`.

This deterministic preview exists and is statically verified. Representative visual quality remains runtime/human evidence.

## Schematic writer evidence

Current writer target:

```text
mcschematic==11.4.4
Minecraft Java 1.21.4
Sponge Version 2
DataVersion 4189
```

The writer fixture proves file creation, reload, and exact BlockState round-trip for representative full/stair/slab states. The latest M1 smoke run on the hardening commit is PASS.

This proves writer/schema behavior, not Axiom import.

## Axiom static integration baseline

Exact audited baseline remains:

```text
Axiom 5.3.0 client
sha256 8026fdb448686cd6db69e69c695fa17f54508f801ddddb3ffeb850b79b04eae5
Axiom API family 9

AxiomPaper 5.0.1+1.21.4
sha256 cecafb3e1beba81245ee5bcfc3251052035526b99bb111127b968b09c92d86c8
Axiom API family 9
```

AxiomPaper 4.0.4 remains rejected for this baseline because it uses API family 8. AxiomPaper 5.0.4+1.21.4 remains only a conditional upgrade candidate for a matching measured problem or explicit user decision.

Architecture remains:

```text
LazyBuilder .schem
→ Axiom 5.3.0 CLIENT parses local file
→ Clipboard / Placement
→ client block buffer
→ AxiomPaper validates session / permission / region / transport
→ Paper world modification
```

LazyBuilder still does not need an Axiom protocol implementation or Paper-side schematic parser for MVP.

## Runtime proof status

```text
HunyuanDiT GPU generation                → LOCAL RUNTIME PROOF REQUIRED
Hunyuan3D-2mv GPU generation             → LOCAL RUNTIME PROOF REQUIRED
GLB quality / Blender import             → LOCAL RUNTIME PROOF REQUIRED
Blender LazyBuilderTarget preparation    → LOCAL RUNTIME PROOF REQUIRED
Minecraftize primitive execution         → LOCAL RUNTIME PROOF REQUIRED
Minecraftize representative conversion  → LOCAL RUNTIME PROOF REQUIRED
Axiom import / Clipboard                 → LOCAL RUNTIME PROOF REQUIRED
AxiomPaper / Paper placement             → LOCAL RUNTIME PROOF REQUIRED
Minecraft final visual fidelity          → LOCAL RUNTIME PROOF REQUIRED
```

The user has explicitly deferred Runtime Acceptance. Do not convert static readiness into runtime PASS.

## Remaining future acceptance input

No additional repository subsystem is required before the first runtime session.

The future controlled case still needs user-selected content:

```text
T1 prompt
I1 front image
I2 front/right/back/left consistent images
intentional target_width_blocks
```

That content is a test fixture decision, not a missing architecture layer.

## Evidence owners

```text
generation environment   → kits/lazy-builder/generation/ENVIRONMENT.md
session/readiness         → kits/lazy-builder/validator/TEST-READINESS.md
artifact contracts       → kits/lazy-builder/validator/ARTIFACT-CONTRACTS.md
Minecraftize             → kits/lazy-builder/minecraftize/CONTRACT.md
schematic export         → kits/lazy-builder/schematic/EXPORT.md
Axiom/runtime validation → kits/lazy-builder/validator/VALIDATION.md
active continuation      → docs/knowledge/next-action.md
```

## Evidence boundary

Repository/static/CI evidence proves only deterministic preparation and behavior actually executed in CI. Runtime-heavy application behavior requires the exact future local acceptance execution and must remain visibly pending until then.
