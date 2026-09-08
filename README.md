# LazyBuilder

LazyBuilder is an AI-assisted R&D system for converting text or non-Minecraft visual references into Minecraft Java structures that can be previewed, exported as `.schem`, and loaded in Axiom.

## Canonical Input → Output

```text
T1 TEXT
→ HunyuanDiT reference
→ approval
→ Hunyuan3D-2mv
→ model.glb

I1 SINGLE IMAGE
→ Hunyuan3D-2mv
→ model.glb

I2 MULTIVIEW
front / right / back / left
→ Hunyuan3D-2mv
→ model.glb

three shape paths
→ select representative GLB
→ Blender LazyBuilderTarget
→ Minecraftize V0
→ canonical blocks.json
├→ canonical preview.svg
└→ mcschematic → build.schem
→ Axiom / AxiomPaper / Paper
→ Minecraft Java world structure
```

The generated mesh is not the final product. LazyBuilder's custom value is **Minecraftize**, which converts prepared geometry into deterministic Minecraft block placement.

## Branch Model

```text
develop  → active repository development
Local    → clean verified integration baseline; one squash commit per approved update
main     → stable repository history
```

Repository behavior is routed by [AGENTS.md](AGENTS.md); GitHub execution policy by [GITHUB_RULES.md](GITHUB_RULES.md); stable product orientation by [CONTEXT.md](CONTEXT.md).

## Execution Modes

```text
remote_github
→ remote repository state, bounded docs/policy, branch/ref, PR, CI, promotion

local
→ source implementation, dependencies/build/tests, binary artifacts,
  Hunyuan, Blender, Axiom, Minecraft runtime
```

Important naming rule:

```text
local  = execution mode
Local  = verified integration branch
```

Normal source development in `local` mode still uses branch `develop`.

## Locked MVP Stack

- **HunyuanDiT** — T1 text-reference generator only.
- **Hunyuan3D-2mv** — only active 3D generator.
- **Blender 5.2.x LTS** — 3D preparation workbench.
- **Minecraftize** — custom deterministic conversion core.
- **mcschematic==11.4.4** — schematic writer.
- **Axiom 5.3.0** — final client import/edit/placement environment.
- **AxiomPaper 5.0.1+1.21.4 / Paper 1.21.4** — multiplayer placement path.
- **Minecraft Java Edition 1.21.4** — current runtime target.

No second 3D provider, MCP/Axiom automation, or custom schematic format is part of the MVP.

## Product Flow

```text
Flow 1  Repository Boot & Project Memory
Flow 2  T1/I1/I2 Reference Intake
Flow 3  Hunyuan Shape Generation
Flow 4  Representative Selection + Blender Target Preparation
Flow 5  Minecraftize Conversion + Canonical Preview
Flow 6  Schematic Validation + Axiom/Minecraft Handoff
```

## Pre-Runtime Verification

Pre-Runtime Verification is preparation, **not application testing**.

It checks:

```text
canonical documentation and source pins
session dependency/invalidation graph
input + artifact digest integrity
artifact schemas
Blender target metadata contract
Minecraftize pure/static contracts
canonical preview path
schematic writer round-trip
acceptance evidence structure
```

It does not launch Hunyuan GPU generation, Blender conversion, Axiom, Paper, or Minecraft.

The later **Runtime Acceptance Test** is the first point where those applications are actually executed.

Current continuation: [docs/knowledge/next-action.md](docs/knowledge/next-action.md).

## Repository Map

```text
.agents/skills/      reusable Development / Production judgment
docs/foundation/     durable product-flow policy
docs/knowledge/      continuation, ownership, decisions, evidence
kits/lazy-builder/   Flow 2–6 procedure + implementation
workspace/           ignored local/external project-package convention
tools/               deterministic repository/pre-runtime verification
.github/             CI / ownership / promotion policy
```

## Working Principle

```text
recover current authority
→ find first wrong owner
→ change smallest canonical owner
→ verify deterministic claims statically
→ require matching runtime evidence for runtime claims
→ stop
```

## Status

LazyBuilder remains pre-MVP. The repository is being prepared to reach a clean **pre-runtime-ready** state before the first controlled runtime acceptance session.

## License

LazyBuilder is publicly accessible for development convenience but is not open source. See [LICENSE](LICENSE).
