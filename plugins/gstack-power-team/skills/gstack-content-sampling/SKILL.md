---
name: gstack-content-sampling
description: "Assess repeated content through a representative declared sample."
---

# Content Sampling

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- content population
- user tasks
- sampling dimensions

Use available evidence; identify missing information only when it changes the decision.

## Method

- Define population and coverage target first.
- Include edge, empty, dense, stale, and high-consequence examples.
- Judge usefulness and consistency against the user task.
- Separate sampled defects from population-wide claims.

## Result

A coverage-labeled sampling report with findings.

## Scope

Read-only; conclusions apply only to declared coverage.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
