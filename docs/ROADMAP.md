# Roadmap

Roadmap dibuat berdasarkan output nyata. Setiap milestone harus menghasilkan sesuatu yang bisa diuji sebelum lanjut.

## M0 — Repository & project setup

Status target:

- [x] `main` sebagai default/stable branch
- [x] `Local` sebagai development branch
- [x] dokumentasi arsitektur awal
- [x] tool stack dikunci

## M1 — Prove `.schem → Axiom`

Tujuan:

Membuktikan output programmatic sederhana bisa dimuat ke Axiom.

Task:

- [ ] setup `mcschematic`
- [ ] generate schematic cube sederhana
- [ ] import `.schem` di Axiom
- [ ] place ke Minecraft Java world
- [ ] dokumentasikan Minecraft version yang diuji

**Exit criteria**

Axiom dapat membuka dan menempatkan `.schem` tanpa error.

## M2 — Hunyuan3D-2mv → Blender

Tujuan:

Membuktikan multi-view input menghasilkan GLB yang dapat digunakan sebagai target geometry.

Task:

- [ ] setup Hunyuan3D-2mv environment terpisah
- [ ] test RTX 3070 8 GB
- [ ] gunakan shape-only
- [ ] test low VRAM mode jika diperlukan
- [ ] generate `.glb` dari multi-view reference
- [ ] import ke Blender

**Exit criteria**

GLB hasil Hunyuan dapat dibuka dan diperiksa normal di Blender.

## M3 — Minecraftize V0: Full Blocks

Tujuan:

Membuktikan mesh Blender dapat dikonversi menjadi struktur Minecraft sederhana.

Task:

- [ ] buat Blender addon skeleton
- [ ] target width / scale setting
- [ ] sample mesh ke Minecraft grid
- [ ] full-block occupancy
- [ ] preview di Blender
- [ ] export menggunakan `mcschematic`

**Exit criteria**

```text
Hunyuan GLB
→ Blender
→ Minecraftize
→ full-block .schem
→ Axiom
```

berjalan end-to-end.

## M4 — Minecraftize V1: Stairs

Tujuan:

Menggunakan stair pada geometry yang memang lebih tepat daripada cube.

Test wajib:

- [ ] 45° roof
- [ ] empat arah facing
- [ ] top/bottom stair
- [ ] valid `.schem` output

**Exit criteria**

Roof 45° secara konsisten lebih halus dibanding full-block baseline.

## M5 — Minecraftize V1: Slabs

Test wajib:

- [ ] top slab
- [ ] bottom slab
- [ ] shallow contour / half-height
- [ ] mixed full + stair + slab

**Exit criteria**

Solver sederhana dapat memilih full/stair/slab tanpa manual placement untuk primitive test.

## M6 — First real building

Input:

```text
front
right
back
left
```

Target:

- [ ] generate bangunan dengan Hunyuan3D-2mv
- [ ] cleanup ringan di Blender
- [ ] Minecraftize full/stair/slab
- [ ] export `.schem`
- [ ] import di Axiom
- [ ] evaluasi silhouette dan proportion

**Exit criteria**

Bangunan dapat dikenali dengan baik dan tidak terlihat sekadar voxel cube kasar.

## M7 — Tambahan block hanya jika diperlukan

Urutan kandidat:

```text
wall
fence
glass pane
trapdoor
iron bars
door
decorative blocks
```

Tidak ada kewajiban mengimplementasikan semua. Setiap jenis block harus memiliki use case nyata dari test building.

## Setelah MVP

Baru evaluasi jika diperlukan:

- automatic material palette;
- improved geometry scoring;
- faster solver;
- component-aware rules;
- MCP automation;
- AI-assisted cleanup;
- additional export formats.

## Prinsip milestone

> Jangan mulai milestone berikut sebelum exit criteria milestone sebelumnya terbukti.
