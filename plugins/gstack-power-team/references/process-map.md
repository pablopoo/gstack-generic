# Development Process

Modification notice: Rewritten and consolidated by Pablo Poo. Attribution and applicable terms: [NOTICE](../NOTICE.md).

Use the smallest set of methods that resolves the requested outcome. Existing decisions and reliable evidence satisfy dependencies; the phases are not a compulsory itinerary.

| Decision needed | Evidence to use | Result needed by the next phase |
| --- | --- | --- |
| Is this worth doing? | User needs, observed problems, constraints, alternatives | Problem framing and scope decision |
| What must change? | Accepted intent and current behavior | Acceptance criteria, boundaries, unresolved choices |
| How should it work? | Experience needs, responsibilities, dependencies, failure modes | Design decisions and feasible sequence |
| Is the change correct? | Actual changed behavior, expected outcomes, relevant unchanged behavior | Supported findings and verification evidence |
| Is local work ready to hand over? | Current review, actual verification coverage, remaining risks | Readiness judgment and next owner |
| What should be retained? | Observed outcomes and decision rationale | Updated knowledge and targeted process improvements |

## Dependencies

- Resolve uncertain demand and scope before expensive solution design.
- For integrated planning, evaluate product and experience concerns first, amend the plan, then review engineering feasibility against that final plan. Preserve requirements and approved decisions across handoffs.
- Define acceptance evidence before implementing consequential changes. Select the simplest coherent approach consistent with established constraints.
- Distinguish investigation, which establishes causes, from correction, which changes behavior. A report-only request ends with findings.
- Evaluate design intent separately from observed usability; a plausible design is not evidence that the implemented interaction works.
- Base review on the actual relevant content. If it changes, review the affected conclusions again before claiming current coverage. A decision to accept a known limitation is not a claim that no limitation exists.
- Keep severity, confidence, review completion, and readiness distinct. An optional improvement may remain deferred when the agreed gate permits it; disclose the reason.
- Empty verification provides no assurance. Record failed attempts, skipped checks, missing evidence, and the scope actually observed.
- Select verification by the behavior at risk, including nonvisual behavior and durable effects. Keep different surfaces' coverage separate and preserve failures across retries.
- Assess test quality or reuse opportunities within health assessment or implementation assessment when relevant. Their advice is not a required extra phase and does not authorize cleanup.
- Required verification remains required when optional exploration ends. A deferred repair remains unresolved; acceptance of a limitation does not turn missing proof into a pass.
- Local readiness depends on the requested acceptance criteria and an honest account of remaining risk. It does not authorize publication or deployment.
- Preserve useful decisions, deliberate shortcuts, owners, and observable revisit conditions. Reconsider them when evidence changes.

## Selecting Methods

Use [the method index](method-index.md) to select the required artifact or decision. Read only the selected methods. Use [the delegation contract](delegation-contract.md) when distinct independent work warrants collaboration, and [collaboration responsibilities](collaboration-roles.md) only when role selection is unresolved.

Stop when the requested result has appropriate evidence, or identify the specific missing decision or unavailable evidence. Do not repeat successful reviews solely to complete a ritual.
