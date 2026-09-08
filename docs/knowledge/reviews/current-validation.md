# Current Validation Status

Updated: 2026-09-08

## Current system state

Working branch: `develop`.  
Verified integration baseline: `Local`.  
Stable branch: `main`.

LazyBuilder remains **pre-MVP**.

Current `develop` contains:

- PRD-Creator-style repository memory/governance;
- GPT Astra 6 ExtraHigh development profile;
- `remote_github` / `local` execution-mode routing;
- executable M1 schematic writer fixture;
- full Axiom 1.21.4 static/research integration audit.

Verified `Local` operating-system milestone:

```text
98046e2339aff0beff3caff8dee9030b258686ef
```

Current production chain:

```text
reference images
→ Hunyuan3D-2mv
→ GLB
→ Blender target
→ Minecraftize
→ Sponge .schem
→ Axiom client
→ AxiomPaper / Paper placement
→ Minecraft Java
```

## Repository/governance evidence

Operating-system baseline was promoted through PR #1 after Local Promotion Verify passed. Subsequent Astra6/execution-mode/M1 changes on `develop` passed Repository Verify.

Execution channels remain:

```text
remote_github
→ remote repository state / bounded repo mutations / branch / PR / CI / promotion

local
→ clone/worktree / source implementation / dependencies / build / tests / binaries /
  Hunyuan / Blender / Axiom / Minecraft runtime
```

Naming boundary:

```text
local  = execution mode
Local  = verified integration branch
```

## M1 schematic writer evidence

Executable evidence:

```text
workflow: M1 Schematic Smoke
run: 34215078021
head: e1f9101ff87cf9000a13fcc0b7bbf6950e58ff20
result: PASS
```

Artifact:

```text
name: lazybuilder-m1-schematic-je-1-21-4
id: 10051411457
size: 978 bytes
digest: sha256:d4f4d27aed5773af671b1d1478c32e9cdf8e0964c4c5dcfa6b6267dd33f8fec6
expires: 2026-09-22
```

Downloaded archive contents:

```text
lazybuilder_m1_smoke.schem  382 bytes
lazybuilder_m1_smoke.json   488 bytes
```

The smoke workflow proves:

- `mcschematic==11.4.4` installs in the execution environment;
- a non-empty Sponge `.schem` is generated;
- the same file reloads successfully with `mcschematic`;
- exact BlockState equality survives round-trip for:
  - `minecraft:stone_bricks`;
  - `minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]`;
  - `minecraft:stone_slab[type=top,waterlogged=false]`.

The exact generated M1 file has:

```text
Sponge Version: 2
DataVersion: 4189
Width: 3
Height: 1
Length: 1
```

## Axiom binary inventory / fingerprints

User-supplied binaries audited directly:

```text
Axiom-5.3.0-for-MC1.21.4.jar
sha256 8026fdb448686cd6db69e69c695fa17f54508f801ddddb3ffeb850b79b04eae5

AxiomPaper-4.0.4-for-MC1.21.4.jar
sha256 f01b1b42ca21626d4c50359eab76bde4e361ea6614a7be5815d05fa81dd26a81

AxiomPaper-5.0.1-for-MC1.21.4.jar
sha256 cecafb3e1beba81245ee5bcfc3251052035526b99bb111127b968b09c92d86c8
```

Client metadata confirms Axiom `5.3.0`, Minecraft `>=1.21.4 <1.21.5`, Fabric Loader `>=0.14.21`, Fabric API required, Java `>=17`, and client license `All Rights Reserved`.

AxiomPaper 5.0.1 metadata confirms Paper `api-version: 1.21` and soft dependencies on CoreProtect, ViaVersion, WorldGuard, and PlotSquared.

## Axiom compatibility verdict — research/static PASS

Direct binary protocol-family result:

```text
Axiom 5.3.0 client           → Axiom API family 9
AxiomPaper 5.0.1+1.21.4     → Axiom API family 9
AxiomPaper 4.0.4+1.21.4     → Axiom API family 8
```

Therefore:

```text
Axiom 5.3.0 + AxiomPaper 5.0.1 → current baseline
Axiom 5.3.0 + AxiomPaper 4.0.4 → rejected for baseline
```

This proves static protocol-family alignment only. Actual handshake remains runtime proof.

## Axiom integration architecture — research/static PASS

Direct binary inspection establishes:

```text
LazyBuilder .schem
→ Axiom 5.3.0 CLIENT parses local file
→ ClipboardObject
→ Placement
→ client block buffer
→ AxiomPaper validates session/restrictions
→ bulk Paper world modification
```

Therefore:

- AxiomPaper is not the `.schem` parser for LazyBuilder;
- `.schem` compatibility is primarily a client-side Axiom contract;
- AxiomPaper owns multiplayer permission/world/region/transport/placement concerns;
- LazyBuilder needs no Axiom network protocol implementation;
- LazyBuilder needs no Paper-side schematic parser;
- direct Axiom automation is not required for MVP.

## Axiom schematic behavior — research/static PASS

Exact supplied Axiom 5.3.0 client findings:

