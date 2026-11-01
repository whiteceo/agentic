# AI 에이전틱 프로젝트 설치서 (v1.0.0)
<!-- 배포 전 작업본. 내부 개정 기록은 AI_에이전틱_검토로그.md에만 둔다. -->

> **누가 · 언제**: 세팅 담당(보통 테크리드) 1명이 **프로젝트를 추가할 때 한 번** 자기 AI에게 건넨다. 일상 작업 중에는 읽지 않는다.
> **AI 규칙**: 단계 순서대로 진행하고, 단계마다 만들거나 바꿀 목록을 먼저 보여 주고 승인받는다. 이미 있는 파일 · 라벨 · 설정은 건너뛰고, 내용이 다르면 덮어쓰지 않고 차이만 보고한다. 계정 · 권한 · 비밀값 등록은 대신하지 않고 사람의 할 일 목록으로 넘긴다. 설정값에 답이 없으면 지어내지 않고 묻는다.
> 결과물의 규칙은 `AI_에이전틱_핵심규약.md`가 정한다. 이 문서는 "어떻게 깔 것인가"만 다룬다.

## 1. 설치 순서

| 단계 | 할 일 | 누가 | 끝 확인 |
| :---: | :--- | :--- | :--- |
| **1** | GitHub 준비: 요금제 확인(비공개 저장소에서 필수 체크 · 저장소 규칙을 쓸 수 있는지), spec-repo · app-repo 생성, 팀(도메인 담당자 · FE 리드 · BE 리드), 권한(아래), CI 토큰 발급과 Secrets 등록(3절) | 사람 | 두 저장소 존재, `gh secret list`에 토큰 이름 |
| **2** | 설정 파일: 2절 질문에 답해 `spec-repo/agentic-env.yaml` 작성 | 세팅 담당 + 도메인 담당자 대표 | 필수 항목이 비어 있지 않음 |
| **3** | spec-repo 골격: `docs/specs/`(빈 `_registry.yaml`), `docs/digest/`, `docs/changes/<도메인>/`, `contracts/`(빈 폴더에는 `.gitkeep`), `AGENTS.md`(= 핵심규약 원문), `.github/CODEOWNERS`, `.github/domain-assignees.json`, `.github/ISSUE_TEMPLATE/question.yml`, 라벨, `assign-issue` 워크플로, `scripts/new-id.sh`, `.claude/skills/`에 `doc-init` · `doc-rule` · `doc-update`, 선택 부록을 하나라도 켰으면 루트에 `AI_에이전틱_선택_부록.md` | AI → 세팅 담당 리뷰 | 개발자 계정으로 `gh issue create --label` 테스트 Issue 1건을 올려 라벨이 붙고 담당자가 자동 지정됨 |
| **4** | app-repo 골격: `spec.lock`, `scripts/sync-spec.sh`, `scripts/check.sh`, `.gitignore`에 `/docs`, `AGENTS.md`, `check` 워크플로, `.claude/skills/`에 `dev-screen` · `spec-check` | AI → 세팅 담당 리뷰 | `sync-spec.sh`가 정본과 로컬 색인 2개를 만듦, 빈 프로젝트에서 `check` 통과 |
| **5** | 정본 만들기: `/doc-init` (기획서가 있으면 정본화, 운영 코드만 있으면 역공학, 아무것도 없으면 인터뷰) | 도메인 담당자 | 정본 v1.0.0 PR 병합 |
| **6** | 계약 만들기: `/doc-rule`로 `contracts/openapi.yaml` · `docs/contracts/00_ui_system.md` | FE · BE 리드 | 계약 PR 병합 |
| **7** | 관문 고정: app-repo main에 `check` 필수 체크, 배포 작업 첫 단계에 `scripts/check.sh --release`. spec-repo main에 PR 필수 + 코드 소유자 리뷰 필수(승인자가 1명뿐이면 아래 예외) | 사람 | 가정 주석이 남은 테스트 브랜치에서 배포 작업이 멈춤, 정본 파일을 바꾼 PR에 도메인 담당자 리뷰가 요구됨 |
| **8** | 시범 1건: `/doc-update` → `/dev-screen` → `/spec-check` → 병합 → 릴리스. 끝나면 `agentic-env.yaml`의 `setup_done: true` | 전원 | 가이드 "사례로 따라가기"가 재현됨 |

