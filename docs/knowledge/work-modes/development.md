# Development Workflow

This file is the human-readable lifecycle overview for repository/system Development. The canonical implementation procedure is `.agents/skills/development-brief/SKILL.md`; do not duplicate that procedure here.

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

## Execution channel

GitHub mechanics remain canonical in root `GITHUB_RULES.md`.

Runtime acceptance claims require matching capability:

```text
Hunyuan generation → local GPU runtime
Blender behavior   → Blender runtime
Axiom import       → Axiom runtime
Minecraft result   → Minecraft runtime
```

Do not create temporary Actions or helper architecture to emulate missing local capabilities.

## Completion

Before `Selesai`, re-check:

- original goal and out-of-scope boundary;
- 2–5 acceptance criteria from development-brief;
- whether actual proof supports the claimed status;
- whether any continuity/decision owner truly changed.

Distinguish implemented from verified when local runtime proof remains unavailable.
