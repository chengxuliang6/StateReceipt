from statereceipt.capture import capture_receipt
from statereceipt.verify import verify

def test_capture_minimum(tmp_path):
    p=tmp_path/"x.py"; p.write_text("print(1)")
    d=capture_receipt(tmp_path,"w","objective","in_progress","tester","human",[p])
    assert d["spec"]["version"] == "0.1"
    assert d["snapshot"]["artifacts"][0]["path"] == "x.py"
    assert d["claims"][0]["supported_by"] == ["evidence-artifact-001"]
    assert verify(d, tmp_path)["claims"]["claim-capture"] == "supported"
