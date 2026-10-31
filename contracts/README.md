# 애플리케이션 계약 예시

이 폴더는 AI가 보완한 앱 수준의 JSON Schema입니다. MCP wire protocol이나 특정 SDK의 공식 스키마가 아닙니다. 실제 앱에 적용할 필드와 상태를 논의하기 위한 예제입니다. `examples/harness`는 별도의 작은 교육용 Python 타입을 사용하며 이 스키마 전체를 구현하지 않습니다.

- `tool-request.schema.json`: 실행 후보 요청. 모델 제안만으로 신원과 권한이 확정되지 않습니다. user_id/run_id는 신뢰된 서버가 주입합니다.
- `tool-result.schema.json`: 결과 코드와 출처. 빈 결과와 실패를 구분합니다.
- `approval.schema.json`: 서버가 저장할 승인 기록. 이 구조만으로 위조 방지가 되지 않습니다. 저장소 접근 통제와 검증이 필요합니다.
- `run-state.schema.json`: 실행 상태와 한도. 실제 비용 예약/정산은 별도 실행 코드가 보장해야 합니다.
- `examples.json`: 각 스키마를 만족하는 가상 데이터.

JSON Schema는 타입과 구조를 검사합니다. 승인 만료, 사용자 권한, 결과의 사실성, 버전 충돌, 외부 부작용의 중복은 별도 코드와 테스트가 필요합니다.

검사: `python -m unittest discover -s scripts -p "test_*.py" -v`. 이 명령에는 `jsonschema`가 필요하며 설치 방법은 [검증 기록](../docs/VERIFICATION.md)을 확인합니다.
