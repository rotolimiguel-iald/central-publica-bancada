"""25 local SOFTWARE_ONLY checks; artificial vectors/receipts and process doubles."""
import contextlib
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from fractions import Fraction

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from budget_counters import CallBudget, validate_limits, EXPECTED_LIMITS
from failure_audit import BudgetStop
from recovery_diagnostics import summarize
from result_acceptance import assess, paired_numerical, campaign_exit
from process_supervision import supervise


class CounterTests(unittest.TestCase):
    def test_01_initialization_counts_no_cap_plus_one(self):
        b = CallBudget(3, 3)
        self.assertEqual([b.take_likelihood() for _ in range(3)], [1, 2, 3])
        with self.assertRaises(BudgetStop): b.take_likelihood()
        self.assertEqual(b.snapshot()["likelihood_started"], 3)

    def test_02_native_guard_before_fourth_call(self):
        b = CallBudget(9, 2)
        b.take_native(); b.take_native()
        with self.assertRaises(BudgetStop): b.take_native()
        self.assertEqual(b.native_reserved, 2)

    def test_03_types_and_fixed_envelope(self):
        for bad in (True, 0, -1, 1.5):
            with self.assertRaises(ValueError): CallBudget(bad, 2)
        limits = dict(EXPECTED_LIMITS)
        validate_limits(limits)
        limits["workers"] = True
        with self.assertRaises(ValueError): validate_limits(limits)


class RecoveryTests(unittest.TestCase):
    def test_04_discrete_quantiles_independent_integer_reference(self):
        xs = [-0.5, 0.0, 0.5, 1.0]; counts = [1, 7, 7, 1]
        expected = []
        for numerator in (5, 50, 95):
            cumulative = 0
            for value, weight in zip(xs, counts):
                cumulative += weight
                if 100 * cumulative >= numerator * sum(counts):
                    expected.append(value); break
        r = summarize(xs, counts, 0.0, numerical_eligible=True)
        self.assertEqual([r["q05"], r["q50"], r["q95"]], expected)
        self.assertEqual(r["F_w_truth"], float(Fraction(8,16)))
        self.assertFalse(r["scientific_qualification"])
        self.assertFalse(r["D_ready"])

    def test_05_edges_included_and_duplicate_values(self):
        r = summarize([-0.8,-0.66,0.0,1.86,2.0], [1,1,4,1,1], 0.0, numerical_eligible=True)
        self.assertEqual(r["mass_lower_prior_edge"], 0.25)
        self.assertEqual(r["mass_upper_prior_edge"], 0.25)
        self.assertEqual(r["q50"], 0.0)

    def test_06_ineligible_has_no_favorable_verdict(self):
        r = summarize([-0.1,0.0,0.1], [1,8,1], 0.0, numerical_eligible=False)
        self.assertIsNone(r["proposed_favorable_condition"])
        self.assertEqual(r["interpretation"], "NUMERICALLY_INCOMPLETE_DESCRIPTIVE_ONLY")

    def test_07_invalid_inputs_never_silently_drop_mass(self):
        for weights in ([0,0],[-1,2],[float("nan"),1],[float("inf"),1],[True,1]):
            with self.assertRaises((ValueError,TypeError)): summarize([0,1],weights,0,numerical_eligible=True)
        for values in ([True,0],[float("nan"),0],[-0.81,0]):
            with self.assertRaises(ValueError): summarize(values,[1,1],0,numerical_eligible=True)

    def test_08_truth_inclusion_alone_not_enough(self):
        r = summarize([-0.8,2.0],[1,1],0.0,numerical_eligible=True)
        self.assertFalse(r["proposed_favorable_condition"])
        self.assertEqual(r["interpretation"],"RECOVERY_NOT_ESTABLISHED_FOR_THIS_REALIZATION")


def fixture():
    counts = {name:200 for name in ("pre_likelihood","post_likelihood","source_after_imports",
              "source_before_temporal","source_before_dictionary","source_before_waveform","source_after_waveform")}
    counts.update(initialization_ready=1,final_before_diagnostics=1,final_before_result=1)
    failures = {name:0 for name in ("source_returned_none_count","source_returned_none_counter_raw",
         "recognized_domain_exception_count","indeterminate_exception_after_native_attempt_count",
         "pre_native_exception_count","temporal_guard_count","application_exception_count","budget_abort_count")}
    failures.update(domain_error_total=None,events=[])
    return {"fixture_scope":"SOFTWARE_ONLY_NOT_A_REAL_P3_RESULT","job_id":"CASE","label":"GR_GAUSS",
        "contract_sha256":"test-contract","pid":7,"preparation_id":"test-preparation",
        "execution_id":"test-execution","decision_sha256":"test-decision","scientific_qualification":False,
        "status":"DLOGZ_REACHED_ESS_OK","likelihood_calls":200,"native_calls":200,
        "budget_counters":{"likelihood_started":200,"native_reserved":200,"likelihood_limit":100000,"native_limit":100000},
        "delta_logz_before_live_addition":0.05,"weighted_ESS":150.0,
        "live_logl_span_before_addition":1.0,"final_live_points_added":True,"error":None,
        "blocked_operations":[],"initialization_qualified":True,
        "initialization_analytic_before_likelihood":[{"fixture":1},{"fixture":2}],
        "initialization_analytic_after_likelihood":[{"fixture":1},{"fixture":2}],
        "D_read":False,"coverage_estimated":False,"independent_noise_realizations":False,
        "audit_latch":{"schema":"AUDIT_LATCH_V1","installed":True,"latched":False,"denial_count":0,
           "first_event":None,"events":[],"journal_error":None,"checkpoint_counts":counts,"interrupted_exceptions":[]},
        "audit_journal_sha256":hashlib.sha256(b"").hexdigest(),"failure_receipt":failures}


