# Prior Art and Related Work

This document records related concepts reviewed before and during StateReceipt development. It is not a claim that the listed projects are equivalent to StateReceipt, nor is it legal advice.

## Standards and infrastructure

### in-toto Attestation Framework / SCAI

Relevant overlap: artifact subjects identified by digests, attestations, attribute assertions, and evidence associated with assertions.

The in-toto Statement model already defines a standard outer structure containing `subject`, `predicateType`, and `predicate`. Its subject model binds attestations to artifacts through immutable digest identifiers. StateReceipt does **not** claim to invent attestations, digest binding, provenance, or evidence-backed assertions.

StateReceipt's optional interoperability profile therefore treats a complete StateReceipt document as an in-toto predicate and derives the outer in-toto subjects from `snapshot.artifacts`. This is an interoperability mapping, not a new attestation framework. See `docs/ATTESTATION_PROFILE.md`.

### DSSE

Relevant overlap: a generic signed envelope for arbitrary payloads, including pre-authentication encoding that binds payload bytes to a payload type.

StateReceipt v0.1 intentionally defines no signature envelope, signing algorithm, key-management scheme, PKI, trust root, or transparency mechanism. If authenticity is needed, the project should wrap an in-toto Statement using an existing DSSE implementation rather than define bespoke cryptography.

A valid DSSE signature authenticates bytes under an external trust policy; it does not prove that a StateReceipt Claim is true or that the recorded work is correct.

Unsigned local StateReceipt documents remain fully conforming. in-toto / DSSE interoperability is optional and additive.

## Agent runtimes and handoff systems

### OpenAI Agents SDK

Relevant overlap: handoffs, sessions, resumable state, and agent orchestration.

StateReceipt is not an agent runtime and does not define delegation, routing, or conversation transfer.

## Memory and continuity systems

Multiple open-source tools address persistent project memory, cross-session continuity, handoff notes, or resumable engineering context. StateReceipt intentionally avoids positioning persistent memory, `HANDOFF.md` generation, generic task orchestration, or cross-agent messaging as its core contribution.

## StateReceipt boundary

StateReceipt focuses on a smaller question:

> At a particular point in time, what claims are being made about an AI-assisted work unit, what explicit evidence is bound to those claims, what artifacts/snapshot did that evidence depend on, and has that support become stale?

The project should be described in those terms rather than as a general memory, handoff, provenance, orchestration, attestation, or cryptographic-signing framework.

## Ongoing review

Before adding a major primitive, maintainers should search for relevant standards and open-source implementations and update this document when overlap is material.
