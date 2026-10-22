"""Finite AST-only orchestration review; never import/launch scientific sources."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse
import ast
import contextlib
import hashlib
import io
import json
import math
import os
import subprocess
import sys
import tempfile
import time
import types

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
SOURCE = BASE / 'refeito/activate_e7_final_v2_013bis.py'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(path, value):
    with path.open('xb') as stream:
        stream.write((json.dumps(value, allow_nan=False, indent=2) + '\n').encode())


def run_case(name, compiled):
    with tempfile.TemporaryDirectory(prefix='e7-fixture-', dir=HERE) as directory:
        root = Path(directory)
        base = root / 'B'
        (base / 'bis').mkdir(parents=True)
        (base / 'cache').mkdir()
        real_now = datetime(2030, 1, 1, tzinfo=timezone.utc)
        clock = [real_now]
        deadline = real_now + timedelta(seconds=60)
        class Clock:
            fromisoformat = staticmethod(datetime.fromisoformat)
            @staticmethod
            def now(tz):
                return clock[0]
        put(base / 'bis/PART_B_BUDGET_START.json', {'hard_deadline_utc': deadline.isoformat()})
        put(base / 'ORCAMENTO_40H.json', {'status':'REGISTERED_ZERO_NEW_PE_MEASURED_INSTRUMENT_WALL','wall_accounting': {'finalization_stop_utc': deadline.isoformat()}})
        result_path = base / 'e6.json'
        review_path = base / 'review.json'
        digest = 'fixture-registration'
        put(result_path, {'schema': 'E6_REACH_TABLE_V2', 'registration_sha256': digest})
        review = {'e6_result_sha256': sha(result_path), 'approved': True}
        if name == 'duplicate_approval':
            raw = '{"approved":false,"approved":true,"e6_result_sha256":"' + sha(result_path) + '"}'
            review_path.write_bytes(raw.encode())
        elif name == 'overflow_review':
            review_path.write_bytes((json.dumps(review)[:-1] + ',"cost":1e999}').encode())
        elif name == 'nonfinite_review':
            review_path.write_bytes((json.dumps(review)[:-1] + ',"cost":NaN}').encode())
        else:
            if name == 'approval_false':
                review['approved'] = False
            put(review_path, review)
        existing = None
        if name == 'existing_log':
            existing = base / 'bis/E7_FINAL_1.log'
        if name == 'existing_pending':
            existing = base / 'bis/E7_FINAL_2.log.pending'
        if name == 'existing_product':
            existing = base / 'bis/E7_FULLSAMPLE_RESULT_V1.json'
        if existing:
            existing.write_bytes(b'KEEP EXACT BYTES')
        if name == 'expired':
            clock[0] = deadline
        calls = []
        def fake_run(cmd, **kwargs):
            calls.append({'command': cmd, 'timeout': kwargs['timeout']})
            kwargs['stdout'].write(b'fixture process output only\n')
            if name == 'timeout_first' or (name == 'timeout_second' and len(calls) == 2):
                raise subprocess.TimeoutExpired(cmd, kwargs['timeout'])
            if name == 'interrupted':
                raise KeyboardInterrupt('fixture only')
            if name == 'nonzero_first':
                return types.SimpleNamespace(returncode=7)
            target = Path(cmd[cmd.index('--output') + 1])
            if not (name == 'missing_final' and len(calls) == 2):
                auth_path=base/'bis/E7_FINAL_AUTHORIZATION_V1.json'
                if len(calls)==1:
                    payload={'schema':'POSTERIORES_PSEOB_V1','registration_sha256':digest,'authorization_sha256':sha(auth_path),
                        'events':[{'event_id':'FIXTURE_'+str(j),'role':'calibration'} for j in range(33)]}
                    if name=='wrong_role': payload['events'][0]['role']='blind_test'
                    if name=='wrong_count': payload['events'].pop()
                else:
                    posterior_path=base/'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json'
                    payload={'status':'PREPARED_FAIL_CLOSED_NO_PHYSICAL_TEST','registration_sha256':digest,
                        'authorization_sha256':sha(auth_path),'posterior_sha256':sha(posterior_path),
                        'calibration_events':33,'test_events_added':0,'lnB':None,'z_physical':None,
                        'matrix':[{'verdict':'AWAITING_DATA','lnB':None,'z_physical':None,'correction_over_sigma_physical':None} for j in range(20)]}
                    if name=='physical_claim':payload['lnB']=3
                    if name=='wrong_matrix':payload['matrix'].pop()
                    if name=='wrong_posterior_pin':payload['posterior_sha256']='wrong'
                    if name=='bool_test_count':payload['test_events_added']=False
                    if name=='nonfinite_output':
                        with target.open('xb') as f:f.write((json.dumps(payload)[:-1]+',"bad":1e999}').encode())
                        return types.SimpleNamespace(returncode=0)
                put(target, payload)
            if name == 'deadline_crossed' and len(calls) == 2:
                clock[0] = deadline + timedelta(seconds=1)
            return types.SimpleNamespace(returncode=0)
        spec = {'plan_sha256': 'fixture-plan', 'producer_tree_sha256': {}, 'producer_directory': 'fixture-producer','plan_path':'B/plan.json'}
        put(base/'plan.json',{'events':[{'event_id':'FIXTURE_'+str(j),'role':'calibration'} for j in range(33)]})
        fake_sys = types.SimpleNamespace(executable='NEVER_EXECUTE', argv=[str(SOURCE), '--e6-result', str(result_path),
            '--e6-review', str(review_path), '--e6-review-sha256', sha(review_path)])
        ns = dict(Path=Path, datetime=Clock, timezone=timezone, argparse=argparse,
            hashlib=hashlib, json=json, math=math, os=os, subprocess=types.SimpleNamespace(run=fake_run, STDOUT=subprocess.STDOUT,TimeoutExpired=subprocess.TimeoutExpired),
            sys=fake_sys, time=time, B=base, R=root, __file__=str(SOURCE), sha=sha,
            publish_new=put, checked_registration=lambda: ({'e7': spec}, digest))
        exec(compiled, ns)
        old_argv = sys.argv
        exception = None
        try:
            sys.argv = fake_sys.argv
            with contextlib.redirect_stdout(io.StringIO()):
                ns['main']()
        except (Exception, SystemExit) as exc:
            exception = type(exc).__name__
        finally:
            sys.argv = old_argv
        receipt_path = base / 'bis/E7_FINAL_EXECUTION_V1.json'
        receipt = json.loads(receipt_path.read_bytes()) if receipt_path.exists() else None
        return dict(case=name, simulated_calls=len(calls), exception=exception,
            authorization_created=(base / 'bis/E7_FINAL_AUTHORIZATION_V1.json').exists(),
            receipt=receipt, existing_bytes_preserved=(existing.read_bytes() == b'KEEP EXACT BYTES') if existing else None,
            artifact_paths_are_temporary_fixture_only=True)


def main():
    before = sha(SOURCE)
    tree = ast.parse(SOURCE.read_bytes())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('main','strict_load')]
    if len(functions) != 2:
        raise ValueError('Expected main and strict_load')
    compiled = compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), 'exec')
    names = ['normal', 'missing_final', 'duplicate_approval', 'nonfinite_review', 'existing_log',
             'existing_product', 'timeout_first', 'timeout_second', 'nonzero_first', 'deadline_crossed', 'expired', 'approval_false','overflow_review','existing_pending','interrupted','wrong_role','wrong_count','physical_claim','wrong_matrix','wrong_posterior_pin','bool_test_count','nonfinite_output']
    rows = [run_case(name, compiled) for name in names]
    by = {r['case']: r for r in rows}
    success = 'E7_EXECUTED_NO_PHYSICAL_TEST'
    checks = {
        'source_unchanged': before == sha(SOURCE),
        'normal_fixture_success': by['normal']['receipt']['status'] == success,
        'normal_two_complete_records':len(by['normal']['receipt']['commands'])==2 and all(r['direct_child_reaped'] for r in by['normal']['receipt']['commands']),
        'existing_product_refused_before_auth':by['existing_product']['existing_bytes_preserved'] and not by['existing_product']['authorization_created'],
        'existing_log_refused_before_auth':by['existing_log']['existing_bytes_preserved'] and not by['existing_log']['authorization_created'],
        'pending_refused_before_auth':by['existing_pending']['existing_bytes_preserved'] and not by['existing_pending']['authorization_created'],
        'timeout_first_attempt_retained':len(by['timeout_first']['receipt']['commands'])==1 and by['timeout_first']['receipt']['commands'][0]['log_sha256'] is not None,
        'timeout_second_attempt_retained':len(by['timeout_second']['receipt']['commands'])==2 and by['timeout_second']['receipt']['commands'][1]['log_sha256'] is not None,
        'timeout_direct_reap_scoped':all(r['direct_child_reaped'] and 'group_absent' not in r for r in by['timeout_second']['receipt']['commands']),
        '30_seconds_reserved':all(r['timeout_seconds']==30 for r in by['normal']['receipt']['commands']),
        'interruption_retained_not_claimed_reaped':by['interrupted']['receipt']['failure']['type']=='KeyboardInterrupt' and not by['interrupted']['receipt']['commands'][0]['direct_child_reaped'],
    }
    for name in ('duplicate_approval','nonfinite_review','overflow_review','expired','approval_false'):
        checks[name+'_refused_before_auth']=not by[name]['authorization_created'] and by[name]['simulated_calls']==0
    for name in ('missing_final','nonzero_first','deadline_crossed','wrong_role','wrong_count','physical_claim','wrong_matrix','wrong_posterior_pin','bool_test_count','nonfinite_output','timeout_first','timeout_second','interrupted'):
        checks[name+'_failed_visible']=by[name]['receipt']['status']=='E7_FAILED_VISIBLE'
    if not all(checks.values()):
        raise ValueError(checks)
    pins = {}
    for rel in ['refeito/activate_e7_final_v2_013bis.py', 'bis/e2_code/registration_guard.py',
                'bis/e7_prepare/producer/extrai_posteriores_pseob.py',
                'bis/e7_prepare/producer/tgl_ringdown_ampliacao.py', 'RINGDOWN_5SIGMA_V1.json',
                'bis/e7_prepare/EXTRACTION_PLAN.json', 'bis/PART_B_BUDGET_START.json']:
        pins[rel] = sha(BASE / rel)
    registration = json.loads((BASE / 'RINGDOWN_5SIGMA_V1.json').read_bytes())
    plan = json.loads((BASE / 'bis/e7_prepare/EXTRACTION_PLAN.json').read_bytes())
    spec = registration['e7']
    pins_checks = {
        'guard_pin_matches': pins['bis/e2_code/registration_guard.py'] == spec['guard_sha256'],
        'plan_pin_matches': pins['bis/e7_prepare/EXTRACTION_PLAN.json'] == spec['plan_sha256'],
        'producer_tree_matches': {p.relative_to(BASE / 'bis/e7_prepare/producer').as_posix(): sha(p)
            for p in (BASE / 'bis/e7_prepare/producer').rglob('*.py')} == spec['producer_tree_sha256'],
        'plan_33_unique_calibration_ids': len(plan['events']) == len({r['event_id'] for r in plan['events']}) == 33
            and all(r['role'] == 'calibration' for r in plan['events']),
    }
    if not all(pins_checks.values()):
        raise ValueError(pins_checks)
    put(HERE / 'E7_ORCHESTRATION_V2_FINITE_RECEIPT.json', dict(
        status='FINITE_V2_CORRECTIONS_VERIFIED_NO_SCIENCE_EXECUTED',
        created_utc=datetime.now(timezone.utc).isoformat(), checks=checks, pin_checks=pins_checks,
        pins=pins, test_source_sha256=sha(__file__), optimization=sys.flags.optimize, cases=rows,
        limits='Only original main AST executed with fake guard, publisher, subprocess and clock. No production import, child process, HDF5, posterior, waveform or science. Does not retest frozen guard or scientific algorithms.'))
    print(json.dumps({'checks': len(checks) + len(pins_checks), 'all_true': True, 'source_sha256': before}))


if __name__ == '__main__':
    main()
