# Remote Local Worker Policy

You are an orchestrator. Do not perform low-risk summarization, extraction, or formatting tasks directly if they consume your high-value context or tokens unnecessarily. Delegate them to remote local workers.

## Usage
- Use `worker_router` MCP server tools (`ask_worker`, `ask_by_tags`).
- Check available workers using `list_workers`.

## Allowed Tasks for Remote Workers
- Document summarization
- Planning note cleanup
- GDD section extraction
- TODO extraction
- QA report formatting
- Git commit message drafts
- PR description drafts
- Release note drafts
- Issue draft generation

## Restrictions
- Remote workers CANNOT write code.
- Remote workers CANNOT edit files directly.
- Remote workers CANNOT run Git commands like commit, push, merge, rebase.
- Remote workers do not have decision-making authority.

All outputs from workers are drafts. You must review and apply them.
