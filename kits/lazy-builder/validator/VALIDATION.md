# Validation and Handoff

## Proof layers

```text
1 repository/static contract
2 conversion primitive correctness
3 schematic file compatibility
4 Axiom import
5 Minecraft placement
6 visual fidelity
```

A lower layer does not prove a higher layer.

## Current M1 status

```text
Layer 3 writer/round-trip     → PASS
Layer 4 Axiom import          → LOCAL RUNTIME PROOF REQUIRED
Layer 5 Minecraft placement   → LOCAL RUNTIME PROOF REQUIRED
Layer 6 visual result         → LOCAL RUNTIME PROOF REQUIRED
```

Executable writer evidence:

```text
workflow: M1 Schematic Smoke
run: 34215078021
result: PASS
artifact: lazybuilder-m1-schematic-je-1-21-4
artifact id: 10051411457
fixture Minecraft enum: JE_1_21_4
```

The writer fixture saves and reloads exact BlockStates for:

```text
minecraft:stone_bricks
minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]
minecraft:stone_slab[type=top,waterlogged=false]
```

This establishes writer-level compatibility only. `JE_1_21_4` remains the M1 fixture target until actual Axiom/Minecraft testing confirms the intended production compatibility.

## M1 runtime acceptance

Use the **exact generated artifact**, not a hand-created substitute.

1. obtain `lazybuilder_m1_smoke.schem` from artifact `lazybuilder-m1-schematic-je-1-21-4`;
2. import it through Axiom **Import Schematic**;
3. confirm it appears in Axiom Clipboard;
4. place it in the target Minecraft Java world;
5. verify the three blocks appear as:
   - full stone-bricks block;
   - stair facing north, bottom half, straight shape;
   - top stone slab;
6. record Minecraft version, Axiom version, result, and any compatibility limitation.

M1 is end-to-end PASS only after all runtime steps above pass.

This proof happens **before** sophisticated Minecraftize logic so file/handoff failures are not confused with geometry-conversion failures.

## Later conversion acceptance

- full-block V0: end-to-end model→schem path works;
- stair: primitive state/facing/half tests plus visual improvement on slope;
- slab: top/bottom/mixed primitive tests;
- real building: silhouette/proportion and block-shape composition are acceptable relative to reference at intended target scale.

## Evidence language

Use `LOCAL RUNTIME PROOF REQUIRED` when repository/CI state is ready but the exact Axiom/Minecraft execution has not been performed.

Do not claim PASS from screenshots or downstream manual polish when the exact pre-polish engine output was not inspected.
