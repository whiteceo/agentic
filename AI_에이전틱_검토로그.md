# AI 에이전틱 환경 구축 검토 및 변경 로그

> **문서 목적**: 외부 검토 모델(Genspark)의 단계별 기술 검토 피드백과 그에 따른 아키텍처 정비·개정 내역을 영구 기록하는 독립 로그 문서다.  
> **운영 원칙**: 에이전틱 환경 구축 관련 검토 상태는 본 문서에서 전담 관리한다. 2026-11-01 기존 정산 프로젝트 저장소의 `plans/`에서 이 저장소로 분리했으며, 1.1~1.7절의 `plans/` 경로와 `PROJECT_STATE.md` 언급은 분리 전 기록이다.  

---

## 1. Genspark 4~10차 기술 검토 및 아키텍처 개정 (v1.3.0 수립, 2026-11-01)

### 1.1 검토 범위 및 환경
- **검토 대상 커밋**: `802adb8` (v1.2.0, blob `bd813c3`)
- **검토 범위**: `plans/AI_에이전틱_환경_구축.md` 500줄 전수 검토 (jsDelivr 및 터미널 출력 교차 검증)
- **파일 정합성**: 원본 커밋(`802adb8`, 55,191B)과 로컬(55,691B) 간 500B 차이는 500행 개행(LF ➔ CRLF) 차이임을 수치 검증 완료

---

### 1.2 핵심 미결 사항 및 7대 해결 결정 내역 (A1 ~ A7)

| 번호 | 검토 지적 사항 | 최종 결정 및 정본 반영 내용 | 적용 위치 |
| :---: | :--- | :--- | :--- |
| **A1** | **질문 파일 생성 위치 불일치**<br>• 개발 저장소(`app-repo`)의 `/docs`는 `.gitignore`된 사본인데, AI가 그 안에 질문 파일을 생성하면 커밋/PR/CODEOWNERS가 동작하지 않음<br>• CI 검사 범위에 질문 상태 조회 누락 | • **원격 GitHub Issue 직접 발의**: 개발자 AI는 로컬 파일이 아닌 GitHub CLI(`gh issue create --repo <org>/spec-repo`)로 원격 `spec-repo`에 질문 Issue를 직접 발의<br>• **spec-repo는 결과 아카이브**: 질문이 해결(`RESOLVED`)된 후 최종 결론만 `docs/questions/<도메인>/Q-*.md`로 아카이브 커밋<br>• **CI 검사 범위 확장**: `check.sh`에 spec-repo 질문 API 연동을 통한 OPEN 상태 주석 차단 검사 및 hotfix 3영업일 기한 검증 추가 | 제1.2절, 제1.4-(2)절, 제3.4절 |
| **A2** | **ASSUMPTION 주석 해소 시점 다중성**<br>• L243, L245, L479, L497 간 주석 차단 기준 불일치 | • **OPEN 상태 주석만 차단, RESOLVED 주석은 병합 허용**으로 통일<br>• GitHub Issue가 `RESOLVED` 처리된 주석은 main 병합을 허용하며, 다음 화면 작업이나 정기 리팩토링 시 정규 `@policy POL-ID` 주석으로 교체 권장 | 제1.4-(2)절, 제3.4절, 제3.5절, 제4절 |
| **A3** | **LATEST_TASK.md 충돌 및 status 누락**<br>• 다중 PO 동시 작업 시 인덱스 파일 충돌 가능성<br>• TASK 파일의 완료 상태 필드 누락 | • **현행 분산 구조 유지 및 status 필드 보강**<br>• `docs/changes/<도메인>/TASK-*.md` frontmatter에 `status: OPEN \| IN_PROGRESS \| DONE` 필드 명시<br>• `LATEST_TASK.md`는 미완료(`OPEN`, `IN_PROGRESS`) 안건 목록을 자동 취합 | 제1.2절, 제1.4-(1)절 |
| **A4** | **POL 정책 본문 위치 엇갈림**<br>• 정책 추적 ID 절([B]에 헤더 위치)과 초기 정본 스킬([C]에 본문 정의) 간 모순 | • **본문은 [C]에 1회만 단일 정의, [B] 화면 행에는 POL ID 목록과 Figma URL만 간결 매핑**<br>• 정책 1건이 다수 화면에 적용되는 현실을 반영하여 중복 제거<br>• `canon_index.md`가 화면 × POL 매핑을 1:1로 펼쳐 보여줌 | 제1.2.2절, 제3.1절 |
| **A5** | **Figma Node URL의 정본 [B] 등록 주체 미정**<br>• URL 원본은 기획 정본 [B]이나 생성 주체는 디자이너임 | • **UIX 디자이너가 [B]의 URL 칸만 수정하는 경량 PR 제출 및 PO/PM 승인**<br>• 디자이너가 시안을 `Ready for Dev`로 확정할 때 직접 PR을 발의하고 PO가 승인·병합함으로써 Root SSOT에 시각 정본 URL 안착 | 제1.2.1-2절, 제1.5절 |
| **A6** | **Level 3 Hotfix 범위 모순 및 기한 미정**<br>• L3에 단순 오탈자가 포함되어 L271("운영 장애에만 한정")과 충돌<br>• 3영업일 카운트 주체 및 기준 시점 모호 | • **L3는 운영 긴급 장애에만 한정 적용, 프로덕션 단순 오탈자는 L2 정기 패치로 이동**<br>• **기한 3영업일 유지**: CI가 hotfix PR 병합 완료 시점부터 영업일 3일을 자동 계산하며, 3영업일 이내 정본 사후 동기화 PR 미완료 시 다음 정기 릴리스 main 병합 자동 차단 | 제0절, 제1.4-(4)절 |
| **A7** | **검토 기록 보관 위치**<br>• PROJECT_STATE.md 기준선 유지 필요 | • **본 문서(`plans/AI_에이전틱_검토로그.md`)를 전용 로그로 신설**하여 체계적 관리 | 본 문서 |

