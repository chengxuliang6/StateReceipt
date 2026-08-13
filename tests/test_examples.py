from pathlib import Path
import yaml
from statereceipt.schema import schema_errors
from statereceipt.semantic import semantic_errors

def test_examples_conform():
    root=Path(__file__).parents[1]/"examples"
    for p in root.glob("*.yaml"):
        d=yaml.safe_load(p.read_text())
        assert schema_errors(d) == [], p
        assert semantic_errors(d) == [], p
