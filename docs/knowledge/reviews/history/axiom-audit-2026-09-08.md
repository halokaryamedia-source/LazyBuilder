# Axiom Integration Audit — 2026-09-08

Status: research/static audit complete; runtime placement proof still required  
Scope: LazyBuilder → `.schem` → Axiom 5.3.0 → AxiomPaper 5.0.1 → Minecraft Java 1.21.4

## Purpose

This audit establishes the exact Axiom integration boundary for LazyBuilder before more Minecraftize/Hunyuan development begins.

The goal is to answer:

1. which supplied Axiom/Paper binaries form the correct 1.21.4 pair;
2. who actually parses `.schem`;
3. what schematic format/version Axiom 5.3.0 accepts;
4. how imported coordinates/origin are handled;
5. how Clipboard/Placement hands data to Paper;
6. which permissions/config/region checks can block placement;
7. which limits are real integration constraints;
8. what LazyBuilder must implement versus deliberately not implement.

This review records research/static evidence only. Axiom import/Clipboard/Minecraft placement remain runtime claims until executed in the user's real environment.

---

## 1. Evidence sources and precedence

For exact current-environment behavior, evidence precedence in this audit is:

```text
current explicit user runtime intent
→ exact supplied binary/JAR contents
→ actual future runtime execution
→ official version-specific release metadata
→ official Axiom documentation
→ current upstream AxiomPaper source
→ general assumptions/history
```

The exact supplied binaries outrank current upstream source for 5.0.1-specific behavior because upstream may have changed after 5.0.1.

The public Axiom docs are useful but currently state `Last Documentation Update: 31/Jul/25`; the supplied Axiom 5.3.0 binary therefore resolves any exact-version discrepancy.

Public references:

- Axiom docs: https://axiomdocs.moulberry.com/
- File / Import Schematic: https://axiomdocs.moulberry.com/editor/mainmenubar/file.html
- Clipboard: https://axiomdocs.moulberry.com/editor/windows/clipboard.html
- Placement: https://axiomdocs.moulberry.com/editor/placement.html
- Commands: https://axiomdocs.moulberry.com/advanced/commands.html
- Configuration: https://axiomdocs.moulberry.com/advanced/configuration.html
- Blueprints: https://axiomdocs.moulberry.com/editor/windows/blueprints.html
- Multiplayer whitelist: https://axiomdocs.moulberry.com/other/whitelist.html
- Commercial license: https://axiomdocs.moulberry.com/other/commerciallicense.html
- AxiomPaper source/README: https://github.com/Moulberry/AxiomPaperPlugin
- Axiom 5.3.0 / MC 1.21.4: https://modrinth.com/mod/axiom/version/b7V5vQES
- AxiomPaper 5.0.1 / MC 1.21.4: https://modrinth.com/plugin/axiom-paper-plugin/version/5.0.1%2B1.21.4
- AxiomPaper 5.0.4 / MC 1.21.4: https://modrinth.com/plugin/axiom-paper-plugin/version/5.0.4%2B1.21.4

---

## 2. Supplied binary inventory

### Axiom client

```text
file: Axiom-5.3.0-for-MC1.21.4.jar
sha256: 8026fdb448686cd6db69e69c695fa17f54508f801ddddb3ffeb850b79b04eae5
```

`fabric.mod.json` establishes:

```text
id: axiom
version: 5.3.0
description: Client-side building utility mod
license: All Rights Reserved
minecraft: >=1.21.4 <1.21.5
fabricloader: >=0.14.21
fabric-api: required
java: >=17
```

Declared breaks include old/incompatible Sodium, OptiFabric, and older Immersive Portals ranges. Exact local modpack compatibility remains a runtime concern.

Official Modrinth also lists Axiom 5.3.0 for Minecraft 1.21.4/Fabric.

### AxiomPaper candidate A

```text
file: AxiomPaper-4.0.4-for-MC1.21.4.jar
sha256: f01b1b42ca21626d4c50359eab76bde4e361ea6614a7be5815d05fa81dd26a81
Axiom API_VERSION: 8
```

This is not the correct baseline for Axiom 5.3.0.

### AxiomPaper candidate B

```text
file: AxiomPaper-5.0.1-for-MC1.21.4.jar
sha256: cecafb3e1beba81245ee5bcfc3251052035526b99bb111127b968b09c92d86c8
plugin version: 5.0.1+1.21.4
api-version: 1.21
Axiom API_VERSION: 9
```

