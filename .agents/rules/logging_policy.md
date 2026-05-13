# Logging Policy

This repository currently contains design documents and assets, so runtime logging is usually not applicable.

## Operating Logs

- Active session status belongs only in `.agents/state/session_registry.md`.
- Active locks belong only in `.agents/state/resource_locks.md`.
- Progress belongs only in `.agents/state/current_progress.md`.
- Long console logs, debugging transcripts, and analysis dumps should stay in chat unless the user asks for a durable artifact.

## Future Code Repositories

- Use the project's standard logger.
- Do not introduce raw `Debug.Log`, `console.log`, or ad hoc print logging in production code unless that is the established project standard.
- If logging behavior changes, note the verification result in the task summary or progress file.
