# Lead Session Handoff Prompt Template

Use this template when one lead/coordinator session needs another lead session
to review, decide, unblock, or prepare worker-session instructions.

## Handoff Metadata

- From lead Role:
- To lead Role:
- Coordinator:
- Date:
- Handoff type:
  - consultation
  - dependency review
  - design review
  - ownership transfer
  - unblock request
  - worker-prompt review
- Related repositories:
- Related shared resources or locks:

## Why This Handoff Is Needed

Explain why the receiving lead session is needed and why the sender should not
decide this alone.

## Current State

- What is already known:
- What has already been decided:
- What work has already been completed:
- Relevant files or documents:

## Open Questions

1.
2.
3.

## Requested Action From The Receiving Lead

The receiving lead session should:

1.
2.
3.

The receiving lead session should not:

- Directly implement project work unless separately authorized.
- Change another Role's owned files without coordinator approval or the required
  lock.
- Turn unresolved questions into final decisions without identifying the needed
  approver.

## Delegation Guidance

If the receiving lead determines that worker-session work is needed, it should
return:

1. A coordinator-only allocation note containing:
   - Recommended model tier.
   - Candidate model names for that tier.
   - Reason for the tier choice.
   - Escalation conditions that would require a higher tier.
2. A separate clean copyable worker-session prompt.

Do not embed model-selection rationale inside the worker prompt unless the user
explicitly requests it.

Worker prompts should be dry, direct, and limited to execution-critical content.

## Required Reading

- Add required reading here.

## Constraints

- Registered Roles remain authoritative.
- Ordinary task prompts do not change a session Role.
- If this handoff requires shared contracts, DB schema, deterministic combat,
  public APIs, rewards/resources, or multiple repositories, identify the
  coordinator approval and lock requirements explicitly.

## Expected Return Format

1. Understanding of the handoff
2. Findings or design assessment
3. Recommended next action
4. Coordinator-only allocation notes for worker tasks, if any
5. Clean copyable worker-session prompts, if any
6. Required locks or coordinator decisions
7. Remaining risks or unanswered questions
