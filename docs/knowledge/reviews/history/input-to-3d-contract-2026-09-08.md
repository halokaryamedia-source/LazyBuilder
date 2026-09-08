# Input-to-3D Contract Review — 2026-09-08

Status: research + static implementation complete; local GPU proof required.

## Scope

Establish and implement the smallest correct LazyBuilder path for:

```text
text → 3D
image / multiview → 3D
```

without adding another 3D provider or hiding uncertainty behind automatic routing.

## Research conclusions

### Hunyuan3D-2mv

Official Hunyuan3D-2mv materials establish that the model is a multiview-controlled **image-to-shape** model. The runtime accepts one to four named views such as front/right/back/left.

It is not a direct text-to-3D endpoint.

Exact MVP shape checkpoint:

```text
tencent/Hunyuan3D-2mv
subfolder: hunyuan3d-dit-v2-mv
```

Fast and Turbo subfolders also exist upstream, but they are not introduced as automatic routing before a controlled standard-model proof.

### Official text path

Tencent's Hunyuan3D-2 application handles text input by first generating an image with HunyuanDiT and then feeding the generated image into shape generation.

The exact checkpoint referenced by the official Hunyuan3D-2 code is:

```text
Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
```

A temporary repository note had named an unverified `HunyuanDiT v1.2 Diffusers Distilled Lite` model. That label is retired from the active contract.

### Text-reference defaults

The upstream HunyuanDiT helper uses a Diffusers text-to-image pipeline with float16/PAG and a 1024×1024, 25-step, PAG-scale-1.3 style baseline.

LazyBuilder preserves those key first-proof defaults but adds:

- deterministic front-reference framing cues;
- one generated canonical front view only;
- model CPU offload by default for the 8 GB development GPU;
- an explicit review gate before 3D.

### 8 GB strategy

Text reference and shape generation are separate processes. LazyBuilder does not require HunyuanDiT and Hunyuan3D to reside in VRAM simultaneously.

The initial shape profile uses:

```text
octree_resolution: 256
num_chunks: 8000
```

The 8000 chunk value follows the upstream low-VRAM UI behavior. This is a proof baseline, not a final performance/quality claim.

## Implemented static contract

```text
runtime_contract.py
→ exact IDs/defaults/input validation/manifests

generate_text_reference.py
→ text → reference_front.png
→ hard USER_REVIEW_REQUIRED_BEFORE_3D boundary

generate_shape.py
→ 1–4 named views → shape-only model.glb

test_generation_contract.py
→ dependency-light static invariants

generation-contract-verify.yml
→ CI unit/dry-run checks without model downloads/GPU claims
```

Heavy model imports occur only during real execution so static validation remains cheap.

## Deliberately not implemented

```text
no second 3D provider
no 3D provider router
no automatic Fast/Turbo routing
no automatic text → four independent views
no texture generation
no Blender-Python embedding
no API/MCP orchestration
no Minecraftize runtime in this milestone
```

## Runtime evidence still required

On the user's actual development machine:

```text
HunyuanDiT startup
reference generation
peak VRAM / runtime
user approval
Hunyuan3D-2mv startup
single-view GLB
multiview GLB
peak VRAM / runtime
Blender 5.2.x LTS import
geometry quality relevant to Minecraft conversion
```

Static implementation does not imply any of these runtime claims.

## Public references

- https://huggingface.co/tencent/Hunyuan3D-2mv
- https://huggingface.co/spaces/tencent/Hunyuan3D-2mv/blob/main/gradio_app.py
- https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/gradio_app.py
- https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/hy3dgen/text2image.py
- https://huggingface.co/Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
