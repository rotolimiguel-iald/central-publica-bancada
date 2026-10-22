"""Prepared pure doubles. Not executed in this preparation unit."""
from pathlib import Path
import copy
import hashlib
import json
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "candidate"))
from audit_guard import AuditLatch, AuditViolation
from result_acceptance import assess, campaign_exit

class Doubles(unittest.TestCase):
    def latch(self, writer=None):
        rows=[]
        g=AuditLatch(writer if writer is not None else rows.append)
        g.installed()
        return g,rows

    def swallowed(self, g, target="/denied/cache.pyc"):
        try:
            g.deny("open",target,mode="r",flags=0,reason="Exact allowlist")
        except PermissionError:
            pass

    def clean_result(self):
        g,_=self.latch()
        for phase in ("initialization_ready","pre_likelihood","pre_likelihood_evaluation",
                      "post_likelihood","source_after_imports","source_before_temporal",
                      "source_before_dictionary","source_before_waveform","source_after_waveform",
                      "final_before_diagnostics","final_before_result"):
            g.checkpoint(phase)
        failures={k:0 for k in ("source_returned_none_count","source_returned_none_counter_raw",
                    "recognized_domain_exception_count","indeterminate_exception_after_native_attempt_count",
                    "pre_native_exception_count","temporal_guard_count","application_exception_count")}
        failures.update(events=[],domain_error_total=None,budget_abort_count=0)
        return dict(job_id="DOUBLE_JOB",label="DOUBLE_LABEL",contract_sha256="DOUBLE_PIN",pid=123,
                    status="STOPPED_NOT_CONVERGED",likelihood_calls=1,native_calls=1,
                    blocked_operations=[],initialization_qualified=True,
                    initialization_analytic_before_likelihood=[{"name":"H1"},{"name":"L1"}],
                    initialization_analytic_after_likelihood=[{"name":"H1"},{"name":"L1"}],
                    D_read=False,coverage_estimated=False,independent_noise_realizations=False,
                    audit_latch=g.snapshot(),audit_journal_sha256=hashlib.sha256(b"").hexdigest(),
                    failure_receipt=failures)

    def assess(self, result, journal=b"", rc=0, state="PROCESS_RETURNED"):
        return assess(result,journal,returncode=rc,process_state=state,expected_job="DOUBLE_JOB",
                      expected_label="DOUBLE_LABEL",expected_contract="DOUBLE_PIN",
                      expected_pid=123,max_calls=10000)

    def test_pre_ll_swallowed_block_prevents_call(self):
        g,rows=self.latch();self.swallowed(g);calls=[]
        with self.assertRaises(AuditViolation):
            g.evaluate(lambda:calls.append("called"))
        self.assertEqual(calls,[]);self.assertEqual(len(rows),1)

    def test_post_ll_swallowed_block_discards_return(self):
        g,_=self.latch()
        def fake():
            self.swallowed(g)
            return 42.0
        with self.assertRaises(AuditViolation):
            g.evaluate(fake)
        self.assertEqual(g.snapshot()["checkpoint_counts"]["post_likelihood"],1)

    def test_import_probe_checkpoint_prevents_native_double(self):
        g,_=self.latch();called=[]
        self.swallowed(g)
        with self.assertRaises(AuditViolation):
            g.checkpoint("source_after_imports")
            called.append("native double")
        self.assertEqual(called,[])

    def test_finalization_fails_even_after_finite_value(self):
        g,_=self.latch()
        self.assertEqual(g.evaluate(lambda:42.0),42.0)
        self.swallowed(g)
        with self.assertRaises(AuditViolation):
            g.checkpoint("final_before_result")

    def test_first_event_and_all_acts_are_retained(self):
        g,rows=self.latch();g.context("source_after_imports",7,6)
        self.swallowed(g,"first");self.swallowed(g,"second")
        a=g.snapshot()
        self.assertEqual(a["denial_count"],2)
        self.assertEqual(a["first_event"]["target"],"first")
        self.assertEqual([e["sequence"] for e in a["events"]],[1,2])
        self.assertEqual(a["first_event"]["likelihood_calls_at_event"],7)
        self.assertEqual(a["first_event"]["native_attempts_completed_at_event"],6)
        self.assertEqual([json.loads(x)["target"] for x in rows],["first","second"])
        a["first_event"]["target"]="changed"
        self.assertEqual(g.snapshot()["first_event"]["target"],"first")

    def test_journal_io_failure_still_latches(self):
        def fail(_):raise OSError("double IO failure")
        g,_=self.latch(fail)
        with self.assertRaises(OSError):
            g.deny("open","outside",reason="denied")
        self.assertTrue(g.snapshot()["latched"])
        self.assertEqual(g.snapshot()["first_event"]["target"],"outside")
        self.assertIsNotNone(g.snapshot()["journal_error"])
        with self.assertRaises(AuditViolation):
            g.checkpoint("final_before_result")

    def test_exception_only_is_not_infallible(self):
        caught=[]
        try:
            raise SystemExit("double swallowed exit")
        except BaseException:
            caught.append(True)
        self.assertEqual(caught,[True])
        g,_=self.latch();self.swallowed(g)
        try:
            g.checkpoint("caught_checkpoint")
        except BaseException:
            pass
        with self.assertRaises(AuditViolation):
            g.checkpoint("next_checkpoint")

    def test_original_exception_record_survives_audit_priority(self):
        g,_=self.latch()
        def fake():
            self.swallowed(g)
            raise ValueError("original double")
        with self.assertRaises(AuditViolation):
            g.evaluate(fake)
        self.assertEqual(g.snapshot()["interrupted_exceptions"][0]["type"],"ValueError")

    def test_clean_exception_is_rethrown(self):
        g,_=self.latch()
        def fake():raise ValueError("original")
        with self.assertRaisesRegex(ValueError,"original"):
            g.evaluate(fake)
        self.assertFalse(g.snapshot()["latched"])

    def test_partial_clean_is_accepted_without_convergence_claim(self):
        a=self.assess(self.clean_result())
        self.assertTrue(a["accepted"]);self.assertEqual(a["disposition"],"CLEAN_PARTIAL")

    def test_child_error_overrides_clean_partial(self):
        self.assertFalse(self.assess(self.clean_result(),rc=-15)["accepted"])

    def test_missing_result_is_terminal(self):
        a=self.assess(None)
        self.assertFalse(a["accepted"]);self.assertIn("RESULT_MISSING_OR_MALFORMED",a["reasons"])

    def test_dirty_partial_is_terminal(self):
        r=self.clean_result();g,rows=self.latch();self.swallowed(g)
        r["audit_latch"]=g.snapshot();r["blocked_operations"]=["denied"]
        a=self.assess(r,b"".join(rows))
        self.assertFalse(a["accepted"])

    def test_external_journal_catches_stale_clean_result(self):
        r=self.clean_result()
        self.assertFalse(self.assess(r,b'{"event":"open"}\n')["accepted"])

    def test_absent_journal_is_terminal(self):
        self.assertFalse(self.assess(self.clean_result(),None)["accepted"])

    def test_malformed_identity_and_boolean_counter_rejected(self):
        for field,value in (("job_id","wrong"),("contract_sha256","wrong"),("pid",True),
                            ("likelihood_calls",True),("native_calls",10001)):
            r=self.clean_result();r[field]=value
            with self.subTest(field=field):
                self.assertFalse(self.assess(r)["accepted"])

    def test_missing_final_checkpoint_rejected(self):
        r=self.clean_result();del r["audit_latch"]["checkpoint_counts"]["final_before_result"]
        self.assertFalse(self.assess(r)["accepted"])

    def test_stopped_partial_cannot_hide_native_failure(self):
        r=self.clean_result();r["failure_receipt"]["application_exception_count"]=1
        r["failure_receipt"]["events"]=[{"kind":"APPLICATION_EXCEPTION"}]
        self.assertFalse(self.assess(r)["accepted"])

    def test_budget_partial_clean_is_protocol_partial(self):
        r=self.clean_result();r["status"]="BUDGET_EXHAUSTED_PARTIAL"
        r["failure_receipt"]["events"]=[{"kind":"BUDGET_STOP"}]
        r["failure_receipt"]["budget_abort_count"]=1
        self.assertEqual(self.assess(r)["disposition"],"CLEAN_PARTIAL")

    def test_campaign_failure_stops_next_double_and_returns_nonzero(self):
        launched=[];decisions=[]
        for r in (None,self.clean_result()):
            launched.append("double")
            a=self.assess(r);decisions.append(a)
            if not a["accepted"]:break
        self.assertEqual(len(launched),1)
        self.assertEqual(campaign_exit(decisions,2),2)

    def test_clean_complete_campaign_exit_zero_but_partial_stays_partial(self):
        a=self.assess(self.clean_result())
        self.assertEqual(campaign_exit([a,a],2),0)
        self.assertEqual(a["disposition"],"CLEAN_PARTIAL")

if __name__=="__main__":
    unittest.main()
