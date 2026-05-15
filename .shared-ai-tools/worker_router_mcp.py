import os
import sys
import yaml
import subprocess
import json
import traceback
import socket
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("WorkerRouter")

def load_workers() -> Dict[str, Any]:
    yaml_path = os.path.join(os.path.dirname(__file__), "workers.yaml")
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@mcp.tool()
def list_workers() -> str:
    """Returns a list of enabled workers and their models."""
    config = load_workers()
    workers = config.get('workers', [])
    
    result = []
    for w in workers:
        if not w.get('enabled', False):
            continue
        worker_info = f"Worker ID: {w['id']} (Host: {w['host']}, OS: {w['os']})\n"
        for m in w.get('models', []):
            worker_info += f"  - Model: {m['name']} | Tags: {', '.join(m.get('tags', []))} | Priority: {m.get('priority', 0)} | Tokens: {m.get('max_input_tokens', 0)} in / {m.get('max_output_tokens', 0)} out\n"
        result.append(worker_info)
    
    return "\n".join(result) if result else "No enabled workers found."

@mcp.tool()
def health_check_workers() -> str:
    """Checks the health of all enabled workers via SSH."""
    config = load_workers()
    workers = [w for w in config.get('workers', []) if w.get('enabled', False)]
    
    results = []
    for w in workers:
        host = w['host']
        port = str(w.get('port', 22))
        user = w.get('user', '')
        target = f"{user}@{host}" if user else host
        python_cmd = w.get('python_cmd', 'python')
        
        # We use a combined command to check everything quickly, including Ollama API
        check_cmd = f"hostname && {python_cmd} --version && git --version && {python_cmd} -c \"import urllib.request; urllib.request.urlopen('http://127.0.0.1:11434/api/tags', timeout=2)\" && echo API_OK || echo API_FAIL"
        
        try:
            # BatchMode=yes prevents password prompts and fails immediately if keys are not set up
            output = subprocess.check_output(
                ["ssh", "-p", port, "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", target, check_cmd],
                stderr=subprocess.STDOUT,
                timeout=15,
                text=True
            )
            
            if "API_OK" in output:
                results.append(f"[OK] Worker {w['id']} ({host}): SSH, Git, Python, and Ollama are reachable.")
            else:
                results.append(f"[WARN] Worker {w['id']} ({host}): SSH connected, but Ollama API check failed.\nOutput:\n{output}")
        except subprocess.TimeoutExpired:
            results.append(f"[FAIL] Worker {w['id']} ({host}): Connection timed out.")
        except subprocess.CalledProcessError as e:
            results.append(f"[FAIL] Worker {w['id']} ({host}): SSH command failed (Check if SSH key auth works without password). \nError: {e.output.strip()}")
            
    return "\n\n".join(results)

@mcp.tool()
def wake_worker(worker_id: str) -> str:
    """Sends a Wake-On-LAN (WOL) magic packet to boot a remote worker."""
    config = load_workers()
    worker = next((w for w in config.get('workers', []) if w.get('id') == worker_id), None)
    
    if not worker:
        return f"Error: Worker {worker_id} not found."
    
    mac = worker.get('mac_address')
    if not mac or "TODO" in mac:
        return f"Error: MAC address for worker {worker_id} is not configured."
        
    try:
        # Clean MAC address and build magic packet
        mac_clean = mac.replace(':', '').replace('-', '')
        if len(mac_clean) != 12:
            return f"Error: Invalid MAC address format: {mac}"
            
        data = bytes.fromhex('FF' * 6 + mac_clean * 16)
        
        wol_port = int(worker.get('wol_port', 9))
        target_host = worker.get('host', '255.255.255.255')
        
        # Send to the specific host and port
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(data, (socket.gethostbyname(target_host), wol_port))
            
        return f"Success: Magic packet sent to {worker_id} ({mac}) via {target_host}:{wol_port}. Please wait 1-2 minutes for boot."
    except Exception as e:
        return f"Error sending WOL packet: {str(e)}"

