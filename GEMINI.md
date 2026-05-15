# GEMINI.md

Gemini entrypoint for this repository.

Before doing any work, read `.agents/README.md` and follow the lifecycle documents under `.agents/lifecycle/`.

If Gemini is used as `COORDINATOR`, it should coordinate work, detect conflicts, prepare task prompts, review results, and update operating state. It should not directly edit project content unless the user explicitly assigns a Worker Role.

Current state must remain in:

- `.agents/state/session_registry.md`
- `.agents/state/resource_locks.md`
- `.agents/state/current_progress.md`


# Remote AI Worker Policy

The desktop AI CLI session is the orchestrator. Remote local LLMs and OpenAI lightweight workers are low-risk task workers.

## Orchestrator

Gemini CLI or Codex is responsible for:
- task planning
- work decomposition
- selecting input scope
- reviewing worker outputs
- applying final changes
- deciding schedules
- deciding priorities
- Git operations

## Remote local workers

Remote local LLM workers are accessed through the worker_router MCP server.

Available initial workers:
- laptop-gemma-e2b
- macmini-exaone
- macmini-qwen

Use local workers for:
- document summarization
- planning note cleanup
- GDD section extraction
- TODO extraction
- QA report formatting
- Git commit message drafts
- PR description drafts
- release note drafts
- issue draft generation

Do not use local workers for:
- source code writing
- source code editing
- source code review
- architecture decisions
- final design decisions
- final prioritization decisions
- git commit
- git push
- git merge
- git rebase
- merge conflict resolution

## OpenAI lightweight worker

Use openai_light_workers with gpt-4.1-nano for:
- grammar/style checks
- Markdown structure checks
- document template extraction
- commit message drafts
- branch name suggestions
- session summaries
- low-risk normalization tasks

Do not use gpt-4.1-nano for:
- final decisions
- code reasoning
- Git execution
- file modification
- priority decisions
- schedule decisions

## Task sizing

For laptop / gemma4:e2b:
- one objective per call
- input under 1,500 tokens if possible
- output under 500 tokens by default

For macmini / 7B-8B models:
- one objective per call
- input under 4,000 tokens if possible
- output under 1,000 tokens by default

For gpt-4.1-nano:
- one bounded task per call
- prefer structured JSON output
- avoid source code full diffs
- use git status/name-status/stat instead of full diff

## Git workflow

Default:
- Workers produce text outputs only.
- Workers do not run git write commands.
- Codex/Gemini or the user handles Git operations.

Allowed read-only Git commands:
- git status
- git diff --name-status
- git diff --stat
- git log

Forbidden for workers:
- git add
- git commit
- git push
- git merge
- git rebase
- conflict resolution

## Project management

Initial project management uses Google Sheets.
Obsidian Markdown remains the source of truth for planning documents.
Git manages versions of code and Obsidian documents.
The Google Sheets schema should be migration-friendly for future GitHub Issues / GitHub Projects adoption.

## Review rule

All worker output is draft material.
The orchestrator must review, integrate, and state uncertainties.
