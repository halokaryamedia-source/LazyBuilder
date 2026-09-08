# Local / Remote GitHub Execution Modes Decision

Date: 2026-09-08  
Status: current

## Context

LazyBuilder follows the PRD-Creator operating model. That model separates repository-native GitHub work from work that needs an actual local/Codex-style workspace or matching runtime capability. The user wants this distinction to be explicit and easy to use in daily development.

Without explicit names, sessions may either overuse remote GitHub operations for work that belongs in a real workspace, or treat every small repository change as requiring a full local setup.

## Decision

Use two canonical execution modes:

```text
remote_github
local
```

They are execution channels, not agent skills, directories, branches, or product subsystems.

### `remote_github`

Use for work that GitHub can natively and safely own:

- exact remote repository/branch/file state;
- bounded text/policy/documentation changes when atomicity remains acceptable;
- branch/ref operations;
- pull requests/review metadata;
- CI/workflow inspection;
- remote verification and branch-promotion mechanics.

### `local`

Use for work that requires a real workspace/runtime:

- source implementation and coordinated multi-file patches;
- dependency installation/build/test commands;
- binary/heavy artifacts;
- Hunyuan3D-2mv GPU execution;
- Blender and Minecraftize runtime;
- Axiom/Minecraft runtime proof;
- real Git staging/diff semantics when materially useful.

Normal local source work uses branch `develop`.

## Naming boundary

```text
local  = execution mode / local clone or worktree / runtime
Local  = verified integration branch
```

The lowercase execution mode never grants permission to edit uppercase branch `Local` directly.

## Normal hybrid workflow

```text
remote_github
→ pin/recover remote authority when needed

local
→ implement / build / run
→ targeted proof
→ commit on develop
→ push develop

remote_github
→ confirm remote state / CI
→ PR / promotion when the repository boundary requires it
```

A task may remain entirely in one mode when that is sufficient. Mode switching should happen only when the current task actually requires the other capability.

## Why

This keeps the workflow practical:

- remote operations remain fast for repository coordination;
- heavy/code/runtime work stays where the required tools actually exist;
- binary and multi-file work does not get fragmented into remote file-write commits;
- GitHub Actions is not abused as a remote shell;
- runtime claims remain tied to real runtime evidence;
- the branch model stays independent from the execution channel.

## Tradeoffs / not chosen

Not chosen:

- `.agents/skills/local` or `.agents/skills/remote_github`;
- a new mode router program or framework;
- temporary GitHub workflows that emulate local execution;
- a second branch named after an execution mode;
- forcing all work through local or all work through remote GitHub.

The cost is one explicit mode-selection decision before implementation. That cost is small and avoids much larger transfer/runtime confusion.

## Evidence / validation boundary

Repository verification can prove the mode names, ownership, routing references, and skill-set boundary. It cannot prove that a local workstation/runtime is currently configured or that Hunyuan/Blender/Axiom/Minecraft runs successfully.

## Follow-up owner

- exact execution-mode policy and handoff → `GITHUB_RULES.md`;
- human routing explanation → `docs/knowledge/work-routing.md`;
- Development lifecycle application → `docs/knowledge/work-modes/development.md`;
- local Git synchronization → `CONTRIBUTING.md`.
