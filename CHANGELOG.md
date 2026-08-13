# Changelog

All notable changes to StateReceipt will be documented here.

The project follows semantic versioning where practical during the 0.x development series; incompatible specification changes may occur before 1.0 and will be called out explicitly.

## [0.1.0] - 2026-08-13

First public milestone: StateReceipt v0.1 specification draft and Python reference implementation.

### Specification and model

- StateReceipt v0.1 draft specification using RFC-style normative language.
- Draft 2020-12 JSON Schema for point-in-time work-state Receipts.
- Explicit Claim–Evidence bindings and artifact digest snapshots.
- Deterministic Claim evaluation with ordered `contradicted`, `stale`, `supported`, `unknown`, and `unsupported` semantics.
- Explicit rule that `stale` means prior support can no longer be relied upon for the current snapshot; it does not mean a Claim is false.
- Immutable Receipt lifecycle semantics using optional `receipt.predecessor.id`.
- Local predecessor-chain validation for duplicate Receipt IDs, self-reference, cycles, and external/unresolved predecessors.

### Reference CLI

- `statereceipt init`
- `statereceipt capture`
- `statereceipt validate`
- `statereceipt validate-chain`
- `statereceipt verify`
- `statereceipt inspect`
- `statereceipt diff`
- SHA-256/SHA-512 artifact integrity checks.
- Git snapshot capture and commit existence checks.
- Semantic/reference integrity validation.
- Artifact-driven staleness detection and lifecycle-aware diff output.

### Replay security

- Verification is non-executing by default.
- `--replay` alone is refused before command execution.
- Reproducible command/test evidence executes only when both `--replay --trust-receipt` are supplied.
- `--trust-receipt` is documented as an execution-risk acknowledgement, not producer authentication, a signature check, or a sandbox guarantee.
- Replay safety regression tests cover default non-execution and explicit opt-in behavior.

### Documentation and accessibility

- First-party documentation entry points in English, Simplified Chinese, and Spanish.
- Five-minute cross-platform Quick Start demonstrating `supported -> artifact change -> stale` without an LLM API.
- Lifecycle/predecessor guides in all three languages.
- Replay security guidance in all three languages.
- Optional in-toto Statement / DSSE interoperability profile in all three languages.
- `DESIGN_PROVENANCE.md`, `PRIOR_ART.md`, `THIRD_PARTY_NOTICES.md`, contribution and security policies.

### Interoperability

- Exploratory, optional mapping of a complete StateReceipt document into an in-toto Statement predicate.
- `snapshot.artifacts` can be projected into in-toto subjects by artifact ID and digest.
- Optional authenticity is layered through existing DSSE implementations rather than bespoke StateReceipt cryptography.
- Unsigned local YAML/JSON Receipts remain fully conforming and first-class.
- No claim that a cryptographic signature proves Claim truth or work correctness.

### Examples and verification

- Python software-development example Receipt.
- FPGA/Verilog engineering example Receipt.
- MATLAB/research simulation example Receipt.
- End-to-end Quick Start regression coverage.
- Linux, Windows, and macOS CI across Python 3.11, 3.12, and 3.13.
- Release-package CI that builds both wheel and sdist, installs each into a fresh virtual environment, exercises the installed CLI, and verifies packaged JSON Schema resources.
- Automated consistency checks for Python package version and repository/packaged schema equality.

### Explicit non-goals for v0.1.0

StateReceipt v0.1.0 is not a persistent AI memory system, RAG database, chat synchronization format, agent orchestrator, task scheduler, sandbox, signature system, PKI, or proof that AI-generated natural-language Claims are true.
