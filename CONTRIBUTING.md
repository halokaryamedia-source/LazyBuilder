# Contributing

LazyBuilder is currently a personal/internal development repository. Public visibility is for development convenience and does not imply that external contributions or reuse are automatically accepted.

## Branch model

```text
develop
→ active repository development
→ working commits may be numerous

Local
→ verified integration / stable working baseline
→ exactly one squash commit per approved promoted update

main
→ stable repository history
```

Routine repository work happens on `develop`. Do not make routine changes directly on `Local` or `main`.

### Promote `develop` → `Local`

Use a dedicated pull request when one coherent development outcome is ready for the verified baseline.

The PR must:

- come from `develop`;
- pass `Local Promotion Verify`;
- represent one approved logical update;
- use **Squash and merge** so the update becomes exactly one new commit on `Local`.

After squash merge, synchronize/reset `develop` to resulting `Local` HEAD before starting the next development cycle.

```text
one approved develop → Local promotion
= exactly +1 commit on Local
```

For a local clone, preserve any uncommitted work first, then:

```bash
git fetch origin
git switch develop
git reset --hard origin/develop
```

### Promote `Local` → `main`

Use a dedicated stable pull request only when an explicitly approved update needs to become stable repository state.

The PR must:

- come from `Local`;
- pass `Release Verify`;
- use a normal merge commit so `main` records the stable boundary explicitly.

Do not reset `Local` to the resulting `main` merge commit. Tags/releases are separate explicit publishing actions.

## Before committing

Run the cheapest relevant proof for the changed claim.

Repository/documentation changes:

```bash
python tools/verify_repository.py
```

Future executable Minecraftize changes should add targeted tests when the behavior exists. Do not create speculative test frameworks before executable behavior is present.

## CI behavior

- `Repository Verify` is the current static repository safety net.
- `Local Promotion Verify` is the integration boundary for `develop` → `Local`.
- `Release Verify` is the stable boundary for `Local` → `main`.
- Hunyuan, Blender, Axiom, and Minecraft runtime claims remain local-runtime evidence and are not proved by GitHub CI.

## Commit discipline

```text
feat:      new capability
fix:       behavior correction
refactor:  internal restructuring without intended behavior change
docs:      documentation/policy-only change
test:      test-only change
ci:        workflow/CI change
build:     dependency/toolchain change
release:   explicit release/publish state
chore:     bounded maintenance when no better category fits
```

`Local` is milestone history. `main` is stable history. Do not use transfer experiments, placeholder files, generated fragments, or temporary helper architecture as permanent repository history.

## Project-data boundary

The public repository tracks the LazyBuilder **system**, not live project packages.

Project-specific packages under `workspace/active/<project>/` and `workspace/archive/<project>/` are ignored by Git and must remain local or in another authorized/private location.

Do not add credentials, private client/reference material, generated project GLBs/Blend files/schematics, or temporary transfer payloads without an explicit public-visibility decision.

See `SECURITY.md`.

## Pull requests

Use `.github/PULL_REQUEST_TEMPLATE.md` and keep a PR scoped to one logical delivery. `develop` → `Local` is squash. `Local` → `main` is a normal merge commit.

## License

The repository is not open source. External reuse, redistribution, or commercial use requires prior written permission from the copyright holder. See `LICENSE`.
