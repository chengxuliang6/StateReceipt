# StateReceipt

**Machine-verifiable point-in-time receipts for AI-assisted work state.**

**Languages:** English | [简体中文](docs/README.zh-CN.md) | [Español](docs/README.es.md)

StateReceipt is an open, vendor-neutral specification and Python reference CLI for recording claims about a work unit together with explicit evidence, artifact snapshots, validity dependencies, and deterministic freshness checks.

The motivating question is narrow: **when an AI-assisted task is interrupted or continued elsewhere, which claims about the work are still supported by the current artifacts?**

## Why StateReceipt?

A prose handoff can say “tests pass” or “the implementation is complete,” but the next engineer or agent may have no deterministic way to know whether that statement still applies after files change. StateReceipt represents the claim, the evidence explicitly bound to it, and the snapshot on which that evidence depended.

```text
Claim ──supported_by──> Evidence ──depends_on──> Artifact digest
  ^                                            |
  |---------------- freshness ----------------|
```

If a depended-on artifact changes, supporting evidence can become stale and the affected claim can require re-evaluation. In StateReceipt, **stale does not mean false**.

## What StateReceipt is not

StateReceipt is not a memory database, RAG system, chat-history sync format, agent runtime, orchestrator, scheduler, or replacement for Git/CI. The deterministic verifier does not ask an LLM to decide whether arbitrary natural-language evidence is logically true.

## Install for development

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## CLI

```bash
statereceipt init
statereceipt capture src/app.py tests/test_app.py --work-id AUTH-17 --objective "Implement auth middleware"
statereceipt validate .statereceipt/receipts/receipt.yaml
statereceipt verify .statereceipt/receipts/receipt.yaml
statereceipt verify .statereceipt/receipts/receipt.yaml --replay
statereceipt inspect .statereceipt/receipts/receipt.yaml
statereceipt diff old.yaml new.yaml
```

## v0.1 capabilities

- Draft 2020-12 JSON Schema validation.
- Semantic/reference integrity validation.
- SHA-256/SHA-512 artifact integrity checks.
- Git commit capture/checking.
- Explicit claim/evidence binding.
- Artifact-driven staleness detection.
- Deterministic claim evaluation.
- Optional replay of reproducible command/test evidence.
- Receipt inspection and diffing.

## Example domains

The same v0.1 schema is exercised against three deliberately different workflows:

- Python software development: `examples/python-auth.yaml`
- FPGA/Verilog engineering: `examples/fpga-verilog.yaml`
- MATLAB/research simulation: `examples/matlab-qpsk.yaml`

## Specification

Normative semantics live in [`spec/SPEC.md`](spec/SPEC.md). The machine-readable schema is [`spec/statereceipt-v0.1.schema.json`](spec/statereceipt-v0.1.schema.json).

The English specification is the normative source for v0.1. Translated documentation is provided for accessibility; if a translation conflicts with `spec/SPEC.md`, the English normative text controls.

The specification uses RFC-style `MUST`, `SHOULD`, and `MAY` language. StateReceipt v0.1 intentionally does not define a cryptographic signing envelope; future authentication should reuse established attestation mechanisms rather than inventing bespoke cryptography.

## Project provenance and related work

StateReceipt was designed after a prior-art review specifically to avoid presenting established concepts such as agent handoffs, persistent memory, artifact digests, generic attestations, or evidence-backed assertions as new inventions.

See [`DESIGN_PROVENANCE.md`](DESIGN_PROVENANCE.md) and [`PRIOR_ART.md`](PRIOR_ART.md) for the development boundary and related-work record.

## Contributing and security

See [`CONTRIBUTING.md`](CONTRIBUTING.md) before proposing implementation or specification changes. See [`SECURITY.md`](SECURITY.md) before replaying receipts from untrusted sources or reporting a vulnerability.

## License

Apache-2.0. See [`LICENSE`](LICENSE).
