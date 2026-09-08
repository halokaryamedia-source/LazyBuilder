from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from acceptance_report import build_report
from session_contract import (
    ContractError,
    STAGE_ORDER,
    create_session,
    record_artifacts,
    record_inputs,
    refresh_ready,
    stage_map,
    validate_case,
    validate_session,
)
from session_controller import build_action, invalidate_from


def make_case(root: Path) -> dict:
    (root / "inputs/text").mkdir(parents=True)
    (root / "inputs/single").mkdir(parents=True)
    (root / "inputs/multiview").mkdir(parents=True)
    (root / "inputs/text/prompt.txt").write_text("compact stone station", encoding="utf-8")
    (root / "inputs/single/front.png").write_bytes(b"front")
    for view in ("front", "right", "back", "left"):
        (root / f"inputs/multiview/{view}.png").write_bytes(view.encode())
    return {
        "schema_version": 1,
        "case_id": "fixture",
        "minecraft_version": "1.21.4",
        "inputs": {
            "T1": {"kind": "text", "prompt_path": "inputs/text/prompt.txt"},
            "I1": {"kind": "single", "views": {"front": "inputs/single/front.png"}},
            "I2": {
                "kind": "multiview",
                "views": {view: f"inputs/multiview/{view}.png" for view in ("front", "right", "back", "left")},
            },
        },
        "target": {"target_width_blocks": 64},
    }


class PreRuntimeContractTests(unittest.TestCase):
    def test_case_contract_requires_all_three_input_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            normalized = validate_case(case, case_root=root, require_files=True)
            self.assertEqual(normalized["inputs"]["T1"]["kind"], "text")
            broken = json.loads(json.dumps(case))
            del broken["inputs"]["I2"]["views"]["left"]
            with self.assertRaises(ContractError):
                validate_case(broken, case_root=root, require_files=True)

    def test_session_starts_with_only_preflight_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-001", run_dir=root / "runs/run-001")
            stages = stage_map(session)
            self.assertEqual(stages["preflight"]["status"], "READY")
            self.assertEqual(stages["text_reference"]["status"], "PENDING")
            self.assertEqual(stages["minecraftize_primitives"]["status"], "PENDING")
            self.assertEqual(session["active_stage"], "preflight")
            validate_session(session)

    def test_preflight_unlocks_generation_and_independent_primitive_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-002", run_dir=root / "runs/run-002")
            stages = stage_map(session)
            stages["preflight"]["status"] = "PASS"
            refresh_ready(session)
            self.assertEqual(stages["text_reference"]["status"], "READY")
            self.assertEqual(stages["shape_single"]["status"], "READY")
            self.assertEqual(stages["shape_multiview"]["status"], "READY")
            self.assertEqual(stages["minecraftize_primitives"]["status"], "READY")
            self.assertEqual(stages["blender"]["status"], "PENDING")

    def test_blender_requires_all_shape_proofs_and_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-003", run_dir=root / "runs/run-003")
            stages = stage_map(session)
            for stage_id in ("preflight", "text_reference", "shape_text", "shape_single", "shape_multiview"):
                stages[stage_id]["status"] = "PASS"
            refresh_ready(session)
            self.assertEqual(stages["blender"]["status"], "PENDING")
            session["selected_shape_stage"] = "shape_multiview"
            refresh_ready(session)
            self.assertEqual(stages["blender"]["status"], "READY")

    def test_invalidation_preserves_true_independent_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-004", run_dir=root / "runs/run-004")
            stages = stage_map(session)
            for stage_id in STAGE_ORDER:
                stages[stage_id]["status"] = "PASS"
            session["selected_shape_stage"] = "shape_multiview"
            invalidate_from(session, "blender", "new representative shape")
            self.assertEqual(stages["minecraftize_primitives"]["status"], "PASS")
            self.assertEqual(stages["blender"]["status"], "READY")
            self.assertEqual(stages["minecraftize_model"]["status"], "PENDING")
            self.assertEqual(stages["minecraft_preview"]["status"], "PENDING")
            self.assertEqual(stages["schematic"]["status"], "PENDING")
            self.assertEqual(stages["axiom"]["status"], "PENDING")

    def test_case_input_drift_is_rejected_before_stage_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-005", run_dir=root / "runs/run-005")
            stages = stage_map(session)
            stages["preflight"]["status"] = "PASS"
            refresh_ready(session)
            (root / "inputs/single/front.png").write_bytes(b"changed")
            with self.assertRaisesRegex(ContractError, "input drift detected"):
                record_inputs(session, stages["shape_single"])

    def test_upstream_artifact_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-006", run_dir=root / "runs/run-006")
            stages = stage_map(session)
            shape = stages["shape_single"]
            for path in shape["output_paths"]:
                p = Path(path)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b"original")
            record_artifacts(shape)
            shape["status"] = "PASS"
            session["selected_shape_stage"] = "shape_single"
            blender = stages["blender"]
            blender["input_paths"] = list(shape["output_paths"])
            Path(shape["output_paths"][0]).write_bytes(b"mutated")
            with self.assertRaisesRegex(ContractError, "input drift detected"):
                record_inputs(session, blender)

    def test_action_contract_exposes_preflight_preview_and_v0_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-007", run_dir=root / "runs/run-007")
            preflight = build_action(session, "preflight")
            self.assertIn("collect_environment.py", " ".join(preflight["argv"]))
            self.assertTrue(preflight["required_record_keys"])
            self.assertIn("hunyuan3d_model_revision", preflight["auto_recorded_keys"])
            self.assertNotIn("hunyuan3d_model_revision", preflight["required_record_keys"])

            stage_action = build_action(session, "shape_multiview")
            self.assertEqual(stage_action["kind"], "command")
            self.assertIn("--front", stage_action["argv"])
            self.assertIn("--left", stage_action["argv"])

            primitives = build_action(session, "minecraftize_primitives")
            self.assertIn("run_primitive_suite.py", " ".join(primitives["argv"]))

            model = build_action(session, "minecraftize_model")
            joined = " ".join(model["argv"])
            self.assertIn("minecraftize_v0.py", joined)
            self.assertIn("LazyBuilderTarget", model["argv"])
            self.assertIn("64", model["argv"])

            preview = build_action(session, "minecraft_preview")
            self.assertIn("build_preview.py", " ".join(preview["argv"]))
            self.assertTrue(preview["argv"][-1].endswith("45-preview"))

    def test_acceptance_report_contains_lineage_and_never_upgrades_partial(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-008", run_dir=root / "runs/run-008")
            report = build_report(session)
            self.assertEqual(report["overall_status"], "PARTIAL")
            self.assertIn("stage_evidence", report)
            self.assertIn("input_snapshot", report)
            stages = stage_map(session)
            stages["preflight"]["status"] = "BLOCKED"
            report = build_report(session)
            self.assertEqual(report["overall_status"], "BLOCKED")
            self.assertEqual(report["first_failed_stage"], "preflight")


if __name__ == "__main__":
    unittest.main()