Soft dependencies:

```text
CoreProtect
ViaVersion
WorldGuard
PlotSquared
```

Official Modrinth states 5.0.0 added Axiom 5.0+ support; 5.0.1 then fixed restrictions re-sending on re-handshake and improved empty BlockState conversion.

### Compatibility verdict

The supplied Axiom 5.3.0 client uses API version 9 in its hello packet. AxiomPaper 5.0.1 expects API version 9. AxiomPaper 4.0.4 expects API version 8.

Therefore:

```text
Axiom 5.3.0 + AxiomPaper 5.0.1 → static protocol-family match
Axiom 5.3.0 + AxiomPaper 4.0.4 → reject for baseline
```

Actual handshake still requires runtime proof.

---

## 3. Actual integration architecture

This is the most important result of the audit.

AxiomPaper does **not** need to parse LazyBuilder's `.schem` file.

The actual path is:

```text
LazyBuilder creates .schem
        ↓
Axiom CLIENT opens local file
        ↓
Axiom client parses schematic into ClipboardObject
        ↓
Clipboard → Placement
        ↓
client calculates final block buffer
        ↓
AxiomPaper receives/validates block buffer
        ↓
Paper modifies world in chunk/section batches
```

Consequences:

- schematic-format compatibility is a client-side contract;
- Paper plugin compatibility is a multiplayer placement/session contract;
- no Axiom network protocol should be implemented in LazyBuilder;
- no server-side `.schem` loader should be built;
- no direct Paper integration is needed for the MVP exporter.

---

## 4. Axiom 5.3.0 import support

### File picker

The supplied Axiom 5.3.0 client currently allows three extensions:

```text
schem
schematic
litematic
```

The older public File documentation mentions `.schem` and `.schematic`; binary inspection shows `.litematic` is also accepted by this exact client.

LazyBuilder should not widen its output formats because of this. `.schem` remains the one output contract.

### Format sniffing

The supplied client reads NBT and chooses its loader based on content:

```text
Regions   → Litematic
Version   → Sponge schematic
Materials → legacy pre-1.13 schematic
otherwise → Unknown format
```

On successful non-empty load, the client calls its Clipboard setter. This confirms that `Import Schematic → Clipboard` is local client behavior.

### Import permission gate

Before showing/using Import Schematic on multiplayer, the supplied client checks `CAN_IMPORT_BLOCKS`. If the Paper server restrictions do not allow it, the File menu can display import as disabled with a server-disallowed message.

For M1, `axiom.can_import_blocks` therefore matters before file parsing is even reached on multiplayer.

---

## 5. Sponge schematic behavior in Axiom 5.3.0

### Supported Sponge schema versions

The supplied `SchematicLoader$SpongeSchematic.parse` accepts exactly:

```text
Version = 2
Version = 3
```

Other Sponge Version values result in an unsupported-version load error.

### Sponge Version 2 fields

The supplied parser requires/uses:

```text
DataVersion  int
Width        short
Height       short
Length       short
Palette      compound
BlockData    byte array
```

Optional/supporting data includes:

```text
Metadata.Name
BlockEntities
additional remaining tags/metadata
```

Dimensions are interpreted as unsigned shorts (`value & 65535`), so the parser can represent up to 65535 per dimension at the schema-read level. This is **not** a claim that structures near that scale are operationally safe; performance/memory/transport limits require separate tests.

### Sponge Version 3

The supplied client also contains a V3 parser where block palette/data are read from a `Blocks` compound. LazyBuilder has no present reason to move to V3.

### Why V2 remains preferred

Axiom 5.3.0's own `SaveSchematicAction` writes Sponge `Version = 2` and produces the same general family of fields used by `mcschematic`:

```text
Version
DataVersion
Width / Height / Length
Metadata
Offset
BlockData
BlockEntities
Palette
PaletteMax
```

It writes GZIP NBT with root name `Schematic`.

This is strong structural evidence that the current `mcschematic` V2 path is appropriate for the target client. There is no demonstrated value in writing a custom format implementation.

---

## 6. DataVersion / BlockState behavior

When loading a Sponge schematic, Axiom 5.3.0 compares schematic `DataVersion` with its current Minecraft data version.

Observed behavior:

```text
schematic older than current client
→ build BlockState NBT
→ Minecraft DataFixer updateBlockState
→ use upgraded state

schematic current or newer
→ parse serialized BlockState string directly
```

