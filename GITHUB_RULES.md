# GitHub Rules

Canonical operating rules for AI/ChatGPT working with GitHub in this repository.

Repository-specific `AGENTS.md` rules may narrow domain behavior, but they must not weaken the safety, integrity, proof, efficiency, or STOP boundaries here.

## How to use this file

For normal repository work, apply Core Rules 1–7 in order.

```text
PIN
→ READ MINIMUM
→ DIAGNOSE
→ TOOL + TRANSFER GATE
→ WRITE ONCE
→ VERIFY + FAILURE POLICY
→ STOP
```

# Core Rules

## 1. PIN — establish exact current authority

Before a material change, know the repository, intended working branch/ref, current HEAD when relevant, requested scope, and whether the target is writable.

- Direct branch/file fetch is current-state authority; search is discovery.
- Never silently fall back to the default branch.
- Every write must explicitly target the intended branch/ref when supported.
- `main` is stable-only; `Local` is integration-only; normal Development writes go to `develop`.
- For replacement/deletion, use the current blob/content SHA from the exact target branch.
- Re-check HEAD only when concurrent movement can materially matter.

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

Use the simplest capability that safely produces the required final state.

```text
exact current file/branch
→ direct GitHub fetch

one small bounded text file
→ Contents API

coherent multi-file logical delivery / commit atomicity matters / binary or patch semantics required
→ proper Git workspace or known-safe atomic Git capability

final artifact cannot be transferred safely by active capability
→ Manual Handoff

Hunyuan / Blender / Axiom / Minecraft runtime claim
→ actual matching local runtime capability
```

### Transfer gate before first repository mutation

Establish:

```text
final content/artifact ready?
exact repo/ref/path known?
complete logical file set known?
method can carry the real payload?
method preserves acceptable repository history?
```

Never create placeholder final files, transfer-only loaders, base64 stand-ins for normal binary assets, temporary workflows, or alternate repository structures merely to bypass a connector limit.

### Manual Handoff

When direct transfer does not fit:

1. stop the unsupported path;
2. finish and validate the exact artifact locally;
3. provide the exact file/ZIP to the user;
4. provide repository, branch, destination, action, and expected result;
5. never claim GitHub contains it until upload actually occurs.

## 5. WRITE ONCE — deliver one meaningful logical state

Prepare the complete intended logical result before the first branch mutation.

- Same-file/overlapping mutations are serial.
- One intentional write per file is the default, but one logical multi-file delivery should not become one commit per file merely because a connector works that way.
- Use one canonical owner for each durable rule/state where practical.
- Do not add new files, workflows, abstractions, compatibility layers, reports, branches, PRs, issues, or labels unless the task/workflow proves a need.

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
- Axiom import/Minecraft placement → actual Axiom/Minecraft runtime proof.
- Hunyuan/Blender claim → actual local GPU/Blender execution.
- Only completed successful checks are PASS.
- Never weaken a valid test/workflow merely to obtain green status.

Failure handling:

| Failure class | Action |
|---|---|
| known capability mismatch | STOP method; 0 retries |
| permission/safety denial | STOP operation |
| genuinely uncertain capability | at most 1 bounded probe |
| malformed valid request / 422 | correct once |
| missing/inaccessible / 404 | verify exact repo/ref/target once |
| stale SHA / 409 | refetch relevant state once and retry |
| 429 | respect rate limit |
| 5xx/timeout/unknown mutation | inspect target state before retry |
| same-cause failure with new plausible evidence | maximum 2 attempts |

Do not reinterpret a known limitation as an invitation to invent transfer architecture.

## 7. STOP — completion is a terminal state

Stop when:

```text
requested outcome + relevant proof satisfied
→ STOP

confirmed capability mismatch + fitting fallback delivered
→ STOP

operation blocked by authoritative safety/permission boundary
→ report boundary → STOP
```

Do not automatically audit another layer, start the next backlog item, add compatibility support, or promote branches after the requested boundary is complete.

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

Repository CI can prove repository/static contracts only. It cannot prove:

- Hunyuan3D-2mv actually runs on a specific GPU setup;
- generated GLB quality;
- Blender viewport/addon behavior;
- Axiom import success;
- Minecraft placement/visual quality.

Those claims require the matching runtime evidence. Do not substitute static confidence for executed proof.
