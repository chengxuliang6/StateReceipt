from pathlib import Path
import shutil
import subprocess
import sys

from typer.testing import CliRunner

from statereceipt.cli import app


runner = CliRunner()
ROOT = Path(__file__).resolve().parents[1]
SOURCE_LAB = ROOT / "examples" / "cross-assistant"


def _run_helper(path: Path) -> None:
    cp = subprocess.run([sys.executable, str(path)], check=False, capture_output=True, text=True)
    assert cp.returncode == 0, cp.stderr


def test_cross_assistant_receipt_changes_receiver_decision(tmp_path: Path):
    lab = tmp_path / "cross-assistant"
    shutil.copytree(SOURCE_LAB, lab)

    _run_helper(lab / "reset_stage_a.py")

    result = runner.invoke(app, ["verify", str(lab / "stage-a.yaml"), "--root", str(lab)])
    assert result.exit_code == 0, result.stdout
    assert "claim-clamp-behavior: supported" in result.stdout
    assert "claim-tests-pass: supported" in result.stdout

    _run_helper(lab / "mutate_after_handoff.py")

    result = runner.invoke(app, ["verify", str(lab / "stage-a.yaml"), "--root", str(lab)])
    assert result.exit_code == 0, result.stdout
    assert "claim-clamp-behavior: stale" in result.stdout
    assert "claim-tests-pass: stale" in result.stdout
