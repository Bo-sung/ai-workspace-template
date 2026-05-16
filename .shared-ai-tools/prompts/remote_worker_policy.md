# Remote Worker Policy

## Orchestrator (메인 세션)

작업 계획, 분해, 입력 범위 선정, 워커 출력 검토, 최종 적용, Git 작업, 우선순위·일정 결정은 모두 메인 세션(Claude Code / Codex / Gemini CLI)이 직접 수행한다.

## Invocation

모든 워커 호출은 `.shared-ai-tools/cli/ask.py` 통해 이뤄진다. MCP/OpenAI 경로는 모두 폐기됨.

진입 예:
```
python <repo>/.shared-ai-tools/venvs/ai-tools/Scripts/python.exe <repo>/.shared-ai-tools/cli/ask.py <subcommand> ...
```

서브커맨드: `list` / `health` / `call` / `batch`

대표 사용:
```
ask.py call --tags <a,b> --task "..." --input-file <path> --output-file <path> --max-output-tokens <n> --peek 120
```

`--peek N` 옵션은 출력 파일에 결과를 저장한 뒤 stdout 상태 라인에 첫 N자 미리보기를 함께 출력 — 메인 세션이 결과 검증을 위해 별도 Read를 안 해도 됨.

stdout 상태 라인 형식 (with `--output-file`):
```
OK [worker_id/model] (tok in:N out:N) Mc → <path> | <peek text>
```
stdout 직접 결과 (without `--output-file`): 결과 본문이 stdout, 토큰 사용량은 stderr.

`--auto-output` 옵션을 쓰면 `--output-file`을 명시하지 않아도 ask.py가 `workers.yaml`의 `defaults.output_dir`(기본 `.ai-cache/`) 아래에 `YYYYMMDD-HHMMSS-<task-hash>.md` 형식으로 자동 생성한다. Orchestrator는 매 호출마다 경로를 직접 짜지 않아도 되고, 경로 인자 boilerplate가 줄어든다.

### Task 템플릿 (`--task-template <NAME>`)

자주 쓰는 task prompt는 `.shared-ai-tools/prompts/templates/<NAME>.md`로 미리 저장돼있다. Orchestrator는 매 호출마다 task 본문을 인라인으로 짜지 않고 템플릿 이름만 지정한다. 현재 제공 템플릿은 해당 디렉토리의 `README.md` 참조.

사용 예:
```
ask.py call --tags korean,summary --task-template summarize-ko --input-file <path> --auto-output --peek 120
```

우선순위: `--task` > `--task-file` > `--task-template`. 셋 중 하나는 반드시 지정.

운영 권장:
- 반복되는 task 유형은 새 템플릿을 만들어 인라인 task 작성을 줄일 것 (호출당 30~80 토큰 절감)
- 템플릿 본문에 "출력 형식 명시", "새 내용 생성 금지", "머리말 금지" 같은 가드 문구를 포함해 워커 응답의 군더더기 감소

### Batch 호출 (`ask.py batch --batch-file <yaml>`)

여러 task를 한 번의 명령으로 묶어 실행한다. 호출별 boilerplate(파이썬 진입점 풀패스 + 인자 키)가 명령 한 번으로 압축된다. 호출 사이에 워커 노드의 keep-alive를 활용하면 모델 로드 비용도 절감.

YAML 형식 (둘 다 허용):
```yaml
- task: "..."
  tags: docs,summary
  input_file: src1.md
  max_output_tokens: 200
- task: "..."
  worker: macmini-worker
  model: qwen3:4b
  input: "..."
  peek: 80
```
또는 `{calls: [...]}` 래핑.

기본값: `auto_output: true` (배치 항목엔 명시 안 하면 자동 출력 경로). `--fail-fast`로 첫 실패 시 즉시 중단 가능.

운영 패턴:
- 같은 종류의 작은 task(분류·라벨링·간단 요약) 5~10개를 묶어 배치로 실행.
- Orchestrator는 명령 한 줄만 작성. 결과는 각 task별 출력 파일로 분리됨.
- 보일러플레이트 절감 효과는 호출 수 N에 비례 — 5개 묶으면 한 호출 대비 약 80×(N−1) 토큰 절감.
- `--parallel K`로 K개 동시 실행 (지연 시간 절감, 토큰 영향 없음). 출력은 항목별 캡처 후 `[i/N]` 프리픽스로 식별.
- `--index-file <path>` 또는 `--auto-index`로 batch 종료 시 모든 항목의 상태·출력경로·peek를 한 markdown 표로 저장. Orchestrator가 결과 검증 시 개별 파일을 일일이 열지 않아도 됨.

### 추가 운영 옵션

