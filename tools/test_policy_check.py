"""policy_check.merge의 시험. 실행: python -m unittest tools/test_policy_check.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from policy_check import merge  # noqa: E402

TENANT = {
    "version": 1,
    "allowed_models": ["m-a", "m-b"],
    "blocked_data_classes": ["실데이터", "개인정보"],
    "cost_caps": {"max_tokens_per_run": 200000},
    "gate_floors": {"risk_a": 2, "release": 2},
    "retention": {"실행 증명": {"floor_days": 365, "ceiling_days": 1825}},
    "identity": "github-app",
}


class MergeTest(unittest.TestCase):
    def test_stricter_domain_passes(self):
        d = {"allowed_models": ["m-a"], "cost_caps": {"max_tokens_per_run": 100000},
             "gate_floors": {"risk_a": 3}, "agents": {"enabled": False}}
        errors, table = merge(TENANT, d)
        self.assertEqual(errors, [])
        self.assertIn(("allowed_models", ["m-a"], "domain"), table)
        self.assertIn(("gate_floors.risk_a", 3, "domain"), table)
        self.assertIn(("gate_floors.release", 2, "tenant"), table)

    def test_looser_values_fail(self):
        d = {"allowed_models": ["m-c"], "blocked_data_classes": ["실데이터"],
             "cost_caps": {"max_tokens_per_run": 999999}, "gate_floors": {"risk_a": 1}}
        errors, _ = merge(TENANT, d)
        self.assertEqual(len(errors), 4)

    def test_unknown_key_fails(self):
        errors, _ = merge(TENANT, {"new_policy": True})
        self.assertTrue(any("모르는 키" in e for e in errors))

    def test_tenant_only_value(self):
        errors, _ = merge(TENANT, {"identity": "other"})
        self.assertTrue(any("테넌트만" in e for e in errors))

    def test_retention_floor_needs_basis_and_must_not_exceed_ceiling(self):
        d = {"retention": {"실행 증명": {"floor_days": 3650}}}
        errors, _ = merge(TENANT, d)
        self.assertTrue(any("근거" in e for e in errors))
        self.assertTrue(any("바닥 3650일 > 천장 1825일" in e for e in errors))

    def test_retention_raised_with_basis_ok(self):
        d = {"retention": {"실행 증명": {"floor_days": 1000, "basis": "법령 X조"}}}
        errors, table = merge(TENANT, d)
        self.assertEqual(errors, [])
        self.assertIn(("retention.실행 증명", {"floor_days": 1000, "ceiling_days": 1825}, "tenant+domain"), table)


if __name__ == "__main__":
    unittest.main()
