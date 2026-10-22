"""Finite AST-only orchestration review; never import/launch scientific sources."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse
import ast
import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import types

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
SOURCE = BASE / 'refeito/activate_e7_final_013bis.py'


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
        put(base / 'ORCAMENTO_40H.json', {'wall_accounting': {'finalization_stop_utc': deadline.isoformat()}})
        result_path = base / 'e6.json'
        review_path = base / 'review.json'
        digest = 'fixture-registration'
        put(result_path, {'schema': 'E6_REACH_TABLE_V2', 'registration_sha256': digest})
        review = {'e6_result_sha256': sha(result_path), 'approved': True}
        if name == 'duplicate_approval':
            raw = '{"approved":false,"approved":true,"e6_result_sha256":"' + sha(result_path) + '"}'
            review_path.write_bytes(raw.encode())
        elif name == 'nonfinite_review':
            review_path.write_bytes((json.dumps(review)[:-1] + ',"cost":NaN}').encode())
        else:
            if name == 'approval_false':
                review['approved'] = False
            put(review_path, review)
        existing = None
        if name == 'existing_log':
            existing = base / 'bis/E7_FINAL_1.log'
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
            if name == 'nonzero_first':
                return types.SimpleNamespace(returncode=7)
            target = Path(cmd[cmd.index('--output') + 1])
            if not (name == 'missing_final' and len(calls) == 2):
                put(target, {'fixture': True})
            if name == 'deadline_crossed' and len(calls) == 2:
                clock[0] = deadline + timedelta(seconds=1)
            return types.SimpleNamespace(returncode=0)
        spec = {'plan_sha256': 'fixture-plan', 'producer_tree_sha256': {}, 'producer_directory': 'fixture-producer'}
        fake_sys = types.SimpleNamespace(executable='NEVER_EXECUTE', argv=[str(SOURCE), '--e6-result', str(result_path),
            '--e6-review', str(review_path), '--e6-review-sha256', sha(review_path)])
        ns = dict(Path=Path, datetime=Clock, timezone=timezone, argparse=argparse,
            hashlib=hashlib, json=json, os=os, subprocess=types.SimpleNamespace(run=fake_run, STDOUT=subprocess.STDOUT),
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
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main']
    if len(functions) != 1:
        raise ValueError('Expected exactly one main')
    compiled = compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), 'exec')
    names = ['normal', 'missing_final', 'duplicate_approval', 'nonfinite_review', 'existing_log',
             'existing_product', 'timeout_first', 'timeout_second', 'nonzero_first', 'deadline_crossed', 'expired', 'approval_false']
    rows = [run_case(name, compiled) for name in names]
    by = {r['case']: r for r in rows}
    success = 'E7_EXECUTED_NO_PHYSICAL_TEST'
    checks = {
        'source_unchanged': before == sha(SOURCE),
        'normal_fixture_success': by['normal']['receipt']['status'] == success,
        'missing_final_false_success_demonstrated': by['missing_final']['receipt']['status'] == success and len(by['missing_final']['receipt']['products']) == 1,
        'duplicate_approval_accepted_demonstrated': by['duplicate_approval']['simulated_calls'] == 2,
        'nonfinite_review_accepted_demonstrated': by['nonfinite_review']['simulated_calls'] == 2,
        'existing_log_preserved_but_auth_published': by['existing_log']['existing_bytes_preserved'] and by['existing_log']['authorization_created'],
        'existing_product_refused_before_auth': by['existing_product']['existing_bytes_preserved'] and not by['existing_product']['authorization_created'],
        'timeout_first_omits_attempt_record': by['timeout_first']['receipt']['commands'] == [] and by['timeout_first']['simulated_calls'] == 1,
        'timeout_second_omits_attempt_record': len(by['timeout_second']['receipt']['commands']) == 1 and by['timeout_second']['simulated_calls'] == 2,
        'nonzero_first_fails_without_second': by['nonzero_first']['receipt']['status'] == 'E7_FAILED_VISIBLE' and by['nonzero_first']['simulated_calls'] == 1,
        'deadline_crossing_success_demonstrated': by['deadline_crossed']['receipt']['status'] == success,
        'expired_refused_before_auth': not by['expired']['authorization_created'] and by['expired']['simulated_calls'] == 0,
        'approval_false_refused_before_auth': not by['approval_false']['authorization_created'] and by['approval_false']['simulated_calls'] == 0,
    }
    if not all(checks.values()):
        raise ValueError(checks)
    pins = {}
    for rel in ['refeito/activate_e7_final_013bis.py', 'bis/e2_code/registration_guard.py',
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
    put(HERE / 'E7_ORCHESTRATION_FINITE_RECEIPT.json', dict(
        status='FINITE_COUNTEREXAMPLES_REPRODUCED_NO_SCIENCE_EXECUTED',
        created_utc=datetime.now(timezone.utc).isoformat(), checks=checks, pin_checks=pins_checks,
        pins=pins, test_source_sha256=sha(__file__), optimization=sys.flags.optimize, cases=rows,
        limits='Only original main AST executed with fake guard, publisher, subprocess and clock. No production import, child process, HDF5, posterior, waveform or science. Does not retest frozen guard or scientific algorithms.'))
    print(json.dumps({'checks': len(checks) + len(pins_checks), 'all_true': True, 'source_sha256': before}))


if __name__ == '__main__':
    main()
