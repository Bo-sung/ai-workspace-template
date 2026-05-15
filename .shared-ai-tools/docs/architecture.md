# Architecture of Shared AI Tools

The Shared AI Tools infrastructure is designed to provide a uniform toolset for both Gemini CLI and Codex, standardizing the use of remote local LLMs (via SSH) and lightweight OpenAI models for low-risk, bounded tasks.

## Components

1. **`workers.yaml`**: The single source of truth for the remote worker registry. It avoids hardcoding hosts, models, and limits.
2. **`worker_router_mcp.py`**: An MCP server that reads `workers.yaml` and executes remote tasks via SSH and the local Ollama API. It exposes tools for orchestrators to use.
3. **`openai_light_mcp.py`**: An MCP server wrapping `gpt-4.1-nano` for deterministic, bounded normalization and summarization tasks.
4. **Docs & Prompts**: Standard operating procedures, schemas, and instructions ensuring both Gemini and Codex treat workers identically.

## Security & Principles
- **Orchestrator Pattern**: Gemini/Codex handles decisions, project state, and Git operations. Workers only provide draft content.
- **SSH Key Auth**: Passwordless execution to remote local machines.
- **Read-Only Git for Workers**: Remote workers can only read Git state. Writing is strictly for the orchestrator/user.
