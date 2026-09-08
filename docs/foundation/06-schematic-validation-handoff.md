# Schematic Validation & Axiom Handoff Policy

Flow 6 serializes the canonical Minecraft block model, hands it to Axiom/Minecraft, and distinguishes preparation evidence from actual runtime proof.

## Writer boundary

Use `mcschematic==11.4.4` while it correctly carries required Minecraft Java BlockState strings and produces the audited target:

```text
Minecraft Java 1.21.4
Sponge Schematic Version 2
DataVersion 4189
```

Do not build a custom Sponge/NBT serializer unless a concrete writer defect cannot be solved more simply.

## Canonical handoff

```text
Minecraftize blocks.json
├→ canonical preview.svg
└→ mcschematic → build.schem
                 ↓
              Axiom client
                 ↓
          Clipboard / Placement
                 ↓
        AxiomPaper / Paper
                 ↓
             Minecraft
```

Preview and `.schem` share the same `blocks.json` source. The writer does not reinterpret or repair geometry.

## Validation layers

```text
Pre-Runtime Verification
→ repository/source/schema/digest/command consistency

writer round-trip
→ .schem can be produced/reloaded with exact expected BlockStates

Axiom runtime
→ exact generated .schem imports to Clipboard

Paper runtime
→ placement is accepted through AxiomPaper / Paper

Minecraft runtime
→ expected structure/states appear in the target world

visual fidelity
→ final result is acceptably faithful to reference/prepared target
```

Never claim a deeper layer from a shallower proof.

## Current static baseline

```text
writer/schema round-trip         → PASS
Axiom binary/static integration  → PASS (research/static)
Axiom import / Clipboard         → LOCAL RUNTIME PROOF REQUIRED
AxiomPaper / Paper placement     → LOCAL RUNTIME PROOF REQUIRED
Minecraft visual result          → LOCAL RUNTIME PROOF REQUIRED
```

## Runtime Acceptance boundary

The first end-to-end runtime milestone passes only when the **exact generated** schematic from the controlled session can be imported by Axiom, appears correctly in Clipboard, is placed through the target Paper/AxiomPaper environment, and produces the expected Minecraft result.

No hand-created replacement artifact may substitute for that proof.

## Failure ownership

```text
blocks.json wrong
→ Minecraftize

blocks.json correct + preview wrong
→ preview

blocks.json correct + .schem wrong
→ schematic exporter

.schem correct + Axiom import wrong
→ Axiom compatibility/session

Clipboard correct + server placement wrong
→ AxiomPaper/Paper permission/world/region/transport
```

Quality improvements such as stairs/slabs build on a proven V0 handoff rather than expanding architecture before evidence.

Detailed owners: `kits/lazy-builder/schematic/EXPORT.md` and `kits/lazy-builder/validator/VALIDATION.md`.
