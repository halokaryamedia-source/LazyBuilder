# Blender Target Model

## Role

Blender prepares the selected generated mesh to be sampled by Minecraftize. It is not the final asset pipeline and does not need conventional game/film-quality retopology.

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

- import the selected GLB successfully;
- preserve the source object/collection for recovery;
- correct orientation;
- establish intentional target width/scale;
- remove severe floating/noise geometry that would create false blocks;
- repair only major form errors that materially harm conversion;
- preserve silhouette/depth needed by Minecraftize;
- save the prepared scene as `target.blend`;
- create canonical `target.json` with `write_target_metadata.py`.

## Canonical target.json

Minimum structure:

```json
{
  "schema_version": 1,
  "stage": "blender",
  "status": "PREPARED_TARGET_RUNTIME_CONVERSION_PENDING",
  "source": {
    "path": ".../model.glb",
    "sha256": "...",
    "selected_shape_stage": "shape_multiview"
  },
  "blender": {
    "version": "5.2.x",
    "target_object_name": "LazyBuilderTarget"
  },
  "target": {
    "target_width_blocks": 64,
    "bounds_world": {"min": [0, 0, 0], "max": [1, 1, 1]}
  },
  "orientation": {
    "minecraft_x": "blender_x",
    "minecraft_y": "blender_z",
    "minecraft_z": "-blender_y"
  },
  "cleanup": {"notes": []},
  "target_blend_sha256": "..."
}
```

Use:

```bash
python kits/lazy-builder/blender/write_target_metadata.py --help
```

after manual preparation to avoid hand-copying hashes/orientation fields.

## Avoid

- long retopology for its own sake;
- UV/texture polish that will be discarded;
- animation/rigging;
- micro-detail invisible at target Minecraft scale;
- changing shape merely to hide a converter weakness without recording that tradeoff.

## Readiness question

> If Minecraftize samples `LazyBuilderTarget` now, are remaining errors cheaper to solve in block conversion than by further Blender cleanup?

If yes, continue.

## Preview expectation

Canonical preview is generated **after Minecraftize** from the same `blocks.json` that feeds schematic export:

```text
blocks.json
├─ build_preview.py → preview.svg
└─ export_blocks.py → build.schem
```

There is no independent preview conversion path.
