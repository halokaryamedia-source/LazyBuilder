# Maintenance Workflow

Use Maintenance for bugs, regressions, review/cleanup, stale documentation, broken routing, and behavior-preserving refactors.

```text
reported bug/review/cleanup
→ identify affected owner
→ observe/reproduce concrete drift
→ cause/scope grounded?
   no → UNKNOWN / LOCAL RUNTIME PROOF REQUIRED / Perlu pemeriksaan
   yes
   → smallest safe correction
   → targeted proof
   → scope/diff review
   → update only canonical owner whose state changed
```

## Categories

- **Bug** — reproduce/inspect, diagnose cause, correct smallest owner, add only useful regression proof.
- **Artifact defect** — decide whether source, Hunyuan generation, Blender target, Minecraftize, export, or validation is first wrong.
- **Small refactor** — preserve behavior; prefer deletion/simplification over new abstraction.
- **Documentation cleanup** — edit current owner and remove duplicate/stale routing.
- **Historical review cleanup** — preserve capture-time review body; current meaning belongs in `reviews/README.md`.

## Root-cause rule

Before editing establish:

1. what is actually wrong;
2. where the first incorrect owner/state appears;
3. why the proposed fix addresses that cause;
4. what evidence proves the defect no longer exists.

Examples:

```text
bad block layout in exported .schem
→ inspect Minecraftize model first
→ do not patch schematic bytes manually

Hunyuan mesh contradicts references
→ inspect reference consistency/generation
→ do not treat generated mesh as authority

Axiom manual polish looks good
→ valid delivery evidence
→ not proof original Minecraftize output was already correct
```

## Validation economy

Run only proof invalidated by the change. Do not replay the entire pipeline for a local documentation or converter correction when a targeted proof can falsify it.

## Scope rules

- diagnose before patching;
- do not turn cleanup into feature work;
- do not add fallback/provider/compatibility layers unless cause proves they are needed;
- stop repeating the same failed direction after two attempts without new evidence;
- `No change required` is valid when inspection disproves the reported defect.
