# Schematic Validation & Axiom Handoff Policy

Flow 6 turns the Minecraft block model into a deliverable and proves only the claims actually tested.

## Writer boundary

Use `mcschematic` as the writer while it correctly carries required Minecraft Java BlockState strings and produces Axiom-compatible `.schem` output.

Do not build a custom Sponge/NBT serializer unless a concrete writer defect cannot be solved more simply.

## Validation layers

```text
repository/static contract
→ file can be produced by code / expected path and state strings

schematic compatibility
→ output can be parsed/opened by the intended schematic tooling

Axiom runtime
→ Axiom imports schematic to Clipboard

Minecraft runtime
→ structure can be placed in target Minecraft Java world

visual quality
→ in-world result preserves intended silhouette/detail sufficiently
```

Never claim a deeper layer from a shallower proof.

## MVP handoff success

The first end-to-end milestone passes when a generated `.schem` can be imported by Axiom and placed in Minecraft Java without format/state failure.

Quality improvements (stairs/slabs/etc.) build on this proven handoff rather than replacing it with a larger architecture.

Detailed owners: `kits/lazy-builder/schematic/EXPORT.md` and `kits/lazy-builder/validator/VALIDATION.md`.
