# Next Action

## Current Status

`M1_AXIOM_AUDIT_COMPLETE_RUNTIME_REQUIRED`

The repository operating system, Astra6 development profile, execution-mode routing, M1 schematic writer proof, and full Axiom static/research audit are established.

M1 is **not yet end-to-end complete** because the exact user runtime still needs to prove Axiom client import, Clipboard, Paper handshake/placement, and Minecraft BlockState behavior.

Branch state:

```text
develop → active Development continuation
Local   → verified operating-system milestone
main    → stable repository history
```

Verified `Local` milestone:

```text
98046e2339aff0beff3caff8dee9030b258686ef
```

## Locked product stack

```text
Hunyuan3D-2mv
→ Blender
→ Minecraftize
→ mcschematic
→ Sponge .schem
→ Axiom client
→ AxiomPaper / Paper placement
→ Minecraft Java
```

## Current Axiom baseline

Use the exact supplied compatibility pair for M1:

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

Do not use the supplied AxiomPaper 4.0.4 with this client; it is API family 8.

AxiomPaper 5.0.4+1.21.4 is a **conditional upgrade candidate only** if runtime shows the matching slow-update/permission issue or the user explicitly changes the baseline.

## Research/static conclusions now locked

```text
LazyBuilder writes Sponge V2 .schem
→ Axiom 5.3.0 CLIENT parses it locally
→ Clipboard / Placement
→ Axiom client creates block buffer
→ AxiomPaper handles handshake / permissions / regions / bulk placement
```

Current schematic compatibility target:

```text
Sponge Version 2
Minecraft Java 1.21.4
DataVersion 4189
```

Axiom 5.3.0 recenters imported Sponge coordinates by schematic dimensions. LazyBuilder should export tight bounds and must not depend on WorldEdit/Sponge Offset metadata for the active Axiom paste pivot.

Normal entities are out of the current Sponge import contract. Block-entity NBT is deferred until a dedicated requirement/test exists.

## M1 writer proof — PASS

```text
workflow: M1 Schematic Smoke
run: 34215078021
result: PASS
artifact: lazybuilder-m1-schematic-je-1-21-4
artifact id: 10051411457
fixture target: Sponge V2 / JE_1_21_4 / DataVersion 4189
```

Exact fixture:

```text
lazybuilder_m1_smoke.schem
stone bricks
north-facing bottom straight stone-brick stair
top stone slab
```

## Next Step — exact runtime proof

### 1. Record environment preflight

Before changing versions/config, record what is actually installed:

```text
Minecraft client version
Fabric Loader version
Fabric API version
Axiom client version/hash
Paper version + exact build
AxiomPaper version/hash
OP vs permission-plugin setup
ViaVersion yes/no
WorldGuard yes/no
PlotSquared yes/no
CoreProtect yes/no
```

Do not guess unknown values.

### 2. Establish Axiom session

Use the supplied `Axiom 5.3.0` + `AxiomPaper 5.0.1` pair.

For first controlled test use OP or grant `axiom.default`, then reconnect.

If Axiom is not active:

```text
/whynoaxiom
/axiomhandshake
```

Diagnose permission/handshake before touching the schematic writer.

### 3. Import the exact M1 artifact

```text
lazybuilder_m1_smoke.schem
→ Axiom File / Import Schematic
→ confirm Clipboard
```

Expected file contract:

```text
Sponge V2
DataVersion 4189
3 × 1 × 1
```

### 4. Place without transformations

Use an empty test area. Do not rotate/scale/flip before the first proof.

```text
Clipboard
→ Ctrl+V Placement
→ confirm placement
```

Verify:

```text
stone bricks              correct
stair north/bottom/straight correct
slab top                  correct
```

### 5. Record exact outcome

M1 becomes end-to-end PASS only after:

```text
Axiom import
+ Clipboard
+ Paper placement
+ Minecraft state/orientation
= PASS
```

## Failure routing

```text
Import disabled
→ Axiom permission/session

unknown/unsupported schematic
→ schematic compatibility

imports but Clipboard wrong
→ Axiom client parsing/content

Clipboard correct but server placement fails
→ AxiomPaper permission/world/region/transport

placement works but stair/slab wrong
→ exporter / BlockState owner

slow update with otherwise correct permissions
→ measure first, then evaluate Paper 5.0.4 candidate
```

## Stop Boundary

Do not automatically:

- start M2 / install/configure Hunyuan3D-2mv;
- implement Minecraftize V0;
- add entity/NBT support;
- add Axiom automation/MCP/protocol code;
- tune AxiomPaper packet/rate settings;
- upgrade Axiom/AxiomPaper;
- promote `develop` to `Local` or `Local` to `main`.

The only active continuation is completing the exact Axiom/Paper/Minecraft M1 runtime proof.
