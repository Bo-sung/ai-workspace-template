# Worker Session Prompt Template

Use this template for the copyable prompt sent to a worker session.

Do not include coordinator-only allocation notes here unless the user explicitly
asks for them. Model tier, candidate models, tier rationale, and escalation
rationale belong outside this prompt.

Style rule:

- Dry and direct.
- Include only execution-critical information.
- Omit praise, framing, rationale that does not change execution, and other
  non-essential prose.

## Role

You are the `<ROLE>` worker session for Frontier Bastion.

## Task

Describe the concrete task the worker must complete.

## Repository

- Read:
- Modify:

## Allowed Paths

- Add allowed paths here.

## Forbidden Paths

- Add forbidden paths here.

## Read First

- Add required reading here.

## Work Items

1.
2.
3.

## Completion Criteria

- Add completion criteria here.

## Validation

- Add validation steps here.

## Stop And Report If

- A shared contract, public API, DB schema, Config schema, reward/resource rule,
  deterministic combat rule, package/solution setting, or multi-repo change is
  required.
- The work exceeds the assigned Role or allowed paths.
- Existing user changes would need to be overwritten.

## Report Format

1. Files read or changed
2. What was done
3. Validation result
4. Blockers or risks
5. Suggested next step

## Session Boundary

This prompt assigns work to a new worker session. It does not change the Role of
the lead session that authored it.
