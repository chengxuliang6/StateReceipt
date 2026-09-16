# Assistant integration recipes

These recipes exercise the checked-in [`examples/cross-assistant`](../examples/cross-assistant/README.md) lab. They require no model API and do not transfer chat history or hidden model state.

## Recipe A: continue in a fresh Codex session

1. In the producing session, finish a bounded work unit and capture the relevant artifacts:

   ```bash
   statereceipt capture src tests --work-id SR-EXAMPLE --objective "Complete the current work unit"
   ```

2. Commit the receipt or otherwise place it beside the exact worktree being handed off.
3. Start a fresh Codex session with no earlier conversation and provide this instruction:

   ```text
   Read the repository instructions and the supplied StateReceipt. Validate and verify the receipt against the current worktree before relying on any recorded claim. If a claim is stale, inspect and re-test its changed dependencies. Continue only from supported claims and the explicit next_actions. Do not replay receipt commands unless they have been reviewed and explicitly trusted.
   ```

4. The receiving session runs:

   ```bash
   statereceipt validate path/to/receipt.yaml
   statereceipt verify path/to/receipt.yaml --root .
   statereceipt inspect path/to/receipt.yaml
   ```

Expected behavior: unchanged artifact-bound claims remain `supported`; a changed depended-on artifact makes those claims `stale`.

## Recipe B: Codex to another assistant

This is a provider-independent handoff. The receiving assistant may be Claude, DeepSeek, Gemini, another Codex session, or a human workflow.

1. The Codex producer leaves the repository, the receipt, and [`RECEIVER_PROMPT.md`](../examples/cross-assistant/RECEIVER_PROMPT.md).
2. Deliberately remove access to the producing conversation. The receiver gets only those artifacts.
3. The receiver follows the prompt and reports:
   - receipt validation result;
   - current status of every claim;
   - changed or missing dependencies;
   - unresolved items and the next safe action.
4. To reproduce a stale handoff locally, run:

   ```bash
   python examples/cross-assistant/reset_stage_a.py
   statereceipt verify examples/cross-assistant/stage-a.yaml --root examples/cross-assistant
   python examples/cross-assistant/mutate_after_handoff.py
   statereceipt verify examples/cross-assistant/stage-a.yaml --root examples/cross-assistant
   ```

The first verification supports the artifact-bound claims. The second marks them stale because the implementation changed after capture.

## Report a real workflow result

Use the repository's **Workflow feedback** issue form. Include the producer/receiver boundary, the receipt version, whether verification detected stale state, and any private information removed from the example. A report is evidence of a real trial only when submitted by the person or team that performed it.
