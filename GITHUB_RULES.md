# GitHub Rules

Canonical operating rules for AI/ChatGPT working with GitHub in this repository.

Repository-specific `AGENTS.md` rules may narrow domain behavior, but they must not weaken the safety, integrity, proof, efficiency, or STOP boundaries here.

## How to use this file

For normal repository work, apply Core Rules 1–7 in order.

```text
PIN
→ READ MINIMUM
→ DIAGNOSE
→ SELECT EXECUTION MODE
→ TOOL + TRANSFER GATE
→ WRITE ONCE
→ VERIFY + FAILURE POLICY
→ STOP
```

## Execution modes

LazyBuilder uses two named execution modes. These are **work channels**, not branches, skills, or new subsystems.

### `remote_github`

Use `remote_github` when the final state can be produced safely through GitHub-native repository operations.

Typical scope:

- read exact remote branch/file/commit state;
- small bounded UTF-8 documentation or policy changes;
- repository metadata and current-state inspection;
- branch/ref operations permitted by repository policy;
- pull requests, review state, CI/workflow inspection, and promotion operations;
- final remote verification after locally produced work is pushed.

`remote_github` is a repository control/coordination channel. It is **not** a remote shell and must not be stretched into one with temporary Actions, transport helpers, or generated repository machinery.

### `local`

Use `local` when the task needs a real clone/worktree, filesystem, toolchain, binary handling, coordinated patch semantics, or application/runtime execution.

Typical scope:

- source-code implementation and refactors spanning multiple files;
- dependency installation, build commands, local scripts, and test execution;
- binary/heavy project artifacts such as `.glb`, `.blend`, and `.schem`;
- Hunyuan3D-2mv GPU execution;
- Blender execution and addon testing;
- Axiom and Minecraft runtime proof;
- work where real Git staging/diff/commit semantics materially improve safety or reviewability.

Normal `local` repository work still targets branch `develop` unless current authority explicitly says otherwise.

### Naming boundary: `local` vs `Local`

These names are intentionally different:

```text
local  = execution mode / clone / worktree / runtime
Local  = verified integration branch
```

Never interpret `local` mode as permission to edit branch `Local`. Routine work remains on `develop`; `Local` receives only verified squash promotions.

### Mode selection

```text
Need GPU / Blender / Axiom / Minecraft / binary artifacts /
dependency install / build / real tests / coordinated patch semantics?
→ local

Otherwise bounded repository-native state / docs / branch / PR / CI work?
→ remote_github
```

If `remote_github` discovers a genuine local requirement, switch once to `local`. Do not build remote workarounds to emulate missing local capability.

Normal handoff after local implementation:

```text
local
→ targeted local proof
→ commit on develop
→ push develop
→ remote_github confirms remote state / CI / PR / promotion when needed
```

A task may use both modes, but each step should stay in the mode that natively fits it.

# Core Rules

## 1. PIN — establish exact current authority

Before a material change, know the repository, intended working branch/ref, current HEAD when relevant, requested scope, target writability, and selected execution mode.

- Direct branch/file fetch is current-state authority; search is discovery.
- Never silently fall back to the default branch.
- Every write must explicitly target the intended branch/ref when supported.
- `main` is stable-only; `Local` is integration-only; normal Development writes go to `develop`.
- For replacement/deletion, use the current blob/content SHA from the exact target branch.
- Re-check HEAD only when concurrent movement can materially matter.
- Mode switching does not change branch authority.

## 2. READ MINIMUM — read only what can change the decision

Default budget:

```text
owner files      1–3
history reads    0
broad scans      0
```

After mandatory Development boot, open more only for a concrete unresolved question. Truncated/paginated output is incomplete evidence, not proof of absence.

## 3. DIAGNOSE — fix the first wrong owner

```text
requirement / reference interpretation wrong
→ semantic/source owner

generation procedure wrong
→ generation owner

Blender preparation contract wrong
→ Blender owner

Minecraft conversion behavior wrong
→ Minecraftize owner

export correct + test stale
→ test/validation owner

repository routing/CI wrong
→ governance/workflow owner

derived schematic wrong
→ first upstream canonical/implementation owner
```

Do not widen Maintenance into redesign. `No change required` is valid when current behavior already satisfies the requirement.

## 4. TOOL + TRANSFER GATE — choose a method that natively fits

Use the selected execution mode and simplest capability that safely produces the required final state.

```text
exact remote current file/branch or bounded repo-native text change
→ remote_github

coherent multi-file source work / patch semantics / dependencies /
binaries / build / local test / application runtime
→ local

final artifact cannot be transferred safely by active capability
→ Manual Handoff
```

### Transfer gate before first repository mutation

Establish:

```text
final content/artifact ready?
exact repo/ref/path known?
complete logical file set known?
selected mode can carry the real payload?
method preserves acceptable repository history?
```

