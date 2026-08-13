from __future__ import annotations

from statereceipt.diffing import diff_receipts
from statereceipt.lifecycle import direct_relation, validate_chain
from statereceipt.semantic import semantic_errors


def receipt(rid: str, predecessor: str | None = None, state: str = "in_progress") -> dict:
    r = {"id": rid, "created_at": "2026-08-13T00:00:00Z", "producer": {"type": "human", "name": "tester"}}
    if predecessor is not None:
        r["predecessor"] = {"id": predecessor}
    return {
        "spec": {"name": "StateReceipt", "version": "0.1"},
        "receipt": r,
        "work": {"id": "w1", "objective": "test lifecycle", "state": state},
        "snapshot": {"artifacts": [{"id": "a1", "path": "a.txt", "digest": {"algorithm": "sha256", "value": "00"}}]},
        "claims": [{"id": "c1", "kind": "observation", "statement": "state", "source": {"type": "human"}, "verification": {"status": "unsupported"}}],
        "evidence": [],
        "continuation": {"next_actions": [], "unresolved": []},
    }


def test_normal_three_receipt_chain_is_valid():
    a = receipt("SR-A", state="interrupted")
    b = receipt("SR-B", predecessor="SR-A", state="in_progress")
    c = receipt("SR-C", predecessor="SR-B", state="completed")

    result = validate_chain([a, b, c])

    assert result["valid"] is True
    assert result["errors"] == []
    assert result["unresolved_predecessors"] == []


def test_external_predecessor_is_reported_but_not_invalid():
    b = receipt("SR-B", predecessor="external-SR-A")

    result = validate_chain([b])

    assert result["valid"] is True
    assert result["unresolved_predecessors"] == [{"receipt": "SR-B", "predecessor": "external-SR-A"}]


def test_duplicate_receipt_id_is_invalid():
    result = validate_chain([receipt("SR-A"), receipt("SR-A")])

    assert result["valid"] is False
    assert "duplicate receipt id in chain set: SR-A" in result["errors"]


def test_self_reference_is_invalid_in_single_receipt_semantics():
    doc = receipt("SR-A", predecessor="SR-A")

    assert "receipt SR-A: predecessor self-reference" in semantic_errors(doc)


def test_local_cycle_is_invalid():
    a = receipt("SR-A", predecessor="SR-C")
    b = receipt("SR-B", predecessor="SR-A")
    c = receipt("SR-C", predecessor="SR-B")

    result = validate_chain([a, b, c])

    assert result["valid"] is False
    assert any(error.startswith("predecessor cycle:") for error in result["errors"])


def test_direct_relation_is_explicit_and_directional():
    a = receipt("SR-A")
    b = receipt("SR-B", predecessor="SR-A")
    x = receipt("SR-X")

    assert direct_relation(a, b) == "direct_successor"
    assert direct_relation(b, a) == "direct_predecessor"
    assert direct_relation(a, a) == "same_receipt"
    assert direct_relation(a, x) == "not_directly_linked"


def test_diff_reports_direct_successor_relation():
    a = receipt("SR-A", state="interrupted")
    b = receipt("SR-B", predecessor="SR-A", state="in_progress")

    result = diff_receipts(a, b)

    assert result["lifecycle_relation"] == "direct_successor"
    assert result["work_state"] == {"from": "interrupted", "to": "in_progress"}


def test_diff_does_not_assume_unlinked_receipts_are_related():
    result = diff_receipts(receipt("SR-A"), receipt("SR-Z"))

    assert result["lifecycle_relation"] == "not_directly_linked"
