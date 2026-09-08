# Reference Intake

## Purpose

Settle material reference evidence and target constraints before Hunyuan3D shape generation.

## Image mode

Preferred set:

```text
front.png
right.png
back.png
left.png
```

One to four views are allowed. More views are not automatically better; consistent views are more valuable than many conflicting views.

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
text_reference.json
```

The reference is generated evidence, not authority. Review it against the user's intent before using it for shape generation.

Required gate:

```text
text intent
→ reference_front.png
→ review / approval
→ generation
```

Do not independently generate front/right/back/left from the same text for MVP; separate image generations can drift and create contradictory 3D conditioning.

## Handoff to generation

Hand Flow 3 only:

- approved/supplied named images;
- known dimensions or target Minecraft scale when material;
- only shape constraints that affect generation.

Do not create a broad project-metadata system before a real use case requires it.
