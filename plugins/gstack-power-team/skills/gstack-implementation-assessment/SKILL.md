---
name: gstack-implementation-assessment
description: "Assess implementation choices or code-reuse opportunities against requirements and maintenance costs."
---

# Implementation Assessment

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- implementation, change, or bounded reuse opportunity
- requirements
- constraints and alternatives

Use available evidence; identify missing information only when it changes the decision.

## Method

- Restate requirements, invariants, and non-goals.
- Trace affected boundaries, failure modes, and maintenance burden.
- Compare alternatives only where they change the decision.
- For reuse proposals, verify actual authored consumers and common behavior, preserve meaningful differences, and prefer a compatible existing capability. Similar appearance or imagined future consumers is not sufficient evidence.
- Weigh reliability gains and total maintenance savings against migration, verification, coupling, and shared-failure risk. Exclude generated or third-party copies from duplication savings and check for overlapping work.
- Distinguish defects from optional simplification.
- State evidence that would reverse the recommendation.

## Result

An independent recommendation with tradeoffs and confidence.

## Scope

Assessment only; does not modify implementation.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
