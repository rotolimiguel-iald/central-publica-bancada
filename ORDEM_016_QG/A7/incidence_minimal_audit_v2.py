# Supersedes output serialization only; tuple keys converted to records.
# Predecessor SHA256 9ac656013289aa9d4ddaf80494d85db22249db6e98238a4792e710f45f36d012
"""Audit the received Kimi enumerator with small exact counterexamples only."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
import ast,hashlib,json,re,time,uuid
HERE=Path(__file__).resolve().parent;DEST=HERE/'incidence_minimal_audit_v2';DEST.mkdir(exist_ok=True)
src=HERE/'received_reviews/04dae5a6-b78a-4f0f-83c7-4cb1b6c3c0be.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj,raw=False):
    b=obj if raw else json.dumps(obj,ensure_ascii=False,indent=2).encode()
    assert not p.exists();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
code=re.findall(r'```python\s*\n(.*?)\n```',src.read_text('utf-8'),re.S)
assert len(code)==1
tree=ast.parse(code[0])
for node in ast.walk(tree):
    if isinstance(node,(ast.Import,ast.ImportFrom)):
        assert isinstance(node,ast.ImportFrom) and node.module in ['itertools','collections']
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
        assert node.func.id not in ['open','eval','exec','compile','__import__']
new(DEST/'received_code.py',code[0].encode(),raw=True)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(src),extracted_code_sha256=sha(DEST/'received_code.py'),
    scope='Emax1 inventory, typed validator adversaries, monotonicity comparison with unpruned oracle',
    no_full_enumeration=True,no_remote_calls=True))
cpu=time.process_time();wall=time.perf_counter();ns={'__name__':'received_incidence_under_local_audit'}
exec(compile(tree,str(DEST/'received_code.py'),'exec'),ns)
inv=ns['inventario'](emax=1)
classes={c for row in inv for c in row['classes']}
assert classes=={'METRIC_ORD'}
# At V=1 the ghost trilinear admits a ghost tadpole, leaving one external H.
mat=((1,),);slots=[('CB','C','H')]
direct=ns['atribuicoes_linhas'](slots,mat)
assert any(lines==[('G',0,0)] for lines,rest in direct)
inv_af=ns['inventario'](emax=1,permitir_antifield_em_linha=True)
assert len(inv_af)==len(inv)
validate=ns['valida_tipo']
# These are intentionally inconsistent and should not pass a genuine graph validator.
assert validate(1,mat,[],{'H':1},99) is True
assert validate(1,mat,[('INVALID',7,9)],{'H':1},99) is True
all_zero_ghost=all(sum(ns['GHOST_NUM'][f] for f in ns['slots_da_classe'](name,3))==0
                   for name in ns['CLASSES'])
assert all_zero_ghost
assert ns['certificado_e_aut'](mat,((3,'METRIC_ORD'),))[0]==ns['certificado_e_aut'](mat,((3,'GHOST_ORD'),))[0]
# Test the purported moving-index problem independently of the actual class collision.
# Edge option resources are disjoint for the two vertices in this catalog.
def no_monotone(slots,mat):
    cont={}
    for i,fs in enumerate(slots):
        for f in fs:
            if f in ['H','C','CB']:cont[i,f]=cont.get((i,f),0)+1
    groups=[(i,j) for i in range(len(mat)) for j in range(i,len(mat)) for _ in range(mat[i][j])]
    out=set()
    def rec(k,remaining,ops):
        if k==len(groups):out.add(tuple(sorted(ops)));return
        i,j=groups[k]
        for op in ns['_opcoes_linha'](i,j,remaining):
            rec(k+1,ns['_consome'](remaining,op),ops+[op])
    rec(0,cont,[])
    return out
mono_cases=0
for counts in product(range(3),repeat=6):
    slots=[tuple(f for f,n in zip(['H','C','CB'],counts[3*i:3*i+3]) for _ in range(n)) for i in range(2)]
    for m in range(1,4):
        mat2=((0,m),(m,0))
        actual={tuple(sorted(lines)) for lines,_ in ns['atribuicoes_linhas'](slots,mat2)}
        assert actual==no_monotone(slots,mat2),(counts,m)
        mono_cases+=1
# Do not claim the coordinator's moving-index criticism is established: it did
# not reproduce here; independent disjoint resource types explain why.
result=dict(at=datetime.now(timezone.utc).isoformat(),
    raw_inventory_E1=inv,direct_ghost_tadpole=[dict(lines=lines,remaining=[dict(vertex=i,field=f,count=n) for (i,f),n in rest.items()]) for lines,rest in direct],
    measured_defects=['vertex-class certificate collision removes ghost sector already atE1',
        'antifield mutation changes no edge options; advertised negative is ineffective',
        'validator accepts no lines and invalid endpoints/types/ghost count',
        'all listed vertices have ghost0; gh1 needs a genuinely marked Ward insertion'],
    moving_index_claim='NOT_REPRODUCED_IN_2187_PARALLEL_EDGE_CASES; do not assert as measured bug',
    monotonicity_cases=mono_cases,full_enumeration_run=False,
    cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['raw_inventory_E1','direct_ghost_tadpole']},ensure_ascii=False))
