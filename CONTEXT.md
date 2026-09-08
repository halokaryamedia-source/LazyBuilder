# LazyBuilder Context

Status: active R&D / pre-MVP  
Development branch: `develop`  
Verified integration baseline: `Local`  
Stable branch: `main`

This file is the stable orientation layer for new sessions and repository Development.

## Product

LazyBuilder turns text or non-Minecraft visual references into a Minecraft Java schematic through one intentionally narrow production chain:

```text
TEXT (optional)
→ HunyuanDiT Lite reference image
→ review / approval
        ↘
IMAGE / MULTIVIEW REFERENCES
→ Hunyuan3D-2mv
→ model.glb
→ Blender
→ light target cleanup
→ Minecraftize
→ Minecraft block preview
→ Sponge .schem
→ Axiom client
→ AxiomPaper / Paper placement
→ Minecraft Java world
```

The product does not train a new 3D model. Existing generation is reused; custom development is concentrated on making Blender geometry convert into useful Minecraft-native block placement.

## Canonical production sequence

```text
Flow 1  Repository Boot & Project Memory
Flow 2  Reference Intake / Text Reference / Multi-view Recovery
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
current user instruction / text intent
+ approved build decisions
+ authoritative reference images / dimensions
→ approved generated text reference when text mode is used
→ generated Hunyuan3D target hypothesis
→ cleaned Blender working target
→ Minecraftize block model
→ schematic delivery
→ Axiom/Minecraft runtime evidence
```

Authority decreases downstream. Generated reference images, 3D, preview, schematic, and final screenshots do not silently redefine the upstream requirement.

## Locked MVP stack

- **Text reference only:** HunyuanDiT v1.2 Diffusers Distilled Lite when the user starts from text.
- **3D generation:** Hunyuan3D-2mv only.
- **3D workspace:** Blender 5.2.x LTS.
- **Custom conversion core:** Blender addon `Minecraftize`.
- **Schematic writer:** pinned `mcschematic==11.4.4` while compatible.
- **Schematic format:** Sponge Schematic Version 2 for the current target.
- **Final client editor / placement:** Axiom.
- **Target:** Minecraft Java Edition.

HunyuanDiT is not a second 3D provider. It only creates a reviewable 2D reference so text input can enter the same Hunyuan3D-2mv shape path.

## Current generation input contract

```text
MULTIVIEW (preferred)
front/right/back/left
→ Hunyuan3D-2mv

SINGLE CANONICAL VIEW
front OR right OR back OR left
→ Hunyuan3D-2mv

TEXT
→ HunyuanDiT Lite
→ reference_front.png
→ user approval
→ Hunyuan3D-2mv
```

Do not independently generate four T2I views for MVP. Cross-view identity/proportion drift can make multiview conditioning worse than a single approved canonical reference.

Text-reference and 3D-shape stages run as separate processes so the 8 GB development GPU does not need both models resident simultaneously.

Detailed decision: `docs/knowledge/decisions/text-image-to-3d-input-contract.md`.

## Current Axiom integration baseline

Current research/static baseline is the exact user-supplied Minecraft 1.21.4 environment:

```text
CLIENT
Minecraft Java 1.21.4
Fabric
Axiom 5.3.0
Axiom API family 9
sha256 8026fdb448686cd6db69e69c695fa17f54508f801ddddb3ffeb850b79b04eae5

SERVER
Paper 1.21.4
AxiomPaper 5.0.1+1.21.4
Axiom API family 9
sha256 cecafb3e1beba81245ee5bcfc3251052035526b99bb111127b968b09c92d86c8

SCHEMATIC
Sponge Schematic Version 2
DataVersion 4189
```

Supplied `AxiomPaper 4.0.4` is not part of this baseline because it uses Axiom API version 8.

`AxiomPaper 5.0.4+1.21.4` is only a researched upgrade candidate for a demonstrated slow-update/permission issue or an explicit user upgrade decision. Do not upgrade silently.

### Axiom architecture rule

```text
LazyBuilder / mcschematic
→ .schem
→ Axiom 5.3.0 CLIENT parses the file
→ Clipboard / Placement
→ client block buffer
→ AxiomPaper validates multiplayer session / permission / region / transport
→ Paper world modification
```

This means LazyBuilder does **not** need:

- an Axiom protocol implementation;
- a Paper-side schematic parser;
- direct Axiom automation/MCP;
- `.bp` Blueprint output.

