# Reference Intake

## Purpose

Settle material reference evidence and target constraints before Hunyuan3D shape generation.

## Canonical input modes

```text
T1 TEXT
I1 SINGLE IMAGE
I2 MULTIVIEW (front/right/back/left)
```

The three modes are independent input paths. None silently redefines another.

## Image mode

Preferred multiview set:

```text
front.png
right.png
back.png
left.png
```

One named canonical image is valid for I1. Four consistent views are required for the first controlled I2 comparison case.

Check:

- same object/design/version across views;
- no material shape contradiction;
- known dimensions/target Minecraft width retained;
- hidden/missing side uncertainty stated;
- user instruction remains higher authority than generated inference.

## Text mode

Text input first creates **one canonical front reference**:

```bash
python kits/lazy-builder/generation/generate_text_reference.py \
  --prompt "<user intent>" \
  --output-dir workspace/active/<project>/generated/text
```

Expected:

```text
reference_front.png
manifest.json
```

The manifest records the pinned HunyuanDiT model revision and output SHA-256.

The generated reference is evidence, not authority. Required gate:

```text
text intent
→ reference_front.png
→ review / approval
→ Hunyuan3D-2mv shape generation
```

Do not independently generate front/right/back/left from the same text for MVP; separate image generations can drift and create contradictory 3D conditioning.

## Handoff to generation

Hand Flow 3 only:

- approved/supplied named images;
- known dimensions or target Minecraft scale when material;
- shape constraints that affect generation;
- authoritative input paths retained so the session can lock SHA-256.

Do not create a broad project-metadata system before a real use case requires it.
