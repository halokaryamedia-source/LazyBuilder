# Blender Target Preparation Policy

Flow 4 turns generated GLB into a stable working target for Minecraftize.

## Blender role

Blender is the workbench, not the final Minecraft engine and not the schematic writer.

Allowed preparation focuses on conversion value:

- correct orientation;
- establish target scale / intended Minecraft width;
- remove severe floating/noise geometry;
- correct obvious symmetry/large-form errors when they materially affect Minecraft output;
- preserve useful silhouette and surface depth.

## Do not over-clean

Avoid long retopology, UV, texture, material, animation, or micro-detail work when it will be discarded by Minecraft discretization.

The question is not “is this a perfect production mesh?” but:

> Is this geometry sufficiently stable and meaningful for Minecraftize to sample?

## Target readiness

A target is ready when:

- orientation and scale are intentional;
- major silhouette/volume is usable;
- severe mesh artifacts that would create false blocks are removed;
- remaining imperfections are cheaper to handle in Minecraftize than by more Blender work.

Detailed procedure: `kits/lazy-builder/blender/TARGET-MODEL.md`.
