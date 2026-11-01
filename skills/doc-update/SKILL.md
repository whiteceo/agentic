---
name: doc-update
description: 도메인 담당자가 정책이나 요구사항 변경을 말로 지시하면, POL 번호로 영향 범위를 찾아 보고하고, 승인 후 정본·계약을 고치고 작업 지시서(TASK)를 만든다. 핫픽스 사후 동기화(--sync-from-code)도 맡는다.
---

# /doc-update — 정책 변경

규칙은 `AGENTS.md`를 따른다. 승인 전에는 파일을 고치지 않는다.

## 1. 영향 조회와 보고
1. 변경 내용을 듣고 관련 POL 번호를 찾는다. 새 정책이면 다음 번호를 제안한다.
2. `grep -rniE "POL[-_]<도메인>[-_]<번호>"`로 정본 · `contracts/` · 요약본 · (계산기 부록을 켰으면) `engine/`을 찾는다.
3. 보고: 바뀔 정본 절, 영향 화면 코드, Figma URL(있으면), 계약 수정 여부, 관련된 열린 질문 Issue, 화면 UI가 바뀌는지(`ui_change` 제안). `[B]` 표가 바뀌면 `ui_change: yes`다.

## 2. 승인 후 개정
1. 정본 본문과 `## 문서 개정 이력`(버전 · 날짜 · 담당자 · 화면 코드 · POL · 요약)을 고친다.
2. 응답 필드나 산식이 바뀌면 `contracts/openapi.yaml`을 함께 고친다. 영향 화면의 요약본을 갱신한다.
3. 결정 배경은 PR 본문에 적는다.

## 3. 작업 지시서
1. `scripts/new-id.sh`로 id를 받아 `docs/changes/<도메인 폴더>/TASK-<도메인>-YYYYMMDD-<hash>.md`를 만든다(frontmatter는 설치서 5-1).
2. 담당자를 물어 `assignee`에 적는다. 모르면 비워 두고 "담당자 미정, 백로그에서 배정 필요"라고 보고한다.
3. PR 본문에 담당자를 `@계정`으로 적어 알림이 가게 한다.

## 4. 핫픽스 사후 동기화 (`--sync-from-code`)
`hotfix-sync` Issue가 가리키는 핫픽스 PR의 diff를 읽고, 바뀐 규칙을 정본에 반영하는 PR을 만든다. PR 본문에 핫픽스 PR과 Issue 번호를 적고, 병합되면 Issue를 닫는다.