def check(row):
    return assess(row,b"",returncode=0,process_state="PROCESS_RETURNED",expected_job="CASE",
        expected_label="GR_GAUSS",expected_contract="test-contract",expected_pid=7,max_calls=100000,
        expected_preparation="test-preparation",expected_execution="test-execution",
        expected_decision="test-decision",max_native=100000,dlogz=0.1,ess_min=100)


class AcceptanceTests(unittest.TestCase):
    def test_09_finite_numerical_stop_is_not_science(self):
        d=check(fixture());self.assertTrue(d["accepted"]);self.assertTrue(d["numerical_criteria_met"])
        self.assertFalse(d["scientific_qualification"]);self.assertFalse(d["recovery_qualified"])

    def test_10_forged_status_bad_delta(self):
        for v in (None,0.1,0.3,-1,float("nan"),float("inf"),True):
            r=fixture();r["delta_logz_before_live_addition"]=v
            self.assertFalse(check(r)["accepted"])

    def test_11_forged_status_bad_ess(self):
        for v in (None,0,99,float("nan"),float("inf"),True):
            r=fixture();r["weighted_ESS"]=v;self.assertFalse(check(r)["accepted"])

    def test_12_nonflat_field_finite_and_positive(self):
        for v in (None,0,-1,float("nan"),float("inf"),True):
            r=fixture();r["live_logl_span_before_addition"]=v;self.assertFalse(check(r)["accepted"])

    def test_13_identity_binding(self):
        for field in ("preparation_id","execution_id","decision_sha256"):
            r=fixture();r[field]="wrong";self.assertFalse(check(r)["accepted"])

    def test_14_missing_fields_bool_counters_scope(self):
        for field in ("weighted_ESS","delta_logz_before_live_addition","scientific_qualification",
                      "preparation_id","execution_id","decision_sha256"):
            r=fixture();del r[field];self.assertFalse(check(r)["accepted"])
        r=fixture();r["likelihood_calls"]=True;self.assertFalse(check(r)["accepted"])

    def test_15_honest_clean_partial_not_numerical(self):
        r=fixture();r.update(status="STOPPED_NOT_CONVERGED",weighted_ESS=None,
             delta_logz_before_live_addition=57.0,final_live_points_added=False)
        d=check(r);self.assertTrue(d["accepted"]);self.assertFalse(d["numerical_criteria_met"])
        r.update(status="BUDGET_EXHAUSTED_PARTIAL",error="MAXCALL")
        r["failure_receipt"].update(events=[{"kind":"BUDGET_STOP"}],budget_abort_count=1)
        self.assertTrue(check(r)["accepted"])

    def test_16_both_cases_required_for_pair(self):
        good=check(fixture());partial=dict(good,numerical_criteria_met=False,disposition="CLEAN_PARTIAL")
        self.assertFalse(paired_numerical([good]));self.assertFalse(paired_numerical([good,partial]))
        self.assertTrue(paired_numerical([good,good]))
        self.assertEqual(campaign_exit([good,partial],2),0)
        self.assertNotEqual(campaign_exit([good],2),0)

    def test_17_audit_failure_invalidates_numeric_status(self):
        r=fixture();r["audit_latch"]["latched"]=True;self.assertFalse(check(r)["accepted"])
        r=fixture();r["blocked_operations"]=["TEST_ONLY"];self.assertFalse(check(r)["accepted"])

    def test_18_final_live_flag_and_call_boundary(self):
        for v in (None,False,1):
            r=fixture();r["final_live_points_added"]=v;self.assertFalse(check(r)["accepted"])
        r=fixture();r["likelihood_calls"]=100000;r["budget_counters"]["likelihood_started"]=100000
        self.assertFalse(check(r)["accepted"])


