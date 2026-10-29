---
name: gstack-change-review
description: "Review current or aging local changes for defects, semantic drift, missing proof, and avoidable complexity."
---

# Change Review

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- change set
- requirements and invariants
- relevant checks and states

Use available evidence; identify missing information only when it changes the decision.

## Method

- Bind review to observed content and confirm it remains current. For aging work, reassess the original problem, proposed solution, and necessary assumptions against current behavior; mechanical compatibility, age, and sunk effort do not establish value. Recommend retain, rework, or retire with evidence, without implying authority to alter the work.
- Trace risks, regressions, missing proof, and incomplete behavior from cause to impact. Test the premise that makes a risky change safe across indirect consumers and lifecycle boundaries, not only direct callers. When accepted inputs widen, inspect downstream handling and reachable sibling paths; distinguish cleared risks from unproven ones.
- Collect and consolidate findings against the same candidate before any separately authorized correction. Confirm affected reviewers have finished or stopped before changing their inputs.
- Consolidate project checks and manual observations; label unavailable evidence. Expiration of optional exploration does not waive required verification; report unfinished required checks explicitly.
- Assess duplicate capability, needless abstraction, and dead flexibility. Reuse advice needs verified authored consumers, compatible behavior, and a benefit after integration costs; similarity alone is not a defect.
- For changed tests, identify the protected contract, a credible regression, and why existing evidence is insufficient. After removal or renaming, check whether negative assertions now pass without exercising the intended contract. Prefer extending useful coverage over duplicating it; a weak test does not close a coverage gap.
- Separate blockers from optional simplification; incomplete passes are not clean.
- Re-review after fixes or concurrent edits affect relevant content, including supporting consumers and evidence. Reuse evidence only when relevant content, inputs, and conditions remain equivalent, not merely because a label is unchanged. Reuse prior advice decisions only while their scope and supporting facts still hold.
- Apply review depth proportionate to consequence while retaining required checks. Interpret exceptions against the governing authority outside the candidate change; an exception does not erase the need to inspect affected content.
- Keep approved, completed, verified, deferred, and unresolved actions distinct. Skipping a repair leaves its defect unresolved; a prior fix cannot suppress a recurring defect.

## Result

A current finding set or clean result with coverage limits.

## Scope

Read-only unless fixes are separately authorized.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
