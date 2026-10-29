---
name: gstack-specification
description: "Turn ambiguous intent into bounded scope, decisions, and testable acceptance criteria."
---

# Specification

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- stated intent
- current local state
- constraints and stakeholders

Use available evidence; identify missing information only when it changes the decision.

## Method

- Establish why work matters and verify current state.
- Define behavior, exclusions, dependencies, and affected areas.
- Write observable acceptance criteria and recovery posture. For planned checks, state the wrong outcome they should reject and what a pass would not establish, including simulated substitutes for real behavior.
- Expose ambiguity, contradictions, and unresolved decisions.
- Reject detail that changes no necessary decision.

## Result

An executable specification with scope, acceptance evidence, and open decisions.

## Scope

Defines work; does not commit implementation.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
