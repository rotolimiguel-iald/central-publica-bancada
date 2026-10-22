"""Supervise a single light historical calibration replay, not a campaign."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,subprocess,time
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import write,save,sha
def wsl(p):return '/mnt/c/'+str(p.resolve())[3:].replace('\\','/')
def main():
    regfile=B/'RINGDOWN_5SIGMA_V1_1_1.json';r=json.loads(regfile.read_bytes());spec=r['e7_rite_v1_1']
    source=B/'cache'/spec['posterior_product_name'];receipt=json.loads((ROOT/spec['execution_receipt_path']).read_bytes())
    wanted=receipt['products'][source.name]['sha256']
    target=D/'RITE_REPLAY_RESULT.json';assert not target.exists()
    command=['wsl.exe','--','env','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1',
      '/opt/lal_env/bin/python','-B',wsl(D/'producer/tgl_ringdown_ampliacao.py'),
      '--root',wsl(ROOT),'--registration',wsl(regfile),'--registration-sha256',sha(regfile),
      '--nuisance',wsl(ROOT/r['e7']['nuisance_path']),'--nuisance-sha256',r['e7']['nuisance_sha256'],
      '--posterior',wsl(source),'--posterior-sha256',wanted,'--output',wsl(target)]
    at=datetime.now(timezone.utc).isoformat();start=time.perf_counter();p=subprocess.run(command,capture_output=True,timeout=600)
    log=D/'RITE_REPLAY.log';write(log,p.stdout+b'\nSTDERR\n'+p.stderr)
    rec=dict(at=at,command=command,returncode=p.returncode,wall_seconds=time.perf_counter()-start,
        log_sha256=sha(log),output_sha256=sha(target) if target.exists() else None,heavy_machine_hours=0,
        scope='HISTORICAL_CALIBRATION_READ_ONLY_NO_PE_OR_MONTE_CARLO',gate_changed=False)
    save(D/'RITE_REPLAY_RECEIPT.json',rec);print(json.dumps(rec),flush=True)
    if p.returncode:print(p.stderr.decode('utf-8','replace'));raise SystemExit(p.returncode)
    value=json.loads(target.read_bytes());assert value['test_count']==0 and value['status']=='AWAITING_DATA'
    assert all(x['systematic_gate']=='red' and x['z_physical'] is None for x in value['matrix'])
    p=subprocess.run(['wsl.exe','--','/opt/lal_env/bin/python','-B',wsl(D/'check_launch_guards.py')],capture_output=True,timeout=60)
    write(D/'LAUNCH_GUARDS.log',p.stdout+b'\nSTDERR\n'+p.stderr)
    assert p.returncode==0,p.stderr.decode('utf-8','replace')
    out=json.loads(p.stdout.decode('utf-8'));save(D/'LAUNCH_GUARDS.json',out);print(json.dumps(out))
if __name__=='__main__':main()
