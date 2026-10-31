# 도구 계약 양식

AI 보완 설계 양식입니다. 모델에게 보이는 설명과 실제 실행 검사를 모두 정의합니다.

```text
name=,version=,owner=
purpose=,use_when=,do_not_use_when=
input_schema=,output_schema=
side_effect=read또는write,scope=
auth=,approval_required_when=,approval_binding=
timeout=,deadline=,max_output_size=
retryable_codes=,max_attempts=,backoff=
idempotency_scope=,key=,payload_conflict=
status_codes=ok/empty/denied/invalid/transient_error/permanent_error
provenance_fields=,redaction=,audit_events=
```

서버는 알 수 없는 필드와 도구 이름을 거부하고 인자를 검증합니다. description은 “무엇을 반환하며 언제 쓰지 말아야 하는가”까지 설명합니다. 출력 스키마가 맞아도 값의 진실성은 별도 검증 대상입니다.

필수 계약 사례: 정상, 빈 결과, 인자 경계값, 잘못된 단위, 권한 거부, 지연, 중복 키, 같은 키의 다른 인자, 악성 외부 텍스트, 취소 뒤 상태. 쓰기에는 외부 작업 ID와 복구 시 대사 방법을 추가합니다.
