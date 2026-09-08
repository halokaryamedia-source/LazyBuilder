# Minecraftize Contract

Minecraftize is LazyBuilder's custom conversion core.

## Input

A Blender target mesh with intentional orientation and scale.

## Output

A Minecraft Java block model suitable for schematic serialization, with positions plus valid BlockState strings for currently supported shapes.

## Implementation progression

### V0 — Full block

Required:

- target width / grid scale;
- mesh occupancy sampling;
- full-block placement;
- preview;
- handoff to schematic writer.

### V1 — Stair

Required primitive coverage before real-building reliance:

```text
45° roof/slope
facing north/east/south/west
half top/bottom
straight
inner_left / inner_right
outer_left / outer_right when implementation reaches corner solving
```

Do not claim corner support before exact tests pass.

### V1 — Slab

Required:

```text
top
bottom
double when semantically needed
mixed full + stair + slab primitive test
```

## Rule-based first

Initial candidate logic should be understandable and falsifiable:

```text
solid/interior occupancy → full block
45°-like surface        → stair candidate
half-height contour     → slab candidate
```

Do not add an inverse-meshing optimization framework until primitive/real-build evidence proves local rules cannot meet quality goals.

## Block family boundary

`wall`, `fence`, `glass pane`, `trapdoor`, `iron bars`, doors, and decoration are not pre-required. Add each only from a documented real use case.

## Source/output discipline

During engine validation, correct Minecraftize at the first wrong conversion owner. Do not manually edit exported schematic/Axiom result and then attribute that quality to the engine.

## Proof

Each supported shape needs a reproducible primitive test before it is trusted in a real building. A final real-building test validates composition, not individual state correctness by itself.
