# Decision Log

Dokumen ini mencatat keputusan yang sudah dikunci agar development tidak melebar tanpa hasil.

## D-001 — Branch workflow

**Keputusan**

- `main` = stable/default.
- `Local` = active development.
- Semua eksperimen, dokumentasi, dan coding dilakukan di `Local` terlebih dahulu.
- Hanya pekerjaan yang sudah layak yang dipromosikan ke `main`.

## D-002 — Satu model 3D saja

**Keputusan**

Pakai **Hunyuan3D-2mv** sebagai satu-satunya generator 3D pada tahap ini.

**Tidak dipakai**

- Tripo
- TRELLIS
- Pixal3D
- provider router

**Alasan**

Mengurangi setup, maintenance, branching behavior, dan debugging. Fokus kualitas diarahkan ke Minecraft conversion, bukan perbandingan model 3D terus-menerus.

## D-003 — Multi-view sebagai input utama

Input ideal:

```text
front
right
back
left
```

Tujuan utamanya meningkatkan konsistensi bentuk dari beberapa sisi dan mengurangi tebakan dari single image.

## D-004 — Blender sebagai workspace, bukan final engine

Blender dipakai untuk melihat dan membersihkan hasil 3D sebelum conversion.

Kita tidak membangun workflow Blender yang kompleks jika tidak berdampak langsung ke output Minecraft.

## D-005 — Minecraftize adalah custom core utama

Custom development difokuskan pada:

```text
Blender mesh
→ Minecraft-native block placement
```

Tahap awal:

```text
Full Block
→ Stair
→ Slab
```

Jenis block lain ditambahkan hanya setelah fondasi terbukti.

## D-006 — Rule-based lebih dulu

Tidak langsung memakai ML/inverse solver kompleks.

Mulai dari aturan geometry yang sederhana dan terukur. Optimizer baru dibuat jika hasil test menunjukkan rule-based tidak cukup.

## D-007 — Reuse schematic writer

Tidak membuat serializer Sponge/NBT sendiri.

Gunakan `mcschematic` selama memenuhi kebutuhan BlockState dan kompatibilitas output.

## D-008 — Axiom adalah final editor

LazyBuilder bertugas menghasilkan `.schem` yang valid dan berkualitas.

Axiom menangani:

- import;
- placement;
- final manual polish.

Tidak ada direct Axiom automation di MVP.

## D-009 — MCP ditunda

MCP hanya automation/control layer. Ia tidak meningkatkan kualitas geometry atau schematic.

Karena itu MCP baru dipertimbangkan setelah workflow manual end-to-end sudah terbukti.

## D-010 — Tidak overdevelop

Sebelum menambah dependency atau subsystem baru, harus ada salah satu alasan berikut:

1. bug nyata yang tidak bisa diselesaikan stack sekarang;
2. kualitas output terbukti terhambat;
3. performance menjadi bottleneck terukur;
4. fitur tersebut dibutuhkan untuk milestone berikutnya.

Jika tidak ada alasan tersebut, jangan ditambahkan.
