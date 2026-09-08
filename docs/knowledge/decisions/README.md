# Decision Index

This directory stores durable LazyBuilder repository/product decisions whose reasons must survive future sessions.

Current execution does **not** start from historical decision prose. Use `../next-action.md` for active continuation, `../ownership.md` for current owners, `../source-authority.md` for precedence, and the nearest current foundation/kit contract for exact behavior.

## Current Durable Decisions

| Decision | Current status / owner |
|---|---|
| Repository Development uses `develop`, `Local` is one-squash-commit-per-approved-milestone history, and `main` is stable merge-boundary history | [branch-governance.md](branch-governance.md) |
| Hunyuan3D-2mv is the only active 3D generation provider for MVP | [single-hunyuan-provider.md](single-hunyuan-provider.md) |
| Custom development concentrates on Minecraftize; Blender is the workbench, `mcschematic` the writer, Axiom the downstream editor/placement tool | [minecraftize-core-boundary.md](minecraftize-core-boundary.md) |
| GPT Astra 6 ExtraHigh is the preferred Development operator profile; repository context stays compact, evidence-first, deterministic where possible, and model-portable | [astra6-extrahigh-development-profile.md](astra6-extrahigh-development-profile.md) |
| Do not add providers, frameworks, optimization layers, automation, or compatibility machinery without demonstrated need | [anti-overdevelopment-simplification.md](anti-overdevelopment-simplification.md) |
| Formal durable decision records require a real cross-session/cross-owner reason | [recording-policy.md](recording-policy.md) |

## How to Read Decisions

```text
Need current task/status?
→ ../next-action.md

Need current owner?
→ ../ownership.md

Need source/state precedence?
→ ../source-authority.md

Need why a durable current boundary exists?
→ this index → matching decision file
```

Historical decisions are rationale, not automatic current work.

## Recording Rule

Create or materially update a decision only when the reason must survive sessions and cannot be represented cleanly by current state/owner documentation alone. Ordinary fixes, bounded revisions, generated artifacts, and active task status do not become durable decisions.
