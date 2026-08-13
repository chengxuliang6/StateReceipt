# Receiver instructions

You are continuing work from a prior assistant/session. Do not assume the prior assistant's Claims are still valid.

1. Read `stage-a.yaml` as the point-in-time StateReceipt.
2. Run deterministic verification against the current lab root before relying on any Claim:

   ```bash
   statereceipt verify examples/cross-assistant/stage-a.yaml --root examples/cross-assistant
   ```

3. Inspect the Receipt's work objective, Claims, unresolved items, and `continuation.next_actions`.
4. Treat `supported` as currently backed by the explicit evidence/dependencies captured in the Receipt.
5. Treat `stale` as requiring re-evaluation; do not interpret it as automatically false.
6. If a Claim relevant to the next action is stale, inspect the changed artifact and rerun or add appropriate tests before continuing.
7. Do not infer missing prior-chat context. State what information is absent if the Receipt and repository are insufficient.
8. Do not run Receipt replay commands unless you have independently reviewed them and intentionally accept the execution risk required by StateReceipt's replay trust model.

Your goal is not to recreate the prior conversation. Your goal is to continue safely from the verifiable work state that exists now.