---

### 1.3 소소한 정비 사항 (5대 항목) 반영 내역

1. **Short Hash 자릿수 일치**:
   - `docs/changes/settlement/TASK-SETT-20261101-b1c.md` (3자리) ➔ `TASK-SETT-20261101-b1c8.md` (4자리)로 예시 수정 (4~6자리 규격 충족).
2. **질문 발의 라벨 세분화 및 알림 실패 폴백**:
   - `blocking: true` ➔ `--label "domain:<도메인>" --label "blocking-question"`
   - `blocking: false` ➔ `--label "domain:<도메인>" --label "assumption-question"` (비차단 질문에 blocking 라벨 부착 방지)
   - 웹훅/gh CLI 호출 실패 시 로컬 `tmp/questions-failed/` 큐에 에러 로깅 후 터미널 경고 출력 및 다음 실행 시 재시도.
3. **색인 예시 파일명 통일**:
   - `canon_index.md` 표 예시의 `03_정산.md` ➔ 저장소 표준 파일명인 `03_정산_환불.md`로 일치.
4. **용어 사전 및 검수 판정 등급 영문 표기 일치**:
   - 용어 사전 L21: `🟡 Assumption Validated` ➔ `🟡 Pending`으로 수정.
   - 검수 5대 등급: `✅ 일치 (Validated)`, `❌ 위반/누락 (Mismatch)`, `⚠️ 임의 구현 (Untracked)`, `🟡 가정 진행 (Pending)`, `❓ 정본/시안 미정의 (Missing)` 영문명 문서 전수 반영.
5. **OpenAPI 계약 변경 상호 승인 기술적 강제**:
   - GitHub Branch Protection의 "Code Owner 1명 + 1명" 우회 가능성을 차단하기 위해, **FE 테크리드 팀(@org/fe-leads) 1명 이상 승인 AND BE 테크리드 팀(@org/be-leads) 1명 이상 승인을 모두 검증하는 필수 CI 상태 체크(Required Status Check)** 워크플로 결합을 명시.

---

### 1.4 산출물 동기화 현황
- `plans/AI_에이전틱_환경_구축.md` (Executable Spec v1.3.0 수립 완료)
- `plans/AI_에이전틱_환경_가이드.html` (Visual Guide v1.3.0 동기화 완료: 용어사전, 질문 Issue 발의, Hotfix 게이트 3영업일)
- `plans/AI_에이전틱_검토로그.md` (본 검토 로그 문서 신설)
- `PROJECT_STATE.md` (정산 엔진 v7.21 기준선 불변 유지)

### 1.5 Genspark 5차 사전 커밋 검토 (커밋 전 미세 조정 5건) 및 향후 메커니즘 과제

