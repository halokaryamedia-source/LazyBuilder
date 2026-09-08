# LazyBuilder Product Package

This package owns detailed Flow 2–6 production procedure and executable implementation where it exists. Root `AGENTS.md` owns repository work mode/continuity; `docs/foundation/` owns durable product policy.

## Package architecture

```text
kits/lazy-builder/
├── AGENTS.md
├── README.md
├── SKILL.md
├── intake/        reference/text input + approval procedure
├── generation/    HunyuanDiT reference + Hunyuan3D-2mv runners/contracts
├── blender/       target-model preparation contract
├── minecraftize/  deterministic Minecraft conversion contract + future implementation
├── schematic/     export contract
└── validator/     acceptance / runtime-proof / unified test-readiness contract
```

## Product chain

```text
text (optional)
→ HunyuanDiT reference
→ review / approval
        ↘
reference images
→ Hunyuan3D-2mv
→ model.glb
→ Blender target preparation
→ Minecraftize
→ canonical Minecraft block model / preview
→ mcschematic
→ .schem
→ Axiom / Minecraft validation
```

## Current implementation state

The package is **pre-MVP but no longer procedure-only**.

Current repository-owned executable/static surfaces include:

```text
generation/runtime_contract.py
generation/generate_text_reference.py
generation/generate_shape.py
generation/test_generation_contract.py

repository M1 schematic smoke fixture / pinned mcschematic writer
```

These provide static/CI contract evidence only where they have actually executed. No claim is made that Hunyuan GPU generation, Blender preparation, representative Minecraftize conversion, Axiom import, or Minecraft placement has already passed locally.

## Test-readiness direction

Local runtime proof is intentionally deferred until Flow 2–6 can be executed as one prepared acceptance session.

Canonical session design:

`validator/TEST-READINESS.md`

Exact Axiom/Paper/Minecraft runtime acceptance:

`validator/VALIDATION.md`

The intended workflow is:

```text
complete design + non-runtime scaffolding
→ declare TEST_READY
→ one controlled local acceptance session
→ resume from first invalidated stage if a real failure occurs
```

Do not turn each newly implemented stage into a separate exploratory local test by default.

## Architecture rule

Add implementation only to the owner that actually needs it. Do not create parallel kits for Hunyuan, Blender, schematic, or Minecraftize; they remain categorized domains of one LazyBuilder product package.

Do not add another provider, custom schematic format, MCP, or Axiom automation merely to make the acceptance harness look more complete.