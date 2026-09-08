# End-to-End Test Readiness

Status: canonical design for the first LazyBuilder local acceptance session.

This file defines how the complete Flow 2–6 chain must be prepared **before** local runtime testing starts.

## Objective

The first local test should feel like executing a prepared product pipeline, not debugging one tool at a time.

```text
prepare once
→ execute a known session
→ capture every artifact/evidence consistently
→ stop only for required human/runtime boundaries
→ resume from the first invalidated stage after a real failure
```

Local GPU, Blender, Axiom, Paper, and Minecraft execution remains deferred until this contract reaches `TEST_READY` and the user explicitly starts the local session.

Repository/static CI may run meanwhile.

## Locked chain under test

```text
TEXT (optional)
→ HunyuanDiT v1.1 reference
→ review / approval
        ↘
IMAGE / SINGLE / MULTIVIEW
→ Hunyuan3D-2mv
→ model.glb
→ Blender 5.2.x LTS target
→ Minecraftize
→ canonical block model
→ mcschematic 11.4.4
→ Sponge V2 .schem / DataVersion 4189
→ Axiom 5.3.0
→ AxiomPaper 5.0.1 + Paper 1.21.4
→ Minecraft Java 1.21.4
```

No alternate 3D provider, automatic variant router, MCP, direct Axiom automation, or custom schematic format is part of this session.

## TEST_READY gate

All items below must be satisfied before local runtime starts.

### A. Session control

- one canonical session directory layout is defined;
- one run ID owns all outputs for one acceptance attempt;
- stage statuses and resume behavior are defined;
- commands/entrypoints for executable repository-owned stages are known;
- manual application stages have exact operator steps and evidence requirements;
- no stage depends on chat history to remember parameters.

### B. Input fixtures

The first acceptance batch contains three generation inputs:

```text
T1  TEXT
    one bounded prompt used only to prove text → approved reference

I1  SINGLE IMAGE
    one canonical front reference

I2  MULTIVIEW
    consistent front + right + back + left references
```

The object/build used for I1/I2 should be geometrically clear enough to judge silhouette and orientation. The test is not intended to maximize artistic quality.

T1 does not require four independently generated T2I views.

### C. Downstream fixtures

Minecraftize validation contains two classes in the same acceptance session:

```text
P1  PRIMITIVES
    full block
    stair orientation/half/shape cases
    slab top/bottom/double where supported

R1  REPRESENTATIVE MODEL
    one Blender-prepared Hunyuan result converted through the same engine
```

Primitive correctness proves BlockState behavior. R1 proves that primitives compose into a useful real conversion.

### D. Artifact contracts

Every stage must have an explicit input, output, and evidence record before runtime begins.

### E. Failure ownership

Every stage must map a failure to its first likely owner. A test should never require redesigning the whole repository merely because one stage fails.

## Canonical local session layout

Live test data remains ignored/local and is never required in the public repository.

Recommended structure:

```text
workspace/active/lazybuilder-e2e/
├── case.json
├── inputs/
│   ├── text/
│   │   └── prompt.txt
│   ├── single/
│   │   └── front.png
│   └── multiview/
│       ├── front.png
│       ├── right.png
│       ├── back.png
│       └── left.png
└── runs/
    └── <run-id>/
        ├── session.json
        ├── 00-preflight/
        │   └── environment.json
        ├── 10-reference/
        │   ├── reference_front.png
        │   └── manifest.json
        ├── 20-shape-single/
        │   ├── model.glb
        │   └── manifest.json
        ├── 21-shape-multiview/
        │   ├── model.glb
        │   └── manifest.json
        ├── 30-blender/
        │   ├── target.blend
        │   └── target.json
        ├── 40-minecraftize-primitives/
        │   ├── blocks.json
        │   └── report.json
        ├── 41-minecraftize-model/
        │   ├── blocks.json
        │   └── report.json
        ├── 50-schematic/
        │   ├── build.schem
        │   └── manifest.json
        ├── 60-axiom/
        │   └── runtime.json
        └── acceptance-report.json
```

Screenshots may be stored beside the relevant runtime record when useful. They are supporting evidence, not a substitute for exact stage data.

## Session state contract

