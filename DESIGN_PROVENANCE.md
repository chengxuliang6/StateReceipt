# Design Provenance

## Origin

StateReceipt originated from a practical engineering problem: after an AI-assisted task is interrupted or moved to another assistant, a prose summary is easy to trust even when its claims are stale, incomplete, or unsupported by the current repository state.

The project was therefore scoped around **point-in-time work-state receipts** rather than persistent memory or agent orchestration.

## Prior-art review before implementation

Before the reference implementation was written, related systems and standards were reviewed to identify capabilities that StateReceipt should not claim as original. The review included agent handoff/session systems, memory/continuity tools, software attestation standards, and evidence-oriented engineering workflows.

Important design consequences of that review:

- agent-to-agent handoff is treated as established prior art;
- persistent cross-session memory is outside StateReceipt's core scope;
- artifact digests, provenance, attestations, and evidence-backed assertions are not claimed as StateReceipt inventions;
- cryptographic signing should interoperate with established attestation/envelope mechanisms rather than introducing a bespoke signature format;
- the StateReceipt-specific focus is the work-state domain model: claims about an AI-assisted work unit, explicit validity dependencies, deterministic freshness/staleness evaluation, and a narrow continuation boundary.

## Independent implementation rule

The v0.1 reference implementation was designed from the StateReceipt specification and its tests. Related projects may be studied for publicly documented behavior and problem framing, but their implementation code, private logic, schemas, prompts, tests, documentation prose, branding, and artwork are not to be copied into StateReceipt without a documented license review.

## Design identity

The core StateReceipt model is:

```text
work + snapshot
     |
   claims ----supported/contradicted by----> evidence
     |                                        |
     +------ validity dependencies ----------+
                         |
                    artifacts/digests
                         |
                  freshness evaluation
```

A receipt is immutable, point-in-time data. A later work state is represented by a new receipt rather than editing the previous receipt.
