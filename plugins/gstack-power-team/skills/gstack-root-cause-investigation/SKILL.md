---
name: gstack-root-cause-investigation
description: "Establish the cause of unexpected behavior before choosing a repair."
---

# Root Cause Investigation

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- reported behavior
- reproduction evidence
- relevant state or history

Use available evidence; identify missing information only when it changes the decision.

## Method

- Preserve the smallest reliable reproduction.
- Build competing causal hypotheses from evidence, including the premise behind the requested remedy. When repeated attempts fail on the same premise, test that premise with a discriminating observation before varying the remedy again.
- Choose checks that discriminate hypotheses and record negatives. For order-sensitive failures, preserve and minimize the triggering sequence without losing interactions, then locate leaked state and its owner. For concurrent failures, examine the suspected ordering with safe authorized probes and check the durable invariant, not merely absence of errors.
- Trace the supported cause to the diverging boundary.
- State confidence limits and next evidence when uncertain.

## Result

A causal conclusion or bounded hypothesis set with evidence.

## Scope

Investigation only; repair is separate.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
