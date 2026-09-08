# Reference Intake Policy

Flow 2 establishes the source evidence LazyBuilder is allowed to interpret.

## Preferred input

For buildings or objects where side fidelity matters:

```text
front
right
back
left
```

Fewer views are allowed when that is the actual source, but missing sides remain inference rather than verified geometry.

## Intake requirements

- all views must describe the same design/version of the object;
- crop/scale/perspective should be reasonably consistent when possible;
- preserve any known real dimensions or intended Minecraft target size;
- retain the original reference as authority; do not replace it with an AI-generated view and forget provenance;
- contradictory references must be surfaced rather than averaged silently when the difference is material.

## Approval economy

Do not create a ceremonial approval step when current references and explicit user instruction already settle the intended build.

Ask only when a material ambiguity changes geometry, scale, required side interpretation, or the expected output.

## Output

Flow 2 hands Flow 3 a settled reference set plus only the material build constraints needed for generation/conversion.

Detailed procedure: `kits/lazy-builder/intake/REFERENCE-INTAKE.md`.