Integration policy:

- emit current target DataVersion `4189` for Minecraft 1.21.4;
- do not intentionally emit a future DataVersion;
- preserve exact vanilla serialized BlockState strings;
- validate state orientation/property round-trip with executable tests.

The current M1 file already uses:

```text
Sponge Version: 2
DataVersion: 4189
Width: 3
Height: 1
Length: 1
```

and contains the expected stone-bricks/stair/slab palette.

---

## 7. Block-data ordering

The Axiom Sponge loader reads block palette indices with this coordinate nesting:

```text
for y
  for z
    for x
```

So X varies fastest, then Z, then Y.

`mcschematic` already handles the actual serialization ordering. LazyBuilder should not duplicate this logic in prose or build a second serializer.

---

## 8. Clipboard origin / placement pivot

### Critical finding

Axiom 5.3.0 does not use Sponge `Offset`/WorldEdit offset metadata as the active imported Clipboard origin.

During Sponge import, it inserts each block at:

```text
x - floor(width / 2)
y - floor(height / 2)
z - floor(length / 2)
```

Block entities receive the same coordinate transformation.

For the current M1 file (`3 × 1 × 1`), the three imported X positions are therefore expected around:

```text
-1, 0, +1
```

### Metadata behavior

The client retains additional schematic metadata and its exporter contains logic for `WEOffsetX/Y/Z`, `Offset`, and WorldEdit origin fields when re-exporting/downgrading. That metadata preservation does not change the observed load-time centering calculation.

### LazyBuilder consequence

- export tight bounds;
- do not build a custom origin-offset abstraction just to control Axiom paste pivot;
- final positioning belongs to Axiom Placement/Gizmo;
- use Axiom's `Snap to ground` when appropriate;
- add an explicit anchor system only if a real project later proves centered placement insufficient.

---

## 9. Air behavior

A `.schem` is a bounded volume; cells not occupied by non-air structure are effectively air within that volume.

The supplied Axiom Placement defaults include `pasteAir = true`, and public docs expose a `Paste Air` option.

Implications:

- tight bounds reduce accidental clearing;
- runtime handoff must be aware of `Paste Air` when placing into an existing build;
- use an empty test area for M1;
- LazyBuilder should not invent a nonstandard no-air schematic format;
- if non-destructive placement is desired, that is a Placement option/policy, not an exporter format fork.

---

## 10. Entities

The supplied Axiom Sponge import path creates its Clipboard object with an empty normal-entity list.

Therefore LazyBuilder must treat entity preservation through Sponge `.schem` as unsupported/unproven for this integration baseline.

This does not conflict with Axiom's general Placement `Paste Entities` option; that option can apply when a Clipboard source actually contains entities. It is not evidence that imported Sponge entity data is preserved by this exact path.

MVP remains blocks-only.

---

## 11. Block entities / NBT

Axiom 5.3.0 can import Sponge block-entity data when:

- a block-entity entry has `Pos`;
- it has a valid `Id`;
- that block-entity type is valid for the target BlockState.

The client removes positional/type wrapper fields before compressing the payload and stores the compressed block entity at the centered local coordinate.

On AxiomPaper 5.0.1, the received block buffer only exposes block-entity NBT to the placement operation when the player has `BUILD_NBT` / `axiom.build.nbt`.

Additional server restriction:

- game-master block NBT requires sufficient operator permission; otherwise the server warns and does not apply that privileged data.

LazyBuilder M1/V0/V1 does not require block entities. Add NBT support only when a concrete block family/use case requires it, then create a dedicated executable test.

---

## 12. Clipboard and Placement behavior

Official docs confirm:

```text
Import Schematic
→ Clipboard
→ Ctrl+V creates Placement
→ Enter or Ctrl+V confirms
```

Placement can be repositioned/rotated with the Gizmo. Documented options include:

- Keep Existing;
- Merge Blocks;
- Paste Air;
- Paste Entities;
- Unlock Rotation;
- Rotate/Scale;
- Flip;
- Snap to ground;
- Paste / Paste Copy / Paste and Select.

Binary defaults in the supplied client include:

```text
keepExisting = false
prioritizeFullBlocks = false
pasteAir = true
pasteEntities = true
unlockRotation = false
reposition = true
```

These are client UI/runtime defaults, not LazyBuilder file-format rules.

