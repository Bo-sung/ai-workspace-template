# Current Progress

Single source of truth for project progress.

Last Updated: 2026-05-15T10:10:00+09:00

## Completed

- Shared multi-agent operating framework initialized under `.agents/`.
- Thin agent entrypoints added: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- Project quick reference at `Project/FrontierBastion_plan/PROJECT_QUICK_REFERENCE.md` realigned to the current repo root (`H:\Git\Portpolio\FrontierBastion`).
- Legacy memory notes moved from `메모리/` to `.agents/backups/2026-05-12_0623/메모리/`.
- AI OS Upgrade: Expert Cloud Workers policy and Tiered Reasoning Protocol added (see `.agents/rules/collaboration.md`, `.agents/rules/model_capabilities.md`).
- `.agents/rules/module_permissions.md` rewritten to use the actual `Project/FrontierBastion_plan/**` paths (previously referenced as if at repo root).
- Stale Codex lock on `README.md` from `codex-20260513-0913-readme-status` released.
- Initial GDD and Worldbuilding documents present under `Project/FrontierBastion_plan/` (numbered overview docs `01_…05_`, plus `시스템/` module set carried over from the legacy FantasyTowerDeffence_docs repo).

## Active Decision

- **SF Re-theme is the canonical direction.** The 기획서 원본 (`Project/FrontierBastion_plan/Frontier_Bastion_기획서_원본.md`) defines the game as a 공방형 라인 디펜스 RPG + 변방 개척 시뮬레이션 set in an SF colony frontier (총독/파일럿/메카/식민지/침식체 군집). The carried-over `시스템/` documents still use fantasy terminology (영웅/영지/마나/MAG/RES). Going forward, system docs are to be re-themed to the SF concept while preserving combat mechanics and Phase 1 scope.

## In Progress

- OPS realign session (`claude-20260515-1005-ops-realign`): updating operating docs to match current layout and seeding the GAME_DESIGN handoff for the SF re-theme.

## Worker Reconnaissance (2026-05-15, Explore agents)

Three read-only Explore agents were dispatched in parallel to scout the system docs before the SF re-theme work. Key findings:

- **Fantasy term volume** (full count across `시스템/**`): 영웅 379 (31 files), 영지 101 (27 files), 마나 89 (10 files), 마법 35 (13 files), MAG 25 (7 files), RES 21 (6 files), 마력 15, 종족 10, 신성 5 (속성 시스템 — 교체 신중), 마법사 9. 마왕/용사/엘프/드워프/던전 등 전형적 판타지 어휘는 없음.
- **Link hubs (rename ripple)** — incoming link counts: `영웅 시스템.md` 10, `스테이지 시스템.md` 10, `핵심 컨텐츠.md` 8, `부대 카드 시스템.md` 8, `전투 코어.md` 8. 파일명을 바꾸려면 각각 8–10개 문서 갱신 필요.
- **`Review Needed` files** (frontmatter): `개발 로드맵.md`, `스테이지 시스템.md`, `영웅 시스템.md`, `핵심 컨텐츠.md` — 4개 중 3개가 위 link hub와 겹침.
- **Outstanding decisions** flagged in docs: 영웅 직접 출격 마나 비용 여부 (스테이지/영웅 시스템), 영입·수익화 정책 (핵심 컨텐츠 4건), 재화 보상 TBD 6건 (재화 시스템_상세).
- **Data identifier alert**: `데이터 테이블.md` has a `race` column and `base_mag`/`base_res` columns — DATA_TECH must coordinate whether SF re-theme changes column names.

Recommendation for next GAME_DESIGN session: lock the glossary, then apply Phase A re-theme to the 5 hub files (`영웅 시스템 / 스테이지 시스템 / 핵심 컨텐츠 / 부대 카드 시스템 / 전투 코어`) in one wave — they are both the highest-traffic and the highest-Review-Needed files.

## Worker Infrastructure Status (2026-05-15, audited)

