---
name: gstack-design-implementation-planning
description: "Translate approved design direction into buildable interface decisions."
---

# Design Implementation Planning

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- approved direction
- existing interface structure
- implementation constraints

Use available evidence; identify missing information only when it changes the decision.

## Method

- Map direction to states, components, content, and interactions.
- Identify decisions required before implementation.
- Resolve shared structure and responsive behavior before polish.
- Define representative states and observable acceptance criteria, including primary-action invalid, pending, failure, and success states where relevant. Separate source-backed claims from illustrative content; expose missing proof and unresolved dependencies without inventing them or authorizing external setup.
- When motion is relevant, name the user purpose and appropriate motion budget. Preserve approved content and interactions without animation or with reduced motion; define starting, interrupted, resting, and repeating states where applicable.

## Result

A buildable design plan with state coverage.

## Scope

Planning only.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
