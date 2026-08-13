from __future__ import annotations

def diff_receipts(a: dict, b: dict) -> dict:
    aa = {x["id"]: x for x in a["snapshot"]["artifacts"]}
    bb = {x["id"]: x for x in b["snapshot"]["artifacts"]}
    added = sorted(set(bb)-set(aa))
    removed = sorted(set(aa)-set(bb))
    changed = sorted(k for k in set(aa)&set(bb) if aa[k]["digest"] != bb[k]["digest"] or aa[k]["path"] != bb[k]["path"])
    ca = {x["id"]: x for x in a["claims"]}
    cb = {x["id"]: x for x in b["claims"]}
    claim_added = sorted(set(cb)-set(ca))
    claim_removed = sorted(set(ca)-set(cb))
    claim_changed = sorted(k for k in set(ca)&set(cb) if ca[k] != cb[k])
    return {
        "receipt_from": a["receipt"]["id"],
        "receipt_to": b["receipt"]["id"],
        "artifacts": {"added": added, "removed": removed, "changed": changed},
        "claims": {"added": claim_added, "removed": claim_removed, "changed": claim_changed},
        "work_state": {"from": a["work"]["state"], "to": b["work"]["state"]},
    }
