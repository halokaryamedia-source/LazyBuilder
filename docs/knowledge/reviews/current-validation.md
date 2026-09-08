# Current Validation Status

Updated: 2026-09-08

## Current system state

Working branch: `develop`.  
Verified integration baseline: `Local`.  
Stable branch: `main`.

LazyBuilder remains **pre-MVP**.

Current `develop` includes:

- PRD-Creator-style repository memory/governance;
- GPT Astra 6 ExtraHigh development profile;
- `remote_github` / `local` execution-mode routing;
- the first executable M1 schematic writer fixture.

Verified `Local` operating-system milestone:

```text
98046e2339aff0beff3caff8dee9030b258686ef
```

Current production chain remains:

```text
reference images
→ Hunyuan3D-2mv
→ GLB
→ Blender target
→ Minecraftize
→ .schem
→ Axiom
→ Minecraft Java
```

## Repository/governance evidence

Operating-system baseline was promoted through PR #1 after Local Promotion Verify passed. Subsequent Astra6 and execution-mode changes on `develop` passed Repository Verify.

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

Downloaded archive contents were checked:

```text
lazybuilder_m1_smoke.schem  382 bytes
lazybuilder_m1_smoke.json   488 bytes
```

The smoke workflow proves:

- `mcschematic==11.4.4` installs in the execution environment;
- a non-empty `.schem` is generated;
- the same `.schem` reloads successfully with `mcschematic`;
- exact BlockState equality survives round-trip for:
  - `minecraft:stone_bricks`;
  - north-facing bottom `stone_brick_stairs`;
  - top `stone_slab`.

The M1 fixture currently saves using `mcschematic.Version.JE_1_21_4`. This is a compatibility-test target, not a permanent global production target until actual Axiom/Minecraft runtime is confirmed.

Durable evidence is recorded in `reviews/history/m1-writer-smoke-2026-09-08.md`.

## Runtime proof status

```text
M1 writer / BlockState round-trip → PASS
Axiom import                     → LOCAL RUNTIME PROOF REQUIRED
Axiom Clipboard                  → LOCAL RUNTIME PROOF REQUIRED
Minecraft placement              → LOCAL RUNTIME PROOF REQUIRED
visual state/orientation          → LOCAL RUNTIME PROOF REQUIRED
```

Also not yet claimed:

- Hunyuan3D-2mv local generation on RTX 3070 8 GB;
- GLB import/cleanup in Blender;
- Minecraftize full-block conversion;
- Minecraftize stair/slab conversion;
- real-building visual fidelity.

## Evidence boundary

GitHub/static/writer execution proves only the behavior actually executed. It does not prove Axiom, Minecraft, GPU generation, Blender behavior, or visual fidelity.

M1 becomes end-to-end PASS only after the exact generated `lazybuilder_m1_smoke.schem` is imported into Axiom, appears in Clipboard, and is placed/checked in Minecraft Java.
