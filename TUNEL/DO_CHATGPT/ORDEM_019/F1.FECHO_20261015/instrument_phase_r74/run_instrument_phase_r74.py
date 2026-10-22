"""Run one previously reviewed/frozen R74 synthetic transport; no implicit retry."""
from pathlib import Path
import datetime as dt, hashlib, json, sys, time, traceback, importlib.util
ROOT=Path(__file__).resolve().parent

def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def put(name,value):
    with (ROOT/name).open('x',encoding='utf-8') as f:json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False)

def main():
    freeze=json.loads((ROOT/'FREEZE_R74.json').read_text(encoding='utf-8'))
    for row in freeze['files']:assert pin(row['path'])==row
    assert pin(ROOT/'run_instrument_phase_r74.py') in freeze['files']
    review=json.loads(Path(freeze['review']['path']).read_text(encoding='utf-8'))
    assert pin(freeze['review']['path'])==freeze['review']
    assert review['status'].startswith('PASS') and review['reviewer']!='codex-gerente-tgl'
    for name in ['consumer_r74.py','run_instrument_phase_r74.py','PLAN_R74.json']:
        assert pin(ROOT/name) in review['evidence']
    for name in ['START_R74.json','RESULT_R74.json','COMMAND_RESULT_R74.json']:
        if (ROOT/name).exists():raise FileExistsError('Existing run artifact: '+name)
    start=dt.datetime.now(dt.timezone.utc)
    assert dt.datetime.fromisoformat(freeze['created_utc'])<start
    put('START_R74.json',{'started_utc':start.isoformat(),'freeze':pin(ROOT/'FREEZE_R74.json'),'execution_count':1})
    timer=time.perf_counter();exit_code=1
    try:
        spec=importlib.util.spec_from_file_location('new_consumer_r74',ROOT/'consumer_r74.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        plan=json.loads((ROOT/'PLAN_R74.json').read_text(encoding='utf-8'))
        result=module.calculate(plan);exit_code=0 if result['passed'] else 1
        equality=[x['value'] for x in result['checks'] if x['relation']=='le']
        negatives=[x for x in result['checks'] if x['relation']=='gt']
        result.update({'max_equality_residual':max(equality,default=0.),'negative_controls':negatives,'source_pins':plan['sources']})
    except Exception:
        result={'status':'ERROR_SYNTHETIC_FRAME_INSTRUMENT','passed':False,'checks':[],'traceback':traceback.format_exc()}
    end=dt.datetime.now(dt.timezone.utc);seconds=time.perf_counter()-timer
    result.update({'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'seconds':seconds,'exit_code':exit_code,'freeze':pin(ROOT/'FREEZE_R74.json')})
    put('RESULT_R74.json',result)
    put('COMMAND_RESULT_R74.json',{'command':[sys.executable,'-B','-X','utf8',str(Path(__file__).resolve())],'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'seconds':seconds,'exit_code':exit_code,'result':pin(ROOT/'RESULT_R74.json'),'execution_count':1})
    print(json.dumps({'passed':result['passed'],'exit_code':exit_code,'checks':len(result['checks']),'result':pin(ROOT/'RESULT_R74.json')},ensure_ascii=False))
    return exit_code

if __name__=='__main__':
    sys.dont_write_bytecode=True
    raise SystemExit(main())

