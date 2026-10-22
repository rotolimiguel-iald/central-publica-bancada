"""Preregister and measure the corrected finite action incidence catalog."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
from incidence_decorated_engine import *
HERE=Path(__file__).resolve().parent;DEST=HERE/'incidence_decorated';DEST.mkdir(exist_ok=True)
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    scope='Connected unicircular action types E1..6, original four vertex classes; no Ward insertion inferred',
    engine_sha256=hashlib.sha256((HERE/'incidence_decorated_engine.py').read_bytes()).hexdigest(),
    cutoff_and_EOM_insertions='NOT_IN_CATALOG',cpu_budget_seconds=300,
    quantum_anomaly_computed=False))
cpu=time.process_time();wall=time.perf_counter();all_rows=[];families_out=[]
for E in range(1,7):
    for vs in families(E):
        rows=enumerate_family(vs);all_rows.extend(rows)
        families_out.append(dict(E=E,valences=vs,count=len(rows)))
        print(json.dumps(families_out[-1]),flush=True)
        if time.process_time()-cpu>300:
            new(DEST/'PARTIAL_BUDGET.json',dict(families=families_out,rows=all_rows,cpu_seconds=time.process_time()-cpu))
            raise RuntimeError('Local inventory CPU budget reached; preserve partial result')
assert len(families_out)==29
first=[r for r in all_rows if r['E']==1]
assert {tuple(r['classes']) for r in first}=={('METRIC',),('GHOST',)}
assert any(r['classes']==('GHOST','GHOST') and sorted(e[0] for e in r['edges'])==['G','G'] for r in all_rows)
negatives=[]
for edges in [[],[('INVALID',0,0)],[('G',0,7)],[('G',0,0)],[('A',0,0)]]:
    try:validate((3,),('METRIC',),edges)
    except ValueError:negatives.append(str(edges))
    else:raise AssertionError('invalid decorated graph accepted')
result=dict(at=datetime.now(timezone.utc).isoformat(),families=families_out,types=len(all_rows),
    by_E={str(E):sum(r['E']==E for r in all_rows) for E in range(1,7)},
    contains_class={c:sum(c in r['classes'] for r in all_rows) for c in ['METRIC','GHOST','HDAG','CDAG']},
    negatives=negatives,all_ghost_zero=all(r['ghost']==0 for r in all_rows),
    action_catalog_complete_for_stated_four_signatures=True,Ward_catalog_complete=False,
    cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall)
new(DEST/'inventory.json',all_rows);new(DEST/'results.json',result)
print(json.dumps(result),flush=True)
