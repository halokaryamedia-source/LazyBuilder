# Next Action

## Current Status

`E2E_HARNESS_IMPLEMENTED_FIXTURE_PACK_REQUIRED_RUNTIME_DEFERRED`

The user explicitly wants the complete pipeline prepared before local runtime testing. Do not launch Hunyuan GPU generation, Blender conversion, Axiom, Paper, or Minecraft yet.

## Completed readiness implementation

```text
text/single/multiview generation runners
→ session manifest + digest/resume controller
→ Blender target contract
→ Minecraftize canonical blocks.json
→ Blender-native Minecraftize V0 full-block entrypoint
→ actual-engine primitive suite entrypoint
→ general blocks.json → .schem exporter
→ Axiom/Paper/Minecraft acceptance contract
→ consolidated acceptance report
→ static dry-run/CI contract
```

Minecraftize V0 runtime design:

```text
LazyBuilderTarget
→ Blender evaluated world mesh
→ mathutils BVHTree
→ pitch from target_width_blocks
→ deterministic occupancy
→ full-block blocks.json + report.json
```

Stair/slab remain intentionally unimplemented and must be reported `SKIPPED` during V0 acceptance.

## Only remaining preparation before local acceptance

Select/populate one real fixture package following `kits/lazy-builder/validator/FIXTURE-PACK.md`:

```text
T1 prompt
I1 front image
I2 front/right/back/left images
intentional target_width_blocks
```

The same bounded object/build should be represented across T1/I1/I2.

Use `prepare_case.py` to scaffold the ignored workspace. This is preparation only and must not start runtime.

## When the user later explicitly starts testing

Run one resumable acceptance session:

```text
preflight once
→ T1/I1/I2 generation
→ select representative GLB
→ Blender LazyBuilderTarget
→ Minecraftize primitive V0
→ Minecraftize representative model
→ .schem writer round-trip
→ Axiom / Clipboard / Placement
→ Paper / Minecraft verification
→ acceptance report
```

Failure resumes from the first invalidated owner rather than restarting the entire chain.

## Stop Boundary

Do not automatically start local runtime, add stairs/slabs, add Fast/Turbo routing, add another 3D provider, add MCP/Axiom automation, tune Axiom packets/performance, or promote `develop` to `Local`/`main`.
