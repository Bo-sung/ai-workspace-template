# Shared AI Tools Architecture

## Goal

데스크탑 메인 세션(Claude Code / Codex / Gemini CLI)이 잡무를 원격 로컬 LLM에 위임해 토큰 소모를 줄이는 것.

## Components

- **workers.yaml** — 노드/모델 레지스트리 + 운영 정책(`policies` 블록).
- **cli/ask.py** — 유일한 진입점. CLI 무관(어느 메인 세션이든 셸 도구로 호출).
- **venvs/ai-tools/** — Python venv (yaml 등). 메인 세션이 ask.py를 이 venv의 python으로 실행.
- **prompts/remote_worker_policy.md** — 워커 system message 본문 + 운영 정책 본문.

## Call path

메인 세션 (Claude/Codex/Gemini) → Bash/shell 도구로 ask.py 실행 (venv python 통해) → ask.py가 workers.yaml 읽어 라우팅 결정 → SSH로 워커 노드 접속 (key 인증) → 워커 노드의 ollama API (127.0.0.1:11434) 호출 → 응답 반환 (stdout 또는 --output-file).

## Why CLI not MCP

- 토큰 surface 비용 최소화: MCP는 세션당 ~2000–4000 토큰 고정 비용, CLI는 ~300 토큰.
- 다중 CLI 호환: Claude Code / Codex / Gemini CLI 모두 셸 도구를 가지므로 공통 진입점 역할.
- 파일 기반 I/O로 컨텍스트 우회 가능: `--output-file`을 쓰면 큰 결과가 메인 세션 컨텍스트에 들어오지 않음.
- Windows stdio 함정 회피: MCP child process가 부모 stdin을 상속해 발생하는 hang을 구조적으로 제거.
- 설정 파일 0개: `.mcp.json`이나 CLI별 config 스니펫 없이 동작.

## Security

- SSH는 key 인증만. 패스워드 SSH 사용 금지.
- 워커는 read-only git만 가능. commit/push/merge/rebase 금지.
- 워커에 source code full diff 전달 금지 — `git status` / `--name-status` / `--stat` 요약만.
- API key·private key·환경변수 값 stdout/stderr 출력 금지.

## Status (작성일 기준: 2026-05-16)

- 활성 노드: macmini-worker (qwen3:4b, qwen3:8b, exaone3.5:7.8b).
- 비활성: laptop-gemma-e2b (WSL 경유 활성화는 별도 후속 작업).
