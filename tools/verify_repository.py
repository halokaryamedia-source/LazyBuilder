#!/usr/bin/env python3
"""Static repository contract checks for LazyBuilder.

This gate protects stable repository/routing/integration invariants. It does not
prove Hunyuan, Blender, Axiom, Paper, Minecraft runtime behavior, or subjective
build quality.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_SKILLS = {"development-brief", "build-production"}
KIT_ROOT = ROOT / "kits" / "lazy-builder"
KIT_DIRS = {"intake", "generation", "blender", "minecraftize", "schematic", "validator"}
KIT_ROOT_MARKDOWN = {"README.md", "AGENTS.md", "SKILL.md"}

REQUIRED_PATHS = [
    "AGENTS.md",
    "GITHUB_RULES.md",
    "CONTEXT.md",
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "LICENSE",
    ".gitignore",
    ".gitattributes",
    "requirements.txt",
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/repository-verify.yml",
    ".github/workflows/local-promotion-verify.yml",
    ".github/workflows/release-verify.yml",
    ".github/workflows/m1-schematic-smoke.yml",
    ".agents/skills/development-brief/SKILL.md",
    ".agents/skills/build-production/SKILL.md",
    "docs/foundation/README.md",
    "docs/foundation/00-product-boundaries.md",
    "docs/foundation/01-production-flow.md",
    "docs/foundation/02-reference-intake.md",
    "docs/foundation/03-hunyuan-generation.md",
    "docs/foundation/04-blender-target-preparation.md",
    "docs/foundation/05-minecraftize-conversion.md",
    "docs/foundation/06-schematic-validation-handoff.md",
    "docs/knowledge/README.md",
    "docs/knowledge/next-action.md",
    "docs/knowledge/work-routing.md",
    "docs/knowledge/ownership.md",
    "docs/knowledge/source-authority.md",
    "docs/knowledge/work-modes/development.md",
    "docs/knowledge/work-modes/maintenance.md",
    "docs/knowledge/work-modes/maintenance-note-template.md",
    "docs/knowledge/skills/README.md",
    "docs/knowledge/skills/activation-matrix.md",
    "docs/knowledge/decisions/README.md",
    "docs/knowledge/decisions/recording-policy.md",
    "docs/knowledge/decisions/branch-governance.md",
    "docs/knowledge/decisions/execution-modes-local-remote-github.md",
    "docs/knowledge/decisions/single-hunyuan-provider.md",
    "docs/knowledge/decisions/minecraftize-core-boundary.md",
    "docs/knowledge/decisions/anti-overdevelopment-simplification.md",
    "docs/knowledge/decisions/astra6-extrahigh-development-profile.md",
    "docs/knowledge/decisions/axiom-1.21.4-integration-baseline.md",
    "docs/knowledge/reviews/README.md",
    "docs/knowledge/reviews/audit-template.md",
    "docs/knowledge/reviews/current-validation.md",
    "docs/knowledge/reviews/history/README.md",
    "docs/knowledge/reviews/history/axiom-audit-2026-09-08.md",
    "docs/knowledge/operations/backlog.md",
    "docs/knowledge/operations/boot-baseline.md",
    "kits/lazy-builder/README.md",
    "kits/lazy-builder/AGENTS.md",
    "kits/lazy-builder/SKILL.md",
    "kits/lazy-builder/intake/REFERENCE-INTAKE.md",
    "kits/lazy-builder/generation/HUNYUAN3D-2MV.md",
    "kits/lazy-builder/blender/TARGET-MODEL.md",
    "kits/lazy-builder/minecraftize/CONTRACT.md",
    "kits/lazy-builder/schematic/EXPORT.md",
    "kits/lazy-builder/validator/VALIDATION.md",
    "tools/m1_schematic_smoke.py",
    "workspace/README.md",
    "workspace/active/README.md",
    "workspace/archive/README.md",
]

RETIRED_PATHS = [
    "docs/ARCHITECTURE.md",
    "docs/DECISIONS.md",
    "docs/ROADMAP.md",
    "docs/TOOLS.md",
]

MARKDOWN_ROOTS = [
    ROOT / "AGENTS.md",
    ROOT / "GITHUB_RULES.md",
    ROOT / "CONTEXT.md",
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "docs" / "foundation",
    ROOT / "docs" / "knowledge",
    ROOT / ".agents" / "skills",
    KIT_ROOT,
    ROOT / "workspace",
]

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for item in MARKDOWN_ROOTS:
        if item.is_file():
            files.append(item)
        elif item.is_dir():
            files.extend(item.rglob("*.md"))
    return sorted(set(files))


def check_required_paths(errors: list[str]) -> None:
    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).is_file():
            fail(errors, f"missing required owner: {rel}")


def check_retired_paths(errors: list[str]) -> None:
    for rel in RETIRED_PATHS:
        if (ROOT / rel).exists():
            fail(errors, f"retired duplicate owner must not return: {rel}")


def check_skill_shape(errors: list[str]) -> None:
    root = ROOT / ".agents" / "skills"
    if not root.is_dir():
        fail(errors, "missing .agents/skills root")
        return
    actual = {p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")}
    if actual != CANONICAL_SKILLS:
        fail(errors, f"canonical skill set drift: expected {sorted(CANONICAL_SKILLS)}, got {sorted(actual)}")
    for skill in CANONICAL_SKILLS:
        if not (root / skill / "SKILL.md").is_file():
            fail(errors, f"missing SKILL.md for canonical skill: {skill}")
    for forbidden in ("local", "remote_github"):
        if (root / forbidden).exists():
            fail(errors, f"execution mode must not become a root skill: {forbidden}")


def check_kit_shape(errors: list[str]) -> None:
    kits_root = ROOT / "kits"
    if not kits_root.is_dir():
        fail(errors, "missing kits/ root")
        return
    actual_kits = {p.name for p in kits_root.iterdir() if p.is_dir() and not p.name.startswith(".")}
    if actual_kits != {"lazy-builder"}:
        fail(errors, f"active product kit drift: expected ['lazy-builder'], got {sorted(actual_kits)}")
    if not KIT_ROOT.is_dir():
        return
    actual_dirs = {p.name for p in KIT_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")}
    if actual_dirs != KIT_DIRS:
        fail(errors, f"kit domain drift: expected {sorted(KIT_DIRS)}, got {sorted(actual_dirs)}")
    actual_root_md = {p.name for p in KIT_ROOT.glob("*.md")}
    if actual_root_md != KIT_ROOT_MARKDOWN:
        fail(errors, f"kit root Markdown drift: expected {sorted(KIT_ROOT_MARKDOWN)}, got {sorted(actual_root_md)}")


def check_branch_contract(errors: list[str]) -> None:
    owners = ["AGENTS.md", "CONTEXT.md", "CONTRIBUTING.md"]
    for rel in owners:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for branch in ("develop", "Local", "main"):
            if branch not in text:
                fail(errors, f"{rel} missing branch contract marker: {branch}")
    contributing = ROOT / "CONTRIBUTING.md"
    if contributing.is_file():
        text = contributing.read_text(encoding="utf-8")
        for marker in ("Squash and merge", "normal merge commit", "exactly one new commit"):
            if marker not in text:
                fail(errors, f"CONTRIBUTING.md missing promotion marker: {marker}")


def check_execution_modes(errors: list[str]) -> None:
    owners = [
        "GITHUB_RULES.md",
        "docs/knowledge/work-routing.md",
        "docs/knowledge/work-modes/development.md",
    ]
    for rel in owners:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in ("remote_github", "`local`", "`Local`"):
            if marker not in text:
                fail(errors, f"{rel} missing execution-mode marker: {marker}")

    rules = ROOT / "GITHUB_RULES.md"
    if rules.is_file():
        text = rules.read_text(encoding="utf-8")
        for marker in (
            "local  = execution mode",
            "Local  = verified integration branch",
            "git pull --ff-only origin develop",
        ):
            if marker not in text:
                fail(errors, f"GITHUB_RULES.md missing execution-mode contract: {marker}")

    decision = ROOT / "docs" / "knowledge" / "decisions" / "execution-modes-local-remote-github.md"
    if decision.is_file():
        text = decision.read_text(encoding="utf-8")
        for marker in ("remote_github", "local  = execution mode", "Local  = verified integration branch"):
            if marker not in text:
                fail(errors, f"execution-mode decision missing marker: {marker}")


def check_product_markers(errors: list[str]) -> None:
    context = ROOT / "CONTEXT.md"
    if not context.is_file():
        return
    text = context.read_text(encoding="utf-8")
    for marker in (
        "Hunyuan3D-2mv",
        "Blender 5.2.x LTS",
        "Minecraftize",
        "mcschematic==11.4.4",
        "Axiom",
        "Minecraft Java Edition",
    ):
        if marker not in text:
            fail(errors, f"CONTEXT.md missing locked product marker: {marker}")


def check_m1_contract(errors: list[str]) -> None:
    requirements = ROOT / "requirements.txt"
    if requirements.is_file():
        lines = [line.strip() for line in requirements.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines != ["mcschematic==11.4.4"]:
            fail(errors, f"M1 writer dependency drift: expected only mcschematic==11.4.4, got {lines}")

    script = ROOT / "tools" / "m1_schematic_smoke.py"
    if script.is_file():
        text = script.read_text(encoding="utf-8")
        for marker in (
            'DEFAULT_VERSION = "JE_1_21_4"',
            "minecraft:stone_bricks",
            "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
            "minecraft:stone_slab[type=top,waterlogged=false]",
            "MCSchematic(str(schem_path))",
            "getBlockStateAt(position)",
        ):
            if marker not in text:
                fail(errors, f"M1 smoke script missing contract marker: {marker}")

    workflow = ROOT / ".github" / "workflows" / "m1-schematic-smoke.yml"
    if workflow.is_file():
        text = workflow.read_text(encoding="utf-8")
        for marker in (
            "M1 Schematic Smoke",
            "m1_schematic_smoke.py",
            "JE_1_21_4",
            "lazybuilder-m1-schematic-je-1-21-4",
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
        ):
            if marker not in text:
                fail(errors, f"M1 workflow missing contract marker: {marker}")

    gitignore = ROOT / ".gitignore"
    if gitignore.is_file() and "artifacts/" not in gitignore.read_text(encoding="utf-8"):
        fail(errors, ".gitignore must ignore generated artifacts/")


def check_axiom_contract(errors: list[str]) -> None:
    context = ROOT / "CONTEXT.md"
    if context.is_file():
        text = context.read_text(encoding="utf-8")
        for marker in (
            "Axiom 5.3.0",
            "AxiomPaper 5.0.1+1.21.4",
            "Axiom API family 9",
            "Sponge Schematic Version 2",
            "DataVersion 4189",
            "Axiom 5.3.0 CLIENT parses the file",
        ):
            if marker not in text:
                fail(errors, f"CONTEXT.md missing Axiom integration marker: {marker}")

    decision = ROOT / "docs" / "knowledge" / "decisions" / "axiom-1.21.4-integration-baseline.md"
    if decision.is_file():
        text = decision.read_text(encoding="utf-8")
        for marker in (
            "Axiom 5.3.0",
            "AxiomPaper 5.0.1+1.21.4",
            "AxiomPaper 4.0.4",
            "API version is 8",
            "AxiomPaper `5.0.4+1.21.4`",
            "## Upgrade policy",
            "Sponge Schematic Version 2",
            "DataVersion 4189",
            "CLIENT parses file locally",
        ):
            if marker not in text:
                fail(errors, f"Axiom decision missing marker: {marker}")

    export = KIT_ROOT / "schematic" / "EXPORT.md"
    if export.is_file():
        text = export.read_text(encoding="utf-8")
        for marker in (
            "mcschematic==11.4.4",
            "Sponge Schematic Version 2",
            "DataVersion 4189",
            "localX = x - floor(width / 2)",
            "Axiom client",
            "tight bounds",
        ):
            if marker not in text:
                fail(errors, f"schematic EXPORT.md missing Axiom contract marker: {marker}")

    validation = KIT_ROOT / "validator" / "VALIDATION.md"
    if validation.is_file():
        text = validation.read_text(encoding="utf-8")
        for marker in (
            "AxiomPaper 5.0.1+1.21.4",
            "axiom.can_import_blocks",
            "/whynoaxiom",
            "/axiomhandshake",
            "LOCAL RUNTIME PROOF REQUIRED",
            "AxiomPaper 5.0.4+1.21.4",
        ):
            if marker not in text:
                fail(errors, f"VALIDATION.md missing Axiom runtime marker: {marker}")

    audit = ROOT / "docs" / "knowledge" / "reviews" / "history" / "axiom-audit-2026-09-08.md"
    if audit.is_file():
        text = audit.read_text(encoding="utf-8")
        for marker in (
            "AxiomPaper does **not** need to parse LazyBuilder's `.schem` file",
            "Version = 2",
            "Version = 3",
            "DataVersion 4189",
            "x - floor(width / 2)",
            "allow-large-payload-for-all-packets",
            "AxiomPaper 5.0.4+1.21.4",
        ):
            if marker not in text:
                fail(errors, f"Axiom audit missing evidence marker: {marker}")

    for jar in ROOT.rglob("*.jar"):
        if jar.name.lower().startswith("axiom"):
            fail(errors, f"Axiom runtime JAR must remain external and untracked: {jar.relative_to(ROOT)}")


def check_markdown_links(errors: list[str]) -> None:
    for path in iter_markdown_files():
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(errors, f"Markdown link escapes repository in {path.relative_to(ROOT)}: {raw}")
                continue
            if not resolved.exists():
                fail(errors, f"broken Markdown link in {path.relative_to(ROOT)}: {raw}")


def main() -> int:
    errors: list[str] = []
    check_required_paths(errors)
    check_retired_paths(errors)
    check_skill_shape(errors)
    check_kit_shape(errors)
    check_branch_contract(errors)
    check_execution_modes(errors)
    check_product_markers(errors)
    check_m1_contract(errors)
    check_axiom_contract(errors)
    check_markdown_links(errors)

    if errors:
        print("LazyBuilder repository verification FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("LazyBuilder repository verification PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
