# Agent Guide

공개 저장소: [chyj1022/Agent-Guide](https://github.com/chyj1022/Agent-Guide). AI 진입점: [AGENTS.md](AGENTS.md).

해커톤에서 AI 앱을 설계할 때, 에이전트에게 어떤 일을 맡기고 무엇을 코드로 통제해야 하는지 찾는 한국어 가이드입니다. 사용자 제공 강의 PDF 두 권의 개념을 재서술하고, 앱 구조, MCP 연결, 하네스, 평가에 적용하는 양식을 덧붙였습니다. 자료 정리와 교육용 예제이며 실서비스의 완성이나 안전을 인증하지 않습니다.

## 바로 시작하기

AI에게 저장소 URL과 함께 이렇게 요청하세요.

```text
AGENTS.md와 docs/START_HERE.md를 읽고 내 요구사항을 분류해라.
metadata/topics.json에서 관련 주제만 선택하고 docs/design의 대응 지침을 읽어라.
templates/APP_SPEC.md를 채우되 모르는 것은 미확정으로 표시해라.
출처 기반 원칙, 이번 앱의 설계 선택, 실제 검증 결과를 구별하고
도구 계약, 상태 전이, 권한, 예산, 실패 처리, 평가 사례를 포함해라.
구현 전에 빠진 결정과 최소 구현 범위를 제시해라.
```

1. [AI와 사람의 읽기 순서](docs/START_HERE.md)
2. [작업별 문서 선택](docs/ROUTES.md)
3. [요구사항과 에이전트 선택](docs/design/01-requirements.md)
4. [앱 아키텍처](docs/design/02-architecture.md)
5. [하네스와 상태 제어](docs/design/03-harness.md)
6. [MCP 연결과 버전](docs/design/04-mcp.md)
7. [데이터와 컨텍스트](docs/design/05-data-context.md)
8. [권한, 승인, 보안](docs/design/06-security.md)
9. [평가와 검증](docs/design/07-evaluation.md)
10. [배포와 해커톤 실행](docs/design/08-delivery.md)
11. [GPU 가격 비교 앱 적용 예시](docs/design/09-worked-example.md)
12. [복사해 쓸 설계/추출/검증 프롬프트](docs/PROMPTS.md)

오프라인 통합 열람: [guide.html](guide.html). `python scripts/search_topics.py MCP`처럼 로컬에서 주제를 찾을 수도 있습니다. 검증/HTML 생성 명령은 [검증 기록](docs/VERIFICATION.md)에 있습니다.

## 자료를 찾는 세 가지 방법

- 개념부터: [전체 개념 색인](docs/CONCEPTS.md). Agentic AI 37개, AI Agent 59개 주제를 안정적인 ID로 찾습니다.
- 설계부터: [설계 양식](templates/APP_SPEC.md), [도구 양식](templates/TOOL_SPEC.md), [평가 양식](templates/EVAL_PLAN.md)을 채웁니다.
- 근거부터: [출처 정책](SOURCE_POLICY.md), [쪽별 반영표](metadata/page-coverage.csv), [주제 색인](metadata/topics.json)을 봅니다. 자동 대응은 수동 대조와 다릅니다.

## 저장소 구성

```text
AGENTS.md, llms.txt          AI용 진입점
docs/concepts/              96개 원문 주제의 재서술
docs/design/                AI 보완 설계 지침
templates/                  요구사항, 도구, 평가, 인계 양식
contracts/                  JSON Schema와 예시
examples/harness/           외부 API 없이 실행하는 제어 예제
metadata/                   주제, 출처, PDF 쪽별 대응 정보
scripts/                    색인과 로컬 링크 검사
docs/VERIFICATION.md        실제 검사 범위와 한계
```

## 공개와 재사용 범위

원문 PDF, OCR 전문, 보관 HTML은 배포하지 않습니다. 강의 내용을 재서술한 문서와 AI가 보완한 설계를 구분합니다. 원문 저작물 전체에 대한 재배포 권한이나 라이선스를 주장하지 않습니다. 출처와 재사용 범위는 [SOURCE_POLICY.md](SOURCE_POLICY.md)를 확인하세요. 연결할 SDK와 MCP 사양은 배포 환경에서 다시 고정해야 합니다.
