"""Remove only checked Python bytecode caches named in F0.3.E5."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,os,subprocess,sys
O=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019')
B=Path(r'C:\IALD\PROGRAMA_IALD')
D=O/'F0.3';PLAN=D/'CACHE_HYGIENE_E5_PLAN_20261008.json';RESULT=D/'CACHE_HYGIENE_E5_RESULT_20261008.json'
UNITS=('ADENDO003_COORD','F2.3','F3.6','F5.2','F7.2','F9.9')
EXPECT={'ADENDO003_COORD/CANCEL_MEMORY_PIN_CANDIDATE/__pycache__','F2.3/__pycache__','F3.6/ASIMOV_LAMBDA_SANDBOX/__pycache__','F5.2/CANDIDATO_R2_20261008/__pycache__','F5.2/CANDIDATO_R3_20261008/__pycache__','F7.2/__pycache__','F7.2/STAGING/bancada/__pycache__','F9.9/STAGING/__pycache__','F9.9/STAGING/iald_orchestrator/__pycache__'}
def wx(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def h(p):return sha256(p.read_bytes()).hexdigest()
def main():
 if PLAN.exists() or RESULT.exists():raise FileExistsError('cache output exists')
 state=json.loads(subprocess.check_output([sys.executable,'-X','utf8',str(B/'iald.py'),'ver','F0.3.E5'],text=True));cl=state.get('reivindicacao') or {}
 if state.get('status')!='EM_CURSO' or cl.get('quem')!='codex-coordenadora' or not all(u in cl.get('nota','') for u in UNITS):raise RuntimeError('named F0.3.E5 claim required')
 dirs=sorted({p for u in UNITS for p in (O/u).rglob('__pycache__') if p.is_dir()},key=str)
 actual={p.relative_to(O).as_posix() for p in dirs}
 if actual!=EXPECT:raise RuntimeError('unexpected cache inventory '+repr((actual-EXPECT,EXPECT-actual)))
 root=O.resolve(strict=True);rows=[]
 for p in dirs:
  target=p.resolve(strict=True)
  if not target.is_relative_to(root) or target!=p.absolute() or p.is_symlink() or os.path.isjunction(p):raise RuntimeError('unsafe cache path '+str(p))
  for par in [p,*p.parents]:
   if par==O.parent:break
   if par.is_symlink() or os.path.isjunction(par):raise RuntimeError('reparse parent '+str(par))
  files=list(p.iterdir())
  if not files or any(not x.is_file() or x.suffix!='.pyc' or x.is_symlink() for x in files):raise RuntimeError('unexpected cache content '+str(p))
  rs=[dict(path=str(x),sha256=h(x),bytes=x.stat().st_size) for x in sorted(files)]
  rows.append(dict(directory=str(p),resolved=str(target),files=rs))
 plan=dict(unit='F0.3.E5',claim=cl,started_utc=datetime.now(timezone.utc).isoformat(),scope='nine caches in six named units; files must be regular .pyc; no recursive delete',targets=rows)
 wx(PLAN,(json.dumps(plan,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
 for row in rows:
  p=Path(row['directory'])
  for x in row['files']:
   f=Path(x['path'])
   if h(f)!=x['sha256']:raise RuntimeError('cache changed before deletion '+str(f))
   f.unlink()
  p.rmdir()
 if any(p.is_dir() for u in UNITS for p in (O/u).rglob('__pycache__')):raise RuntimeError('cache remains')
 result=dict(unit='F0.3.E5',plan_path=str(PLAN),plan_sha256=h(PLAN),completed_utc=datetime.now(timezone.utc).isoformat(),directories_removed=len(rows),files_removed=sum(len(x['files']) for x in rows),bytes_removed=sum(y['bytes'] for x in rows for y in x['files']),all_targets_absent=True,no_data_or_gate=True)
 wx(RESULT,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()