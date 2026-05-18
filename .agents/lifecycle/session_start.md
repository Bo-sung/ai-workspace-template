# Session Start Checklist

1. Read the agent entrypoint: `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`.
2. Read `.agents/README.md`.
3. Read `.agents/state/session_registry.md`.
4. Read `.agents/rules/module_permissions.md`.
5. Read `.agents/state/resource_locks.md`.
6. Read `.agents/state/current_progress.md`.
7. Read the handoff file for the intended Role.
8. If no Role is assigned, remain read-only.
9. If the intended Role is free, register the session.
10. If the intended Role is occupied, stop and report to the user.
11. Treat the registered Role as locked for the session unless the coordinator
    explicitly changes it and updates the registry first.
