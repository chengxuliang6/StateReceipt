from __future__ import annotations
from pathlib import Path
import subprocess


def _run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)


def git_snapshot(root: Path) -> dict | None:
    inside = _run(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return None
    head = _run(root, "rev-parse", "HEAD")
    if head.returncode != 0:
        return None
    status = _run(root, "status", "--porcelain")
    return {"vcs": "git", "commit": head.stdout.strip(), "dirty": bool(status.stdout.strip())}


def commit_exists(root: Path, commit: str) -> bool:
    cp = _run(root, "cat-file", "-e", f"{commit}^{{commit}}")
    return cp.returncode == 0
