# Schematic Export

## Role

Serialize the Minecraftize block model to Minecraft Java `.schem` using an existing writer rather than implementing NBT/Sponge serialization from scratch.

## Current writer

Use `mcschematic` while it satisfies the required BlockState and Axiom compatibility behavior.

Minecraftize hands the exporter values conceptually equivalent to:

```text
(x, y, z)
+
minecraft:block[property=value,...]
```

Examples:

```text
minecraft:stone_bricks
minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight]
minecraft:stone_slab[type=top]
```

## Boundary

If export fails, determine whether the Minecraftize block/state model is invalid or the writer is actually at fault before replacing the library.

Do not build a custom serializer for theoretical control.

## Output

Primary output:

```text
<build>.schem
```

Additional formats are not MVP scope.
