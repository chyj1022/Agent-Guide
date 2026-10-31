# Agent design guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Execute tasks without intermediate permission requests.

**Goal:** 두 PDF의 개념을 AI가 앱 설계에 재사용할 수 있는 출처 연결 가이드로 만든다.

**Architecture:** 원문 96주제를 독립 개념 문서에 재서술하고 설계 가이드가 이를 연결한다. 진입점, 기계 판독 색인, 쪽별 대응표, 테스트를 별도 계층으로 둔다.

**Tech Stack:** Markdown, JSON, Python standard library, local HTML download view. PDF OCR and HTML parsing are private research steps.

### Task 1: 원문 개념 재서술
- [x] 보관 HTML 두 개의 본문을 전부 읽고 PDF OCR과 비교한다.
- [x] `docs/concepts/agentic/` 37주제와 `docs/concepts/agent/` 59주제를 목적, 작동, 적용, 한계, 복습 질문으로 작성한다.
- [x] `metadata/agentic-topics.json`, `metadata/agent-topics.json`에 ID, 출처 앵커, 문서 경로를 기록한다.
- [x] 명세 검토와 품질 검토에서 누락, 과도한 복사, 단정, 버전 문제를 확인한다.

### Task 2: 설계 적용 계층
- [x] `docs/design/`에 요구사항, 구조, MCP, 하네스, 데이터, 안전, 평가, 배포 가이드를 쓴다.
- [x] `templates/`와 `contracts/`에 채워 쓰는 설계 양식 및 JSON 계약 예제를 쓴다.
- [x] `examples/`에 외부 모델 없이 작동하는 제한된 실행 제어 예제를 쓰고 위험 경계를 테스트한다.

### Task 3: 출처와 AI 진입점
- [x] `README.md`, `AGENTS.md`, `llms.txt`, `metadata/topics.json`, 작업별 경로를 연결한다.
- [x] 178쪽 OCR에 대응 주제와 자동 추정/수동 확인 범위를 기록한다.
- [x] `SOURCE_POLICY.md`에 원문 재배포 및 보조 자료 판독 한계를 밝힌다.

### Task 4: 검증과 전달
- [x] 코드 테스트, JSON 파싱, 전체 주제/쪽 수, 로컬 링크, 비공개 경로 및 민감 원문 혼입을 검사한다.
- [x] 명세 검토 후 별도 품질 검토를 실시하고 발견된 문제를 수정한다.
- [x] 실행 명령과 실제 결과를 기록하고 오프라인 열람 HTML 및 ZIP을 만든다.
- [x] 최종 경로와 미검증 사항을 사용자에게 전달한다. 공개 업로드는 완성본 검토 뒤 진행한다.
