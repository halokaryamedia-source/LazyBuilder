# LazyBuilder Kit Agent Rules

Root `AGENTS.md` owns repository mode, continuity, authority, proof, branch policy, and the GPT Astra 6 ExtraHigh development profile. This file owns package-level file/mechanical routing and context economy. Normal Production Execution starts from `SKILL.md`.

## Open the smallest active owner

| Need | Owner |
|---|---|
| Reference set / side consistency / target dimensions | `intake/REFERENCE-INTAKE.md` |
| Hunyuan3D-2mv setup/generation | `generation/HUNYUAN3D-2MV.md` |
| Blender orientation/scale/cleanup/readiness | `blender/TARGET-MODEL.md` |
| block occupancy / stairs / slabs / Minecraft block-state conversion | `minecraftize/CONTRACT.md` |
| `.schem` serialization/export | `schematic/EXPORT.md` |
| acceptance / Axiom / Minecraft proof boundary | `validator/VALIDATION.md` |
| end-to-end production routing | `SKILL.md` |

Do not broad-read the kit. Expand only for a material dependency.

## Technical ownership

Current product source code is intentionally not invented before milestone implementation. When executable files are added, document their exact ownership here rather than creating parallel registries.

Expected implementation boundary:

```text
minecraftize/
→ Blender addon / geometry sampling / block-state selection

schematic/
→ thin adapter around existing schematic writer only if required

validator/
→ reusable static validation helpers only when concrete tests require them
```

Hunyuan remains an external provider/runtime, Blender remains the external workbench, and Axiom remains an external final editor.

## Astra6 package execution contract

Once the exact package owner is known, give Astra6 the owner plus the failing/changed contract—not the entire production chain.

```text
exact owner
+ current input/state
+ expected output/invariant
+ concrete failure or requested delta
+ acceptance criteria
```

Use Astra6 for semantic/architectural diagnosis and bounded implementation choices. Keep repeatable mechanics deterministic:

- grid/mesh sampling, coordinate transforms, and shape scoring belong in code;
- Minecraft BlockState transforms and validation belong in code/tests;
- `.schem` serialization belongs to the writer/adapter;
- actual Hunyuan, Blender, Axiom, and Minecraft behavior requires the matching runtime.

Do not ask the model to hand-author bulk block coordinates, large NBT structures, or repetitive geometry that a deterministic implementation can generate.

## Canonical vs derived

```text
reference / approved constraints
→ Hunyuan generated mesh
→ cleaned Blender target
→ Minecraftize block model
→ .schem
→ Axiom/Minecraft acceptance evidence
```

Generated downstream output never outranks reference authority.

## Context economy

```text
smallest owner/source
→ unresolved material dependency?
   no → continue
   yes → open smallest adjacent owner
→ stop when grounded
```

Prefer exact contracts and failing tests over narrative recaps. A high-reasoning model is expected to infer local consequences from authoritative source; do not duplicate the same rule across several files for convenience.

## Bounded technical changes

```text
observe drift
→ identify first wrong owner
→ smallest complete correction
→ regenerate/re-export only invalidated downstream output
→ cheapest proof that can falsify correction
→ stop
```

Do not solve a Minecraftize defect by silently changing the reference target or adding another model provider.

## Verification routing

- repository/doc routing → `tools/verify_repository.py`;
- Hunyuan generation → local Hunyuan runtime;
- Blender behavior → Blender runtime;
- conversion rules → targeted primitive/addon tests once executable code exists;
- `.schem` compatibility → writer/parser + Axiom runtime when claimed;
- Minecraft visual quality → actual Minecraft placement evidence.

## Anti-overdevelopment

Do not add databases, dependency-injection frameworks, model routers, custom renderers, generic registries, caching layers, ML training, alternate schematic formats, compatibility aliases, or Astra-specific infrastructure without a concrete defect.

The desired package is small, explicit, deterministic where possible, easy to test, and hard to misuse.
