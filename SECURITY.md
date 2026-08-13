# Security Policy

## Supported versions

StateReceipt is currently pre-1.0. Security fixes are applied to the latest released 0.x version.

## Reporting a vulnerability

Please do not open a public issue for a vulnerability that could enable arbitrary command execution, receipt tampering, path traversal, unsafe replay, or another security-sensitive failure.

Use GitHub's private security reporting feature when it is enabled for this repository. If private reporting is unavailable, contact the maintainer through the contact method listed on the maintainer's GitHub profile and include `StateReceipt security` in the subject.

## Replay warning

`statereceipt verify --replay` may execute commands recorded in a receipt. Treat receipts from untrusted sources as untrusted input. Review replayable commands before execution and run them in an appropriately isolated environment.

StateReceipt v0.1 does not define cryptographic signing or producer authentication. A structurally valid receipt is not proof of author identity.