`session.json` is the single continuation record for the acceptance run.

Minimum fields:

```text
schema_version
run_id
created_at
minecraft_version
stage_order
active_stage
status
inputs
artifacts
stages[]
```

Each stage record contains:

```text
id
status
input_paths
input_digests
output_paths
output_digests
parameters
started_at
finished_at
metrics
notes
failure_class
```

Allowed stage status values:

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

A successful stage becomes immutable evidence for that run unless an upstream change invalidates it.

## Resume semantics

```text
all upstream stages PASS
→ start at first PENDING/READY stage

stage FAIL
→ preserve outputs/logs
→ fix first wrong owner
→ mark only invalidated stage/downstream as stale
→ resume from first invalidated stage

upstream input changes
→ invalidate every dependent downstream artifact
```

Do not delete prior failed outputs; keep them isolated under the run ID or a new run ID so comparison remains possible.

## Phase 0 — environment preflight

Capture once at session start:

```text
OS + build
CPU
system RAM
GPU
exact VRAM
NVIDIA driver
CUDA runtime/toolkit state
Python version(s)
PyTorch version
free disk
Blender version
Java version
Minecraft version
Fabric Loader
Fabric API
Axiom client version + hash
Paper version/build
AxiomPaper version + hash
OP/permission state
ViaVersion / WorldGuard / PlotSquared / CoreProtect presence
```

Preflight records facts. It should not silently upgrade packages or modify Minecraft server policy.

Acceptance:

```text
required executable/runtime components are discoverable
+ versions are recorded
+ no known locked-stack mismatch is present
```

## Phase 1 — reference coverage

### T1 text reference

Execute the existing text-reference runner with the pinned model/defaults.

Expected output:

```text
reference_front.png
manifest.json
```

Human gate:

```text
reference acceptable for intended object/build
→ PASS

reference materially wrong
→ REJECT / regenerate only this stage
```

This is the only mandatory semantic approval before text-generated imagery may enter shape generation.

### I1 single image

Validate one canonical named view and record its digest.

### I2 multiview

Validate front/right/back/left consistency and record each digest.

Do not attempt automatic image repair or cross-view synthesis during the first acceptance session.

## Phase 2 — Hunyuan3D shape coverage

Run Standard Hunyuan3D-2mv only.

Required outputs:

```text
I1 → 20-shape-single/model.glb
I2 → 21-shape-multiview/model.glb
```

The approved T1 reference may also be run as a single-view input to prove the text-origin path.

Record per generation:

```text
model + subfolder
steps
guidance
octree
num_chunks
seed
background removal
runtime
peak VRAM when measurable
output size
major geometry defects
```

Acceptance is not “perfect mesh”. It is:

```text
GLB generated
+ opens as structurally valid geometry
+ preserves enough intended silhouette/proportion to justify Blender/Minecraft conversion
```

Fast/Turbo comparison is excluded from the first session.

## Phase 3 — Blender target preparation

Use `../blender/TARGET-MODEL.md` as the exact target contract.

One representative generated GLB is selected for downstream conversion. Selection is recorded; the source file is never silently replaced.

Expected outputs:

```text
target.blend
target.json
```

`target.json` records at minimum:

```text
source GLB digest
chosen source case
front/up convention
target width in blocks
source bounds
prepared bounds
applied transforms
cleanup operations
remaining known defects
```

Acceptance:

```text
import works
+ orientation is canonical
+ target scale is intentional
+ severe floating/noisy geometry is removed or documented
+ remaining defects are cheaper to evaluate in Minecraftize than to continue mesh cleanup
```

## Phase 4 — Minecraftize primitive acceptance

Use `../minecraftize/CONTRACT.md`.

Primitive tests are executed in one batch before the representative model is trusted.

Required proof order:

```text
full block
→ straight stairs (4 facings × relevant halves)
→ stair corner shapes when implemented
→ slabs
→ mixed primitive composition
```

Each produced block is represented canonically as:

```text
x
y
z
block_state
source_reason / classifier label when useful for diagnosis
```

Acceptance:

- no duplicate coordinate with conflicting state;
- canonical valid BlockState strings;
- deterministic output for same normalized input + settings;
- primitive orientation/half/shape matches expected fixture.

