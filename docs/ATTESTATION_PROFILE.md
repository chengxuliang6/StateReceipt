# StateReceipt in-toto / DSSE Interoperability Profile

[简体中文](ATTESTATION_PROFILE.zh-CN.md) | [Español](ATTESTATION_PROFILE.es.md)

**Status:** exploratory interoperability profile for StateReceipt v0.1. This document does not make signed attestations a core requirement.

## Design goal

StateReceipt should interoperate with established attestation and signing standards without inventing a new cryptographic envelope.

The profile uses the in-toto Statement v1 model:

```text
in-toto Statement
├── _type
├── subject[]
├── predicateType
└── predicate  ← complete StateReceipt document
```

Optional signing is layered outside the Statement using DSSE.

## Lossless mapping

The mapping is intentionally simple and reversible.

### `subject`

For every entry in `StateReceipt.snapshot.artifacts`, produce one in-toto subject:

```json
{
  "name": "<artifact.id>",
  "digest": {
    "<artifact.digest.algorithm>": "<artifact.digest.value>"
  }
}
```

StateReceipt v0.1 currently allows SHA-256 and SHA-512, both of which fit the in-toto DigestSet model.

`artifact.id` is used as the subject name because StateReceipt requires artifact IDs to be unique within a Receipt. The original path, media type, and all other StateReceipt semantics remain available inside the predicate.

The repository commit in `snapshot.repository`, when present, remains in the StateReceipt predicate. v0.1 does not automatically reinterpret a Git commit as an additional in-toto subject.

### `predicateType`

A stable versioned predicate TypeURI must be assigned before a production interoperability release. This draft deliberately does **not** freeze a URI while the project has no stable specification namespace.

Examples in this document therefore use:

```text
<STATERECEIPT_PREDICATE_TYPE_URI>
```

A future release MUST replace that placeholder with a stable versioned URI before advertising interoperable signed attestations.

### `predicate`

The in-toto `predicate` is the complete StateReceipt document, unchanged:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [
    {
      "name": "artifact-001",
      "digest": {
        "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
      }
    }
  ],
  "predicateType": "<STATERECEIPT_PREDICATE_TYPE_URI>",
  "predicate": {
    "spec": {"name": "StateReceipt", "version": "0.1"},
    "receipt": {"id": "sr-example", "created_at": "2026-08-13T00:00:00Z", "producer": {"type": "human", "name": "example"}},
    "work": {"id": "DEMO-1", "objective": "Demonstrate attestation mapping", "state": "completed"},
    "snapshot": {
      "artifacts": [
        {
          "id": "artifact-001",
          "path": "artifact.txt",
          "digest": {
            "algorithm": "sha256",
            "value": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
          }
        }
      ]
    },
    "claims": [
      {
        "id": "claim-001",
        "kind": "observation",
        "statement": "Artifact captured.",
        "source": {"type": "human"},
        "verification": {"status": "unsupported"}
      }
    ],
    "evidence": [],
    "continuation": {"next_actions": [], "unresolved": []}
  }
}
```

Because the complete StateReceipt object is preserved as the predicate, extracting `statement.predicate` reconstructs the original Receipt without loss.

## Subject/predicate consistency

The outer `subject` is a digest projection of `predicate.snapshot.artifacts`; it is intentionally redundant.

A StateReceipt-aware attestation consumer SHOULD verify that:

1. every `predicate.snapshot.artifacts[*].id` has one corresponding subject name;
2. the subject digest algorithm and value match the artifact digest in the predicate;
3. no additional subject is silently interpreted as part of the StateReceipt snapshot unless a later profile explicitly defines that behavior.

A mismatch means the outer attestation binding and the embedded StateReceipt disagree. Consumers should reject or explicitly flag that condition rather than guessing which layer is authoritative.

## Optional DSSE wrapping

If authenticity is required, the **in-toto Statement**, not the raw Receipt alone, should be serialized and wrapped by a standard DSSE implementation.

Conceptually:

```text
StateReceipt
   ↓ mapping
in-toto Statement
   ↓ serialize
DSSE payload
   ↓ external signer
DSSE Envelope
```

For an in-toto JSON Statement, the in-toto envelope specification permits the generic payload type:

```text
application/vnd.in-toto+json
```

DSSE handles pre-authentication encoding and signature envelopes. StateReceipt does not define PAE, signature algorithms, key IDs, PKI, key rotation, transparency logs, or trust roots.

## Verification layers remain separate

Three independent questions must not be conflated:

1. **StateReceipt conformance:** Is the embedded predicate a valid StateReceipt and are its deterministic work-state checks valid?
2. **Attestation consistency:** Does the in-toto subject projection agree with the embedded StateReceipt artifact digests?
3. **Authenticity:** Does an external DSSE/signature verifier accept the envelope under a caller-selected trust policy?

A valid signature does not make a Claim true. It authenticates bytes according to the external signing policy.

## Unsigned local Receipts remain first-class

A plain YAML/JSON StateReceipt remains fully conforming without in-toto or DSSE.

This interoperability profile is optional and additive. It must not force local users to provision keys, adopt PKI, use a transparency service, or depend on network infrastructure.

## Explicit non-goals

StateReceipt does not introduce:

- a custom signature format;
- a custom pre-authentication encoding;
- key management or PKI;
- a replacement for in-toto Statement;
- a replacement for DSSE;
- a claim that a cryptographic signature proves work correctness.

## Primary standards reviewed

This profile was designed against the official in-toto Attestation Framework Statement v1 and Envelope specifications, plus the Secure Systems Lab DSSE protocol and envelope specification. StateReceipt treats those mechanisms as prior art and interoperability dependencies, not project inventions.