- 5 · 6단계의 디자인 준비(토큰 · 컴포넌트 매핑)는 팀이 원할 때 선택 부록 1절을 따른다. 설치 순서를 막지 않는다.
- **권한**: spec-repo는 팀 전원(도메인 담당 · 디자인 · 개발) 쓰기, 그 밖의 파트(마케팅 · 운영 · CS)는 Triage. 쓰기나 Triage가 없으면 Issue의 라벨 · 담당자가 오류 없이 빠져 `assign-issue`가 돌지 않는다(신뢰 3·학습 지식). 정본 · 계약은 CODEOWNERS와 코드 소유자 리뷰 필수로 지키므로 쓰기 권한을 넓혀도 정본은 담당자 승인 없이 바뀌지 않는다(아래 승인자 1명 예외에서는 이 보호가 없다).
- **정본 승인자가 1명뿐이면**(PO/PM 대행 포함) spec-repo main의 필수 승인 수를 0으로 두고 코드 소유자 리뷰 필수도 끈 채 본인이 병합한다. GitHub는 작성자가 자기 PR을 승인하지 못하게 하기 때문이다(신뢰 3·학습 지식). 이 동안에는 쓰기 권한이 있는 누구나 정본 PR을 병합할 수 있으므로, 정본 PR은 담당자만 병합한다는 약속을 팀에 알린다. 승인자가 둘 이상이 되면 승인 1과 코드 소유자 리뷰 필수를 켠다.
- 테크리드가 없으면 저장소 관리 권한이 있는 사람이 세팅 담당을 맡는다. 그 전까지 도메인 담당자는 `/doc-init` 인터뷰 답을 로컬 초안으로 모아 둘 수 있다.

## 2. 설정 질문 (`agentic-env.yaml`)

| # | 질문 | 기본값 | 구분 |
| :---: | :--- | :--- | :---: |
| 1 | GitHub 조직 이름, spec-repo · app-repo 이름(app-repo가 여럿이면 모두) | — | 필수 |
| 2 | GitHub 요금제, 비공개 저장소에서 필수 체크를 쓸 수 있는가 | — | 필수 |
| 3 | 기준 브랜치 | `main` | 권장 |
| 4 | 도메인 목록: 약어(ID용) · 폴더명(경로용) · 정본 파일명 | `SETT`/`settlement`/`03_정산_환불.md` | 필수 |
| 5 | 도메인 담당자(질문을 받고 정본을 승인, PO/PM 또는 대행)와 부재 시 대리인. 대행이면 위임한 사람 | — | 필수 |
| 6 | FE 리드 · BE 리드 GitHub 팀 핸들 | `@<org>/fe-leads`, `@<org>/be-leads` | 필수 |
| 7 | Blocking 범주(더하거나 뺄 것) | 금액 · 정산 수수료 · 권한 · 상태 전이 · 개인정보 · 결제 연동 | 권장 |
| 8 | 릴리스 방식(태그 · 릴리스 브랜치 · 수동)과 배포 작업 위치 | — | 필수 |
| 9 | 핫픽스를 선언할 수 있는 사람 | 테크리드 · 온콜 | 필수 |
| 10 | 화면 코드 접두어(채널 추가 여부) | `ADMN`, `USER` | 권장 |
| 11 | CI 토큰의 Secrets 이름 | `SPEC_REPO_TOKEN` | 필수 |
| 12 | 켜는 선택 부록(디자인 시스템 · 계약 테스트 · 계산기 · 메신저 알림) | 모두 끔 | 선택 |

