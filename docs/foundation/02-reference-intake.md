# Reference Intake Policy

Flow 2 establishes the source evidence LazyBuilder is allowed to interpret before shape generation.

## Supported input modes

### Image / multiview

Preferred set when side fidelity matters:

```text
front
right
back
left
```

One to four named views are allowed. Missing sides remain inferred geometry rather than verified geometry.

### Text

Text does not go directly into Hunyuan3D-2mv.

```text
user text intent
→ Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
→ reference_front.png
→ review / approval
→ Flow 3
```

The generated reference is a **generated hypothesis**. It does not outrank the user's text intent, explicit dimensions, or later authoritative references.

Do not independently generate four text-to-image views for MVP. Cross-view identity/proportion drift can create contradictory multiview conditioning.

## Intake requirements

- all supplied image views must describe the same design/version;
- crop/scale/perspective should be reasonably consistent when possible;
- preserve known real dimensions or intended Minecraft target size;
- retain original references as authority;
- surface material contradictions instead of averaging them silently;
- text-generated references require review before 3D generation.

## Approval economy

Normal authoritative image references do not require ceremonial approval when intent is already settled.

Text mode intentionally has one approval gate because the generated 2D reference introduces new inferred geometry that can materially change the later 3D result.

## Output

Flow 2 hands Flow 3 one settled named-view set plus only material shape constraints.

Detailed procedure: `kits/lazy-builder/intake/REFERENCE-INTAKE.md`.
