# Axiom Audit Verification — 2026-09-08

Status: PASS for repository/static audit contract; local Axiom/Paper/Minecraft runtime still required.

## Audit delivery

```text
commit: ef26a1db8ad78922032020d2c55282f75456fd7b
message: docs(axiom): audit 1.21.4 integration baseline
```

This delivery added/updated the canonical Axiom decision, full binary/research review, exporter contract, validator contract, source-authority rules, continuation, current validation, context, and repository verifier.

The first verifier run correctly failed because three new checks were overly literal about documentation wording, not because the audit facts conflicted.

## Verifier correction

```text
commit: fc9ff82800293a293526dac0e018ad8f0d39ce97
message: test(axiom): align audit contract verifier
```

The correction changed only verifier marker matching so it validates the intended semantic contract without requiring accidental capitalization/wording.

## Repository verification

```text
workflow: Repository Verify
run: 34221732836
head: fc9ff82800293a293526dac0e018ad8f0d39ce97
result: PASS
```

The passing gate protects, among other things:

- Axiom 5.3.0 client baseline;
- AxiomPaper 5.0.1+1.21.4 baseline;
- rejection of supplied AxiomPaper 4.0.4 for API-family mismatch;
- Sponge Schematic Version 2 / DataVersion 4189 contract;
- dimension-centered Axiom import behavior;
- M1 import/handshake diagnostic contract;
- external-only Axiom runtime JAR boundary.

## Writer regression after audit

The audit delivery also reran the executable writer fixture:

```text
workflow: M1 Schematic Smoke
run: 34221558236
head: ef26a1db8ad78922032020d2c55282f75456fd7b
result: PASS
```

This confirms the Axiom documentation/integration audit did not break the existing `mcschematic` generation + reload contract.

## Evidence boundary

This record proves repository consistency and writer regression only.

Still required in the user's exact runtime:

```text
Axiom 5.3.0 client startup
AxiomPaper 5.0.1 startup
API-family 9 handshake
Import Schematic permission
lazybuilder_m1_smoke.schem import
Clipboard result
Paper/Minecraft placement
stair/slab orientation
```

Do not mark M1 end-to-end PASS or start M2 solely from this static/repository evidence.
