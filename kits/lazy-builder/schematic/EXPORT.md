# Schematic Export

## Role

Serialize the Minecraftize block model to Minecraft Java `.schem` using an existing writer rather than implementing NBT/Sponge serialization from scratch.

## Current integration target

Current audited handoff baseline:

```text
Minecraft Java Edition 1.21.4
Axiom 5.3.0 client
AxiomPaper 5.0.1+1.21.4 server plugin
Axiom protocol/API family 9
```

The `.schem` file is parsed by the **Axiom client**, not by AxiomPaper. AxiomPaper only becomes relevant when the resulting Clipboard/Placement is applied to a multiplayer Paper world.

## Current writer

Use pinned `mcschematic==11.4.4` while it satisfies the required BlockState and Axiom compatibility behavior.

Minecraftize hands the exporter values conceptually equivalent to:

```text
(x, y, z)
+
minecraft:block[property=value,...]
```

Examples:

```text
minecraft:stone_bricks
minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]
minecraft:stone_slab[type=top,waterlogged=false]
```

## Canonical file contract

For the current target, emit:

```text
Sponge Schematic Version 2
DataVersion 4189
Minecraft Java 1.21.4
GZIP NBT
root name: Schematic
```

Axiom 5.3.0's supplied binary accepts Sponge Version 2 and Version 3. Its own schematic exporter writes Sponge Version 2, so V2 remains the simplest compatible target.

LazyBuilder exports only:

```text
<build>.schem
```

Do not add `.schematic`, `.litematic`, `.bp`, or another format just because Axiom can read them.

## Bounds and Axiom Clipboard origin

Export **tight bounds** around the intended schematic volume.

For Sponge import, Axiom 5.3.0 recenters coordinates by dimensions:

```text
localX = x - floor(width / 2)
localY = y - floor(height / 2)
localZ = z - floor(length / 2)
```

Block entities use the same centering.

Do not rely on Sponge `Offset`, `WEOffsetX/Y/Z`, or related WorldEdit metadata to control the active Axiom paste pivot. The supplied client may preserve/re-emit that metadata, but the observed import placement coordinates are dimension-centered.

Final positioning/rotation belongs to Axiom Placement/Gizmo. `Snap to ground` is an Axiom-side placement tool, not an exporter feature.

## BlockState and DataVersion rules

- emit canonical vanilla serialized BlockState strings;
- use exact Minecraft 1.21.4 `DataVersion 4189` for the current environment;
- do not emit a future DataVersion;
- keep deterministic property/orientation tests for stairs/slabs and later directional blocks.

Axiom 5.3.0 can DataFix older schematic BlockStates using Minecraft's DataFixer. The current integration should still target the exact current version rather than relying on upgrade behavior.

## Air behavior

A schematic is a bounded volume and unused cells inside that volume are air. Axiom Placement exposes `Paste Air`, and the supplied Axiom 5.3.0 defaults it to enabled.

Therefore:

- tight bounds are required to minimize accidental clearing;
- use an empty area for compatibility tests;
- non-destructive placement into an existing build should treat `Paste Air` as a handoff/runtime choice;
- do not invent a custom no-air file format.

## Entity / block-entity boundary

### Normal entities

Treat normal entities as unsupported/out-of-scope for LazyBuilder Sponge `.schem` integration. The supplied Axiom 5.3.0 Sponge loader constructs an empty entity list.

### Block entities

Axiom 5.3.0 can parse valid Sponge block entities, but Paper placement additionally requires `axiom.build.nbt` to apply their NBT.

MVP full blocks/stairs/slabs require no block entities. Do not add NBT support until a concrete block family/use case requires it and a dedicated runtime test is defined.

## M1 writer fixture

The repository owns one small executable smoke fixture:

```text
requirements.txt
tools/m1_schematic_smoke.py
.github/workflows/m1-schematic-smoke.yml
```

Local command when the environment has normal Python package access:

```bash
python -m pip install -r requirements.txt
python tools/m1_schematic_smoke.py
```

Default output:

```text
artifacts/m1/lazybuilder_m1_smoke.schem
artifacts/m1/lazybuilder_m1_smoke.json
```

The fixture contains one full block, one north-facing bottom stair, and one top slab. It saves the schematic, reloads the same file with `mcschematic`, and asserts exact BlockState equality.

Current executable evidence:

```text
M1 Schematic Smoke
run 34215078021
PASS
artifact: lazybuilder-m1-schematic-je-1-21-4
```

The produced M1 file is Sponge Version 2 / DataVersion 4189 and is structurally aligned with the format family Axiom 5.3.0 itself exports.

## Failure ownership

```text
writer cannot produce/reload expected states
→ schematic writer / Minecraftize state owner

Axiom says unknown/unsupported schematic format
→ schematic compatibility owner

Import Schematic disabled by server
→ Axiom permission/session owner

file imports + Clipboard correct but placement fails
→ AxiomPaper permission/world/region/transport owner

placement succeeds but state/orientation wrong
→ first wrong exporter/BlockState owner
```

Do not replace `mcschematic` until the failure is demonstrated to belong to the writer.

## Explicitly not required

Do not build:

- custom Sponge/NBT serializer;
- Axiom protocol client;
- Paper schematic parser;
- Axiom automation/MCP;
- Blueprint `.bp` exporter;
- packet tuning layer.

Full Axiom evidence is recorded in `docs/knowledge/reviews/history/axiom-audit-2026-09-08.md` and the durable baseline is owned by `docs/knowledge/decisions/axiom-1.21.4-integration-baseline.md`.
