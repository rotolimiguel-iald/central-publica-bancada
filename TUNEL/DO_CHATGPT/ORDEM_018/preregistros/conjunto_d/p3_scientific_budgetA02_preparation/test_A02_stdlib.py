"""A02-only cooperative supervisor checks: artificial handles and clock.

No Popen, real child, OS signals, scientific imports, or external data.
"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from process_supervision import Cancellation, supervise


class Clock:
    def __init__(self):
        self.t = 0.0
    def __call__(self):
        return self.t


class Process:
    pid = 987654  # Synthetic identifier; never passed to an OS function.
    def __init__(self, clock, events=(), poll_hook=None):
        self.clock = clock
        self.events = list(events)
        self.rc = None
        self.poll_hook = poll_hook
        self.waits = []
        self.polls = 0
    def wait(self, timeout):
        self.waits.append(timeout)
        if self.events:
            event = self.events.pop(0)
            if callable(event):
                return event(self, timeout)
            if isinstance(event, BaseException):
                raise event
            if event != "timeout":
                self.rc = event
                return event
        elif self.rc is not None:
            return self.rc
        self.clock.t += timeout
        raise subprocess.TimeoutExpired("FAKE_ONLY", timeout)
    def poll(self):
        self.polls += 1
        if self.poll_hook is not None:
            return self.poll_hook(self)
        return self.rc


class Checks(unittest.TestCase):
    def fixture(self, events=(), poll_hook=None):
        clock, token = Clock(), Cancellation()
        return clock, token, Process(clock, events, poll_hook)
    def run_case(self, clock, token, proc, *, spawn_hook=None, kill_hook=None,
                 work=1.0, cleanup=2.0):
        self.spawns, self.kills = [], []
        def spawn():
            self.spawns.append("ONCE")
            if spawn_hook:
                spawn_hook()
            return proc
        def kill(pid):
            self.kills.append(pid)
            self.assertEqual(pid, proc.pid)
            if kill_hook:
                kill_hook()
            else:
                proc.rc = -9
        return supervise(spawn, wait_deadline=work, cleanup_deadline=cleanup,
                         clock=clock, kill_owned_group=kill, cancellation=token)
    def cancelled(self, row):
        self.assertFalse(row["process_accepted"])
        self.assertEqual(row["supervisor_status"], "SUPERVISOR_CANCELLED")
        self.assertTrue(row["cancellation_requested"])
    def test_01_normal_exit_zero_no_kill(self):
        clock, token, proc = self.fixture([0])
        row = self.run_case(clock, token, proc)
        self.assertTrue(row["process_accepted"])
        self.assertTrue(row["termination_certain"])
        self.assertEqual(self.kills, [])
        self.assertEqual(len(self.spawns), 1)
    def test_02_wait_slices_then_success(self):
        clock, token, proc = self.fixture(["timeout", "timeout", 0])
        row = self.run_case(clock, token, proc)
        self.assertTrue(row["process_accepted"])
        self.assertEqual(clock.t, 0.5)
        self.assertTrue(all(0 < x <= 0.25 for x in proc.waits))
    def test_03_nonzero_never_accepted(self):
        clock, token, proc = self.fixture([7])
        row = self.run_case(clock, token, proc)
        self.assertFalse(row["process_accepted"])
        self.assertTrue(row["termination_certain"])
        self.assertEqual(self.kills, [])
    def test_04_cancel_before_spawn(self):
        clock, token, proc = self.fixture()
        token.request(15)
        row = self.run_case(clock, token, proc)
        self.cancelled(row)
        self.assertTrue(row["no_child_started"])
        self.assertEqual(self.spawns, [])
        self.assertEqual(self.kills, [])
    def test_05_cancel_during_spawn_retains_handle(self):
        clock, token, proc = self.fixture()
        row = self.run_case(clock, token, proc, spawn_hook=lambda: token.request(15))
        self.cancelled(row)
        self.assertTrue(row["termination_certain"])
        self.assertEqual(self.kills, [proc.pid])
        self.assertEqual(len(self.spawns), 1)
    def test_06_cancel_during_wait_reaped(self):
        clock, token, proc = self.fixture()
        def event(p, timeout):
            token.request(2)
            p.clock.t += timeout
            raise subprocess.TimeoutExpired("FAKE", timeout)
        proc.events = [event]
        row = self.run_case(clock, token, proc)
        self.cancelled(row)
        self.assertEqual(self.kills, [proc.pid])
        self.assertTrue(row["termination_certain"])
        self.assertEqual(clock.t, 0.25)
    def test_07_cancel_at_cleanup_entry_does_not_escape(self):
        clock, token, proc = self.fixture()
        def poll(p):
            token.request(15)
            return p.rc
        proc.poll_hook = poll
        row = self.run_case(clock, token, proc)
        self.cancelled(row)
        self.assertEqual(self.kills, [proc.pid])
        self.assertTrue(row["termination_certain"])
    def test_08_cancel_during_kill_still_reaps(self):
        clock, token, proc = self.fixture()
        def kill():
            token.request(15)
            proc.rc = -9
        row = self.run_case(clock, token, proc, kill_hook=kill)
        self.cancelled(row)
        self.assertTrue(row["termination_certain"])
        self.assertEqual(self.kills, [proc.pid])
    def test_09_cancel_during_reap_zero_is_not_success(self):
        clock, token, proc = self.fixture()
        def reap(p, timeout):
            token.request(2)
            p.rc = 0
            return 0
        proc.events = [RuntimeError("WAIT_FAKE"), reap]
        row = self.run_case(clock, token, proc)
        self.cancelled(row)
        self.assertTrue(row["termination_certain"])
        self.assertEqual(row["returncode"], 0)
    def test_10_work_timeout_kill_reap_no_retry(self):
        clock, token, proc = self.fixture()
        row = self.run_case(clock, token, proc)
        self.assertEqual(row["supervisor_status"], "SUPERVISOR_TIMEOUT")
        self.assertFalse(row["process_accepted"])
        self.assertTrue(row["termination_certain"])
        self.assertEqual(clock.t, 1.0)
        self.assertEqual(len(self.spawns), 1)
        self.assertEqual(self.kills, [proc.pid])
    def test_11_spawn_error_without_handle_is_uncertain(self):
        clock, token, proc = self.fixture()
        def fail():
            raise OSError("FAKE_SPAWN")
        row = self.run_case(clock, token, proc, spawn_hook=fail)
        self.assertFalse(row["process_accepted"])
        self.assertTrue(row["spawn_result_uncertain"])
        self.assertFalse(row["termination_certain"])
        self.assertEqual(self.kills, [])
        self.assertEqual(len(self.spawns), 1)
    def test_12_unexpected_wait_error_still_cleans(self):
        clock, token, proc = self.fixture([RuntimeError("FAKE")])
        row = self.run_case(clock, token, proc)
        self.assertFalse(row["process_accepted"])
        self.assertEqual(self.kills, [proc.pid])
        self.assertTrue(row["termination_certain"])
    def test_13_keyboardinterrupt_double_still_cleans(self):
        clock, token, proc = self.fixture([KeyboardInterrupt("FAKE_NOT_SIGNAL")])
        row = self.run_case(clock, token, proc)
        self.assertFalse(row["process_accepted"])
        self.assertTrue(row["termination_certain"])
        self.assertEqual(self.kills, [proc.pid])
    def test_14_already_exited_after_timeout_never_killed(self):
        clock, token, proc = self.fixture()
        def poll(p):
            p.rc = 0
            return 0
        proc.poll_hook = poll
        row = self.run_case(clock, token, proc)
        self.assertFalse(row["process_accepted"])
        self.assertTrue(row["termination_certain"])
        self.assertEqual(self.kills, [])
    def test_15_kill_failure_and_live_child_are_uncertain(self):
        clock, token, proc = self.fixture()
        def kill():
            raise OSError("FAKE_KILL")
        row = self.run_case(clock, token, proc, kill_hook=kill)
        self.assertFalse(row["process_accepted"])
        self.assertFalse(row["termination_certain"])
        self.assertFalse(row["within_cleanup_deadline"])
        self.assertEqual(clock.t, 2.0)
        self.assertEqual(len(self.kills), 1)
    def test_16_reap_failure_never_infers_termination_from_kill(self):
        clock, token, proc = self.fixture([RuntimeError("WAIT"), OSError("REAP")])
        row = self.run_case(clock, token, proc)
        self.assertFalse(row["process_accepted"])
        self.assertFalse(row["termination_certain"])
        self.assertEqual(self.kills, [proc.pid])
    def test_17_no_cleanup_budget_refuses_late_zero(self):
        clock, token, proc = self.fixture()
        row = self.run_case(clock, token, proc, work=1.0, cleanup=1.0)
        self.assertFalse(row["process_accepted"])
        self.assertFalse(row["within_cleanup_deadline"])
        self.assertEqual(clock.t, 1.0)
        self.assertIn("CLEANUP_DEADLINE_EXHAUSTED", row["supervision_errors"])
    def test_18_blocking_wait_late_return_is_rejected(self):
        clock, token, proc = self.fixture()
        def late(p, timeout):
            p.clock.t = 3.0
            p.rc = 0
            return 0
        proc.events = [late]
        row = self.run_case(clock, token, proc)
        self.assertFalse(row["process_accepted"])
        self.assertFalse(row["within_cleanup_deadline"])
        self.assertTrue(row["termination_certain"])
    def test_19_poll_error_no_blind_signal(self):
        clock, token, proc = self.fixture([0])
        def poll(p):
            raise OSError("POLL_FAKE")
        proc.poll_hook = poll
        row = self.run_case(clock, token, proc)
        self.assertFalse(row["process_accepted"])
        self.assertEqual(self.kills, [])
        self.assertTrue(row["termination_certain"])
    def test_20_repeated_requests_do_not_raise_or_clear(self):
        token = Cancellation()
        token.request(2)
        token.request(15)
        self.assertTrue(token.requested)
        self.assertEqual(token.signal_number, 15)
    def test_21_deadline_before_spawn_never_launches(self):
        clock, token, proc = self.fixture()
        row = self.run_case(clock, token, proc, work=0.0)
        self.assertFalse(row["process_accepted"])
        self.assertTrue(row["no_child_started"])
        self.assertEqual(self.spawns, [])
    def test_22_launcher_handler_records_only_no_mask_mutation(self):
        # AST only: do not import/execute launcher/admission/scientific source.
        tree = ast.parse((ROOT / "launch_p3.py").read_text())
        handlers = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
                    and n.name == "interrupted"]
        self.assertEqual(len(handlers), 1)
        body = handlers[0].body
        self.assertEqual(len(body), 1)
        self.assertEqual(ast.unparse(body[0]), "cancellation.request(sig)")
        mask_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                      and ast.unparse(n.func) == "signal.pthread_sigmask"]
        self.assertEqual(len(mask_calls), 1)
        self.assertEqual(ast.unparse(mask_calls[0]),
                         "signal.pthread_sigmask(signal.SIG_BLOCK, set())")
        text = (ROOT / "launch_p3.py").read_text()
        self.assertNotIn("SIG_IGN", text)
        self.assertNotIn("cleanup_context", text)
        self.assertNotIn("ownership_context", text)
        self.assertIn("return 2 if cancellation.requested else exit_code", text)
        final_guard = "if exit_code == 0 and time.perf_counter() >= campaign_deadline:"
        self.assertIn(final_guard, text)
        self.assertLess(text.rindex("signal.signal(s, handler)"), text.index(final_guard))
        self.assertLess(text.index(final_guard),
                        text.index("return 2 if cancellation.requested else exit_code"))


if __name__ == "__main__":
    started, cpu = time.perf_counter(), time.process_time()
    protocol = json.loads((ROOT / "PROTOCOLO_TESTES_A02_V2.json").read_bytes())
    for row in protocol["pins"]:
        raw = (ROOT / row["relative_path"]).read_bytes()
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise RuntimeError("Frozen A02 test input differs")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Checks)
    if suite.countTestCases() != protocol["exact_test_count"]:
        raise RuntimeError("Exact test count differs")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({"status": "PASS" if result.wasSuccessful() else "FAIL",
                      "tests": result.testsRun, "failures": len(result.failures),
                      "errors": len(result.errors), "wall_s": time.perf_counter()-started,
                      "cpu_s": time.process_time()-cpu,
                      "scope": "ARTIFICIAL_STDLIB_DOUBLES_AND_AST_ONLY",
                      "real_children": 0, "real_signals": 0, "scientific_calls": 0}))
    sys.exit(0 if result.wasSuccessful() else 1)