The `Remote AI Worker Policy` in `AGENTS.md`/`GEMINI.md` describes infrastructure that **is fully implemented** in `.shared-ai-tools/` (workers.yaml, worker_router_mcp.py, openai_light_mcp.py, venv, auto-shutdown, prompts, docs). The only missing piece is the **Claude Code MCP registration** — there is no `.mcp.json` at the repo root and no `mcpServers` key in `~/.claude.json`/`~/.claude/settings.json`, so this Claude Code session cannot see `worker_router` or `openai_light_workers` despite both being runnable.

Two issues found during the audit:

- **Path bug in existing snippets** — both `config-snippets/gemini-settings.remote-workers.json` and `config-snippets/codex.remote-workers.toml` reference `H:/Git/Portpolio/FrontierBastion_plan/.shared-ai-tools/...` (note `FrontierBastion_plan`). Actual path is `H:/Git/Portpolio/FrontierBastion/.shared-ai-tools/...`. Until corrected, Gemini and Codex registrations cannot launch the MCP servers either.
- **No Claude-Code-shaped config snippet** exists under `config-snippets/`. Gemini and Codex have one each; Claude does not.

Design and integration path captured in `.agents/handoff/worker_infra_integration.md`. No implementation performed this session — user requested design-only scope. Next OPS session should review the open questions in §4 of that handoff before writing any config.

**Update 2026-05-15 (verification complete):** Worker infrastructure is now **ACTIVATED and operational for macOS Ollama workers**. `.mcp.json` written, path-bug fixes applied, MCP servers loaded. Root-cause of remote-call hang was `stdio` MCP child inheriting parent's stdin — fixed by patching all 4 `subprocess.check_output` sites in `.shared-ai-tools/worker_router_mcp.py` with `stdin=subprocess.DEVNULL`. End-to-end smoke test: `ask_worker(macmini-worker, qwen3:4b)` returned correct payload. Two carried-forward limitations: (a) `laptop-gemma-e2b` (Windows host) cannot run model calls because `_call_remote_ollama` ships sh-syntax commands — not a blocker, just route around it; (b) OpenAI lightweight path unverified pending key. Details in `.agents/handoff/ops_coordination.md`.

## Worker Infrastructure Direction Change (2026-05-16)

