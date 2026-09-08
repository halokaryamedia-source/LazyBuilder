# LazyBuilder

LazyBuilder adalah project R&D untuk mengubah referensi non-Minecraft menjadi struktur Minecraft Java yang bisa diekspor sebagai `.schem` dan dimuat di Axiom.

## Target utama

```text
Multi-view images
→ Hunyuan3D-2mv
→ GLB
→ Blender
→ Minecraftize
→ .schem
→ Axiom
→ Minecraft Java
```

Fokus utama project bukan membuat AI 3D baru. Kita memakai model yang sudah ada untuk membuat draft 3D, lalu fokus development pada konversi mesh Blender menjadi bentuk Minecraft yang lebih native dan rapi.

## Stack yang dikunci

- **3D generation:** Hunyuan3D-2mv saja.
- **3D workspace:** Blender 5.2.x LTS.
- **Minecraft conversion:** custom Blender addon `Minecraftize`.
- **Schematic writer:** `mcschematic`.
- **Final editor / placement:** Axiom.
- **Target:** Minecraft Java Edition.

## Prinsip development

- Satu model 3D saja: **Hunyuan3D-2mv**.
- Tidak memakai MCP pada MVP.
- Tidak memakai Tripo, TRELLIS, Pixal3D, atau router multi-model.
- Tidak membuat format schematic sendiri.
- Tidak membuat renderer, AI critic, training dataset, atau architecture engine sebelum dibutuhkan.
- Pakai tool existing sebanyak mungkin; custom development hanya pada bagian yang belum tersedia dengan kualitas yang kita butuhkan.

## Branch policy

- `main` — branch default/stabil. Hanya menerima pekerjaan yang sudah layak dipromosikan.
- `Local` — branch kerja aktif untuk seluruh development, eksperimen, dokumentasi, dan testing.

> Semua pekerjaan saat ini dilakukan di `Local`.

## MVP

MVP dianggap berhasil ketika pipeline berikut benar-benar berjalan end-to-end:

1. Multi-view reference masuk ke Hunyuan3D-2mv.
2. Hasil `.glb` dapat diimpor ke Blender.
3. `Minecraftize` dapat menghasilkan preview full-block.
4. Hasil dapat diekspor menjadi `.schem`.
5. `.schem` dapat dimuat ke Axiom dan ditempatkan di Minecraft Java.
6. Tahap berikutnya menambahkan **stairs** dan **slabs** agar bentuk tidak sekadar voxel cube.

Dokumentasi detail tersedia di [`docs/`](docs/).
