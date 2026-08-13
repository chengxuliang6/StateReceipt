# StateReceipt Receipt Lifecycle

[简体中文](LIFECYCLE.zh-CN.md) | [Español](LIFECYCLE.es.md)

> The normative lifecycle rules are in [`spec/SPEC.md`](../spec/SPEC.md). This guide is explanatory.

StateReceipt Receipts are immutable point-in-time artifacts. Later work should produce a new Receipt rather than editing an earlier one.

## Direct predecessor

A later Receipt may identify exactly one direct predecessor:

```yaml
receipt:
  id: SR-B
  predecessor:
    id: SR-A
```

This means `SR-B` directly continues the work state represented by `SR-A`.

A Receipt may not name itself as its predecessor. A predecessor ID may refer to a Receipt that is not present locally; StateReceipt v0.1 has no global registry and does not require network resolution.

## Example chain

```text
SR-A (interrupted)
  ↓
SR-B (in_progress)
  ↓
SR-C (completed)
```

The work-state labels do not form a StateReceipt-controlled state machine. They are recorded snapshots.

## Validate a local chain set

```bash
statereceipt validate-chain sr-a.yaml sr-b.yaml sr-c.yaml
```

The command rejects:

- duplicate Receipt IDs in the supplied set;
- predecessor self-reference;
- cycles that can be resolved inside the supplied set.

A predecessor absent from the supplied files is reported as external/unresolved but does not make the set invalid by itself.

## Diff does not imply lineage

```bash
statereceipt diff sr-a.yaml sr-b.yaml
```

The result reports `lifecycle_relation` as one of:

- `same_receipt`
- `direct_successor`
- `direct_predecessor`
- `not_directly_linked`

`not_directly_linked` only means the two supplied Receipts are not direct neighbors. They may still be non-adjacent members of a larger chain.
