---
name: gstack-early-signal-observation
description: "Observe critical changed behavior for early failure signals."
---

# Early Signal Observation

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- changed behavior
- critical flows
- expected signals and thresholds

Use available evidence; identify missing information only when it changes the decision.

## Method

- Select flows whose failure invalidates the change.
- Declare the starting state, expected outcomes, observation window, interval, and stop conditions.
- Observe declared conditions rather than treating silence as proof.
- Separate absent signals, unavailable observation, and failures.
- State when observation ended; do not imply continued monitoring after completion.

## Result

A time-bounded observation record and follow-up recommendation.

## Scope

Observation only; not broad reliability proof.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
