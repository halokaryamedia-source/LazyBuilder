# Pre-Runtime Readiness

Status: `PRE_RUNTIME_SYSTEM_READY_RUNTIME_NOT_STARTED`.

This historical filename remains for continuity. The phase is **Pre-Runtime Verification**, not the later **Runtime Acceptance Test**.

No Hunyuan inference, Blender conversion, Axiom import, Paper placement, or Minecraft placement is claimed by this status.

## Canonical product path

```text
T1 TEXT
→ pinned native HunyuanDiTPipeline (distilled, 25-step baseline)
→ reference_front.png
→ user approval
→ pinned Hunyuan3D-2mv shape

I1 SINGLE IMAGE → pinned Hunyuan3D-2mv shape
I2 MULTIVIEW    → pinned Hunyuan3D-2mv shape

three GLBs
→ representative selection
→ Blender LazyBuilderTarget + target.json
→ Minecraftize V0 primitive proof
→ Minecraftize representative model
→ canonical blocks.json
→ canonical preview.svg → user approval
→ mcschematic 11.4.4 / Sponge V2 / DataVersion 4189
→ Axiom / AxiomPaper / Paper / Minecraft
→ acceptance-report.json
```

## Source-audit hardening

The pre-runtime evidence policy is explicitly **fail-closed**: missing, mismatched, stale, or unverifiable evidence must block PASS rather than be treated as an acceptable unknown.

Repository preparation intentionally rejects several false-green conditions:

```text
manifest claims pinned Hunyuan source but imported checkout differs
→ FAIL

imported Hunyuan checkout contains local modifications
→ FAIL

required runtime package / Blender executable absent during preflight
→ FAIL

installed generation API signatures no longer match wrapper calls
→ FAIL

text or preview stage attempts RUNNING → PASS without review
→ FAIL

case input changes without explicit snapshot refresh
→ INPUT_DRIFT

Blender bounds contain NaN/Infinity/zero/inverted extent
→ FAIL

Minecraftize/preview/schematic report metadata disagrees with canonical blocks
→ FAIL

Axiom runtime evidence points to another schematic/environment
→ FAIL
```

## Generation authority

```text
HunyuanDiT model revision
527cf2ecce7c04021975938f8b0e44e35d2b1ed9

Hunyuan3D source commit
f8db63096c8282cb27354314d896feba5ba6ff8a
required actual checkout: same commit + clean

Hunyuan3D-2mv model revision
08766051fa711c6ef5caf86b97e50304fdfcf0ef
```

Hunyuan3D extraction-critical settings are explicit in the manifest rather than inherited silently from future upstream defaults.

## Session graph

```text
preflight
├─ text_reference → shape_text ─┐
├─ shape_single ────────────────┼→ representative selection → blender ─┐
├─ shape_multiview ─────────────┘                                     ├→ minecraftize_model
└─ minecraftize_primitives ────────────────────────────────────────────┘

minecraftize_model
→ minecraft_preview (approval gate)
→ schematic
→ axiom / paper / minecraft
```

Minecraftize primitive proof is independent of representative Blender target but still requires the same validated host preflight.

## Input integrity and refresh

Session start snapshots SHA-256 for all controlled T1/I1/I2 inputs. Stage start re-hashes inputs against case snapshot or upstream PASS digest.

Intentional changes use `refresh_case_input.py`, which refreshes only the named input authority and invalidates only its true downstream chain. This avoids both silent drift and an impossible invalidate/retry loop with a stale snapshot.

## Human gates

Future runtime requires actual judgment only where output meaning can change materially:

```text
T1 reference       RUNNING → APPROVAL_REQUIRED → PASS
representative GLB explicit selection
Blender target     manual application + metadata
Minecraft preview  RUNNING → APPROVAL_REQUIRED → PASS
Axiom/Minecraft    exact runtime evidence
```

Deterministic mechanics do not need ceremonial approval.

## Preflight contract

`collect_environment.py` does not launch runtime apps. It captures installed package/executable facts, source checkout identity, API signature compatibility, and declared target environment values.

If packages, driver, Blender, Hunyuan checkout, or Axiom/Paper environment changes after preflight, invalidate preflight before continuing.

## Minecraftize V0

```text
full_block → SUPPORTED
stair      → SKIPPED
slab       → SKIPPED
```

Prepared runtime primitives:

```text
3×2×2 boundary case
5×5×5 true-interior case
```

The latter must prove non-near-surface occupancy. Actual Blender execution remains future runtime evidence.

## Preview and schematic source of truth

```text
canonical blocks.json
├→ build_preview.py → preview.svg
└→ export_blocks.py → build.schem
```

Preview manifest must agree with real blocks metadata. Schematic writer reloads/verifies every source block state, while the manifest keeps only bounded diagnostic samples plus total verified count.

## Runtime evidence lineage

Future `runtime.json` is created with `write_runtime_evidence.py` and binds the exact accepted schematic + preflight environment hashes. The session controller refuses Axiom PASS when either hash differs from the session’s authoritative PASS artifact.

## Static proof

Pre-Runtime Verify covers:

```text
owner/document synchronization
source/model/wrapper contracts
session/invalidation/approval tests
artifact contract tests
static controller dry-run
Minecraftize pure/block-model tests
runtime entrypoint compilation without launching apps
canonical preview generation
schematic export + exhaustive reload BlockState verification
```

Expected marker:

`STATIC_PRE_RUNTIME_DRY_RUN_PASS_RUNTIME_NOT_STARTED`

## Runtime-only unknowns

Static/source correctness cannot prove:

```text
CUDA/driver/VRAM startup behavior
actual Hunyuan image/mesh quality
Blender BVH execution on target geometry
Minecraftize visual fidelity
Axiom client import behavior
AxiomPaper/Paper placement behavior
Minecraft final visual result/performance
```

These remain `LOCAL RUNTIME PROOF REQUIRED` until the user explicitly starts Runtime Acceptance.

## Stop boundary

Do not automatically add stairs/slabs, Fast/Turbo routing, another 3D provider, Axiom automation/MCP, packet tuning, NBT/entity support, or promote `develop` to `Local`/`main`.
