# Resource Policy

Shared resources are managed through `.agents/state/resource_locks.md`.

## Lock Targets

Acquire a lock before editing:

- Shared root documents and project-wide indexes
- Canonical glossary, roadmap, and progress documents
- Cross-Role design contracts
- Binary assets that may be replaced or regenerated
- Generated artifacts and generator outputs
- Build, deployment, environment, or tool configuration
- Any resource currently being edited by another session

## Acquiring A Lock

1. Re-read `.agents/state/resource_locks.md`.
2. Confirm the resource is not already locked.
3. Add a row with Type, Resource, Agent, Session, Role, Locked At, and Reason.
4. Re-read the file after editing if the work is high-risk.
5. Begin the edit only after the lock is visible.

## Releasing A Lock

Release the lock immediately after the edit is complete, blocked, or abandoned.

Never leave a lock as a reminder. Put reminders in the relevant handoff file or `current_progress.md`.

## Conflict Handling

If a lock already exists, stop and report to the user. Do not wait, override, or edit around another session's lock.

Stale locks are not expired automatically. Report them to the user with the lock row and the affected resource.

## State File Updates

Agents may update their own session row, lock row, progress entry, or handoff notes according to lifecycle rules. Re-read the file immediately before editing to avoid overwriting another session.
