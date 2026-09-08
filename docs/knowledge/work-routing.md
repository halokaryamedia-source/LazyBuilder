# Work Routing

Root `AGENTS.md` is the canonical top-level work-mode/boot authority. This file explains the route only when more context is needed. Product Flow remains separately owned by `docs/foundation/01-production-flow.md`.

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
```

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

## Mode boundaries

### Plan

Use for understanding/decision support. Do not implement merely to make the plan concrete.

### Production Execution

Use LazyBuilder's existing pipeline to create/revise a build. Start from `build-production` and the first affected Flow owner.

### Development

Use when changing LazyBuilder itself: repository policy, Hunyuan procedure, Blender contract, Minecraftize behavior, export, validation, or shared tooling.

### Maintenance

Use for bugs, regressions, cleanup, stale routing/docs, and behavior-preserving corrections. Begin from the concrete defect and first wrong owner.

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
