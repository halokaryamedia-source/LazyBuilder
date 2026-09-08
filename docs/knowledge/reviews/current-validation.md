# Current Validation Status

Updated: 2026-09-08

## Current system state

Working branch: `develop`.  
Verified integration baseline: `Local`.  
Stable branch: `main`.

LazyBuilder remains **pre-MVP**. The PRD-Creator-style repository operating/documentation baseline is verified and promoted to `Local`; product runtime is not yet claimed.

The current `develop` cycle additionally defines **GPT Astra 6 ExtraHigh** as the preferred repository Development operator profile and formalizes the two execution modes **`remote_github`** and **`local`** while keeping repository authority and executable proof model-portable.

## Current production chain

```text
reference images
→ Hunyuan3D-2mv
→ GLB
→ Blender target
→ Minecraftize
→ .schem
→ Axiom
→ Minecraft Java
```

## Repository operating-system evidence

Initial candidate:

```text
3ff6b3e259aecc8342f43f8ba5b8e83d64c51d7e
chore(governance): adopt structured repository operating system
```

Static evidence:

```text
Repository Verify
run 34202778188
Static repository contract → PASS
```

Integration evidence:

```text
PR #1 — Adopt PRD-Creator operating model
head: develop
base: Local
Local Promotion Verify run 34202955180 → PASS
merge method: squash
Local milestone: 98046e2339aff0beff3caff8dee9030b258686ef
```

After the squash promotion, `develop` was synchronized/reset to the resulting `Local` milestone before opening the next cycle.

The verified baseline establishes:

- `develop` active Development / `Local` verified milestone / `main` stable history;
- canonical root routing/governance owners;
- `docs/foundation/` durable Flow policy;
- `docs/knowledge/` continuation/ownership/decision/review/backlog separation;
- canonical skills `development-brief` + `build-production`;
- one `kits/lazy-builder/` product package;
- ignored local/external workspace project-data boundary;
- static repository and promotion gates;
- retirement of old duplicate `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md`, and `docs/TOOLS.md` owners.

## Astra6 ExtraHigh development-profile evidence

Current development-profile change:

```text
438b08b9249658281eb589df55c3deffd00a7231
docs(governance): optimize development flow for Astra6 ExtraHigh
```

Repository verification:

```text
Repository Verify
run 34207246235
Static repository contract → PASS
```

The change establishes these current Development boundaries:

- Astra6 receives a compact task packet after canonical boot: Goal, Owner, constraints/out-of-scope, 2–5 acceptance criteria, proof budget, and exact evidence/failure;
- default post-boot expansion stays at 1–3 additional owner files unless a real dependency requires more;
- Astra6 reasoning owns requirement/architecture/tradeoff/root-cause work;
- deterministic code owns repeatable geometry, coordinate, BlockState, serialization, and test invariants;
- Hunyuan, Blender, Axiom, and Minecraft claims require matching runtime proof;
- no Astra-specific skill/framework/MCP layer was introduced;
- repository memory remains the durable authority so another capable model/developer can reproduce current state without hidden reasoning history.

## Local / Remote GitHub execution-mode evidence

Current execution-mode candidate ends at:

```text
98902b1d018eff3a04dc0ca68b964a8bc7d8e217
docs(governance): complete local and remote_github mode routing
```

Repository verification:

```text
Repository Verify
run 34211141538
Static repository contract → PASS
```

Current execution contract:

```text
remote_github
→ exact remote state / bounded repository-native changes / branch / PR / CI / promotion

local
→ real clone/worktree / coding / dependencies / build / tests / binary artifacts /
  Hunyuan / Blender / Axiom / Minecraft runtime
```

Naming is explicitly protected:

```text
local  = execution mode
Local  = verified integration branch
```

Normal local source work still targets `develop`. Local implementation may hand off to `remote_github` after targeted proof and push so remote state/CI/PR/promotion can be verified without turning GitHub into a remote shell.

No `local` or `remote_github` root skill, framework, mode daemon, or temporary runtime workflow was added. `tools/verify_repository.py` now checks the canonical execution-mode owners and keeps the root skill set unchanged.

This proves repository routing/policy only. It does not prove that a local workstation is configured or that any product runtime has executed successfully.

## Product/runtime proof status

Not yet claimed:

- Hunyuan3D-2mv local generation on RTX 3070 8 GB;
- GLB import/cleanup in Blender;
- Minecraftize full-block conversion;
- stairs/slabs conversion;
- `.schem` Axiom import;
- Minecraft world placement/visual quality.

These require actual matching local runtime evidence and will be recorded only after execution.

## Evidence boundary

GitHub/static verification proves repository contracts only. It does not prove GPU generation, Blender behavior, Axiom import, Minecraft placement, subjective visual fidelity, or the relative quality of a model configuration.