#### (1) 커밋 전 미세 조정 5건 반영 내역
1. **GitHub CLI 라벨 플래그 문법 교정 (제1.4-(1)절, 제3.4절)**:
   - `--label "domain:<도메인>", "blocking-question"`의 쉼표/따옴표 분리 오류를 `--label "domain:<도메인>" --label "blocking-question"`(및 `assumption-question`)으로 전수 수정하여 셸 환경별 인자 파싱 깨짐 원천 차단.
2. **검토로그 diff 노출 (`git add -N`)**:
   - 새로 생성된 `plans/AI_에이전틱_검토로그.md`가 untracked 상태여서 `git diff` 및 `--stat`에 미포함되던 현상을 해결하기 위해 `git add -N`을 적용, 전체 diff에 포함하여 RULES A3 준수.
3. **HTML 가이드 용어 사전 동기화**:
   - `가정 진행 (Pending)` 설명에서 A2 결정(RESOLVED 주석은 main 병합 허용, 미해결 OPEN 상태 주석만 병합 차단)을 반영하여 MD 정본과 일치.
   - SVG 다이어그램 및 용어 사전의 `Q-*.md` 표기를 `질문 Issue` 및 `Q-ID Issue` 체계로 전수 동기화.
4. **Visual SSOT Figma URL 원본 경로 점검**:
   - 제1.2.1-2절 시각 정본 경로가 기획 정본 표준 경로인 `docs/specs/`의 `[B] 화면 명세` 표로 단일화되어 있음을 최종 확인 (과거 턴의 오기 `01_master_policy.md` 잔존 없음).
5. **질문 파일 생성 구 문맥 전수 제거 및 Issue 체계 단일화**:
   - 채번 규칙: "여러 에이전트가 동시에 질문 Issue를 발의해도"로 수정.
   - 단일 식별자 표준: `Q-<도메인>-YYYYMMDD-<short_hash>` 단일화 (이중 ID 및 레거시 ID 예외 없이 단일 정규식 준수).
   - 에이전트 협업 규약 5번: "spec-repo에 질문 GitHub Issue로 발의"로 통일.
   - `/doc-init` 레거시 의심 로직: spec-repo에 `legacy-question` Issue로 발의 후 해결 시 `docs/questions/`에 아카이빙하는 규칙으로 일원화 (핵심 정책 공백에 한해 `blocking-question` 라벨 선택 추가).
   - 출구 조건(Exit Gate) 명문화: `[ASSUMPTION: Q-ID]` 주석 해소 판정 시 GitHub Issue가 `Closed(completed, state_reason == completed)` 상태여야 main 병합 허용 (`not_planned` 종결 건은 차단).

#### (2) 차기 고도화 메커니즘 과제 (외부 검토 제안)
- **정본 반영 PR과 Issue 종결 연동**:
  - PO/PM 정본 수정 PR 본문에 `Closes #142` 키워드를 명시하여 PR이 기본 브랜치 머지 시 Issue가 자동 종결되도록 유도.
  - CI는 Issue의 `state_reason == completed` 여부까지 검증하여 `not planned` 종결 질문의 비인가 통과 차단.
- **ASSUMPTION 주석 CI 자동 검사 규칙**:
  - CI가 코드 내 `[ASSUMPTION: Q-ID]`를 파싱하여 spec-repo의 Issue 제목(`[Q-ID]`)과 대조.
  - Issue를 조회할 수 없거나(발의 실패로 인한 미등록 포함), 조회된 Issue가 미해결(`OPEN`) 상태이거나 `not_planned`·`duplicate`로 종결된 경우 main 병합을 즉시 차단 (`state_reason == completed` 정상 종결 건만 통과).
- **저장소 간 CI 권한 (GitHub App / PAT)**:
  - `app-repo` CI 기본 토큰(`GITHUB_TOKEN`)은 타 저장소(`spec-repo`) Issue 읽기 권한이 제한되므로, 프로덕션 환경 구축 시 GitHub App 또는 read 권한 PAT 구비 필요성을 가이드.
- **Hotfix 3영업일 자동 추적 연동**:
  - 사후 동기화 PR 본문에 원본 hotfix PR URL을 필수로 바인딩하여 CI가 머지 시점과 영업일 3일을 정확히 추적.
  - 사내 공휴일 캘린더 API/JSON 출처를 표준화하여 영업일 산정 신뢰성 확보 (캘린더 연동 전에는 머지 완료 시점 기준 주말 제외 평일 3일 산정 규칙 적용).

