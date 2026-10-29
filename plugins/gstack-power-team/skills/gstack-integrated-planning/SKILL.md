---
name: gstack-integrated-planning
description: "Turn a proposed plan into an ordered, testable delivery plan."
---

# Integrated Plan Review

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../../NOTICE.md).

## Inputs

- proposed plan
- desired outcome
- constraints and affected areas

Use available evidence; identify missing information only when it changes the decision.

## Method

- Test whether the plan addresses a real problem and outcome.
- Challenge scope, wedge, assumptions, and exclusions.
- Review experience and operator consequences where material. Failure feedback should distinguish rejection from partial or unknown effects, agree across human and automated signals where applicable, name safe recovery and retry limits, and provide stable identification and useful diagnostics without exposing sensitive information.
- Amend the plan from product and experience findings, preserve accepted requirements, then review architecture, sequence, risk, and verification against that final plan.
- Turn unresolved choices into owned decision gates. Keep independently selectable changes separate, preserve accepted commitments across alternatives, and do not treat a navigation choice as implementation approval.
- Distinguish the accepted plan, proposed amendments, reviewer inputs, and completed reconciliation. Resume at the first incomplete obligation; artifact existence or acknowledgement alone does not establish review completion.

## Result

An amended plan with ordered work, acceptance evidence, and open decisions.

## Scope

Planning and critique only.

Apply within the authorized local development scope. Choose means from the project's existing conventions. Scale evidence to the consequence of error and disclose material limitations.

## Related Work

For a dependency spanning methods, consult [the process map](../../references/process-map.md). For useful independent collaboration, consult [the delegation contract](../../references/delegation-contract.md). Neither is a required extra phase for a self-contained task.
