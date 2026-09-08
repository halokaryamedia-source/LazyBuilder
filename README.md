# LazyBuilder

LazyBuilder is an AI-assisted R&D system for converting non-Minecraft visual references into Minecraft Java structures that can be exported as `.schem` and loaded in Axiom.

## Input → Output

| Input | Processing | Output |
|---|---|---|
| Multi-view reference images | Hunyuan3D-2mv shape generation | `model.glb` |
| Generated GLB | Blender target preparation | cleaned working target |
| Blender target | Minecraftize conversion | Minecraft block preview |
| Minecraft block model | `mcschematic` export | `.schem` |
| `.schem` | Axiom import / placement | Minecraft Java world structure |

The generated 3D mesh is not the final product. LazyBuilder's custom value is the **Minecraftize** stage that converts target geometry into increasingly Minecraft-native block usage.

## Branch Model

```text
develop  → active repository development
Local    → clean verified integration baseline; one squash commit per approved update
main     → stable repository history
```

Repository behavior is routed by [AGENTS.md](AGENTS.md); GitHub execution policy by [GITHUB_RULES.md](GITHUB_RULES.md); stable product orientation by [CONTEXT.md](CONTEXT.md).

## Execution Modes

LazyBuilder uses two work channels:

```text
remote_github
→ remote repository state, bounded docs/policy, branch/ref, PR, CI, promotion

local
→ source coding, dependencies/build/tests, binary artifacts,
  Hunyuan, Blender, Axiom, Minecraft runtime
```

Important naming rule:

```text
local  = execution mode
Local  = verified integration branch
```

Normal source development in `local` mode still uses branch `develop`.

Typical cycle:

```text
remote_github → pin/recover remote authority when needed
local         → implement + targeted proof + commit/push develop
remote_github → confirm remote state/CI → PR/promotion when required
```

Do not create GitHub Actions or helper infrastructure merely to emulate a local runtime.

## Locked MVP Stack

- **Hunyuan3D-2mv** — only active 3D generator.
- **Blender 5.2.x LTS** — 3D workbench.
- **Minecraftize** — custom Blender conversion addon/core.
- **mcschematic** — schematic writer.
- **Axiom** — final import/edit/placement environment.
- **Minecraft Java Edition** — target game.

No MCP or multi-model routing is part of the MVP.

## Product Flow

```text
Flow 1  Repository Boot & Project Memory
Flow 2  Reference Intake & Multi-view Recovery
Flow 3  Hunyuan3D-2mv Shape Generation
Flow 4  Blender Target Preparation
Flow 5  Minecraftize Conversion
Flow 6  Schematic Validation & Axiom Handoff
```

## Current Development Strategy

Development is output-driven:

```text
prove .schem → Axiom
→ prove Hunyuan3D-2mv → Blender
→ full-block Minecraftize
→ stairs
→ slabs
→ first real building
→ add other block families only when a real case requires them
```

Do not build a sophisticated optimizer, custom renderer, model router, or automation layer before the simpler pipeline proves a specific need.

## Repository Map

```text
.agents/skills/      reusable Development / Production judgment
docs/foundation/     durable production-flow policy
docs/knowledge/      continuation, ownership, decisions, evidence, backlog
kits/lazy-builder/   production procedure + implementation owner
workspace/           ignored local/external project-package convention
tools/               repository verification
.github/             CI / ownership / promotion policy
```

## Working Principle

```text
identify work mode
→ find first wrong/changed owner
→ select remote_github or local
→ read only required context
→ change the canonical owner
→ run the proof that can falsify the changed claim
→ stop
```

## Status

LazyBuilder is pre-MVP. Repository operating structure is established; executable product milestones are still pending runtime proof.

## License

LazyBuilder is publicly accessible for development convenience but is not open source. See [LICENSE](LICENSE).
