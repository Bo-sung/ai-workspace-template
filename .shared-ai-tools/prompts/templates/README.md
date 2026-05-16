# Task Prompt Templates

`ask.py call --task-template <name>` 으로 참조하는 task prompt 모음.

`<name>`은 이 디렉토리 내 파일명에서 `.md` 제외한 부분. 예:
- `summarize-ko.md` → `--task-template summarize-ko`

## 현재 템플릿

| name | 용도 | 권장 모델·태그 |
| --- | --- | --- |
| `summarize-ko` | 한국어 본문 요약 | exaone3.5 / qwen3:8b — tags: korean,summary or docs,summary |
| `classify-ko` | 라벨 후보 중 분류 한 개 출력 | qwen3:4b — tags: light,classify |
| `extract-todos` | TODO/FIXME/미정 마커 추출 | qwen3:4b — tags: light,classify |
| `git-commit-msg` | conventional-commits 후보 3개 (git status 요약 기반) | qwen3:4b — tags: light,git |
| `sf-naming-ko` | 판타지 → SF 한국어 용어 매핑 후보 | exaone3.5 — tags: korean,docs |
| `normalize-md` | 마크다운 구조 정규화 (의미 변경 금지) | qwen3:8b — tags: docs |

## 새 템플릿 추가

1. `<name>.md` 파일 추가 (본문에 task 지시만)
2. 위 표에 한 줄 추가
3. 첫 호출로 검증

## 작성 규칙

- task 지시만 담을 것. 입력 자체는 `--input` / `--input-file`로 전달.
- 출력 형식 명시 (머리말 금지, 군더더기 차단 등)
- 워커 자율 결정·창작 차단 문구 권장 ("새 내용 생성 금지", "있는 것만" 등)
- 한국어/영어 명시 — 워커가 어느 언어로 답할지 모호하면 안 됨
