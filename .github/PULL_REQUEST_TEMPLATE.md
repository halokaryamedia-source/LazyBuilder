## Purpose

Describe the one logical outcome this pull request delivers.

## Target boundary

- [ ] `develop` work / review only
- [ ] `develop` → `Local` verified integration promotion
- [ ] `Local` → `main` stable promotion

## Scope

**Changed owners:**

**Intentionally not changed:**

## Verification

- [ ] Cheapest relevant proof completed
- [ ] `python tools/verify_repository.py` when repository contracts changed
- [ ] Targeted executable/runtime proof when product behavior changed
- [ ] Local promotion gate for `develop` → `Local`
- [ ] Stable release gate for `Local` → `main`

Evidence / relevant result:

## Repository hygiene

- [ ] No credentials, private references, or live project-package data added
- [ ] No generated/transfer-only artifact was promoted to source of truth
- [ ] No unrelated cleanup/refactor was bundled into this change

## Local promotion contract

For `develop` → `Local` promotion:

- [ ] This PR represents one approved logical update
- [ ] Merge method will be **Squash and merge**
- [ ] Result must add exactly **one** new commit to `Local`
- [ ] After merge, `develop` will be synchronized/reset to resulting `Local` HEAD before new work begins

## Stable main promotion contract

For `Local` → `main` promotion:

- [ ] Source branch is `Local`
- [ ] `Release Verify` passes
- [ ] Merge method will be a normal **merge commit**
- [ ] The resulting `main` stable marker will not be synchronized back into `Local` or `develop`

Tags/releases are separate explicit publishing actions.
