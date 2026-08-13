# Prior Art and Related Work

This document records related concepts reviewed before and during StateReceipt development. It is not a claim that the listed projects are equivalent to StateReceipt, nor is it legal advice.

## Standards and infrastructure

### in-toto Attestation Framework / SCAI

Relevant overlap: artifact subjects identified by digests, attestations, attribute assertions, and evidence associated with assertions.

StateReceipt does **not** claim to invent attestations, digest binding, provenance, or evidence-backed assertions. Its specification instead defines a domain-specific work-state receipt and deterministic freshness semantics for AI-assisted work.

### DSSE

Relevant overlap: a generic signed envelope for arbitrary payloads.

StateReceipt v0.1 intentionally defines no signature envelope. Future authentication should prefer interoperability with established mechanisms such as DSSE/in-toto rather than a bespoke cryptographic format.

## Agent runtimes and handoff systems

### OpenAI Agents SDK

Relevant overlap: handoffs, sessions, resumable state, and agent orchestration.

StateReceipt is not an agent runtime and does not define delegation, routing, or conversation transfer.

## Memory and continuity systems

Multiple open-source tools address persistent project memory, cross-session continuity, handoff notes, or resumable engineering context. StateReceipt intentionally avoids positioning persistent memory, `HANDOFF.md` generation, generic task orchestration, or cross-agent messaging as its core contribution.

## StateReceipt boundary

StateReceipt focuses on a smaller question:

> At a particular point in time, what claims are being made about an AI-assisted work unit, what explicit evidence is bound to those claims, what artifacts/snapshot did that evidence depend on, and has that support become stale?

The project should be described in those terms rather than as a general memory, handoff, provenance, or orchestration framework.

## Ongoing review

Before adding a major primitive, maintainers should search for relevant standards and open-source implementations and update this document when overlap is material.
