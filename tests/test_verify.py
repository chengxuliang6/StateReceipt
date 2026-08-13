from pathlib import Path
import hashlib
from statereceipt.verify import verify, _evaluate_claim


def sha(s: bytes):
    return hashlib.sha256(s).hexdigest()


def doc_for(path="a.txt", digest=None):
    return {
        "spec": {"name": "StateReceipt", "version": "0.1"},
        "receipt": {"id": "sr1", "created_at": "2026-08-13T00:00:00Z", "producer": {"type": "human", "name": "tester"}},
        "work": {"id": "w1", "objective": "test", "state": "in_progress"},
        "snapshot": {"artifacts": [{"id": "a1", "path": path, "digest": {"algorithm": "sha256", "value": digest}}]},
        "claims": [{
            "id": "c1",
            "kind": "observation",
            "statement": "file captured",
            "source": {"type": "tool"},
            "verification": {"status": "supported"},
            "supported_by": ["e1"],
            "depends_on": {"artifacts": ["a1"]},
        }],
        "evidence": [{"id": "e1", "type": "artifact", "strength": "checkable", "artifact_ref": "a1"}],
        "continuation": {"next_actions": [], "unresolved": []},
    }


def test_valid_artifact_supported(tmp_path: Path):
    p = tmp_path / "a.txt"
    p.write_bytes(b"hello")
    r = verify(doc_for(digest=sha(b"hello")), tmp_path)
    assert r["valid"] is True
    assert r["claims"]["c1"] == "supported"


def test_changed_artifact_makes_claim_stale(tmp_path: Path):
    p = tmp_path / "a.txt"
    p.write_bytes(b"changed")
    r = verify(doc_for(digest=sha(b"hello")), tmp_path)
    assert r["valid"] is True
    assert r["claims"]["c1"] == "stale"


def claim(**overrides):
    value = {
        "id": "c1",
        "kind": "observation",
        "statement": "state",
        "source": {"type": "agent"},
        "verification": {"status": "unknown"},
    }
    value.update(overrides)
    return value


def test_valid_contradiction_has_highest_precedence():
    c = claim(
        supported_by=["support"],
        contradicted_by=["contra"],
        depends_on={"artifacts": ["a1"]},
    )
    result = _evaluate_claim(c, {"a1": "stale"}, {"support": "valid", "contra": "valid"})
    assert result == "contradicted"


def test_explicit_stale_dependency_overrides_valid_support():
    c = claim(supported_by=["support"], depends_on={"artifacts": ["a1"]})
    result = _evaluate_claim(c, {"a1": "stale"}, {"support": "valid"})
    assert result == "stale"


def test_one_valid_support_is_enough_when_no_dependency_is_stale():
    c = claim(supported_by=["fresh", "old"])
    result = _evaluate_claim(c, {}, {"fresh": "valid", "old": "stale"})
    assert result == "supported"


def test_all_invalidated_supports_make_claim_stale():
    c = claim(supported_by=["old", "failed"])
    result = _evaluate_claim(c, {}, {"old": "stale", "failed": "invalid"})
    assert result == "stale"


def test_unknown_support_prevents_stale_conclusion():
    c = claim(supported_by=["old", "uncertain"])
    result = _evaluate_claim(c, {}, {"old": "stale", "uncertain": "unknown"})
    assert result == "unknown"


def test_no_support_references_is_unsupported():
    assert _evaluate_claim(claim(), {}, {}) == "unsupported"


def test_stale_evidence_dependency_marks_claim_stale():
    c = claim(depends_on={"evidence": ["e1"]})
    assert _evaluate_claim(c, {}, {"e1": "stale"}) == "stale"
