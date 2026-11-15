"""run_record_check.check의 시험. 실행: python -m unittest tools/test_run_record_check.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from run_record_check import check  # noqa: E402

OK = ("본문\n<!-- agentic-run: role=judge model=m-a skill=spec-check@abc1234 "
      "criteria=l4_criteria@def5678 head=1234567 actor=judge-app tokens_in=1 -->")


class RunRecordTest(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(check(OK, "writer-app", "l4_criteria@def5678"), ([], []))

    def test_missing_line(self):
        errors, _ = check("기록 없음", "writer-app")
        self.assertEqual(len(errors), 1)

    def test_missing_field(self):
        errors, _ = check(OK.replace("criteria=l4_criteria@def5678 ", ""), "writer-app")
        self.assertIn("빈 칸: criteria", errors)

    def test_actor_equals_author(self):
        errors, _ = check(OK, "judge-app")
        self.assertTrue(any("작성자와 같다" in e for e in errors))

    def test_criteria_version_warning_only(self):
        errors, warnings = check(OK, "writer-app", "l4_criteria@9999999")
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)


if __name__ == "__main__":
    unittest.main()