- **`--retry N`** — SSH/Ollama 일시적 실패에 N회 재시도 (지수 백오프 1s/2s/4s). 기본값은 `workers.yaml` `defaults.retry`. 일시 네트워크 흔들림 흡수용.
- **`--trim` / `--no-trim`** — 워커 응답에서 명백한 군더더기 prefix/suffix 제거 (`Sure, here's…`, `Let me know…`, `다음은…`, `결과:` 등). 기본 비활성(`defaults.trim: false`); opt-in. 응답당 10~50 토큰 절감, 다만 코드 펜스 보존 등 보수적으로 동작.
- **`--with-header`** — 출력 파일 상단에 YAML frontmatter (`worker / model / ts / tok_in / tok_out / chars / duration_ms / task_hint`) 자동 삽입. 사후 검토·통계에 유용. 결과 본문 내용은 변경 없음.

### 호출 통계 누적 (자동)

`defaults.stats_log: true`(기본)면 ask.py가 호출마다 `.ai-cache/stats.jsonl`에 한 줄씩 append. 필드: `ts / worker / model / tok_in / tok_out / chars / duration_ms / status / attempts / task_hint`. 운영자가 `jq` 또는 `wc -l`로 누적 토큰 사용량·실패율·평균 지연을 즉시 분석 가능. 끄려면 `defaults.stats_log: false`.

## Token-efficiency rules

- 입력이 200단어 초과면 `--input-file` 사용. ask.py는 큰 페이로드를 SSH stdin으로 파이프(`curl --data-binary @-`)하므로 시스템 문서(10KB+) 통째로도 무리 없음.
- 결과 예상 100단어 초과면 `--output-file` 사용.
- `--max-output-tokens` 항상 명시 (모델 기본값 의존 금지).
- 큰 결과는 그대로 본문에 옮기지 말고 `.ai-cache/`에 두고 필요 시 Read offset/limit.
- 체이닝: 한 워커 출력 파일을 다음 워커 `--input-file`로.
- **결과 파일 500자 초과 시 통째로 Read 금지** — `--peek N`으로 stdout에서 미리보기를 받거나 사용자에게 파일 경로를 전달해 직접 확인하게 한다. Orchestrator 본문에 결과 전체가 들어가는 순간이 가장 큰 토큰 낭비 지점.
- ask.py가 stdout 상태 라인에 ollama의 토큰 사용량(`tok in:N out:N`)을 포함하므로, 호출별 회계를 stderr 또는 상태 라인에서 즉시 확인 가능. 운영 측정 자료로 활용할 것.

## Delegate (워커가 해도 되는 일)

- 문서 요약, 문서 정리
- TODO/FIXME 추출
- 짧은 분류·라벨링
- GDD 섹션 추출
- 회의록 정리
- QA 리포트 포맷팅
- Git 커밋 메시지 초안
- PR 설명 초안
- 릴리즈 노트 초안
- 표준 형식 변환

## Do NOT delegate (메인 세션이 직접)

- 코드 작성·수정·리뷰
- 아키텍처/디자인 결정
- 최종 우선순위/일정 결정
- `git commit` / `push` / `merge` / `rebase` / 충돌 해결
- 파일 직접 편집 (워커는 draft 생산만)
- 가공 안 된 source code full diff를 워커에 넘기는 것 — `git status` / `--name-status` / `--stat` 요약만 전달

## Worker catalog (현재 활성)

| 작업 유형 | 권장 모델 | 태그 |
| --- | --- | --- |
| 한국어 문서 요약/계획/회의록/릴리즈노트 | exaone3.5:7.8b (NC — 토글) | korean,docs,planning,meeting,release-notes |
| 일반 문서 요약/계획/QA/이슈 초안 | qwen3:8b | docs,planning,qa,issue-draft |
| 짧은 분류·라벨링·TODO 추출·git 메시지 | qwen3:4b | light,classify,git,summary |

추후 laptop-gemma-e2b WSL 활성화 시 light/fast 라우팅이 그쪽으로 가도록 추가 예정 — 현재는 비활성.

## EXAONE NC license

`workers.yaml`의 `policies.exaone_session_approval` 토글로 통제.

- `true` → ask.py가 EXAONE 호출 시 자동으로 `user_approved=True` 적용 (warning에 기록).
- `false` → 호출마다 `--user-approved` 인자 명시 필요. 없으면 exit 2.

코드 작업 중심 세션이라 EXAONE 부르면 안 되는 상황이면 `false`로 둘 것.

## Workers (existing system message — 워커가 받는 프롬프트)

아래 블록은 ask.py 내부 `SYSTEM_PROMPT` 변수의 내용과 동일하다. 한 글자도 바꾸지 말 것 — ask.py가 이 텍스트를 직접 사용한다.

```
You are a small remote local LLM worker used by Gemini CLI or Codex.

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
All output is draft material for the orchestrator to review.
```

## Review rule

모든 워커 출력은 draft. Orchestrator(메인 세션)가 검토·통합하고 불확실성은 명시.
