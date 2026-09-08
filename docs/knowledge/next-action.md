# Next Action

## Current Status

`E2E_TEST_READINESS_DESIGN_COMPLETE_RUNTIME_DEFERRED`

The repository operating system, Astra6 profile, execution-mode routing, M1 writer/Axiom research baseline, image/text→3D runners, and the complete Flow 2–6 unified acceptance design are established.

The user explicitly does **not** want local runtime testing yet. Do not start Hunyuan GPU, Blender, Axiom, Paper, or Minecraft runtime proof until the test-readiness implementation is complete and the user explicitly starts that session.

Branch state:

```text
develop → active Development continuation
Local   → verified integration milestone
main    → stable repository history
```

## Locked pipeline

```text
TEXT (optional)
→ Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
→ reference_front.png
→ USER REVIEW / APPROVAL
        ↘
IMAGE / SINGLE / MULTIVIEW
→ Hunyuan3D-2mv
→ model.glb
→ Blender 5.2.x LTS
→ Minecraftize
→ canonical blocks.json
→ mcschematic==11.4.4
→ Sponge V2 .schem / DataVersion 4189
→ Axiom 5.3.0
→ AxiomPaper 5.0.1 + Paper 1.21.4
→ Minecraft Java 1.21.4
```

Hunyuan3D-2mv remains the only 3D provider. HunyuanDiT is only the optional text-reference generator.

## Unified acceptance decision

The first local runtime effort will be one prepared acceptance session rather than a series of isolated stage tests.

Canonical owners:

```text
docs/knowledge/decisions/unified-local-acceptance-session.md
kits/lazy-builder/validator/TEST-READINESS.md
```

The session covers:

```text
preflight once
→ T1 text-reference path
→ I1 single-image path
→ I2 multiview path
→ choose representative GLB
→ Blender target preparation
→ Minecraftize primitive batch
→ representative Minecraftize conversion
→ schematic export
→ Axiom import / Clipboard / Placement
→ Minecraft world verification
→ consolidated acceptance report
```

A failure preserves valid upstream evidence and resumes from the first invalidated stage.

## Test-session data contract

Planned local package:

```text
workspace/active/lazybuilder-e2e/
├── case.json
├── inputs/
└── runs/<run-id>/
    ├── session.json
    ├── 00-preflight/
    ├── 10-reference/
    ├── 20-shape-single/
    ├── 21-shape-multiview/
    ├── 30-blender/
    ├── 40-minecraftize-primitives/
    ├── 41-minecraftize-model/
    ├── 50-schematic/
    ├── 60-axiom/
    └── acceptance-report.json
```

Allowed stage state:

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

Generated/live artifacts remain ignored local project data.

## Established stage contracts

### Flow 2/3 — input/generation

Repository runners already exist for:

```text
text → canonical reference
single/multiview → Hunyuan3D-2mv GLB
```

No local GPU proof is claimed yet.

### Flow 4 — Blender

Canonical target contract now defines:

```text
Blender up    +Z
Blender front -Y
Minecraft X =  Blender X
Minecraft Y =  Blender Z
Minecraft Z = -Blender Y
```

Primary scale input is an explicit target dimension such as `target_width_blocks`, not arbitrary Blender units.

The raw imported source remains recoverable; a separate prepared target is sampled by Minecraftize.

### Flow 5 — Minecraftize

Design is an explicit deterministic pass pipeline:

```text
normalize grid
→ occupancy candidates
→ full-block baseline
→ surface classification
→ stairs
→ stair corners when implemented
→ slabs
→ conflict resolution
→ preview + canonical blocks.json
```

Primitive fixtures prove state correctness; one representative prepared model proves composition.

### Flow 6 — schematic/Axiom

The existing `mcschematic` writer contract and Axiom 1.21.4 research/static baseline remain authoritative.

The representative `build.schem` from the same run—not a manually rebuilt substitute—must be the file used for final Axiom/Minecraft acceptance.

## Next Step — non-runtime test-readiness implementation

Continue on `develop` without local runtime execution.

Implement the smallest deterministic scaffolding required by `validator/TEST-READINESS.md`:

1. session/case manifest schema + validation;
2. run-state/resume controller for repository-owned script stages;
3. canonical `blocks.json` schema/helpers;
4. deterministic Minecraftize primitive fixtures/tests that do not depend on Hunyuan runtime;
5. acceptance-report generation/aggregation;
6. dry-run/static contract coverage tying stage paths and statuses together.

Blender/Axiom remain manual/runtime surfaces; do not build automation merely to remove those manual boundaries.

## TEST_READY threshold

Do not start the local acceptance session until the repository can answer all of these without inventing procedure at test time:

```text
what input fixture is used?
what exact command/action is next?
what artifact is expected?
where is it stored?
what is PASS/FAIL?
what evidence is recorded?
which owner handles failure?
where does a resumed run continue?
```

Only then may the state advance to `TEST_READY_AWAITING_LOCAL_ACCEPTANCE`.

## Existing runtime evidence remains unchanged

Still `LOCAL RUNTIME PROOF REQUIRED`:

```text
HunyuanDiT GPU generation
Hunyuan3D-2mv GPU generation
GLB import/preparation in Blender 5.2.x
representative Minecraftize conversion quality
Axiom 5.3.0 import / Clipboard
AxiomPaper handshake / placement
Minecraft final placement / visual state
```

M1 writer/static evidence remains PASS but M1 end-to-end runtime remains pending.

## Stop Boundary

Do not automatically:

- start any local runtime test;
- install/run Hunyuan models locally;
- launch Blender/Axiom/Minecraft for proof;
- add Tripo / TRELLIS / Pixal3D / another 3D provider;
- add Hunyuan3D-2 base as a parallel path;
- add automatic Fast/Turbo routing;
- generate four independent T2I views;
- enable Hunyuan texture generation;
- add MCP/API-server/background orchestration;
- automate Axiom directly;
- promote `develop` to `Local` or `Local` to `main`.
