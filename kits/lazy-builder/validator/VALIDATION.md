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

## MVP runtime acceptance

First end-to-end milestone:

1. programmatically generate a minimal `.schem`;
2. import it into Axiom;
3. confirm it appears in Axiom Clipboard;
4. place it in the target Minecraft Java world;
5. record the tested Minecraft/Axiom context and any compatibility limitation.

This proof should happen **before** sophisticated Minecraftize logic so file/handoff failure is not confused with geometry-conversion failure.

## Later conversion acceptance

- full-block V0: end-to-end model→schem path works;
- stair: primitive state/facing/half tests plus visual improvement on slope;
- slab: top/bottom/mixed primitive tests;
- real building: silhouette/proportion and block-shape composition are acceptable relative to reference at intended target scale.

## Evidence language

Use `LOCAL RUNTIME PROOF REQUIRED` when the repository state is ready but actual Hunyuan/Blender/Axiom/Minecraft execution has not been performed.

Do not claim PASS from screenshots or downstream manual polish when the exact pre-polish engine output was not inspected.
