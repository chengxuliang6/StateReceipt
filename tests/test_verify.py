from pathlib import Path
import hashlib
from statereceipt.verify import verify

def sha(s: bytes): return hashlib.sha256(s).hexdigest()

def doc_for(path="a.txt", digest=None):
    return {
      "spec":{"name":"StateReceipt","version":"0.1"},
      "receipt":{"id":"sr1","created_at":"2026-08-13T00:00:00Z","producer":{"type":"human","name":"tester"}},
      "work":{"id":"w1","objective":"test","state":"in_progress"},
      "snapshot":{"artifacts":[{"id":"a1","path":path,"digest":{"algorithm":"sha256","value":digest}}]},
      "claims":[{"id":"c1","kind":"observation","statement":"file captured","source":{"type":"tool"},"verification":{"status":"supported"},"supported_by":["e1"],"depends_on":{"artifacts":["a1"]}}],
      "evidence":[{"id":"e1","type":"artifact","strength":"checkable","artifact_ref":"a1"}],
      "continuation":{"next_actions":[],"unresolved":[]}
    }

def test_valid_artifact_supported(tmp_path: Path):
    p=tmp_path/"a.txt"; p.write_bytes(b"hello")
    r=verify(doc_for(digest=sha(b"hello")), tmp_path)
    assert r["valid"] is True
    assert r["claims"]["c1"] == "supported"

def test_changed_artifact_makes_claim_stale(tmp_path: Path):
    p=tmp_path/"a.txt"; p.write_bytes(b"changed")
    r=verify(doc_for(digest=sha(b"hello")), tmp_path)
    assert r["valid"] is True
    assert r["claims"]["c1"] == "stale"