```yaml
# spec-repo/agentic-env.yaml — 값의 <...>는 자리표시자
version: 1
org: <org>
spec_repo: <spec-repo>
app_repos: [<app-repo>]
github_plan: <free|team|enterprise>
main_branch: main
domains:
  - code: SETT
    dir: settlement
    spec_file: 03_정산_환불.md
    owners: [<github-id>]          # 질문 담당 + 정본 승인
    backup: <github-id>
    delegated_by: null             # 대행이면 위임한 사람
teams: {fe_leads: "@<org>/fe-leads", be_leads: "@<org>/be-leads"}
blocking_categories: [금액, 정산 수수료, 권한, 상태 전이, 개인정보, 결제 연동]
release: {method: tag, deploy_workflow: .github/workflows/<deploy>.yml}
hotfix_declarers: [<github-id>]
screen_prefix: [ADMN, USER]
ci_token_secret: SPEC_REPO_TOKEN
options: {design_system: false, contract_test: false, engine: false, notify: false}
setup_done: false
```

## 3. CI 토큰과 워크플로

- **토큰 1개**: app-repo의 `check`가 `spec.lock` 시점의 비공개 spec-repo를 받아야 하므로, spec-repo **Contents 읽기** 권한이 있는 fine-grained 토큰(또는 GitHub App) 하나를 app-repo Secrets에 둔다. spec-repo가 공개면 필요 없다.
- **라벨**: spec-repo에 `domain:<약어>`(도메인마다), `blocking-question`, `assumption-question`, `legacy-question`, `hotfix-sync`. app-repo에 `hotfix`.

| 워크플로 | 저장소 · 트리거 | 하는 일 |
| :--- | :--- | :--- |
| `assign-issue.yml` | spec-repo · `issues: opened, labeled` | `domain:` 라벨과 `domain-assignees.json`으로 담당자 지정. 권한 `issues: write` + `contents: read`(담당자 파일을 읽기 위해). 최소본은 5-7 |
| `check.yml` | app-repo · `pull_request`, `push: main` | `spec.lock` 정본을 받아 `scripts/check.sh` 실행. 권한 `contents: read` + CI 토큰. 최소본은 5-8 |

그 밖의 자동화(색인 커밋 · 질문 아카이브 · 상태 자동 전환 · 기한 알림)는 두지 않는다. 색인은 `sync-spec.sh`가 로컬에서 만들고, 질문 기록은 Issue 자체이며, 진행 관리는 도메인 담당자의 백로그와 주간 회의가 맡는다.

## 4. 스크립트

| 스크립트 | 하는 일 |
| :--- | :--- |
| `scripts/new-id.sh` (spec-repo) | TASK 해시(5자) 생성 |
| `scripts/sync-spec.sh` (app-repo) | `spec.lock`의 커밋으로 정본 · 계약 · 요약본(· 설치된 선택 부록)을 `/docs`에 받고 `canon_index.md`(화면코드 → 정본 앵커 · Figma URL)를 만든다. `open_tasks.md`(`status: OPEN`인 TASK와 담당자)는 spec-repo main의 최신 `docs/changes/`로 만든다. 새 TASK가 `spec.lock`을 올리기 전에도 보이게 하기 위해서다. 정본은 `gh`로 받는다(`gh repo clone` 또는 `gh auth setup-git` 뒤 git). CI 토큰은 `GH_TOKEN`으로만 넘어오고 git은 이 변수를 읽지 않기 때문이다. |
| `scripts/check.sh` (app-repo) | 린트 · 테스트, `[BLOCKED` 0개, 코드 · 테스트에 나온 POL 번호가 모두 `_registry.yaml`에 있음, 대장에 같은 번호가 두 번 없음(YAML 파서는 중복 키를 조용히 합치므로 텍스트로 센다). `--release`면 `[ASSUMPTION` 0개도 확인. 검사 대상은 앱 코드 · 테스트 폴더뿐이다(`AGENTS.md` · `.claude/` · `docs/` · `scripts/`에는 규칙 설명으로 이 글자들이 들어 있다) |

## 5. 받아 둘 파일 형식

**1. TASK frontmatter**

```yaml
---
id: TASK-SETT-20261101-b1c8e
domain: SETT
ui_change: no            # yes면 디자이너 시안 확정 후 구현
status: OPEN             # OPEN | DONE
assignee: [<github-id>]  # 비어 있으면 도메인 담당자가 백로그에서 배정
screen_ids: [ADMN-SETT-005]
pol_ids: [POL-SETT-001]
created_at: 2026-11-01
---
```

