from __future__ import annotations


def predecessor_id(doc: dict) -> str | None:
    return doc.get("receipt", {}).get("predecessor", {}).get("id")


def direct_relation(a: dict, b: dict) -> str:
    """Return the directly observable lifecycle relation between two receipts."""
    aid = a["receipt"]["id"]
    bid = b["receipt"]["id"]
    if aid == bid:
        return "same_receipt"
    if predecessor_id(b) == aid:
        return "direct_successor"
    if predecessor_id(a) == bid:
        return "direct_predecessor"
    return "not_directly_linked"


def validate_chain(receipts: list[dict]) -> dict:
    """Validate lifecycle properties detectable from a local receipt set.

    Missing predecessors are reported as external/unresolved references rather than
    errors because v0.1 predecessor IDs are opaque and may refer to receipts that
    are not present in the current validation set.
    """
    errors: list[str] = []
    unresolved: list[dict[str, str]] = []

    ids = [doc.get("receipt", {}).get("id") for doc in receipts]
    seen: set[str] = set()
    duplicates: set[str] = set()
    for rid in ids:
        if rid in seen:
            duplicates.add(rid)
        seen.add(rid)
    for rid in sorted(duplicates):
        errors.append(f"duplicate receipt id in chain set: {rid}")

    # Only unique IDs can participate in deterministic local graph validation.
    by_id = {doc["receipt"]["id"]: doc for doc in receipts if doc.get("receipt", {}).get("id") not in duplicates}

    for rid, doc in by_id.items():
        pred = predecessor_id(doc)
        if pred is None:
            continue
        if pred == rid:
            errors.append(f"receipt {rid}: predecessor self-reference")
        elif pred not in by_id:
            unresolved.append({"receipt": rid, "predecessor": pred})

    # Detect cycles among locally resolvable predecessor edges.
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(rid: str, stack: list[str]) -> None:
        if rid in visited:
            return
        if rid in visiting:
            start = stack.index(rid) if rid in stack else 0
            cycle = stack[start:] + [rid]
            errors.append("predecessor cycle: " + " -> ".join(cycle))
            return
        visiting.add(rid)
        stack.append(rid)
        pred = predecessor_id(by_id[rid])
        if pred in by_id and pred != rid:
            walk(pred, stack)
        stack.pop()
        visiting.remove(rid)
        visited.add(rid)

    for rid in sorted(by_id):
        if rid not in visited:
            walk(rid, [])

    return {
        "valid": not errors,
        "errors": errors,
        "unresolved_predecessors": sorted(unresolved, key=lambda x: (x["receipt"], x["predecessor"])),
        "receipt_count": len(receipts),
    }
