# Model Capabilities Guide

This guide helps the Orchestrator (Coordinator) choose the right tool for the job.

## Expert Cloud Workers

### Claude 3.5 Sonnet / Opus
- **Strengths:** Complex coding, UI/UX design, precise instruction following, creative worldbuilding.
- **Best for:** Core game mechanics, UI architecture, narrative consistency.

### Gemini 1.5 Pro (Flash/High)
- **Strengths:** Long context reasoning, project-wide analysis, multi-modal tasks, rapid prototyping.
- **Best for:** Large codebase refactoring, summarizing long GDDs, cross-referencing multiple files.

### Codex / GPT-4o / o1
- **Strengths:** Logic puzzles, mathematical balance, structured data generation.
- **Best for:** Combat balance tables, KPI architecture, server-side logic.

## Remote Local Workers

### Gemma-2b / 7b
- **Strengths:** Low latency, privacy, basic text manipulation.
- **Best for:** TODO extraction, grammar checks, simple summaries.

### Exaone / Qwen (7B-14B)
- **Strengths:** Specialized reasoning, regional language nuances.
- **Best for:** Korean text repair, cultural localization.

## OpenAI Lightweight (gpt-4.1-nano)
- **Best for:** Markdown linting, commit message drafts, JSON normalization.
