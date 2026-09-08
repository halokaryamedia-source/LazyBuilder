# Hunyuan3D-2mv Generation

## Role

Hunyuan3D-2mv is the single active provider for multi-view → shape generation.

## Runtime setup boundary

- keep Hunyuan Python/CUDA environment separate from Blender Python;
- use the official Hunyuan3D-2mv model/implementation when setting up runtime;
- prioritize **shape-only** output;
- texture generation is normally off for Minecraft production;
- use low-VRAM mode when necessary for RTX 3070 8 GB;
- export/save GLB for Blender.

## Production flow

```text
settled multi-view references
→ Hunyuan3D-2mv
→ inspect generation success
→ model.glb
→ Blender target preparation
```

## Failure routing

If shape is poor:

1. verify reference consistency;
2. verify correct multi-view model/runtime/config;
3. determine whether the defect materially survives Minecraft discretization;
4. use bounded Blender cleanup when cheaper than regeneration;
5. only reopen provider architecture through a durable decision if repeated evidence shows current provider is fundamentally inadequate.

## Proof

Only actual local generation proves this flow. Repository/static checks cannot mark Hunyuan runtime PASS.
