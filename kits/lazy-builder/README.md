# LazyBuilder Product Package

This package owns detailed Flow 2–6 production procedure and future executable implementation. Root `AGENTS.md` owns repository work mode/continuity; `docs/foundation/` owns durable product policy.

## Package architecture

```text
kits/lazy-builder/
├── AGENTS.md
├── README.md
├── SKILL.md
├── intake/        reference input procedure
├── generation/    Hunyuan3D-2mv procedure
├── blender/       target-model preparation contract
├── minecraftize/  Minecraft conversion contract + future addon
├── schematic/     export contract
└── validator/     acceptance / runtime-proof contract
```

## Product chain

```text
reference images
→ intake
→ Hunyuan3D-2mv
→ model.glb
→ Blender target preparation
→ Minecraftize
→ Minecraft block preview
→ mcschematic
→ .schem
→ Axiom / Minecraft validation
```

## Current implementation state

The package is currently procedure-first / pre-executable-MVP. No claim is made that Hunyuan setup, Minecraftize code, or Axiom runtime validation has already been implemented in this repository.

## Architecture rule

Add implementation only to the owner that actually needs it. Do not create parallel kits for Hunyuan, Blender, schematic, or Minecraftize; they remain categorized domains of one LazyBuilder product package.
