---
name: build-production
description: Reusable production judgment for LazyBuilder reference-to-schematic work. Route a build through reference intake, Hunyuan3D-2mv, Blender target preparation, Minecraftize conversion, schematic export, and runtime validation without inventing source geometry or expanding the tool stack.
---

# Build Production

Use for normal LazyBuilder Production Execution and bounded build revisions. Changes to LazyBuilder itself route to `development-brief`.

## Route first

```text
new / materially uncertain reference set
→ intake

reference settled, 3D missing
→ Hunyuan3D-2mv generation

3D generated but unusable/noisy
→ Blender target preparation

target acceptable, Minecraft output missing/wrong
→ Minecraftize

block model correct, schematic export wrong
→ schematic owner

schematic valid, Axiom/Minecraft claim unproved
→ runtime validation owner
```

Start with the smallest owner that can settle the issue. Expand only for a real dependency or contradiction.

## Canonical sequence

```text
user instruction + reference images
→ reference intake / consistency check
→ Hunyuan3D-2mv shape-only generation
→ GLB
→ Blender orientation / scale / light cleanup
→ Minecraftize preview
→ full-block baseline first
→ stairs/slabs only when current milestone supports them
→ mcschematic export
→ .schem
→ Axiom import / Minecraft placement proof when required
```

## Cross-flow invariants

- Current user instruction and authoritative references outrank generated geometry.
- Hunyuan3D-2mv is the only active 3D provider for MVP.
- Do not regenerate or add another provider merely because one result is imperfect; diagnose reference consistency, generation, cleanup, or Minecraft conversion first.
- Blender cleanup is bounded: fix geometry only when it materially improves Minecraft conversion.
- Minecraftize begins rule-based and incremental; do not invent ML/optimizer frameworks before a demonstrated failure requires them.
- `mcschematic` owns file writing while it remains sufficient; do not recreate Sponge/NBT serialization for convenience.
- Axiom/manual polish is downstream delivery behavior, not proof that LazyBuilder engine output was already correct.
- Static checks do not prove GPU generation, Blender, Axiom, or Minecraft runtime behavior.

## First wrong owner

```text
reference conflict / missing side / intended dimensions
→ intake

Hunyuan setup or GLB generation
→ generation

orientation / scale / obvious mesh noise
→ Blender target owner

block occupancy / stair / slab / block-state selection
→ Minecraftize

schematic serialization
→ schematic exporter

acceptance/runtime evidence
→ validator
```

## Stop condition

Stop when requested build scope is complete and evidence supports the claim. Do not automatically add another block family, model provider, automation layer, or cleanup pass merely because more improvement is possible.
