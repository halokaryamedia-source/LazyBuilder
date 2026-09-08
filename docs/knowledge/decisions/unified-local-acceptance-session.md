# Unified Local Acceptance Session

Status: active durable decision.

## Decision

LazyBuilder will not use a sequence of small exploratory local runtime tests as the default path to MVP proof.

Before the first local runtime session begins, Flow 2–6 must be designed as one coherent testable chain with explicit inputs, outputs, checkpoints, failure ownership, resumability, and evidence capture.

The first local runtime effort is therefore a **unified acceptance session**:

```text
one environment preflight
→ input/reference coverage
→ Hunyuan generation
→ Blender target preparation
→ Minecraftize primitive + representative conversion
→ schematic export
→ Axiom import / Clipboard / Placement
→ Minecraft world verification
→ one consolidated report
```

Static repository/CI checks may continue before that session. They do not count as local runtime proof.

## Why

Testing one runtime surface immediately after it is implemented creates repeated setup cost and weakens diagnosis because later stage contracts are still moving.

A prepared acceptance session provides:

- one known environment snapshot;
- one fixed test-case package;
- deterministic artifact names and manifests;
- explicit stage acceptance criteria before execution;
- clear resume behavior after a failure;
- fewer repeated installs, launches, imports, and manual notes;
- one final evidence package instead of disconnected test fragments.

## Readiness boundary

Local runtime execution remains deferred until the test-readiness owner declares `TEST_READY`.

`TEST_READY` requires the repository to define, at minimum:

1. canonical workspace/test-session layout;
2. environment preflight fields;
3. exact test cases and stage order;
4. stage input/output contracts;
5. Blender target normalization contract;
6. Minecraftize intermediate output contract and primitive acceptance;
7. schematic/Axiom handoff contract;
8. stage status + resume semantics;
9. consolidated evidence/report format;
10. explicit items that still require human inspection.

Detailed procedure: `../../../kits/lazy-builder/validator/TEST-READINESS.md`.

## Human gates

A unified session does not mean blindly automating every step.

The session may stop only for a real human/runtime boundary, principally:

- approval of a text-generated canonical reference before it is allowed to condition 3D generation;
- manual Blender/Axiom/Minecraft operations that cannot be proved statically;
- a hard runtime failure whose first wrong owner must be fixed before continuing.

Routine successful stages should not require a separate chat confirmation merely because a stage ended.

## Failure and resume rule

A failed stage does not invalidate proven upstream stages automatically.

```text
failure
→ record exact failing stage + evidence
→ diagnose first wrong owner
→ fix only invalidated scope
→ resume from first invalidated stage
```

Do not restart the whole session unless the fix changes an upstream input or contract that makes previous outputs stale.

## Scope retained

This decision does not add:

- another 3D provider;
- automatic Hunyuan Fast/Turbo routing;
- MCP or background orchestration;
- direct Axiom automation;
- custom schematic/NBT serialization;
- direct Minecraft world injection.

It changes **when and how runtime proof is collected**, not the locked MVP stack.

## Current consequence

Until test readiness is complete:

```text
repository/static design + implementation work → allowed
local GPU generation test                  → deferred
Blender runtime test                       → deferred
Axiom/Minecraft runtime test               → deferred
```

Runtime claims remain `LOCAL RUNTIME PROOF REQUIRED` until the unified acceptance session actually executes them.