"""Prepare a new immutable v391 memory release, reusing the existing builder."""
from pathlib import Path
import copy,hashlib,json,os,sqlite3,subprocess,sys
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(B))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.program_controls import require_claim
from iald_orchestrator.safe_files import replace_bytes,save_json,utc_now
def pin(p):
 p=Path(p); raw=p.read_bytes()
 return {'path':str(p),'bytes':len(raw),'sha256':cm.digest(raw)}
def main():
 require_claim('F0.3','codex-coordenadora')
 assert not (W/'PREPARATION_V391.json').exists(), 'Recover existing preparation'
 lookup=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F0.3'],capture_output=True,check=True)
 replace_bytes(W/'NOS_VIVO_V391.txt',lookup.stdout)
 active_raw=cm.ACTIVE.read_bytes();old=json.loads(active_raw)
 old_manifest,old_fresh=cm.load(refresh=False)
 catalog=json.loads(cm.CATALOG.read_bytes())
 entries=[e for e in catalog['files'] if Path(e['source']).suffix.lower()!='.pdf']
 assert len(entries)==13 and {Path(e['source']).name for e in entries}==cm.SNAPSHOT_NAMES
 source_data={};sources=[]
 for e in entries:
  p=Path(e['source'])
  assert p.is_file() and not p.is_symlink()
  assert any(p.resolve().is_relative_to(r) for r in [Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'),Path(r'C:\IALD\Artigo\the_boundary')])
  raw=p.read_bytes();source_data[p.name]=raw
  sources.append({'path':str(p),'bytes':len(raw),'sha256':cm.digest(raw),'mtime_ns':p.stat().st_mtime_ns})
 seal=json.loads(source_data['um_absoluto_selo.json'])
 proof=json.loads(source_data['tgl_kernel_proof_manifest.json'])
 result=json.loads(source_data['um_absoluto.json']);statute=result['core']['estatuto_da_prova_v391']
 assert seal['um_version']=='v391' and seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
 assert seal['formal_source_hash']==proof['formal_source_hash']
 sealed_checked=[]
 for name,raw in source_data.items():
  if name in seal['sha256']:
   assert cm.digest(raw)==seal['sha256'][name], name
   sealed_checked.append(name)
 assert statute['all_verified'] and statute['does_not_gate_core']
 assert statute['certificacao']['um_py_sha256_lido_de_si']==cm.digest(source_data['um.py'])
 assert statute['prova_3_gpu']['estatuto'].startswith('[COMPUTED]')
 generation=cm.digest(json.dumps([(Path(x['path']).name,x['sha256']) for x in sources],ensure_ascii=False).encode())
 epoch='v391_'+generation[:16];target=cm.RELEASES/epoch;root=target/'snapshots'/epoch
 assert not target.exists(),'Existing release: recover, never rebuild immutable release'
 save_json(W/'BUILD_INTENT_V391.json',{'at':utc_now(),'epoch':epoch,'generation':generation,'target':str(target),'sources':sources,'baseline_active':old})
 staged=copy.deepcopy(catalog)
 for e in staged['files']:
  src=Path(e['source'])
  if src.suffix.lower()=='.pdf':continue
  dst=root/src.name;replace_bytes(dst,source_data[src.name])
  stamp=next(s['mtime_ns'] for s in sources if s['path']==str(src))
  os.utime(dst,ns=(stamp,stamp));e['source']=str(dst)
 save_json(W/'CATALOG_V391.json',staged)
 m=cm.build(target,W/'CATALOG_V391.json')
 assert m['generation']==generation
 binding={'schema':1,'source_mode':cm.SNAPSHOT_MODE,'release':'v391','generation':generation,'index_sha256':m['index_sha256'],
 'documents':[{k:d[k] for k in ('name','sha256','bytes')} for d in m['documents']],'formal_source_hash':seal['formal_source_hash']}
 save_json(root/'SEALED_SNAPSHOT.json',binding)
 m.update(source_mode=cm.SNAPSHOT_MODE,snapshot_root=str(root),snapshot_manifest_sha256=cm.digest((root/'SEALED_SNAPSHOT.json').read_bytes()))
 save_json(target/'manifest.json',m)
 loaded,fresh=cm.load(target,refresh=False)
 assert fresh=='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED'
 for s in sources: assert pin(s['path'])['sha256']==s['sha256'],'Original changed during preparation'
 assert cm.ACTIVE.read_bytes()==active_raw
 prior,_=cm.load(cm.RELEASES/old['epoch'],refresh=False)
 assert prior['generation']==old['generation']
 save_json(W/'ESTATUTO_V391_LIDO.json',{'source':pin(root/'um_absoluto.json'),'record_path':'core.estatuto_da_prova_v391','record':statute,
   'scope':'Transcricao de registro existente, sem nova execucao cientifica.'})
 report={'status':'PREPARED_INACTIVE','unit':'F0.3','at':utc_now(),'release':'v391','epoch':epoch,'generation':generation,
 'target':str(target),'manifest':pin(target/'manifest.json'),'chunks':m['chunks'],'documents':len(m['documents']),
 'sources':sources,'source_seal_pins_checked':sealed_checked,'freshness':fresh,'previous_active':old,
 'reused':['canonical_memory.build','sealed snapshot verifier','F9.2 ACTIVE pointer','F9.9 Nos packet'],
 'provider_calls':0,'scientific_execution':False,'originals_modified':False,'gate_modified':False,'pending_approvals_resolved':False,
 'catalog_allowlist':pin(cm.CATALOG),'canonical_module':pin(Path(cm.__file__)),'script':pin(__file__)}
 save_json(W/'PREPARATION_V391.json',report)
 print(json.dumps({k:report[k] for k in ('status','release','epoch','generation','documents','chunks','freshness')}))
if __name__=='__main__':main()

