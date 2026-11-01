# AI 에이전틱 환경 온보딩 질문지 (환경 설정 체크리스트)

> **문서 용도**: `AI_에이전틱_환경_구축.md`(v1.3.0) 본문은 **기본 권장값**만 담는다. 팀마다 달라지는 운영 SLA · 인프라 · 조직 매핑 값은 이 질문지로 분리했다. 신규(Greenfield) · 레거시(Brownfield) 프로젝트에 도입할 때 팀이 이 질문지에 답하고, 답을 `spec-repo` 루트의 **`agentic-env.yaml`**에 기록한다.
> **AI 에이전트 규칙**: 본문에서 `ENV-xx` 또는 `UPPER_SNAKE` 변수명이 붙은 값은 `agentic-env.yaml`의 값을 우선한다. 파일이나 해당 키가 없으면 본문의 기본값을 쓰고, 그 사실을 실행 결과 보고에 한 줄로 밝힌다.
> **작성 원칙**: "기본값"은 명세서 본문의 현재 값이다. 질문에 답하지 않은 항목은 기본값으로 운영하되, **필수** 표시 항목은 비워 둔 채 가동하지 않는다.

---

## 0. 작성 방법

1. 리드 PO/PM이 이 문서를 복사해 프로젝트별로 답을 채운다. 결정 주체 칸의 담당자에게 해당 항목을 확인받는다.
2. 답을 `agentic-env.yaml`로 옮긴다(9절 서식). 비밀값(웹훅 URL · 토큰)은 파일에 쓰지 않고 **GitHub Secrets 이름**만 적는다.
3. `AGENTS.md`의 "프로젝트 환경 변수" 절에 `agentic-env.yaml`을 필독 파일로 등록한다.
4. 값을 바꿀 때는 `agentic-env.yaml` 수정 PR로 바꾸고, SLA · 게이트 값(5절) 변경은 리드 PO/PM과 테크리드가 함께 승인한다.

| 표시 | 의미 |
| :---: | :--- |
| **필수** | 답이 없으면 파이프라인이 동작하지 않는다(저장소 이름, 팀 핸들, 담당자 매핑 등). |
| **권장** | 기본값으로도 동작하지만 팀 상황에 맞게 정하는 편이 낫다. |
| **선택** | 확장 기능을 쓸 때만 답한다. |

---

## 1. 저장소 · 조직 구조

| ID | 변수명 | 질문 | 기본값 (본문) | 구분 | 결정 주체 | 본문 위치 |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| ENV-01 | `GH_ORG` | GitHub 조직(또는 계정) 이름은 무엇인가? | `<org>` | 필수 | 테크리드 | 1.2, 1.4-(2), 3.1, 3.4 |
| ENV-02 | `SPEC_REPO` | 정본 저장소 이름은 무엇인가? | `spec-repo` (예: `example-spec`) | 필수 | 리드 PO/PM | 1.2 |
| ENV-03 | `APP_REPOS` | 개발 저장소는 몇 개이며 이름은 무엇인가? (FE · BE 분리 여부 포함) | `app-repo` 1개 (예: `example-app`) | 필수 | 테크리드 | 1.2 |
| ENV-04 | `MAIN_BRANCH` | 병합 차단 게이트를 걸 기준 브랜치는 무엇인가? (`main` / `develop` / 릴리스 브랜치) | `main` | 권장 | 테크리드 | 1.2.1-1, 1.4-(2), 1.4-(4) |
| ENV-05 | `SPEC_SYNC_METHOD` | app-repo가 정본을 받는 방식은? (스크립트 복사 / git submodule / 패키지) | `scripts/sync-spec.sh`로 `.gitignore`된 `/docs`에 복사, 기준 커밋은 `spec.lock`으로 고정 | 권장 | 테크리드 | 1.2, 3.4 Step 1 |
| ENV-06 | `CROSS_REPO_AUTH` | app-repo CI가 spec-repo Issue를 읽을 권한은 무엇으로 줄 것인가? (GitHub App / 읽기 전용 PAT) · Secrets 이름은? | 미정 (기본 `GITHUB_TOKEN`은 다른 저장소 Issue를 못 읽을 수 있어 별도 권한 필요) | 필수 | 테크리드 · 보안 담당 | 1.2 (CI), 검토로그 1.5-(2) |

## 2. 도메인 · 담당자 매핑

