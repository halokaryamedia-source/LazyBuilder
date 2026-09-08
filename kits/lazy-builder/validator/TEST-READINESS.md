# Pre-Runtime Readiness

Status: `PRE_RUNTIME_SYSTEM_READY_RUNTIME_NOT_STARTED`.

This file keeps its historical filename for repository continuity, but the phase is now named **Pre-Runtime Verification**. It must not be confused with the later **Runtime Acceptance Test**.

No Hunyuan GPU generation, Blender conversion, Axiom import, Paper placement, or Minecraft placement is claimed by this status.

## Canonical product path

```text
T1 TEXT
→ pinned HunyuanDiT reference
→ user approval
→ pinned Hunyuan3D-2mv shape

I1 SINGLE IMAGE
→ pinned Hunyuan3D-2mv shape

I2 MULTIVIEW front/right/back/left
→ pinned Hunyuan3D-2mv shape

three GLBs
→ select representative GLB
→ Blender 5.2.x / LazyBuilderTarget + target.json
→ Minecraftize V0 primitive suite
→ Minecraftize representative model
→ canonical blocks.json
→ canonical preview.svg from the same blocks.json
→ mcschematic 11.4.4 / Sponge V2 / DataVersion 4189
→ Axiom 5.3.0
→ AxiomPaper 5.0.1 / Paper 1.21.4
→ Minecraft Java 1.21.4
→ acceptance-report.json
```

## What Pre-Runtime Verification proves

Repository-owned deterministic/static preparation covers:

```text
generation model/source pins + dry-run contracts
session graph / resume / invalidation
input and upstream artifact digest locking
artifact schema validation
Blender target metadata contract
Minecraftize V0 pure logic
Blender-native runtime entrypoints compile without launch
primitive suite definition includes a true-interior proof
canonical blocks.json validation
canonical SVG preview from blocks.json
schematic writer round-trip
consolidated evidence/lineage report
```

Expected static marker:

`STATIC_PRE_RUNTIME_DRY_RUN_PASS_RUNTIME_NOT_STARTED`

## Session graph

```text
preflight
├─ text_reference → shape_text ─┐
├─ shape_single ────────────────┼→ representative selection → blender ─┐
├─ shape_multiview ─────────────┘                                     ├→ minecraftize_model
└─ minecraftize_primitives ────────────────────────────────────────────┘

minecraftize_model
→ minecraft_preview
→ schematic
→ axiom / paper / minecraft
```

`minecraftize_primitives` depends on the environment preflight, **not** on the selected Blender target. Changing the selected GLB therefore invalidates Blender and its true downstream dependents without throwing away an already valid primitive proof.

## Input integrity

Session initialization snapshots SHA-256 for T1/I1/I2.

Every stage start verifies its current inputs against either:

```text
original case snapshot digest
or
upstream PASS artifact digest
```

Changed input is not silently accepted. The stage owner must be explicitly invalidated and resumed.

Changing the representative shape after Blender/downstream evidence exists invalidates:

```text
blender
→ minecraftize_model
→ minecraft_preview
→ schematic
→ axiom
```

and preserves independent `minecraftize_primitives` evidence.

## Artifact contract

`ARTIFACT-CONTRACTS.md` is the detailed owner. A stage cannot become `PASS` merely because output files exist.

Every successful boundary must pass structure/version/digest checks appropriate to that artifact.

## Generation reproducibility

`generation/ENVIRONMENT.md` owns local setup. Generation manifests record:

```text
HunyuanDiT model + revision
Hunyuan3D-2mv model + revision
Hunyuan3D source repository + commit
input hashes
parameters
output hash
```

Exact Python/PyTorch/CUDA/driver versions are captured from the real target machine during preflight; they are not guessed from static CI.

## Minecraftize V0 boundary

V0 remains full-block only.

```text
full_block → SUPPORTED
stair      → SKIPPED
slab       → SKIPPED
```

The Blender runtime primitive suite is prepared with two full-block cases:

```text
3×2×2 boundary case
5×5×5 true-interior case
```

The second case must contain cells that are not merely inside the near-surface band, so runtime proof will actually exercise BVH parity/interior occupancy.

That primitive suite is **prepared but not runtime-proven** until Blender is explicitly launched in the future acceptance session.

## Preview contract

Preview is not a second converter.

```text
canonical blocks.json
├─ build_preview.py → preview.svg (top/front/right projections)
└─ export_blocks.py → build.schem
```

The preview manifest binds the exact source/output SHA-256.

## Human/application gates during future runtime

Only these require real judgment/action:

1. approve the generated T1 reference;
2. select the representative GLB;
3. prepare/judge `LazyBuilderTarget` in Blender;
4. inspect canonical block preview;
5. execute/inspect Axiom → Paper → Minecraft placement.

Successful deterministic script stages do not need ceremonial chat confirmation.

## Resume rule

```text
failure or intentional source change
→ identify first wrong owner
→ invalidate only true dependents
→ preserve independent valid evidence
→ resume from first invalidated stage
```

## What remains outside repository preparation

The system-side pre-runtime preparation is complete when static verification is green.

A future runtime session still needs user-selected test content:

```text
T1 prompt
I1 front image
I2 front/right/back/left consistent images
intentional target_width_blocks
```

Those are acceptance inputs, not missing architecture.

## Runtime Acceptance boundary

Do not start runtime until the user explicitly requests it.

Runtime Acceptance means actual execution of:

```text
HunyuanDiT / Hunyuan3D GPU
Blender target + primitive/model conversion
Axiom import / Clipboard
AxiomPaper / Paper placement
Minecraft visual verification
```

Static/CI PASS never upgrades those claims.

## Stop Boundary

Do not automatically add stairs/slabs, Fast/Turbo routing, another 3D provider, Axiom automation/MCP, packet tuning, NBT/entity support, or promote `develop` to `Local`/`main`.
