"""Fresh-process, offline verification of the v391 release."""
from pathlib import Path
import json,os,sqlite3,sys
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True;sys.path.insert(0,str(B))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.safe_files import save_json,utc_now
p=json.loads((W/'PREPARATION_V391.json').read_bytes());target=Path(p['target'])
m,fresh=cm.load(target,refresh=False)
assert m['generation']==p['generation'] and fresh=='SEALED_SNAPSHOT_ALL_SOURCE_HASHES_VERIFIED'
checks=[]
for d in m['documents']:
 assert cm.digest(Path(d['path']).read_bytes())==d['sha256']
checks.append('all_13_source_byte_hashes')
with sqlite3.connect((target/'index.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
 assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert db.execute('SELECT COUNT(*) FROM passages').fetchone()[0]==m['chunks']
 # Every chunk and line range is reproduced from the immutable source bytes.
 for d in m['documents']:
  expected=list(cm.chunks(Path(d['path']).read_bytes().decode('utf-8-sig')))
  actual=[(int(a),int(b),s) for a,b,s in db.execute('SELECT first_line,last_line,body FROM passages WHERE document=? ORDER BY rowid',(d['name'],))]
  assert actual==expected,d['name']
 checks.append('entire_fts_index_matches_all_source_chunks_and_lines')
 hit=db.execute("SELECT count(*) FROM passages WHERE passages MATCH ?",('"estatuto_da_prova_v391"',)).fetchone()[0]
 assert hit>0
 checks.append('new_core_record_indexed')
receipts={}
for mode in ('standard','maximum','deepseek_maximum'):
 packet=cm.prepare('estatuto_da_prova_v391 PROVADA validade creditacao COMPUTED',target,
  allowed_sources=['um.py','um_absoluto.json','um_absoluto_selo.json','um_absoluto_forma_canonica.md'],
  mode=mode,max_chars=24000)
 assert packet['receipt']['generation']==p['generation']
 assert 'estatuto_da_prova_v391' in packet['prompt'],mode
 assert packet['receipt']['packet_sha256']==cm.digest(packet['prompt'].encode())
 receipts[mode]=packet['receipt']
 checks.append('retrieval_'+mode)
old,_=cm.load(cm.RELEASES/p['previous_active']['epoch'],refresh=False)
assert old['generation']==p['previous_active']['generation']
checks.append('v389_still_readable_by_version')
assert cm.digest((target/'manifest.json').read_bytes())==p['manifest']['sha256']
save_json(W/'FRESH_PROCESS_VERIFICATION.json',{'status':'PASS','at':utc_now(),'pid':os.getpid(),
 'generation':m['generation'],'release':'v391','freshness':fresh,'checks':checks,'retrieval':receipts,'provider_calls':0,
 'source_execution':False,'module_sha256':cm.digest(Path(cm.__file__).read_bytes()),'script_sha256':cm.digest(Path(__file__).read_bytes())})
print(json.dumps({'status':'PASS','checks':checks,'pid':os.getpid(),'generation':m['generation']}))

