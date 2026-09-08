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


class TestReadinessContractTests(unittest.TestCase):
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
            self.assertEqual(session["active_stage"], "preflight")
            validate_session(session)

    def test_preflight_unlocks_independent_generation_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-002", run_dir=root / "runs/run-002")
            stages = stage_map(session)
            stages["preflight"]["status"] = "PASS"
            from session_contract import refresh_ready

            refresh_ready(session)
            self.assertEqual(stages["text_reference"]["status"], "READY")
            self.assertEqual(stages["shape_single"]["status"], "READY")
            self.assertEqual(stages["shape_multiview"]["status"], "READY")
            self.assertEqual(stages["shape_text"]["status"], "PENDING")

    def test_blender_requires_all_shape_proofs_and_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-003", run_dir=root / "runs/run-003")
            stages = stage_map(session)
            for stage_id in ("preflight", "text_reference", "shape_text", "shape_single", "shape_multiview"):
                stages[stage_id]["status"] = "PASS"
            from session_contract import refresh_ready

            refresh_ready(session)
            self.assertEqual(stages["blender"]["status"], "PENDING")
            session["selected_shape_stage"] = "shape_multiview"
            refresh_ready(session)
            self.assertEqual(stages["blender"]["status"], "READY")

    def test_invalidation_preserves_history_and_resumes_from_first_wrong_stage(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-004", run_dir=root / "runs/run-004")
            stages = stage_map(session)
            for stage_id in STAGE_ORDER[:8]:
                stages[stage_id]["status"] = "PASS"
            stages["minecraftize_model"]["notes"] = ["old evidence"]
            session["selected_shape_stage"] = "shape_multiview"
            invalidate_from(session, "minecraftize_model", "converter defect")
            self.assertEqual(stages["blender"]["status"], "PASS")
            self.assertEqual(stages["minecraftize_model"]["status"], "READY")
            self.assertEqual(stages["schematic"]["status"], "PENDING")
            self.assertTrue(stages["minecraftize_model"]["history"])

            stages["shape_single"]["status"] = "PASS"
            stages["shape_multiview"]["status"] = "PASS"
            invalidate_from(session, "shape_single", "new single-image input")
            self.assertEqual(stages["shape_single"]["status"], "READY")
            self.assertEqual(stages["shape_multiview"]["status"], "PASS")
            self.assertEqual(stages["blender"]["status"], "PENDING")

    def test_action_contract_exposes_real_paths_and_known_blockers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-005", run_dir=root / "runs/run-005")
            stage_action = build_action(session, "shape_multiview")
            self.assertEqual(stage_action["kind"], "command")
            self.assertIn("--front", stage_action["argv"])
            self.assertIn("--left", stage_action["argv"])
            blocker = build_action(session, "minecraftize_model")
            self.assertEqual(blocker["kind"], "blocked")
            self.assertEqual(blocker["blocker"], "MINECRAFTIZE_RUNTIME_ENTRYPOINT_NOT_IMPLEMENTED")

    def test_acceptance_report_never_upgrades_partial_to_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = make_case(root)
            session = create_session(case=case, case_root=root, run_id="run-006", run_dir=root / "runs/run-006")
            report = build_report(session)
            self.assertEqual(report["overall_status"], "PARTIAL")
            stages = stage_map(session)
            stages["preflight"]["status"] = "BLOCKED"
            report = build_report(session)
            self.assertEqual(report["overall_status"], "BLOCKED")
            self.assertEqual(report["first_failed_stage"], "preflight")


if __name__ == "__main__":
    unittest.main()
