# Security Policy

## Supported versions

StateReceipt is currently pre-1.0. Security fixes are applied to the latest released 0.x version.

## Reporting a vulnerability

Please do not open a public issue for a vulnerability that could enable arbitrary command execution, receipt tampering, path traversal, unsafe replay, or another security-sensitive failure.

Use GitHub's private security reporting feature when it is enabled for this repository. If private reporting is unavailable, contact the maintainer through the contact method listed on the maintainer's GitHub profile and include `StateReceipt security` in the subject.

## Replay trust model

StateReceipt verification is non-executing by default. A normal command such as:

```bash
statereceipt verify receipt.yaml
```

never replays commands from the receipt.

`--replay` is only a request to replay reproducible evidence. The CLI MUST also receive an explicit trust acknowledgement:

```bash
statereceipt verify receipt.yaml --replay --trust-receipt
```

If `--replay` is supplied without `--trust-receipt`, the CLI refuses execution and exits before any replayable command is run.

`--trust-receipt` means only that the caller has reviewed the receipt and accepts the risk of executing its replayable commands. It is **not** cryptographic authentication, producer verification, a signature check, or a declaration that the receipt is safe.

## No sandbox guarantee

StateReceipt does **not** provide process isolation, container isolation, privilege dropping, syscall filtering, filesystem confinement, network isolation, or any other sandbox guarantee.

Replayable `evidence[].execution.argv` values are executable input. Before enabling replay:

- inspect the receipt and every replayable command;
- do not replay receipts from unknown or untrusted sources;
- use a disposable container, VM, or other suitable isolation boundary for higher-risk commands;
- run with the least privileges required;
- remember that JSON Schema validation checks structure, not command safety.

StateReceipt may add policy hooks in future versions, but the core project does not claim to make arbitrary commands safe to execute.

## Receipt identity

StateReceipt v0.1 does not define cryptographic signing or producer authentication. A structurally valid receipt is not proof of author identity.

## Translations

For accessibility, replay guidance is also available in [Simplified Chinese](docs/SECURITY.zh-CN.md) and [Spanish](docs/SECURITY.es.md). This English file is the authoritative security policy if translations differ.
