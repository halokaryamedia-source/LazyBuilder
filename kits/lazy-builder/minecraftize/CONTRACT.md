# Minecraftize Contract

Minecraftize is LazyBuilder's custom deterministic conversion core.

Its job is to translate a normalized Blender target into a canonical Minecraft Java block model that can be previewed, tested, and serialized without requiring Axiom to repair conversion logic.

## Input contract

Minecraftize receives one prepared Blender target that already satisfies `../blender/TARGET-MODEL.md`.

Required inputs:

```text
prepared evaluated mesh
canonical Blender axis convention
target scale / normalized block grid
prepared bounds
conversion settings
```

Minecraftize must not guess object front, final target width, or source-reference authority from arbitrary scene state.

## Canonical coordinate mapping

The Blender preparation contract defines:

```text
Minecraft X =  Blender X
Minecraft Y =  Blender Z
Minecraft Z = -Blender Y
```

Minecraftize normalizes output to tight integer build coordinates. Final Minecraft world coordinates and final rotation belong to Axiom placement.

## Canonical block-model output

The engine output before schematic serialization is a deterministic list/map of block placements.

Minimum logical record:

```text
x: integer
y: integer
z: integer
block_state: canonical Minecraft Java BlockState string
```

Optional diagnostic fields may exist in debug/report output but are not part of the serializer requirement:

```text
classifier
confidence/reason
source_surface_normal
occupancy_score
```

The canonical block model must satisfy:

- one final state per coordinate;
- no conflicting duplicate coordinates;
- deterministic ordering for serialization/debugging;
- deterministic result for the same normalized mesh + settings;
- valid BlockState strings for every supported block family.

Recommended deterministic ordering:

```text
Y → Z → X
```

This ordering is for stable output/diffs and does not redefine schematic coordinate semantics.

## Conversion pipeline

Minecraftize is designed as explicit passes rather than one opaque optimizer.

```text
Pass 0  normalize evaluated target + grid bounds
Pass 1  occupancy / candidate cells
Pass 2  full-block baseline
Pass 3  surface classification
Pass 4  stair candidates
Pass 5  stair neighborhood/corner resolution when supported
Pass 6  slab candidates
Pass 7  conflict resolution
Pass 8  preview + canonical blocks.json
```

Each later pass may replace a baseline full block only when its rule has stronger explicit evidence.

No ML/inverse solver is required before these deterministic passes demonstrate a concrete limitation on representative builds.

## Pass 0 — normalized grid

Use the applied Blender target transform and target dimension contract.

The converter constructs tight candidate grid bounds in normalized Minecraft units.

Grid ownership is local to the build:

```text
minimum occupied output → normalized near origin
final world location    → not encoded here
```

The converter report records the grid dimensions and normalization transform.

## Pass 1 — occupancy candidates

The first implementation must expose occupancy as a falsifiable function rather than burying it in visual heuristics.

Conceptually:

```text
mesh + grid cell
→ occupancy evidence
→ occupied / empty candidate
```

The exact low-level mesh sampling implementation may use Blender-native evaluated geometry/BVH behavior, but the public contract is:

- identical normalized input produces identical occupied cells;
- exterior floating noise should not silently become structural occupancy when the Blender target has already marked/removed it;
- thin geometry below the active grid resolution may be lost and should be reported rather than guessed into decoration;
- occupancy thresholds/settings are explicit in the run report.

Do not introduce an external voxel/geometry framework merely to avoid implementing the smallest Blender-native proof.

## Pass 2 — full-block baseline

V0 converts occupied cells to a known full block family.

Initial material mapping may use one configured full block, for example:

```text
minecraft:stone_bricks
```

The first engine proof is geometric, not a material-selection system.

V0 acceptance:

```text
occupied cells produce exactly one block
empty cells produce no block
tight bounds are correct
same input/settings produce same coordinates
preview and blocks.json use the same output
```

## Pass 3 — surface classification

After V0 is correct, Minecraftize may classify boundary cells using local geometric evidence.

Useful evidence includes:

```text
surface normal
local height coverage
neighbor occupancy
slope direction
surface continuity
```

The classifier must produce an explainable candidate such as:

```text
FULL
STAIR
SLAB
UNSUPPORTED
```

A cell remains FULL when evidence for a more specific primitive is weak or conflicting.

## Pass 4 — stair candidates

Stair support is introduced only after full-block occupancy is stable.

Initial straight-stair requirements:

```text
facing = north | east | south | west
half   = top | bottom
shape  = straight
```

Direction is derived from the projected surface slope/normal in canonical Minecraft coordinates, not from arbitrary Blender object rotation.

A candidate should require evidence that the local surface is meaningfully stair-like at the active block scale. Do not convert every non-horizontal normal into a stair.

## Pass 5 — stair corner resolution

Corner shapes are a neighborhood-resolution pass performed after straight stair candidates exist.

Target states:

```text
inner_left
inner_right
outer_left
outer_right
```

Corner shape is determined from adjacent compatible stair candidates and their facings.

