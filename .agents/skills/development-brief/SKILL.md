---
name: development-brief
description: Mandatory front door for non-trivial LazyBuilder repository/system Development. Recover current continuity, identify the actual requirement and first wrong owner, define the smallest scope with 2–5 falsifiable acceptance criteria and a proof budget, then execute with at most one useful product specialist.
---

# Development Brief

Turn a repository/system create/change request into the smallest grounded development contract, then continue into implementation when requested reversible scope is clear.

Root `AGENTS.md` owns work mode, continuity, authority, action intent, evidence, and skill budget. `GITHUB_RULES.md` owns GitHub execution.

## Entry boundary

Use for changes to how LazyBuilder itself works: policy, skills, workflow, Hunyuan integration contract, Blender preparation contract, Minecraftize behavior, schematic export, validation, repository structure, or shared tooling.

Normal use of LazyBuilder to produce a project build is Production Execution and routes to `build-production`.

A read-only inspect/understand/recover request is Plan behavior and stops after reporting current state unless implementation was also requested.

## Mandatory Development continuity

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules when GitHub work is material
→ CONTEXT.md
→ docs/knowledge/next-action.md
→ smallest current owner/evidence that can change the decision
```

Do not ask the user to restate information recoverable from current repository/source state.

If continuity and implementation disagree:

```text
verify current owner
→ identify stale continuity vs stale implementation
→ reconcile stale owner
→ continue from actual state
```

## Minimal development contract

Before writing, establish:

```text
Goal / actual requirement
First wrong owner
In scope / out of scope
Acceptance criteria: 2–5
Proof budget
Unresolved material decision only when one really remains
```

Treat a user-proposed method/reference as input to the requirement, not automatically the requirement itself.

## Procedure

1. Recover current context and diagnose actual behavior.
2. Identify the first semantic/implementation/test/workflow owner that is wrong or missing.
3. Bound the smallest complete change and 2–5 falsifiable acceptance criteria.
4. Choose the cheapest proof that can falsify the changed claim.
5. Use `build-production` only when product-domain judgment adds real value; pure repository mechanics do not need it.
6. Execute through completion once the reversible scope is clear.
7. Re-check original goal, scope, acceptance criteria, and actual proof.
8. Update `next-action.md` only when continuation/blocker/milestone/next meaningful objective changed.

`No change required` remains a valid result.

## User-facing brief

Expose only when it materially helps:

```text
Tujuan:
Hasil yang dituju:
Tidak diubah:
Cara memastikan benar:
```

Do not turn internal planning into another deliverable.
