# Current Validation Status

Updated: 2026-09-09

## Current system state

```text
status: PRE_RUNTIME_SYSTEM_READY_RUNTIME_NOT_STARTED
working branch: develop
verified integration baseline: Local
stable branch: main
product maturity: pre-MVP
runtime acceptance: intentionally deferred by user
```

LazyBuilder has now undergone a second source-focused audit specifically aimed at finding conditions that could **look reproducible/correct in CI while being materially wrong at runtime**.

No Hunyuan inference, Blender conversion, Axiom/Paper placement, or Minecraft runtime proof was performed during this audit.

## Source-audit result

The audit found and corrected several false-confidence paths.

### 1. Hunyuan source identity

Previously the shape manifest recorded the *expected* upstream source commit but did not prove that the imported `hy3dgen` package actually came from that commit.

Now:

```text
import hy3dgen
→ resolve package file to Git checkout
→ git HEAD must equal pinned commit
→ working tree must be clean
→ actual checkout path/commit recorded
→ otherwise generation fails before inference
```

Pinned source:

```text
Tencent-Hunyuan/Hunyuan3D-2
f8db63096c8282cb27354314d896feba5ba6ff8a
```

### 2. Text-reference wrapper accuracy

The previous custom PAG layer selection was removed because it was not sufficiently grounded for the pinned distilled model.

Current text baseline uses:

```text
Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled
revision 527cf2ecce7c04021975938f8b0e44e35d2b1ed9
native HunyuanDiTPipeline
25 inference steps
guidance_scale 7.5
```

This keeps the baseline closer to the model's native documented usage and avoids an unproved optimization path.

### 3. Shape extraction defaults

Extraction-critical values are now explicit instead of inheriting mutable upstream defaults:

```text
variant fp16
use_safetensors true
box_v 1.01
mc_level 0.0
mc_algo null
output_type trimesh
steps 30
guidance_scale 7.5
octree_resolution 256
num_chunks 8000
seed 12345
```

Zero/empty mesh output is rejected.

### 4. Preflight is fail-closed

Preflight PASS now requires:

```text
required runtime packages installed
Git + Blender executable paths available
installed generation API signatures compatible with LazyBuilder calls
actual Hunyuan checkout pinned + clean
required machine/runtime/Axiom/Paper facts declared
source/model pins exact
```

Preflight remains non-runtime: it imports/inspects interfaces but does not execute model inference or launch Blender/Axiom/Minecraft.

### 5. Intentional input changes

Unexpected T1/I1/I2 changes remain `INPUT_DRIFT`.

A new explicit helper now supports legitimate source updates:

```text
refresh_case_input.py
→ refresh named authoritative input SHA-256
→ invalidate first affected owner + true dependents
→ preserve independent evidence
```

This fixes the previous situation where invalidating a stage alone could leave the old case snapshot and cause the same drift failure again.

### 6. Human gates are enforced

The controller now refuses direct `RUNNING → PASS` for:

```text
text_reference
minecraft_preview
```

Both require:

```text
RUNNING → APPROVAL_REQUIRED → PASS
```

### 7. Cross-artifact consistency

Validators now reject:

```text
non-finite / zero / inverted Blender bounds
Minecraftize report count/bounds disagreeing with blocks.json
preview manifest metadata disagreeing with canonical blocks.json
schematic source metadata disagreeing with canonical blocks.json
```

### 8. Schematic evidence scale

The exporter still reloads and compares **every source block state** after save.

The manifest no longer duplicates every block as diagnostic evidence. It records:

```text
round_trip_verified_block_count = full source block count
≤64 deterministic diagnostic samples
```

Thus verification remains exhaustive while evidence size stays bounded.

### 9. Runtime evidence lineage

`write_runtime_evidence.py` now binds future Axiom/Paper/Minecraft observations to:

```text
exact build.schem SHA-256
exact preflight environment.json SHA-256
import / clipboard / placement / minecraft_world / visual_state
```

The session controller rejects Axiom PASS if runtime evidence hashes do not equal the session's authoritative schematic/preflight PASS digests.

