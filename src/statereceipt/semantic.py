from __future__ import annotations


def semantic_errors(doc: dict) -> list[str]:
    errors: list[str] = []
    claims = doc.get("claims", [])
    evidence = doc.get("evidence", [])
    artifacts = doc.get("snapshot", {}).get("artifacts", [])

    receipt = doc.get("receipt", {})
    receipt_id = receipt.get("id")
    predecessor = receipt.get("predecessor", {}).get("id")
    if receipt_id is not None and predecessor == receipt_id:
        errors.append(f"receipt {receipt_id}: predecessor self-reference")

    claim_ids = [x.get("id") for x in claims]
    evidence_ids = [x.get("id") for x in evidence]
    artifact_ids = [x.get("id") for x in artifacts]

    for label, ids in (("claim", claim_ids), ("evidence", evidence_ids), ("artifact", artifact_ids)):
        seen = set()
        for x in ids:
            if x in seen:
                errors.append(f"duplicate {label} id: {x}")
            seen.add(x)

    evset, artset = set(evidence_ids), set(artifact_ids)
    for c in claims:
        cid = c.get("id", "<claim>")
        for field in ("supported_by", "contradicted_by"):
            for ref in c.get(field, []):
                if ref not in evset:
                    errors.append(f"{cid}: dangling {field} evidence reference: {ref}")
        dep = c.get("depends_on", {})
        for ref in dep.get("evidence", []):
            if ref not in evset:
                errors.append(f"{cid}: dangling evidence dependency: {ref}")
        for ref in dep.get("artifacts", []):
            if ref not in artset:
                errors.append(f"{cid}: dangling artifact dependency: {ref}")

    for e in evidence:
        eid = e.get("id", "<evidence>")
        if e.get("artifact_ref") and e["artifact_ref"] not in artset:
            errors.append(f"{eid}: dangling artifact_ref: {e['artifact_ref']}")
        if e.get("execution_ref") and e["execution_ref"] not in evset:
            errors.append(f"{eid}: dangling execution_ref: {e['execution_ref']}")
    return errors
