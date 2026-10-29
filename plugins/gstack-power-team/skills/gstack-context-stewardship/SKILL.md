---
name: gstack-context-stewardship
description: "Preserve, restore, and refresh decision-relevant context without trusting stale notes as fact."
---

# Context Stewardship

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- current goal
- prior decisions and evidence
- current state

Use available evidence; identify missing information only when it changes the decision.

## Method

- Separate durable decisions, assumptions, evidence, and pending work. Preserve project, task, and revision identity; the newest record is not necessarily the relevant one.
- Mark claims with source, freshness, and invalidating conditions.
- Reconcile stored context with current state after a pause; failed access means unknown, not empty or obsolete context. Before replaying a proposed state change, verify the actual target and prior effects; reading the procedure alone does not establish that repeating it is safe.
- Preserve only context that changes future decisions.
- State the next action and needed evidence. Preserve the exact scope and source of approvals across handoffs; stored acknowledgement is not authority for changed work.
- Retain only decision-relevant context and omit secrets or unrelated personal information.

## Result

A current context record with trusted facts, stale items, and next steps.

## Scope

Does not substitute notes for fresh verification.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