| ID | 변수명 | 질문 | 기본값 (본문) | 구분 | 결정 주체 | 본문 위치 |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| ENV-07 | `DOMAINS` | 도메인 목록과 각 도메인의 약어(ID용) · 폴더명(경로용)은? | `SETT`/`settlement`, `ORDER`/`order`, `AUTH`/`auth` | 필수 | 리드 PO/PM | 1.2, 1.4-(2) |
| ENV-08 | `SPEC_FILES` | 도메인별 정본 파일 이름과 번호는? | `01_회원_권한.md`, `02_상품_주문.md`, `03_정산_환불.md` | 필수 | 리드 PO/PM | 1.2 |
| ENV-09 | `DOMAIN_ASSIGNEES` | 도메인별 담당 PO/PM GitHub 계정(질문 Issue 담당자)은? 담당자가 여럿이면 1순위 · 부재 시 대리인은? | `.github/domain-assignees.json` (값 없음) | 필수 | 리드 PO/PM | 1.4-(2) 1 |
| ENV-10 | `CODEOWNERS_MAP` | 경로별 코드 오너(정본 폴더 → 도메인 PO/PM, `contracts/` → FE · BE 리드)는? | `.github/CODEOWNERS` (값 없음) | 필수 | 리드 PO/PM · 테크리드 | 1.2, 1.2.1-3 |
| ENV-11 | `FE_LEADS_TEAM` · `BE_LEADS_TEAM` | FE · BE 테크리드 GitHub 팀 핸들은? | `@org/fe-leads`, `@org/be-leads` | 필수 | 테크리드 | 1.2, 1.2.1-3, 3.2 |

## 3. 식별자 · 명명 규칙

| ID | 변수명 | 질문 | 기본값 (본문) | 구분 | 결정 주체 | 본문 위치 |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| ENV-12 | `SCREEN_CODE_PREFIX` | 화면 코드 접두어는? (백오피스 / 유저 프론트 / 앱 등 추가 채널) | `ADMN-<도메인>-<NNN>`, `USER-<도메인>-<NNN>` | 권장 | 리드 PO/PM | 1.3, 3.1 |
| ENV-13 | `POL_ID_FORMAT` | 정책 ID 형식과 번호 자릿수는? | `POL-<도메인>-<3자리>` | 권장 | 리드 PO/PM | 1.2.2 |
| ENV-14 | `SHORT_HASH_LEN` | TASK ID의 단축 해시 길이는? (`scripts/new-id.sh`가 생성. Q-ID는 Issue 번호를 쓰므로 해당 없음) | 5자 | 권장 | 테크리드 | 1.4-(1) |
| ENV-15 | `COMMIT_MSG_FORMAT` | 커밋 메시지 형식은? (Conventional Commits 여부, `Ref: POL-*` 위치) | `feat(<도메인>): <요약> (<화면코드> · Ref: POL-*)` | 권장 | 테크리드 | 1.2.2-1, 3.4 Step 4 |

## 4. 질문 Issue 체계 · 알림

| ID | 변수명 | 질문 | 기본값 (본문) | 구분 | 결정 주체 | 본문 위치 |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| ENV-16 | `ISSUE_LABELS` | 질문 · 핫픽스 라벨 이름은? (기존 라벨 체계와 충돌 여부 확인) | `domain:<도메인>`, `blocking-question`, `assumption-question`, `legacy-question`, `hotfix` | 권장 | 리드 PO/PM | 1.4-(2), 1.4-(4), 3.1, 3.4 |
| ENV-17 | `BLOCKING_CATEGORIES` | 작업을 멈추는 Blocking 대상 범주는? (추가 · 제외할 범주) | 결제 금액 산식, 정산 수수료, 회원 권한/인가, 상태 전이 조건, 개인정보, PG 연동 | 권장 | 리드 PO/PM | 1.4-(2) 2 |
| ENV-18 | `NOTIFY_CHANNEL` · `NOTIFY_WEBHOOK_SECRET` | 질문 즉시 알림 메신저(Slack / Teams / 기타)와 채널, 웹훅 URL을 담을 Secrets 이름은? 도메인별 채널을 나누는가? | Slack/Teams 웹훅 (URL 미정) | 필수 | 리드 PO/PM · 테크리드 | 1.4-(2) 1 |
| ENV-19 | `NOTIFY_LABELS` | 즉시 알림을 보낼 라벨 범위는? (Blocking만 / 전체) | `blocking-question`만 웹훅, 나머지는 GitHub 알림 | 권장 | 리드 PO/PM | 1.4-(2) 1 |
| ENV-20 | `QUESTION_FAIL_QUEUE_DIR` · `QUESTION_RETRY` | 발의 · 알림 실패 시 로컬 큐 경로와 재시도 횟수는? 큐 폴더는 `.gitignore`에 등록했는가? | `tmp/questions-failed/`, 다음 실행 시 재시도 (횟수 미정) | 권장 | 테크리드 | 1.4-(2) 1, 3.4 Step 3 |
| ENV-21 | `ASSIGN_WORKFLOW` | 담당자 자동 지정 워크플로 파일 이름 · 매핑 파일 이름은? 다른 방식(GitHub Projects 자동화 등)을 쓰는가? | `.github/workflows/assign-issue.yml` + `.github/domain-assignees.json` | 권장 | 테크리드 | 1.4-(2) 1 |
| ENV-22 | `BLOCKING_ANSWER_SLA` | Blocking 질문에 PO/PM이 답할 목표 기한과, 기한을 넘기면 누구에게 올리는가(에스컬레이션)? | 미정 (본문에 없음) | 권장 | 리드 PO/PM | 1.4-(2) 2 (신규 제안) |