---

### 1.6 Genspark 6~10차 사전 커밋 검토 (정밀 보강 및 단일화) 반영 내역

1. **질문 Issue 담당자 자동 지정 (Assignee) 메커니즘 단일화 (제1.4-(2)절, 제1.4-(5)절)**:
   - CODEOWNERS는 PR 리뷰어 전용 도구이므로, 개발자 AI는 `domain:<도메인>` 라벨만 부착하여 발의하고, spec-repo GitHub Actions(`.github/workflows/assign-issue.yml`)가 도메인 매핑 설정(`.github/domain-assignees.json`)을 참조하여 담당 PO/PM을 Issue Assignee로 자동 지정하도록 단일화.
   - 웹훅 알림 대상이 아닌 `assumption-question` 및 `legacy-question`도 담당자 배정이 누락되지 않도록 조치.
2. **Hotfix 사후 동기화 기한 시작 시점 및 평일 산정 단일화 (제1.2절, 제1.4-(4)절)**:
   - "hotfix PR 병합 완료 시점"으로 기한 산정 기준 시점을 전수 일치시키고, 임의의 72시간 대신 "주말을 제외한 평일 3일(사내 공휴일 캘린더 연동 시 공휴일 자동 제외)" 기준으로 명확히 규정.
3. **`not_planned` 기각 및 `duplicate` 중복 종결 처리 절차 명문화 (제1.2절, 제1.4-(2)절, 제3.4절)**:
   - `Closed: not_planned` 기각 시: 임시 가정 코드 삭제·롤백 및 `[ASSUMPTION: Q-ID]` 주석 제거로 병합 차단 해소.
   - `Closed: duplicate` 중복 종결 시: 주석의 Q-ID를 먼저 발의된 원본 Issue의 Q-ID로 교체하여 원본 질문의 해결·종결 여부를 추적하도록 명시 (출구 조건에서 not_planned · duplicate 종결 건 병합 차단 명문화).
4. **미세 어휘 및 명칭 정비**:
   - 레거시 Issue 발의 문구: `--label "blocking-question"` 라벨 추가 부착으로 단일 발의 의미 명확화.
   - Level 2 명칭 정비: `Logic Fast-Track` ➔ `Logic & Patch Fast-Track` (UI 무변동 로직 및 단순 패치).
   - `/doc-update` Step 1 미해결 질문 목록에 `legacy-question` 명시.
   - 질문 아카이브 YAML frontmatter: `status: CLOSED`, `resolution: completed | not_planned | duplicate`, `duplicate_of: null` 필드 구비 및 `docs/questions/` 역할을 종결(completed, not_planned, duplicate) 아카이브로 명문화(기각·중복 건도 resolution 상태값과 함께 아카이브 커밋).
   - 버전 번호 상향: 질문 체계의 근본적 개편(로컬 파일 ➔ 원격 GitHub Issue) 및 출구 조건 정밀화에 따라 사양서 및 가이드 버전을 `v1.2.0`에서 `v1.3.0`으로 상향 일치.

---

### 1.7 Claude Code 최종 검토: 환경 변수 분리 및 MD ↔ HTML 정합성 (2026-11-01)

1. **온보딩 질문지 신설 (`plans/AI_에이전틱_온보딩_질문지.md`)**:
   - 본문에 하드코딩된 운영 SLA · 인프라 · 조직 매핑 값 46개를 `ENV-01`~`ENV-46`으로 분리(저장소 · 도메인 담당자 · 식별자 · 질문 Issue · SLA 게이트 · CI · 디자인 · 채널 8개 묶음). 항목마다 기본값(본문 값) · 필수/권장/선택 · 결정 주체 · 본문 위치를 적었다.
   - 답변 기록 파일 `spec-repo/agentic-env.yaml` 서식과 프로젝트 유형별 우선 질문을 함께 제시.
   - 본문에 없던 빈칸을 질문으로 추가: 저장소 간 CI 권한(ENV-06), 정기 릴리스 판별 방법(ENV-26), Blocking 질문 답변 기한 · 에스컬레이션(ENV-22), 담당자 부재 시 대리인(ENV-09).