Axiom 5.3.0 recenters imported Sponge schematic coordinates from dimensions. Export tight bounds and do not depend on `Offset`, `WEOffsetX/Y/Z`, or WorldEdit origin metadata to control Axiom's active Clipboard pivot. Final positioning belongs to Axiom Placement/Gizmo.

Normal entities are outside the current Sponge import contract. BlockEntity/NBT support is deferred until a concrete requirement and separate test exist.

Detailed evidence lives in `docs/knowledge/reviews/history/axiom-audit-2026-09-08.md`; the durable decision lives in `docs/knowledge/decisions/axiom-1.21.4-integration-baseline.md`.

## Development operator profile

Preferred repository Development model: **GPT Astra 6 — ExtraHigh**.

The repository is optimized for that high-reasoning workflow through small context packets, explicit ownership, falsifiable acceptance criteria, and deterministic proof. This is not a product dependency and must not introduce model-specific runtime code, hidden-state assumptions, prompt scaffolding frameworks, or duplicate documentation.

Canonical execution principle:

```text
Astra6 reasons about meaning / architecture / diagnosis
→ code performs deterministic computation
→ runtime proves runtime behavior
```

Detailed model-execution rules are owned by `AGENTS.md` and `.agents/skills/development-brief/SKILL.md`. The durable rationale is recorded under `docs/knowledge/decisions/astra6-extrahigh-development-profile.md`.

## Explicitly inactive scope

Do not add by default:

- MCP automation;
- Tripo, TRELLIS, Pixal3D, Hunyuan3D-2 base, or multi-3D-model routing;
- automatic four-view T2I generation;
- custom foundation model training;
- Hunyuan texture generation;
- custom schematic/NBT format;
- direct Minecraft world injection;
- direct Axiom automation/protocol implementation;
- Paper-side schematic parsing;
- Axiom Blueprint `.bp` output;
- entity/NBT support before a concrete need/test;
- packet/rate tuning before observed scale evidence;
- complex optimizer/ML solver before rule-based conversion proves insufficient;
- broad Minecraft block-family support before a real build requires it.

## Product package boundary

`kits/lazy-builder/` is the single procedure/implementation owner for Flow 2–6.

```text
intake/        reference-input procedure
generation/    text-reference + Hunyuan3D-2mv procedure/runtime wrappers
blender/       target-model preparation contract
minecraftize/  Minecraft conversion contract and future addon code
schematic/     export contract
validator/     proof / handoff contract
```

## Project-data boundary

The public LazyBuilder repository owns the system, not live build/project data.

`workspace/active/` and `workspace/archive/` are local/external mount conventions. Their project subdirectories are ignored by Git; only guidance is tracked.

Do not commit private references, client imagery, generated T2I references, generated GLBs, `.blend` work files, output schematics, credentials, Axiom client JARs, model weights, or other project production state unless an explicit visibility decision authorizes it and licensing permits it.

## Operating direction

- recover repository/project context before asking the user to repeat it;
- use the smallest owner that can settle the current decision;
- preserve Hunyuan3D-2mv as the single 3D provider until evidence proves it inadequate;
- treat text-generated reference images as generated hypotheses until user approval;
- run text-reference and 3D shape generation sequentially on the 8 GB GPU;
- keep M1 exact `.schem → Axiom 5.3.0 → AxiomPaper 5.0.1 → Minecraft 1.21.4` runtime proof visibly pending until executed;
- explicit user instruction may advance Flow 3 implementation research/scaffolding in parallel, but no runtime PASS is implied;
- build Minecraftize incrementally: full blocks first, then stairs, then slabs;
- export tight schematic bounds;
- preserve canonical Minecraft BlockState strings and exact current DataVersion;
- add wall/fence/pane/decorative blocks only from real use cases;
- prefer existing official tools over copied/custom infrastructure;
- use Astra6 ExtraHigh reasoning to reduce rework, not to expand scope;
- keep deterministic calculations and file-format mechanics in code rather than prose/model improvisation;
- use the cheapest proof that can falsify the active claim;
- diagnose Axiom failures by first wrong owner: client format/import vs session/permission vs Paper/world/region vs exporter BlockState;
- historical audits/backlog/TODOs are not active work unless promoted by current continuation;
- `No change required` is valid;
- stop when requested scope is complete and sufficiently proven.

## Repository map

```text
AGENTS.md            top-level routing / continuity / model-execution rules
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