Never create placeholder final files, transfer-only loaders, base64 stand-ins for normal binary assets, temporary workflows, or alternate repository structures merely to bypass a connector limit.

### Manual Handoff

When direct transfer does not fit:

1. stop the unsupported path;
2. finish and validate the exact artifact locally when possible;
3. provide the exact file/ZIP to the user;
4. provide repository, branch, destination, action, and expected result;
5. never claim GitHub contains it until upload actually occurs.

## 5. WRITE ONCE — deliver one meaningful logical state

Prepare the complete intended logical result before the first branch mutation.

- Same-file/overlapping mutations are serial.
- One intentional write per file is the default, but one logical multi-file delivery should not become one commit per file merely because a connector works that way.
- Use one canonical owner for each durable rule/state where practical.
- Do not add new files, workflows, abstractions, compatibility layers, reports, branches, PRs, issues, or labels unless the task/workflow proves a need.
- If a coherent change needs local Git semantics, use `local` instead of fragmenting it through remote file writes.

### Commit discipline

A commit is a categorized logical delivery, not a file save or tool call.

Default message format:

```text
<type>(<optional-scope>): <concise logical outcome>
```

Categories:

```text
feat:      new capability
fix:       behavior correction
refactor:  internal restructuring without intended behavior change
docs:      documentation/policy-only change
test:      test-contract-only change
ci:        workflow/CI change
build:     dependency/toolchain change
release:   explicit release/publish state
chore:     bounded maintenance when no better category fits
```

Working commits on `develop` may be granular when useful. One approved `develop` → `Local` promotion becomes exactly one squash commit. `main` stable promotions use merge commits.

## 6. VERIFY + FAILURE POLICY

Run the cheapest proof that can falsify the changed claim.

- Documentation/routing changes → repository contract/link/owner checks.
- Minecraftize code changes → targeted executable tests for affected geometry/block-state behavior.
- `.schem` format claim → writer/parser/static format proof where available.
- Axiom import/Minecraft placement → actual Axiom/Minecraft runtime proof in `local` mode.
- Hunyuan/Blender claim → actual local GPU/Blender execution in `local` mode.
- Only completed successful checks are PASS.
- Never weaken a valid test/workflow merely to obtain green status.

Failure handling:

| Failure class | Action |
|---|---|
| known capability mismatch | STOP method; 0 retries; switch to the fitting mode/handoff |
| permission/safety denial | STOP operation |
| genuinely uncertain capability | at most 1 bounded probe |
| malformed valid request / 422 | correct once |
| missing/inaccessible / 404 | verify exact repo/ref/target once |
| stale SHA / 409 | refetch relevant state once and retry |
| 429 | respect rate limit |
| 5xx/timeout/unknown mutation | inspect target state before retry |
| same-cause failure with new plausible evidence | maximum 2 attempts |

Switching mode does not reset the failure budget for the same diagnosed cause. Do not reinterpret a known limitation as an invitation to invent transfer architecture.

## 7. STOP — completion is a terminal state

Stop when:

```text
requested outcome + relevant proof satisfied
→ STOP

confirmed capability mismatch + fitting mode/fallback delivered
→ STOP

operation blocked by authoritative safety/permission boundary
→ report boundary → STOP
```

Do not automatically audit another layer, start the next backlog item, add compatibility support, or promote branches after the requested boundary is complete.

# Local workspace synchronization

For an ordinary clean local start:

```bash
git fetch origin
git switch develop
git status --short
git pull --ff-only origin develop
```

If local changes exist, preserve or intentionally discard them before synchronization. Do not use destructive reset as the normal start procedure.

After an approved `develop` → `Local` squash promotion, a pre-squash local `develop` chain may diverge from the synchronized remote branch. Preserve any work that still matters first, then follow the reset procedure documented in `CONTRIBUTING.md`.

# Branch promotion rules

## `develop` → `Local`

- source must be `develop`;
- Local promotion verification must pass;
- PR represents one approved logical update;
- merge method is squash;
- result adds exactly one Local commit;
- synchronize/reset `develop` to resulting `Local` HEAD before new Development.

## `Local` → `main`

- source must be `Local`;
- stable verification must pass;
- promotion requires explicit approval;
- merge method is normal merge commit;
- main-only stable marker is not synchronized back into lower branches;
- tags/releases are separate publishing actions.

# Runtime proof boundary

Repository CI and `remote_github` can prove remote/static contracts only. They cannot prove:

- Hunyuan3D-2mv actually runs on a specific GPU setup;
- generated GLB quality;
- Blender viewport/addon behavior;
- Axiom import success;
- Minecraft placement/visual quality.

Those claims require matching `local` runtime evidence. Do not substitute remote/static confidence for executed proof.
