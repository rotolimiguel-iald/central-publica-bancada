"""Local terminal-receipt controls; no subprocess or scientific sample."""
from pathlib import Path
import sys,json,copy
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import save,write,sha
from t03_terminal_guard import require_terminal

def fixture(name,complete=False,damage=None):
    root=D/'t04/terminal_guard_tests'/name
    d=root/'ORDEM_013_RINGDOWN/bis/015';run=d/'nulls_campaign_001'
    count=30 if complete else 6
    names=['cell_'+str(i) for i in range(30)]
    plan=dict(cell_ids=names,registration_sha256='fixture-only')
    save(run/'PLAN.json',plan)
    result=dict(plan_sha256=sha(run/'PLAN.json'),registration_sha256='fixture-only',
        status='SYNTHETIC_NULLS_COMPLETED_NOT_PHYSICAL_5SIGMA' if complete else 'T03_MEDIDA_PARTIAL_NO_RETRY',
        fault=None if complete else dict(type='TimeoutError'),machine_hours_union=.99,
        finished=[dict(cell=k,accepted=complete,pid=120+i,returncode=0 if complete else -15,end_utc='fixture-only') for i,k in enumerate(names[:count])],
        not_started=names[count:])
    if damage=='unfinished':result['finished'][0].pop('end_utc')
    if damage=='hours':result['machine_hours_union']=1.1
    if damage=='duplicate':result['not_started'].append(names[0])
    save(run/'RESULT.json',result)
    summary=dict(campaign_sha256=sha(run/'RESULT.json'),registration_sha256='fixture-only',
        status='T03_SYNTHETIC_TAILS_MEASURED' if complete else 'T03_MEDIDA_INCOMPLETE_WITH_COST',
        completed=30 if complete else 0,rows=[{} for _ in range(30)] if complete else [])
    if damage=='raw_result':return d
    if damage=='hash':summary['campaign_sha256']='altered'
    save(run/'SUMMARY.json',summary)
    text=sha(run/'RESULT.json')+'\n'+sha(run/'SUMMARY.json')
    out=root/'TUNEL/DO_CHATGPT'
    write(out/'ENTREGA_015_T03_nulos_1e8.md',text.encode())
    if not complete and damage!='missing_medida':write(out/'ENTREGA_015_MEDIDA_T03_nulos_parciais.md',text.encode())
    return d

def main():
    rows=[]
    for name,complete,damage,expect in [
        ('complete',True,None,True),('partial_documented',False,None,True),
        ('raw_result',False,'raw_result',False),('hash',False,'hash',False),
        ('missing_medida',False,'missing_medida',False),('unfinished',False,'unfinished',False),
        ('overbudget',False,'hours',False),('duplicate',False,'duplicate',False),
        ('still_running',True,None,False)]:
        d=fixture(name,complete,damage)
        try:result=require_terminal(d,running=lambda _:name=='still_running');accepted=True;error=None
        except (AssertionError,KeyError,FileNotFoundError) as exc:accepted=False;error=type(exc).__name__
        rows.append(dict(test=name,expected=expect,accepted=accepted,passed=accepted==expect,error=error))
    receipt=dict(tests=rows,passed=sum(r['passed'] for r in rows),total=len(rows),
        source_sha256=sha(D/'t03_terminal_guard.py'),scientific_runs=0,
        scope='Synthetic receipt validation; does not verify native source or live process lifecycle')
    save(D/'t04/TERMINAL_GUARD_TESTS.json',receipt)
    print(json.dumps(receipt))
    assert all(r['passed'] for r in rows)
if __name__=='__main__':main()
