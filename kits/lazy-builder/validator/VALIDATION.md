# Validation and Handoff

## Proof layers

```text
1 repository/static contract
2 conversion primitive correctness
3 schematic writer / schema compatibility
4 Axiom client import + Clipboard
5 AxiomPaper handshake / placement permission
6 Minecraft world placement
7 visual fidelity
```

A lower layer does not prove a higher layer.

## Current audited runtime target

Use the exact supplied baseline for M1:

```text
Minecraft Java Edition 1.21.4

CLIENT
Fabric
Axiom 5.3.0
sha256 8026fdb448686cd6db69e69c695fa17f54508f801ddddb3ffeb850b79b04eae5
Axiom API family 9

SERVER
Paper 1.21.4
AxiomPaper 5.0.1+1.21.4
sha256 cecafb3e1beba81245ee5bcfc3251052035526b99bb111127b968b09c92d86c8
Axiom API family 9
```

Do not use supplied AxiomPaper 4.0.4 for this test; it is API family 8.

Paper 5.0.4 is only an upgrade candidate if an actual slow-update/permission problem appears or the user explicitly changes the baseline.

## Current M1 status

```text
Layer 3 writer/round-trip        → PASS
Axiom binary integration audit   → PASS (research/static)
Layer 4 Axiom import             → LOCAL RUNTIME PROOF REQUIRED
Layer 5 Paper handshake/permission → LOCAL RUNTIME PROOF REQUIRED
Layer 6 Minecraft placement      → LOCAL RUNTIME PROOF REQUIRED
Layer 7 visual state             → LOCAL RUNTIME PROOF REQUIRED
```

Executable writer evidence:

```text
workflow: M1 Schematic Smoke
run: 34215078021
result: PASS
artifact: lazybuilder-m1-schematic-je-1-21-4
artifact id: 10051411457
fixture target: Sponge V2 / JE_1_21_4 / DataVersion 4189
```

The writer fixture saves and reloads exact BlockStates for:

```text
minecraft:stone_bricks
minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]
minecraft:stone_slab[type=top,waterlogged=false]
```

## M1 runtime preflight

Before import, record the actual environment:

```text
Minecraft client version
Fabric Loader version
Fabric API version
Axiom client version + SHA-256
Paper version/build
AxiomPaper version + SHA-256
OP or permission-plugin setup
ViaVersion installed? yes/no
WorldGuard installed? yes/no
PlotSquared installed? yes/no
CoreProtect installed? yes/no
Axiom commercial license / whitelist state as applicable
```

Unknown items are allowed before the test, but they must not be guessed in the final evidence.

## Axiom session preflight

For the first controlled multiplayer proof use either:

```text
OP
```

or:

```text
axiom.default
+ disconnect/reconnect
```

The official plugin README requires reconnect after changing OP/permission state.

If Axiom is not active, use:

```text
/whynoaxiom
```

and optionally:

```text
/axiomhandshake
```

before changing files or exporter code.

The import menu itself requires the server-provided `CAN_IMPORT_BLOCKS` capability/`axiom.can_import_blocks` permission.

## Exact M1 runtime acceptance

Use the **exact generated artifact**, not a hand-created substitute:

`lazybuilder_m1_smoke.schem`

### A. Client file import

1. open Axiom Editor;
2. File → Import Schematic;
3. choose the exact M1 `.schem`;
4. confirm there is no unknown-format/unsupported-version error.

Expected current format:

```text
Sponge Version 2
DataVersion 4189
3 × 1 × 1
```

### B. Clipboard

Confirm the imported schematic appears in Axiom Clipboard.

Because Axiom 5.3.0 centers Sponge imports by dimensions, the expected local X positions for the 3×1×1 fixture are approximately:

```text
-1, 0, +1
```

Do not require `WEOffset`/`Offset` metadata to control the pivot.

### C. Placement preview

Create a Placement using Clipboard paste.

For M1:

- use an empty test area;
- do not rotate/scale/flip before the first proof;
- keep placement semantics otherwise default unless a setting visibly interferes;
- note the state of `Paste Air` if the test is not in an empty area.

### D. Paper/world placement

Confirm the placement is accepted by the server and appears in the world.

Expected blocks:

- full stone-bricks block;
- stone-brick stair facing north, bottom half, straight shape;
- top stone slab.

M1 is end-to-end PASS only when client import, Clipboard, Paper placement and state/orientation all pass.

## Failure routing

Diagnose the first wrong owner:

```text
Import Schematic menu disabled
→ permission/session: axiom.can_import_blocks / handshake

unknown format / unsupported Sponge Version
→ schematic schema compatibility

file imports but Clipboard empty
→ client parsing/content compatibility

Clipboard correct but Placement cannot start
→ BUILD_SECTION permission / client restrictions

Placement starts but server rejects/does nothing
→ AxiomPaper handshake, world restriction, region integration, rate/transport

some sections place and others do not
→ region/section permissions, world height, server restrictions

specific block/state missing
→ disallowed-blocks or BlockState compatibility

blocks place but stair/slab orientation wrong
→ exporter / BlockState owner

block entity data missing later
→ axiom.build.nbt + BlockEntity test owner

slow updates with correct permissions
→ measure first; then evaluate AxiomPaper 5.0.4+1.21.4 candidate
```

Do not change `mcschematic`, packet limits, or Axiom versions before the failure class is known.

## Server policy/config checks

The supplied AxiomPaper 5.0.1 defaults should remain unchanged for M1.

If placement is unexpectedly blocked, check:

```text
whitelist-world-regex
blacklist-world-regex
disallowed-blocks
WorldGuard/PlotSquared bounds
AxiomModifyWorldEvent integrations
```

Do not enable `allow-large-payload-for-all-packets` for M1.

## Scale/performance validation — later

Do not infer a production structure-size limit from the packet-size config alone.

After M1 and Minecraftize V0 work, benchmark representative builds with:

```text
block count
occupied chunk sections
schematic dimensions
import time
Clipboard responsiveness
placement preview responsiveness
server placement time
chunk/light update behavior
memory/VRAM impact where relevant
```

Only then consider rate/packet/plugin tuning.

## NBT/entity validation — later

Normal entities are not part of the current LazyBuilder Sponge integration contract.

BlockEntity/NBT proof requires a separate fixture because:

- Axiom client parsing rules differ from normal blocks;
- Paper placement requires `axiom.build.nbt`;
- privileged block NBT can require OP level.

Do not mix NBT testing into basic full/stair/slab M1.

## Later conversion acceptance

- full-block V0: end-to-end model→schem path works;
- stair: primitive state/facing/half tests plus visual improvement on slope;
- slab: top/bottom/mixed primitive tests;
- real building: silhouette/proportion and block-shape composition are acceptable relative to reference at intended target scale.

## Evidence language

Use `LOCAL RUNTIME PROOF REQUIRED` when repository/audit/CI state is ready but the exact Axiom/Paper/Minecraft execution has not been performed.

Do not claim PASS from static binary inspection, documentation, screenshots of a manually altered result, or downstream polish when the exact target artifact was not executed.
