# Changelog

All notable LazyBuilder system changes are recorded here.

## Unreleased

### Added

- PRD-Creator-style repository operating memory: `AGENTS.md`, `CONTEXT.md`, `GITHUB_RULES.md`, foundation policy, knowledge routing, decisions, reviews, backlog, and work modes.
- `develop` working branch model with `Local` verified integration baseline and `main` stable history.
- Repository verification and promotion workflows.
- Single product package routing under `kits/lazy-builder/`.
- Explicit workspace boundary for live project/reference/generated data.

### Changed

- Active Development moves from direct `Local` editing to `develop`.
- Early standalone `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/ROADMAP.md`, and `docs/TOOLS.md` are replaced by canonical owners under root, `docs/foundation/`, and `docs/knowledge/`.

### Current product decisions preserved

- Hunyuan3D-2mv is the only active 3D generator.
- Blender 5.2.x LTS is the 3D workbench.
- Minecraftize is the only custom core targeted for MVP development.
- `mcschematic` is the intended schematic writer.
- Axiom is the final import/edit/placement tool.
- MCP and multi-model routing remain deferred.
