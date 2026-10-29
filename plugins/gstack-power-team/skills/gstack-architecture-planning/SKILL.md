---
name: gstack-architecture-planning
description: "Resolve responsibilities, boundaries, sequencing, and failure behavior for a consequential change."
---

# Architecture Planning

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- accepted scope and requirements
- existing system responsibilities
- constraints and acceptance evidence

Use available evidence; identify missing information only when it changes the decision.

## Method

- Map responsibilities, data and control flow, dependencies, and ownership boundaries.
- Compare plausible approaches against invariants, complexity, reversibility, and the cost of change. For a consequential new public boundary, include a structurally different responsibility or ownership split, not only refinements of the same shape; assess the coordination burden exposed to consumers.
- Identify partial failure, recovery, compatibility, and transition states before sequencing implementation. For repeated or interrupted state changes, define how to reconcile prior effects before retrying; do not assume an unknown outcome means nothing happened.
- When concurrent writers collide, first consider separating ownership or state. Where shared state is necessary, make the coordination responsibility explicit rather than relying on an unstated one-writer assumption.
- Prefer existing capabilities when they meet the requirements without obscuring responsibility. Justify proposed sharing through compatible behavior and net reliability or maintenance benefit after integration and shared-failure risks; label planned consumers as assumptions.
- Define the evidence needed at each risky boundary and identify unresolved decisions that block implementation. Each proposed test should name its protected behavior, a credible regression, and why existing coverage cannot provide the same assurance.

## Result

A feasible architecture and implementation sequence with invariants, failure handling, and verification criteria.

## Scope

Planning only; use the current amended requirements and do not choose a technology on the user's behalf without need.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
