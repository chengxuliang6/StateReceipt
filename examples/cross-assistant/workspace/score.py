def normalize_score(value: int) -> int:
    """Clamp an integer score into the inclusive 0..100 range."""
    return max(0, min(100, value))