- file picker accepts `.schem`, `.schematic`, `.litematic`;
- NBT format sniffing recognizes Litematic, Sponge schematic and legacy pre-1.13 schematic;
- Sponge `Version = 2` and `Version = 3` are accepted;
- Axiom's own schematic exporter writes Sponge `Version = 2`;
- older BlockStates can be upgraded through Minecraft DataFixer;
- exact current target should remain `DataVersion 4189` for Minecraft 1.21.4;
- Sponge BlockData iteration order is Y → Z → X;
- normal entities are not preserved by the observed Sponge import path;
- valid block entities can be parsed but are outside current MVP.

Current LazyBuilder `mcschematic` V2 structure is therefore aligned with the target client at the schema/structure level.

## Axiom imported origin / pivot — research/static PASS

Exact supplied Sponge loader centers imported coordinates by dimensions:

```text
localX = x - floor(width / 2)
localY = y - floor(height / 2)
localZ = z - floor(length / 2)
```

The same transform applies to block-entity coordinates.

For the M1 3×1×1 fixture, expected local X values are approximately:

```text
-1, 0, +1
```

Observed import positioning does not use Sponge/WorldEdit Offset metadata as the active Clipboard pivot. LazyBuilder should therefore export tight bounds and leave final positioning to Axiom Placement/Gizmo.

## Axiom/Paper permission and placement audit — research/static PASS

Supplied AxiomPaper 5.0.1 includes normal/default permission families such as:

```text
axiom.default
axiom.use
axiom.can_import_blocks
axiom.can_export_blocks
axiom.build.place
axiom.build.section
axiom.build.nbt
```

The Axiom client can disable Import Schematic when the server does not grant the import capability.

The Paper block-buffer path checks session/dispatch state, build-section permission, matching world, world whitelist/blacklist, modify-world event/integrations, region/section permission, and separate NBT permission before/while modifying world data.

Bulk placement updates chunk sections and related lighting/POI/block-entity data. It is not modeled as command-per-block placement.

## Supplied Paper config research baseline

Relevant supplied 5.0.1 defaults include:

```text
max-chunk-load-distance: 256
blueprint-sharing: false
allow-large-chunk-data-request: false
allow-large-payload-for-all-packets: false
incompatible-data-version: warn
unsupported-axiom-version: warn
max-block-buffer-packet-size: 0x100000
block-buffer-rate-limit: 0
disallowed-blocks: []
infinite-reach-limit: 256
log-core-protect-changes: true
```

No packet/rate/config tuning is justified before a real benchmark/failure.

## Conditional Paper upgrade research

Official version metadata shows `AxiomPaper 5.0.4+1.21.4` exists and fixes slow updates due to permission issues.

It is **not** the current baseline. Supplied 5.0.1 remains the reproducible M1 target until an actual matching symptom or explicit user upgrade decision exists.

## Current M1 runtime proof status

```text
M1 writer / BlockState round-trip       → PASS
Axiom exact-version static audit        → PASS
AxiomPaper API-family static match      → PASS
Axiom client import                     → LOCAL RUNTIME PROOF REQUIRED
Axiom Clipboard                         → LOCAL RUNTIME PROOF REQUIRED
AxiomPaper handshake                    → LOCAL RUNTIME PROOF REQUIRED
Paper permission/world/region behavior  → LOCAL RUNTIME PROOF REQUIRED
Minecraft placement                     → LOCAL RUNTIME PROOF REQUIRED
stair/slab visual orientation           → LOCAL RUNTIME PROOF REQUIRED
```

Before the runtime proof, exact environment values still need to be recorded where unknown:

```text
Paper version/build
Fabric Loader version
Fabric API version
OP vs permission plugin setup
ViaVersion presence
WorldGuard presence
PlotSquared presence
CoreProtect presence
applicable Axiom whitelist/commercial-license state
```

## Not yet claimed

- Hunyuan3D-2mv local generation on RTX 3070 8 GB;
- GLB import/cleanup in Blender;
- Minecraftize full-block conversion;
- Minecraftize stair/slab conversion;
- production-scale Axiom placement throughput;
- BlockEntity/NBT placement;
- normal entity preservation;
- real-building visual fidelity.

## Evidence owners

Durable Axiom decision:

`docs/knowledge/decisions/axiom-1.21.4-integration-baseline.md`

Full audit:

`docs/knowledge/reviews/history/axiom-audit-2026-09-08.md`

Exporter contract:

`kits/lazy-builder/schematic/EXPORT.md`

Runtime acceptance:

`kits/lazy-builder/validator/VALIDATION.md`

## Evidence boundary

GitHub/static/binary/writer execution proves only the behavior actually inspected or executed. It does not prove Axiom/Paper/Minecraft runtime success.

M1 becomes end-to-end PASS only after the exact generated `lazybuilder_m1_smoke.schem` is imported by Axiom 5.3.0, appears correctly in Clipboard, survives the AxiomPaper 5.0.1 handshake/placement path, and places the expected BlockStates in Minecraft Java 1.21.4.
