# 검증 기록과 남은 범위

검증일: 2026-10-31. 문서 작성, 원자료 판독과 코드 실행을 구분합니다.

실행 환경: Python 3.13.9, jsonschema 4.25.1, Markdown 3.10. 하네스 12개, 계약 4개 테스트가 통과했습니다. 구조 검사에서 96개 주제, 178개 쪽 항목과 로컬 링크가 통과했습니다. HTML은 파싱 후 문서/링크 구조를 검사했으며 브라우저에서 모든 상호작용을 수동 확인하지 않았습니다.

## 재현 명령

Python 3.11 이상을 사용하세요. 하네스는 표준 라이브러리만 사용합니다. 계약 검사와 HTML 생성에는 추가 패키지가 필요합니다.

```text
python -m pip install -r requirements-checks.txt
python -B scripts/build_index.py
python -B scripts/validate.py
python -B -m unittest discover -s examples/harness -v
python -B -m unittest discover -s scripts -p "test_*.py" -v
python -B examples/harness/harness.py
python -B scripts/search_topics.py MCP
python -B scripts/build_html.py
```

## 확인한 것

- 두 이미지 PDF 53쪽과 125쪽을 렌더링하고 kor+eng OCR 추출했습니다. 추출 프로세스 오류는 없었습니다. OCR 문자 정확도를 측정한 것은 아닙니다.
- 보관 HTML의 37개와 59개 섹션 본문을 읽고 대응 개념 문서를 작성했습니다. 각 섹션 앵커, 고유 ID와 본문 경로를 검사합니다.
- PDF 중 SRC-01의 1/25쪽, SRC-02의 1/73쪽만 제한적으로 시각 대조했습니다. 나머지는 자동 OCR 대응 후보입니다.
- 오프라인 하네스 12개 테스트, 앱 계약 4개 테스트를 실행했습니다. 승인 실행 ID 누락을 검토에서 발견해 수정하고 회귀 테스트를 추가했습니다.
- 하네스 명세 검토 후 별도 코드 품질 검토를 수행했습니다. 실제 모델과 MCP 서버 연결은 범위 밖입니다.

구조 검사는 JSON 문법, 96개 ID, 178쪽의 연속성, 로컬 링크, 기초적인 로컬 경로와 비공개 파일 혼입을 검사합니다. 기초 문자열 검사가 모든 비밀정보 유출 가능성을 증명하는 것은 아닙니다.

## 확인하지 않은 것

178쪽 모든 문장/코드/그림의 수동 대조, 원문 실습 C-01~C-10 전체 재실행, 실제 모델의 정확도/비용/지연, MCP Host/Client/Server의 상호운용, 운영 인증, DB 동시성, 분산 환경의 중복 효과 방지와 법률 적합성을 확인하지 않았습니다. 교육용 코드의 메모리 상태는 프로세스 재시작 뒤 유지되지 않습니다.

이 저장소는 설계의 출발점입니다. 실제 앱은 선택한 SDK/사양 버전, 데이터, 권한과 위험을 반영해 계약 테스트 및 시나리오 평가를 추가해야 합니다.
