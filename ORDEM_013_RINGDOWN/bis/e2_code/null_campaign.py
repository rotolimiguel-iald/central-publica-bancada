"""Execute each frozen E2 synthetic null once, sequentially; fail visibly."""
import os,subprocess,sys,time,json
from pathlib import Path
from datetime import datetime,timezone
from registration_guard import checked_registration,BASE,sha,time_guard,publish_new


def main():
    reg,digest=checked_registration();names=sorted(reg['nulls']['cells'])
    out=BASE/'bis/RESULT_E2_NULL_CAMPAIGN.json'
    if out.exists():raise FileExistsError('Campaign already has a receipt')
    existing=[n for n in names if (BASE/'bis'/('RESULT_E2_NULL_'+n+'.json')).exists() or (BASE/'bis'/('RESULT_E2_NULL_'+n+'_FAILURE.json')).exists()]
    if existing:raise FileExistsError('Cells were previously attempted; resume requires explicit preserved-attempt audit')
    start=time.perf_counter();utc=datetime.now(timezone.utc).isoformat();receipts=[];failed=None
    name=None
    try:
      for name in names:
        time_guard(reg)
        try:
            result=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('null_runner.py')),'--cell',name],
              env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'},
              capture_output=True,text=True,timeout=max(1,time_guard(reg).timestamp()-time.time()-10))
        except subprocess.TimeoutExpired as exc:
            log=BASE/'bis'/('E2_NULL_'+name+'_TIMEOUT.log')
            as_bytes=lambda x:x if isinstance(x,bytes) else (x or '').encode('utf-8')
            raw=as_bytes(exc.stdout)+as_bytes(exc.stderr)
            with log.open('xb') as f:f.write(raw)
            failed={'cell':name,'returncode':None,'exception':'TimeoutExpired','log_sha256':sha(log)}
            break
        log=BASE/'bis'/('E2_NULL_'+name+'.log')
        with log.open('x') as f:f.write(result.stdout+result.stderr)
        path=BASE/'bis'/('RESULT_E2_NULL_'+name+'.json')
        if result.returncode or not path.exists():failed={'cell':name,'returncode':result.returncode,'log_sha256':sha(log)};break
        value=json.loads(path.read_bytes())
        if value['registration_sha256']!=digest or value['cell']!=reg['nulls']['cells'][name] or value['result']['draws']!=reg['nulls']['cells'][name]['draws']:
            raise ValueError('Null receipt does not match frozen cell')
        receipts.append({'cell':name,'result_sha256':sha(path),'log_sha256':sha(log),'wall_seconds':value['wall_seconds']})
        print(json.dumps({'completed':len(receipts),'total':len(names),'cell':name,'wall_seconds':value['wall_seconds']}),flush=True)
    except Exception as exc:
        failed={'cell':name,'exception':type(exc).__name__,'message':str(exc),
                'completed_receipts_preserved':len(receipts)}
    value={'status':'SYNTHETIC_NULLS_COMPLETED_NOT_PHYSICAL_5SIGMA' if failed is None else 'SYNTHETIC_NULL_CAMPAIGN_FAILED',
      'registration_sha256':digest,'started_utc':utc,'finished_utc':datetime.now(timezone.utc).isoformat(),
      'wall_seconds':time.perf_counter()-start,'requested_cells':names,'completed':receipts,'failed':failed,
      'code_sha256':sha(Path(__file__))}
    publish_new(out,value)
    print(json.dumps({'status':value['status'],'sha256':sha(out)}),flush=True)
    if failed:raise SystemExit(2)


if __name__=='__main__':main()