## 5. SLA · 병합 게이트

| ID | 변수명 | 질문 | 기본값 (본문) | 구분 | 결정 주체 | 본문 위치 |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| ENV-23 | `HOTFIX_SYNC_SLA` | 핫픽스 병합 후 정본 사후 동기화 기한은? (영업일 수, 기산 시점) | hotfix PR 병합 완료 시점부터 평일 3일 | 필수 | 리드 PO/PM · 테크리드 | 1.2, 1.4-(4) |
| ENV-24 | `HOLIDAY_CALENDAR` | 영업일 계산에 쓸 공휴일 출처는? (사내 캘린더 API / 저장소 JSON / 없음) | 연동 전에는 주말만 제외 | 권장 | 테크리드 | 1.4-(4), 검토로그 1.5-(2) |
| ENV-25 | `HOTFIX_SLA_PENALTY` | 기한을 넘기면 어떻게 하는가? (알림 · 에스컬레이션만 / 다음 릴리스 차단 / 모든 main 병합 차단) | 알림 · 에스컬레이션만 (담당 PO/PM 재알림 → 리드 PO/PM · 테크리드) | 권장 | 테크리드 | 1.4-(4) |
| ENV-26 | `RELEASE_CADENCE` | 릴리스의 주기와 판별 방법은? (릴리스 브랜치 · 태그 · 라벨) — ASSUMPTION 릴리스 게이트가 이 시점에 걸린다 | 미정 | 필수 | 테크리드 | 1.4-(4) |
| ENV-27 | `ASSUMPTION_GATE` | `[ASSUMPTION: Q-ID]` 주석을 어느 시점에 막는가? | main 병합: `OPEN` · `completed` 허용, `Q-PENDING` · 조회 불가 · 미정리 `not_planned`/`duplicate` 차단 / 릴리스: `completed`만 허용 | 권장 | 리드 PO/PM · 테크리드 | 1.4-(2) 2, 3.5 |
| ENV-28 | `ASSUMPTION_CLEANUP_WINDOW` | `completed` 종결 후 주석을 `@policy`로 바꾸는 기한은? (다음 `/dev-screen` / N일 / 스프린트 끝) | 다음 `/dev-screen` 실행 또는 정기 리팩토링 시 | 권장 | 테크리드 | 1.4-(2) 2, 3.4 Step 3 |
| ENV-29 | `CONTRACT_APPROVAL_RULE` | `contracts/openapi.yaml` 변경에 필요한 승인 수는? (FE n명 AND BE n명) | FE 리드 1명 이상 AND BE 리드 1명 이상 | 권장 | 테크리드 | 1.2.1-3, 3.2 |

## 6. CI · 검증 도구

| ID | 변수명 | 질문 | 기본값 (본문) | 구분 | 결정 주체 | 본문 위치 |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| ENV-30 | `CI_PLATFORM` | CI는 무엇을 쓰는가? (GitHub Actions / 사내 CI) | GitHub Actions | 필수 | 테크리드 | 1.2, 1.2.1-3 |
| ENV-31 | `CHECK_SCRIPT` | 결정론적 검사 진입점과 포함 항목은? (린트 · 계약 테스트 · 임시 DB 테스트 · 계산기 대조 · ASSUMPTION 게이트 · 핫픽스 기한) | `scripts/check.sh` (6개 항목 전부) | 권장 | 테크리드 | 1.2, 3.4 Step 4 |
| ENV-32 | `CONTRACT_TEST_TOOL` | API 계약 검증 · Mock 도구는? (Prism / Pact / 기타) | Prism (3.5 표에는 Pact/Prism 병기) | 권장 | BE 리드 | 1.2, 3.2, 3.5 |
| ENV-33 | `CONTRACT_FORMAT` | 계약 정본 형식은? (OpenAPI 3.x / JSON Schema) · 버전은? | `contracts/openapi.yaml` 또는 JSON Schema | 권장 | BE 리드 | 1.2, 3.2 |
| ENV-34 | `TEST_DB` | 임시 DB 테스트 방식은? (Docker 컨테이너 / 인메모리 / 공용 테스트 DB) | 임시 DB 병렬 테스트 (방식 미정) | 권장 | BE 리드 | 1.2 |
| ENV-35 | `ENGINE_DIR` | 도메인 기준 계산기 · 정답 시나리오 위치와 언어는? 계산기가 없는 도메인은? | `engine/` + 시나리오 JSON | 선택 | 리드 PO/PM · BE 리드 | 1.2, 3.3 |

