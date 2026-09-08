# LazyBuilder Context

Status: active R&D / pre-MVP  
Development branch: `develop`  
Verified integration baseline: `Local`  
Stable branch: `main`

This file is the stable orientation layer for new sessions and repository Development.

## Product

LazyBuilder turns text or non-Minecraft visual references into a Minecraft Java schematic through one intentionally narrow chain:

```text
TEXT (optional)
→ Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
→ reference_front.png
→ review / approval
        ↘
IMAGE / MULTIVIEW REFERENCES
→ Hunyuan3D-2mv
→ model.glb
→ Blender 5.2.x LTS
→ Minecraftize
→ mcschematic==11.4.4
→ Sponge .schem
→ Axiom
→ Minecraft Java Edition
```

The product does not train a new 3D model. **Hunyuan3D-2mv remains the only 3D provider.** HunyuanDiT only generates a reviewable 2D reference when the starting input is text.

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

## Stable source authority

```text
current user instruction / text intent
+ approved build decisions
+ authoritative reference images / dimensions
→ approved generated text reference when text mode is used
→ Hunyuan3D mesh as generated geometric hypothesis
→ Blender working target
→ Minecraftize block model
→ .schem
→ Axiom/Minecraft runtime acceptance evidence
```

Generated references and downstream artifacts do not silently redefine upstream intent.

## Locked MVP stack

- **Text reference only:** `Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled`.
- **3D generation:** Hunyuan3D-2mv only.
- **3D workspace:** Blender 5.2.x LTS.
- **Custom conversion core:** Minecraftize.
- **Schematic writer:** mcschematic==11.4.4 while compatibility remains proven.
- **Schematic format:** Sponge Schematic Version 2 for the current target.
- **Final editor / placement:** Axiom.
- **Target:** Minecraft Java Edition.

## Current generation input contract

```text
MULTIVIEW (preferred)
front / right / back / left
→ Hunyuan3D-2mv

SINGLE CANONICAL IMAGE
one of front / right / back / left
→ Hunyuan3D-2mv

TEXT
→ Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
→ reference_front.png
→ USER REVIEW / APPROVAL
→ Hunyuan3D-2mv
```

Do not independently generate four text-to-image views for MVP. Cross-view identity/proportion drift can make conditioning worse than one approved canonical reference.

Text-reference and 3D-shape stages run as **separate processes** so the RTX 3070 8 GB development GPU does not need both models resident simultaneously.

Current first-proof shape baseline:

```text
model: tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
texture: OFF
```

Fast/Turbo variants are not automatically routed. Standard is proven first; variant comparison requires measured same-reference evidence and downstream Minecraft usefulness.

Detailed decision: `docs/knowledge/decisions/text-image-to-3d-input-contract.md`.

## Current Axiom integration baseline

Current research/static baseline is the exact user-supplied Minecraft 1.21.4 environment:

```text
CLIENT
Minecraft Java 1.21.4
Fabric
Axiom 5.3.0
Axiom API family 9

SERVER
Paper 1.21.4
AxiomPaper 5.0.1+1.21.4
Axiom API family 9

SCHEMATIC
Sponge Schematic Version 2
DataVersion 4189
```

Supplied AxiomPaper 4.0.4 is outside this baseline because it uses API family 8. AxiomPaper 5.0.4+1.21.4 remains only a conditional upgrade candidate for a matching measured problem or explicit user decision.

Canonical architecture:

```text
LazyBuilder / mcschematic
→ .schem
→ Axiom 5.3.0 CLIENT parses the file
→ Clipboard / Placement
→ client block buffer
→ AxiomPaper validates multiplayer session / permission / region / transport
→ Paper world modification
```

LazyBuilder therefore does not need an Axiom protocol implementation, a Paper-side schematic parser, direct Axiom automation/MCP, or Blueprint `.bp` output for MVP.

## Development operator profile

Preferred repository Development model: **GPT Astra 6 — ExtraHigh**.

Canonical execution principle:

```text
Astra6 reasons about meaning / architecture / diagnosis
→ code performs deterministic computation
→ runtime proves runtime behavior
```

The repository remains model-portable; no hidden reasoning history or model-specific runtime framework is product authority.

## Explicitly inactive scope

Do not add by default:

- Tripo, TRELLIS, Pixal3D, Hunyuan3D-2 base, or multi-3D-model routing;
- automatic four-view T2I generation;
- automatic Fast/Turbo routing;
- Hunyuan texture generation;
- custom foundation model training;
- custom schematic/NBT format;
- entity/NBT support without a concrete requirement/test;
- direct Minecraft world injection;
- direct Axiom automation/protocol implementation;
- Paper-side schematic parsing;
- Axiom Blueprint `.bp` output;
- packet/rate tuning before observed scale evidence;
- MCP orchestration without a demonstrated workflow need;
- complex optimizer/ML solver before rule-based conversion proves insufficient;
- broad Minecraft block-family support before a real build requires it.

## Product package boundary

`kits/lazy-builder/` is the single procedure/implementation owner for Flow 2–6.

```text
intake/        reference/text intake + approval procedure
generation/    text-reference + Hunyuan3D-2mv runtime wrappers
blender/       target-model preparation contract
minecraftize/  Minecraft conversion contract
schematic/     export contract
validator/     proof / handoff contract
```

## Project-data boundary

The public repository owns the system, not live project data. `workspace/active/` and `workspace/archive/` remain local/external conventions.

Do not commit private references, generated T2I references, generated GLBs, `.blend`, output schematics, model weights, credentials, Axiom JARs, or Minecraft worlds unless an explicit visibility/licensing decision permits it.

## Operating direction

- recover context before repeating questions;
- use the smallest canonical owner;
- keep Hunyuan3D-2mv as the single 3D provider until evidence proves otherwise;
- treat text-generated references as hypotheses until approval;
- run text-reference and shape generation sequentially on 8 GB VRAM;
- keep M1 Axiom/Paper/Minecraft runtime proof visibly pending until actually executed;
- explicit user instruction may advance generation implementation in parallel without converting M1 to PASS;
- prove the first local GLB before implementing Minecraftize runtime code;
- build Minecraftize full blocks → stairs → slabs;
- use deterministic code for repeatable transforms/state/file mechanics;
- use the cheapest proof that can falsify the active claim;
- do not promote `develop` to `Local` without the repository promotion boundary being satisfied;
- stop when current scope is complete.

## Repository map

```text
AGENTS.md            routing / continuity / model-execution rules
GITHUB_RULES.md      GitHub execution / history / proof discipline
CONTEXT.md           stable product/repository orientation
docs/foundation/     durable Flow policy
docs/knowledge/      continuation / decisions / evidence / operations
.agents/skills/      small reusable semantic skills
kits/lazy-builder/   Flow 2–6 procedure + implementation
workspace/           ignored local/external project data
tools/               deterministic verification
.github/             CI / promotion gates
```

## Continuation

Read `docs/knowledge/next-action.md` after this file for active work. If continuation disagrees with actual implementation state, reconcile the stale owner before proceeding.
