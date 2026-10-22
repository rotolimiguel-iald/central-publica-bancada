"""Verify v388 retrieval and update reviewed provenance; never dispatch jobs."""
from pathlib import Path
from contextlib import closing
import ast,copy,hashlib,json,sqlite3,sys
from datetime import datetime,timezone
W=Path(__file__).resolve().parent
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.dont_write_bytecode=True
sys.path.insert(0,str(B))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.safe_files import save_json
sha=lambda data:hashlib.sha256(data).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def queue():
 with closing(sqlite3.connect((B/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True)) as db:
  db.execute('PRAGMA query_only=ON')
  out={}
  for table,key in [('tasks','status'),('coordination_jobs','stage')]:
   out[table]={'counts':db.execute(f'SELECT {key},count(*) FROM {table} GROUP BY {key}').fetchall(),
    'identity_sha256':sha(json.dumps(db.execute(f'SELECT * FROM {table} ORDER BY id').fetchall(),ensure_ascii=False).encode())}
  out['nonterminal']=db.execute("SELECT id,request_id,stage,execution_constraints FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled')").fetchall()
  out['running_attempts']=db.execute("SELECT COUNT(*) FROM attempts WHERE status='running' AND finished_at IS NULL").fetchone()[0]
  return out
oldp=(B/'provenance.json').read_bytes();provenance=json.loads(oldp)
source=Path(provenance['sources'][0]['path']);old=source.with_name(source.name+'.bak_formula_20261001_123708')
assert sha(old.read_bytes())==provenance['sources'][0]['sha256']
a=ast.parse(old.read_bytes());b=ast.parse(source.read_bytes())
removed=[]
class RemoveAddition(ast.NodeTransformer):
 def visit_FunctionDef(self,node):
  if node.name=='_formula_completa':removed.append('function');return None
  return self.generic_visit(node)
 def visit_Assign(self,node):
  if ast.unparse(node)=="results['formula_completa'] = _formula_completa()":removed.append('call');return None
  return self.generic_visit(node)
b=RemoveAddition().visit(b)
assert removed==['function','call'] and ast.dump(a)==ast.dump(b),'Unreviewed source change'
for row in provenance['sources'][1:]:assert pin(Path(row['path']))['sha256']==row['sha256']
qbefore=queue();assert qbefore['running_attempts']==0
m,freshness=cm.load(refresh=False)
checks=[dict(pin(Path(d['path'])),matches=pin(Path(d['path']))['sha256']==d['sha256']) for d in m['documents']]
assert all(d['matches'] for d in checks)
seal=json.loads(Path(next(d['path'] for d in m['documents'] if d['name']=='um_absoluto_selo.json')).read_bytes())
assert seal['um_version']=='v388'
program=next(d for d in m['documents'] if d['name']=='um.py')
assert program['sha256']==seal['sha256']['um.py']
assert sha((cm.MEMORY/'index.sqlite3').read_bytes())==m['index_sha256']
with closing(sqlite3.connect((cm.MEMORY/'index.sqlite3').as_uri()+'?mode=ro',uri=True)) as db:
 assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
 assert db.execute('SELECT COUNT(*) FROM passages').fetchone()[0]==m['chunks']
receipts={}
for mode in ['standard','maximum','deepseek_maximum']:
 packet=cm.prepare('beta_runs_bounded_below_v388 hubble_ratio_opening_v388 TheCouplingRunsBoundedBelow beta piso inferior Fase 9 INCONCLUSIVE_SYSTEMATICS',mode=mode,allowed_sources=['um.py','um_absoluto_selo.json','um_absoluto_forma_canonica.md'])
 assert packet['receipt']['generation']==m['generation']
 assert 'v388' in packet['prompt'] and 'INCONCLUSIVE_SYSTEMATICS' in packet['prompt']
 receipts[mode]=packet['receipt']
newp=copy.deepcopy(provenance);newp['sources'][0]['sha256']=sha(source.read_bytes())
newp['source_review']={'at':datetime.now(timezone.utc).isoformat(),'scope':'Local source pin reviewed after operator request to update whole system to v388; unchanged policy, queue and scientific gates.',
 'evidence':str(W/'delivery.json'),'previous_manifest_sha256':sha(oldp),'difference':'AST identical after removing only new _formula_completa function and its result assignment. Runner not imported/executed.'}
assert (B/'provenance.json').read_bytes()==oldp
save_json(W/'provenance.before.json',provenance)
save_json(B/'provenance.json',newp)
for row in newp['sources']:assert pin(Path(row['path']))['sha256']==row['sha256']
qafter=queue();assert qbefore==qafter,'Queue changed independently; investigate before claiming unchanged'
report={'status':'V388_COMMON_MEMORY_VERIFIED_AND_SOURCE_ANCHOR_UPDATED','at':datetime.now(timezone.utc).isoformat(),
 'program':pin(Path(program['path'])),'memory_generation':m['generation'],'documents':checks,'chunks':m['chunks'],
 'memory_cache_rebuilt':False,'memory_cache_reason':'Already built from v388; all 13 source hashes and index integrity freshly verified.',
 'catalog_upload_snapshot':pin(cm.CATALOG),'chatgpt_uploaded_files_updated':False,
 'uploaded_snapshot_reason':'Historic v369 attachment manifest preserved. Optional Work receives current canonical_memory.prompt per transport; no cloud upload claimed.',
 'provenance_before_sha256':sha(oldp),'provenance_after':pin(B/'provenance.json'),
 'anchor_review':{'prior':pin(old),'current':pin(source),'remaining_ast_equal':True,'removed_additions':removed},
 'retrieval':receipts,'queue':qafter,'queue_unchanged':True,'old_generation_constraints_preserved':True,
 'remote_calls':0,'scientific_execution':False,'source_originals_modified':False}
save_json(W/'delivery.json',report)
print(json.dumps({k:report[k] for k in ['status','memory_generation','chunks','queue_unchanged','remote_calls']}))
