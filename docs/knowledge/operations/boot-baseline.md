# Boot and Routing Baseline

This baseline protects context recovery and execution routing without turning boot into repository-wide reading or another workflow engine.

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
→ choose execution mode
→ implementation after task is grounded
```

Pass when stable boundaries and active continuation are preserved, old backlog/review items are not promoted automatically, and execution uses the capability that actually fits.

## Scenario C — bounded Maintenance

```text
AGENTS.md
→ GITHUB_RULES.md Core Rules when material
→ exact defect/owner
→ choose fitting execution mode
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
→ local when generation/Blender/Axiom/Minecraft runtime is required
```

Normal production does not invoke development-brief merely because project files are created.

## Scenario E — bounded repository-native change

Example: update one policy sentence, inspect CI, or prepare a repository PR.

```text
exact remote state
→ remote_github
→ bounded change/operation
→ repository proof when applicable
→ STOP
```

Pass when the task does not create a local-workspace framework or unnecessary transfer path.

## Scenario F — real implementation/runtime work

Example: implement Minecraftize sampling, install a dependency, generate a GLB, or validate Axiom import.

```text
pin current develop state
→ local
→ real workspace/tool/runtime
→ targeted proof
→ commit/push develop when repository source changed
→ remote_github for remote CI/PR/promotion when needed
```

Pass when GitHub Actions or remote helper files are not used to imitate the missing local runtime.

## Canonical routing regression set

| Example request | Expected route | Must not |
|---|---|---|
| `Amati repo ini dan jelaskan statusnya.` | Plan / observe only | edit files, start next-action, broad CI |
| `Perbaiki typo di satu owner Markdown.` | Maintenance + `remote_github` when a bounded remote write fits | require Blender/local runtime |
| `Implement Minecraftize full-block sampling dan test.` | Development + `local` | fragment source implementation into remote file-write commits |
| `Generate model dari 4 reference.` | Production Execution + `local` Hunyuan runtime | claim generation from static GitHub evidence |
| `Cek workflow promotion yang gagal.` | Maintenance + `remote_github` | run Hunyuan/Blender |
| `Buat model dari 4 reference ini dengan pipeline yang sudah ada.` | Production Execution → build-production | redesign repository or add provider |
| `Fix stair facing yang salah; target mesh sudah benar.` | Maintenance → Minecraftize owner, normally `local` for executable proof | reopen Hunyuan/reference design |
| `Ubah cara LazyBuilder memilih stair/slab.` | Development → development-brief → Minecraftize owner → `local` | treat as one-off project edit |
| `Tambahkan model 3D provider kedua.` | Development/decision boundary | add immediately because provider exists |
| `Change GitHub promotion behavior.` | Development → GITHUB_RULES owner → `remote_github` when bounded | modify product conversion contracts |

## Naming regression

```text
local  = execution mode
Local  = verified integration branch
```

Pass only when sessions keep this distinction explicit. `local` mode is not authorization to edit branch `Local` directly.

## Pass conditions

- user is not asked to repeat recoverable context;
- observe requests remain read-only unless implementation also requested;
- non-trivial Development recovers stable context + continuation first;
- bounded work does not broad-read unrelated history;
- correct owner is reached without redundant skills;
- `remote_github` is used for fitting remote repository operations;
- `local` is used for real workspace/runtime needs;
- mode switching occurs only when capability requirements change;
- branch `Local` is never confused with execution mode `local`;
- backlog/reviews/old TODOs do not become active automatically;
- evidence expectations match actual execution capability;
- no ceremonial telemetry/session log/extra state system is created.

Add or change a scenario only after a real routing failure exposes a missing case.
