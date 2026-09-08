# Tooling

Dokumen ini mengunci tool yang digunakan pada tahap awal LazyBuilder.

## Tool aktif

| Tool | Fungsi | Status di project |
|---|---|---|
| Hunyuan3D-2mv | Multi-view image → 3D shape | Dipakai sebagai satu-satunya 3D generator |
| Blender 5.2.x LTS | Workspace 3D | Dipakai |
| Minecraftize | Blender mesh → Minecraft blocks | Kita develop |
| mcschematic | Menulis `.schem` | Dipakai sebagai existing dependency |
| Axiom | Import/edit/place schematic | Dipakai sebagai final editor |

## Hunyuan3D-2mv

Keputusan:

- hanya memakai seri `Hunyuan3D-2mv`;
- tidak memakai router multi-model;
- shape generation adalah prioritas;
- texture generation bukan kebutuhan utama karena output akhir menggunakan material Minecraft;
- environment Hunyuan dipisahkan dari Python milik Blender;
- hasil generation masuk ke Blender sebagai `.glb`.

Recommended mode untuk development pada RTX 3070 8 GB:

```text
Hunyuan3D-DiT-v2-mv
low_vram_mode = enabled bila diperlukan
texture generation = off
```

## Blender

Digunakan untuk:

- import GLB;
- scale/orientation;
- cleanup ringan;
- geometry inspection;
- Minecraft preview;
- menjalankan addon Minecraftize.

Blender bukan schematic writer dan bukan AI model host utama.

## Minecraftize

Custom addon yang kita miliki sendiri.

Scope awal UI:

```text
Minecraftize
---------------------------
Target Width : [120]

Allowed Shapes
[x] Full Block
[x] Stair
[x] Slab

Material Base
[Stone Bricks]

[ Generate Preview ]
[ Export .schem ]
```

Implementasi jangan dibuat lebih luas sebelum kebutuhan teruji.

## mcschematic

Dependency untuk menghasilkan file schematic.

Minecraftize cukup memberikan:

```text
(x, y, z)
+
Minecraft BlockState string
```

Contoh:

```text
minecraft:stone_bricks
minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight]
minecraft:stone_slab[type=top]
```

Writer menangani file schematic.

## Axiom

Tidak dikembangkan atau dimodifikasi.

Workflow:

```text
LazyBuilder output.schem
→ Axiom Import Schematic
→ Clipboard
→ placement / polish di world
```

## Tool yang sengaja tidak digunakan sekarang

- MCP
- Tripo
- TRELLIS / TRELLIS.2
- Pixal3D
- ObjToSchematic sebagai core
- Blockpedia
- custom ML model
- custom schematic format
- custom Minecraft renderer

Tool tersebut dapat dievaluasi ulang hanya jika ada masalah nyata yang tidak dapat diselesaikan stack saat ini.

## Reference projects

Project existing seperti Blender-to-schematic exporters atau voxel converters boleh dipakai sebagai referensi algoritma/proof-of-concept, tetapi tidak otomatis menjadi dependency utama.

Prinsip umum:

> Reuse yang sudah matang. Custom hanya pada bagian yang langsung meningkatkan kualitas output Minecraft.
