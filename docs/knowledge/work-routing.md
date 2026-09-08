# Work Routing

Root `AGENTS.md` is the canonical top-level work-mode/boot authority. This file explains the route only when more context is needed. Product Flow remains separately owned by `docs/foundation/01-production-flow.md`; exact execution-mode mechanics remain owned by root `GITHUB_RULES.md`.

## Routing overview

```text
User request
→ read-only context request?
   yes → recover root context → report → STOP
   no  → choose work mode

Plan
→ inspect evidence/owner

Production Execution
→ build-production
→ smallest kits/lazy-builder owner

Development
→ continuity recovery
→ development-brief
→ smallest relevant owner

Maintenance
→ concrete defect
→ first wrong owner

then, when execution is required:
→ choose remote_github or local
```

Work mode answers **what kind of work this is**. Execution mode answers **where/how the work should run**. They are separate decisions.

## Context recovery is not implementation

When the user says only `amati`, inspect, understand, study, or recover:

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules when material
→ CONTEXT.md
→ next-action.md
→ smallest owner needed
→ report
→ STOP
```

Do not execute the recorded next step merely because it was discovered.

## Non-trivial Development continuity

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules
→ CONTEXT.md
→ next-action.md
→ development-brief
→ smallest relevant owner/source
```

After this bootstrap, further reading remains bounded.

## Work-mode boundaries

### Plan

Use for understanding/decision support. Do not implement merely to make the plan concrete.

### Production Execution

Use LazyBuilder's existing pipeline to create/revise a build. Start from `build-production` and the first affected Flow owner.

### Development

Use when changing LazyBuilder itself: repository policy, Hunyuan procedure, Blender contract, Minecraftize behavior, export, validation, or shared tooling.

### Maintenance

Use for bugs, regressions, cleanup, stale routing/docs, and behavior-preserving corrections. Begin from the concrete defect and first wrong owner.

## Execution-mode routing

Canonical execution modes:

```text
remote_github
local
```

### `remote_github`

Use for bounded repository-native work:

- exact remote state inspection;
- small text/documentation changes that safely fit GitHub operations;
- branches/refs;
- PR/review operations;
- CI/workflow inspection;
- remote verification and promotion.

### `local`

Use when real workspace/runtime capability matters:

- source coding or coordinated multi-file patches;
- dependencies/build/tests;
- binary/heavy artifacts;
- Hunyuan GPU execution;
- Blender;
- Axiom;
- Minecraft;
- real Git staging/diff semantics when they materially help.

Important:

```text
local  = execution mode
Local  = verified integration branch
```

`local` work normally happens on branch `develop`, not branch `Local`.

### Normal hybrid cycle

```text
remote_github
→ recover current remote authority when needed
→ select task owner

local
→ implement/build/run when local capability is required
→ targeted proof
→ commit + push develop

remote_github
→ confirm pushed state / CI
→ PR or promotion only when requested/required
```

If a remote task exposes a genuine local requirement, switch to `local` instead of creating GitHub Actions or helper architecture to simulate a local machine.

## Product/technical routing

```text
reference/intended build meaning wrong
→ intake / build-production

Hunyuan generation procedure wrong
→ generation owner

Blender target preparation wrong
→ Blender owner

Minecraft block conversion wrong
→ Minecraftize owner

schematic writing wrong
→ schematic owner

runtime proof/handoff wrong
→ validator owner

repository routing/CI wrong
→ repository engineering owner
```

## Continuity and inactive work

```text
active continuation  → next-action.md
future/non-active    → operations/backlog.md
historical evidence  → reviews/history/
durable rationale    → decisions/
```

Old TODOs/reviews/decisions do not become active work by themselves.