## 7. 디자인 · UI

| ID | 변수명 | 질문 | 기본값 (본문) | 구분 | 결정 주체 | 본문 위치 |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| ENV-36 | `UI_TRACKS` | 화면별 트랙 배정 기준은? (백오피스 = Track A, 유저 프론트 = Track B 외 예외) | `ADMN-*` = Track A, `USER-*` = Track B | 권장 | 리드 PO/PM · UIX 리드 | 1.3 |
| ENV-37 | `ARCHETYPES` | Track A 표준 화면 골격 종류는? (추가 · 제외) | `List-Modal`, `Detail-Form`, `Stats-Dashboard`, `Tabs-Complex` | 권장 | FE 리드 | 1.3, 3.2 |
| ENV-38 | `SCREEN_STATES` | 화면 상태 매트릭스의 기본 상태와 도메인별 추가 상태는? | 기본 5종(정상 · 로딩 · 빈 화면 · 오류 · 권한 없음) + 정산 · 주문은 부분 실패 · 처리 중 | 권장 | UIX 리드 · 리드 PO/PM | 1.3 |
| ENV-39 | `FIGMA_FILES` · `FIGMA_MCP` | Figma 팀 · 파일 위치, Figma MCP 서버 종류와 접근 권한(좌석 · 토큰)은? | Figma MCP 서버 (노드 조회 도구) | 필수(Track B) | UIX 리드 · 테크리드 | 1.2.2-2, 1.3, 3.4 |
| ENV-40 | `CODE_CONNECT` | Figma Code Connect를 쓰는가(요금제 확인)? 대상 컴포넌트 라이브러리 경로는? | 사용 (경로 미정). 못 쓰면 `00_ui_system.md` 컴포넌트 매핑표 | 권장(Track B) | FE 리드 · UIX 리드 | 1.3 |
| ENV-41 | `TOKEN_STANDARD` | 디자인 토큰 표준 · 버전과 빌드 도구는? 토큰 원본은 어디인가? | W3C DTCG (2025.10), Figma Variables 원본 · 코드용 자동 빌드 | 권장 | UIX 리드 · FE 리드 | 1.3 |
| ENV-42 | `READY_FOR_DEV_LINT` | `Ready for Dev` 전환 기준은? (미바인딩 값 · Detach 인스턴스 허용 개수, 검사 도구) | 미바인딩 값 0개 · Detach 0개 | 권장 | UIX 리드 | 1.3, 3.2 |

## 8. AI 도구 · 소통 채널 · 컨텍스트

| ID | 변수명 | 질문 | 기본값 (본문) | 구분 | 결정 주체 | 본문 위치 |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| ENV-43 | `AGENT_TOOLS` | 팀이 쓰는 코딩 에이전트와 스킬 설치 경로는? | Claude Code · 안티그래비티, `.claude/skills/<스킬명>/SKILL.md` | 권장 | 테크리드 | 3 (머리말) |
| ENV-44 | `CHANNEL_MODE` | 작업 지시 · 피드백 채널은? (Core Git만 / Option A 사내 플랫폼 API / Option B Google Workspace) | Core (Git 내장 MD) | 권장 | 리드 PO/PM | 1.4-(5) |
| ENV-45 | `PLATFORM_API` | Option A를 쓸 경우 API 주소 · 인증 방식 · `project-meta.json` 위치는? | 경량 API 3종(POST 등록 · GET 조회 · PATCH 상태), 주소 미정 | 선택 | 사내 플랫폼 담당 | 1.4-(5) |
| ENV-46 | `CONTEXT_LOAD_RULE` | 화면 작업 때 AI가 읽는 범위는? (Digest만 / Digest + 색인이 가리키는 정본 절) | Digest + `canon_index.md` 앵커가 가리키는 정본 절 | 권장 | 테크리드 | 3.4 Step 1 |
| ENV-47 | `INCIDENT_DECLARER` | Level 3(핫픽스) 진입을 선언할 수 있는 사람 · 역할은? 장애 등급 기준은? | 운영 책임자(온콜 · 테크리드) | 필수 | 테크리드 · 운영 책임자 | 1.4-(4) |
| ENV-48 | `LEGACY_QUESTION_CAP` | 레거시 정본화(`/doc-init`) 1회에 도메인당 발의할 `legacy-question` 상한은? | 20건, 넘치면 묶음 Issue 1건 | 권장 | 리드 PO/PM | 3.1 |