SYSTEM_PROMPT = """You are a small remote local LLM worker used by Gemini CLI or Codex.

You may:
- summarize documents
- extract TODOs
- classify planning notes
- draft commit messages from git summaries
- draft PR descriptions
- format QA reports
- draft release notes
- normalize document structure

You must not:
- edit source code
- review source code semantics
- make architecture decisions
- make final design decisions
- run git commit, push, merge, or rebase
- invent facts not in the input
- decide priorities

Return concise structured output.
If unsure, explicitly list uncertainties.
All output is draft material for the orchestrator to review."""

def _call_remote_ollama(worker: Dict[str, Any], model_name: str, task: str, input_text: str, output_format: str, num_ctx: int, temperature: float, max_output_tokens: int) -> str:
    host = worker['host']
    port = str(worker.get('port', 22))
    user = worker.get('user', '')
    target = f"{user}@{host}" if user else host
    python_cmd = worker.get('python_cmd', 'python')
    
    prompt = f"Task:\n{task}\n\nFormat:\n{output_format}\n\nInput:\n{input_text}"
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "options": {
            "num_ctx": num_ctx,
            "temperature": temperature,
            "num_predict": max_output_tokens
        },
        "stream": False,
        "keep_alive": 0
    }
    
    payload_json = json.dumps(payload).replace("'", "'\\''")
    
    # Send curl command and touch active file for auto-shutdown service
    cmd = f"touch ~/.ai_worker_active 2>/dev/null; curl -s -X POST http://127.0.0.1:11434/api/chat -H 'Content-Type: application/json' -d '{payload_json}'"
    
    try:
        output = subprocess.check_output(
            ["ssh", "-p", port, "-o", "BatchMode=yes", target, cmd],
            stderr=subprocess.STDOUT,
            timeout=120,
            text=True
        )
        res = json.loads(output)
        if "message" in res and "content" in res["message"]:
            return res["message"]["content"]
        return f"Error: Unexpected response format: {output}"
    except Exception as e:
        return f"Error executing remote request: {str(e)}"

@mcp.tool()
def ask_worker(worker_id: str, model: str, task: str, input_text: str, output_format: str = "text", max_output_tokens: int = 500, num_ctx: int = 4096, temperature: float = 0.2, user_approved: bool = False) -> str:
    """Executes a task on a specific remote worker using its local LLM."""
    if "exaone" in model.lower() and not user_approved:
        return "ERROR_LICENSE: EXAONE is restricted to Non-Commercial (NC) use. You MUST explicitly ask the USER for permission to use this model. If the USER approves, call this tool again with user_approved=True."
        
    config = load_workers()
    worker = next((w for w in config.get('workers', []) if w.get('id') == worker_id), None)
    
    if not worker:
        return json.dumps({"error": f"Worker {worker_id} not found."})
    
    if not worker.get('enabled', False):
         return json.dumps({"error": f"Worker {worker_id} is disabled."})
         
    model_config = next((m for m in worker.get('models', []) if m.get('name') == model), None)
    if not model_config:
         return json.dumps({"error": f"Model {model} not found in worker {worker_id}."})
         
    warnings = []
    if max_output_tokens > model_config.get('max_output_tokens', max_output_tokens):
        warnings.append(f"Warning: Requested max_output_tokens ({max_output_tokens}) exceeds model's configured max ({model_config.get('max_output_tokens')}).")
    
    result = _call_remote_ollama(worker, model, task, input_text, output_format, num_ctx, temperature, max_output_tokens)
    
    return json.dumps({
        "worker_id": worker_id,
        "model": model,
        "warnings": warnings,
        "result": result
    }, ensure_ascii=False)

