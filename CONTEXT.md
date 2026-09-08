# LazyBuilder Context

Status: active R&D / pre-MVP  
Development branch: `develop`  
Verified integration baseline: `Local`  
Stable branch: `main`

This file is the stable orientation layer for new sessions and repository Development.

## Product

LazyBuilder turns non-Minecraft visual references into a Minecraft Java schematic through one intentionally narrow production chain:

```text
multi-view reference images
→ Hunyuan3D-2mv
→ model.glb
→ Blender
→ light target cleanup
→ Minecraftize
→ Minecraft block preview
→ .schem
→ Axiom
→ Minecraft Java world
```

The product does not attempt to train a new 3D model. Existing generation is reused; custom development is concentrated on making Blender geometry convert into useful Minecraft-native block placement.

## Canonical production sequence

```text
Flow 1  Repository Boot & Project Memory
Flow 2  Reference Intake & Multi-view Recovery
Flow 3  Hunyuan3D-2mv Shape Generation
Flow 4  Blender Target Preparation
Flow 5  Minecraftize Conversion
Flow 6  Schematic Validation & Axiom Handoff
```

Agent work modes and product Flows are separate layers.

## Branch authority

```text
develop
→ active repository Development
→ working commits may be numerous

Local
→ verified integration / stable working baseline
→ exactly one squash commit per approved promoted update

main
→ stable repository history
→ receives explicit Local stable promotions
```

After `develop` → `Local` squash promotion, synchronize/reset `develop` to resulting `Local` HEAD. Stable `main` merge markers do not flow back into lower branches.

## Stable authority shape

```text
current user instruction
+ approved build decisions
+ authoritative reference images / dimensions
→ generated Hunyuan target hypothesis
→ cleaned Blender working target
→ Minecraftize block model
→ schematic delivery
→ Axiom/Minecraft runtime evidence
```

Authority decreases downstream. Generated 3D, preview, schematic, and final screenshots do not silently redefine the reference requirement.

## Locked MVP stack

- **3D generation:** Hunyuan3D-2mv only.
- **3D workspace:** Blender 5.2.x LTS.
- **Custom conversion core:** Blender addon `Minecraftize`.
- **Schematic writer:** `mcschematic` unless a demonstrated compatibility defect requires reassessment.
- **Final editor / placement:** Axiom.
- **Target:** Minecraft Java Edition.

## Explicitly inactive scope

Do not add by default:

- MCP automation;
- Tripo, TRELLIS, Pixal3D, or multi-model routing;
- custom foundation model training;
- custom schematic/NBT format;
- direct Minecraft world injection;
- direct Axiom automation;
- complex optimizer/ML solver before rule-based conversion proves insufficient;
- broad Minecraft block-family support before a real build requires it.

## Product package boundary

`kits/lazy-builder/` is the single procedure/implementation owner for Flow 2–6.

```text
intake/        reference-input procedure
generation/    Hunyuan3D-2mv procedure
blender/       target-model preparation contract
minecraftize/  Minecraft conversion contract and future addon code
schematic/     export contract
validator/     proof / handoff contract
```

## Project-data boundary

The public LazyBuilder repository owns the system, not live build/project data.

`workspace/active/` and `workspace/archive/` are local/external mount conventions. Their project subdirectories are ignored by Git; only guidance is tracked.

Do not commit private references, client imagery, generated GLBs, `.blend` work files, output schematics, credentials, or other project production state unless an explicit visibility decision authorizes it.

## Operating direction

- recover repository/project context before asking the user to repeat it;
- use the smallest owner that can settle the current decision;
- preserve the single-provider Hunyuan3D-2mv choice until evidence proves it inadequate;
- prove `.schem → Axiom` before building sophisticated conversion logic;
- build Minecraftize incrementally: full blocks first, then stairs, then slabs;
- add wall/fence/pane/decorative blocks only from real use cases;
- prefer existing tools over custom infrastructure;
- use the cheapest proof that can falsify the active claim;
- historical audits/backlog/TODOs are not active work unless promoted by current continuation;
- `No change required` is valid;
- stop when requested scope is complete and sufficiently proven.

## Repository map

```text
AGENTS.md            top-level routing / continuity rules
GITHUB_RULES.md      GitHub execution / history / proof discipline
CONTEXT.md           stable product/repository orientation
docs/foundation/     durable Flow policy
docs/knowledge/      continuation, ownership, decisions, evidence, backlog
.agents/skills/      reusable work-mode/product judgment
kits/lazy-builder/   Flow 2–6 procedure + implementation owner
workspace/           ignored local/external project mount convention
tools/               repeatable repository verification
.github/             CI / ownership / promotion gates
```

## Continuation

For new-chat context recovery and non-trivial Development, read `docs/knowledge/next-action.md` after this file.

`next-action.md` owns the active continuation boundary; current source/state owns actual implementation truth. If they disagree, reconcile the stale owner before continuing.
