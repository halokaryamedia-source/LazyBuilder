---
name: lazy-builder
version: 0.1.0-dev
---

# LazyBuilder

Use for normal Production Execution and bounded build revisions. Changes to LazyBuilder itself route to repository Development.

## Route first

```text
reference meaning / side consistency uncertain
→ intake

reference settled, 3D missing
→ generation

3D generated but conversion target unusable
→ Blender target preparation

target correct, Minecraft model missing/wrong
→ Minecraftize

block model correct, schematic output wrong
→ schematic

schematic produced, runtime acceptance unresolved
→ validator
```

Start with the smallest owner that can settle the issue. Expand only for a real dependency or contradiction.

## Canonical sequence

```text
reference images / instruction
→ reference consistency + target constraints
→ Hunyuan3D-2mv shape-only generation
→ GLB
→ Blender orientation / scale / bounded cleanup
→ Minecraftize preview
→ current supported block shapes
→ mcschematic export
→ `.schem`
→ Axiom import / Minecraft placement proof when required
```

## Cross-flow invariants

### Authority decreases downstream

```text
current user instruction
→ approved decisions
→ authoritative references
→ generated Hunyuan geometry
→ Blender working target
→ Minecraftize block model
→ schematic / Axiom / screenshots
```

Generated output never repairs or outranks its upstream owner.

### One provider for MVP

Hunyuan3D-2mv is the only active 3D provider. Do not add provider routing as a production shortcut.

### Conversion evolves incrementally

```text
full block
→ stairs
→ slabs
→ only then extra block families from real evidence
```

Rule-based conversion precedes complex optimization/ML.

### Proof stays truthful

Repository checks prove repository contracts. Local Hunyuan/Blender/Axiom/Minecraft claims require actual runtime evidence.

## First wrong owner

```text
reference conflict / intended geometry / dimensions
→ intake

Hunyuan setup / generation
→ generation

orientation / scale / severe mesh noise
→ Blender

occupancy / stair / slab / block state
→ Minecraftize

schematic writing
→ schematic

runtime acceptance
→ validator
```

## Artifact lifecycle

Typical local project package (ignored by Git):

```text
workspace/active/<project>/
├── references/
├── generated/
│   └── model.glb
├── blender/
│   └── project.blend
└── output/
    └── build.schem
```

This is a working convention, not a requirement to commit project data.

## Stop condition

Stop when requested scope is complete and evidence supports the claim. Do not continue into another block family, provider, optimizer, or automation layer merely because more work is possible.
