# Workspace Agent Routing

This repository is LazyBuilder system memory. Current repository/project sources are authority for repository state; chat history is supporting context only.

## Branch and boot

```text
develop  → active repository development; working commits may be numerous
Local    → verified integration / stable working baseline; one squash commit per approved update
main     → clean stable repository history
```

- Normal repository Development happens on `develop`.
- `Local` is not a routine edit target. Promote `develop` to `Local` only through the verified integration boundary.
- Every `develop` → `Local` promotion uses squash merge so one approved update adds exactly one commit to `Local`.
- After promotion, synchronize/reset `develop` to the resulting `Local` HEAD before starting the next development cycle.
- `main` is stable-only. Promote `Local` to `main` only through an explicitly approved stable PR after the stable gate passes.
- A resulting `main` stable merge commit is a main-only marker and is not synchronized back into `Local` or `develop`.
- Version tags/releases are separate publishing actions and are created only when explicitly approved.

Choose the smallest sufficient boot for the task.

### Observe / recover context

When the user only asks to inspect, understand, study, or recover repository context:

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules when GitHub work is material
→ CONTEXT.md
→ docs/knowledge/next-action.md
→ smallest owner needed to explain current state
→ report understanding
→ STOP
```

This is read-only Plan behavior. Do not edit, advance `next-action`, promote backlog work, or start the recorded next step unless the user also asks to continue.

### Non-trivial Development

Before changing LazyBuilder itself:

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules
→ CONTEXT.md
→ docs/knowledge/next-action.md
→ development-brief
→ smallest relevant owner/source
```

### Bounded Maintenance

A clearly bounded defect may start from the exact failing owner when wider product context cannot change the decision. Do not turn Maintenance into repository-wide redesign.

## Work modes

| Intent | Mode | Front door |
|---|---|---|
| Understand/decide/recover before editing | Plan | inspect evidence + owner; no edit until requested |
| Use LazyBuilder to produce/revise a Minecraft build | Production Execution | `build-production` + smallest active kit owner |
| Change LazyBuilder policy/workflow/converter/repository mechanics | Development | `development-brief` + at most one useful specialist |
| Bug/regression/cleanup/stale docs/behavior-preserving correction | Maintenance | concrete failure → first wrong owner |

Creating project artifacts during normal production does not make the task Development.

## Action intent and steering

An explicit user request to create, change, fix, continue, apply, or otherwise perform work authorizes that reversible scope through completion. Do not stop at capability acknowledgement, a plan, an offer to continue, or an extra confirmation step that no authoritative owner requires.

Ask only when a real boundary remains:

- a material build/product decision cannot be resolved responsibly from current authority;
- a high-impact, destructive, irreversible, security-sensitive, publishing, promotion, or other repository action explicitly requires approval;
- the actual target/scope cannot be recovered from current conversation, project state, repository authority, or connected source.

When the user changes direction while work is in progress, preserve completed work that still satisfies the new instruction, invalidate only affected scope, and continue from actual state.

## Production front door

```text
reference images / approved build request
→ build-production
→ smallest active owner in kits/lazy-builder/
```

### Project package resolution

Live build/project packages are production data, not system-repository content. They may live locally under ignored `workspace/active/<project>/` paths or another authorized location.

```text
user names a project
→ use that exact package

current conversation unambiguously establishes one project
→ continue that project

multiple available projects + request ambiguous
→ ask which project before changing project state
```

Never infer project focus from directory order or recency.

## Authority and conflict

Use the nearest authoritative owner for each claim:

1. current explicit user instruction;
2. approved build/project decisions;
3. authoritative reference images, dimensions, drawings, or supplied source;
4. normalized current project state when one exists;
5. generated Hunyuan3D mesh as a geometric hypothesis only;
6. cleaned Blender target as a working representation;
7. Minecraftize preview / block model as generated implementation;
8. `.schem`, Axiom placement, screenshots, reviews, and chat/history as downstream evidence only.

