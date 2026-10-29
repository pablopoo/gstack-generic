---
name: gstack-defect-correction
description: "Reproduce, correct, and verify a defect within bounded implementation scope."
---

# Defect Correction

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- reproduction
- supported cause or repair hypothesis
- affected behavior and constraints

Use available evidence; identify missing information only when it changes the decision.

## Method

- Confirm the smallest reproducer against the intended contract, not recorded faulty behavior.
- Choose the narrowest coherent correction.
- Verify the reproducer and adjacent behavior.
- Add or extend regression coverage when practical, showing failure for the original defect before repair and success afterward. If this comparison cannot run safely, report missing proof rather than a verified regression fix.
- Separate invalid test setup from a product defect; preserve valid failing evidence rather than deleting it or changing expectations to accept the defect.
- Report fixed behavior separately from remaining risk.

## Result

A bounded correction with reproduction and regression evidence.

## Scope

Edits only authorized scope; uncertain causes return to investigation.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