---

## 13. AxiomPaper handshake

The supplied AxiomPaper 5.0.1 `HelloPacketListener` checks the client hello before Axiom becomes active.

Important checks:

1. user is permitted to use Axiom;
2. Axiom API version matches the plugin's expected API 9;
3. client/server data/protocol compatibility is acceptable;
4. configured mismatch policy is applied.

The supplied default config uses:

```text
unsupported-axiom-version: warn
incompatible-data-version: warn
```

For these `warn` policies, incompatibility warns and disables the Axiom session instead of establishing a valid active editor session.

Diagnostics:

- official plugin README recommends OP or `axiom.default`, followed by reconnect;
- `/whynoaxiom` provides status/diagnostic information;
- official Axiom docs describe `/axiomhandshake` as a connection test/re-handshake command.

---

## 14. AxiomPaper permissions

### High-level permissions in supplied 5.0.1

```text
axiom.all
axiom.default
axiom.use
axiom.can_import_blocks
axiom.can_export_blocks
```

`axiom.default` includes the recommended normal build/editor permission families.

### Placement-specific permissions

```text
axiom.build.place
axiom.build.section
axiom.build.nbt
```

The server block-buffer path explicitly checks `BUILD_SECTION` before queuing placement. NBT is separately gated.

### M1 permission profile

M1 requires no entity or block-entity NBT capability. A controlled baseline can use either:

```text
OP
```

or:

```text
axiom.default
+ reconnect
```

Using granular permissions is useful later, but not necessary to prove the first compatibility chain.

---

## 15. World/region restrictions

AxiomPaper 5.0.1's `canModifyWorld` checks:

- `whitelist-world-regex` when configured;
- `blacklist-world-regex` when configured;
- `AxiomModifyWorldEvent`, which another plugin can cancel.

During bulk section modification, the operation also calls integration section permission checks. WorldGuard/PlotSquared or another integration can therefore veto/restrict parts of a placement even when the Axiom handshake itself is active.

Failure diagnosis must distinguish:

```text
Axiom inactive
vs
Import permission denied
vs
World forbidden
vs
Region/section denied
vs
BlockState/file problem
```

---

## 16. Server block-buffer placement model

AxiomPaper 5.0.1 does not place every block by dispatching normal commands.

The received block buffer is processed by a bulk `SetBlockBufferOperation` that:

- groups data into chunk/section work;
- checks section/region permissions;
- works within world build-height section bounds;
- updates chunk section BlockStates;
- updates lighting-relevant state;
- updates POI changes;
- creates/replaces/removes block entities as needed;
- optionally loads NBT when permitted;
- can log placement/removal through CoreProtect integration;
- sends/relights changed chunks.

This matters for LazyBuilder because output performance should be tested as bulk schematic placement, not modeled as command-per-block cost.

---

## 17. Packet/rate limits and safe defaults

Supplied AxiomPaper 5.0.1 initial/internal limits include:

```text
packet collection read limit: 1024
NBT decompression limit: 131072 bytes
available dispatch sends/default rate base: 1024
max chunk load distance default: 256
```

Relevant supplied config:

```text
allow-large-chunk-data-request: false
allow-large-payload-for-all-packets: false
max-block-buffer-packet-size: 0x100000
block-buffer-rate-limit: 0
```

When `allow-large-payload-for-all-packets` is enabled, the plugin increases broad packet/NBT limits. The config itself warns against doing this for public servers.

Integration policy:

- keep defaults during M1;
- do not derive a fake maximum schematic size from one packet-size constant;
- do not tune packet sizes/rates until a real large-build benchmark fails;
- if scale becomes an issue, measure actual placement throughput and failure mode first.

---

## 18. Disallowed blocks

The supplied config supports a `disallowed-blocks` list, including full serialized states.

AxiomPaper builds the allowed block registry/restrictions from this configuration, so a server can forbid a block or specific state independent of whether the `.schem` is syntactically valid.

For future Minecraftize palette validation:

- a valid vanilla BlockState can still be operationally rejected by server policy;
- server `disallowed-blocks` should be treated as runtime/deployment constraints, not baked into the general converter unless the project explicitly supplies such a restriction set.

---

## 19. Optional integrations

AxiomPaper 5.0.1 soft-depends on:

- CoreProtect: optional change logging;
- ViaVersion: can affect cross-version protocol/data compatibility handling;
- WorldGuard: region restrictions;
- PlotSquared: plot/edit bounds.