A feature not yet implemented is `SKIPPED`, not a fake PASS.

## Phase 5 — representative Minecraftize conversion

Run the same converter on the selected Blender target.

Expected outputs:

```text
blocks.json
report.json
```

Record:

```text
target dimensions
occupied block count
full/stair/slab counts
unsupported/ambiguous cells
conversion settings
runtime
```

Quality acceptance for the first end-to-end session is intentionally bounded:

```text
recognizable silhouette
+ intentional scale/proportion retained
+ no catastrophic holes/noise caused by converter
+ block-state mix is explainable
```

Do not require final artistic polish before the pipeline itself is proven.

## Phase 6 — schematic export

Serialize the representative block model with the existing pinned writer.

Expected:

```text
build.schem
manifest.json
```

Acceptance:

```text
Sponge Version 2
DataVersion 4189
tight bounds
round-trip/parser check succeeds where applicable
sampled coordinates retain exact BlockState strings
```

The existing M1 primitive smoke remains a useful static fixture, but the representative build file is the artifact used for final Axiom acceptance.

## Phase 7 — Axiom / Paper / Minecraft acceptance

Use the exact process in `VALIDATION.md`.

One runtime record captures:

```text
Axiom import
Clipboard appearance
Placement creation
AxiomPaper handshake/permission state
world placement
sample block-state orientation
final visible result
```

Final end-to-end PASS requires the **exact representative `build.schem` produced by this run** to reach the Minecraft world.

Do not substitute a manually rebuilt schematic.

## Consolidated acceptance report

`acceptance-report.json` is generated/filled only after the session finishes or is intentionally stopped.

Minimum summary:

```text
run_id
overall_status
first_failed_stage
passed_stages
failed_stages
blocked_stages
selected representative artifact
runtime metrics
known limitations
follow-up owner
```

Possible overall statuses:

```text
PASS
FAIL
BLOCKED
PARTIAL
```

`PARTIAL` means some stage evidence exists but the end-to-end claim is not complete.

## First-failure routing

```text
preflight mismatch
→ environment/bootstrap owner

text output wrong
→ text/reference owner

shape startup/VRAM failure
→ generation environment/profile owner

shape geometry unusable
→ generation/reference owner

GLB cannot be normalized/imported
→ Blender target owner

primitive BlockState wrong
→ Minecraftize primitive owner

representative silhouette wrong after correct Blender target
→ Minecraftize conversion owner

blocks.json correct but .schem wrong
→ schematic exporter owner

.schem valid but Axiom import fails
→ Axiom/client compatibility owner

Clipboard correct but world placement fails
→ AxiomPaper/permission/world owner

world blocks place with wrong orientation
→ first wrong Minecraftize/export BlockState owner
```

## Human-effort policy

The test session should minimize repeated user intervention.

Required human interaction is limited to actions that genuinely cannot be inferred safely:

1. text-reference approval when T1 is used;
2. Blender visual inspection/cleanup judgment;
3. Axiom/Minecraft manual import/placement and final visual inspection.

Do not require separate confirmation after every successful script stage.

## What may be prepared before local testing

The following work is explicitly allowed before any local runtime test:

- complete stage/interface design;
- manifest/session schema implementation;
- deterministic CLI/session controller;
- dry-run and static contract tests;
- Blender helper/operator design and non-runtime-safe source work;
- Minecraftize data model, transform rules, primitive fixtures, and deterministic unit tests that do not depend on the unproven Hunyuan output;
- schematic/report integration;
- CI checks that do not claim GPU/Blender/Axiom/Minecraft runtime success.

## What remains forbidden before explicit local-test start

```text
no Hunyuan GPU proof
no Blender application proof
no Axiom import proof
no Minecraft placement proof
```

Do not report those as PASS from design, mocks, or CI.

## Completion definition for design phase

The design phase is complete when:

```text
all Flow 2–6 interfaces are explicit
+ test cases are explicit
+ artifacts are explicit
+ failure/resume rules are explicit
+ human gates are explicit
+ one future session can execute without inventing procedure mid-test
```

The next repository-development phase may implement the remaining non-runtime scaffolding against this contract. Local runtime starts only after the readiness gate is deliberately opened.