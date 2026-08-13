from pathlib import Path

from typer.testing import CliRunner

from statereceipt.cli import app


runner = CliRunner()


def test_quickstart_supported_then_stale(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    artifact = tmp_path / "quickstart-demo.txt"
    artifact.write_text("version 1\n", encoding="utf-8")

    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0, result.stdout

    result = runner.invoke(
        app,
        [
            "capture",
            "quickstart-demo.txt",
            "--work-id",
            "DEMO-1",
            "--objective",
            "Track a tiny artifact",
        ],
    )
    assert result.exit_code == 0, result.stdout

    receipt = ".statereceipt/receipts/receipt.yaml"

    result = runner.invoke(app, ["verify", receipt])
    assert result.exit_code == 0, result.stdout
    assert "claim-capture: supported" in result.stdout

    artifact.write_text("version 2\n", encoding="utf-8")

    result = runner.invoke(app, ["verify", receipt])
    assert result.exit_code == 0, result.stdout
    assert "claim-capture: stale" in result.stdout
