# Next Action

## Current Status

`E2E_TEST_READINESS_SCAFFOLDING_IMPLEMENTED_MINECRAFTIZE_ENGINE_REQUIRED`

The repository operating system, Astra6 profile, `remote_github`/`local` routing, Axiom research baseline, text/image→3D runners, Flow 2–6 acceptance design, and deterministic test-readiness harness are established on `develop`.

The user explicitly does **not** want local runtime testing yet. Do not run Hunyuan GPU, Blender, Axiom, Paper, or Minecraft until the repository reaches `TEST_READY_AWAITING_LOCAL_ACCEPTANCE` and the user explicitly opens that session.

## Locked product chain

```text
T1 TEXT
→ HunyuanDiT v1.1
→ approved reference
→ Hunyuan3D-2mv
→ GLB

I1 SINGLE IMAGE ───────┐
I2 MULTIVIEW ──────────┼→ Hunyuan3D-2mv → GLBs
T1 approved reference ─┘

three shape proofs
→ select representative GLB
→ Blender 5.2.x LTS
→ Minecraftize
→ canonical blocks.json
→ mcschematic==11.4.4
→ Sponge V2 / DataVersion 4189 .schem
→ Axiom 5.3.0
→ AxiomPaper 5.0.1 / Paper 1.21.4
→ Minecraft Java 1.21.4
```

Hunyuan3D-2mv remains the only 3D provider.

## Implemented non-runtime readiness harness

Canonical owner: `kits/lazy-builder/validator/TEST-READINESS.md`.

Repository-owned implementation now includes:

```text
validator/case.template.json
validator/session_contract.py
validator/session_controller.py
validator/acceptance_report.py
validator/test_test_readiness.py

minecraftize/block_model.py
minecraftize/fixtures/primitive_cases.json
minecraftize/build_primitive_fixture.py
minecraftize/test_block_model.py

schematic/export_blocks.py
schematic/test_export_blocks.py

tools/verify_test_readiness.py
.github/workflows/test-readiness-verify.yml
```

Generation runners are aligned with the session layout:

```text
text reference → reference_front.png + manifest.json
shape          → model.glb + manifest.json
```

The text runner accepts `--prompt-file` so the acceptance case can be reproduced from `case.json` without copying prompt text from chat.

## Session behavior now defined

One run owns:

```text
run ID
T1/I1/I2 input snapshot + SHA-256
stage dependency graph
input/output digests
stage history
representative shape selection
resume/invalidation state
consolidated acceptance report
```

Allowed statuses:

```text
PENDING
READY
RUNNING
APPROVAL_REQUIRED
PASS
FAIL
BLOCKED
SKIPPED
```

Invalidation follows true dependencies. Example: changing I1 invalidates `shape_single` and its actual downstream dependents, while preserving independent T1 and multiview evidence.

Every stage `PASS` requires its declared artifacts to exist and be non-empty.

## Canonical block-model contract

`minecraftize/block_model.py` now owns the deterministic pre-schematic representation:

```text
schema_version: 1
minecraft_version: 1.21.4
coordinate mapping:
  Minecraft X = Blender X
  Minecraft Y = Blender Z
  Minecraft Z = -Blender Y

blocks[]:
  x
  y
  z
  canonical block_state
  optional source_reason
```

Rules:

```text
one state per coordinate
no duplicate coordinates
deterministic Y → Z → X order
canonical BlockState property order
tight computed bounds
preview/export must use this same block model
```

The current primitive fixture proves only this data/serializer contract. It is not Minecraftize geometry-classifier proof.

## General schematic handoff now implemented

```text
canonical blocks.json
→ kits/lazy-builder/schematic/export_blocks.py
→ mcschematic 11.4.4
→ build.schem
→ reload same file
→ exact BlockState round-trip
→ manifest.json
```

Axiom runtime remains unexecuted.

## Next Step — deterministic Minecraftize engine implementation

Continue on `develop` without local Hunyuan/Blender/Axiom/Minecraft runtime.

Implement the smallest actual Minecraftize execution surface required to remove the current controller blocker:

1. normalized mesh/grid input contract that can be exercised with deterministic synthetic geometry;
2. V0 occupancy/full-block conversion;
3. primitive stair/slab classification/state helpers in the locked progression;
4. runtime entrypoint producing the same canonical `blocks.json` + `report.json` contract;
5. connect the repository primitive cases to the engine tests;
6. keep representative real-Hunyuan quality explicitly unproved until the unified local session.

Do not add ML/inverse solver, extra block families, Blender automation, or another geometry framework unless deterministic evidence demonstrates need.

## TEST_READY threshold still pending

Do not open the local acceptance session until:

```text
actual Minecraftize entrypoint exists
+ primitive engine tests pass
+ controller no longer reports Minecraftize runtime blocker
+ real T1/I1/I2 fixture pack is selected and populated
+ target_width_blocks is intentional
+ one final non-runtime controller dry-run resolves every command/action
```

Then advance to:

`TEST_READY_AWAITING_LOCAL_ACCEPTANCE`

## Runtime evidence remains unchanged

Still `LOCAL RUNTIME PROOF REQUIRED`:

```text
HunyuanDiT GPU generation
Hunyuan3D-2mv GPU generation
GLB import/preparation in Blender 5.2.x
representative Minecraftize visual quality
Axiom 5.3.0 import/Clipboard
AxiomPaper handshake/placement
Minecraft final placement/visual state
```

M1 writer/static evidence remains PASS, but M1 end-to-end runtime remains pending.

## Stop Boundary

Do not automatically:

- start the local acceptance session;
- install/run Hunyuan models locally;
- launch Blender/Axiom/Minecraft for proof;
- add another 3D provider or model router;
- enable Hunyuan texture generation;
- add MCP/API-server/background orchestration;
- automate Axiom;
- add broad Minecraft block-family support;
- promote `develop` to `Local` or `Local` to `main`.
