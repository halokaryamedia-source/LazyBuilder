# Architecture

## 1. Product flow

```text
REFERENCE IMAGES
(front / left / right / back)
        ↓
Hunyuan3D-2mv
        ↓
model.glb
        ↓
Blender
        ↓
minor cleanup
        ↓
Minecraftize
        ↓
Minecraft block preview
        ↓
export .schem
        ↓
Axiom
        ↓
Minecraft Java world
```

## 2. Role setiap tahap

### Hunyuan3D-2mv
Membuat **draft 3D** dari beberapa reference view. Output utamanya adalah `.glb`.

Hasil Hunyuan tidak dianggap sebagai hasil Minecraft final. Ia hanya menjadi target geometry yang akan dibaca Blender dan Minecraftize.

### Blender
Workspace untuk:

- import `.glb`;
- memperbaiki orientasi dan scale;
- membuang noise/floating geometry yang jelas salah;
- melakukan cleanup ringan;
- menampilkan preview hasil Minecraftize.

Kita tidak melakukan retopology/detailing panjang jika tidak berdampak pada hasil Minecraft.

### Minecraftize
Satu-satunya custom core utama project.

Tugasnya:

```text
Blender mesh
→ sample ke grid Minecraft
→ tentukan block placement
→ pilih bentuk block yang didukung
→ preview
→ kirim BlockState ke exporter
```

Urutan dukungan shape:

1. Full block
2. Stair
3. Slab
4. Wall / fence / glass pane
5. Trapdoor / iron bars / door / decorative blocks bila memang dibutuhkan

### mcschematic
Digunakan hanya sebagai writer/export layer untuk menghasilkan `.schem`. Kita tidak membuat implementasi Sponge/NBT sendiri jika library existing sudah mencukupi.

### Axiom
Final editor dan placement tool. LazyBuilder hanya perlu menghasilkan schematic yang valid dan bagus; placement dan polish manual dapat dilakukan di Axiom.

## 3. Target input

Input utama adalah beberapa view dari objek/bangunan yang sama.

Recommended set:

```text
front.png
right.png
back.png
left.png
```

Rule:

- desain objek harus sama di semua view;
- proporsi/crop sedapat mungkin konsisten;
- jangan mencampur variasi desain yang berbeda;
- reference yang konsisten lebih penting daripada jumlah image yang banyak.

## 4. Target output

Output utama:

```text
<project-name>.schem
```

Target pertama adalah vanilla Minecraft Java block states.

## 5. Minecraftize V1

### Full block pass
Menentukan occupancy utama dari mesh.

### Stair pass
Digunakan untuk area slope/contour yang lebih cocok direpresentasikan sebagai stairs daripada full cube.

State minimum:

```text
facing=north|south|east|west
half=top|bottom
shape=straight|inner_left|inner_right|outer_left|outer_right
```

### Slab pass
Digunakan untuk half-height atau contour yang lebih halus.

State minimum:

```text
type=top|bottom|double
```

## 6. Rule sederhana sebelum optimizer kompleks

Kita mulai rule-based, bukan ML.

Contoh awal:

```text
solid/interior cell  → full block
slope mendekati 45°  → stair
half-height surface  → slab
```

Jika rule sederhana sudah terbukti kurang, baru ditambah scoring/optimizer.

## 7. Preview

Minecraftize harus bisa membuat preview di Blender sebelum export.

Minimal mode:

```text
Original Mesh
Minecraft Preview
Original + Minecraft Overlay
```

Tujuannya agar masalah terlihat sebelum masuk Axiom.

## 8. Bukan bagian MVP

Belum dibuat:

- MCP automation;
- multi-model routing;
- custom renderer;
- AI critic;
- model training;
- interior generation;
- semantic architecture engine;
- modded block support;
- direct world injection;
- direct Axiom automation.

Tambahkan hanya jika pipeline dasar sudah terbukti dan ada kebutuhan nyata.
