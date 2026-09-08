# Repository Knowledge

This directory is the navigation and operating-memory layer for LazyBuilder. It does not define a second boot policy or duplicate contracts owned by root/foundation/kits.

## Boot ownership

Root `../../AGENTS.md` owns how a session boots. Do not broad-read every knowledge file by default.

## Current owners

| Need | Owner |
|---|---|
| Active continuation / resume checkpoint | `next-action.md` |
| Detailed work-routing explanation | `work-routing.md` |
| Repository/code/procedure ownership | `ownership.md` |
| Source/state authority | `source-authority.md` |
| Development lifecycle overview | `work-modes/development.md` |
| Maintenance workflow | `work-modes/maintenance.md` |
| Skill inventory | `skills/README.md` |
| Ambiguous specialist selection | `skills/activation-matrix.md` |
| Durable decision index | `decisions/README.md` |
| Current validation evidence | `reviews/current-validation.md` |
| Historical review evidence | `reviews/history/` |
| Future/non-active work | `operations/backlog.md` |
| Boot/routing regression scenarios | `operations/boot-baseline.md` |

## Directory structure

```text
docs/knowledge/
├── README.md
├── next-action.md
├── work-routing.md
├── ownership.md
├── source-authority.md
├── work-modes/
├── skills/
├── decisions/
├── reviews/
└── operations/
```

## Separation rule

```text
active continuation       → next-action.md
durable choice/reason     → decisions/
current proof             → reviews/current-validation.md
historical proof          → reviews/history/
future/non-active work    → operations/backlog.md
production policy         → ../foundation/
project-specific state    → external/local project package under ../../workspace/
```

Historical reviews/decisions are evidence and rationale, not automatic current work.
