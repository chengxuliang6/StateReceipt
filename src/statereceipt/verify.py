from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import subprocess
from .hashing import digest_file
from .git import commit_exists
from .schema import schema_errors
from .semantic import semantic_errors

@dataclass
class Check:
    level: str
    subject: str
    status: str
    message: str

    def as_dict(self):
        return asdict(self)


def _artifact_checks(doc: dict, root: Path) -> tuple[list[Check], dict[str, str]]:
    checks: list[Check] = []
    states: dict[str, str] = {}
    for a in doc["snapshot"]["artifacts"]:
        aid, rel = a["id"], a["path"]
        p = root / rel
        if not p.exists():
            states[aid] = "missing"
            checks.append(Check("integrity", aid, "fail", f"artifact missing: {rel}"))
            continue
        expected = a["digest"]["value"].lower()
        actual = digest_file(p, a["digest"]["algorithm"]).lower()
        if actual != expected:
            states[aid] = "stale"
            checks.append(Check("integrity", aid, "stale", f"digest changed: {rel}"))
        else:
            states[aid] = "valid"
            checks.append(Check("integrity", aid, "pass", f"digest matches: {rel}"))
    return checks, states


def _git_checks(doc: dict, root: Path) -> list[Check]:
    repo = doc.get("snapshot", {}).get("repository")
    if not repo:
        return []
    ok = commit_exists(root, repo["commit"])
    return [Check("integrity", "repository.commit", "pass" if ok else "fail", "captured commit exists" if ok else "captured commit not found")]


def _replay_evidence(e: dict, root: Path) -> Check:
    execution = e.get("execution")
    if not execution:
        return Check("replay", e["id"], "skip", "no inline execution to replay")
    cwd = root / execution.get("cwd", ".")
    try:
        cp = subprocess.run(execution["argv"], cwd=cwd, text=True, capture_output=True, check=False, timeout=120)
    except FileNotFoundError as ex:
        return Check("replay", e["id"], "fail", f"command not found: {ex.filename}")
    except subprocess.TimeoutExpired:
        return Check("replay", e["id"], "fail", "command timed out")
    expected = execution["exit_code"]
    if cp.returncode == expected:
        return Check("replay", e["id"], "pass", f"exit code {cp.returncode} matched")
    return Check("replay", e["id"], "fail", f"exit code {cp.returncode}, expected {expected}")


def verify(doc: dict, root: Path, replay: bool = False) -> dict:
    checks: list[Check] = []
    serr = schema_errors(doc)
    merr = semantic_errors(doc) if not serr else []
    for e in serr:
        checks.append(Check("schema", "$", "fail", e))
    for e in merr:
        checks.append(Check("schema", "$", "fail", e))
    if serr or merr:
        return {"valid": False, "checks": [c.as_dict() for c in checks], "claims": {}}
    checks.append(Check("schema", "$", "pass", "schema and references valid"))

    ac, artifact_state = _artifact_checks(doc, root)
    checks.extend(ac)
    checks.extend(_git_checks(doc, root))

    evidence_state: dict[str, str] = {}
    for e in doc["evidence"]:
        state = "valid"
        if e["type"] == "artifact":
            state = artifact_state.get(e["artifact_ref"], "unknown")
        if replay and e["strength"] == "reproducible":
            rc = _replay_evidence(e, root)
            checks.append(rc)
            if rc.status == "fail": state = "invalid"
        evidence_state[e["id"]] = state

    claim_results: dict[str, str] = {}
    for c in doc["claims"]:
        deps = c.get("depends_on", {})
        dep_art_states = [artifact_state.get(x, "unknown") for x in deps.get("artifacts", [])]
        if any(s in {"stale", "missing"} for s in dep_art_states):
            result = "stale"
        else:
            contrad = [evidence_state.get(x, "unknown") for x in c.get("contradicted_by", [])]
            supported = [evidence_state.get(x, "unknown") for x in c.get("supported_by", [])]
            if any(s == "valid" for s in contrad):
                result = "contradicted"
            elif supported and any(s == "valid" for s in supported):
                result = "supported"
            elif supported and all(s in {"stale", "missing", "invalid"} for s in supported):
                result = "stale"
            elif supported:
                result = "unknown"
            else:
                result = "unsupported"
        claim_results[c["id"]] = result
        checks.append(Check("claim", c["id"], "pass" if result in {"supported","unsupported","unknown"} else result, f"evaluated as {result}"))

    hard_fail = any(c.status == "fail" for c in checks)
    return {"valid": not hard_fail, "checks": [c.as_dict() for c in checks], "claims": claim_results}
