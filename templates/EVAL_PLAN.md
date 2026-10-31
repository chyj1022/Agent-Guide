# 평가 계획 양식

AI 보완 양식입니다. 값이나 임계값은 실제 위험과 요구사항을 근거로 정하세요.

```text
case_id=,requirement_id=,category=
input_fixture=,fixture_version=,expected_scope=
expected_result=,required_evidence=
required_actions=,forbidden_actions=
max_calls=,max_cost=,max_latency=
expected_terminal_status=,oracle=
actual_result=,trace_ref=,pass_or_fail=,failure_reason=
```

검증 계층은 도구 단위, 워크플로 궤적, 사용자 결과로 나눕니다. 정답을 확인하는 oracle은 모델의 자기평가만 사용하지 않습니다. 결정적 계산기, 원문 위치 대조, 전문가 확인 등 무엇을 썼는지 씁니다. 개인정보와 비밀값이 든 실제 입력 대신 허용된 가상/비식별 fixture를 저장합니다.

정상뿐 아니라 미첨부, 범례/빈칸, 상충 출처, 단위 불일치, 권한 거부, 악성 지시, 승인 변경, 중복, 재시작, 예산 소진을 포함합니다. 실패가 하나라도 있을 때 평균값만 보고 치명적 경계를 덮지 않습니다.