Do not claim corner support until exact primitive fixtures prove every implemented orientation combination.

If the neighborhood is ambiguous, retain a simpler valid state rather than inventing an unstable corner.

## Pass 6 — slab candidates

Slab support follows stable full/stair behavior.

Target states:

```text
type=bottom
type=top
type=double when semantically required
```

Use local half-height/coverage evidence and neighboring continuity.

A slab may replace a full block only when the resulting surface better represents the prepared mesh at the target scale.

## Pass 7 — conflict resolution

One coordinate must end with one BlockState.

Default precedence is based on explicit geometric fit, not block-family prestige.

Conceptually:

```text
strong validated stair/slab evidence
→ specific primitive

ambiguous/weak evidence
→ full block fallback

unsupported decorative/thin case
→ report unsupported; do not invent a new family
```

Conflict decisions must be deterministic and testable.

## BlockState contract

### Full block

Example:

```text
minecraft:stone_bricks
```

### Stair

Example:

```text
minecraft:stone_brick_stairs[
  facing=north,
  half=bottom,
  shape=straight,
  waterlogged=false
]
```

Required properties:

```text
facing=north|east|south|west
half=top|bottom
shape=straight|inner_left|inner_right|outer_left|outer_right
waterlogged=false
```

### Slab

Example:

```text
minecraft:stone_slab[type=top,waterlogged=false]
```

Required properties:

```text
type=top|bottom|double
waterlogged=false
```

Canonical property ordering should remain stable in generated output/tests even if Minecraft itself does not require textual property ordering.

## Primitive fixture suite

Before a real Hunyuan model is trusted, one batch must cover deterministic primitive behavior.

### Full block

```text
single occupied cell
small solid box
tight-bound edge cells
```

### Straight stairs

At minimum:

```text
4 facings × bottom
4 facings × top when top-half classification is implemented
```

### Stair corners

Only when implemented:

```text
inner_left
inner_right
outer_left
outer_right
```

with enough rotated fixtures to prove facing/handedness logic.

### Slabs

```text
bottom
top
double if implemented as an explicit output choice
```

### Mixed composition

One deterministic fixture contains full blocks + stairs + slabs so conflict ordering and serializer handoff are exercised together.

A missing feature is `SKIPPED`, not PASS.

## Representative-model acceptance

After primitive coverage passes, run one prepared Hunyuan/Blender target through the same converter.

Required report metrics:

```text
grid dimensions
occupied block count
full-block count
stair count
slab count
unsupported/ambiguous count
conversion settings
runtime
```

First end-to-end quality bar:

- recognizable silhouette;
- intended target scale retained;
- major proportions retained;
- no catastrophic holes caused by conversion;
- no obvious disconnected noise that should have been excluded upstream;
- stair/slab use is explainable rather than random;
- same input/settings remain deterministic.

This is pipeline acceptance, not final artistic perfection.

## Preview contract

Preview is evidence, not a separate approximate rendering path.

Required future modes:

```text
Prepared Mesh
Minecraft Preview
Prepared Mesh + Minecraft Overlay
```

The preview must consume the exact canonical block model that is sent to schematic export.

If preview and exported coordinates differ, the implementation is wrong even if the final screenshot looks acceptable.

## Output files for unified acceptance

```text
40-minecraftize-primitives/
├── blocks.json
└── report.json

41-minecraftize-model/
├── blocks.json
└── report.json
```

`blocks.json` contains canonical placements only.

`report.json` owns diagnostics, metrics, classifier counts, settings, unsupported cases, and source/target digests.

## Schematic handoff

Minecraftize hands `blocks.json` semantics to `../schematic/EXPORT.md`.

The writer should not reinterpret geometry.

```text
Minecraftize decides coordinate + BlockState
→ schematic writer serializes it
```

If `blocks.json` is correct and `.schem` is wrong, fix the exporter. If `blocks.json` is already wrong, do not patch the `.schem` or Axiom result.

## Block family boundary

Do not pre-build support for:

```text
wall
fence
glass pane
trapdoor
iron bars
doors
vegetation
decoration
block entities
```

Add a family only when a representative build demonstrates a concrete geometric need and a primitive fixture can define correctness.

## Failure ownership

```text
wrong normalized dimensions/axes
→ Blender/Minecraftize boundary

wrong occupied cells with correct prepared mesh
→ occupancy pass

correct occupancy but wrong stair/slab classification
→ surface classifier

straight stairs correct but corners wrong
→ neighborhood/corner resolver

blocks.json correct but preview wrong
→ preview owner

blocks.json correct but .schem wrong
→ schematic exporter

manual Axiom cleanup needed to look right
→ record it separately; do not attribute it to Minecraftize
```

## Runtime boundary

This contract may be designed and covered by deterministic unit fixtures before Hunyuan/Blender/Axiom runtime is executed.

Actual representative conversion quality remains `LOCAL RUNTIME PROOF REQUIRED` until the unified acceptance session is explicitly started.