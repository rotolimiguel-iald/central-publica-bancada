"""Execute only documentary authorizer functions against owned synthetic paths."""
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
import sys
import tempfile

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
SOURCE = B/'refeito/activate_wall_budget_v2_013bis.py'


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
        data = {'schema_version':'E3_BUDGET_WALL_CANDIDATE_V1','status':'CANDIDATE_AWAITING_INDEPENDENT_REVIEW_NOT_ACTIVE','parent_registration_sha256':sha(reg),
            'allocation':dict.fromkeys(('new_PE_count','new_injection_count','new_download_count','new_science_wall_seconds','pipeline_repair_seconds'),0),
            'wall_accounting':{'finalization_stop_utc':(now+timedelta(seconds=-1 if name=='expired' else 600)).isoformat()},
            'jobs_relative_to_Chatgpt':'B/jobs.json','jobs_sha256':sha(jobs)}
        (base/'bis/PART_B_BUDGET_START.json').write_text(json.dumps({'hard_deadline_utc':(now+timedelta(seconds=500 if name=='global_exceeded' else 1000)).isoformat()}),encoding='utf-8')
        if name=='bool_allocation': data['allocation']['new_PE_count']=False
        candidate = base/'bis/e3_budget_wall/ORCAMENTO_40H_CANDIDATE.json'
        candidate.write_text(json.dumps(data),encoding='utf-8')
        review = root/'review.json'
        raw = '{"approved":true,"candidate_sha256":"'+sha(candidate)+'"}'
        if name=='duplicate_approval': raw=raw.replace('"approved":true','"approved":false,"approved":true')
        if name=='nonfinite_review': raw=raw[:-1]+',"score":NaN}'
        if name=='overflow_review': raw=raw[:-1]+',"score":1e999}'
        raw=raw[:-1]+',"created_utc":"'+(now+timedelta(seconds=1 if name=='future_review' else -1)).isoformat()+'"}'
        review.write_text(raw,encoding='utf-8')
        output = base/'ORCAMENTO_40H.json'; receipt=base/'bis/E3_WALL_BUDGET_ACTIVATION_V1.json'
        if name=='existing_budget': output.write_bytes(b'KEEP')
        if name=='existing_pending': output.with_name(output.name+'.pending').write_bytes(b'KEEP')
        if name=='jobs_changed': jobs.write_bytes(b'changed')
        ns=dict(Path=Path, datetime=Clock, timezone=timezone, argparse=argparse,hashlib=hashlib,json=json,os=os,math=math,
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
    rows=[case(n,compiled) for n in ('normal','duplicate_approval','nonfinite_review','missing_opening','expired','existing_budget','existing_pending','jobs_changed','overflow_review','future_review','bool_allocation','global_exceeded')]
    by={r['case']:r for r in rows}
    checks={
        'source_unchanged':before==sha(SOURCE),
        'normal_documentary_fixture':by['normal']['receipt_written'] and by['normal']['witness_written'],
        'duplicate_approval_refused':not by['duplicate_approval']['budget_written'],
        'nonfinite_review_refused':not by['nonfinite_review']['budget_written'],
        'opening_failure_after_budget':by['missing_opening']['budget_written'] and not by['missing_opening']['receipt_written'],
        'expired_refused':not by['expired']['budget_written'],
        'existing_budget_preserved':by['existing_budget']['original_preserved'] and not by['existing_budget']['receipt_written'],
        'pending_refused':not by['existing_pending']['budget_written'],
        'jobs_change_refused':not by['jobs_changed']['budget_written'], **{n+'_refused':not by[n]['budget_written'] for n in ('overflow_review','future_review','bool_allocation','global_exceeded')}}
    if not all(checks.values()): raise ValueError(checks)
    opening = B.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
    actual_candidate = B/'bis/e3_budget_wall/ORCAMENTO_40H_CANDIDATE.json'
    candidate_review = HERE/'E3_WALL_BUDGET_CANDIDATE_REVIEW_v2.json'
    actual = json.loads(actual_candidate.read_bytes())
    reviewed = json.loads(candidate_review.read_bytes())
    checks['actual_opening_exists'] = opening.is_file()
    checks['actual_candidate_approved_pin'] = reviewed['approved'] is True and reviewed['candidate_sha256'] == sha(actual_candidate)
    checks['actual_reserve_unexpired_at_review'] = datetime.now(timezone.utc) < datetime.fromisoformat(actual['wall_accounting']['finalization_stop_utc'])
    if not all(checks.values()): raise ValueError(checks)
    receipt=dict(status='WALL_BUDGET_ACTIVATION_V2_CLOSED_DOCUMENTARY_ONLY',approved=True,
        authorizer_sha256=before,candidate_sha256=sha(actual_candidate),
        candidate_review_sha256=sha(candidate_review),opening_witness_sha256=sha(opening),
        created_utc=datetime.now(timezone.utc).isoformat(),
        blocking_findings=[], closed_findings=['BW-A1'],
        notes=[{'id':'BW-N1','status':'NONBLOCKING_RESIDUAL',
                'reason':'Opening-witness read remains after budget publication. Actual opening exists and is hashed here; missing-opening fixture leaves partial documentary output. If any publication fails preserve it and issue explicit failure/successor, never treat partial budget alone as completed activation.'}],
        checks=checks,finite_cases=rows,optimization=sys.flags.optimize,review_source_sha256=sha(__file__),
        scope='Approved for exact reviewed candidate and authorizer bytes, documentary zero-job activation only. AST fixtures in owned temporary roots; real activation NOT performed. No runtime guard override/science approval. Principal must use the independently issued candidate review hash; sender self-approval is outside this authorization.',
        finalization_stop_utc=actual['wall_accounting']['finalization_stop_utc'],
        trust_boundary='External principal-supplied independent review hash, not cryptographic reviewer identity authentication.',
        positive_findings=['Duplicate keys, NaN and overflow refused before write.',
            'Schema/status and exact integer-zero fields validated.',
            'Fixed reserve and global cap, future/naive review rejection; no deadline restart.',
            'No subprocess/science or job override. Exclusive writes and pending preflight.',
            'Exact reviewed parent registration/jobs pins and candidate identity.'])
    path=HERE/'E3_WALL_BUDGET_ACTIVATION_V2_CLOSING_REVIEW.json'
    with path.open('xb') as f:f.write((json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
    print(json.dumps({'authorizer_sha256':before,'receipt_sha256':sha(path),'checks':len(checks),'blocking':[]}))


if __name__=='__main__':main()
