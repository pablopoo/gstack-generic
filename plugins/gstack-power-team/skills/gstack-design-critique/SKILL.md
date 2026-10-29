---
name: gstack-design-critique
description: "Evaluate an implemented experience for hierarchy, flow, feedback, consistency, and accessibility."
---

# Design Critique

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- implemented states
- user journeys
- documented design decisions

Use available evidence; identify missing information only when it changes the decision.

## Method

- Inspect representative rendered states and label inference separately.
- Trace tasks through transitions, feedback, errors, and recovery. Check applicable human and automated failure signals agree, recovery is safe, and diagnostic context is useful without disclosing secrets; unobserved error paths remain unknown.
- Assess hierarchy, affordances, consistency, accessibility, and responsive behavior. Where motion exists, verify content remains usable without it and inspect transitions, interruption, rest, and repetition for lost state, overflow, or obscured information.
- Locate user impact and consolidate duplicate observations. Distinguish real claims and supplied proof from illustrative data, and flag unresolved primary-action dependencies rather than inventing convincing content or silently changing approved decisions.
- Preserve justified exceptions rather than applying generic rules.

## Result

A prioritized finding set with evidence and affected states.

## Scope

Read-only critique.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