---

## 9. `agentic-env.yaml` 서식 (예시)

> 아래 값은 기본값을 옮긴 **자리표시자**다. `<...>` 부분은 반드시 팀 값으로 바꾼다.

```yaml
# spec-repo/agentic-env.yaml — AI_에이전틱_온보딩_질문지.md 답변 기록
version: 1
repo:
  org: <org>                         # ENV-01
  spec_repo: <spec-repo>             # ENV-02
  app_repos: [<app-repo>]            # ENV-03
  main_branch: main                  # ENV-04
  spec_sync: script                  # ENV-05  script | submodule | package
  cross_repo_auth_secret: <SECRET_NAME>  # ENV-06  GitHub App 또는 읽기 전용 PAT
domains:                             # ENV-07 · ENV-08 · ENV-09
  - code: SETT
    dir: settlement
    spec_file: 03_정산_환불.md
    assignees: [<github-id>]
    backup_assignee: <github-id>
teams:
  fe_leads: "@<org>/fe-leads"        # ENV-11
  be_leads: "@<org>/be-leads"
ids:
  screen_prefix: [ADMN, USER]        # ENV-12
  pol_digits: 3                      # ENV-13
  task_hash_len: 5                   # ENV-14  scripts/new-id.sh
questions:
  labels:                            # ENV-16
    domain: "domain:<도메인>"
    blocking: blocking-question
    assumption: assumption-question
    legacy: legacy-question
    hotfix: hotfix
  blocking_categories: [결제 금액, 정산 수수료, 권한, 상태 전이, 개인정보, PG]  # ENV-17
  notify:
    channel: slack                   # ENV-18  slack | teams | none
    webhook_secret: <SECRET_NAME>
    labels: [blocking-question]      # ENV-19
  fail_queue_dir: tmp/questions-failed/  # ENV-20
  retry: 3
  answer_sla_business_days: <n>      # ENV-22
gates:
  hotfix_sync_business_days: 3       # ENV-23
  holiday_calendar: none             # ENV-24  none | <url> | <path.json>
  hotfix_sla_penalty: notify_escalate     # ENV-25  notify_escalate | block_next_release | block_main
  release_detect: <tag|branch|label> # ENV-26
  assumption_main_allow: [open, completed]   # ENV-27
  assumption_release_allow: [completed]
  contract_approvals: {fe: 1, be: 1} # ENV-29
ci:
  platform: github-actions           # ENV-30
  check_script: scripts/check.sh     # ENV-31
  contract_tool: prism               # ENV-32
design:
  token_standard: dtcg-2025.10       # ENV-41
  ready_for_dev_lint: {unbound: 0, detached: 0}  # ENV-42
channel:
  mode: core                         # ENV-44  core | platform-api | google-workspace
incident:
  declarers: [<github-id>]           # ENV-47
legacy:
  question_cap_per_domain: 20        # ENV-48
```

---

## 10. 프로젝트 유형별 우선 질문

| 유형 | 먼저 답할 항목 | 이유 |
| :--- | :--- | :--- |
| 신규 구축 (Greenfield) | ENV-01~11, ENV-12~13, ENV-30, ENV-36~42 | 저장소 · 식별자 · 디자인 시스템을 처음부터 같은 규칙으로 시작한다. |
| 전면 리뉴얼 | ENV-01~11, ENV-16~17, ENV-23~27 | 레거시 의심 로직이 `legacy-question`으로 몰리므로 라벨 · 담당자 · 게이트가 먼저 필요하다. |
| 운영 · 고도화 (Brownfield) | ENV-03~06, ENV-23~26, ENV-31 | 기존 브랜치 전략 · 릴리스 주기 · CI에 게이트를 얹는 것이 먼저다. 화면 코드 체계(ENV-12)는 기존 체계를 유지할지부터 정한다. |
