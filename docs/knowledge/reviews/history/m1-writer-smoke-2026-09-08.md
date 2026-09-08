# M1 Writer Smoke Evidence — 2026-09-08

## Scope

This record captures the first executable proof for the LazyBuilder schematic handoff path. It proves writer-level `.schem` generation and BlockState round-trip only. It does not prove Axiom import or Minecraft placement.

## Candidate

```text
workflow: M1 Schematic Smoke
run: 34215078021
head: e1f9101ff87cf9000a13fcc0b7bbf6950e58ff20
result: PASS
```

## Fixture

`tools/m1_schematic_smoke.py` generated a three-block Minecraft Java schematic using `mcschematic==11.4.4` and `mcschematic.Version.JE_1_21_4`:

```text
(0,0,0) minecraft:stone_bricks
(1,0,0) minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]
(2,0,0) minecraft:stone_slab[type=top,waterlogged=false]
```

The workflow required the generated `.schem` to be non-empty, reloaded the same file with `mcschematic`, and checked exact BlockState equality for all three positions.

## Artifact

```text
artifact name: lazybuilder-m1-schematic-je-1-21-4
artifact id: 10051411457
artifact size: 978 bytes
artifact digest: sha256:d4f4d27aed5773af671b1d1478c32e9cdf8e0964c4c5dcfa6b6267dd33f8fec6
expires: 2026-09-22
```

Archive contents observed after download:

```text
lazybuilder_m1_smoke.schem  382 bytes
lazybuilder_m1_smoke.json   488 bytes
```

## Proven

- pinned `mcschematic` dependency installs in the CI runtime;
- the M1 fixture serializes to a non-empty `.schem`;
- the generated file can be reloaded by the same writer library;
- full-block, stair, and slab BlockState strings survive the save/reload round trip exactly;
- a concrete artifact exists for Axiom testing.

## Not proven

```text
Axiom import      → LOCAL RUNTIME PROOF REQUIRED
Axiom Clipboard   → LOCAL RUNTIME PROOF REQUIRED
Minecraft place   → LOCAL RUNTIME PROOF REQUIRED
visual result     → LOCAL RUNTIME PROOF REQUIRED
```

`JE_1_21_4` is the M1 fixture compatibility target, not a permanent global target until actual Axiom/Minecraft runtime evidence confirms the intended production version.

## Next proof

Use the exact `lazybuilder_m1_smoke.schem` from artifact `10051411457` in Axiom, confirm it reaches Clipboard, place it in Minecraft Java, and verify the full block, north-facing bottom stair, and top slab visually.
