# Codex Handoff Prompt

When Codex tokens are recharged, paste the following prompt to Codex to initialize it with the new infrastructure:

---

**Initialize Shared AI Tools Infrastructure**

I have built a shared AI tools infrastructure in `.shared-ai-tools/`.
Please read `.shared-ai-tools/docs/architecture.md` and `.shared-ai-tools/prompts/remote_worker_policy.md` to understand the setup.

Your tasks:
1. Review the available MCP server configurations in `.shared-ai-tools/config-snippets/`.
2. Add the `worker_router` and `openai_light_workers` MCP servers to your `config.toml` using the provided snippets.
3. Verify connection to the MCP servers by running `list_workers` tool.
4. Confirm you understand the division of labor: You are the Orchestrator (decision maker, Git committer, code editor), and you should delegate summarization, drafting, and linting tasks to the MCP worker tools.
5. Review `AGENTS.md` and `GEMINI.md` to sync with the updated Remote AI Worker Policy.