class FakeProcess:
    """No Popen, no OS signal, no real child."""
    def __init__(self, actions, clock):
        self.pid=7;self.actions=list(actions);self.rc=None;self.calls=[];self.clock=clock
    def wait(self,timeout):
        self.calls.append(("wait",timeout))
        action=self.actions.pop(0) if self.actions else self.rc
        if isinstance(action,BaseException):raise action
        if callable(action):return action(self)
        self.rc=action;return action
    def poll(self):
        self.calls.append(("poll",));return self.rc


def supervise_fixture(actions, *, kill_fails=False, clock_values=None):
    now=[0.0]
    p=FakeProcess(actions,now);kills=[]
    def kill(pid):
        kills.append(pid)
        if kill_fails:raise PermissionError("ARTIFICIAL_KILL_FAILURE")
    def clock():
        if clock_values and clock_values[0] is not None:return clock_values.pop(0)
        return now[0]
    r=supervise(lambda:p,wait_deadline=5,cleanup_deadline=9,clock=clock,
                kill_owned_group=kill,cleanup_context=contextlib.nullcontext)
    return r,p,kills


class SupervisionTests(unittest.TestCase):
    def test_19_normal_exit_and_already_finished_no_signal(self):
        r,p,k=supervise_fixture([0,0])
        self.assertTrue(r["process_accepted"]);self.assertTrue(r["termination_certain"]);self.assertEqual(k,[])

    def test_20_timeout_killed_reaped_still_failure(self):
        r,p,k=supervise_fixture([subprocess.TimeoutExpired("FAKE",5),-9])
        self.assertFalse(r["process_accepted"]);self.assertTrue(r["termination_certain"]);self.assertEqual(k,[7])

    def test_21_keyboard_interrupt_cleanup(self):
        r,p,k=supervise_fixture([KeyboardInterrupt(),-9])
        self.assertFalse(r["process_accepted"]);self.assertTrue(r["termination_certain"]);self.assertEqual(k,[7])

    def test_22_unexpected_wait_error_cleanup(self):
        r,p,k=supervise_fixture([RuntimeError("ARTIFICIAL_WAIT"),-9])
        self.assertFalse(r["process_accepted"]);self.assertEqual(k,[7])

    def test_23_kill_failure_never_success(self):
        r,p,k=supervise_fixture([KeyboardInterrupt(),0],kill_fails=True)
        self.assertTrue(r["termination_certain"]);self.assertFalse(r["process_accepted"])
        self.assertTrue(any("KILL_OR_POLL" in e for e in r["supervision_errors"]))

    def test_24_reap_failure_termination_uncertain(self):
        r,p,k=supervise_fixture([KeyboardInterrupt(),subprocess.TimeoutExpired("FAKE",4)])
        self.assertFalse(r["termination_certain"]);self.assertFalse(r["process_accepted"])

    def test_25_cleanup_deadline_never_extended(self):
        def slow_return(proc):
            proc.clock[0]=10
            proc.rc=0
            return 0
        r,p,k=supervise_fixture([slow_return])
        self.assertFalse(r["process_accepted"])
        self.assertFalse(r["within_cleanup_deadline"])
        self.assertTrue(any("DEADLINE" in e for e in r["supervision_errors"]))
        self.assertTrue(all(item[1]>0 for item in p.calls if item[0]=="wait"))


if __name__=="__main__":
    started=time.perf_counter()
    protocol=json.loads((ROOT/"PROTOCOLO_TESTES_STDLIB.json").read_bytes())
    for row in protocol["pins"]:
        raw=(ROOT/row["relative_path"]).read_bytes()
        if len(raw)!=row["bytes"] or hashlib.sha256(raw).hexdigest()!=row["sha256"]:
            raise RuntimeError("Software test source differs")
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
         for c in (CounterTests,RecoveryTests,AcceptanceTests,SupervisionTests))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if result.testsRun!=25:raise RuntimeError("Unexpected test count")
    report={"scope":"SOFTWARE_ONLY_ARTIFICIAL_VECTORS_AND_DOUBLES_NOT_P3_CONSUMPTION",
      "tests":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),
      "status":"PASS" if result.wasSuccessful() else "FAIL","wall_s":time.perf_counter()-started,
      "scientific_functions_called":0,"real_children_started":0,"external_inputs_opened":0,
      "candidate_driver_or_admission_imported":False,"runtime":sys.version,
      "preparation_id":protocol["preparation_id"]}
    q=ROOT/"RESULTADO_TESTES_STDLIB.json";t=q.with_name(q.name+".tmp")
    if q.exists():raise FileExistsError("Existing software result: inspect before deciding any repeat")
    raw=(json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode()
    with t.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if t.read_bytes()!=raw:raise OSError("Test report bytes differ")
    os.replace(t,q)
    print(json.dumps(report))
    sys.exit(0 if result.wasSuccessful() else 1)
