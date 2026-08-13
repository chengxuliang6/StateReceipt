from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "workspace" / "score.py"

STAGE_A = '''def normalize_score(value: int) -> int:
    """Clamp an integer score into the inclusive 0..100 range."""
    return max(0, min(100, value))
'''

TARGET.write_text(STAGE_A, encoding="utf-8")
print(f"Reset {TARGET.relative_to(ROOT)} to the Stage A snapshot")
