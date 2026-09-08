# Axiom 1.21.4 Integration Baseline

Date: 2026-09-08  
Status: current

## Context

LazyBuilder uses Axiom as the final interactive placement/editor surface after `.schem` generation. The exact runtime files supplied for this project are:

```text
Axiom-5.3.0-for-MC1.21.4.jar
AxiomPaper-4.0.4-for-MC1.21.4.jar
AxiomPaper-5.0.1-for-MC1.21.4.jar
```

The integration must be based on the actual supplied binaries first, then supported by official Axiom documentation, official release metadata, and upstream source. Public documentation alone is insufficient for exact-version behavior because the current public docs can lag the supplied binary.

## Decision

Use this current compatibility baseline:

```text
Minecraft Java Edition 1.21.4

CLIENT
Fabric
Axiom 5.3.0
Axiom protocol/API family: 9

SERVER
Paper 1.21.4
AxiomPaper 5.0.1+1.21.4
Axiom protocol/API family: 9
```

`AxiomPaper 4.0.4` is rejected for this baseline because its Axiom API version is 8 while Axiom 5.3.0 uses API version 9.

The exact user-supplied binary fingerprints are:

```text
Axiom 5.3.0
sha256 8026fdb448686cd6db69e69c695fa17f54508f801ddddb3ffeb850b79b04eae5

AxiomPaper 4.0.4
sha256 f01b1b42ca21626d4c50359eab76bde4e361ea6614a7be5815d05fa81dd26a81

AxiomPaper 5.0.1
sha256 cecafb3e1beba81245ee5bcfc3251052035526b99bb111127b968b09c92d86c8
```

Do not commit these JAR files to LazyBuilder. The client JAR declares `All Rights Reserved`; the repository only records compatibility facts/fingerprints and keeps runtime binaries external.

## Integration architecture

The authoritative integration boundary is:

```text
LazyBuilder / mcschematic
→ Sponge .schem
→ Axiom 5.3.0 CLIENT parses file locally
→ Axiom Clipboard
→ Placement preview / transform / snap-to-ground
→ Axiom client creates block buffer
→ AxiomPaper 5.0.1 validates session + restrictions
→ Paper bulk placement into Minecraft world
```

Therefore:

1. `.schem` file-format compatibility is primarily an **Axiom client contract**.
2. AxiomPaper is primarily a **multiplayer permission/transport/placement contract**.
3. LazyBuilder does **not** need an Axiom protocol implementation.
4. LazyBuilder does **not** need a Paper-side schematic parser.
5. LazyBuilder does **not** need direct Axiom automation for MVP.
6. Keep `mcschematic` unless an executed compatibility defect proves it inadequate.

## Schematic contract

For the current environment, use:

```text
Sponge Schematic Version 2
DataVersion 4189
Minecraft Java 1.21.4
```

This aligns with the current M1 `mcschematic.Version.JE_1_21_4` output and with the fact that Axiom 5.3.0's own schematic exporter writes Sponge Version 2.

Axiom 5.3.0's supplied binary accepts Sponge Version 2 and Version 3. The current file picker also accepts `.schem`, `.schematic`, and `.litematic`; LazyBuilder intentionally exports only `.schem`.

## Imported origin / pivot behavior

For Sponge schematic import, Axiom 5.3.0 recenters the loaded block coordinates using the schematic dimensions:

```text
localX = x - floor(width / 2)
localY = y - floor(height / 2)
localZ = z - floor(length / 2)
```

Block-entity positions are transformed the same way.

Do not rely on Sponge `Offset`, `WEOffsetX/Y/Z`, or related metadata to control the active Axiom Clipboard pivot. Those fields may be preserved/re-emitted as schematic metadata, but the observed import coordinate calculation is based on dimensions.

LazyBuilder should therefore export tight bounds and treat final placement positioning as Axiom Placement/UI responsibility.

## Data-version behavior

Axiom 5.3.0 upgrades older schematic BlockStates using Minecraft's DataFixer when the schematic DataVersion is older than the client. When the schematic is current or newer, it parses the serialized BlockState directly.

For deterministic current integration, LazyBuilder should emit the exact current Minecraft 1.21.4 DataVersion rather than a future DataVersion.

