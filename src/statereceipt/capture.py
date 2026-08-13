from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import mimetypes
import secrets
from .hashing import digest_file
from .git import git_snapshot


def artifact_descriptor(path: Path, root: Path, idx: int) -> dict:
    rel = path.resolve().relative_to(root.resolve()).as_posix()
    media, _ = mimetypes.guess_type(path.name)
    return {
        "id": f"artifact-{idx:03d}",
        "path": rel,
        **({"media_type": media} if media else {}),
        "digest": {"algorithm": "sha256", "value": digest_file(path, "sha256")},
    }


def capture_receipt(root: Path, work_id: str, objective: str, work_state: str, producer_name: str, producer_type: str, artifacts: list[Path], predecessor: str | None = None) -> dict:
    desc = [artifact_descriptor(p, root, i+1) for i,p in enumerate(artifacts)]
    receipt = {
        "id": f"sr_{secrets.token_hex(6)}",
        "created_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "producer": {"type": producer_type, "name": producer_name},
    }
    if predecessor:
        receipt["predecessor"] = {"id": predecessor}
    snapshot = {"artifacts": desc}
    repo = git_snapshot(root)
    if repo:
        snapshot["repository"] = repo
    evidence = [
        {
            "id": f"evidence-{a['id']}",
            "type": "artifact",
            "strength": "checkable",
            "artifact_ref": a["id"],
        }
        for a in desc
    ]
    return {
        "spec": {"name": "StateReceipt", "version": "0.1"},
        "receipt": receipt,
        "work": {"id": work_id, "objective": objective, "state": work_state},
        "snapshot": snapshot,
        "claims": [{
            "id": "claim-capture",
            "kind": "observation",
            "statement": "The listed artifacts were captured at receipt creation time.",
            "source": {"type": "tool", "ref": "statereceipt capture"},
            "verification": {"status": "supported"},
            "supported_by": [e["id"] for e in evidence],
            "depends_on": {
                "artifacts": [x["id"] for x in desc],
                "evidence": [e["id"] for e in evidence],
            },
        }],
        "evidence": evidence,
        "continuation": {"next_actions": [], "unresolved": []},
    }
