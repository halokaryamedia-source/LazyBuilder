# Boot and Routing Baseline

This baseline protects context recovery without turning boot into repository-wide reading. It is a small routing regression contract, not another workflow engine.

## Scenario A — new chat, observe/recover only

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules when material
→ CONTEXT.md
→ next-action.md
→ smallest owner needed
→ report understanding
→ STOP / NO EDIT
```

Pass when the agent can state what LazyBuilder is, current active boundary/next step, constraints, and likely owner without starting implementation or asking the user to reconstruct recoverable history.

## Scenario B — non-trivial repository Development

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules
→ CONTEXT.md
→ next-action.md
→ development-brief
→ smallest relevant owner/source
→ implementation after task is grounded
```

Pass when stable boundaries and active continuation are preserved and old backlog/review items are not promoted automatically.

## Scenario C — bounded Maintenance

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules when material
→ exact defect/owner
→ targeted proof
→ STOP
```

Wider context may be skipped only when it cannot materially change the correction.

## Scenario D — normal build Production Execution

```text
AGENTS.md
→ current project/reference state
→ build-production
→ smallest active kits/lazy-builder owner
```

Normal production does not invoke development-brief merely because project files are created.

## Canonical routing regression set

| Example request | Expected route | Must not |
|---|---|---|
| `Amati repo ini dan jelaskan statusnya.` | Plan / observe only | edit files, start next-action, broad CI |
| `Buat model dari 4 reference ini dengan pipeline yang sudah ada.` | Production Execution → build-production | redesign repository or add provider |
| `Fix stair facing yang salah; target mesh sudah benar.` | Maintenance → Minecraftize owner | reopen Hunyuan/reference design |
| `Ubah cara LazyBuilder memilih stair/slab.` | Development → development-brief → Minecraftize owner | treat as one-off project edit |
| `Tambahkan model 3D provider kedua.` | Development/decision boundary | add immediately because provider exists |
| `Change GitHub promotion behavior.` | Development → GITHUB_RULES owner | modify product conversion contracts |

## Pass conditions

- user is not asked to repeat recoverable context;
- observe requests remain read-only unless implementation also requested;
- non-trivial Development recovers stable context + continuation first;
- bounded work does not broad-read unrelated history;
- correct owner is reached without redundant skills;
- backlog/reviews/old TODOs do not become active automatically;
- evidence expectations match actual execution capability;
- no ceremonial telemetry/session log/extra state system is created.

Add a scenario only after a real routing failure exposes a missing case.
