"""Isolate only the pure single-event table loop and mutate in-memory inputs."""
import ast,copy,json,hashlib,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def get(p):return json.loads((R/p).read_bytes())
def need(ok,msg):
    if not ok:raise ValueError(msg)
source=R/'refeito/summarize_f2_tables_013bis.py';tree=ast.parse(source.read_text(encoding='utf-8'))
loops=[n for n in tree.body if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [v.id for v in n.target.elts]==['name','event']]
need(len(loops)==1,'Unrecognized loop')
fragment=ast.Module(body=loops,type_ignores=[]);code=compile(ast.fix_missing_locations(fragment),str(source),'exec',optimize=1)
cat=get('C4_CATALOG_220.json');gw=next(e for e in cat['rows'] if e['event']=='GW250114_082203');py=get('C4_PYRING.json')
readings=[r['reading'] for r in cat['catalog']]+['R-PROP','R-RAIZ-COHERENT']
def sigma(event):
    rb=next(r for r in event['rows'] if r['reading']=='R-B');return abs(rb['shift_05_50_95'][1])/rb['correction_over_sigma']
def run(data):
    env=dict(gw=gw,py=data,readings=readings,sigma=sigma,statistics=statistics,rows=[])
    exec(code,env);return env['rows']
positive=run(py);mut=copy.deepcopy(py);mut['rows']=[r for r in mut['rows'] if r['reading']!='R-MOD'];rows=run(mut)
before=next(r for r in positive if r['dataset']=='GW250114_pyRing' and r['reading']=='R-MOD')
after=next(r for r in rows if r['dataset']=='GW250114_pyRing' and r['reading']=='R-MOD')
need(len(rows)==20 and after['lnB']==0 and after['analytic'],'Probe did not reproduce fallback')
result=dict(status='MISSING_COMPUTED_READING_SILENTLY_BECOMES_ANALYTIC_ZERO',builder_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),removed='C4_PYRING.rows[R-MOD] in memory only',positive=before,mutated=after,loop_output_rows=len(rows),top_level_count_would_still_be=40+len(rows),no_production_executed_or_written=True)
p=R/'bis/c1_review/table_missing_row_results.json';need(not p.exists(),'Output exists');raw=(json.dumps(result,indent=2)+'\n').encode();tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
need(tmp.read_bytes()==raw,'Write differs');tmp.rename(p)
print(json.dumps(dict(status=result['status'],original_lnB=before['lnB'],mutated_lnB=after['lnB'],count=40+len(rows))))
