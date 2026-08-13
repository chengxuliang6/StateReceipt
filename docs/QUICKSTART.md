# StateReceipt 5-minute Quick Start

[简体中文](QUICKSTART.zh-CN.md) | [Español](QUICKSTART.es.md)

This walkthrough demonstrates the core StateReceipt behavior without any LLM API: a claim is initially `supported`, then becomes `stale` after the artifact it depends on changes.

## 1. Install the development version

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## 2. Create a tiny work artifact

The same command works on Windows, macOS, and Linux:

```bash
python -c "from pathlib import Path; Path('quickstart-demo.txt').write_text('version 1\n', encoding='utf-8')"
```

## 3. Initialize and capture a receipt

```bash
statereceipt init
statereceipt capture quickstart-demo.txt --work-id DEMO-1 --objective "Track a tiny artifact"
```

StateReceipt writes the receipt to:

```text
.statereceipt/receipts/receipt.yaml
```

The generated receipt contains an artifact digest, artifact evidence, a claim about the captured state, and explicit validity dependencies.

## 4. Verify the unchanged artifact

```bash
statereceipt verify .statereceipt/receipts/receipt.yaml
```

The claim result should include:

```text
claim-capture: supported
```

Why? The current file still matches the digest captured in the receipt, so its evidence remains valid.

## 5. Change the artifact

```bash
python -c "from pathlib import Path; Path('quickstart-demo.txt').write_text('version 2\n', encoding='utf-8')"
```

Now the file no longer matches the point-in-time snapshot stored in the receipt.

## 6. Verify again

```bash
statereceipt verify .statereceipt/receipts/receipt.yaml
```

The claim should now include:

```text
claim-capture: stale
```

`stale` does **not** mean the claim is false. It means the evidence captured earlier can no longer be relied on for the current artifact state.

## What just happened?

```text
T0
quickstart-demo.txt digest = A
        ↓
artifact evidence valid
        ↓
claim-capture = supported

T1
quickstart-demo.txt digest = B
        ↓
captured dependency invalidated
        ↓
claim-capture = stale
```

That distinction is the core idea behind StateReceipt: work-state claims are tied to explicit evidence and point-in-time artifacts rather than trusted as free-form handoff prose.

## Cleanup

```bash
python -c "from pathlib import Path; p=Path('quickstart-demo.txt'); p.unlink() if p.exists() else None"
```

You may also remove `.statereceipt/` after the demo.
