from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from typer.testing import CliRunner

from statereceipt.cli import app
from statereceipt.io import dump_receipt


runner = CliRunner()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _replay_receipt(tmp_path: Path) -> Path:
    artifact = tmp_path / "artifact.txt"
    artifact.write_bytes(b"captured\n")

    receipt = {
        "spec": {"name": "StateReceipt", "version": "0.1"},
        "receipt": {
            "id": "sr-replay-safety",
            "created_at": "2026-08-13T00:00:00Z",
            "producer": {"type": "human", "name": "tester"},
        },
        "work": {"id": "SEC-1", "objective": "test replay trust", "state": "in_progress"},
        "snapshot": {
            "artifacts": [
                {
                    "id": "artifact-001",
                    "path": "artifact.txt",
                    "digest": {"algorithm": "sha256", "value": _sha256(b"captured\n")},
                }
            ]
        },
        "claims": [
            {
                "id": "claim-replay",
                "kind": "validation",
                "statement": "Replay command exits successfully.",
                "source": {"type": "tool"},
                "verification": {"status": "supported"},
                "supported_by": ["evidence-replay"],
            }
        ],
        "evidence": [
            {
                "id": "evidence-replay",
                "type": "command",
                "strength": "reproducible",
                "execution": {
                    "argv": [
                        sys.executable,
                        "-c",
                        "from pathlib import Path; Path('replay-marker.txt').write_text('executed', encoding='utf-8')",
                    ],
                    "cwd": ".",
                    "exit_code": 0,
                },
            }
        ],
        "continuation": {"next_actions": [], "unresolved": []},
    }

    path = tmp_path / "receipt.yaml"
    dump_receipt(receipt, path)
    return path


def test_default_verify_never_replays(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    receipt = _replay_receipt(tmp_path)

    result = runner.invoke(app, ["verify", str(receipt), "--root", str(tmp_path)])

    assert result.exit_code == 0, result.stdout
    assert not (tmp_path / "replay-marker.txt").exists()


def test_replay_without_trust_is_refused(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    receipt = _replay_receipt(tmp_path)

    result = runner.invoke(app, ["verify", str(receipt), "--root", str(tmp_path), "--replay"])

    assert result.exit_code == 2
    assert "replay refused" in result.stdout
    assert "--trust-receipt" in result.stdout
    assert not (tmp_path / "replay-marker.txt").exists()


def test_replay_runs_only_with_explicit_trust(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    receipt = _replay_receipt(tmp_path)

    result = runner.invoke(
        app,
        ["verify", str(receipt), "--root", str(tmp_path), "--replay", "--trust-receipt"],
    )

    assert result.exit_code == 0, result.stdout
    assert (tmp_path / "replay-marker.txt").read_text(encoding="utf-8") == "executed"
    assert "evidence-replay" in result.stdout


def test_trust_flag_without_replay_does_not_execute(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    receipt = _replay_receipt(tmp_path)

    result = runner.invoke(
        app,
        ["verify", str(receipt), "--root", str(tmp_path), "--trust-receipt"],
    )

    assert result.exit_code == 0, result.stdout
    assert "has no effect without --replay" in result.stdout
    assert not (tmp_path / "replay-marker.txt").exists()
