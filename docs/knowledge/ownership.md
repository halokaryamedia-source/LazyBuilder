# Repository Ownership

Use this file only to answer **who owns what**. Exact procedure/contracts remain in the named owners; do not duplicate them here.

## Root operating owners

| Boundary | Owner |
|---|---|
| Top-level boot, work modes, continuity, authority, skill budget | `AGENTS.md` |
| Execution-mode selection (`remote_github` / `local`), GitHub branch/ref, write/history, CI/API/transfer safety | `GITHUB_RULES.md` |
| Stable repository/product orientation | `CONTEXT.md` |
| Contribution, local synchronization, and promotion procedure | `CONTRIBUTING.md` |
| Public-repository data handling | `SECURITY.md` |
| Active continuation | `docs/knowledge/next-action.md` |
| Source/state precedence | `docs/knowledge/source-authority.md` |
| Current validation evidence | `docs/knowledge/reviews/current-validation.md` |
| Durable decisions/rationale | `docs/knowledge/decisions/` |
| Future/non-active work | `docs/knowledge/operations/backlog.md` |

Execution-mode rationale lives in `docs/knowledge/decisions/execution-modes-local-remote-github.md`; it does not create another execution-policy owner.

## Repository areas

| Area | Responsibility |
|---|---|
| `.agents/skills/` | reusable Development / Production judgment |
| `docs/foundation/` | durable Flow policy |
| `docs/knowledge/` | continuation, routing, ownership, decisions, evidence |
| `kits/lazy-builder/` | Flow 2–6 procedure + implementation owner |
| `tools/`, `.github/` | engineering verification and promotion |
| `workspace/active/`, `workspace/archive/` | ignored local/external project-package mount points |

## Package root owners

| Boundary | Owner |
|---|---|
| Package orientation / architecture map | `kits/lazy-builder/README.md` |
| Package technical/file routing | `kits/lazy-builder/AGENTS.md` |
| End-to-end Flow 2–6 execution router | `kits/lazy-builder/SKILL.md` |

## Production owners

| Boundary | Owner |
|---|---|
| Reference consistency/intake | `kits/lazy-builder/intake/REFERENCE-INTAKE.md` |
| Hunyuan3D-2mv runtime procedure | `kits/lazy-builder/generation/HUNYUAN3D-2MV.md` |
| Blender target readiness | `kits/lazy-builder/blender/TARGET-MODEL.md` |
| Minecraft conversion behavior | `kits/lazy-builder/minecraftize/CONTRACT.md` |
| `.schem` writing/export | `kits/lazy-builder/schematic/EXPORT.md` |
| Runtime/acceptance proof | `kits/lazy-builder/validator/VALIDATION.md` |

## Engineering owners

Current executable repository tooling is intentionally small:

| Boundary | Owner |
|---|---|
| Static repository invariant verification | `tools/verify_repository.py` |
| Repository CI | `.github/workflows/repository-verify.yml` |
| develop → Local integration gate | `.github/workflows/local-promotion-verify.yml` |
| Local → main stable gate | `.github/workflows/release-verify.yml` |

Future Minecraftize source/test ownership should be added here only when those files actually exist.

## Routing rule

```text
Who owns this?
→ ownership.md

Which execution mode fits?
→ GITHUB_RULES.md

What durable product policy applies?
→ docs/foundation/

What exact production procedure applies?
→ kits/lazy-builder/

Which source/state outranks another?
→ source-authority.md
```

Create a new owner only when responsibility is genuinely different. Do not create parallel registries or duplicate schemas for convenience.
