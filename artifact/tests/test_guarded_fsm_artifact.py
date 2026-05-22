from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import run_guarded_fsm_sim as sim


class GuardedFsmArtifactTests(unittest.TestCase):
    def test_approval_guard_rejects_execute_before_approval(self) -> None:
        policy = sim.APPROVAL_POLICY
        outcome = sim.run_sequence(policy, sim.controller_fsm_guard, ("request", "execute"))
        self.assertFalse(outcome["unsafe"])
        self.assertEqual(outcome["trace"], ["request"])
        self.assertEqual(outcome["blocked"], 1)

    def test_schema_guard_allows_history_sensitive_approval_violation(self) -> None:
        policy = sim.APPROVAL_POLICY
        outcome = sim.run_sequence(policy, sim.controller_schema_guard, ("request", "execute"))
        self.assertTrue(outcome["unsafe"])
        self.assertEqual(outcome["trace"], ["request", "execute"])

    def test_disclosure_guard_rejects_external_send_while_private(self) -> None:
        policy = sim.DISCLOSURE_POLICY
        outcome = sim.run_sequence(policy, sim.controller_fsm_guard, ("readPrivate", "sendExternal"))
        self.assertFalse(outcome["unsafe"])
        self.assertEqual(outcome["trace"], ["readPrivate"])
        self.assertEqual(outcome["blocked"], 1)

    def test_schema_guard_allows_disclosure_violation(self) -> None:
        policy = sim.DISCLOSURE_POLICY
        outcome = sim.run_sequence(policy, sim.controller_schema_guard, ("readPrivate", "sendExternal"))
        self.assertTrue(outcome["unsafe"])
        self.assertEqual(outcome["trace"], ["readPrivate", "sendExternal"])

    def test_fsm_enumeration_has_no_unsafe_sequences(self) -> None:
        rows = sim.exhaustive_enumeration(sim.APPROVAL_POLICY, 4)
        rows += sim.exhaustive_enumeration(sim.DISCLOSURE_POLICY, 4)
        fsm_rows = [row for row in rows if row["controller_id"] == "fsm_guard"]
        self.assertTrue(fsm_rows)
        self.assertTrue(all(row["unsafe_sequences"] == 0 for row in fsm_rows))

    def test_proof_obligations_record_blocked_unsafe_pairs(self) -> None:
        rows = sim.proof_obligation_rows()
        approval_execute = [
            row
            for row in rows
            if row["policy"] == "approval"
            and row["state"] == "Idle"
            and row["action"] == "execute"
        ]
        disclosure_external = [
            row
            for row in rows
            if row["policy"] == "disclosure"
            and row["state"] == "Private"
            and row["action"] == "sendExternal"
        ]
        self.assertEqual(approval_execute[0]["guard_decision"], "blocked")
        self.assertEqual(approval_execute[0]["unsafe_if_accepted"], "yes")
        self.assertEqual(disclosure_external[0]["guard_decision"], "blocked")
        self.assertEqual(disclosure_external[0]["unsafe_if_accepted"], "yes")

    def test_expected_results_validation_accepts_regenerated_quick_output(self) -> None:
        rows = sim.exhaustive_enumeration(sim.APPROVAL_POLICY, 4)
        rows += sim.exhaustive_enumeration(sim.DISCLOSURE_POLICY, 4)
        sim.validate_expected_results(
            {
                "enumeration": rows,
                "adversarial": sim.adversarial_trace_rows(),
            },
            quick=True,
        )


if __name__ == "__main__":
    unittest.main()
