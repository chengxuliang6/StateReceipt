from __future__ import annotations
from pathlib import Path
import json
import typer
from rich.console import Console
from rich.table import Table
from .capture import capture_receipt
from .diffing import diff_receipts
from .io import load_receipt, dump_receipt
from .lifecycle import validate_chain
from .schema import schema_errors
from .semantic import semantic_errors
from .verify import verify as verify_doc

app = typer.Typer(help="StateReceipt v0.1 reference CLI")
console = Console()

@app.command()
def init(path: Path = typer.Argument(Path("."))):
    d = path / ".statereceipt"
    d.mkdir(parents=True, exist_ok=True)
    (d / "receipts").mkdir(exist_ok=True)
    console.print(f"Initialized [bold]{d}[/bold]")

@app.command()
def capture(
    artifacts: list[Path] = typer.Argument(..., help="Artifact paths to capture"),
    output: Path = typer.Option(Path(".statereceipt/receipts/receipt.yaml"), "--output", "-o"),
    work_id: str = typer.Option(..., "--work-id"),
    objective: str = typer.Option(..., "--objective"),
    state: str = typer.Option("in_progress", "--state"),
    producer: str = typer.Option("human", "--producer"),
    producer_type: str = typer.Option("human", "--producer-type"),
    root: Path = typer.Option(Path("."), "--root"),
    predecessor: str | None = typer.Option(None, "--predecessor"),
):
    root = root.resolve()
    resolved = [(root / p).resolve() if not p.is_absolute() else p.resolve() for p in artifacts]
    missing = [str(p) for p in resolved if not p.is_file()]
    if missing:
        raise typer.BadParameter(f"missing artifact(s): {', '.join(missing)}")
    doc = capture_receipt(root, work_id, objective, state, producer, producer_type, resolved, predecessor)
    out = output if output.is_absolute() else root / output
    dump_receipt(doc, out)
    console.print(f"Captured [bold]{doc['receipt']['id']}[/bold] -> {out}")

@app.command(name="validate")
def validate_cmd(receipt: Path):
    doc = load_receipt(receipt)
    errs = schema_errors(doc) + semantic_errors(doc)
    if errs:
        for e in errs:
            console.print(f"[red]ERR[/red] {e}")
        raise typer.Exit(1)
    console.print("[green]OK[/green] schema and references valid")

@app.command(name="validate-chain")
def validate_chain_cmd(receipts: list[Path] = typer.Argument(..., help="Receipt files to validate as a local lifecycle set"), json_output: bool = typer.Option(False, "--json")):
    docs = []
    errors: list[str] = []
    for path in receipts:
        doc = load_receipt(path)
        per_receipt = schema_errors(doc) + semantic_errors(doc)
        if per_receipt:
            errors.extend(f"{path}: {err}" for err in per_receipt)
        docs.append(doc)

    result = validate_chain(docs) if not errors else {
        "valid": False,
        "errors": errors,
        "unresolved_predecessors": [],
        "receipt_count": len(docs),
    }
    if json_output:
        console.print_json(json.dumps(result))
    else:
        for err in result["errors"]:
            console.print(f"[red]ERR[/red] {err}")
        for item in result["unresolved_predecessors"]:
            console.print(f"[yellow]WARN[/yellow] {item['receipt']}: predecessor {item['predecessor']} is external or not in this validation set")
        if result["valid"]:
            console.print(f"[green]OK[/green] lifecycle set valid ({result['receipt_count']} receipts)")
    if not result["valid"]:
        raise typer.Exit(1)

@app.command()
def verify(
    receipt: Path,
    root: Path = typer.Option(Path("."), "--root"),
    replay: bool = typer.Option(
        False,
        "--replay",
        help="Request replay of reproducible evidence. Requires --trust-receipt.",
    ),
    trust_receipt: bool = typer.Option(
        False,
        "--trust-receipt",
        help="Acknowledge that replay commands in this receipt may execute arbitrary programs. Does not provide sandboxing or authenticate the producer.",
    ),
    json_output: bool = typer.Option(False, "--json"),
):
    if trust_receipt and not replay:
        console.print("[yellow]WARN[/yellow] --trust-receipt has no effect without --replay")
    if replay and not trust_receipt:
        console.print(
            "[red]ERR[/red] replay refused: receipt commands are untrusted executable input. "
            "Review the receipt and pass --trust-receipt only if you accept the execution risk."
        )
        console.print(
            "StateReceipt does not sandbox replayed commands and does not authenticate the receipt producer."
        )
        raise typer.Exit(2)

    result = verify_doc(load_receipt(receipt), root.resolve(), replay=replay and trust_receipt)
    if json_output:
        console.print_json(json.dumps(result))
    else:
        for c in result["checks"]:
            mark = "OK" if c["status"] == "pass" else ("SKIP" if c["status"] == "skip" else "ERR")
            console.print(f"{mark:4} {c['level']:9} {c['subject']}: {c['message']}")
        if result["claims"]:
            console.print("\nClaims:")
            for cid, status in result["claims"].items():
                console.print(f"  {cid}: {status}")
    if not result["valid"]:
        raise typer.Exit(1)

@app.command()
def inspect(receipt: Path):
    d = load_receipt(receipt)
    t = Table(title=f"StateReceipt {d['receipt']['id']}")
    t.add_column("Field")
    t.add_column("Value")
    t.add_row("Work", d["work"]["id"])
    t.add_row("State", d["work"]["state"])
    t.add_row("Producer", f"{d['receipt']['producer']['type']}:{d['receipt']['producer']['name']}")
    t.add_row("Artifacts", str(len(d["snapshot"]["artifacts"])))
    t.add_row("Claims", str(len(d["claims"])))
    t.add_row("Evidence", str(len(d["evidence"])))
    t.add_row("Next actions", str(len(d["continuation"]["next_actions"])))
    console.print(t)
    console.print(d["work"]["objective"])

@app.command(name="diff")
def diff_cmd(receipt_a: Path, receipt_b: Path):
    console.print_json(json.dumps(diff_receipts(load_receipt(receipt_a), load_receipt(receipt_b))))

if __name__ == "__main__":
    app()
