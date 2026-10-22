"""Execute frozen E7 after a reviewed E6 result; exclusive, auditable outputs."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

B = Path(__file__).resolve().parents[1]
R = B.parent
sys.path.insert(0, str(B / 'bis/e2_code'))
from registration_guard import checked_registration, publish_new, sha


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
    review = json.loads(args.e6_review.read_bytes())
    if review.get('e6_result_sha256') != sha(args.e6_result) or review.get('approved') is not True:
        raise ValueError('E6 result has not passed independent closing')
    e6 = json.loads(args.e6_result.read_bytes())
    if e6.get('registration_sha256') != digest or e6.get('schema') != 'E6_REACH_TABLE_V2':
        raise ValueError('Wrong predecessor result')
    budget = json.loads((B / 'ORCAMENTO_40H.json').read_bytes())
    deadline = min(datetime.fromisoformat(json.loads((B / 'bis/PART_B_BUDGET_START.json').read_bytes())['hard_deadline_utc']),
                   datetime.fromisoformat(budget['wall_accounting']['finalization_stop_utc']))
    if datetime.now(timezone.utc) >= deadline:
        raise TimeoutError('Part B envelope expired')
    spec = reg['e7']
    authorization = B / 'bis/E7_FINAL_AUTHORIZATION_V1.json'
    output = B / 'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json'
    result = B / 'bis/E7_FULLSAMPLE_RESULT_V1.json'
    receipt = B / 'bis/E7_FINAL_EXECUTION_V1.json'
    if any(p.exists() for p in (authorization, output, result, receipt)):
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
            timeout = min(900, (deadline - task_started).total_seconds())
            if timeout <= 0:
                raise TimeoutError('Part B deadline')
            with log.open('xb') as stream:
                run = subprocess.run(cmd, stdout=stream, stderr=subprocess.STDOUT,
                    timeout=timeout, env=dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
                                              MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1'))
            records.append(dict(command=cmd, returncode=run.returncode,
                started_utc=task_started.isoformat(), finished_utc=datetime.now(timezone.utc).isoformat(),
                log_sha256=sha(log)))
            if run.returncode:
                raise RuntimeError('Frozen E7 subprocess failed; log retained')
    except Exception as exc:
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
