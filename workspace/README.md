# Workspace

`workspace/` is a local/external project-package mount convention. The public LazyBuilder repository owns the **system**, not live project/reference/generated data.

```text
workspace/
├── active/
│   └── <project>/
└── archive/
    └── <project>/
```

Project subdirectories are ignored by Git.

A typical local project may contain:

```text
references/
generated/model.glb
blender/project.blend
output/build.schem
```

This is a working convention only. Do not commit private references, client files, generated production meshes, `.blend` files, schematics, Minecraft worlds, or credentials unless an explicit public-visibility decision authorizes it.
