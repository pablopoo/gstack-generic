---
name: gstack-evidence-extraction
description: "Extract decision-relevant facts from an artifact or observed surface."
---

# Evidence Extraction

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- source artifact or surface
- questions to answer
- required fact structure

Use available evidence; identify missing information only when it changes the decision.

## Method

- Define decisions the facts must support.
- Capture location, observation date, and confidence.
- Separate direct observation, source claim, and inference.
- Retain ambiguity and conflicting evidence. Keep summaries and proposed checks no stronger than their supporting observations; an observed message does not prove the event it describes or establish recurrence.
- Return unresolved questions instead of assumptions.

## Result

A traceable fact record with uncertainty and open questions.

## Scope

Does not validate claims beyond inspected sources.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
