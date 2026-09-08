# Generation Runtime Environment

This file owns the reproducible **local generation environment contract**. It prepares runtime; it does not prove runtime success.

## Scope

Generation uses two separate processes:

```text
TEXT reference process
→ HunyuanDiT
→ exit / release memory

SHAPE process
→ Hunyuan3D-2mv
→ exit / release memory
```

Do not keep both models resident on the RTX 3070 8 GB development target.

## Pinned upstream authority

Hunyuan3D source code:

```text
repository: Tencent-Hunyuan/Hunyuan3D-2
commit: f8db63096c8282cb27354314d896feba5ba6ff8a
```

Hunyuan3D-2mv Standard shape weights:

```text
repository: tencent/Hunyuan3D-2mv
revision: 08766051fa711c6ef5caf86b97e50304fdfcf0ef
subfolder: hunyuan3d-dit-v2-mv
```

HunyuanDiT text-reference weights:

```text
repository: Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
revision: 527cf2ecce7c04021975938f8b0e44e35d2b1ed9
```

`runtime_contract.py` owns these pins. Runners must record them in manifests.

The Hunyuan3D runner explicitly downloads the pinned model snapshot before calling the upstream pipeline because the audited upstream `smart_load_model()` path does not expose a model revision argument itself.

## Installation strategy

Use an isolated environment dedicated to LazyBuilder generation.

```text
1. install a PyTorch/CUDA build compatible with the actual NVIDIA driver;
2. clone Tencent-Hunyuan/Hunyuan3D-2 at the exact source commit above;
3. install the pinned source repository's requirements;
4. ensure the pinned source checkout provides `hy3dgen` to the environment;
5. install/verify Diffusers + Transformers + Accelerate required by HunyuanDiT;
6. keep Hugging Face cache available for the pinned model snapshots;
7. run preflight capture before any first generation session.
```

Do **not** duplicate the upstream Hunyuan dependency list into root `requirements.txt`. Root `requirements.txt` intentionally remains the small deterministic schematic-writer environment (`mcschematic==11.4.4`).

Do not build texture-only custom rasterizers for the first LazyBuilder proof unless the shape-only path unexpectedly proves they are required. Texture remains OFF.

## Why Python / Torch / CUDA are not guessed here

The exact compatible Python, PyTorch, CUDA runtime and NVIDIA driver combination must be recorded from the actual target machine before runtime. Static CI uses Python 3.11 for repository contracts only and is not evidence that Hunyuan GPU runtime is compatible with that exact local stack.

The first preflight must capture at minimum:

```text
OS / architecture
Python version
PyTorch version
CUDA runtime / driver
GPU name + VRAM
Diffusers / Transformers / Accelerate / huggingface_hub versions
Hunyuan3D source commit
Hunyuan3D model revision
HunyuanDiT model revision
Blender version
Minecraft/Axiom/Paper environment facts
```

`validator/collect_environment.py` owns the machine-readable preflight capture surface.

## Cache and model identity

Never rely on an unqualified mutable `main` model snapshot during acceptance evidence.

```text
model ID + revision
→ resolved local cache snapshot
→ manifest
```

If a pinned snapshot is intentionally changed, treat that as a generation-contract change and invalidate affected downstream evidence.

## Runtime boundary

Preparing/installing this environment later is `local` execution work. Repository/static verification only proves that the pins, commands, and manifests are internally consistent.

No Hunyuan runtime has been executed merely because this file exists.

The collector auto-records these immutable repository-owned identities; the user does not need to type them manually:

```text
hunyuan3d_source_commit
hunyuan3d_model_revision
hunyuandit_model_revision
```

Machine/environment facts remain explicit records because they must come from the actual runtime host rather than repository assumptions.
