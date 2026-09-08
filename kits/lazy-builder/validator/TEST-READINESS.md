# End-to-End Test Readiness

Status: deterministic scaffolding implemented; local runtime remains deferred.

This owner defines the first LazyBuilder local acceptance session. The goal is one prepared run across Flow 2–6, not a sequence of disconnected experiments.

## Locked chain

```text
T1 TEXT
→ HunyuanDiT v1.1
→ reference_front.png
→ human approval
→ Hunyuan3D-2mv
→ 19-shape-text/model.glb

I1 SINGLE IMAGE
→ Hunyuan3D-2mv
→ 20-shape-single/model.glb

I2 MULTIVIEW
front/right/back/left
→ Hunyuan3D-2mv
→ 21-shape-multiview/model.glb

all three shape proofs
→ select one representative GLB
→ Blender 5.2.x LTS
→ Minecraftize primitives
→ Minecraftize representative model
→ canonical blocks.json
→ mcschematic 11.4.4
→ Sponge V2 / DataVersion 4189 .schem
→ Axiom 5.3.0
→ AxiomPaper 5.0.1 + Paper 1.21.4
→ Minecraft Java 1.21.4
```

Hunyuan3D-2mv remains the only 3D provider. No Fast/Turbo router, second provider, texture pipeline, Axiom automation, or custom schematic format is part of this session.

## Repository-owned readiness tooling

```text
validator/case.template.json
→ canonical T1/I1/I2 case shape

validator/session_contract.py
→ case/session schema + stage dependency contract

validator/session_controller.py
→ init/status/next/mark/select-shape/invalidate

validator/acceptance_report.py
→ consolidated PASS/FAIL/BLOCKED/PARTIAL report

minecraftize/block_model.py
→ canonical deterministic blocks.json model

minecraftize/fixtures/primitive_cases.json
minecraftize/build_primitive_fixture.py
→ static primitive data-contract fixture

schematic/export_blocks.py
→ canonical blocks.json → mcschematic → build.schem

tools/verify_test_readiness.py
.github/workflows/test-readiness-verify.yml
→ deterministic/static CI proof only
```

The primitive fixture proves the block-model/serializer contract only. It does **not** prove the future Minecraftize geometry classifier.

## Canonical local package

Before the first local acceptance session, copy `case.template.json` to the ignored workspace and replace the example values with the selected real fixture.

```text
workspace/active/lazybuilder-e2e/
├── case.json
├── inputs/
│   ├── text/prompt.txt
│   ├── single/front.png
│   └── multiview/
│       ├── front.png
│       ├── right.png
│       ├── back.png
│       └── left.png
└── runs/<run-id>/
    ├── session.json
    ├── 00-preflight/environment.json
    ├── 10-reference/
    │   ├── reference_front.png
    │   └── manifest.json
    ├── 19-shape-text/
    │   ├── model.glb
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
    ├── 60-axiom/runtime.json
    └── acceptance-report.json
```

Generated/live files remain ignored project data.

## Case contract

The first real `case.json` contains exactly:

```text
T1 text prompt file
I1 one canonical front image
I2 consistent front/right/back/left images
target_width_blocks
Minecraft target 1.21.4
```

The controller snapshots input paths and SHA-256 digests into `session.json` so the run does not depend on chat history.

T1, I1, and I2 should normally describe the same bounded object/build when comparing input modes. They do not need to be artistically complex; geometry/orientation must be judgeable.

## Session state

Allowed stage states:

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

Canonical stages:

```text
preflight
text_reference
shape_text
shape_single
shape_multiview
blender
minecraftize_primitives
minecraftize_model
schematic
axiom
```

`PASS` requires every declared output file to exist, be non-empty, and be digested into the session record.

When a stage starts, declared input files are also digested.

## Dependency / resume semantics

Invalidation follows the dependency graph, not simple file order.

Example:

```text
I1 / shape_single changes
→ invalidate shape_single
→ invalidate Blender and its true downstream dependents
→ keep valid shape_text and shape_multiview evidence
```

A stage snapshot is retained in its history before invalidation. Existing failed files are not deleted automatically.

This allows one acceptance run to resume from the first actually invalidated owner.

## Human gates

Only genuine application/semantic boundaries require user intervention:

1. review/approve T1 `reference_front.png`;
2. choose the representative GLB after the three shape paths are available;
3. Blender visual cleanup/target judgment;
4. Axiom/Minecraft import, placement, and final visual verification.

