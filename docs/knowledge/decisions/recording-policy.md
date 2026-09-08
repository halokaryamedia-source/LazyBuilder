# Decision Recording Policy

Use this guide to decide where a LazyBuilder change belongs and when ordinary bounded work should become a durable decision.

## Source-of-truth routing

- current active task/status → `docs/knowledge/next-action.md`;
- durable decision/reason → `docs/knowledge/decisions/`;
- stable production policy → `docs/foundation/`;
- current implementation ownership → `docs/knowledge/ownership.md`;
- evidence/findings → `docs/knowledge/reviews/`;
- future/non-active work → `docs/knowledge/operations/backlog.md`;
- project-specific state → active external/local workspace package.

Do not create a second planning/state hierarchy.

## When to record a durable decision

Record when at least one is true:

- the choice changes architecture/workflow across sessions;
- several owners depend on the same reason;
- a tradeoff/constraint must survive chat history;
- an old method/provider is explicitly superseded/retired;
- future agents need the **why**, not only the resulting diff.

Do not create a decision for every wording fix, local bug, generated file, or obvious implementation detail.

## Decision shape

```text
Context
Decision
Why
Tradeoffs / not chosen
Evidence / validation boundary
Follow-up owner
```

A short entry in the decision index is preferred. Create a dedicated note only when reasoning is substantial enough to justify it.

## Cross-owner threshold

Escalate to a coordinated durable note only when multiple owners must change as one contract, a migration/compatibility promise spans phases, several sessions need one architectural contract, or existing `next-action` + decision index cannot represent the tradeoff clearly.

## Change rules

- solve the verified problem with the smallest complete change;
- reuse current owners before adding files/skills/abstractions;
- do not add provider/fallback/compatibility layers without evidence;
- references remain authority/evidence, not excuses for parallel architectures;
- unavailable local runtime proof remains an evidence limitation, not a reason to invent more process.
