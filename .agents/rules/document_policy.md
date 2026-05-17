# Document Policy

## Allowed Operating Documents

Portable operating documents may live under:

- `.agents/rules/*.md`
- `.agents/lifecycle/*.md`
- `.agents/templates/*.md`
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `PROJECT_QUICK_REFERENCE.md`

Project-specific operating documents may live under:

- `.agents/state/*.md`
- `.agents/handoff/*.md`
- `.agents/project/**`

Generated, derived, or temporary agent data may live under:

- `.agents/cache/**`
- `.ai-cache/**`

Backups of legacy state may live under `.agents/backups/`.

## Reusable Base Rule

Do not put project-specific repository paths, module ownership, current progress,
or handoff details into reusable base rules unless this repository is explicitly
being used as the versioned control repo for that single project.

Preferred split:

- Tracked base rules describe how agents work in any project.
- `.agents/project/**` describes the current local project and is ignored by
  default.
- `.agents/state/**` and `.agents/handoff/**` describe live work and should stay
  concise.

## Do Not Create By Default

Do not create standalone explanation documents, analysis reports, prompt
collections, test checklists, or meeting-style notes unless the user explicitly
asks.

Temporary reasoning and analysis should be delivered in chat. Durable operating
state belongs only in the approved state, handoff, overlay, or cache locations.

## State Duplication Ban

- Do not duplicate active session status outside `.agents/state/session_registry.md`.
- Do not duplicate active locks outside `.agents/state/resource_locks.md`.
- Do not duplicate project progress outside `.agents/state/current_progress.md`.
- Do not mirror live state into agent-specific files.
- Do not copy project overlay content into reusable base rules.

## Legacy Notes

Archived notes are references, not current truth. To make an archived note
actionable, integrate only the needed next step into the current project state or
a Role handoff file.
