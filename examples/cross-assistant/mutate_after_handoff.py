from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "workspace" / "score.py"

MUTATED = '''def normalize_score(value: int) -> int:
    """Clamp an integer score into the inclusive 0..100 range, then round down to a multiple of 5."""
    clamped = max(0, min(100, value))
    return clamped - (clamped % 5)
'''

TARGET.write_text(MUTATED, encoding="utf-8")
print(f"Mutated {TARGET.relative_to(ROOT)} after the Stage A handoff")
