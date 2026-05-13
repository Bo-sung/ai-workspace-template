# OPS/COORDINATION Handoff

## Setup Notes

- The operating framework files exist under `.agents/`.
- Legacy memory is archived at `.agents/backups/2026-05-12_0623/메모리/`.
- For active sessions, locks, and progress, read `.agents/state/`.

## Next Session Notes

- Keep entrypoint files thin.
- Update only `.agents/state/session_registry.md`, `.agents/state/resource_locks.md`, and `.agents/state/current_progress.md` for live state.
- If another Role needs a path outside its ownership, require a lock or user confirmation.
