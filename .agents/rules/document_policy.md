# Document Policy

## Allowed Operating Documents

Operating documents may live under:

- `.agents/rules/*.md`
- `.agents/lifecycle/*.md`
- `.agents/state/*.md`
- `.agents/handoff/*.md`
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `PROJECT_QUICK_REFERENCE.md`

Backups of legacy state may live under `.agents/backups/`.

## Do Not Create By Default

Do not create standalone explanation documents, analysis reports, prompt collections, test checklists, or meeting-style notes unless the user explicitly asks.

Temporary reasoning and analysis should be delivered in chat. Durable operating state belongs only in the approved state or handoff files.

## State Duplication Ban

- Do not duplicate active session status outside `.agents/state/session_registry.md`.
- Do not duplicate active locks outside `.agents/state/resource_locks.md`.
- Do not duplicate project progress outside `.agents/state/current_progress.md`.
- Do not mirror live state into agent-specific files.

## Legacy Notes

Archived notes are references, not current truth. To make an archived note actionable, integrate only the needed next step into `.agents/state/current_progress.md` or a Role handoff file.