2. **실행 명세서 반영**: 0.1절(환경 변수 읽는 법 · 종결 상태 표기 규칙) 신설, 저장소 구조에 `agentic-env.yaml` 추가, 해당 수치 옆에 `ENV-xx` 참조 표시, 4절 협업 규약 6번(설정값은 `agentic-env.yaml` PR로만 변경) 추가. 기본값 자체는 바꾸지 않았다.
3. **종결 상태 용어 단일화**: GitHub에 없는 `RESOLVED` 표기를 `completed`(`Closed: completed`)로 전수 교체(MD 10곳 · HTML 4곳). "RESOLVED 주석은 병합 허용" 문구가 `not_planned` · `duplicate` 종결 건까지 허용하는 것처럼 읽히던 모순을 해소하고, 병합 허용은 `completed`만이라는 1.4-(2) 규칙과 용어 사전 · 3.5 · 4절을 일치시킴. CI 설명의 "OPEN 상태 주석 차단"도 "미종결 주석 차단"으로 정정.
4. **HTML 잔존 구체계 제거**: 폐지된 `docs/changes/QUESTIONS.md` 표기 8곳(조감도 · 피드백 루프 · 저장소 구조 · 06절 · 확장 제안 모달, 주석 2곳)을 질문 Issue 체계로 교체.
5. **명칭 · 경로 일치**: HTML `Level 2 · Logic Track` ➔ `Logic & Patch`(설명도 "UI 무변동 로직 · 단순 패치"), 판정 등급 `❓ 미정의 질문` ➔ `❓ 정본/시안 미정의`(MD 2절 · HTML 용어 사전), `/doc-rule` 산출물에 `contracts/openapi.yaml` 병기(HTML 07절 · 로드맵 STEP 2), MD `digest/<화면코드>_baseline.md` ➔ `digest/<화면코드>.md`(3.1절과 일치), 3.5 `Pact/Prism` ➔ 기본 Prism.
6. **HTML 안내 보강**: 로드맵 STEP 1에 질문지 작성 단계 추가, 서랍 메뉴에 질문지 다운로드 버튼 추가. 바뀐 SVG 문구 10개는 Playwright 렌더링으로 상자 안에 들어가는지 확인(넘침 0, 콘솔 오류 0).

---

### 1.8 저장소 분리 (2026-11-01)

- 범용 규약 문서라 정산 프로젝트에서 분리해 독립 저장소 `agentic`으로 옮겼다. `plans/` 아래 에이전틱 파일 4개와 `assets/hero-agentic-system.jpg`의 커밋 이력 17개를 보존했고, 파일은 저장소 최상위에 둔다.
- 가이드 HTML은 GitHub Pages(`main` 브랜치 루트)로 연다. `index.html`이 가이드로 연결한다.

### 1.9 분리 후 정합성 재점검 (2026-11-01)

- HTML에만 남아 있던 "마스터 정책서" 표기를 명세서 용어 "도메인별 정본(PRD)"으로 통일(2곳).
- Code SSOT 설명에 기계 정본 `contracts/openapi.yaml`을 병기하고 `00_domain_contracts.md`는 해설서로 표기(2곳). 용어 사전 추적 ID 설명의 "고유" ➔ "영구"(명세서 0절과 일치).
- 저장소 분리로 깨지는 상대 경로 없음 확인(MD 다운로드 · 질문지 다운로드 · 표지 이미지 모두 저장소 최상위 기준).

### 1.10 설계 검토 반영 (정책 판단이 필요 없는 항목, 2026-11-01)

Claude Code 설계 검토 21건 중 정책 판단이 필요한 2건(비차단 ASSUMPTION 차단 시점, 핫픽스 기한 초과 시 벌칙)과 HTML 용어 사전 축소(P3)를 뺀 18건을 반영했다.

