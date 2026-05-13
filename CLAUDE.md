# CLAUDE.md

Claude Code entrypoint for this repository.

Before doing any work, read `.agents/README.md` and follow the lifecycle documents under `.agents/lifecycle/`.

Project state is not kept in Claude-specific memory or this file. The single sources of truth are:

- `.agents/state/session_registry.md`
- `.agents/state/resource_locks.md`
- `.agents/state/current_progress.md`

Local Claude settings, hooks, or skills may exist under `.claude/`, but they must point back to `.agents/` for operating rules and must not duplicate current status.
