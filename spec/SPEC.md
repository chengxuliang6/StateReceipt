# StateReceipt Specification v0.1

**Status:** Draft implementation baseline

StateReceipt is a machine-readable point-in-time record of claims about an AI-assisted work unit, the evidence supporting or contradicting those claims, the snapshot against which they were evaluated, and the continuation metadata needed to resume work safely.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in RFC 2119.

## 1. Scope

StateReceipt is an artifact specification. It is **not** a memory database, agent runtime, orchestrator, chat-history format, task scheduler, or replacement for Git/CI.

A StateReceipt:
- MUST describe exactly one point-in-time work state.
- MUST identify the work unit.
- MUST contain at least one artifact in the captured snapshot.
- MUST contain at least one claim.
- MAY contain reproducible evidence.
- SHOULD bind mutable artifacts by cryptographic digest.
- MUST NOT treat `stale` as equivalent to `false`.

## 2. Top-level objects

A v0.1 receipt MUST contain:
- `spec`
- `receipt`
- `work`
- `snapshot`
- `claims`
- `evidence`
- `continuation`

Unknown top-level properties are invalid in v0.1.

## 3. Receipt immutability

A receipt represents one point in time. Producers SHOULD NOT mutate an issued receipt to reflect later work. A later state SHOULD be represented by a new receipt, optionally linked through `receipt.predecessor.id`.

## 4. Work

`work.state` is the producer's description of lifecycle state. `completed` MUST NOT be interpreted by a verifier as proof of completion.

Allowed states:
`planned`, `in_progress`, `blocked`, `completed`, `abandoned`, `interrupted`.

## 5. Snapshot

`snapshot.artifacts` binds referenced work artifacts to digests.

If a repository is present, `snapshot.repository.commit` identifies the Git commit against which the receipt was captured. When `dirty: true`, artifact digests SHOULD capture relevant uncommitted files.

## 6. Claims

A Claim is a producer assertion about work state.

Allowed kinds:
`completion`, `behavior`, `validation`, `decision`, `constraint`, `assumption`, `blocker`, `risk`, `observation`.

Each Claim MUST have a unique `id`.

`source.type` identifies the origin of the assertion and MAY be `human`, `agent`, `tool`, or `imported`.

`verification.status` MAY be:
- `unsupported`
- `supported`
- `contradicted`
- `stale`
- `unknown`

A supported claim is not necessarily universally true; it means the receipt contains currently valid evidence that the producer has explicitly bound to the claim.

## 7. Evidence

Evidence is a recorded observation or reference associated with a claim.

v0.1 evidence types:
- `artifact`
- `command`
- `test`
- `vcs`
- `human`

Evidence strength describes what a verifier can do:
- `recorded`: preserved assertion/observation only.
- `checkable`: can be checked against current artifacts or metadata.
- `reproducible`: contains enough execution information to replay the check.

For executable evidence, `argv` SHOULD be used instead of a shell command string.

## 8. Claim–Evidence bindings

Claims MAY list `supported_by` and `contradicted_by` evidence IDs.

A verifier MUST reject dangling evidence references.

The core verifier MUST NOT use an LLM to infer whether arbitrary natural-language evidence logically proves a claim. The producer establishes the binding; the verifier checks reference integrity, freshness, and replayable observations.

## 9. Validity dependencies and staleness

A Claim MAY declare `depends_on.artifacts` and `depends_on.evidence`. These fields are **validity dependencies**: they identify objects whose invalidation requires the claim to be re-evaluated.

If a depended-on artifact no longer matches its captured digest, that artifact dependency is `stale`. A missing depended-on artifact is treated as an invalidated dependency for claim evaluation.

`stale` means the prior support can no longer be relied upon for the current snapshot. It does not mean the claim is false.

### 9.1 Deterministic claim-evaluation precedence

A conforming v0.1 verifier MUST evaluate each Claim using the following precedence, in order:

1. **Valid contradiction wins.** If any evidence referenced by `contradicted_by` is currently `valid`, the Claim MUST evaluate to `contradicted`.
2. **Explicit invalidated dependency causes staleness.** If any object referenced by `depends_on.artifacts` or `depends_on.evidence` is `stale`, `missing`, or `invalid`, the Claim MUST evaluate to `stale` unless rule 1 already produced `contradicted`.
3. **Any independent valid support is sufficient.** If at least one `supported_by` evidence reference is `valid`, the Claim MUST evaluate to `supported`, provided rules 1 and 2 did not apply.
4. **All prior supports invalidated means stale.** If `supported_by` is non-empty, no support is `valid`, and every supporting evidence state is one of `stale`, `missing`, or `invalid`, the Claim MUST evaluate to `stale`.
5. **Partially unresolved support means unknown.** If `supported_by` is non-empty and at least one support state is `unknown` while no earlier rule applies, the Claim MUST evaluate to `unknown`.
6. **No support references means unsupported.** If `supported_by` is absent or empty and no earlier rule applies, the Claim MUST evaluate to `unsupported`.

A verifier MUST apply these rules deterministically and MUST NOT reorder them.

### 9.2 Truth table examples

| Valid contradiction | Explicit stale dependency | Valid support | Other support states | Result |
|---|---|---|---|---|
| yes | any | any | any | `contradicted` |
| no | yes | any | any | `stale` |
| no | no | yes | any | `supported` |
| no | no | no | all stale/missing/invalid | `stale` |
| no | no | no | includes unknown | `unknown` |
| no | no | no | no support references | `unsupported` |

Examples:

- One stale support plus one independent valid support evaluates to `supported` when no explicit claim dependency is stale.
- A valid support does **not** preserve `supported` if the Claim explicitly declares a stale artifact dependency; the result is `stale`.
- A valid contradictory evidence item evaluates the Claim to `contradicted` even if a declared dependency is stale.

## 10. Verification levels

A conforming verifier SHOULD support:

1. **Schema** — structure, types, identifiers, references.
2. **Integrity** — artifact existence, digests, repository identity.
3. **Replay** — rerun reproducible command/test evidence when requested.
4. **Claim evaluation** — compute `supported`, `unsupported`, `contradicted`, `stale`, or `unknown` from explicit bindings and evidence validity.

Core verification MUST remain deterministic.

## 11. Continuation

`continuation` records the resume boundary, not a task-management system.

`next_actions` SHOULD include explicit acceptance criteria.
`unresolved` SHOULD list questions or decisions that remain open.

## 12. Security and attestation interoperability

StateReceipt v0.1 does not define a cryptographic signature envelope.

Future authentication SHOULD reuse established attestation mechanisms such as in-toto Statement and DSSE rather than defining a bespoke signing format.

## 13. Conformance

A document conforms to StateReceipt v0.1 when:
- it validates against the published v0.1 JSON Schema;
- all identifiers and references are internally consistent;
- any claimed verifier result is produced according to the deterministic validation semantics defined above.

## 14. Non-goals

StateReceipt v0.1 does not define:
- persistent AI memory
- vector search / RAG
- cross-agent messaging
- scheduling or orchestration
- agent spawning
- user profiling
- cryptographic signatures
- LLM-based truth adjudication
