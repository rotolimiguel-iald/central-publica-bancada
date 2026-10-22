"""Check the proposed local change against the principal BV identity.

No execution on import of check scripts; only the pure sparse engine is used.
"""
from pathlib import Path
from datetime import datetime, timezone
from time import perf_counter, process_time
import hashlib, json
from marked_polynomial_engine import *

HERE = Path(__file__).resolve().parent
DEST = HERE / 'ghost_coordinate'
DEST.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode()
    assert not p.exists(), str(p)
    temp = p.with_name(p.name + '.tmp')
    with temp.open('xb') as stream: stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(p)

new(DEST/'PRE_REGISTER.json', dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)), engine_sha256=sha(HERE/'marked_polynomial_engine.py'),
    primitive_sha256=sha(HERE/'ghost_bracket_primitive/results.json'),
    target='R1coord(H,k;l,v)=Lie_F(l)v H - K_(k+l) Z(H,k;l,v)',
    acceptance='Full symbolic principal h*cc identity or record sign failure; compare actual R1 separately',
    forbidden='Do not identify R1coord with actual R1 without comparison'))
start, cpu = perf_counter(), process_time()

def F(k,v): return add(scale(v,-QQ(3,8)*dot(k,k)),scale(k,dot(k,v)/4))
def Z(H,k,l,v):
    tr, hv, hk, hl = trace(H), mv(H,v), mv(H,k), mv(H,l)
    coefficient = tr*(-dot(k,k)/24 + QQ(3,16)*dot(k,l) - QQ(5,48)*dot(l,l))
    coefficient -= QQ(3,8)*dot(k,hl) + QQ(7,24)*dot(l,hl)
    out = scale(v, coefficient)
    out = add(out, scale(hv,dot(k,k)/12+dot(k,l)/4-dot(l,l)/24))
    return add(add(out,scale(hk,dot(k,v)/12)),scale(hl,dot(l,v)/4))
def pred(H,k,l,v):
    return madd(lie(H,k,l,F(l,v)),mscale(gauge(add(k,l),Z(H,k,l,v)),-1))

saved=json.loads((HERE/'ghost_bracket_primitive/results.json').read_bytes())
tri={(x['v'],x['w'],x['Y']): R.from_expr(__import__('sympy').sympify(x['triangle']))
     for x in saved['triangle_basis']}
basis=[]
for i in range(4):
    for j in range(i,4):
        basis.append([[ONE if (m,n) in ((i,j),(j,i)) else ZERO for n in range(4)] for m in range(4)])
checks=[]; mismatch=[]; symmetric=[]; negatives=[]
for ti,T in enumerate(basis):
    for vi,v in enumerate(axes):
        for wi,w in enumerate(axes):
            b1=[tri[vi,wi,i] for i in range(4)]
            free=madd(R0(add(P,Q),bracket(P,v,Q,w)),
                      madd(mscale(lie(R0(Q,w),Q,P,v),-1),lie(R0(P,v),P,Q,w)))
            left=pred(gauge(Q,w),Q,P,v)
            right=pred(gauge(P,v),P,Q,w)
            residue=inner(T,madd(madd(gauge(add(P,Q),b1),free),madd(mscale(left,-1),right)))
            assert residue==ZERO, ('coordinate_identity',ti,vi,wi,str(residue))
            checks.append([ti,vi,wi])
            ln,lmn=marked_numerators(T,Q,w,P,v)
            rn,rmn=marked_numerators(T,P,v,Q,w)
            actual_left=UVLG.extract(ln)-UVLM.extract(lmn)/4
            actual_right=UVRG.extract(rn)-UVRM.extract(rmn)/4
            dl=actual_left-inner(T,left); dr=actual_right-inner(T,right)
            assert dl==dr,('residual_symmetry',ti,vi,wi)
            symmetric.append([ti,vi,wi])
            if dl: mismatch.append(dict(T=ti,v=vi,w=wi,difference=str(dl)))
            # Reversing the Z sign must spoil at least one component.
            flip=2*inner(T,madd(gauge(add(P,Q),Z(gauge(P,v),P,Q,w)),
                                   mscale(gauge(add(P,Q),Z(gauge(Q,w),Q,P,v)),-1)))
            if flip: negatives.append([ti,vi,wi])
assert mismatch, 'Unexpected total equality; investigate before asserting it'
assert negatives
result=dict(statute='DERIVED_PRINCIPAL_GHOST_COORDINATE_COMPATIBILITY_NOT_FULL_VERTEX_MATCH',
    checks_passed=len(checks)+len(symmetric),coordinate_checks=len(checks),
    residual_symmetry_checks=len(symmetric),nonzero_mismatch_components=len(mismatch),
    mismatch=mismatch,negative_control='Reversing Z breaks the identity',
    negative_nonzero_components=len(negatives),full_hstar_hc_matched=False,
    full_Q2=False,gate_changed=False,source_sha256=sha(Path(__file__)),
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='mismatch'},ensure_ascii=False))