1. **게이트 2층 원칙**(1.2): CI 필수 체크는 결정론적 검사만 두고, `/spec-check` 판정은 PR 코멘트 리포트 + 리뷰어 판단으로 분리. 3.5 표 · 핫픽스 `--hotfix` · 4절 2번 문구를 이에 맞춤.
2. **Q-ID를 Issue 번호 기반으로**: `Q-<도메인>-<Issue번호>`(예: `Q-SETT-142`), CI는 번호로 직접 조회(제목 대조 폐지). 발의 실패 시 `Q-PENDING` 표기 후 CI 차단. TASK 해시는 `scripts/new-id.sh`가 생성.
3. **정본 버전 고정**: app-repo `spec.lock`(spec-repo 커밋 SHA), 정본 갱신은 별도 PR.
4. **인덱스 생성 주체**: `LATEST_TASK.md` · `canon_index.md`는 spec-repo main 머지 후 GitHub Actions가 생성(사람 · AI PR에 포함 금지), 색인 위치는 줄 번호 대신 제목 앵커. TASK `DONE` 전환과 질문 아카이브 파일도 Actions 담당.
5. **번호 대장**: `docs/specs/_registry.yaml`에 POL · ADR 번호 예약 + CI 중복 검사. AI는 번호를 제안만 한다.
6. **그 밖**: FE · BE 상호 승인 체크의 구현 부담과 수동 시작안, 계약 필드 변경 승인 범위(POL 필드 = PO/PM), 변경 등급은 PO/PM 확정 + `[B]` 변경 시 L1 승격, Track A 골격 밖 화면의 탈출 경로, Blocking 대기 중 스텁(`[BLOCKED: Q-ID]`) 처리, 정답 채널 단일화, Issue 본문 보안 규칙, L3 선언 주체(ENV-47), 레거시 질문 상한(ENV-48), Figma 도구명 일반화 · Code Connect 대안, 절대 표현 · 근거 없는 수치 정리, "HTML과 다르면 MD가 맞다" 원칙.
7. **질문지**: ENV-05 · 14 · 39 · 40 · 46 갱신, ENV-47 · 48 추가(총 48개).

### 1.11 정책 결정 2건 반영 (white 결정, 2026-11-01)

1. **ASSUMPTION 게이트를 2단계로**: main 병합은 미해결(`OPEN`) 주석도 허용하고, 릴리스(ENV-26) 시점에 `completed` 종결 주석만 허용한다. Issue가 없는 `Q-PENDING` · 조회 불가 주석과 정리하지 않은 `not_planned` · `duplicate` 주석은 main 병합부터 막는다. 사소한 문구 가정이 PO/PM 답변을 기다리며 피처 PR을 묶지 않게 하되, 정본에 없는 가정은 운영에 나가지 않게 한다. (1.4-(2) 2, 0절 용어 사전, 3.4, 3.5, 4절 4번, 질문지 ENV-26 · 27, HTML 용어 사전)
2. **핫픽스 기한 초과는 알림 · 에스컬레이션만**: hotfix PR 병합 시 Actions가 `hotfix-sync` Issue를 만들어 담당 PO/PM에게 배정하고, 영업일 3일(ENV-23)을 넘기면 재알림 후 리드 PO/PM · 테크리드에게 에스컬레이션한다. 개발 병합은 막지 않는다(차단은 ENV-25 선택지로 남김). (1.2 CI 설명, 1.4-(4) 표, 질문지 ENV-25, HTML 06절 · 용어 사전)

### 1.12 가이드 HTML 리디자인 (2026-11-01)

- 어두운 글래스 테마와 대형 SVG 위주였던 가이드를 종이 질감의 편집형 단일 페이지로 다시 썼다(라이트 기본, 다크 모드 자동 · 전환 버튼, 모바일 대응, 고정 목차).
- 내용은 명세서 v1.3.0과 1.10 · 1.11절 결정(게이트 2층, Issue 번호 Q-ID, `spec.lock`, ASSUMPTION 2단계, 핫픽스 에스컬레이션)에 맞춰 11개 절로 재구성했다. 근거 없는 토큰 절감 수치 섹션은 뺐다.
- 용어 사전을 17개에서 핵심 8개로 줄이고 전체 사전은 명세서 0절로 안내(설계 검토 P3-18 반영). 표지 이미지(`assets/hero-agentic-system.jpg`)는 더 이상 쓰지 않는다.

### 1.13 가이드 HTML 디자인 교체 (white 선택, 2026-11-01)

- 1.12절의 편집형 디자인(명조 제목 · 베이지 바탕)은 white 평가로 폐기했다. 다크 제품 랜딩 · 라이트 문서형 · 브리핑 슬라이드형 시안 3개 중 white가 **다크 제품 랜딩형(A)**을 골라 전체 11개 절을 다시 만들었다.
- 글꼴은 Pretendard 한 가지만 쓰고, 한글에는 고정폭 글꼴을 쓰지 않는다. 내용은 1.12절과 같다.
