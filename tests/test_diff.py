from statereceipt.diffing import diff_receipts

def mk(rid,digest):
    return {"receipt":{"id":rid},"work":{"state":"in_progress"},"snapshot":{"artifacts":[{"id":"a","path":"x","digest":{"algorithm":"sha256","value":digest}}]},"claims":[]}

def test_diff_changed_artifact():
    d=diff_receipts(mk("a","1"),mk("b","2"))
    assert d["artifacts"]["changed"] == ["a"]
