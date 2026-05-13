# AGENTS.md

Codex entrypoint for this repository.

Before doing any work, read `.agents/README.md` and follow the lifecycle documents under `.agents/lifecycle/`.

Do not store current session state, locks, progress, or handoff notes in this file. The single sources of truth are:

- `.agents/state/session_registry.md`
- `.agents/state/resource_locks.md`
- `.agents/state/current_progress.md`

If no Role is assigned in the session registry, operate read-only until the user assigns or approves a Role.