Material conflicts remain `UNKNOWN` until reconciled. A generated 3D model never silently outranks the user's reference.

### Continuity reconciliation

`next-action.md` owns active continuation while current source/state owns actual implementation truth.

```text
detect mismatch
→ inspect current source/owner
→ identify stale continuity vs stale implementation
→ reconcile the correct owner
→ continue from actual state
```

Historical TODOs, audits, backlog entries, and Git history are not active work unless current user intent or `next-action` promotes them.

## Evidence boundary

Use evidence labels only when material uncertainty remains:

```text
REFERENCE VERIFIED
REPOSITORY VERIFIED
LOCAL RUNTIME PROOF REQUIRED
UNSUPPORTED
UNKNOWN
```

Static inspection cannot upgrade Hunyuan generation, Blender behavior, Axiom import, or Minecraft-world claims to verified runtime evidence.

## Derived-artifact rule

Preserve the authority chain:

```text
reference / approved decisions
→ generated 3D target
→ cleaned Blender target
→ Minecraftize block model
→ schematic delivery
→ Axiom/Minecraft acceptance evidence
```

Do not patch a downstream `.schem` merely to hide an upstream Minecraftize defect when evaluating LazyBuilder correctness. Manual Axiom polish is a valid final-user workflow, but it must be distinguished from engine output during validation.

## Repository continuity

Canonical current-state owners:

- stable product/repository orientation → `CONTEXT.md`;
- active continuation → `docs/knowledge/next-action.md`;
- durable decisions → `docs/knowledge/decisions/`;
- durable production policy → `docs/foundation/`;
- detailed production procedure/mechanics → affected `kits/lazy-builder/` owner;
- live project data → current external/local project package;
- historical reviews → `docs/knowledge/reviews/history/` only when needed.

Update `next-action.md` only when status, active boundary, blocker, deferred boundary, or next meaningful step actually changes.

## Skill budget

Canonical root skills:

```text
.agents/skills/development-brief
.agents/skills/build-production
```

- Production Execution → `build-production` + smallest kit procedure.
- Development → mandatory `development-brief` + at most one useful product specialist.
- Maintenance → specialist optional.
- Plan → no specialist by default.

Do not create Blender/Hunyuan/exporter/validator skills merely because those surfaces exist.

## Execution channel

`GITHUB_RULES.md` owns GitHub tool selection, transfer safety, write/commit/history discipline, verification, retries, recovery, and STOP behavior.

Repository branch-specific narrowing:

- `develop` CI is the active repository regression safety net.
- `develop` → `Local` requires the Local promotion gate and squash merge.
- After promotion, `develop` must be synchronized/reset to resulting `Local` HEAD.
- `Local` → `main` requires stable verification and explicit stable-promotion approval.
- Do not bypass a failed gate by editing another branch directly.
- GitHub/static checks prove repository contracts only; Hunyuan, Blender, Axiom, and Minecraft runtime claims require the matching local capability.

## User-facing communication

Default to concise, direct language. State the result or decision early. Expose repository machinery only when it materially explains scope, tradeoffs, proof, or next action.

For repository/system Development, a compact brief is enough when useful:

```text
Tujuan:
Hasil yang dituju:
Tidak diubah:
Cara memastikan benar:
```

Final repository/system report:

```text
Status: Selesai | Perlu pemeriksaan | Terhenti
Hasil:
Bukti:
Batasan:
Next step:
```

Use one next step. Explain decisions rather than internal scratch work.

## Product boundaries

- `kits/lazy-builder/` is the single product procedure package.
- Hunyuan3D-2mv is the only active 3D generation provider for the MVP.
- Blender is the 3D workbench; Minecraftize is the custom conversion core.
- `mcschematic` is the planned schematic writer; Axiom is the final external import/edit/placement tool.
- MCP, multi-model routing, custom ML training, direct world injection, and direct Axiom automation are not active MVP scope.
- Live project packages are not tracked in the public LazyBuilder system repository.