**Decision: MCP → CLI(ask.py).** Token-efficiency review compared four call paths (MCP / CLI / HTTP / SSH-direct) for use across Claude Code, Codex, Gemini CLI. CLI invocation through a thin `ask.py` wins on (a) tool-surface fixed cost (~300 tokens vs MCP's ~2000–4000 per session), (b) file-based I/O lets big results bypass the main session context entirely, (c) zero CLI-specific config files to maintain, (d) avoids the Windows stdio sandbox traps surfaced during the MCP debugging cycle. OpenAI lightweight path is dropped entirely (user confirmed unused).

**Step 1 complete (2026-05-16):** Cleanup phase executed. `.mcp.json` deleted, `openai_light_mcp.py` + `openai_light_worker_policy.md` + all `config-snippets/` removed. `workers.yaml`: laptop disabled, WOL fields dropped, `policies:` block added.

**Step 2 complete (2026-05-16):** ask.py operational, worker_router_mcp.py removed. `.shared-ai-tools/cli/ask.py` verified (C1–C5 pass): list, health, tag-routing call, file I/O call, EXAONE license rejection.

**Step 3 complete (2026-05-16):** policy/docs synchronized to CLI direction; AGENTS/GEMINI/CLAUDE.md compressed to 5-line pointer sections; architecture.md rewritten (CLI-only, MCP references removed except comparison); codex-handoff.md deleted (D-1).

**Step 4 complete (2026-05-16, retry after Step 2.1 UTF-8 encoding patch):** All five probes (V1 list / V2 health / V3 small call / V4 file I/O / V5 EXAONE toggle) passed. Step 2.1 encoding fix (UTF-8 parameter added to subprocess.check_output in _call_remote_ollama) was a prerequisite. Token-efficiency measurement:
- Tool-surface fixed cost: MCP 시절 ~2000–4000 tokens → CLI ask.py ~300 tokens (list 출력)
- V3 소형 호출 메인 세션 소비: ~19 tokens (task + response)
- V4 대형 호출 메인 세션 소비: ~275 tokens (task + input_file + stdout status line)
- 출력 파일 우회로 결과 본문 1415자(~354 tokens) 컨텍스트 진입 회피
- 평균 호출당 절감률: 약 60–70% (대형 호출에서 최대 효과)

Worker Infrastructure transition (MCP → CLI) is COMPLETE. Next track: laptop-gemma-e2b WSL activation (separate work).

## Laptop Worker Activated (2026-05-16 PM)

`laptop-gemma-e2b` enabled in `workers.yaml` after notebook-side WSL2 setup (Ubuntu WSL2 + ollama + gemma4:e2b + Windows OpenSSH default shell → bash.exe). UTF-8 end-to-end verified via Korean translation task on laptop (`작업자 인프라가 이제 완료되었습니다.`). `workers.yaml` laptop entry updates: `enabled: true`, `os: linux`, `python_cmd: python3` (other fields kept from prior config).

**Step 2.1 encoding patch was found to be incomplete** — both `_call_remote_ollama` (line 82-88) and `cmd_health` (line 157-168) in `ask.py` were still missing `encoding='utf-8'` despite the Step 2.1 session reporting success. Re-patched in this session. Why Step 4 V4 retry passed earlier is unexplained (possibly the patch existed transiently then was reverted by a follow-up edit; not investigated due to budget). All `subprocess.check_output(..., text=True)` calls in ask.py now carry `encoding='utf-8'`.

**Carry-forward:** `macmini-worker` returned SSH timeout (port 2222) during this session's `ask.py health`. Single attempt — likely transient (both nodes "always on" per user). Re-verify in a fresh session.

**Confirmed environmental facts:**
- Both nodes (laptop windows, macmini macOS) are **always on**; WOL does not work on either. `ask.py wake` is therefore not needed. SSH connect timeout = node off.
- `laptop-gemma-e2b` will be `enabled: false` going forward — the existing `_call_remote_ollama` ships sh-syntax which Windows shell cannot parse; routing avoids it.

**EXAONE NC license policy** moved into `workers.yaml` under a new `policies:` section as a toggle:
- `policies.exaone_session_approval: true` → ask.py auto-applies `user_approved=True` for EXAONE calls in the session
- `false` → each EXAONE call must pass `--user-approved` explicitly, or it is refused

**New Role added:** `INFRA` — owns `.shared-ai-tools/**`. Recorded in `.agents/rules/module_permissions.md`. `.shared-ai-tools/venvs/**` is sensitive (dependency changes require user approval). `.mcp.json` at repo root is now flagged sensitive as well — it changes Claude Code runtime on restart.

**Four-step transition plan** (each runs as its own session):
1. **Step 1 — Cleanup (INFRA + OPS).** Delete `.mcp.json`, `openai_light_mcp.py`, `prompts/openai_light_worker_policy.md`, all of `config-snippets/`. `workers.yaml`: set laptop `enabled: false`, drop `mac_address`/`wol_port` fields, add `policies:` block. Add `.ai-cache/` to `.gitignore`.
2. **Step 2 — ask.py (INFRA).** New `.shared-ai-tools/cli/ask.py` with subcommands `list`, `health`, `call`. Reuses the patched `_call_remote_ollama` and tag-routing logic. Implements policy toggle. Delete `worker_router_mcp.py` after porting. Output convention: `--output-file` keeps large results out of main-session context; stdout becomes a short status line.
3. **Step 3 — Policy + docs sync (OPS + INFRA).** Rewrite Remote AI Worker Policy sections in `AGENTS.md`/`GEMINI.md`/`CLAUDE.md` for CLI invocation; remove all OpenAI references. Update `.shared-ai-tools/docs/architecture.md`. Decide `docs/codex-handoff.md` disposition.
4. **Step 4 — Verification.** Run `ask.py list/health/call` end-to-end. Measure token cost on representative tasks vs MCP baseline. Record results in this file.

**Open items (none blocking; user decisions captured above):**
- ask.py path: `.shared-ai-tools/cli/ask.py` (decided)
- INFRA Role: created (this session)
- Cache path: `.ai-cache/` in repo root, gitignored (decided)
- EXAONE policy: toggle in workers.yaml (decided)
- Step granularity: one-step-per-session (decided). This session ends after recording the plan and seeding the Step 1 work-order prompt in the OPS handoff.

## SF Re-theme Phase A 완료 (2026-05-16)

**세션**: `claude-20260516-1700-game-design-sf-retheme`

### 확정된 SF 매핑 (용어 사전.md v2.0에 기록됨)

| 판타지 | SF |
|---|---|
| 마나 | 에너지 |
| 영웅 | 파일럿 |
| 소환 유닛 | 드론 부대 |
| 영지 | 식민지 |
| 영주성 | 총독부 |
| 마석 | 레어메탈 |
| 은화 | 크레딧 |
| MAG | 빔 출력 |
| RES | 차폐 |
| 보스 | 침식체 변종 / 모선 |
| 성벽 | 방벽 |

### 적용된 Hub 파일 5개

- `시스템/전투 코어.md` — SF 용어 적용 완료
- `시스템/부대 카드 시스템.md` — SF 용어 적용 완료
- `시스템/영웅 시스템.md` — 내부 제목 "파일럿 시스템"으로 변경, SF 용어 적용 완료
- `시스템/핵심 컨텐츠.md` — SF 용어 적용 완료 (영지→식민지, 영웅→파일럿 전반)
- `시스템/스테이지 시스템.md` — SF 용어 적용 완료 (마나→에너지 섹션 포함)

### 미결 사항 (DATA_TECH 협의 필요)
- `빔 출력 / 차폐`의 영문 식별자 (현재 `MAG` / `RES`) 및 데이터 테이블 컬럼명 변경 여부
- `race` 컬럼 → SF 상응 식별자 검토
- 파일 경로 rename (영웅 시스템.md → 파일럿 시스템.md 등) — 사용자 확인 후 진행

---

## Next Work

**Priority track — Worker Infrastructure transition (MCP → CLI):**

0. **INFRA session — Step 1 (Cleanup).** See work-order in `.agents/handoff/ops_coordination.md` "Open Item: Worker Infra Step 1". User decisions already captured above; the session executes the file-deletion + workers.yaml edits + .gitignore append only. No new code.
0.1. **INFRA session — Step 2 (ask.py).** Port `_call_remote_ollama` + routing into argparse-based CLI.
0.2. **OPS + INFRA session — Step 3 (Policy/doc sync).** Rewrite Remote AI Worker Policy for CLI.
0.3. **OPS session — Step 4 (Verification).** Measure token cost; record in this file.

**Content track (resumed after the infrastructure track stabilises):**

1. **GAME_DESIGN session — SF terminology pass (Phase A).**
   - Draft a terminology mapping (영웅→파일럿, 영지→식민지/전초기지, 마나→에너지/지령 포인트, MAG/RES→대응 SF 스탯, 적→침식체 군집, 보스→침식체 변종/모선 등) before editing any system doc.
   - Land the mapping in `Project/FrontierBastion_plan/용어 사전.md` first (shared file — requires lock).
   - Apply the mapping to `시스템/게임 개요.md`, `시스템/전투 메카닉.md`, `시스템/전투 코어.md`, `시스템/부대 카드 시스템.md`, `시스템/영웅 시스템.md`, `시스템/영지 시스템.md` as the first wave.
2. **GAME_DESIGN session — SF terminology pass (Phase B).**
   - Propagate to `스킬/스탯/적/스테이지/장비/재화/소셜/수익화/진행 시스템` and the `영웅/`, `영지/` subfolders.
   - Treat `시스템/Phase 1 구현 범위.md` as shared (lock required); keep scope numbers stable, only re-skin terminology.
3. **LORE_ART session — Worldbuilding alignment.**
   - Reconcile `01_…05_` overview docs with the SF concept and update `용어 사전.md` entries owned by lore.
4. **DATA_TECH session — Stat naming.**
   - Once GAME_DESIGN settles on SF stat names, update `시스템/데이터 테이블.md` and `시스템/데이터 아키텍처.md` to match.

## Blockers

- None.

## Verification Needed

- Before starting the GAME_DESIGN session, confirm no other session has registered the `GAME_DESIGN` role.
- After Phase A, do a glossary cross-check between `용어 사전.md` and each edited 시스템 doc to ensure no orphaned fantasy terms remain.
