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

## Partial supersession

If a later instruction changes one side, dimension, or component, supersede only the affected claim. Do not discard unrelated valid reference meaning.

## Reference conflict rule

If material reference views conflict and precedence cannot resolve them safely:

```text
UNKNOWN
→ identify conflicting views/claims
→ identify affected geometry/output
→ resolve through current user/project authority
```

Never choose silently because one image is newer-looking, sharper, or easier for the model.

## Generated-model boundary

A convincing Hunyuan mesh may still be wrong relative to the source. It is evidence to inspect, not authority to follow blindly.

Likewise, manual Axiom polish can improve delivery but must not be used to claim the pre-polish LazyBuilder engine already produced that quality.