- `DONE`: 개발 PR이 병합되면 개발자 AI가 이 줄만 바꾸는 spec-repo PR을 연다.

**2. 정본 `[B]` 표와 정책 앵커**

```markdown
| 화면코드 | 화면명 | Figma URL | Ref POL | 화면 상태 |
| :--- | :--- | :--- | :--- | :--- |
| USER-MY-011 | 내 정산 내역 | https://figma.com/design/<file>?node-id=<n> | POL-SETT-005 | 기본 5 + 부분 실패 |

<a id="pol-sett-005"></a>
### [POL-SETT-005] <정책명>
```

- 열 순서는 고정이다. Figma URL이 없으면 `-`. 디자이너의 URL 등록 PR은 이 열만 바꾼다.

**3. 질문 Issue 양식** (`.github/ISSUE_TEMPLATE/question.yml`): `screen_id` · `pol_id` · `assumption`(가정 내용). 양식에서 고른 값은 본문 글자가 될 뿐 라벨이 되지 않으므로 도메인 · 종류는 양식에 두지 않는다. 웹으로 올린 사람은 제출 뒤 `domain:` 라벨과 종류 라벨을 단다.

**4. 번호 대장** (`docs/specs/_registry.yaml`)

```yaml
pol:
  POL-SETT-001: {status: active, title: <정책명>}
  POL-SETT-002: {status: retired, title: <정책명>}   # 결번은 지우지 않음
```

- 상태는 `active` · `retired` 둘뿐이다. AI는 새 번호를 `active`로 정본 PR에 함께 넣고, PR이 병합되면 확정, 반려되면 PR과 함께 사라진다. `check.sh`는 대장에 있는 번호만 통과시킨다.

**5. 담당자 매핑** (`.github/domain-assignees.json`): `agentic-env.yaml`의 `domains`에서 만든다. `{ "SETT": { "assignees": ["<github-id>"], "backup": "<github-id>" } }`

**6. CODEOWNERS**: `docs/specs/` 아래 도메인 파일 → 해당 도메인 담당자, `contracts/` → FE 리드 팀과 BE 리드 팀.

**7. `assign-issue.yml` 최소본** (spec-repo, 팀이 고쳐 써도 된다)

```yaml
name: assign-issue
on:
  issues:
    types: [opened, labeled]   # 둘이 함께 와도 같은 담당자를 다시 지정할 뿐이다
permissions:                   # 하나라도 적으면 적지 않은 권한은 none이 된다
  issues: write
  contents: read               # 없으면 비공개 저장소에서 checkout이 실패한다
jobs:
  assign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - env:
          GH_TOKEN: ${{ github.token }}
          LABELS: ${{ toJSON(github.event.issue.labels.*.name) }}
          NUM: ${{ github.event.issue.number }}
        run: |
          d=$(echo "$LABELS" | jq -r '.[] | select(startswith("domain:")) | sub("domain:";"")' | head -1)
          [ -z "$d" ] && exit 0   # domain 라벨이 없으면 아무것도 하지 않는다(디자이너 직접 요청 등)
          who=$(jq -r --arg d "$d" '.[$d].assignees // [] | join(",")' .github/domain-assignees.json)
          [ -z "$who" ] && { echo "::warning::$d 담당자 없음"; exit 0; }
          gh issue edit "$NUM" --repo "$GITHUB_REPOSITORY" --add-assignee "$who"
```

**8. `check.yml` 최소본** (app-repo)

```yaml
name: check
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - env:
          GH_TOKEN: ${{ secrets.SPEC_REPO_TOKEN }}   # 2절 질문 11의 이름
        run: bash scripts/sync-spec.sh
      - run: bash scripts/check.sh
```

- 배포 작업은 첫 단계에서 `bash scripts/sync-spec.sh && bash scripts/check.sh --release`를 부르고, 실패하면 배포 잡이 시작되지 않게 `needs`로 묶는다.
