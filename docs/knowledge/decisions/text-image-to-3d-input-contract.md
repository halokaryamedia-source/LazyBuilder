# Text / Image to 3D Input Contract

Status: current

## Decision

LazyBuilder supports two input paths but keeps **one 3D provider**:

```text
IMAGE / MULTIVIEW
front / right / back / left
→ Hunyuan3D-2mv
→ shape-only GLB

TEXT
→ Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
→ reference_front.png
→ user review / approval
→ Hunyuan3D-2mv
→ shape-only GLB
```

HunyuanDiT is an auxiliary 2D reference generator. It is not a second 3D provider.

## Why this shape

- Hunyuan3D-2mv is explicitly a 1–4 view image-to-shape model, not a direct text-to-3D model.
- Tencent's Hunyuan3D-2 application implements text input by generating an image first with HunyuanDiT, then passing the image into shape generation.
- independent text generation of front/right/back/left can drift in identity, proportion, and hidden geometry; MVP therefore generates one canonical front reference and requires review before 3D.
- text-reference and shape generation remain separate processes so an 8 GB GPU never needs both large models resident at once.

## Exact model baseline

```text
text reference:
Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled

3D shape:
tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
```

Do not use the unverified `HunyuanDiT v1.2 Distilled Lite` label that appeared in temporary repository notes. The official Hunyuan3D-2 text path currently references the v1.1 Diffusers Distilled checkpoint above.

## Text-reference contract

Text mode produces a **generated hypothesis**, not authoritative geometry.

The runtime wrapper:

1. preserves the user's semantic prompt;
2. deterministically adds front-view / isolated-object reference cues;
3. uses HunyuanDiT with model CPU offload by default for the 8 GB development GPU;
4. writes `reference_front.png` + `text_reference.json`;
5. stops for review.

Do not automatically call 3D generation from the text-reference runner.

## Shape input contract

Accepted named views:

```text
front
right
back
left
```

At least one view is required. Four consistent views are preferred when available.

The first runtime baseline is intentionally conservative:

```text
model: tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
background removal: ON
texture generation: OFF
```

`num_chunks=8000` follows the upstream low-VRAM UI behavior. This is an initial RTX 3070 8 GB proof baseline, not a permanent quality optimum.

## Variant policy

Hunyuan3D-2mv also publishes Fast and Turbo subfolders, and Tencent's current UI recommends Turbo for most cases. They are **not routed automatically in MVP**.

First prove the standard baseline. Reopen Fast/Turbo only with measured evidence from the same references and downstream Minecraft discretization.

## Output contract

Text stage:

```text
reference_front.png
text_reference.json
```

Shape stage:

```text
model.glb
generation.json
```

Manifests record model IDs, input paths/hashes, seed, parameters, and output state for reproducibility.

## Runtime boundary

Repository/CI checks can prove argument routing, model IDs, defaults, approval boundary, and manifest planning. They cannot prove:

- CUDA compatibility;
- actual peak VRAM;
- HunyuanDiT output quality;
- Hunyuan3D geometry quality;
- GLB compatibility with Blender.

Those require `local` execution.

## References

- https://huggingface.co/tencent/Hunyuan3D-2mv
- https://huggingface.co/spaces/tencent/Hunyuan3D-2mv/blob/main/gradio_app.py
- https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/gradio_app.py
- https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/hy3dgen/text2image.py
- https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
