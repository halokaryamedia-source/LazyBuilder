# Schematic Export

## Role

Serialize the Minecraftize block model to Minecraft Java `.schem` using an existing writer rather than implementing NBT/Sponge serialization from scratch.

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

The current fixture uses `mcschematic.Version.JE_1_21_4`. This is the **M1 compatibility-test target**, not a permanent global Minecraft target until the intended Axiom/Minecraft runtime is tested.

## Boundary

Writer round-trip PASS proves serialization behavior only. It does not prove Axiom import, Axiom Clipboard behavior, Minecraft placement, or visual fidelity.

If export fails, determine whether the Minecraftize block/state model is invalid or the writer is actually at fault before replacing the library.

Do not build a custom serializer for theoretical control.

## Output

Primary output:

```text
<build>.schem
```

Additional formats are not MVP scope.
