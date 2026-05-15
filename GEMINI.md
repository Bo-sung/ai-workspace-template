# GEMINI.md

Gemini entrypoint for this repository.

Before doing any work, read `.agents/README.md` and follow the lifecycle documents under `.agents/lifecycle/`.

If Gemini is used as `COORDINATOR`, it should coordinate work, detect conflicts, prepare task prompts, review results, and update operating state. It should not directly edit project content unless the user explicitly assigns a Worker Role.

Current state must remain in:

- `.agents/state/session_registry.md`
- `.agents/state/resource_locks.md`
- `.agents/state/current_progress.md`


### Remote Worker Policy

워커 호출은 `.shared-ai-tools/cli/ask.py` CLI 통해 이뤄진다 (MCP/OpenAI 경로 모두 폐기됨).
정책 본문·위임 카탈로그·토큰 효율 규칙·라이선스 토글의 단일 출처는:
`.shared-ai-tools/prompts/remote_worker_policy.md`

핵심 요약 (자세한 건 위 문서 참조):
- Orchestrator(메인 세션)가 결정·편집·git 작업 담당.
- 워커는 요약·추출·분류·포맷팅·초안 작성만. 코드·아키텍처·최종 결정 위임 금지.
- 200단어 초과 입출력은 파일(--input-file / --output-file) 사용해 메인 세션 컨텍스트 절약.
- 워커 출력은 항상 draft.
