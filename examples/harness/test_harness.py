"""교육용 하네스의 실행 경계를 검증한다."""
import unittest

from harness import Harness, ScriptedModel, Status, TransientReadError


def read(key="public"):
    return {"type": "tool", "name": "read_note", "arguments": {"key": key}}


def write(text="검토 초안", key="job-1", approval=""):
    return {"type": "tool", "name": "save_draft", "arguments": {"text": text},
            "idempotency_key": key, "approval": approval}


class HarnessTests(unittest.TestCase):
    def test_approval_is_bound_to_run_identity(self):
        h = Harness()
        token = h.approve({"text": "검토 초안"}, expires_at=100)
        h.run_id = "different-run"
        self.assertEqual(h.execute(write(approval=token)).status, Status.APPROVAL_REQUIRED)
        self.assertEqual(h.drafts, [])

    def test_finished_run_cannot_reuse_approval_or_execute(self):
        h = Harness()
        token = h.approve({"text": "검토 초안"}, expires_at=100)
        h.run(ScriptedModel([{"type": "finish"}]))
        self.assertEqual(h.run(ScriptedModel([write(approval=token)])).status, Status.DENIED)
        self.assertEqual(h.execute(write(approval=token)).status, Status.DENIED)
        self.assertEqual(h.drafts, [])

    def test_normal_completion_and_stop(self):
        h = Harness()
        r = h.run(ScriptedModel([read(), {"type": "finish"}]))
        self.assertEqual(r.status, Status.COMPLETED)
        self.assertEqual(h.results[0].data, "공개 메모")
        self.assertEqual(Harness().run(ScriptedModel([{"type": "stop"}])).status,
                         Status.STOPPED)

    def test_denied_and_unapproved_have_no_effect(self):
        h = Harness()
        self.assertEqual(h.execute(read("private")).status, Status.DENIED)
        self.assertEqual(h.execute(write()).status, Status.APPROVAL_REQUIRED)
        self.assertEqual(h.drafts, [])
        self.assertEqual(h.tool_calls, 0)

    def test_missing_is_distinct_from_denial_and_error(self):
        h = Harness()
        self.assertEqual(h.execute(read("missing")).status, Status.MISSING_DATA)
        h.provider = lambda key: (_ for _ in ()).throw(RuntimeError("secret"))
        self.assertEqual(h.execute(read()).status, Status.ERROR)
        self.assertNotIn("secret", str(h.events))

    def test_approval_binding_and_expiry(self):
        for change in ("arguments", "user", "version", "expiry"):
            with self.subTest(change=change):
                h = Harness(now=lambda: 10)
                token = h.approve({"text": "검토 초안"}, expires_at=20)
                a = write(approval=token)
                if change == "arguments":
                    a["arguments"]["text"] = "바뀐 초안"
                elif change == "user":
                    h.user = "other"
                elif change == "version":
                    h.version = "v2"
                else:
                    h.now = lambda: 20
                self.assertEqual(h.execute(a).status, Status.APPROVAL_REQUIRED)
                self.assertEqual(h.drafts, [])

    def test_idempotency_duplicate_conflict_and_scope(self):
        h = Harness()
        token = h.approve({"text": "검토 초안"}, expires_at=100)
        a = write(approval=token)
        first = h.execute(a)
        self.assertEqual(h.execute(a), first)
        self.assertEqual(len(h.drafts), 1)
        token2 = h.approve({"text": "다름"}, expires_at=100)
        self.assertEqual(h.execute(write("다름", approval=token2)).status, Status.CONFLICT)
        h.user = "other"
        token3 = h.approve({"text": "검토 초안"}, expires_at=100)
        self.assertEqual(h.execute(write(approval=token3)).status, Status.OK)
        self.assertEqual(len(h.drafts), 2)

    def test_limits(self):
        self.assertEqual(Harness(max_steps=1).run(ScriptedModel([read(), read()])).status,
                         Status.LIMIT_REACHED)
        for kwargs in ({"budget": 0}, {"max_tool_calls": 0}):
            h = Harness(**kwargs)
            self.assertEqual(h.execute(read()).status, Status.LIMIT_REACHED)
            self.assertEqual(h.tool_calls, 0)

    def test_malformed_and_unknown_actions(self):
        for action in (None, [], {}, {"type": "launch"},
                       {"type": "finish", "extra": True},
                       {"type": "tool", "name": "shell", "arguments": {}},
                       {"type": "tool", "name": "read_note", "arguments": []},
                       read(123), write(key="")):
            with self.subTest(action=action):
                self.assertEqual(Harness().execute(action).status, Status.INVALID_ACTION)

    def test_retry_ceiling_and_each_attempt_cost(self):
        calls = []
        def unavailable(key):
            calls.append(key)
            raise TransientReadError("private details")
        h = Harness(provider=unavailable, read_attempts=2)
        self.assertEqual(h.execute(read()).status, Status.ERROR)
        self.assertEqual((len(calls), h.tool_calls, h.spent), (2, 2, 2))
        h = Harness(provider=unavailable, read_attempts=3, budget=1)
        self.assertEqual(h.execute(read()).status, Status.LIMIT_REACHED)
        self.assertEqual(h.tool_calls, 1)

    def test_only_transient_reads_retry(self):
        calls = []
        def once(key):
            calls.append(key)
            if len(calls) == 1:
                raise TransientReadError()
            return "성공"
        h = Harness(provider=once)
        self.assertEqual(h.execute(read()).data, "성공")
        self.assertEqual(h.tool_calls, 2)

    def test_events_redact_arguments_and_results(self):
        h = Harness()
        token = h.approve({"text": "SECRET-TEXT"}, expires_at=100)
        h.execute(write("SECRET-TEXT", approval=token))
        self.assertNotIn("SECRET-TEXT", str(h.events))
        self.assertNotIn(token, str(h.events))
        self.assertEqual(h.events[-1]["status"], "ok")


if __name__ == "__main__":
    unittest.main()
