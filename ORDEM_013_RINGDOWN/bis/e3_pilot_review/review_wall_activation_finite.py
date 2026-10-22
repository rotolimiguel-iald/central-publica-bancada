"""Execute only documentary authorizer functions against owned synthetic paths."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse
import ast
import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
SOURCE = B/'refeito/activate_wall_budget_013bis.py'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def case(name, compiled):
    with tempfile.TemporaryDirectory(prefix='wall-fixture-', dir=HERE) as directory:
        root = Path(directory); base = root/'B'; tunnel = root/'TUNEL/DO_CHATGPT'
        (base/'bis/e3_budget_wall').mkdir(parents=True); tunnel.mkdir(parents=True)
        now = datetime(2030,1,1,tzinfo=timezone.utc)
        class Clock:
            fromisoformat = staticmethod(datetime.fromisoformat)
            @staticmethod
            def now(tz): return now
        reg = base/'RINGDOWN_5SIGMA_V1.json'; reg.write_bytes(b'{"fixture":true}')
        jobs = base/'jobs.json'; jobs.write_bytes(b'{"jobs":{},"downloads":{}}')
        opening = tunnel/'ENTREGA_013BIS_ABERTURA_operador.md'
        if name != 'missing_opening': opening.write_bytes(b'fixture witness')
        data = {'parent_registration_sha256':sha(reg),
            'allocation':dict.fromkeys(('new_PE_count','new_injection_count','new_download_count','new_science_wall_seconds','pipeline_repair_seconds'),0),
            'wall_accounting':{'finalization_stop_utc':(now+timedelta(seconds=-1 if name=='expired' else 600)).isoformat()},
            'jobs_relative_to_Chatgpt':'B/jobs.json','jobs_sha256':sha(jobs)}
        candidate = base/'bis/e3_budget_wall/ORCAMENTO_40H_CANDIDATE.json'
        candidate.write_text(json.dumps(data),encoding='utf-8')
        review = root/'review.json'
        raw = '{"approved":true,"candidate_sha256":"'+sha(candidate)+'"}'
        if name=='duplicate_approval': raw=raw.replace('"approved":true','"approved":false,"approved":true')
        if name=='nonfinite_review': raw=raw[:-1]+',"score":NaN}'
        review.write_text(raw,encoding='utf-8')
        output = base/'ORCAMENTO_40H.json'; receipt=base/'bis/E3_WALL_BUDGET_ACTIVATION_V1.json'
        if name=='existing_budget': output.write_bytes(b'KEEP')
        if name=='existing_pending': output.with_name(output.name+'.pending').write_bytes(b'KEEP')
        if name=='jobs_changed': jobs.write_bytes(b'changed')
        ns=dict(Path=Path, datetime=Clock, timezone=timezone, argparse=argparse,hashlib=hashlib,json=json,os=os,
            B=base,R=root,D=tunnel,__file__=str(SOURCE))
        exec(compiled,ns)
        old=sys.argv; error=None
        try:
            sys.argv=[str(SOURCE),'--review',str(review),'--review-sha256',sha(review)]
            with contextlib.redirect_stdout(io.StringIO()): ns['main']()
        except Exception as exc: error=type(exc).__name__
        finally: sys.argv=old
        return dict(case=name,error=error,budget_written=output.exists(),receipt_written=receipt.exists(),
            witness_written=(tunnel/'ENTREGA_013BIS_E3_ORCAMENTO_PAREDE_V1.md').exists(),
            original_preserved=(output.read_bytes()==b'KEEP') if name=='existing_budget' else None)


def main():
    before=sha(SOURCE)
    tree=ast.parse(SOURCE.read_bytes())
    compiled=compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(SOURCE),'exec')
    rows=[case(n,compiled) for n in ('normal','duplicate_approval','nonfinite_review','missing_opening','expired','existing_budget','existing_pending','jobs_changed')]
    by={r['case']:r for r in rows}
    checks={
        'source_unchanged':before==sha(SOURCE),
        'normal_documentary_fixture':by['normal']['receipt_written'] and by['normal']['witness_written'],
        'duplicate_approval_accepted':by['duplicate_approval']['receipt_written'],
        'nonfinite_review_accepted':by['nonfinite_review']['receipt_written'],
        'opening_failure_after_budget':by['missing_opening']['budget_written'] and not by['missing_opening']['receipt_written'],
        'expired_refused':not by['expired']['budget_written'],
        'existing_budget_preserved':by['existing_budget']['original_preserved'] and not by['existing_budget']['receipt_written'],
        'pending_refused':not by['existing_pending']['budget_written'],
        'jobs_change_refused':not by['jobs_changed']['budget_written']}
    if not all(checks.values()): raise ValueError(checks)
    receipt=dict(status='ACTIVATION_CHANGES_REQUIRED_DOCUMENTARY_ONLY',approved=False,
        authorizer_sha256=before,candidate_sha256=sha(B/'bis/e3_budget_wall/ORCAMENTO_40H_CANDIDATE.json'),
        candidate_approval_receipt_sha256=sha(HERE/'E3_WALL_BUDGET_CANDIDATE_REVIEW_v2.json'),
        blocking_findings=[{'id':'BW-A1','reason':'Pinned review accepts duplicate approved keys and NaN. Both finite fixtures register the synthetic budget.',
            'fix':'Strict JSON duplicate/nonfinite rejection for review/candidate/jobs, typed approved identity True; retain exact candidate/review pins.'}],
        notes=[{'id':'BW-N1','reason':'Missing opening witness is read only after budget publication, causing partial publication without receipt.',
            'fix':'Read and pin opening witness before first write; preflight pending paths and retain explicit partial/failure receipt if later publication fails.'}],
        checks=checks,finite_cases=rows,optimization=sys.flags.optimize,review_source_sha256=sha(__file__),
        scope='AST functions only in owned temporary roots. No actual activation, guard, jobs, runtime or science execution. Candidate itself separately approved. External principal-provided independent review hash is trust anchor; authorizer does not authenticate reviewer identity cryptographically.',
        positive_findings=['Fixed candidate reserve is not reset by activation.', 'Exact parent E2 and jobs pins checked; zero new allocations required.',
            'Exclusive temporary writes and hard-link publication preserve existing outputs.', 'No subprocess/science launch or guard/job override.'])
    path=HERE/'E3_WALL_BUDGET_ACTIVATION_REVIEW.json'
    with path.open('xb') as f:f.write((json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
    print(json.dumps({'authorizer_sha256':before,'receipt_sha256':sha(path),'checks':len(checks),'blocking':['BW-A1']}))


if __name__=='__main__':main()
