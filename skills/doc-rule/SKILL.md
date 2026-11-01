---
name: doc-rule
description: 병합된 정본에서 FE와 BE가 함께 쓰는 API 계약(contracts/openapi.yaml)과 화면 골격 규약(docs/contracts/00_ui_system.md)을 만들거나 갱신한다.
---

# /doc-rule — 공통 계약 뽑기

규칙은 `AGENTS.md`를 따른다. 결과는 PR이며 FE 리드와 BE 리드가 모두 리뷰한다.

## 1. API 계약 (`contracts/openapi.yaml`)
1. 도메인별 식별자 접두어와 공통 상태값(enum)과 한글 라벨.
2. 화면이 쓰는 엔드포인트와 요청 · 응답 스키마, 예시 응답(FE가 서버 완성 전에 쓸 수 있게).
3. 정책이 걸린 필드 · 엔드포인트의 `description`에 `[POL-<도메인>-<번호>]`.
4. `POL-`이 붙은 필드의 의미 · 산식은 정본에 있는 그대로만 쓴다. 정본에 없으면 질문 Issue로 올린다.

## 2. 화면 골격 (`docs/contracts/00_ui_system.md`)
1. 백오피스 표준 골격 4종: `List-Modal`, `Detail-Form`, `Stats-Dashboard`, `Tabs-Complex`. 슬롯(검색 필터 · 표 컬럼 · 모달 · 상태 배지) 규격.
2. 상태 배지와 상태값(enum)의 대응.
3. 디자인 시스템 부록을 켠 팀이면 컴포넌트 매핑표(Figma 컴포넌트명 ↔ 코드 컴포넌트)와 토큰 규칙(선택 부록 1절).
