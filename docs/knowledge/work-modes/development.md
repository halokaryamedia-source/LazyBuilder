# Development Workflow

This file is the human-readable lifecycle overview for repository/system Development. The canonical implementation procedure is `.agents/skills/development-brief/SKILL.md`; exact execution-mode mechanics are owned by root `GITHUB_RULES.md`.

Normal build Production Execution does not use this workflow.

## Entry

Non-trivial Development begins only after continuity recovery:

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules
→ CONTEXT.md
→ docs/knowledge/next-action.md
→ development-brief
```

A read-only `amati / inspect / understand / recover context` request stops after context recovery/reporting and does not enter implementation.

## Lifecycle

```text
recover current context
→ development-brief grounds goal / method / owner / scope / proof
→ development needed?
   no → explain/reuse/no-change + minimum proof → STOP
   yes
   → at most one useful product specialist
   → smallest relevant owner/source
   → choose execution mode
   → smallest complete implementation
   → cheapest relevant proof
   → original-scope check
   → update only continuation/decision owner whose state changed
   → STOP
```

## Owner selection

```text
build/reference/Minecraft production meaning
→ optionally build-production

pure technical mechanics with semantics settled
→ kits/lazy-builder/AGENTS.md + exact owner

repository/test/CI mechanics
→ repository engineering owner
```

## Execution modes

Choose the mode from the actual work requirement, not personal preference.

### `remote_github`

Use when the complete task is safely repository-native:

```text
exact remote state
small bounded text/policy change
branch/ref operation
PR/review
CI inspection
promotion verification
```

Do not use `remote_github` as a substitute shell for a local build/runtime requirement.

### `local`

Use when development needs:

```text
real clone/worktree
source coding
coordinated multi-file patch
install/build/test
binary artifact
Hunyuan GPU
Blender
Axiom
Minecraft
```

Normal local source work targets `develop`.

`local` is an execution mode. `Local` is the verified integration branch. They are not interchangeable.

### Typical Development cycle

```text
remote_github: recover/pin remote authority when needed
↓
local: implement + targeted proof
↓
local: commit and push develop
↓
remote_github: confirm remote state / CI
↓
PR/promotion only when the repository boundary requires it
```

A bounded documentation-only change may remain entirely in `remote_github` when that produces one clean logical state. A real source/runtime change should normally use `local`.

## Runtime evidence

Runtime acceptance claims require matching local capability:

```text
Hunyuan generation → local GPU runtime
Blender behavior   → local Blender runtime
Axiom import       → local Axiom runtime
Minecraft result   → local Minecraft runtime
```

Static GitHub/CI proof must not be described as runtime proof.

Do not create temporary Actions or helper architecture to emulate missing local capabilities.

## Completion

Before `Selesai`, re-check:

- original goal and out-of-scope boundary;
- 2–5 acceptance criteria from development-brief;
- whether the selected execution mode actually proved the claimed behavior;
- whether actual proof supports the claimed status;
- whether any continuity/decision owner truly changed.

Distinguish implemented from verified when required local runtime proof remains unavailable.
