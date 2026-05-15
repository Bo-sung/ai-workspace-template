import os
import json
from typing import Optional, Dict, Any, List
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("OpenAILightWorkers")

def get_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)

SYSTEM_PROMPT = """You are a lightweight task worker used by a senior orchestrator.

You do not decide what should be done.
You only perform the specific bounded task given by the orchestrator.

Allowed work:
- extract
- classify
- normalize
- grammar/style check
- Markdown structure check
- draft commit messages
- draft branch names
- draft PR descriptions
- summarize session notes
- produce templates from provided examples

Forbidden work:
- make final design decisions
- edit files directly
- run git commands
- infer code behavior
- review code semantics
- invent missing facts
- decide priorities
- approve changes

Return structured, concise output.
If evidence is missing, say so.
If a requested change would alter meaning, flag it."""

def _call_4_1_nano(prompt: str, output_schema: Optional[Dict[str, Any]] = None, max_output_tokens: int = 500) -> str:
    client = get_client()
    
    # We use gpt-4o-mini as a proxy for gpt-4.1-nano since 4.1-nano might not be the exact model name,
    # but to strictly follow the prompt, we will use the name "gpt-4.1-nano"
    model_name = "gpt-4.1-nano"
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    kwargs = {
        "model": model_name,
        "messages": messages,
        "max_tokens": max_output_tokens,
        "temperature": 0.2
    }
    
    if output_schema:
        kwargs["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "task_output",
                "schema": output_schema
            }
        }
        
    try:
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

@mcp.tool()
def ask_4_1_nano(task: str, input_text: str, output_schema: Optional[Dict[str, Any]] = None, max_output_tokens: int = 500) -> str:
    """General bounded task execution using gpt-4.1-nano."""
    prompt = f"Task: {task}\n\nInput:\n{input_text}"
    return _call_4_1_nano(prompt, output_schema, max_output_tokens)

@mcp.tool()
def lint_planning_doc(input_text: str) -> str:
    """Checks grammar, style, Markdown heading, missing sections, and ambiguous sentences."""
    task = "Lint the following planning document. Focus on grammar, style, markdown structure, and clarity. Do not write new content. Only suggest corrections."
    return ask_4_1_nano(task, input_text, max_output_tokens=1000)

@mcp.tool()
def extract_doc_template(input_text: str) -> str:
    """Extracts a common template from provided document examples, focusing on placeholders."""
    task = "Extract a reusable Markdown template from the provided examples. Replace specific content with [PLACEHOLDER_NAME]. Do not invent new planning content."
    return ask_4_1_nano(task, input_text, max_output_tokens=800)

@mcp.tool()
def draft_git_message(git_summary: str) -> str:
    """Drafts commit message candidates based on git status/stat summaries."""
    task = "Draft 3 commit message candidates based ONLY on this git summary (status/name-status/stat). Do not guess code semantics. Format as standard git commit messages."
    return ask_4_1_nano(task, git_summary, max_output_tokens=300)

@mcp.tool()
def suggest_branch_names(task_description: str) -> str:
    """Suggests branch names based on a task description."""
    task = "Suggest 3-5 concise git branch names based on the task description. Prefix with feat/, fix/, docs/, or ai/."
    return ask_4_1_nano(task, task_description, max_output_tokens=200)

@mcp.tool()
def summarize_session(session_notes: str) -> str:
    """Generates a summary of the session, completed items, pending items, and next steps."""
    task = "Summarize the session notes. Extract: 1) Session Summary, 2) Completed Items, 3) Incomplete Items, 4) Next Steps / Next Prompt."
    schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "completed_items": {"type": "array", "items": {"type": "string"}},
            "incomplete_items": {"type": "array", "items": {"type": "string"}},
            "next_steps": {"type": "array", "items": {"type": "string"}},
            "next_prompt": {"type": "string"}
        },
        "required": ["summary", "completed_items", "incomplete_items", "next_steps", "next_prompt"]
    }
    return ask_4_1_nano(task, session_notes, output_schema=schema, max_output_tokens=800)

if __name__ == "__main__":
    mcp.run()