## Entities and block entities

For Sponge `.schem` import in the supplied Axiom 5.3.0 binary:

- blocks are supported;
- block entities are parsed when valid `Pos` and `Id` data is present and the target BlockState supports the block entity;
- the Sponge import path constructs an empty normal-entity list, so LazyBuilder must not promise entity preservation through this path.

MVP remains blocks only. Block-entity/NBT support is deferred until a separate executable test proves the exact required use case.

On Paper placement, block-entity NBT additionally requires `axiom.build.nbt`. Basic M1 full/stair/slab proof does not need NBT.

## Permissions

For multiplayer, the supplied AxiomPaper 5.0.1 exposes:

```text
axiom.all
axiom.default
axiom.use
axiom.can_import_blocks
axiom.can_export_blocks
axiom.build.place
axiom.build.section
axiom.build.nbt
...
```

`axiom.default` includes the normal import/build/editor capability set. The simplest controlled runtime proof may use OP; a permission-managed non-OP test should grant `axiom.default` and reconnect before retesting.

Axiom client import UI is itself permission-aware: the supplied client checks `CAN_IMPORT_BLOCKS` and can disable Import Schematic when the server disallows importing.

## Paper placement restrictions

Before applying a received block buffer, AxiomPaper 5.0.1 checks, among other things:

- active Axiom session/handshake;
- dispatch/rate budget;
- `BUILD_SECTION` permission;
- matching world/dimension;
- world whitelist/blacklist configuration;
- `AxiomModifyWorldEvent` cancellation;
- region/section integration checks;
- separate `BUILD_NBT` permission for block-entity NBT.

The server then applies blocks in chunk/section batches and updates related chunk data such as lighting/POI/block entities. This is not command-per-block placement.

## Paper config baseline

Keep the supplied AxiomPaper 5.0.1 defaults unless an executed test proves a need to change them.

Important defaults include:

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

Do not enable `allow-large-payload-for-all-packets` merely for theoretical headroom. The plugin explicitly treats that setting as inappropriate for public servers unless there is a demonstrated need.

## Region / plugin integrations

AxiomPaper 5.0.1 declares soft dependencies on:

```text
CoreProtect
ViaVersion
WorldGuard
PlotSquared
```

They are optional for the basic M1 path. Their presence can change diagnostics, compatibility handling, region restrictions, and logging, so actual runtime evidence must record relevant installed integrations.

## Upgrade policy

AxiomPaper `5.0.4+1.21.4` exists and its official changelog says it fixes slow updates caused by permission issues.

Do **not** silently replace the supplied `5.0.1` baseline. Use 5.0.1 for reproducible M1 testing. Consider 5.0.4 only when:

1. M1/runtime evidence shows a matching slow-update/permission symptom; or
2. the user explicitly chooses to update the runtime baseline.

Any baseline change requires a new fingerprint and compatibility record.

## Blueprint boundary

Axiom Blueprints (`.bp`) are a separate Axiom asset system optimized for browsing/searching and may be shared through a server when enabled.

LazyBuilder MVP does not use `.bp`, server blueprint sharing, or blueprint upload APIs. `.schem` remains the handoff format.

## License / multiplayer operational note

Official Axiom documentation states that multiplayer support on private servers is primarily a Commercial License feature, with a whitelist path for qualifying non-commercial use. Commercial use requires the applicable Axiom license.

This is an operational/licensing constraint, not a file-format requirement. It must be handled by the deployment owner; LazyBuilder must not try to bypass it.

## Not chosen

Do not add by default:

- custom Sponge/NBT serializer;
- Axiom protocol client/server implementation;
- Paper schematic parser;
- `.bp` output;
- Axiom JAR redistribution;
- automatic AxiomPaper upgrade;
- packet/config tuning without an observed bottleneck;
- entity/NBT support without a concrete build requirement and test.

## Evidence owner

Full binary/public-reference evidence is recorded in:

`docs/knowledge/reviews/history/axiom-audit-2026-09-08.md`

Runtime acceptance remains owned by:

`kits/lazy-builder/validator/VALIDATION.md`
