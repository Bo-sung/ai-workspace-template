# OpenAI Lightweight Worker Policy

You are an orchestrator. Use the `openai_light_workers` MCP server for fast, cheap, structural tasks.

## Usage
- Use the provided tools like `ask_4_1_nano`, `lint_planning_doc`, `extract_doc_template`, `draft_git_message`, `suggest_branch_names`, `summarize_session`.

## Allowed Tasks
- Grammar/style checks
- Markdown structure validation
- Document template extraction
- Commit message drafting (from status/stat)
- Branch name suggestions
- Session summarization
- Normalizing text output

## Restrictions
- Do not use for source code reasoning or code editing.
- Do not use for file modification or Git execution.
- Do not ask it to invent facts or make architectural decisions.

The output is always a draft. Review before adopting.