@mcp.tool()
def ask_by_tags(preferred_tags: List[str], task: str, input_text: str, output_format: str = "text", max_output_tokens: int = 500, num_ctx: int = 4096, temperature: float = 0.2) -> str:
    """Executes a task on the most appropriate worker/model based on preferred tags and priority."""
    config = load_workers()
    workers = [w for w in config.get('workers', []) if w.get('enabled', False)]
    
    candidates = []
    for w in workers:
        for m in w.get('models', []):
            tags = m.get('tags', [])
            # Calculate match score based on how many preferred tags are present
            match_score = len(set(preferred_tags).intersection(set(tags)))
            if match_score > 0:
                candidates.append({
                    "worker": w,
                    "model": m,
                    "score": match_score,
                    "priority": m.get('priority', 0)
                })
                
    if not candidates:
        return json.dumps({"error": "No available models matching the preferred tags."})
        
    # Sort by match_score (desc), then priority (desc)
    candidates.sort(key=lambda x: (x['score'], x['priority']), reverse=True)
    best = candidates[0]
    
    warnings = []
    if best['score'] < len(preferred_tags):
        warnings.append("Warning: Fallback occurred. Not all preferred tags were matched.")
        
    result = _call_remote_ollama(best['worker'], best['model']['name'], task, input_text, output_format, num_ctx, temperature, max_output_tokens)
    
    return json.dumps({
        "worker_id": best['worker']['id'],
        "model": best['model']['name'],
        "warnings": warnings,
        "result": result
    }, ensure_ascii=False)

@mcp.tool()
def remote_git_snapshot(worker_id: str, repo_path: str) -> str:
    """Gathers read-only git state from a remote worker's repository."""
    config = load_workers()
    worker = next((w for w in config.get('workers', []) if w.get('id') == worker_id and w.get('enabled', False)), None)
    
    if not worker:
        return f"Error: Worker {worker_id} not found or disabled."
        
    host = worker['host']
    port = str(worker.get('port', 22))
    user = worker.get('user', '')
    target = f"{user}@{host}" if user else host
    
    # We run safe git commands separated by markers
    cmds = [
        f"cd {repo_path} || exit 1",
        "echo '=== BRANCH ==='",
        "git branch --show-current",
        "echo '=== STATUS ==='",
        "git status --short",
        "echo '=== DIFF CACHED STAT ==='",
        "git diff --cached --stat",
        "echo '=== DIFF STAT ==='",
        "git diff --stat"
    ]
    
    full_cmd = " && ".join(cmds)
    
    try:
        output = subprocess.check_output(
            ["ssh", "-p", port, "-o", "BatchMode=yes", target, full_cmd],
            stderr=subprocess.STDOUT,
            timeout=30,
            text=True
        )
        return output
    except Exception as e:
        return f"Error executing git snapshot: {str(e)}"

@mcp.tool()
def remote_create_artifact_branch(worker_id: str, repo_path: str, branch_name: str, base_ref: str = "main") -> str:
    """Creates a new branch for artifacts on a remote worker. Branch name must start with 'ai/'."""
    if not branch_name.startswith("ai/"):
        return "Error: branch_name must start with 'ai/' for artifact branches."
        
    config = load_workers()
    worker = next((w for w in config.get('workers', []) if w.get('id') == worker_id and w.get('enabled', False)), None)
    
    if not worker:
        return f"Error: Worker {worker_id} not found or disabled."
        
    host = worker['host']
    port = str(worker.get('port', 22))
    user = worker.get('user', '')
    target = f"{user}@{host}" if user else host
    
    cmds = [
        f"cd {repo_path} || exit 1",
        "git fetch origin",
        f"git checkout {base_ref}",
        "git pull --ff-only",
        f"git checkout -B {branch_name}"
    ]
    
    full_cmd = " && ".join(cmds)
    
    try:
        output = subprocess.check_output(
            ["ssh", "-p", port, "-o", "BatchMode=yes", target, full_cmd],
            stderr=subprocess.STDOUT,
            timeout=60,
            text=True
        )
        return f"Success:\n{output}"
    except Exception as e:
        return f"Error creating branch: {str(e)}"

if __name__ == "__main__":
    mcp.run()
