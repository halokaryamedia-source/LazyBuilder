# Foundation Policy

This directory stores durable LazyBuilder production policy. Detailed execution mechanics belong in `kits/lazy-builder/`; current continuation belongs in `docs/knowledge/next-action.md`.

## Canonical Flow owners

| Flow | Policy owner |
|---|---|
| Product boundaries | `00-product-boundaries.md` |
| End-to-end production sequence | `01-production-flow.md` |
| Reference intake | `02-reference-intake.md` |
| Hunyuan3D-2mv generation | `03-hunyuan-generation.md` |
| Blender target preparation | `04-blender-target-preparation.md` |
| Minecraftize conversion | `05-minecraftize-conversion.md` |
| Schematic validation / Axiom handoff | `06-schematic-validation-handoff.md` |

Foundation policy changes only when the durable product contract changes. Do not use this directory for active task notes or one-off implementation detail.
