#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from session_contract import create_session, stage_map
from session_controller import build_action


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="lazybuilder-pre-runtime-") as name:
        root = Path(name)
        prompt = root / "inputs/text/prompt.txt"
        prompt.parent.mkdir(parents=True, exist_ok=True)
        prompt.write_text("bounded architectural test object\n", encoding="utf-8")
        png = b"\x89PNG\r\n\x1a\nstatic-pre-runtime-placeholder"
        single = root / "inputs/single/front.png"
        _write(single, png)
        multiview = {}
        for view in ("front", "right", "back", "left"):
            path = root / f"inputs/multiview/{view}.png"
            _write(path, png + view.encode("ascii"))
            multiview[view] = str(path.relative_to(root))

        case = {
            "schema_version": 1,
            "case_id": "static-dry-run",
            "minecraft_version": "1.21.4",
            "inputs": {
                "T1": {"kind": "text", "prompt_path": str(prompt.relative_to(root))},
                "I1": {"kind": "single", "views": {"front": str(single.relative_to(root))}},
                "I2": {"kind": "multiview", "views": multiview},
            },
            "target": {"target_width_blocks": 64},
        }
        run_dir = root / "runs/dry-run"
        session = create_session(case=case, case_root=root, run_id="dry-run", run_dir=run_dir)
        session["selected_shape_stage"] = "shape_single"
        actions = {
            stage: build_action(session, stage)
            for stage in (
                "preflight",
                "text_reference",
                "shape_single",
                "shape_multiview",
                "blender",
                "minecraftize_primitives",
                "minecraftize_model",
                "minecraft_preview",
                "schematic",
                "axiom",
            )
        }

        assert actions["preflight"]["kind"] == "command_plus_declared_facts"
        assert "collect_environment.py" in " ".join(actions["preflight"]["argv"])
        assert actions["minecraftize_primitives"]["kind"] == "command"
        assert "run_primitive_suite.py" in " ".join(actions["minecraftize_primitives"]["argv"])
        assert actions["minecraftize_model"]["kind"] == "command"
        model_argv = actions["minecraftize_model"]["argv"]
        assert "minecraftize_v0.py" in " ".join(model_argv)
        assert "LazyBuilderTarget" in model_argv
        assert "64" in model_argv
        assert actions["blender"]["target_object_name"] == "LazyBuilderTarget"
        assert "write_target_metadata.py" in actions["blender"]["metadata_helper"]
        assert actions["minecraft_preview"]["kind"] == "command"
        assert "build_preview.py" in " ".join(actions["minecraft_preview"]["argv"])
        assert actions["schematic"]["kind"] == "command"
        assert actions["axiom"]["kind"] == "manual_application"
        assert stage_map(session)["minecraft_preview"]["output_paths"][0].endswith("preview.svg")

        print(json.dumps({
            "status": "PASS",
            "proof": "STATIC_PRE_RUNTIME_DRY_RUN_PASS_RUNTIME_NOT_STARTED",
            "runtime_launched": False,
            "checked_actions": sorted(actions),
        }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
