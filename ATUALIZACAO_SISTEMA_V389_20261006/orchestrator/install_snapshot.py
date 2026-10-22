"""Install only independently reviewed v389 local snapshot; no remote calls or science."""
from pathlib import Path
from contextlib import closing
import argparse,hashlib,json,sqlite3,sys
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(B))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.safe_files import replace_bytes,save_json,utc_now
sha=lambda x:hashlib.sha256(x).hexdigest()
def pin(p):
 p=Path(p);x=p.read_bytes();return {'path':str(p),'bytes':len(x),'sha256':sha(x)}
def queue():
 with closing(sqlite3.connect((B/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True)) as db:
  db.execute('PRAGMA query_only=ON')
  running=db.execute("SELECT COUNT(*) FROM attempts WHERE status='running' AND finished_at IS NULL").fetchone()[0]
  identities={t:sha(json.dumps(db.execute('SELECT * FROM '+t+' ORDER BY id').fetchall(),ensure_ascii=False).encode()) for t in ['tasks','coordination_jobs']}
  return {'running_attempts':running,'identities':identities}
def main(review_path,decision_path):
 assert not (W/'INSTALL_STARTED.json').exists(),'Prior attempt: recover receipt; no automatic repeat.'
 manifest_bytes=(W/'REVIEW_MANIFEST.json').read_bytes();mh=sha(manifest_bytes)
 review=json.loads(Path(review_path).read_bytes());decision=json.loads(Path(decision_path).read_bytes())
 assert review['status']=='PASS' and review['review_manifest_sha256']==mh
 assert decision['allow_local_install'] is True and decision['review_manifest_sha256']==mh
 assert decision['independent_review_sha256']==sha(Path(review_path).read_bytes())
 for e in json.loads(manifest_bytes)['members']:assert pin(e['path'])==e,'Reviewed member changed'
 plan=json.loads((W/'INSTALL_PLAN.json').read_bytes());prep=json.loads((W/'PREPARATION.json').read_bytes())
 for key in ['module_baseline','catalog_baseline']:assert pin(plan[key]['path'])==plan[key],'Module/catalog changed'
 audit=decision['science_audit'];assert pin(audit['path'])==audit,'Science audit changed'
 memory=B/'state/canonical_memory';target=Path(plan['snapshot_target'])
 assert target==memory/'snapshots'/('v389_'+plan['generation'][:16]) and not target.exists()
 q0=queue();assert q0['running_attempts']==0,'Active execution; postpone local swap'
 old={};new={};ordered=[]
 expected={target/d['name'] for d in json.loads((W/'manifest_install.json').read_bytes())['documents']}
 expected|={target/'SEALED_SNAPSHOT.json',memory/'index.sqlite3',memory/'manifest.json'}
 assert len(plan['files'])==16 and {Path(e['destination']) for e in plan['files']}==expected
 assert [e['destination'] for e in plan['files']][-2:]==[str(memory/'index.sqlite3'),str(memory/'manifest.json')]
 for e in plan['files']:
  src,dst=Path(e['source']),Path(e['destination'])
  assert src.resolve().is_relative_to(W) and dst.resolve().is_relative_to(memory)
  assert not src.is_symlink() and not dst.is_symlink()
  data=src.read_bytes();before=dst.read_bytes() if dst.exists() else None
  assert sha(data)==e['sha256'] and len(data)==e['bytes']
  assert (sha(before) if before is not None else None)==e['baseline_sha256'],'CAS mismatch'
  old[dst]=before;new[dst]=data;ordered.append(dst)
 assert queue()==q0,'Queue changed before claim'
 save_json(W/'INSTALL_STARTED.json',{'at':utc_now(),'status':'STARTED_NO_AUTOMATIC_RETRY','review_manifest_sha256':mh,'decision_sha256':sha(Path(decision_path).read_bytes())})
 written=[]
 try:
  for dst in ordered:
   assert (dst.read_bytes() if dst.exists() else None)==old[dst],'Concurrent local edit'
   written.append(dst);replace_bytes(dst,new[dst]);assert dst.read_bytes()==new[dst]
  m,fresh=cm.load(refresh=False)
  assert m['generation']==plan['generation'] and fresh=='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED'
  for key in ['module_baseline','catalog_baseline']:assert pin(plan[key]['path'])==plan[key]
 except BaseException as exc:
  restored=[];unresolved=[]
  for dst in reversed(written):
   if old[dst] is not None:
    if dst.exists() and dst.read_bytes()==new[dst]:replace_bytes(dst,old[dst]);restored.append(str(dst))
    else:unresolved.append(str(dst))
  save_json(W/'INSTALL_FAILURE.json',{'at':utc_now(),'error_type':type(exc).__name__,'restored_previous_files':restored,'concurrent_or_uncertain_files':unresolved,'new_snapshot_files_retained_for_audit':[str(d) for d in written if old[d] is None],'retry_allowed':False})
  raise
 q1=queue()
 save_json(W/'INSTALL_RECEIPT.json',{'at':utc_now(),'status':'INSTALLED_LOCAL_SNAPSHOT_NEW_PROCESS_CHECK_REQUIRED','generation':m['generation'],'chunks':m['chunks'],'freshness':fresh,'files':[pin(d) for d in ordered],'queue_before':q0,'queue_after':q1,'queue_unchanged_observed':q0==q1,'old_request_constraints_mutated':False,'remote_calls':0,'scientific_execution':False,'code_changed':False,'hot_reload_claimed':False,'old_version_retained':True})
 print(json.dumps({'status':'INSTALLED_LOCAL_SNAPSHOT_NEW_PROCESS_CHECK_REQUIRED','generation':m['generation'],'files':len(ordered),'queue_unchanged_observed':q0==q1}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--review',required=True);p.add_argument('--decision',required=True);a=p.parse_args();main(a.review,a.decision)
