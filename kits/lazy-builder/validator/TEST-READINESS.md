# End-to-End Test Readiness

Status: `E2E_HARNESS_IMPLEMENTED_FIXTURE_PACK_REQUIRED`.

Local Hunyuan, Blender, Axiom, Paper, and Minecraft runtime remains intentionally deferred.

## Locked first acceptance chain

```text
T1 TEXT → HunyuanDiT → approved reference → Hunyuan3D-2mv
I1 SINGLE IMAGE → Hunyuan3D-2mv
I2 FRONT/RIGHT/BACK/LEFT → Hunyuan3D-2mv
→ choose representative GLB
→ Blender 5.2.x / LazyBuilderTarget
→ Minecraftize V0 + primitive suite
→ canonical blocks.json
→ mcschematic 11.4.4 / Sponge V2 / DataVersion 4189
→ Axiom 5.3.0
→ AxiomPaper 5.0.1 / Paper 1.21.4
→ Minecraft Java 1.21.4
→ one acceptance-report.json
```

## Repository-owned harness

```text
case.template.json + prepare_case.py
→ acceptance case scaffold

session_contract.py + session_controller.py
→ stage graph / digest / resume / exact next action

dry_run_readiness.py
→ static command-routing proof without launching runtime apps

minecraftize/block_model.py
→ canonical blocks.json

minecraftize/minecraftize_v0.py
→ Blender-native BVH V0 full-block converter

minecraftize/run_primitive_suite.py
→ actual V0 engine primitive path in Blender

schematic/export_blocks.py
→ exact blocks.json → .schem + writer round-trip

acceptance_report.py
→ consolidated evidence
```

## Canonical local package

```text
workspace/active/lazybuilder-e2e/
├── case.json
├── inputs/
└── runs/<run-id>/
    ├── session.json
    ├── 00-preflight/environment.json
    ├── 10-reference/
    ├── 19-shape-text/
    ├── 20-shape-single/
    ├── 21-shape-multiview/
    ├── 30-blender/target.blend + target.json
    ├── 40-minecraftize-primitives/blocks.json + report.json
    ├── 41-minecraftize-model/blocks.json + report.json
    ├── 50-schematic/build.schem + manifest.json
    ├── 60-axiom/runtime.json
    └── acceptance-report.json
```

## Minecraftize V0 readiness

The runtime entrypoint is now implemented but **not runtime-proven**.

```text
Blender prepared mesh: LazyBuilderTarget
→ evaluated world geometry
→ Blender mathutils BVHTree
→ explicit target_width_blocks-derived pitch
→ deterministic cell centers
→ parity + near-surface occupancy evidence
→ full minecraft:stone_bricks baseline
→ canonical blocks.json + report.json
```

Coordinate mapping remains:

```text
Minecraft X =  Blender X
Minecraft Y =  Blender Z
Minecraft Z = -Blender Y
```

V0 supports **full blocks only**. Stair and slab are explicitly `SKIPPED`, not fake PASS.

The primitive suite creates a deterministic 3×2×2 Blender box and executes the **same V0 converter**. Expected result: 12 full blocks with 3×2×2 tight bounds. This primitive runtime is deferred until the unified session.

## Human/application gates

Only these require real inspection/action:

1. approve the T1 generated reference;
2. choose representative GLB after T1/I1/I2 shapes exist;
3. prepare/judge `LazyBuilderTarget` in Blender;
4. execute/inspect Axiom → Paper → Minecraft placement.

Successful deterministic script stages do not require separate chat confirmations.

## Resume rule

```text
failure
→ record exact stage/evidence
→ fix first wrong owner
→ invalidate only true dependents
→ resume from first invalidated stage
```

Do not restart valid upstream generation merely because a downstream conversion/export/runtime stage failed.

## Fixture pack

`FIXTURE-PACK.md` owns the final input selection rules. Use:

```bash
python kits/lazy-builder/validator/prepare_case.py \
  --workspace workspace/active/lazybuilder-e2e \
  --case-id <id> \
  --target-width-blocks <width>
```

This only creates folders/manifest; it starts no runtime.

The real first case still needs one selected bounded object/build with prompt, single front image, consistent front/right/back/left images, and intentional target width.

## Static readiness proof

CI must run repository owner verification, session/controller tests, static controller dry-run, block-model + V0 pure tests, Blender-entrypoint `py_compile` only, serialization fixture, and mcschematic writer round-trip.

Expected marker:

`STATIC_DRY_RUN_PASS_RUNTIME_DEFERRED`

Static proof never upgrades Hunyuan/Blender/Axiom/Minecraft runtime to PASS.

## Remaining boundary before the first local session

No additional runtime architecture is required before testing.

Remaining preparation is **test data**, not another subsystem:

1. choose/populate the real T1/I1/I2 fixture pack;
2. choose its intentional target width;
3. initialize one run ID;
4. explicitly start the unified local acceptance session.

Do not implement stairs/slabs, Fast/Turbo routing, another 3D provider, Axiom automation, or optimization layers before V0 runtime evidence requires them.
