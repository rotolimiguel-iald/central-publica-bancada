"""Activate the independently reviewed metadata assembler after three real stage reviews."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, os, subprocess, sys, time
B=Path(__file__).resolve().parents[1];R=B.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):return dict(path=p.relative_to(R).as_posix(),sha256=sha(p))
def new(p,value):
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode();tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw):raise OSError('Short write')
    os.link(tmp,p);tmp.unlink()
def main():
    package=B/'bis/e6_prepare_v3';closing=load(B/'bis/e6_review/E6_FOCUSED_CLOSING_V3_RECEIPT.json')
    if closing['blocking_findings'] or closing['status']!='BLOCKERS_CLOSED_PREPARATION_ONLY':raise ValueError('Code review not closed')
    if {n:sha(package/n) for n in closing['package_sha256']}!=closing['package_sha256']:raise ValueError('Reviewed package changed')
    regpath=B/'RINGDOWN_5SIGMA_V1.json';reg=load(regpath);stages={}
    for stage,folder in [('E3.2','e3_2_actual_001'),('E3.3','e3_3_actual_001'),('TEST','test_actual_001')]:
        p=B/'bis/e3_wall_stages/candidates'/folder/'ADAPTER_REVIEWED.json';d=load(p);review=load(R/d['review']['path'])
        if sha(R/d['review']['path'])!=d['review']['sha256'] or review['status']!='ACCEPTED_FOR_E6_MAPPING' or review['blocking_findings']:raise ValueError('Unreviewed stage')
        if d['stage']!=stage or any(review[k]!=d[k] for k in ('stage','registration_sha256','bindings','predecessor','timeline','outcome')):raise ValueError('Stage review differs')
        stages[stage]=pin(p)
    budget=load(B/'ORCAMENTO_40H.json');stop=min(datetime.fromisoformat(budget['wall_accounting']['finalization_stop_utc']),datetime.fromisoformat(load(B/'bis/PART_B_BUDGET_START.json')['hard_deadline_utc']))
    now=datetime.now(timezone.utc)
    if (stop-now).total_seconds()<60:raise TimeoutError('Reserve expired')
    authorization=B/'bis/E6_ACTUAL_AUTHORIZATION_V1.json';receipt=B/'bis/E6_ACTUAL_EXECUTION_V1.json';log=B/'bis/E6_ACTUAL_EXECUTION_V1.log'
    if any(p.exists() or p.with_name(p.name+'.pending').exists() for p in (authorization,receipt,log)) or (package/'runs/wall_actual_001').exists():raise FileExistsError('Preserve actual run')
    auth=dict(status='AUTHORIZED_E6_ASSEMBLY_AFTER_REVIEWED_E3_AND_TEST',issued_utc=now.isoformat(),
        new_scientific_computation_allowed=False,package_sha256=closing['package_sha256'],registration=pin(regpath),
        witness=pin(R/reg['witness_relative_to_Chatgpt']),reviewed_stages=stages,run_id='wall_actual_001',
        code_review=pin(B/'bis/e6_review/E6_FOCUSED_CLOSING_V3_RECEIPT.json'),budget=pin(B/'ORCAMENTO_40H.json'),
        authorizer_sha256=sha(Path(__file__)))
    new(authorization,auth);start=time.perf_counter();error=None;code=None
    cmd=[sys.executable,'-B',str(package/'generate_reach_table.py'),'--execute','--authorization',str(authorization),'--authorization-sha256',sha(authorization)]
    try:
        with log.open('xb') as stream:
            run=subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT,timeout=min(300,(stop-datetime.now(timezone.utc)).total_seconds()-30))
        code=run.returncode
        if code:raise RuntimeError('Assembler failed; log retained')
        if datetime.now(timezone.utc)>=stop:raise TimeoutError('Completion beyond allocation')
    except BaseException as exc:error=dict(type=type(exc).__name__,message=str(exc))
    products={p.name:pin(p) for p in (package/'runs/wall_actual_001').glob('*') if p.is_file()}
    new(receipt,dict(status='E6_ASSEMBLED_PENDING_INDEPENDENT_RESULT_REVIEW' if error is None else 'E6_FAILED_VISIBLE',
        started_utc=now.isoformat(),finished_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.perf_counter()-start,
        authorization_sha256=sha(authorization),command=cmd,returncode=code,error=error,log_sha256=sha(log),products=products))
    print(json.dumps(dict(receipt=str(receipt),sha256=sha(receipt),error=error)))
    if error:raise SystemExit(1)
if __name__=='__main__':main()
