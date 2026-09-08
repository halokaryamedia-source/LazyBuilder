# GPT Astra 6 ExtraHigh Development Profile

Date: 2026-09-08  
Status: current

## Context

LazyBuilder will primarily be developed through ChatGPT using the user's selected **GPT Astra 6 ExtraHigh** configuration. The repository already uses PRD-Creator-style canonical owners, continuity recovery, bounded work modes, and anti-overdevelopment rules. Without an explicit model-execution profile, a high-reasoning session could still waste capability on broad repository rereads, verbose planning, repeated speculative alternatives, or manual generation of data that should be deterministic.

The goal is to make Astra6 effective through repository structure, not through fragile prompt hacks.

## Decision

Use GPT Astra 6 ExtraHigh as the preferred **Development operator profile**, with this execution contract:

```text
minimum canonical boot
→ compact active task packet
→ first wrong / changed owner
→ smallest complete implementation
→ deterministic mechanics in code
→ cheapest falsifying proof
→ bounded repair if needed
→ STOP
```

The compact active task packet is:

```text
Goal
Owner
Hard constraints / out-of-scope
2–5 acceptance criteria
Proof budget
Exact current evidence / failure
```

After mandatory boot, default to 1–3 additional owner files unless a material dependency proves more context is needed.

## Why

A high-reasoning model creates the most value when it is used for:

- requirement synthesis and ambiguity resolution;
- architecture/tradeoff decisions;
- root-cause diagnosis;
- choosing the smallest correct implementation;
- interpreting proof and deciding the next bounded repair.

It creates less value when used to manually emit repetitive coordinates, BlockStates, NBT structures, geometry samples, serialization bytes, or other deterministic data.

Therefore:

```text
reasoning / diagnosis / architecture
→ Astra6

repeatable computation / transforms / serialization / invariants
→ code + tests

external application behavior
→ actual runtime proof
```

## Model-portability boundary

This decision does **not** make LazyBuilder dependent on undocumented Astra6 internals.

Do not depend on:

- private chain-of-thought;
- hidden model state across sessions;
- giant persistent prompts that duplicate repository owners;
- model-specific response quirks;
- an Astra-only MCP/agent framework;
- automatic assumptions that ExtraHigh reasoning is proof of runtime behavior.

A different capable model or developer should be able to recover the same current state from repository owners and execute the same tests.

## Efficiency rules

- Read exact owners, not the repository broadly.
- Use current tool/runtime output as evidence; do not immediately refetch it without reason.
- Prefer one bounded implementation pass over several speculative variants.
- Do not create a plan file per task.
- Do not create an Astra-specific skill; root `AGENTS.md` + `development-brief` own the execution profile.
- Use acceptance criteria to terminate work; do not continue optional cleanup because reasoning budget remains.
- When a deterministic failure is identified, fix its owner before asking the model to redesign adjacent systems.

## Tradeoffs / not chosen

Not chosen:

- a large universal system prompt stored in the repo;
- separate prompts for every package directory;
- an Astra-specific agent framework or MCP layer;
- loading all docs for every development request;
- model-generated bulk Minecraft geometry instead of deterministic conversion code.

The tradeoff is that canonical ownership must stay accurate. This is intentional: repository memory is the durable source, while the model is the reasoning/execution layer.

## Evidence / validation boundary

Repository verification can prove that the execution-profile owners and links remain coherent. It cannot prove subjective model quality or runtime product behavior.

Effectiveness should be judged operationally by:

- fewer unnecessary reads/tool calls;
- less repeated context recovery;
- bounded diffs;
- targeted tests identifying the first wrong owner;
- no extra framework created without demonstrated need;
- successful product milestones with runtime evidence.

## Follow-up owner

- top-level execution behavior → `AGENTS.md`;
- non-trivial Development procedure → `.agents/skills/development-brief/SKILL.md`;
- package context economy → `kits/lazy-builder/AGENTS.md`;
- stable orientation → `CONTEXT.md`.

Do not create another model-profile owner unless this architecture proves insufficient.
