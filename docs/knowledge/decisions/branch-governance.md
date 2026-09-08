# Branch Governance Decision

Status: current

## Context

LazyBuilder initially used only `main` + `Local`, with routine work written directly to `Local`. The user then explicitly required LazyBuilder to follow the operating/documentation system of PRD-Creator 1:1.

## Decision

Use the same three-layer history model:

```text
develop
→ active repository Development
→ working commits may be numerous

Local
→ verified integration / stable working milestones
→ exactly one squash commit per approved update

main
→ stable repository history
→ explicit Local promotions using a normal merge commit
```

After a `develop` → `Local` squash promotion, synchronize/reset `develop` to the resulting `Local` HEAD before starting new Development.

A main-only stable merge marker is not synchronized back into `Local` or `develop`.

## Why

This separates experimentation/history from verified milestones and stable release boundaries while keeping cross-session repository state easy to recover.

## Not chosen

- routine direct edits to `Local`;
- development directly on `main`;
- merging a long develop chain into Local without squash;
- automatically promoting Local to main.

## Follow-up owner

Root `AGENTS.md`, `GITHUB_RULES.md`, `CONTRIBUTING.md`, and promotion workflows own execution.