Basic M1 should preferably minimize variables and record whether these plugins are installed. Their absence is not an error for the core path.

---

## 20. Blueprints are not the integration format

Official docs describe Axiom Blueprints as a separate `.bp` asset format optimized for browsing/searching/thumbnail metadata. Local blueprints normally live under Axiom's configuration path; multiplayer blueprint sharing is a separate server feature.

Supplied AxiomPaper config defaults:

```text
blueprint-sharing: false
```

LazyBuilder therefore remains:

```text
.schem only
```

No `.bp` exporter, server blueprint upload, or Blueprint API integration is needed.

---

## 21. Upgrade observation: Paper 5.0.4

Official Modrinth has `AxiomPaper 5.0.4+1.21.4`, whose changelog is specifically:

```text
Fix slow updates due to permission issues
```

This is useful research but not a reason to silently alter the known environment.

Policy:

```text
baseline = supplied 5.0.1

if actual runtime has slow-update/permission symptom
→ evaluate 5.0.4
→ fingerprint it
→ rerun M1/placement proof
→ update decision if adopted
```

---

## 22. Licensing / deployment boundary

The supplied Axiom client declares `All Rights Reserved`.

Official Axiom docs state that multiplayer support on private servers is primarily included through the Commercial License, while qualifying non-commercial users can request a whitelist; commercial use requires the applicable license.

LazyBuilder must:

- not commit/redistribute the client JAR;
- not bypass Axiom licensing/whitelist mechanisms;
- treat licensing as deployment responsibility separate from schematic compatibility.

AxiomPaper's public repository is MIT-licensed, but that does not change the client license.

---

## 23. LazyBuilder integration decisions resulting from audit

### Keep

```text
mcschematic==11.4.4
Sponge V2
JE_1_21_4 / DataVersion 4189
.schem output
Axiom as manual placement/editor surface
```

### Explicitly avoid

```text
custom NBT/Sponge writer
Axiom protocol implementation
Paper-side schematic loader
Axiom MCP/automation
.bp/Blueprint output
entity output
block-entity NBT before separate test
origin metadata hacks
packet tuning before evidence
```

### New exporter rules

- export tight bounds;
- output canonical serialized BlockStates;
- target the exact current Minecraft DataVersion;
- do not depend on Sponge/WorldEdit offset metadata for Axiom pivot;
- treat imported pivot as center-of-bounds behavior;
- treat normal entities as out of scope;
- keep BlockEntity NBT disabled/unimplemented until required.

### New validation rules

M1 runtime proof must record:

```text
Minecraft client version
Fabric Loader version
Fabric API version
Axiom client version + hash
Paper server version/build
AxiomPaper version + hash
OP or permission setup
relevant WorldGuard/PlotSquared/ViaVersion/CoreProtect presence
/whynoaxiom result if handshake fails
Import Schematic result
Clipboard result
Placement result
BlockState visual/orientation result
```

---

## 24. Current known vs unknown

### Static/research PASS

```text
correct supplied plugin pair identified       PASS
Axiom API family 9 match                       PASS
client-side .schem parsing architecture        PASS
Sponge V2/V3 support identified                PASS
mcschematic V2 structural match                PASS
centered imported coordinate behavior          PASS
Paper permission/placement path identified     PASS
M1 writer round-trip                           PASS
```

### Runtime still required

```text
actual Fabric/Axiom startup                    REQUIRED
actual Paper/AxiomPaper startup                REQUIRED
actual API9 handshake                          REQUIRED
actual Import Schematic permission             REQUIRED
actual M1 .schem import                        REQUIRED
actual Clipboard contents                      REQUIRED
actual placement on server                     REQUIRED
actual stair/slab orientation                  REQUIRED
large-build performance                        LATER
NBT/block-entity placement                     LATER
```

---

## Final audit conclusion

The Axiom integration should stay simple.

LazyBuilder owns the geometry-to-Minecraft conversion and Sponge `.schem` generation. Axiom 5.3.0 owns client-side schematic parsing, Clipboard and Placement. AxiomPaper 5.0.1 owns multiplayer handshake/restrictions and bulk world modification.

There is currently no evidence-based need for any custom Axiom/Paper integration layer beyond producing a correct, tightly bounded Sponge V2 `.schem` for Minecraft Java 1.21.4 and validating the exact runtime handoff.
