# Reference Intake Policy

Flow 2 establishes the source evidence LazyBuilder is allowed to interpret before shape generation.

## Canonical input modes

```text
T1 TEXT
I1 SINGLE IMAGE
I2 MULTIVIEW
```

### T1 — Text

Text does not go directly into Hunyuan3D-2mv.

```text
user text intent
→ pinned HunyuanDiT
→ reference_front.png + manifest.json
→ review / approval
→ Flow 3 Hunyuan3D-2mv
```

The generated reference is a **generated hypothesis**. It does not outrank user intent, explicit dimensions, or authoritative supplied references.

Do not independently generate four text-to-image views for MVP. Cross-view identity/proportion drift can create contradictory conditioning.

### I1 — Single image

Use one canonical named image, normally `front`, when only one reliable view exists.

Unseen sides remain inferred geometry rather than verified geometry.

### I2 — Multiview

Preferred controlled set:

```text
front
right
back
left
```

All views must describe the same design/version with reasonably consistent crop, scale, and perspective.

The generic generation runner accepts one to four named views, but the first controlled T1/I1/I2 acceptance comparison uses the complete front/right/back/left set for I2 so the mode boundary is unambiguous.

## Intake requirements

- preserve original references as authority;
- retain known real dimensions or intended Minecraft target size;
- surface material contradictions rather than averaging silently;
- text-generated references require review before shape generation;
- do not silently replace an acceptance input after the session snapshots it.

## Session integrity

For controlled acceptance, case inputs are SHA-256 snapshotted.

```text
input changed after snapshot
→ detect drift
→ invalidate affected owner explicitly
→ regenerate only true dependents
```

Do not consume silently changed input under an old session identity.

## Approval economy

Normal authoritative image references do not require ceremonial approval when intent is already settled.

T1 intentionally has one approval gate because the generated 2D reference introduces inferred geometry that can materially change later 3D output.

## Output

Flow 2 hands Flow 3 the settled T1/I1/I2 source path plus only material shape/scale constraints.

Detailed procedure: `kits/lazy-builder/intake/REFERENCE-INTAKE.md`.
