---
name: gstack-readiness-triage
description: "Order pending work by dependency, conflict, and evidence needed to become ready."
---

# Readiness Triage

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- pending work
- dependencies and ownership
- readiness evidence

Use available evidence; identify missing information only when it changes the decision.

## Method

- List each item with owner, dependency, conflict, and needed evidence.
- Separate blocked work from unstarted work.
- Order by unblock value and consequence of delay.
- Mark stale, absent, or insufficient evidence.
- Return the next actionable queue only.

## Result

A prioritized readiness queue with blockers and next evidence.

## Scope

Read-only triage; does not modify pending work.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
