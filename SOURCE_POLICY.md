# 출처, 반영 범위와 공개 정책

## 사용자 제공 원문

| ID | 자료 | PDF 쪽 수 | 주제 수 |
| --- | --- | ---: | ---: |
| SRC-01 | agentic ai 공부.pdf | 53 | 37 |
| SRC-02 | Ai agent.pdf | 125 | 59 |

원본은 이미지 기반 PDF입니다. 178쪽을 렌더링하고 한국어/영어 OCR을 수행했습니다. 같은 강의의 보관 HTML 본문을 전체 주제 판독에 활용했습니다. HTML의 표, 코드, 설명과 PDF OCR을 보조적으로 연결했으나 모든 그림과 문자에 대한 수동 대조를 완료했다는 뜻은 아닙니다. 원문 SHA-256과 쪽별 상태는 [출처 메타데이터](metadata/sources.json), [쪽별 반영표](metadata/page-coverage.csv)에서 확인합니다.

개념 문서는 두 강의의 96개 주제를 재서술한 학습 문서입니다. 원문에 나온 예제와 주장을 실제 사용자 성과나 이번 실행 결과로 바꾸지 않습니다. 강의의 코드가 현재 SDK에서 실행된다고 보장하지 않습니다. 설계 적용과 복습 문답은 AI 보완으로 표시합니다. 원문의 모순이나 기술적 단순화는 해당 개념 문서에 설명을 남깁니다.

## 반영표의 의미

쪽별 표의 `auto_candidate`는 OCR과 보관 HTML 구간 간 텍스트 유사도로 고른 후보입니다. 페이지 경계에서 여러 주제가 겹치거나 코드, 그림만 있는 쪽은 대응이 부정확할 수 있습니다. 해당 행의 주제 목록은 확정된 문장별 인용이 아닙니다. `manual_visual`은 직접 확인한 제한된 페이지에만 사용합니다. OCR 오류가 없다는 것은 프로그램이 오류 없이 추출했다는 뜻이며 문자 정확도 100%를 뜻하지 않습니다.

`주제 96개를 문서에 반영`과 `178쪽의 모든 문장을 보존`은 다릅니다. 원문 전문, 코드 전문, 그림 전체의 재배포를 목표로 하지 않습니다. 원문 수준의 정밀한 판독이 필요한 경우 합법적으로 보유한 PDF를 직접 확인해야 합니다.

## 공개 패키지에 넣지 않는 것

원문 PDF, 렌더링 이미지 전체, OCR 전문, 보관 HTML, 개인 노트 전문, 로컬 사용자 경로와 자격 증명을 포함하지 않습니다. 이 저장소의 설명이 원 저작물의 권리를 이전하거나 전체 원문에 오픈소스 라이선스를 부여하지 않습니다. 원문을 추가 공개하려면 별도 이용 조건과 권한을 확인하세요. 별도 명시 없는 제3자 자료에는 포괄적인 MIT 라이선스를 붙이지 않았습니다.

## 공식 문서 보완

2026-10-31 기준 확인한 아래 문서는 강의의 버전 의존 부분을 보완합니다. 실제 구현은 사양/SDK/Host/Server 버전을 각각 고정하고 호환성을 검증해야 합니다.

- [MCP 2026-07-28 architecture](https://modelcontextprotocol.io/specification/2026-07-28/architecture)
- [MCP 2026-07-28 authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [A2A specification](https://a2a-protocol.org/latest/specification/)

위 링크는 원문 강의의 저자 표시를 대신하지 않습니다. 보관 HTML의 ‘사이트 원문’ 링크에서 [Agentic AI 원문 경로](https://tech-learning-hub.pages.dev/courses/agentic-ai/complete-guide.html)와 [AI Agent 원문 경로](https://tech-learning-hub.pages.dev/courses/ai-agent/complete-guide.html)를 확인했습니다. canonical 태그는 없었으며, 현재 온라인 본문과 보관본의 일치는 대조하지 않았습니다. 개념 문서에서는 이 경로와 기존 섹션 앵커를 사용하고, PDF는 파일 ID로 식별합니다. 이 패키지의 모든 구현이 위 프로토콜로 상호운용되는지를 확인한 것은 아닙니다.
