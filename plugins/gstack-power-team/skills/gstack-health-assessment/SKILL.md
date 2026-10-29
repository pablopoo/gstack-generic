---
name: gstack-health-assessment
description: "Assess correctness, test quality, maintainability, and known risk with explicit coverage."
---

# Health Assessment

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- requested dimensions
- available checks
- prior comparable results

Use available evidence; identify missing information only when it changes the decision.

## Method

- Select checks representing requested dimensions and record what ran; distinguish checks that exist from checks that meaningfully protect the assessed behavior.
- Preserve each check's actual result and complete diagnostic counts independently from shortened report output; successful formatting does not make a failed check pass or add a checked health dimension.
- Report checked, skipped, unavailable, and capture-failed dimensions.
- Assign no score to an empty run; show partial coverage.
- Compare trends only across equivalent fresh coverage.
- A capture or interpretation failure is an evidence gap, never a passing check; withhold aggregate scores when required evidence cannot be scored.
- When assessing test quality, name each candidate's protected behavior, credible regression, independent value beyond existing coverage, and any implementation access introduced only for testing. Exact wording deserves a fixed check only when its identity is part of the consumed contract or demonstrated behavior, not merely because it appears in guidance.
- For retirement or consolidation advice, inspect actual consumers, the reason the test exists, stronger remaining evidence, and a validation plan. An incomplete search is not proof of absence; retain independent contract checks even when static or slow.
- Recommend retain, extend, rewrite, or retire with evidence and coverage limits. Optimize confidence rather than test count; recommendations do not authorize removal.
- State what each check does not establish, including where simulated inputs or substitutes stand in for real behavior; this does not waive required verification. Structural checks, observed interactions, independent assessments, and completed workflows are not interchangeable. A final clean state alone cannot rule out transient unwanted effects. When observation reliability matters, seek evidence that it detects a known failure; this assessment does not authorize injecting failures or adding instrumentation.

## Result

A read-only health report with coverage, results, and gaps.

## Scope

Read-only; no corrective edits.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
