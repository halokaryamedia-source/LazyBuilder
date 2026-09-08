# Source Authority

Use this note only when source/state precedence for a claim is unclear. Repository/file ownership lives in `ownership.md`; work-mode routing lives in root `AGENTS.md`.

## Build authority chain

Use the most upstream valid owner:

```text
current explicit user instruction
→ approved build/project decisions
→ authoritative reference images / drawings / dimensions
→ normalized current project constraints when persisted
→ Hunyuan3D-2mv mesh as generated geometric hypothesis
→ Blender target as working implementation representation
→ Minecraftize block model / preview
→ `.schem`
→ Axiom/Minecraft placement, screenshots, reviews, chat/history
```

Authority decreases downstream. Generated artifacts do not repair or outrank the original build/reference requirement.

## Source classes

- **authoritative** — current user instruction, approved decisions, supplied source that establishes current build facts;
- **supporting** — context/evidence that does not outrank current authority;
- **generated hypothesis** — Hunyuan geometry inferred from references;
- **working representation** — cleaned Blender target;
- **derived implementation** — Minecraftize preview/block model and schematic;
- **acceptance evidence** — Axiom/Minecraft runtime result, screenshots, measurements, review.

## Axiom integration source precedence

Exact Axiom compatibility claims use this precedence:

```text
current explicit user runtime instruction
→ exact user-supplied JAR fingerprint/content
→ actual executed runtime behavior with that environment
→ official version-specific Axiom/Modrinth release metadata
→ official Axiom documentation
→ current upstream AxiomPaper source
→ general knowledge / historical assumptions
```

Interpretation rules:

- exact supplied `Axiom 5.3.0` / `AxiomPaper 5.0.1` binary behavior outranks latest upstream source when the question is about this exact baseline;
- actual executed runtime evidence outranks static binary expectations for what really happened in the user's environment;
- current upstream source is supporting evidence only when it has moved beyond the exact supplied release;
- the public Axiom documentation currently reports `Last Documentation Update: 31/Jul/25`, so exact supplied binary behavior resolves version-specific discrepancies;
- a documentation omission does not prove a feature is absent from the supplied binary; for example the exact Axiom 5.3.0 file picker accepts `.litematic` in addition to the public documentation's `.schem` / `.schematic` statement;
- do not commit or redistribute the user-supplied Axiom client JAR. Record hashes/metadata and keep binaries external.

Canonical current Axiom research owners:

```text
durable compatibility decision
→ decisions/axiom-1.21.4-integration-baseline.md

full research/static evidence
→ reviews/history/axiom-audit-2026-09-08.md

export behavior
→ kits/lazy-builder/schematic/EXPORT.md

runtime acceptance/failure routing
→ kits/lazy-builder/validator/VALIDATION.md
```

## Partial supersession

If a later instruction changes one side, dimension, runtime version, or component, supersede only the affected claim. Do not discard unrelated valid reference meaning or compatibility evidence.

For Axiom specifically, changing one runtime component creates a new compatibility state. Example:

```text
AxiomPaper 5.0.1 → 5.0.4
```

does not silently invalidate all schematic findings, but it does require the Paper binary fingerprint, handshake/permission evidence, and placement result to be revalidated before the new pair becomes canonical.

## Reference conflict rule

If material reference views conflict and precedence cannot resolve them safely:

```text
UNKNOWN
→ identify conflicting views/claims
→ identify affected geometry/output
→ resolve through current user/project authority
```

Never choose silently because one image is newer-looking, sharper, or easier for the model.

## Runtime conflict rule

If static/documented expectations disagree with executed Axiom/Paper behavior:

```text
preserve exact runtime evidence
→ record exact binary/version/config/permissions/integrations
→ diagnose first wrong owner
→ update only the affected compatibility claim
```

Do not rewrite the exporter or change versions merely to make expectations match.

## Generated-model boundary

A convincing Hunyuan mesh may still be wrong relative to the source. It is evidence to inspect, not authority to follow blindly.

Likewise, manual Axiom polish can improve delivery but must not be used to claim the pre-polish LazyBuilder engine already produced that quality.
