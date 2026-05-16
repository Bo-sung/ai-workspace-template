#!/usr/bin/env python3
"""ask.py — CLI interface for remote Ollama workers defined in workers.yaml."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

WORKERS_YAML = Path(__file__).parent.parent / "workers.yaml"
REPO_ROOT = WORKERS_YAML.parent.parent  # .shared-ai-tools/.. = repo root
TEMPLATES_DIR = WORKERS_YAML.parent / "prompts" / "templates"


def _resolve_output_dir(defaults):
    """Resolve defaults.output_dir to an absolute Path; default to repo_root/.ai-cache."""
    raw = defaults.get("output_dir", ".ai-cache")
    p = Path(raw)
    return p if p.is_absolute() else (REPO_ROOT / p)


def _auto_output_path(task, output_dir):
    """Generate a unique output file under output_dir from task hash + timestamp."""
    ts = time.strftime("%Y%m%d-%H%M%S")
    task_slug = hashlib.sha1(task.encode("utf-8")).hexdigest()[:8]
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{ts}-{task_slug}.md"

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


def load_workers():
    with open(WORKERS_YAML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _call_remote_ollama(
    worker, model_name, task, input_text, num_ctx, temperature, max_output_tokens
):
    host = worker["host"]
    port = str(worker.get("port", 22))
    user = worker.get("user", "")
    target = f"{user}@{host}" if user else host

    if input_text:
        prompt = f"Task:\n{task}\n\nInput:\n{input_text}"
    else:
        prompt = f"Task:\n{task}"

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "options": {
            "num_ctx": num_ctx,
            "temperature": temperature,
            "num_predict": max_output_tokens,
        },
        "think": False,
        "stream": False,
        "keep_alive": 0,
    }

    payload_json = json.dumps(payload).replace("'", "'\\''")
    cmd = (
        "touch ~/.ai_worker_active 2>/dev/null; "
        "curl -s -X POST http://127.0.0.1:11434/api/chat "
        "-H 'Content-Type: application/json' "
        f"-d '{payload_json}'"
    )

    output = subprocess.check_output(
        ["ssh", "-p", port, "-o", "BatchMode=yes", target, cmd],
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        timeout=120,
        text=True,
        encoding="utf-8",
    )
    res = json.loads(output)
    content = ""
    if "message" in res:
        content = res["message"].get("content", "")
        # thinking-mode models (e.g. qwen3) put output in 'thinking' when think:false suppresses it
        if not content:
            content = res["message"].get("thinking", "")
    if not content:
        raise RuntimeError(f"Unexpected response format: {output[:200]}")
    usage = {
        "in": res.get("prompt_eval_count", 0),
        "out": res.get("eval_count", 0),
    }
    return content, usage


def cmd_list(args):
    config = load_workers()
    workers = config.get("workers", [])
    defaults = config.get("defaults", {})
    policies = config.get("policies", {})

    print("=== Workers ===")
    print(f"{'ID':<25} {'Host':<35} {'OS':<8} {'Status'}")
    print("-" * 78)
    for w in workers:
        status = "enabled" if w.get("enabled", False) else "disabled"
        print(f"{w['id']:<25} {w['host']:<35} {w['os']:<8} {status}")
        for m in w.get("models", []):
            tags_str = ", ".join(m.get("tags", []))
            print(
                f"    {m['name']:<28} tags=[{tags_str}]"
                f"  priority={m.get('priority', 0)}"
                f"  in={m.get('max_input_tokens', 0)}"
                f"  out={m.get('max_output_tokens', 0)}"
            )
    print()
    print("=== Defaults ===")
    for k, v in defaults.items():
        print(f"  {k}: {v}")
    print()
    print("=== Policies ===")
    for k, v in policies.items():
        print(f"  {k}: {v}")


def cmd_health(args):
    config = load_workers()
    workers = config.get("workers", [])

    print(f"{'Worker ID':<25} {'Status':<8} Notes")
    print("-" * 70)
    for w in workers:
        if not w.get("enabled", False):
            print(f"{w['id']:<25} {'SKIP':<8} disabled")
            continue

        host = w["host"]
        port = str(w.get("port", 22))
        user = w.get("user", "")
        target = f"{user}@{host}" if user else host
        python_cmd = w.get("python_cmd", "python")

        check_cmd = (
            f"hostname && {python_cmd} --version && git --version && "
            f"{python_cmd} -c \"import urllib.request; "
            f"urllib.request.urlopen('http://127.0.0.1:11434/api/tags', timeout=2)\" "
            f"&& echo API_OK || echo API_FAIL"
        )

        try:
            output = subprocess.check_output(
                [
                    "ssh", "-p", port,
                    "-o", "BatchMode=yes",
                    "-o", "ConnectTimeout=5",
                    target, check_cmd,
                ],
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                timeout=15,
                text=True,
                encoding="utf-8",
            )
            if "API_OK" in output:
                print(f"{w['id']:<25} {'[OK]':<8} SSH+Git+Python+Ollama reachable")
            else:
                print(f"{w['id']:<25} {'[WARN]':<8} SSH OK but Ollama API check failed")
        except subprocess.TimeoutExpired:
            print(f"{w['id']:<25} {'[FAIL]':<8} connection timed out")
        except subprocess.CalledProcessError as e:
            snippet = (e.output or "").strip()[:80]
            print(f"{w['id']:<25} {'[FAIL]':<8} SSH command failed: {snippet}")


def cmd_call(args):
    config = load_workers()
    workers = config.get("workers", [])
    defaults = config.get("defaults", {})
    policies = config.get("policies", {})

    if not args.worker and not args.tags:
        print("error: must specify --worker or --tags", file=sys.stderr)
        sys.exit(2)

    if not args.task and not args.task_file and not getattr(args, "task_template", None):
        print("error: must specify --task, --task-file, or --task-template", file=sys.stderr)
        sys.exit(2)

    # task source precedence: --task > --task-file > --task-template
    if args.task:
        task = args.task
    elif args.task_file:
        task = Path(args.task_file).read_text(encoding="utf-8")
    elif getattr(args, "task_template", None):
        template_path = TEMPLATES_DIR / f"{args.task_template}.md"
        if not template_path.exists():
            print(f"error: task template not found: {template_path}", file=sys.stderr)
            sys.exit(2)
        task = template_path.read_text(encoding="utf-8")
    else:
        task = None

    input_text = ""
    if args.input_file:
        input_text = Path(args.input_file).read_text(encoding="utf-8")
    elif args.input:
        input_text = args.input

    # --auto-output: generate output path under defaults.output_dir
    if getattr(args, "auto_output", False) and not args.output_file:
        args.output_file = str(_auto_output_path(task, _resolve_output_dir(defaults)))

    warnings = []
    selected_worker = None
    selected_model = None

    if args.worker:
        if not args.model:
            print("error: --worker requires --model", file=sys.stderr)
            sys.exit(2)
        selected_worker = next((w for w in workers if w["id"] == args.worker), None)
        if not selected_worker:
            print(f"error: worker '{args.worker}' not found", file=sys.stderr)
            sys.exit(2)
        if not selected_worker.get("enabled", False):
            print(f"error: worker '{args.worker}' is disabled", file=sys.stderr)
            sys.exit(2)
        selected_model = next(
            (m for m in selected_worker.get("models", []) if m["name"] == args.model),
            None,
        )
        if not selected_model:
            print(
                f"error: model '{args.model}' not found in worker '{args.worker}'",
                file=sys.stderr,
            )
            sys.exit(2)
    else:
        preferred_tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        enabled_workers = [w for w in workers if w.get("enabled", False)]

        candidates = []
        for w in enabled_workers:
            for m in w.get("models", []):
                score = len(set(preferred_tags).intersection(set(m.get("tags", []))))
                if score > 0:
                    candidates.append(
                        {
                            "worker": w,
                            "model": m,
                            "score": score,
                            "priority": m.get("priority", 0),
                        }
                    )

        if not candidates:
            print(f"error: no enabled models match tags: {args.tags}", file=sys.stderr)
            sys.exit(2)

        candidates.sort(key=lambda x: (x["score"], x["priority"]), reverse=True)
        best = candidates[0]
        selected_worker = best["worker"]
        selected_model = best["model"]

        if best["score"] < len(preferred_tags):
            warnings.append("fallback occurred: not all preferred tags were matched")

    model_name = selected_model["name"]
    if "exaone" in model_name.lower():
        if args.user_approved:
            pass
        elif policies.get("exaone_session_approval", False):
            warnings.append("session-level approval applied for EXAONE NC license")
        else:
            print(
                f"error: EXAONE model '{model_name}' requires user approval.\n"
                "  Pass --user-approved flag, or set exaone_session_approval: true in workers.yaml.",
                file=sys.stderr,
            )
            sys.exit(2)

    num_ctx = args.num_ctx if args.num_ctx is not None else defaults.get("num_ctx", 4096)
    temperature = (
        args.temperature if args.temperature is not None else defaults.get("temperature", 0.2)
    )
    max_output_tokens = (
        args.max_output_tokens
        if args.max_output_tokens is not None
        else selected_model.get("max_output_tokens", 500)
    )

    try:
        result, usage = _call_remote_ollama(
            selected_worker, model_name, task, input_text, num_ctx, temperature, max_output_tokens
        )
    except Exception as e:
        if args.json_out:
            print(
                json.dumps(
                    {
                        "worker_id": selected_worker["id"],
                        "model": model_name,
                        "warnings": warnings,
                        "error": str(e),
                    },
                    ensure_ascii=False,
                )
            )
        else:
            print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output_file:
        out_path = Path(args.output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        chars = len(result)
        if args.json_out:
            print(
                json.dumps(
                    {
                        "worker_id": selected_worker["id"],
                        "model": model_name,
                        "warnings": warnings,
                        "result_path": str(out_path),
                        "chars": chars,
                        "usage": usage,
                    },
                    ensure_ascii=False,
                )
            )
        else:
            if warnings:
                print("\n".join(warnings), file=sys.stderr)
            peek_suffix = ""
            if args.peek > 0 and chars > 0:
                peek_text = result[: args.peek].replace("\n", " ").replace("\r", "")
                if chars > args.peek:
                    peek_text += "..."
                peek_suffix = f" | {peek_text}"
            print(
                f"OK [{selected_worker['id']}/{model_name}] "
                f"(tok in:{usage['in']} out:{usage['out']}) {chars}c → {out_path}{peek_suffix}"
            )
    elif args.json_out:
        print(
            json.dumps(
                {
                    "worker_id": selected_worker["id"],
                    "model": model_name,
                    "warnings": warnings,
                    "result": result,
                    "usage": usage,
                },
                ensure_ascii=False,
            )
        )
    else:
        if warnings:
            print("\n".join(warnings), file=sys.stderr)
        print(f"[tok in:{usage['in']} out:{usage['out']}]", file=sys.stderr)
        print(result, end="")


def cmd_batch(args):
    """Run a list of call items defined in a YAML file. Each item is a dict whose keys
    mirror the 'call' subcommand arguments (worker, model, tags, task, input, input_file,
    output_file, auto_output, max_output_tokens, num_ctx, temperature, user_approved, peek).
    Items run sequentially; one failure does not stop the rest unless --fail-fast is set.
    """
    batch_path = Path(args.batch_file)
    if not batch_path.exists():
        print(f"error: batch file not found: {batch_path}", file=sys.stderr)
        sys.exit(2)
    items = yaml.safe_load(batch_path.read_text(encoding="utf-8"))
    if not isinstance(items, list):
        # also accept {"calls": [...]} top-level
        if isinstance(items, dict) and "calls" in items:
            items = items["calls"]
        else:
            print("error: batch file must be a YAML list (or {calls: [...]})", file=sys.stderr)
            sys.exit(2)

    total = len(items)
    failures = 0
    for i, item in enumerate(items, start=1):
        # Build a Namespace mirroring call's args, filling defaults for anything omitted.
        call_args = argparse.Namespace(
            cmd="call",
            worker=item.get("worker"),
            tags=item.get("tags"),
            model=item.get("model"),
            task=item.get("task"),
            task_file=item.get("task_file"),
            task_template=item.get("task_template"),
            input=item.get("input", ""),
            input_file=item.get("input_file"),
            output_file=item.get("output_file"),
            auto_output=item.get("auto_output", True),  # batch default: auto-output ON
            max_output_tokens=item.get("max_output_tokens"),
            num_ctx=item.get("num_ctx"),
            temperature=item.get("temperature"),
            user_approved=item.get("user_approved", False),
            peek=item.get("peek", 0),
            json_out=item.get("json", False),
        )
        print(f"--- batch {i}/{total} ---", file=sys.stderr)
        try:
            cmd_call(call_args)
        except SystemExit as e:
            if e.code and e.code != 0:
                failures += 1
                if args.fail_fast:
                    print(f"error: stopping at batch item {i} (--fail-fast)", file=sys.stderr)
                    sys.exit(e.code)
        except Exception as e:
            failures += 1
            print(f"error: batch item {i} raised: {e}", file=sys.stderr)
            if args.fail_fast:
                sys.exit(1)

    print(f"--- batch complete: {total - failures}/{total} ok ---", file=sys.stderr)
    sys.exit(1 if failures else 0)


def main():
    # Force UTF-8 on stdout/stderr; default on Windows is cp949 which mangles non-ASCII output.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure") and stream.encoding and stream.encoding.lower() != "utf-8":
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(prog="ask.py", description="Remote Ollama worker CLI")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List enabled workers and models")
    sub.add_parser("health", help="Check health of all enabled workers via SSH")

    batch_p = sub.add_parser(
        "batch", help="Run multiple 'call' items from a YAML file sequentially"
    )
    batch_p.add_argument("--batch-file", dest="batch_file", required=True, help="Path to batch YAML")
    batch_p.add_argument(
        "--fail-fast", dest="fail_fast", action="store_true", help="Stop on first failure"
    )

    call_p = sub.add_parser("call", help="Execute a task on a remote worker")
    call_p.add_argument("--worker", help="Target specific worker by ID")
    call_p.add_argument("--tags", help="Comma-separated tags for routing")
    call_p.add_argument("--model", help="Model name (required with --worker)")
    call_p.add_argument("--task", help="Short task instruction string")
    call_p.add_argument("--task-file", dest="task_file", help="Path to task instruction file")
    call_p.add_argument(
        "--task-template",
        dest="task_template",
        metavar="NAME",
        help="Load task from .shared-ai-tools/prompts/templates/<NAME>.md "
             "(precedence: --task > --task-file > --task-template)",
    )
    call_p.add_argument("--input", default="", help="Short input text")
    call_p.add_argument("--input-file", dest="input_file", help="Path to input text file")
    call_p.add_argument("--output-file", dest="output_file", help="Path to write result")
    call_p.add_argument(
        "--auto-output",
        dest="auto_output",
        action="store_true",
        help="Auto-generate --output-file under workers.yaml defaults.output_dir (if --output-file not set)",
    )
    call_p.add_argument(
        "--max-output-tokens", dest="max_output_tokens", type=int, help="Max output tokens"
    )
    call_p.add_argument("--num-ctx", dest="num_ctx", type=int, help="Context window size")
    call_p.add_argument("--temperature", type=float, help="Sampling temperature")
    call_p.add_argument(
        "--user-approved",
        dest="user_approved",
        action="store_true",
        help="Approve EXAONE NC license for this call",
    )
    call_p.add_argument(
        "--peek",
        type=int,
        default=0,
        metavar="N",
        help="With --output-file: append first N chars of result to stdout status line",
    )
    call_p.add_argument(
        "--json",
        dest="json_out",
        action="store_true",
        help="Output raw JSON instead of plain text",
    )

    args = parser.parse_args()

    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "health":
        cmd_health(args)
    elif args.cmd == "call":
        cmd_call(args)
    elif args.cmd == "batch":
        cmd_batch(args)
    else:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
