# GEMINI.md

Gemini entrypoint for this repository.

Before doing any work, read `.agents/README.md` and follow the lifecycle documents under `.agents/lifecycle/`.

If Gemini is used as `COORDINATOR`, it should coordinate work, detect conflicts, prepare task prompts, review results, and update operating state. It should not directly edit project content unless the user explicitly assigns a Worker Role.

Current state must remain in:

- `.agents/state/session_registry.md`
- `.agents/state/resource_locks.md`
- `.agents/state/current_progress.md`