## Latest deliveries

```text
5c6e2a6ddc0ab3384a22afee009b64674b3a05d9
fix(readiness): add explicit case input refresh

e2430948b15803f1bd79e983957bafd54df9977a
fix(readiness): make source evidence fail closed

2b02ef6c9ee39b468ae00a3e9ac5535f4d2c8cd0
docs(readiness): make fail-closed policy explicit
```

## Verification evidence

On core code commit `e243094`:

```text
Generation Contract Verify  → PASS
Repository Verify           → PASS
M1 Schematic Smoke          → PASS
```

The initial Pre-Runtime Verify failed only on a literal documentation marker (`fail-closed`), not a source/test failure. The marker was made explicit without weakening the verifier.

On current synchronized tree `2b02ef6`:

```text
Repository Verify            → PASS
Pre-Runtime Verify            → PASS (run 34262847797)
M1 Schematic Smoke           → PASS
```

Pre-Runtime Verify includes generation/session/artifact unit tests, static session routing, Minecraftize pure tests, entrypoint compilation without launching applications, canonical preview generation, and schematic export/reload verification.

## Canonical product chain

```text
T1 TEXT
→ pinned native HunyuanDiTPipeline
→ reference_front.png
→ approval
→ pinned/verified Hunyuan3D-2mv

I1 SINGLE IMAGE → pinned/verified Hunyuan3D-2mv
I2 MULTIVIEW    → pinned/verified Hunyuan3D-2mv

→ representative GLB
→ Blender LazyBuilderTarget + target.json
→ Minecraftize V0 full blocks
→ canonical blocks.json
→ approved canonical preview.svg
→ mcschematic==11.4.4 / Sponge V2 / DataVersion 4189
→ Axiom 5.3.0
→ AxiomPaper 5.0.1+1.21.4 / Paper 1.21.4
→ Minecraft Java 1.21.4
```

## Axiom static baseline

Existing audited baseline remains unchanged:

```text
Axiom 5.3.0 client / API family 9
AxiomPaper 5.0.1+1.21.4 / API family 9
Sponge V2 / DataVersion 4189
```

AxiomPaper 4.0.4 remains outside the baseline. AxiomPaper 5.0.4+1.21.4 remains only a conditional candidate after measured evidence.

## Runtime proof status

```text
HunyuanDiT GPU generation                → LOCAL RUNTIME PROOF REQUIRED
Hunyuan3D-2mv GPU generation             → LOCAL RUNTIME PROOF REQUIRED
GLB quality / Blender import             → LOCAL RUNTIME PROOF REQUIRED
Blender target preparation               → LOCAL RUNTIME PROOF REQUIRED
Minecraftize primitive execution         → LOCAL RUNTIME PROOF REQUIRED
Minecraftize representative conversion  → LOCAL RUNTIME PROOF REQUIRED
Axiom import / Clipboard                 → LOCAL RUNTIME PROOF REQUIRED
AxiomPaper / Paper placement             → LOCAL RUNTIME PROOF REQUIRED
Minecraft final visual fidelity          → LOCAL RUNTIME PROOF REQUIRED
```

## Current conclusion

At the source/repository level, no known preparation blocker remains. The repository should now be **frozen rather than expanded** until Runtime Acceptance produces real evidence.

This is not a claim that runtime will necessarily PASS; it is a claim that the source has been hardened to avoid several known ways of producing misleading PASS evidence before runtime.

## Evidence owners

```text
generation environment   → kits/lazy-builder/generation/ENVIRONMENT.md
session/readiness         → kits/lazy-builder/validator/TEST-READINESS.md
artifact contracts       → kits/lazy-builder/validator/ARTIFACT-CONTRACTS.md
runtime handoff           → kits/lazy-builder/validator/VALIDATION.md
Minecraftize             → kits/lazy-builder/minecraftize/CONTRACT.md
schematic                 → kits/lazy-builder/schematic/EXPORT.md
active continuation      → docs/knowledge/next-action.md
```
