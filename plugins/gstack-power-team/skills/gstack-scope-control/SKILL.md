---
name: gstack-scope-control
description: "Set or revise a safe boundary for broad, destructive, or expanding work."
---

# Scope Control

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- requested change
- owned surfaces
- irreversible actions and dependencies

Use available evidence; identify missing information only when it changes the decision.

## Method

- State allowed and prohibited surfaces.
- Identify destructive actions, shared ownership, and recovery points.
- Require evidence before widening a boundary.
- Widen only the minimum needed and record new risk.
- Stop when ownership or recovery is unclear. For resource-consuming work, define a proportionate limit, account for concurrent commitments and unknown use, and record a bounded stop or continuation point. Do not evade a limit by splitting or restarting work.
- Define recovery to release only state acquired by this operation whose ownership still matches. Preserve pre-existing or replaced restrictions; ending a session is not evidence that persistent effects disappeared.

## Result

An edit boundary with widening criteria and recovery posture.

## Scope

Does not authorize unrelated changes.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
