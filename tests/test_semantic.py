from statereceipt.semantic import semantic_errors

def test_dangling_evidence_detected():
    doc={"claims":[{"id":"c1","supported_by":["missing"]}],"evidence":[],"snapshot":{"artifacts":[]}}
    assert any("dangling" in x for x in semantic_errors(doc))
