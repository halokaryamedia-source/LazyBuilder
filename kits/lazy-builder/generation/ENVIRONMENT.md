# Generation Runtime Environment

This file owns the reproducible **local generation environment contract**. It prepares runtime; it does not prove runtime success.

## Process boundary

Generation uses two separate processes:

```text
TEXT reference process
→ pinned HunyuanDiT
→ exit / release memory

SHAPE process
→ pinned Hunyuan3D-2mv
→ exit / release memory
```

Do not keep both models resident on the RTX 3070 8 GB development target.

## Pinned upstream authority

```text
Hunyuan3D source repository
Tencent-Hunyuan/Hunyuan3D-2
commit f8db63096c8282cb27354314d896feba5ba6ff8a

Hunyuan3D-2mv model
tencent/Hunyuan3D-2mv
revision 08766051fa711c6ef5caf86b97e50304fdfcf0ef
subfolder hunyuan3d-dit-v2-mv

HunyuanDiT text model
Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
revision 527cf2ecce7c04021975938f8b0e44e35d2b1ed9
pipeline HunyuanDiTPipeline
```

`runtime_contract.py` is the machine-readable owner for these pins.

## Source identity must be actual, not declarative

It is not enough for a manifest to *say* that the pinned Hunyuan3D commit was used.

Before shape generation, LazyBuilder resolves the imported `hy3dgen` package back to its Git checkout and requires:

```text
git HEAD == pinned source commit
working tree clean
```

A different commit or locally modified checkout is a hard failure. The actual resolved checkout path/commit is recorded in the generation manifest.

This prevents a locally edited/editable-installed Hunyuan checkout from silently producing evidence under the pinned commit label.

## Text-reference baseline

The distilled text-reference model uses its native Diffusers pipeline rather than an unproved custom PAG layer selection:

```text
HunyuanDiTPipeline
steps: 25
guidance_scale: 7.5
size: 1024 × 1024
seed: 0
offload: model CPU offload
```

Do not add PAG/custom layer routing unless same-prompt measured evidence later proves it improves LazyBuilder's downstream geometry reference quality.

## Shape extraction baseline

The Hunyuan3D call records and passes the extraction-critical values explicitly so upstream default changes cannot silently alter evidence:

```text
steps: 30
guidance_scale: 7.5
octree_resolution: 256
num_chunks: 8000
seed: 12345
variant: fp16
use_safetensors: true
box_v: 1.01
mc_level: 0.0
mc_algo: null
output_type: trimesh
background removal: ON
texture: OFF
```

The first profile is intentionally bounded for the 8 GB development GPU. It is not claimed as the final quality/performance optimum.

## Installation strategy

Use an isolated environment dedicated to LazyBuilder generation.

```text
1. install a PyTorch/CUDA build compatible with the actual NVIDIA driver;
2. clone Tencent-Hunyuan/Hunyuan3D-2 at the exact pinned commit;
3. install the pinned checkout's requirements;
4. install the checkout so `hy3dgen` resolves back to that Git tree;
5. install/verify Diffusers + Transformers + Accelerate + huggingface_hub;
6. keep Hugging Face cache available for pinned model snapshots;
7. ensure Blender is available on PATH for the acceptance host;
8. run preflight capture before generation.
```

Root `requirements.txt` remains intentionally limited to the deterministic schematic-writer environment (`mcschematic==11.4.4`). Do not duplicate Hunyuan's large upstream dependency set there.

## Preflight is fail-closed

`validator/collect_environment.py` records installed package/executable facts **without launching inference**. `artifact_validation.py` allows preflight PASS only when:

```text
required runtime packages are installed
required executable paths are available
installed generation API signatures match LazyBuilder wrapper expectations
actual hy3dgen checkout is the pinned clean commit
required machine/Axiom/Paper facts are declared
pinned model/source identities match
```

Exact Python/PyTorch/CUDA/driver versions are captured from the actual target host rather than guessed in repository documentation.

If the environment is changed after preflight, invalidate/re-run preflight before continuing. Do not reuse old environment evidence after package, driver, Blender, Hunyuan source, or Axiom/Paper changes.

## Cache/model identity

Never rely on mutable model `main` during acceptance evidence.

```text
model ID + revision
→ resolved local cache snapshot
→ manifest
```

The Hunyuan3D runner explicitly resolves the pinned Hugging Face snapshot before calling the upstream pipeline because the audited upstream model-loading path does not expose a revision argument itself.

## Runtime boundary

Environment setup and future inference are `local` execution work. Static CI proves wrapper contracts and source pins, not CUDA startup, VRAM sufficiency, generated mesh quality, or runtime performance.
