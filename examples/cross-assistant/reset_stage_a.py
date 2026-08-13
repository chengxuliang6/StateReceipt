from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCORE = ROOT / "workspace" / "score.py"
TESTS = ROOT / "tests" / "test_score.py"

STAGE_A_SCORE = '''def normalize_score(value: int) -> int:
    """Clamp an integer score into the inclusive 0..100 range."""
    return max(0, min(100, value))
'''

STAGE_A_TESTS = '''import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from workspace.score import normalize_score


class NormalizeScoreTests(unittest.TestCase):
    def test_clamps_low(self):
        self.assertEqual(normalize_score(-3), 0)

    def test_keeps_middle_value(self):
        self.assertEqual(normalize_score(42), 42)

    def test_clamps_high(self):
        self.assertEqual(normalize_score(120), 100)


if __name__ == "__main__":
    unittest.main()
'''

SCORE.write_text(STAGE_A_SCORE, encoding="utf-8", newline="\n")
TESTS.write_text(STAGE_A_TESTS, encoding="utf-8", newline="\n")
print("Reset workspace/score.py and tests/test_score.py to the exact Stage A byte snapshot")
