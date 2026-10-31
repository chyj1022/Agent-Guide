"""네트워크와 파일 쓰기 없는 교육용 실행 제어 예제. Python 3.10+."""
from dataclasses import dataclass
from enum import Enum
import json


class Status(str, Enum):
    OK = "ok"
    MISSING_DATA = "missing_data"
    DENIED = "denied"
    APPROVAL_REQUIRED = "approval_required"
    CONFLICT = "conflict"
    INVALID_ACTION = "invalid_action"
    ERROR = "error"
    LIMIT_REACHED = "limit_reached"
    COMPLETED = "completed"
    STOPPED = "stopped"


@dataclass(frozen=True)
class Result:
    status: Status
    code: str
    data: str | None = None


class TransientReadError(Exception):
    """읽기 제공자가 일시 오류라고 명시한 경우만 재시도한다."""


class ScriptedModel:
    """고정된 제안을 순서대로 반환한다. 권한 판단은 하네스가 한다."""
    def __init__(self, actions):
        self.actions = iter(actions)

    def next_action(self, observations):
        return next(self.actions, {"type": "stop"})


def canonical(arguments):
    return json.dumps(arguments, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


class Harness:
    def __init__(self, *, user="learner", version="v1", run_id="demo-run", now=lambda: 0,
                 provider=None, max_steps=8, max_tool_calls=8, budget=8,
                 read_attempts=2):
        for value in (max_steps, max_tool_calls, budget):
            if type(value) is not int or value < 0:
                raise ValueError("limits must be nonnegative integers")
        if type(read_attempts) is not int or not 1 <= read_attempts <= 3:
            raise ValueError("read_attempts must be between 1 and 3")
        self.user, self.version, self.now = user, version, now
        if type(run_id) is not str or not 1 <= len(run_id) <= 100:
            raise ValueError("run_id must be a bounded nonempty string")
        self.run_id, self._closed = run_id, False
        self.provider = provider or self._fake_read
        self.max_steps, self.max_tool_calls, self.budget = max_steps, max_tool_calls, budget
        self.read_attempts = read_attempts
        self.tool_calls = self.spent = self.steps = 0
        self.events, self.results, self.drafts = [], [], []
        self._approvals, self._idempotency = {}, {}

    @staticmethod
    def _fake_read(key):
        return {"public": "공개 메모"}.get(key)

    def approve(self, arguments, *, expires_at):
        """신뢰된 사용자 승인 화면의 대역. 모델 도구로 노출하지 않는다.

        토큰은 이 객체 안에서만 의미 있는 조회 키이며 인증용 자격증명이 아니다.
        """
        if (type(arguments) is not dict or set(arguments) != {"text"}
                or type(arguments["text"]) is not str
                or not 1 <= len(arguments["text"]) <= 200):
            raise ValueError("invalid draft")
        token = f"approval-{len(self._approvals) + 1}"
        self._approvals[token] = (self.user, self.version, self.run_id, "save_draft",
                                  canonical(arguments), expires_at)
        return token

    def _record(self, result, tool="none"):
        # 고정 필드와 허용된 이름만 기록한다. 인자/본문/토큰/예외문구는 기록하지 않는다.
        self.events.append({"event": "action_result", "step": self.steps,
                            "tool": tool, "status": result.status.value,
                            "code": result.code, "tool_calls": self.tool_calls,
                            "budget_spent": self.spent})
        self.results.append(result)
        return result

    def _charge(self):
        if self.tool_calls >= self.max_tool_calls or self.spent >= self.budget:
            return False
        self.tool_calls += 1
        self.spent += 1
        return True

    def execute(self, action):
        """모든 제안은 실행 직전에 닫힌 스키마와 정책을 통과해야 한다."""
        if self._closed:
            return self._record(Result(Status.DENIED, "run_closed"))
        invalid = Result(Status.INVALID_ACTION, "invalid_schema")
        if type(action) is not dict:
            return self._record(invalid)
        kind = action.get("type")
        if kind in ("finish", "stop") and set(action) == {"type"}:
            status = Status.COMPLETED if kind == "finish" else Status.STOPPED
            return self._record(Result(status, kind))
        if kind != "tool":
            return self._record(invalid)
        name, args = action.get("name"), action.get("arguments")
        if type(name) is not str or name not in ("read_note", "save_draft"):
            return self._record(invalid)
        expected = {"type", "name", "arguments"}
        if name == "save_draft":
            expected |= {"idempotency_key", "approval"}
        field = "key" if name == "read_note" else "text"
        if (set(action) != expected or type(args) is not dict
                or set(args) != {field} or type(args[field]) is not str
                or not 1 <= len(args[field]) <= 200):
            return self._record(invalid, name)
        if name == "save_draft" and any(
            type(action[k]) is not str or len(action[k]) > 100
            for k in ("idempotency_key", "approval")
        ):
            return self._record(invalid, name)
        if name == "save_draft" and not action["idempotency_key"]:
            return self._record(invalid, name)
        if name == "read_note":
            return self._read(args["key"])
        return self._write(action)

    def _read(self, key):
        name = "read_note"
        if key not in ("public", "missing"):
            return self._record(Result(Status.DENIED, "resource_not_allowed"), name)
        for attempt in range(self.read_attempts):
            if not self._charge():
                return self._record(Result(Status.LIMIT_REACHED, "tool_or_budget_limit"), name)
            try:
                value = self.provider(key)
                if value is None:
                    result = Result(Status.MISSING_DATA, "not_found")
                elif type(value) is str and len(value) <= 1000:
                    result = Result(Status.OK, "read", value)
                else:
                    result = Result(Status.ERROR, "invalid_provider_result")
                return self._record(result, name)
            except TransientReadError:
                if attempt + 1 == self.read_attempts:
                    return self._record(Result(Status.ERROR, "read_retry_exhausted"), name)
            except Exception:
                return self._record(Result(Status.ERROR, "read_failed"), name)

    def _write(self, action):
        name, args = "save_draft", action["arguments"]
        payload = canonical(args)
        approval = self._approvals.get(action["approval"])
        if (approval is None or approval[:5] != (self.user, self.version, self.run_id, name, payload)
                or self.now() >= approval[5]):
            return self._record(Result(Status.APPROVAL_REQUIRED, "approval_not_current"), name)
        scope = (self.user, self.version, self.run_id, name, action["idempotency_key"])
        prior = self._idempotency.get(scope)
        if prior:
            if prior[0] != payload:
                return self._record(Result(Status.CONFLICT, "idempotency_payload_conflict"), name)
            return self._record(prior[1], name)
        if not self._charge():
            return self._record(Result(Status.LIMIT_REACHED, "tool_or_budget_limit"), name)
        # 단일 프로세스·단일 스레드에서 메모리 목록에 넣는 쓰기 대역이다.
        self.drafts.append(args["text"])
        result = Result(Status.OK, "draft_saved", f"draft-{len(self.drafts)}")
        self._idempotency[scope] = (payload, result)
        return self._record(result, name)

    def run(self, model):
        if self._closed:
            return self._record(Result(Status.DENIED, "run_closed"))
        try:
            return self._run(model)
        finally:
            # 객체 하나가 논리 실행 하나다. 새 실행은 새 객체와 새 승인이 필요하다.
            self._closed = True

    def _run(self, model):
        while self.steps < self.max_steps:
            self.steps += 1
            try:
                action = model.next_action(tuple(self.results))
            except Exception:
                return self._record(Result(Status.ERROR, "model_failed"))
            result = self.execute(action)
            # 누락된 읽기만 다음 관찰로 넘긴다. 권한/계약/실행 오류는 중단한다.
            if result.status not in (Status.OK, Status.MISSING_DATA):
                return result
        return self._record(Result(Status.LIMIT_REACHED, "step_limit"))


if __name__ == "__main__":
    harness = Harness()
    approval = harness.approve({"text": "검토용 초안"}, expires_at=60)
    model = ScriptedModel([
        {"type": "tool", "name": "read_note", "arguments": {"key": "public"}},
        {"type": "tool", "name": "save_draft", "arguments": {"text": "검토용 초안"},
         "idempotency_key": "example-1", "approval": approval},
        {"type": "finish"},
    ])
    harness.run(model)
    for event in harness.events:
        print(json.dumps(event, ensure_ascii=False))
