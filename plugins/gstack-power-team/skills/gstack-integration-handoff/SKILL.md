---
name: gstack-integration-handoff
description: "Establish whether completed local work is ready to transfer, integrate, or continue."
---

# Integration Handoff

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- completed changes
- acceptance evidence
- remaining risks and ownership

Use available evidence; identify missing information only when it changes the decision.

## Method

- Confirm the exact work being handed over, its destination, accepted baseline, and concurrent changes affecting evidence; a changed target invalidates earlier readiness or approval where material. Disclose acceptance criteria changed by the candidate and reconcile them with authorized decisions rather than letting the work certify itself against altered requirements.
- Verify acceptance evidence is current and label partial checks. Individually accepted contributions do not prove the combined result; check the actual integrated state and interactions before claiming integrated readiness.
- Separate blockers from optional findings and deferred work.
- Check that documentation relevant to changed behavior reflects the final work, including late corrections. Record missing or stale documentation as such rather than implying an audit completed.
- Record changed surfaces, recovery, remaining risk, and next owner action. Preserve who approved what and under which conditions; carry approval forward only when those conditions still hold. A handoff label is not authority for further action.
- Declare ready only when the stated gate is met.

## Result

A readiness decision and handoff record with evidence.

## Scope

Produces a local readiness judgment and handoff. Publication, deployment, and further changes require their own authorized scope.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
