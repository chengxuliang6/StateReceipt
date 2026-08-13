# Cross-assistant continuation lab

This lab demonstrates the original StateReceipt use case with **two fresh assistant/session boundaries** and no hidden chat-history continuity.

The example is deliberately vendor-neutral. “Assistant A” and “Assistant B” can be two different model providers, two fresh sessions of the same provider, or a human/tool boundary.

## What the lab proves

It does **not** prove that StateReceipt transfers a model's full context or memory. It demonstrates a narrower property:

1. Assistant A leaves a point-in-time Receipt containing explicit Claims, Evidence, artifact digests, unresolved items, and next actions.
2. Assistant B receives the repository plus the Receipt.
3. Assistant B verifies the Receipt against the files that actually exist now instead of trusting the handoff text.
4. A deliberate post-handoff artifact change makes the affected Claims `stale`, changing what Assistant B should do next.

## Layout

```text
examples/cross-assistant/
├── README.md
├── RECEIVER_PROMPT.md
├── stage-a.yaml
├── reset_stage_a.py
├── mutate_after_handoff.py
├── workspace/
│   ├── __init__.py
│   └── score.py
└── tests/
    └── test_score.py
```

The task is intentionally small: `normalize_score()` clamps an integer into `0..100`.

## Stage A — verify the producer snapshot

From the repository root, install StateReceipt for development if needed:

```bash
python -m pip install -e ".[dev]"
```

Reset the lab to Assistant A's captured state:

```bash
python examples/cross-assistant/reset_stage_a.py
```

Run the tests:

```bash
python -m unittest discover -s examples/cross-assistant/tests
```

Verify Assistant A's Receipt against the lab root:

```bash
statereceipt verify examples/cross-assistant/stage-a.yaml --root examples/cross-assistant
```

The behavior and test Claims should evaluate as `supported` because the captured artifact digests still match.

You can also inspect the explicit continuation boundary:

```bash
statereceipt inspect examples/cross-assistant/stage-a.yaml
```

## Simulate a change after the handoff

Now change the implementation *without updating the old Receipt*:

```bash
python examples/cross-assistant/mutate_after_handoff.py
```

The changed implementation still clamps values, but it additionally rounds the clamped result down to a multiple of five. That is enough to invalidate the old snapshot and also changes a previously tested behavior (`42` becomes `40`).

Verify the **same** Receipt again:

```bash
statereceipt verify examples/cross-assistant/stage-a.yaml --root examples/cross-assistant
```

The Claims that explicitly depend on `workspace/score.py` should now evaluate as `stale`.

`stale` does not itself say whether the old Claims are true or false. It says Assistant B must not rely on Assistant A's old support without re-evaluating the changed work.

## Stage B — use a fresh assistant/session

Start a genuinely fresh assistant or session and provide it:

- the repository/worktree;
- `examples/cross-assistant/stage-a.yaml`;
- [`RECEIVER_PROMPT.md`](RECEIVER_PROMPT.md).

Do **not** provide the earlier Assistant A conversation.

A correct receiver workflow is:

```text
load Receipt
    ↓
verify against current artifacts
    ↓
read Claim status + continuation metadata
    ↓
if supported: continue from next_actions
if stale: re-open/re-test the affected assumption before continuing
```

In this mutated state, Assistant B should notice that the old implementation/test Claims are stale and should not simply continue as though “tests passed for the current code.”

## Reset

Return to Assistant A's exact captured implementation at any time:

```bash
python examples/cross-assistant/reset_stage_a.py
```

## Why there is no provider adapter here

Provider adapters would make the first example easier to demo but would blur StateReceipt's core boundary. The Receipt format and deterministic verifier must remain useful without ChatGPT-, DeepSeek-, Claude-, Gemini-, or Codex-specific APIs.

Provider-specific launch recipes can be added later as optional integrations while this lab remains the reference vendor-neutral behavior.
