# Domain Policy

This reusable agent OS does not assume a single project domain. The active
project domain should be described by `.agents/project/domain.md` or another
overlay file under `.agents/project/`.

If no project domain overlay exists, use conservative defaults: read first,
avoid broad rewrites, and ask for approval before editing runtime, generated, or
sensitive files.

## General Domain Rules

- Treat canonical project documents, architecture contracts, glossaries,
  roadmaps, and README files as shared resources unless the overlay says
  otherwise.
- Do not rewrite multiple domains in one task without a clear Role assignment
  and lock plan.
- Binary assets may be inspected freely but should not be replaced or regenerated
  without user confirmation.
- Generated outputs should not overwrite original data. Use separate output
  folders for generated or transformed data.
- Archived legacy memory under `.agents/backups/**` is not canonical current
  state.

## Unity Or Game Client Projects

- `.unity`, `.prefab`, `.asset`, and `.meta` files are readable but require user
  confirmation before broad or automated modification.
- Unity Play mode is normally run by the user unless the project overlay says
  otherwise.
- Agents may read logs to infer causes, but should not run editor menu actions,
  prefab regeneration, scene setup tools, or generators without explicit
  instruction.
- Runtime logging must use the project standard logger. Do not introduce raw
  engine logging unless the project explicitly defines it as the standard.

## Backend, Data, Or Infrastructure Projects

- Database migrations, production environment settings, secrets, and deployment
  configuration require a lock plus user confirmation.
- Schema changes should include migration, rollback, and data-integrity notes
  when the project uses persistent storage.
- Network calls, dependency downloads, and external service changes require the
  normal sandbox/escalation flow.

## Documentation Projects

- Preserve the current document hierarchy unless the user asks for reorganization.
- Prefer small, traceable edits over broad rewrites.
- When a term, scope item, or architecture decision is not settled, mark it as
  pending instead of silently deciding it.
