---
name: gstack-scenario-evaluation
description: "Evaluate an interaction or functional contract across representative states without changing the product."
---

# Scenario Evaluation

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- critical interaction or functional contract
- state preconditions
- expected outcomes and failure modes

Use available evidence; identify missing information only when it changes the decision.

## Method

- Select relevant surfaces from the requested behavior, including those without a visual interface. Map states, transitions, preconditions, expected outcomes, and failure modes before probing.
- Establish isolation and ownership of test state and downstream effects; a local entry point does not prove its effects are local. Unknown ownership blocks affected probes.
- Prepare only authorized realistic state needed for the scenario. Observe both the immediate result and durable effects; acceptance of work is not evidence of completion. A containment or setup failure does not prove the intended target path was exercised.
- Probe documented input constraints independently where relevant: violate the selected rule while satisfying the others, so an earlier rejection cannot hide a missing guard. Inspect failure signals, safe recovery, and caller-appropriate diagnostics against the contract.
- Cover relevant invalid input, denied access, cancellation, retry limits, duplicate effects, competing operations, and partial-failure recovery against the declared contract; do not invent guarantees. For state-changing behavior, map distinct state and owner-action combinations to expected durable results and their own evidence; a sibling case or success status alone does not prove preservation.
- For exploratory work, record each observation, current input state, what was learned, and the next discriminating probe. Preserve prior evidence and mark proposed but unrun probes explicitly.
- For regression comparison, verify the prior evidence matches the target and supports safe replay. Missing replay inputs block that comparison, not independent checks; changed inputs invalidate affected observations.
- Report severity, reproduction, confidence, and coverage limits.
- Keep evidence and coverage separate for different surfaces; do not blend incompatible scores. Distinguish passed, failed, blocked, not run, and inconclusive outcomes.
- Separate report-only findings from authorized corrections; missing test infrastructure is a coverage gap, not permission to install or modify it.

## Result

A scenario report with evidence, findings, and coverage.

## Scope

Product behavior is not changed by this assessment. Use only authorized local test state; report-only requests do not authorize corrective edits.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
