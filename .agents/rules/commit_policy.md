# Commit Policy

## Git Location

- Project root: `H:\Git\FantasyTowerDeffence_docs`
- Git root: `H:\Git\FantasyTowerDeffence_docs`
- Standard command form: `git -C H:\Git\FantasyTowerDeffence_docs <command>`

The project root and Git root currently match. Keep using `git -C` in instructions and automation so the rule remains safe if the working directory changes.

## Before Commit

1. Run `git -C H:\Git\FantasyTowerDeffence_docs status`.
2. Run `git -C H:\Git\FantasyTowerDeffence_docs diff` for tracked changes.
3. Review untracked files.
4. Separate current-agent changes from pre-existing user changes.
5. Check for sensitive files, generated files, binary replacements, and lock conflicts.
6. Run relevant validation for the touched files.
7. Update progress or handoff only if the task outcome changed.

## Commit Message Style

Existing history uses conventional prefixes such as `docs:`, `feat:`, and `refactor:`.

Use concise messages in that style. For operating-document work, prefer:

`docs: 에이전트 운영 체계 추가`

Do not add generated co-author lines, model signatures, tool signatures, or unrelated automatic text.

## After Commit

Report the commit hash and remaining working tree status.
