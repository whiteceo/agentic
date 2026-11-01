# AI 에이전틱 선택 부록 (v1.0.0)
<!-- 배포 전 작업본. 내부 개정 기록은 AI_에이전틱_검토로그.md에만 둔다. -->

> 핵심 규약만으로 파이프라인은 돈다. 이 부록은 팀이 `agentic-env.yaml`의 `options`에서 켠 항목만 따른다. 켜지 않은 항목은 AI가 읽지 않는다.
> 어느 항목도 핵심 규약의 기준 순서(정본 > 계약 > 시안)와 질문 규칙을 바꾸지 않는다.

## 1. 디자인 시스템 (`options.design_system`)

1. **시안과 골격**: 유저 화면(`USER-*`)은 Figma 시안이 기준이고, 백오피스(`ADMN-*`)는 표준 골격 4종이 기준이다. 시안이 있는 백오피스 화면은 시안을 따른다.
2. **Figma MCP**: AI가 Figma 시안을 직접 읽는 연결이다. 디자이너와 개발자의 Figma 좌석 · Dev Mode 권한이 필요할 수 있다(신뢰 3·학습 지식).
3. **컴포넌트 매핑**: Figma 컴포넌트와 코드 컴포넌트를 잇는다. Figma Code Connect를 쓸 수 있으면 FE 리드가 코드 저장소에서 설정하고(요금제 확인), 못 쓰면 `00_ui_system.md`의 매핑표로 대신한다. AI는 매핑된 기존 컴포넌트를 쓰고 새 버튼 · 모달을 만들지 않는다.
4. **토큰**: Figma Variables를 원본으로 두고 코드용 토큰은 빌드한다. 색 이름 토큰(`blue-500`)과 용도 이름 토큰(`color-bg-danger`)을 나누고 AI는 용도 이름 토큰만 쓴다. 표준 포맷은 W3C DTCG를 권장한다.
5. **Ready for Dev 점검**: 상태 5종(핵심 규약)에 더해, 토큰에 연결되지 않은 값과 분리(Detach)된 인스턴스를 몇 개까지 허용할지 UIX 팀이 정한다.
6. **디자인 준비 순서**: 정본 만들기와 동시에 UIX 리드는 Figma 라이브러리를 게시하고, FE 리드는 매핑을 설정한다. 설치 순서를 막지 않는다.

## 2. 계약 테스트와 Mock (`options.contract_test`)

1. `check.sh`에 계약 테스트를 추가한다. 기본 도구는 Prism(스키마 기반 Mock 서버와 응답 검증)이며 팀이 바꿀 수 있다.
2. FE는 서버 완성 전 Prism Mock을 띄워 화면을 만든다.
3. FE · BE 상호 승인을 기계로 강제하고 싶으면 `contracts/**` PR에서 FE 팀 · BE 팀 승인을 각각 1명 이상 확인하는 워크플로를 둔다. 팀 소속 조회에 조직 읽기 권한 토큰이 필요하다. 기본은 핵심 규약 9-4의 "두 리드를 리뷰어로 건다"다.

## 3. 도메인 계산기 (`options.engine`)

1. 정산 · 결제처럼 금액이 핵심인 도메인에만 둔다. `engine/<도메인>/`에 기준 계산기와 정답 시나리오 JSON을 둔다.
2. `check.sh`가 앱의 계산 결과를 정답 시나리오와 대조한다.
3. `/doc-update`는 산식이 바뀌면 시나리오도 함께 고친다.

## 4. 메신저 알림 (`options.notify`)

1. 기본은 GitHub 알림이다. 메신저(Slack · Teams)로도 받고 싶으면 `assign-issue` 워크플로가 `blocking-question` Issue에 한해 웹훅을 보낸다. 웹훅 주소는 spec-repo Secrets에 두고 이름만 `agentic-env.yaml`에 적는다.
2. 웹훅은 워크플로 한 곳에서만 보낸다. AI와 로컬 스크립트는 웹훅을 부르지 않는다.

## 5. 다른 업무 도구와 연결 (미설계)

사내 업무 플랫폼이나 Google Workspace(시트 · 챗)를 붙이고 싶으면 별도로 설계한다. 어느 경우에도 정답 기록은 Git(정본 · TASK)과 spec-repo Issue 하나이고, 다른 도구는 알림과 보기 용도로만 쓴다.

## 6. 청사진: 지금 도입할 것과 이후 목표 (미설계)

지금 이 체계는 사람과 AI가 함께 따르는 운영 규약에 가깝다. 아래처럼 두 층으로 나눈다.

**지금 바로 도입(현재 설계)**: 정본 · API 계약 · 시안, 작업 지시서 · 질문 Issue, 스킬 5종, 자동 검사 · 배포 관문.

**이후 바라볼 목표(+ 요소)**: 완전한 AI 에이전틱 시스템이 되려면 현재 설계 위에 아래 요소가 더해져야 한다. 이번에는 과제로 남겨 둔다.

| 요소 | 한 줄 설명 | 참고 |
| :--- | :--- | :--- |
| 실행 엔진(오케스트레이터) | 질문 Issue나 작업 지시서가 올라오면 에이전트를 실행하고 일을 나눔(이 체계에 적용한 모습) | Anthropic, OpenAI |
| 가드레일 · 사람 승인 | 입력 · 출력 검사, 위험한 작업은 사람이 승인 | OpenAI |
| 보안 | 에이전트 신원 · 최소 권한 · 비밀값 관리 | OWASP |
| 관측성 · 모니터링 | 에이전트 실행 추적과 로그 | OpenTelemetry |
| 평가 | AI 결과 품질을 정해진 시나리오로 반복 측정 | Anthropic |
| 비용 관리 | AI 사용량(토큰) 측정과 한도. 사용량 기록 항목은 OpenTelemetry 생성형 AI 표준을 따름 | OpenTelemetry |
| 도구 연결 표준 | MCP로 GitHub · Figma · 사내 시스템 연결 | MCP 명세 |
| 기억 · 지식 색인 | 작업 간 기억과 정본 검색 | Anthropic |
| 인프라 | 에이전트 실행 환경 · 샌드박스 배포와 관리. 격리된 환경에서 먼저 시험 | Anthropic |

참고 자료:
- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, Demystifying evals for AI agents: https://www.anthropic.com/research/demystifying-evals-for-ai-agents
- OpenAI, A practical guide to building agents: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- OpenTelemetry, AI Agent Observability: https://opentelemetry.io/blog/2025/ai-agent-observability/
- OpenTelemetry, 생성형 AI 표준 속성(Semantic Conventions): https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/
- OWASP Top 10 for Agentic Applications: https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
- Model Context Protocol 명세: https://modelcontextprotocol.io/specification/2026-07-28
