"""Check V1 before/after creating its authorized sibling; no activation or seed read."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,importlib.util,time,resource
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
D=B/'bis/015/t03';SRC=B/'bis/e2_code';DST=B/'bis/e2_code_v1_1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p):return {q.relative_to(p).as_posix():sha(q) for q in sorted(p.rglob('*.py'))}
def publish(p,obj):
    raw=(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode();tmp=p.with_suffix(p.suffix+'.pending')
    if p.exists():raise FileExistsError(p)
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.rename(p)
def check():
    started=time.perf_counter()
    spec=importlib.util.spec_from_file_location('v1_guard_audit_015',SRC/'registration_guard.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    try:m.checked_registration();r=dict(status='SUCCESS')
    except Exception as e:r=dict(status='EXCEPTION',type=type(e).__name__,message=str(e))
    r['wall_seconds']=time.perf_counter()-started
    r['acceptable']=r['status']=='SUCCESS' or (r.get('type')=='TimeoutError' and r.get('message')=='Part B hard deadline reached')
    return r
def main():
    resource.setrlimit(resource.RLIMIT_CPU,(899,900));resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
    D.mkdir(exist_ok=False);start=time.perf_counter()
    regfile=B/'RINGDOWN_5SIGMA_V1.json';reg=json.loads(regfile.read_bytes())
    beforetree=tree(SRC);assert beforetree==reg['own_code_tree_sha256']
    extras=[dict(path=v['relative_to_Chatgpt'],actual=tree(B.parent/v['relative_to_Chatgpt']),expected=v['files_sha256']) for v in reg.get('extra_code_roots',[])]
    assert all(v['actual']==v['expected'] for v in extras)
    before=check();publish(D/'V1_BEFORE.json',before)
    if not before['acceptable']:raise RuntimeError('V1 precheck failed; sibling not created')
    DST.mkdir(exist_ok=False)
    for p in sorted(SRC.rglob('*.py')):
        out=DST/p.relative_to(SRC);out.parent.mkdir(parents=True,exist_ok=True)
        with out.open('xb') as f:f.write(p.read_bytes())
    assert tree(DST)==beforetree
    after=check();publish(D/'V1_AFTER_COPY.json',after)
    unchanged=tree(SRC)==beforetree and all(tree(B.parent/v['path'])==v['actual'] for v in extras)
    result=dict(at=datetime.now(timezone.utc).isoformat(),status='COPIED_NOT_AMENDED_NOT_ACTIVATED' if after['acceptable'] and unchanged else 'VISIBLE_FAILURE',
        original_registration_sha256=sha(regfile),original_tree_sha256=beforetree,copy_tree_sha256=tree(DST),extra_trees=extras,
        before=before,after=after,originals_unchanged=unchanged,wall_seconds=time.perf_counter()-start,cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,
        seed_read=False,heavy_machine_hours=0,budget_R7_created=False)
    publish(D/'COPY_RECEIPT.json',result)
    print(json.dumps({k:result[k] for k in ['status','before','after','originals_unchanged','wall_seconds','cpu_seconds']}))
if __name__=='__main__':main()
