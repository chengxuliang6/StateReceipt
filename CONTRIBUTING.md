# Contributing to StateReceipt

Thank you for helping improve StateReceipt.

## Development principles

StateReceipt is intentionally narrow. Contributions should preserve these constraints:

- deterministic core verification;
- no LLM-based truth adjudication in the core verifier;
- point-in-time receipts rather than mutable agent memory;
- explicit claim/evidence references;
- `stale` is not equivalent to `false`;
- no bespoke cryptographic envelope in the core specification.

## Development setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Before opening a pull request

1. Add or update tests for behavior changes.
2. Run `pytest` locally.
3. If the schema changes, update both copies of the v0.1 schema and add cross-domain examples where appropriate.
4. If normative semantics change, update `spec/SPEC.md` and explain compatibility impact in the PR.
5. Do not copy implementation text, source code, schemas, prompts, or tests from related projects unless the license and attribution requirements are reviewed and documented.

## Specification changes

Changes to normative semantics should be proposed in an issue before implementation. A proposal should state:

- the problem;
- the proposed semantic change;
- compatibility impact;
- verifier impact;
- at least one concrete receipt example.

## Commit and PR guidance

Prefer small, reviewable commits. PR descriptions should explain what changed, why it is needed, and how it was validated.
