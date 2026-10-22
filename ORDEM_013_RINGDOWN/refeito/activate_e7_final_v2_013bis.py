"""Execute frozen E7 after a reviewed E6 result; exclusive, auditable outputs."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time

B = Path(__file__).resolve().parents[1]
R = B.parent
sys.path.insert(0, str(B / 'bis/e2_code'))
from registration_guard import checked_registration, publish_new, sha


def strict_load(path):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('Duplicate JSON key')
            out[key] = value
        return out
    def invalid(value):
        raise ValueError('Nonfinite JSON constant')
    def number(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError('Nonfinite JSON number')
        return result
    return json.loads(Path(path).read_bytes(), object_pairs_hook=pairs, parse_constant=invalid, parse_float=number)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--e6-result', type=Path, required=True)
    ap.add_argument('--e6-review', type=Path, required=True)
    ap.add_argument('--e6-review-sha256', required=True)
    args = ap.parse_args()
    reg, digest = checked_registration()
    for p in (args.e6_result, args.e6_review):
        if not p.resolve().is_relative_to(B):
            raise ValueError('E6 evidence outside the work package')
    if sha(args.e6_review) != args.e6_review_sha256:
        raise ValueError('Independent E6 review changed')
    review = strict_load(args.e6_review)
    if review.get('e6_result_sha256') != sha(args.e6_result) or review.get('approved') is not True:
        raise ValueError('E6 result has not passed independent closing')
    e6 = strict_load(args.e6_result)
    if e6.get('registration_sha256') != digest or e6.get('schema') != 'E6_REACH_TABLE_V2':
        raise ValueError('Wrong predecessor result')
    budget = strict_load(B / 'ORCAMENTO_40H.json')
    if budget.get('status') != 'REGISTERED_ZERO_NEW_PE_MEASURED_INSTRUMENT_WALL':
        raise ValueError('Allocation is not the reviewed wall allocation')
    deadline = min(datetime.fromisoformat(strict_load(B / 'bis/PART_B_BUDGET_START.json')['hard_deadline_utc']),
                   datetime.fromisoformat(budget['wall_accounting']['finalization_stop_utc']))
    if (deadline - datetime.now(timezone.utc)).total_seconds() <= 30:
        raise TimeoutError('Part B envelope expired')
    spec = reg['e7']
    authorization = B / 'bis/E7_FINAL_AUTHORIZATION_V1.json'
    output = B / 'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json'
    result = B / 'bis/E7_FULLSAMPLE_RESULT_V1.json'
    receipt = B / 'bis/E7_FINAL_EXECUTION_V1.json'
    log_paths = [B / ('bis/E7_FINAL_' + str(i) + '.log') for i in (1, 2)]
    planned_paths = [authorization, output, result, receipt, *log_paths]
    if any(p.exists() or p.with_name(p.name+'.pending').exists() for p in planned_paths):
        raise FileExistsError('Preserve earlier E7 attempt; use an explicit successor')
    now = datetime.now(timezone.utc)
    auth = dict(status='AUTHORIZED_BY_PRINCIPAL_AFTER_E2', registered_utc=now.isoformat(),
        registration_sha256=digest, plan_sha256=spec['plan_sha256'],
        producer_tree_sha256=spec['producer_tree_sha256'],
        e6_result_sha256=sha(args.e6_result), e6_review_sha256=sha(args.e6_review),
        allocation_sha256=sha(B / 'ORCAMENTO_40H.json'),
        scope='Full archived calibration samples only; no blind extraction or physical significance',
        authorizer_sha256=sha(Path(__file__)))
    publish_new(authorization, auth)
    common = ['--root', str(R), '--registration', str(B / 'RINGDOWN_5SIGMA_V1.json'),
              '--registration-sha256', digest, '--authorization', str(authorization),
              '--authorization-sha256', sha(authorization)]
    producer = R / spec['producer_directory']
    commands = [[sys.executable, '-B', str(producer / 'extrai_posteriores_pseob.py'),
                 *common, '--output', str(output)]]
    records = []
    started = time.perf_counter()
    failure = None
    try:
        for index in range(2):
            if index == 1:
                commands.append([sys.executable, '-B', str(producer / 'tgl_ringdown_ampliacao.py'),
                    *common, '--posterior', str(output), '--posterior-sha256', sha(output),
                    '--output', str(result)])
            cmd = commands[index]
            log = B / ('bis/E7_FINAL_' + str(index + 1) + '.log')
            task_started = datetime.now(timezone.utc)
            timeout = min(900, (deadline - task_started).total_seconds() - 30)
            if timeout <= 0:
                raise TimeoutError('Part B deadline')
            rec = dict(command=cmd, started_utc=task_started.isoformat(), returncode=None,
                timeout_seconds=timeout, error=None, direct_child_reaped=False,
                process_tree_scope='Frozen entrypoints spawn no explicit children; no group-absence claim')
            records.append(rec)
            try:
                with log.open('xb') as stream:
                    run = subprocess.run(cmd, stdout=stream, stderr=subprocess.STDOUT,
                        timeout=timeout, env=dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
                                                  MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1'))
                rec.update(returncode=run.returncode, direct_child_reaped=True)
            except subprocess.TimeoutExpired as exc:
                rec.update(error=dict(type=type(exc).__name__, message=str(exc)), direct_child_reaped=True,
                           reap_basis='subprocess.run kills and waits for its direct child on timeout')
                raise
            except BaseException as exc:
                rec['error'] = dict(type=type(exc).__name__, message=str(exc))
                raise
            finally:
                rec['finished_utc'] = datetime.now(timezone.utc).isoformat()
                rec['log_sha256'] = sha(log) if log.exists() else None
            if rec['returncode']:
                raise RuntimeError('Frozen E7 subprocess failed; log retained')
        if datetime.now(timezone.utc) >= deadline:
            raise TimeoutError('Result arrived after the allocated deadline')
        if not output.is_file() or not result.is_file() or output.is_symlink() or result.is_symlink():
            raise ValueError('Missing or linked product despite subprocess return code')
        output_pin = sha(output)
        payload = strict_load(output)
        full = strict_load(result)
        plan = strict_load(R / spec['plan_path'])
        expected_ids = [e['event_id'] for e in plan['events']]
        if len(expected_ids) != 33 or len(set(expected_ids)) != 33:
            raise ValueError('Expected frozen calibration plan changed')
        if (payload.get('schema') != 'POSTERIORES_PSEOB_V1' or
                payload.get('registration_sha256') != digest or
                payload.get('authorization_sha256') != sha(authorization) or
                [e['event_id'] for e in payload['events']] != expected_ids or
                any(e['role'] != 'calibration' for e in payload['events'])):
            raise ValueError('Extractor transport contract mismatch')
        if (full.get('status') != 'PREPARED_FAIL_CLOSED_NO_PHYSICAL_TEST' or
                full.get('registration_sha256') != digest or full.get('posterior_sha256') != output_pin or
                full.get('authorization_sha256') != sha(authorization) or
                type(full.get('calibration_events')) is not int or full['calibration_events'] != 33 or
                type(full.get('test_events_added')) is not int or full['test_events_added'] != 0 or
                full.get('lnB') is not None or full.get('z_physical') is not None or len(full['matrix']) != 20 or
                any(row['verdict'] != 'AWAITING_DATA' or row['lnB'] is not None or row['z_physical'] is not None
                    or row['correction_over_sigma_physical'] is not None for row in full['matrix'])):
            raise ValueError('Consumer scope or result transport mismatch')
        if sha(output) != output_pin or datetime.now(timezone.utc) >= deadline:
            raise ValueError('Product changed or final validation exceeded allocation')
    except BaseException as exc:
        failure = dict(type=type(exc).__name__, message=str(exc))
    products = {p.name: dict(sha256=sha(p), bytes=p.stat().st_size) for p in (output, result) if p.exists()}
    publish_new(receipt, dict(status='E7_EXECUTED_NO_PHYSICAL_TEST' if failure is None else 'E7_FAILED_VISIBLE',
        started_utc=now.isoformat(), finished_utc=datetime.now(timezone.utc).isoformat(),
        wall_seconds=time.perf_counter()-started, authorization_sha256=sha(authorization),
        commands=records, products=products, failure=failure))
    print(json.dumps(dict(receipt=str(receipt), sha256=sha(receipt), failure=failure)))
    if failure:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
