---
name: gstack-comparative-evaluation
description: "Plan or assess a comparison when alternatives or before-and-after behavior need equivalent evidence."
---

# Comparative Evaluation

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- alternatives or baseline
- decision criteria
- representative conditions

Use available evidence; identify missing information only when it changes the decision.

## Method

- Define observable success, alternatives, sampling, retry rules, and stopping criteria before measurement. Freeze these for the comparison; later changes start a separately labeled evaluation, not a revised verdict on the original run.
- Separate development examples from held-out evidence and disclose prior exposure. Where identity could bias judgment, conceal irrelevant labels and assess observed behavior rather than self-reported compliance.
- Before a costly or consequential evaluation, validate the measurement process with known positive and negative cases and a bounded pilot. Estimate total resource demand with uncertainty; scaling beyond authorized limits requires approval, not self-approval when the owner is unavailable.
- Hold workload, environment, and coverage constant. For performance claims, verify that correct work actually completes inside the measured interval, separate diagnostic observation from timing, use realistic configurations, and check whether the gain is plausible given the limiting resource and end-to-end workload.
- Separate measured change from inferred cause and correctness from incremental benefit. A baseline already at the measurement ceiling may leave improvement or equivalence unproven.
- Reject missing baselines and non-equivalent coverage.
- Retain every attempt, including failed and interrupted trials. Separate setup failures from evaluated outcomes rather than retrying until a favorable result appears; include failed work and cleanup in total cost comparisons.
- Keep historical verdicts tied to their original criteria and contract version. Distinguish estimated, committed, measured, and unknown resource use; unknown cost is not zero. An interpretation failure is missing evidence, not grounds to change samples or thresholds.
- Distinguish strict invariants from variable behavior: an invariant violation remains a failure; variable outcomes use the declared repeated-sample rule and disclose variation.

## Result

A comparable evidence record and decision with confidence.

## Scope

Does not choose personnel or operational tooling.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
