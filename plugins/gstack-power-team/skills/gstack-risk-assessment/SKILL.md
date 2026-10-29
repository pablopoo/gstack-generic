---
name: gstack-risk-assessment
description: "Assess security, safety, privacy, or misuse risk for a defined surface."
---

# Risk Assessment

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- assessed scope
- assets and trust boundaries
- actors and abuse paths

Use available evidence; identify missing information only when it changes the decision.

## Method

- Define scope, boundaries, assets, actors, and abuse paths.
- Separate supported findings from hypotheses and coverage gaps.
- Calibrate severity from reachability, impact, likelihood, and controls; keep unknown reachability explicitly unknown.
- Report complete, partial, or unassessed coverage.
- Give each supported finding a repair or verification action. For a validated cause, inspect other in-scope entry points for the same pattern; establish each variant's reachability, impact, and evidence independently rather than copying the first finding's verdict.
- Record freshness, confidence, and counterevidence separately from severity; fresh evidence is required to close an earlier finding.
- Assess the actual representation crossing each relevant boundary, including transformations. Unavailable or incomplete checks remain unassessed; report limits without exposing sensitive content.

## Result

A scope-labeled risk assessment with evidence and next actions.

## Scope

Read-only unless remediation is separately authorized.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
