"""Test whether either Euler ordering can alone span the measured h/c defect.

This tests polynomial span, not a fitted renormalization. No coefficients are selected.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from euler_ghost_descendant_contact_engine import Q,TAU,weighted_defect
H=Path(__file__).resolve().parent;D=H/'euler_descendant_span';assert not D.exists();D.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode('utf-8')
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
sources=[H/'euler_ghost_descendant_contact/results.json',
 H/'full_current_contact_matrix/results.json',H/'full_current_contact_matrix_swapped/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 question='Can any scalar normalization of the two existing ordered Euler descendants alone account for the measured localized h/c consistency defect?',
 scope='Polynomial span of existing measured representatives at fixed nonconstant cutoff jets, not full Ward identity or cohomology',
 acceptance='Rank and explicit coefficient-row minor; do not choose tau or change normalization to fit a scalar control',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources],script_sha256=sha(Path(__file__))))
start=time.process_time();checks=0
loc={str(q):q for q in Q};loc['tau']=TAU
mat=lambda rows:s.Matrix([[s.sympify(v,locals=loc) for v in row] for row in rows])
e,original,reverse=[json.loads(p.read_bytes()) for p in sources]
L=tuple(a+b for a,b in zip(e['lambda_x'],e['eta_y']))
D1=mat(e['weighted_antisymmetric_part']).subs(TAU,1)
D2=weighted_defect(mat(e['reverse_B']).subs(TAU,1),L)
target=mat(original['graded_adjoint_defect'])
target_reverse=mat(reverse['graded_adjoint_defect'])
assert tuple(reverse['lambda_x'])==tuple(e['eta_y']);checks+=1
assert tuple(reverse['eta_y'])==tuple(e['lambda_x']);checks+=1
assert L==tuple(a+b for a,b in zip(original['lambda_x'],original['eta_y']));checks+=1
rows=[]
for name,T in [('ordered',target),('cutoff_polarized',(target+target_reverse)/2)]:
    coeffs=[];labels=[]
    for i in range(4):
        for j in range(4):
            ps=[s.Poly(s.expand(M[i,j]),*Q) for M in (D1,D2,T)]
            maps=[dict(p.terms()) for p in ps]
            monomials=sorted(set().union(*(m.keys() for m in maps)),reverse=True)
            for power in monomials:
                values=[m.get(power,s.Integer(0)) for m in maps]
                if any(v!=0 for v in values):coeffs.append(values);labels.append(dict(entry=[i,j],powers=power))
    M=s.Matrix(coeffs)
    _,piv=M.T.rref();rank=len(piv)
    _,piv_gen=M[:,:2].T.rref();rank_gen=len(piv_gen)
    witness=[];det=None
    if rank==3 and rank_gen==2:
        W=M[list(piv),:];det=W.det();assert det!=0;checks+=1
        witness=[dict(**labels[k],coefficients=list(map(str,coeffs[k]))) for k in piv]
    in_span=rank==rank_gen
    # Record both outcomes honestly; there is no demanded nonzero result.
    rows.append(dict(target=name,generator_rank=rank_gen,augmented_rank=rank,in_span=in_span,
        coefficient_rows=len(coeffs),witness=witness,determinant=str(det),
        maximum_degrees=[max(s.Poly(s.expand(v),*Q).total_degree() for v in M0) for M0 in [D1,D2,T]]))
    checks+=1
report=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 rows=rows,normalization_selected=False,engines_changed=False,
 interpretation='If augmented rank exceeds two, no scalar global weight/allocation of these two ordered kernels alone removes this measured defect. This is a failure of that restricted completion, not a cohomological obstruction or failure of full BV theory.',
 next='Retain missing sectors/normalization of composite insertions in the full inhomogeneous Ward equation; do not infer closure by adjusting the q=0 coefficient.',
 full_Q2=False,gate_changed=False)
put('results.json',report)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(report))
