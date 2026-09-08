# LazyBuilder Product Package

This package owns detailed Flow 2–6 procedure and executable implementation. Root `AGENTS.md` owns repository work mode/continuity; `docs/foundation/` owns durable product policy.

## Package architecture

```text
kits/lazy-builder/
├── AGENTS.md
├── README.md
├── SKILL.md
├── intake/        T1/I1/I2 reference/text intake + approval procedure
├── generation/    pinned HunyuanDiT + Hunyuan3D-2mv runners/environment
├── blender/       LazyBuilderTarget + target.json contract/helper
├── minecraftize/  V0 full-block converter + primitive suite + canonical preview
├── schematic/     canonical blocks.json → .schem exporter
└── validator/     session graph, artifact contracts, preflight, acceptance evidence
```

## Product chain

```text
T1 text → HunyuanDiT → approval → Hunyuan3D-2mv ─┐
I1 single image → Hunyuan3D-2mv ─────────────────┼→ representative GLB
I2 multiview → Hunyuan3D-2mv ────────────────────┘
→ Blender LazyBuilderTarget
→ Minecraftize V0
→ blocks.json
├→ preview.svg
└→ mcschematic → build.schem
→ Axiom / Paper / Minecraft
```

## Current implementation state

The package is pre-MVP but has executable preparation across the full chain boundary:

```text
generation/runtime_contract.py
generation/generate_text_reference.py
generation/generate_shape.py
blender/write_target_metadata.py
minecraftize/block_model.py
minecraftize/minecraftize_v0.py
minecraftize/run_primitive_suite.py
minecraftize/build_preview.py
schematic/export_blocks.py
validator/collect_environment.py
validator/artifact_validation.py
validator/session_contract.py
validator/session_controller.py
validator/acceptance_report.py
```

Runtime-heavy entrypoints existing in source does **not** mean they have executed successfully.

## Pre-Runtime Verification vs Runtime Acceptance

```text
Pre-Runtime Verification
→ code/contracts/schema/digests/commands/static CI are coherent
→ no GPU/application runtime claim

Runtime Acceptance
→ actual Hunyuan + Blender + Axiom + Paper + Minecraft execution
```

Current status is owned by `validator/TEST-READINESS.md` and `docs/knowledge/next-action.md`.

## Architecture rule

Add implementation only to the owner that needs it. Do not create parallel kits, another model provider, custom schematic format, MCP, or Axiom automation merely to make the pipeline look more complete.
