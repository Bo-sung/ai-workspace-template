# Domain Policy

This repository is currently a game design and documentation repository, not a Unity project or runtime application repository.

## Current Domain Rules

- Treat `시스템/**`, `세계관/**`, root design docs, and `assets/**` as design source material.
- Do not rewrite multiple design domains in one task without a clear Role assignment and lock plan.
- Binary image assets under `assets/**` may be inspected freely but should not be replaced or regenerated without user confirmation.
- HTML UI mockups under `assets/ui/**` belong to `UI_ASSETS`. If behavior or layout is changed, visually verify it when practical.
- Archived legacy memory under `.agents/backups/**` is not canonical design state.

## If A Unity Project Is Added Later

- `.unity`, `.prefab`, `.asset`, and `.meta` files are readable but require user confirmation before modification.
- Unity Play mode is run by the user.
- Agents may read logs to infer causes, but should not run editor menu actions, prefab regeneration, scene setup tools, or generators without explicit instruction.
- Runtime logging must use the project standard logger. Do not introduce raw `Debug.Log` unless the project explicitly defines it as the standard.

## If Backend Or Data Work Is Added Later

- Database migrations, production environment settings, secrets, and deployment configuration require a lock plus user confirmation.
- Original data must not be overwritten. Use separate output folders for generated or transformed data.
