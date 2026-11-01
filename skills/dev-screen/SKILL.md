---
name: dev-screen
description: 자기에게 배정된 작업 지시서(TASK)의 화면을 요약본·해당 정본 절·필요한 API operation만 읽어 구현하고, 정본에 없는 것은 Blocking 질문 또는 가정 진행으로 처리한 뒤 check를 돌린다.
---

# /dev-screen — 화면 구현

규칙은 `AGENTS.md`를 따른다.

## 1. 준비
1. `bash scripts/sync-spec.sh`. 지시서가 더 새 정본을 요구하면 `spec.lock`만 바꾸는 PR부터 연다.
2. `/docs/open_tasks.md`에서 `assignee`에 내 계정(`gh api user`)이 있는 TASK를 고른다. 없으면 다른 TASK를 집지 않고 "배정된 지시서 없음"으로 알리고 멈춘다.

## 2. 읽기 (이것만 읽는다)
- TASK 파일, 화면별 `docs/digest/<화면코드>.md`, `canon_index.md`가 가리키는 정본 절.
- `contracts/openapi.yaml`에서 그 화면이 쓰는 operation과 참조 스키마만(`yq` 등으로 잘라 읽는다). 계약 파일 전체를 읽지 않는다.
- 백오피스 화면이면 `00_ui_system.md`의 해당 골격 절.

## 3. 구현
1. Figma URL이 있으면 시안을 우선하고(디자인 부록을 켠 팀은 Figma MCP로 읽는다), 없으면 표준 골격에 맞춘다. 맞는 골격이 없으면 가장 가까운 골격으로 만들고 PR에 적는다.
2. 서버가 아직 없으면 계약의 예시 응답으로 화면을 완성한다.
3. 시안이 `Ready for Dev`가 아니거나 화면 상태 5종이 빠졌으면 알린다.

## 4. 정본에 없는 것
- **Blocking 범주**: `gh issue create --repo <org>/<spec-repo> --title "[<도메인>] <제목>" --label "domain:<도메인>" --label blocking-question` → 그 분기를 미구현 예외 + `// [BLOCKED: Q-<도메인>-<번호>]`로 막고 다른 작업을 계속한다.
- **사소한 것**: 같은 명령에 `--label assumption-question` → `// [ASSUMPTION: Q-<도메인>-<번호>] <가정>`을 달고 계속한다.
- `gh`가 실패하면 멈추고 사용자에게 알린다.
- 이전 질문이 닫혔으면 정리한다: `completed`는 `// @policy POL-...`로 바꾸고, `not_planned`는 가정 코드를 되돌리고, `duplicate`는 원본 Q-ID로 바꾼다.

## 5. 마무리
1. `/spec-check`로 셀프 대조, `bash scripts/check.sh` 통과.
2. 테스트에 `@policy POL-...` 주석, 커밋에 화면 코드와 `Ref: POL-...`.
3. PR 본문 첫 줄 `Task: <TASK id>`. 병합되면 spec-repo에 그 TASK의 `status: DONE` 한 줄만 바꾸는 PR을 연다.
