다음 git 요약(`git status` / `git diff --name-status` / `git diff --stat` 출력)을 보고 conventional-commits 스타일 커밋 메시지 후보 3개를 만들어라.

각 후보 구조:
- 한 줄 제목: `<type>(<scope>): <subject>` (50자 내외, 마침표 없음)
- 빈 줄
- 본문 1~3줄: 변경의 *목적* 위주. 변경 *방법*은 git에 이미 있으므로 반복 금지

type 후보: feat / fix / docs / refactor / chore / test / build

규칙:
- 변경된 파일 종류·수에서 추론 가능한 것만 작성
- 코드 의미·내부 로직 추측 금지
- 새로운 사실 생성 금지 — 입력에 있는 것만

출력은 후보 3개를 빈 줄로 구분. 머리말 없이.
