# Skill Activation Matrix

Use only when specialist selection is genuinely ambiguous.

| Task | Work mode | Skill |
|---|---|---|
| Inspect/recover repository context | Plan | none |
| Create/revise a build through current LazyBuilder pipeline | Production Execution | `build-production` |
| Change LazyBuilder architecture/workflow/converter/export behavior | Development | `development-brief`; optionally `build-production` if product semantics matter |
| Fix isolated technical defect with settled semantics | Maintenance | none by default; exact kit owner |
| Change GitHub branch/promotion/transfer policy | Development | `development-brief`; `GITHUB_RULES.md` owner |
| Decide whether a new 3D provider should enter MVP | Plan or Development depending requested action | `development-brief` only if implementing policy change |

## Selection rule

Use the smallest useful set. Development gets at most one product specialist in addition to `development-brief`. Do not load a specialist because its files are adjacent to the changed code.
