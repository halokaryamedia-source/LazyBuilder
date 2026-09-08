# Blender Target Model

## Role

Blender prepares the generated mesh to be sampled by Minecraftize. It is not the final asset pipeline and does not need conventional game/film-quality retopology.

## Required preparation

- import GLB successfully;
- correct orientation;
- establish intentional scale / target Minecraft width;
- remove severe floating/noise geometry that would produce false blocks;
- repair only major form errors that materially harm conversion;
- preserve target silhouette/depth needed by Minecraftize.

## Avoid

- long retopology for its own sake;
- UV/texture polish that will be discarded;
- animation/rigging;
- micro-detail invisible at target Minecraft scale;
- changing shape merely to hide a converter weakness without recording that tradeoff.

## Readiness test

Ask:

> If Minecraftize samples this mesh now, are remaining errors cheaper to solve in block conversion than by further Blender cleanup?

If yes, continue.

## Preview expectation

Minecraftize should eventually support enough Blender preview to compare original mesh, Minecraft block result, and overlay.
