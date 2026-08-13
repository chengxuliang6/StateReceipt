import sys
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
