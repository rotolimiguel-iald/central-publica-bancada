"""Prepare an isolated v389 shared-memory snapshot. No dispatch or installation."""
from pathlib import Path
from contextlib import closing
import copy,hashlib,json,os,sqlite3,sys
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(B))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.safe_files import replace_bytes,save_json,utc_now
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def main():
 assert not (W/'PREPARATION.json').exists(),'Existing preparation: recover identity, do not repeat.'
 memory=B/'state/canonical_memory'
 baseline={name:pin(memory/name) for name in ['index.sqlite3','manifest.json']}
 module=pin(Path(cm.__file__));catalog=pin(cm.CATALOG)
 prior,freshness=cm.load(refresh=False)
 assert freshness=='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED'
 admitted=json.loads(cm.CATALOG.read_bytes())
 files=[e for e in admitted['files'] if Path(e['source']).suffix.lower()!='.pdf']
 assert len(files)==13 and {Path(e['source']).name for e in files}==cm.SNAPSHOT_NAMES
 originals=[];raws={}
 for e in files:
  p=Path(e['source']);assert p.is_file() and not p.is_symlink()
  b=p.read_bytes();raws[p.name]=b;originals.append(dict(pin(p),mtime_ns=p.stat().st_mtime_ns))
 seal=json.loads(raws['um_absoluto_selo.json']);proof=json.loads(raws['tgl_kernel_proof_manifest.json'])
 assert seal['um_version']=='v389' and seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
 assert seal['formal_source_hash']==proof['formal_source_hash']
 for name in ['um.py','um_absoluto.json','tgl_kernel_proof_manifest.json']:
  assert sha(raws[name])==seal['sha256'][name]
 generation=sha(json.dumps([(Path(e['path']).name,e['sha256']) for e in originals],ensure_ascii=False).encode())
 staged_memory=W/'memory_stage';root=staged_memory/'snapshots'/('v389_'+generation[:16])
 assert not root.exists()
 new_catalog=copy.deepcopy(admitted)
 for e in new_catalog['files']:
  src=Path(e['source'])
  if src.suffix.lower()=='.pdf':continue
  p=root/src.name;replace_bytes(p,raws[src.name]);meta=next(q for q in originals if q['path']==str(src));os.utime(p,ns=(meta['mtime_ns'],meta['mtime_ns']));e['source']=str(p)
 save_json(W/'catalog_staged.json',new_catalog)
 m=cm.build(staged_memory,W/'catalog_staged.json')
 assert m['generation']==generation
 binding={'schema':1,'source_mode':cm.SNAPSHOT_MODE,'release':'v389','generation':generation,'index_sha256':m['index_sha256'],'documents':[{k:d[k] for k in ['name','sha256','bytes']} for d in m['documents']],'formal_source_hash':seal['formal_source_hash']}
 save_json(root/'SEALED_SNAPSHOT.json',binding)
 m.update({'source_mode':cm.SNAPSHOT_MODE,'snapshot_root':str(root),'snapshot_manifest_sha256':sha((root/'SEALED_SNAPSHOT.json').read_bytes())})
 save_json(staged_memory/'manifest.json',m)
 loaded,fresh=cm.load(staged_memory,refresh=False)
 assert fresh=='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED'
 with closing(sqlite3.connect((staged_memory/'index.sqlite3').as_uri()+'?mode=ro',uri=True)) as db:
  assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
  assert db.execute('SELECT COUNT(*) FROM passages').fetchone()[0]==m['chunks']
 retrieval={}
 for mode in ['standard','maximum','deepseek_maximum']:
  packet=cm.prepare('text_label_errata_v389 CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET axioma POSTO ledger 1025',staged_memory,mode=mode,allowed_sources=['um.py','um_absoluto_selo.json','um_absoluto_forma_canonica.md'])
  assert packet['receipt']['generation']==generation and 'v389' in packet['prompt']
  retrieval[mode]=packet['receipt']
 target=memory/'snapshots'/root.name
 installed=copy.deepcopy(m);installed['snapshot_root']=str(target)
 for d in installed['documents']:d['path']=str(target/d['name'])
 save_json(W/'manifest_install.json',installed)
 planned=[]
 for p in list(root.iterdir())+[staged_memory/'index.sqlite3',W/'manifest_install.json']:
  dest=target/p.name if p.parent==root else memory/('manifest.json' if p.name=='manifest_install.json' else p.name)
  planned.append({'source':str(p),'destination':str(dest),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'baseline_sha256':sha(dest.read_bytes()) if dest.exists() else None})
 assert len(planned)==16
 for e in originals:assert pin(e['path'])['sha256']==e['sha256'],'Source changed during staging'
 for name,e in baseline.items():assert pin(memory/name)==e,'Installed memory changed during staging'
 report={'status':'PREPARED_NOT_INSTALLED','at':utc_now(),'release':'v389','generation':generation,'chunks':m['chunks'],'snapshot_target':str(target),'sources':originals,'catalog_baseline':catalog,'module_unchanged':module,'installed_baselines':baseline,'prior_generation':prior['generation'],'stage_freshness':fresh,'retrieval':retrieval,'providers_called':0,'source_execution':False,'source_originals_modified':False,'old_request_constraints_changed':False,'existing_mcp_hot_reload_claimed':False}
 save_json(W/'INSTALL_PLAN.json',{'generation':generation,'snapshot_target':str(target),'files':planned,'module_baseline':module,'catalog_baseline':catalog,'swap_order':'13 source copies + descriptor; index; manifest last. Per-file atomicity only. Failure between index and manifest fails closed; backups permit exact rollback.'})
 save_json(W/'PREPARATION.json',report)
 print(json.dumps({k:report[k] for k in ['status','release','generation','chunks','stage_freshness','providers_called']}))
if __name__=='__main__':main()
