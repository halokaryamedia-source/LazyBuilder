# Blender Target Model

## Role

Blender converts one generated GLB into a stable, intentionally oriented and scaled sampling target for Minecraftize.

It is a preparation/workbench stage, not a conventional game/film asset pipeline.

## Input contract

Input is one exact generated GLB selected from the active test/project run.

Before editing, record:

```text
source path
source digest
generation case/run
source dimensions/bounds
known generation defects
intended Minecraft target width in blocks
```

Never silently replace the selected source GLB with a different generation result.

## Canonical scene convention

LazyBuilder uses one explicit coordinate convention so Minecraftize does not guess orientation later.

```text
Blender up       = +Z
Blender right    = +X
Blender front    = -Y

Minecraft up     = +Y
Minecraft right  = +X
Minecraft front  = +Z (south in canonical converter space)
```

Canonical axis mapping for conversion:

```text
Minecraft X =  Blender X
Minecraft Y =  Blender Z
Minecraft Z = -Blender Y
```

This convention is an internal LazyBuilder normalization. Final placement rotation remains an Axiom-side choice.

## Scene organization

Preserve the imported source and prepare a separate conversion target.

Recommended collections:

```text
LB_SOURCE
→ untouched imported source used for comparison/recovery

LB_TARGET
→ duplicated/joined working target sampled by Minecraftize
```

If the GLB contains multiple mesh objects, preserve their source objects and create one evaluated conversion target rather than requiring Minecraftize to infer arbitrary GLB object hierarchy.

## Transform normalization

Before sampling:

1. orient the model to the canonical front/up convention;
2. remove accidental global rotation/scale ambiguity;
3. set intentional target scale;
4. apply transforms on the conversion target only;
5. establish tight evaluated bounds.

Do not use arbitrary Blender units as the product scale contract.

Primary scale input:

```text
target_width_blocks
```

Minecraftize derives the normalized scale from the prepared mesh X width:

```text
scale = target_width_blocks / prepared_width_blender_units
```

The resulting grid uses one Minecraft block as one normalized converter unit.

When width is not the authoritative dimension, the active project may explicitly name another target dimension. The chosen scale driver must be recorded in `target.json`; do not infer it from screenshots later.

## Origin contract

The prepared mesh may remain conveniently positioned in Blender, but Minecraftize output is normalized to tight integer block bounds.

Therefore Blender does not need to encode final Minecraft world coordinates.

Final world positioning belongs to Axiom Placement/Gizmo.

## Cleanup allowed

Only cleanup that materially improves conversion is required:

- remove severe floating/noisy geometry that would generate false blocks;
- fix obvious disconnected fragments caused by generation;
- repair major holes/intersections when they break occupancy interpretation;
- simplify tiny geometry below intended block-scale relevance;
- join/organize mesh parts into the evaluated conversion target;
- correct gross symmetry/proportion defects only when the reference clearly establishes the intended form.

## Cleanup avoided

Do not spend time on:

- production retopology for its own sake;
- UV layout;
- texture/material polish that Minecraftize does not use;
- rigging/animation;
- hidden micro-detail below block resolution;
- manual remodeling whose only purpose is to hide a Minecraftize algorithm defect;
- destructive edits to the preserved source collection.

## Target metadata

The first local acceptance session writes:

```text
30-blender/target.blend
30-blender/target.json
```

`target.json` records at minimum:

```text
schema_version
source_path
source_digest
source_case
front_axis
up_axis
minecraft_axis_mapping
target_dimension_name
target_dimension_blocks
source_bounds
prepared_bounds
applied_rotation
applied_scale
cleanup_operations[]
known_remaining_defects[]
```

Minecraftize should be able to recover its required conversion assumptions from the prepared scene + metadata without chat history.

## Readiness gate before Minecraftize

Proceed when all are true:

```text
GLB imported successfully
canonical orientation established
scale driver is explicit
prepared target has applied transforms
tight bounds are available
severe false-block-producing noise is removed/documented
remaining defects are acceptable to evaluate at Minecraft resolution
```

The question is not whether the Blender mesh is perfect. The question is:

> Is the target now stable enough that Minecraftize results can be judged as converter behavior rather than unresolved orientation/scale/noise?

## Minecraftize preview expectation

The eventual Blender-side preview should support three views/modes:

```text
Original / prepared mesh
Minecraft Preview
Original + Minecraft Overlay
```

Preview must use the exact same normalized transform and block model that will be serialized; a decorative approximation is not acceptable for validation.

## Failure ownership

```text
GLB cannot import
→ generation/export compatibility

orientation ambiguous because references conflict
→ reference/intake owner

orientation wrong despite clear input
→ Blender target owner

scale wrong because target dimension missing
→ project/reference intake

scale formula/axis mapping wrong
→ Blender/Minecraftize boundary contract

severe noise remains and generates false blocks
→ Blender preparation if visibly removable before sampling

prepared target is correct but block silhouette is wrong
→ Minecraftize
```

## Runtime boundary

This file defines the target contract only. Actual Blender 5.2.x LTS import, transforms, cleanup, metadata capture, and preview remain `LOCAL RUNTIME PROOF REQUIRED` until the unified acceptance session is explicitly started.