Do not ask for a new confirmation after every successful deterministic script stage.

## Stage acceptance

### Preflight

Record exact environment facts without silently installing/upgrading packages or modifying server policy.

Required evidence includes OS, CPU/RAM, GPU/VRAM, NVIDIA/CUDA, Python/PyTorch, free disk, Blender, Java, Minecraft/Fabric, Axiom client/hash, Paper build, AxiomPaper/hash, permission state, and relevant optional Paper integrations.

### Text reference

```text
generate_text_reference.py
→ reference_front.png
→ manifest.json
→ APPROVAL_REQUIRED
```

A poor reference invalidates only T1/text-origin work.

### Shape coverage

Standard Hunyuan3D-2mv only:

```text
approved T1 → 19-shape-text/model.glb
I1          → 20-shape-single/model.glb
I2          → 21-shape-multiview/model.glb
```

Record generation parameters, runtime, peak VRAM when measurable, mesh size, and major defects.

### Blender

All shape paths must be available before comparison/selection. The selected source is recorded explicitly.

Use `../blender/TARGET-MODEL.md`:

```text
Blender +Z up / -Y front
Minecraft X = Blender X
Minecraft Y = Blender Z
Minecraft Z = -Blender Y
```

The target scale is driven by the explicit `target_width_blocks` (or another explicitly approved target dimension), never guessed from Blender units.

### Minecraftize primitives

The static primitive fixture already protects canonical BlockState/data-model behavior. Runtime primitive PASS still requires the actual Minecraftize engine entrypoint to produce its own `blocks.json` and `report.json`.

Required engine coverage remains:

```text
full block
straight stairs: 4 facings × relevant halves
corner shapes when implemented
slab top/bottom/double when supported
mixed composition
```

A not-yet-implemented engine feature is `SKIPPED`, never fake PASS.

### Representative Minecraftize model

The same converter runs on the selected Blender target.

Acceptance is bounded to recognizable silhouette, intentional scale/proportion, no catastrophic converter holes/noise, deterministic output, and explainable block-family use.

### Schematic

`schematic/export_blocks.py` consumes the exact representative canonical `blocks.json`.

It writes:

```text
build.schem
manifest.json
```

and reloads the same file with mcschematic to verify exact BlockState round-trip for every emitted coordinate before Axiom runtime is attempted.

### Axiom / Paper / Minecraft

Use `VALIDATION.md` and the exact `50-schematic/build.schem` produced by the same run.

Final PASS requires:

```text
Axiom import
→ Clipboard
→ Placement
→ AxiomPaper/Paper acceptance
→ Minecraft world placement
→ sampled state/orientation verification
```

No manually rebuilt substitute counts as end-to-end proof.

## Controller usage for the future local session

Initialize once:

```bash
python kits/lazy-builder/validator/session_controller.py init \
  --case workspace/active/lazybuilder-e2e/case.json \
  --run-id <run-id> \
  --runs-dir workspace/active/lazybuilder-e2e/runs
```

Then use:

```bash
python kits/lazy-builder/validator/session_controller.py next --session <session.json>
python kits/lazy-builder/validator/session_controller.py status --session <session.json>
```

The controller returns the exact next command/action and expected outputs.

State/evidence changes use `mark`, `select-shape`, and `invalidate`. The controller is a run-state coordinator; it does not bypass required human application boundaries.

## Consolidated report

At an intentional stop or session completion:

```bash
python kits/lazy-builder/validator/acceptance_report.py --session <session.json>
```

Possible overall states:

```text
PASS
FAIL
BLOCKED
PARTIAL
```

A lower static layer never upgrades an unexecuted Hunyuan/Blender/Axiom/Minecraft claim to PASS.

## Current blocker before TEST_READY

The readiness harness is implemented, but the real acceptance session is **not open yet**.

Still required before `TEST_READY_AWAITING_LOCAL_ACCEPTANCE`:

1. implement the actual deterministic Minecraftize engine entrypoint that consumes the prepared target and produces canonical `blocks.json`/`report.json`;
2. connect its primitive suite to the repository-owned cases rather than the static contract fixture alone;
3. select/populate the actual T1/I1/I2 fixture pack and target width;
4. perform one final dry-run of controller paths without launching GPU/Blender/Axiom/Minecraft runtime.

Until then, local runtime remains intentionally deferred.
