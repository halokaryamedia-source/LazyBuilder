# Blender Target Model

## Role

Blender prepares the generated mesh to be sampled by Minecraftize. It is not the final asset pipeline and does not need conventional game/film-quality retopology.

## Canonical prepared target

Keep the raw imported/generated source recoverable and create one separate prepared mesh named exactly:

```text
LazyBuilderTarget
```

Minecraftize V0 reads this object by name. Do not rely on whichever object happens to be active.

Canonical orientation:

```text
Blender up    = +Z
Blender front = -Y
Minecraft X   =  Blender X
Minecraft Y   =  Blender Z
Minecraft Z   = -Blender Y
```

Scale is driven by the explicit target dimension from the acceptance case, initially `target_width_blocks`. Do not treat arbitrary Blender units as Minecraft blocks.

## Required preparation

- import GLB successfully;
- correct orientation;
- establish intentional target width/scale;
- remove severe floating/noise geometry that would produce false blocks;
- repair only major form errors that materially harm conversion;
- preserve target silhouette/depth needed by Minecraftize;
- save the prepared scene as `target.blend` and stage metadata as `target.json`.

## Avoid

- long retopology for its own sake;
- UV/texture polish that will be discarded;
- animation/rigging;
- micro-detail invisible at target Minecraft scale;
- changing shape merely to hide a converter weakness without recording that tradeoff.

## Readiness test

Ask:

> If Minecraftize samples `LazyBuilderTarget` now, are remaining errors cheaper to solve in block conversion than by further Blender cleanup?

If yes, continue.

## Preview expectation

Minecraftize should eventually support enough Blender preview to compare original mesh, Minecraft block result, and overlay. Preview and schematic export must derive from the same canonical `blocks.json` rather than separate conversion paths.
