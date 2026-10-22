"""Install reviewed immutable memory epoch and switch new-process default last."""
from pathlib import Path
import argparse,hashlib,json,os,sys
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True;sys.path.insert(0,str(B))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.safe_files import replace_bytes,save_json,utc_now
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def claim(path,data):
 raw=json.dumps(data,ensure_ascii=False,indent=2).encode()
 with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert path.read_bytes()==raw

def main(review_path,decision_path):
 manifest_raw=(W/'REVIEW_MANIFEST.json').read_bytes();mh=sha(manifest_raw)
 review_raw=Path(review_path).read_bytes();review=json.loads(review_raw)
 decision_raw=Path(decision_path).read_bytes();decision=json.loads(decision_raw)
 assert review['status']=='PASS' and review['review_manifest_sha256']==mh
 assert decision['allow_local_install'] is True and decision['review_manifest_sha256']==mh
 assert decision['independent_review_sha256']==sha(review_raw)
 for e in json.loads(manifest_raw)['members']:assert pin(e['path'])==e,'Reviewed artifact changed'
 audit=decision['science_audit'];assert pin(audit['path'])==audit
 plan=json.loads((W/'INSTALL_PLAN.json').read_bytes());target=Path(plan['new_memory_root'])
 expectedroot=B/'state/canonical_memory/releases'/('v389_'+plan['generation'][:16])
 assert target==expectedroot and not target.exists(),'Existing epoch: recover rather than repeat'
 assert Path(cm.__file__).resolve()==B/'iald_orchestrator/canonical_memory.py'
 for name in ['module_baseline','historical_catalog','old_manifest','old_index']:assert pin(plan[name]['path'])==plan[name]
 module=Path(plan['module_baseline']['path'])
 staged=json.loads((W/'manifest_install.json').read_bytes());sr=Path(staged['snapshot_root'])
 assert sr==target/'snapshots'/target.name
 allowed={sr/d['name'] for d in staged['documents']}|{sr/'SEALED_SNAPSHOT.json',target/'index.sqlite3',target/'manifest.json',module}
 assert len(plan['files'])==17 and {Path(e['destination']) for e in plan['files']}==allowed
 assert plan['files'][-1]['destination']==str(module)
 data={};old_module=module.read_bytes()
 for e in plan['files']:
  src,dst=Path(e['source']),Path(e['destination'])
  assert src.resolve().is_relative_to(W) and (dst==module or dst.resolve().is_relative_to(target))
  assert not src.is_symlink() and not dst.is_symlink()
  raw=src.read_bytes();old=dst.read_bytes() if dst.exists() else None
  assert sha(raw)==e['sha256'] and len(raw)==e['bytes']
  assert (sha(old) if old is not None else None)==e['baseline_sha256'],'Baseline mismatch'
  data[dst]=raw
 # Exclusive, durable reservation: an uncertain or interrupted attempt is never repeated.
 claim(W/'INSTALL_STARTED.json',{'at':utc_now(),'status':'STARTED_NO_AUTOMATIC_RETRY','review_manifest_sha256':mh,'decision_sha256':sha(decision_raw)})
 switched=False
 try:
  for e in plan['files'][:-1]:
   dst=Path(e['destination']);assert not dst.exists(),'Concurrent epoch file'
   replace_bytes(dst,data[dst]);assert dst.read_bytes()==data[dst]
  m,fresh=cm.load(target,refresh=False)
  assert m['generation']==plan['generation'] and fresh=='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED'
  # Verify both roots before publishing the path for future processes.
  for name in ['historical_catalog','old_manifest','old_index']:assert pin(plan[name]['path'])==plan[name]
  assert module.read_bytes()==old_module,'Concurrent module edit'
  replace_bytes(module,data[module]);switched=True
  assert module.read_bytes()==data[module]
 except BaseException as exc:
  rollback=False
  if switched and module.read_bytes()==data[module]:replace_bytes(module,old_module);rollback=True
  save_json(W/'INSTALL_FAILURE.json',{'at':utc_now(),'error_type':type(exc).__name__,'module_restored':rollback,'new_epoch_retained':str(target),'retry_allowed':False})
  raise
 save_json(W/'INSTALL_RECEIPT.json',{'at':utc_now(),'status':'INSTALLED_NEW_EPOCH_NEW_PROCESS_VERIFICATION_REQUIRED','release':'v389','generation':m['generation'],'chunks':m['chunks'],'files':[pin(dst) for dst in data],'prior_root':plan['old_memory_root'],'prior_root_unchanged':all(pin(plan[k]['path'])==plan[k] for k in ['old_index','old_manifest']),'new_process_root':str(target),'module_sha256':sha(data[module]),'provider_calls':0,'scientific_execution':False,'jobs_or_constraints_written':False,'resident_processes_reloaded':False})
 print(json.dumps({'status':'INSTALLED_NEW_EPOCH_NEW_PROCESS_VERIFICATION_REQUIRED','generation':m['generation'],'files':len(data)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--review',required=True);p.add_argument('--decision',required=True);a=p.parse_args();main(a.review,a.decision)
