"""Find a local metric-dependent primitive for the measured ghost bracket.

This is a finite principal-sector linear algebra problem, not removal of the
complete finite causal anomaly and not a solution chosen by a model's vote.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from marked_polynomial_engine import *
HERE=Path(__file__).resolve().parent;DEST=HERE/'ghost_bracket_primitive';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'marked_polynomial_engine.py'),
    target='B1 - delta_F B = Z(Kp v,p;r,w)-Z(Kr w,r;p,v)',
    F='-3/8 p²v +1/4p(p.v), already measured, not fitted',
    ansatz='21 parity-even O4 contractions linear in symmetric H and v, degree2 in k,l',
    method='exact rational coefficient equations, all4 output *4v*4w, symbolic a,b,c',
    expectation='solve or report inconsistent rank; no assumption of exactness',
    forbidden='no claim to match entire h*hc vertex, finite anomaly or canonical counterterm hierarchy'))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,e):
    assert e==ZERO,(name,str(e));checks.append(name)
def reject(name,e):
    assert e!=ZERO,name;neg.append(name)
def F(k,v):return add(scale(v,-QQ(3,8)*dot(k,k)),scale(k,dot(k,v)/4))
def coord(p,v,r,w):
    return add(add(bracket(p,F(p,v),r,w),bracket(p,v,r,F(r,w))),scale(F(add(p,r),bracket(p,v,r,w)),-1))
def triangle(Y,p,v,r,w):
    k=add(q,p);l=add(r,scale(q,-1));ad=ghost_duals(q,p,v);bd=ghost_duals(scale(q,-1),r,w)
    def contract(ds,x):return [[sum((x[m]*ds[m][i][j] for m in range(4)),ZERO) for j in range(4)] for i in range(4)]
    n=inner(itr(contract(ad,l)),contract(bd,Y))-inner(itr(contract(ad,Y)),contract(bd,k))
    return UVTRI.extract(n)
def ansatz(H,k,l,v):
    hk,hl,hv=mv(H,k),mv(H,l),mv(H,v);tr=trace(H)
    kk,kl,ll=dot(k,k),dot(k,l),dot(l,l);kv,lv=dot(k,v),dot(l,v)
    terms=[scale(v,tr*x) for x in (kk,kl,ll)]
    terms += [scale(v,x) for x in (dot(k,hk),dot(k,hl),dot(l,hl))]
    terms += [scale(hv,x) for x in (kk,kl,ll)]
    terms += [scale(hk,kv),scale(hk,lv),scale(hl,kv),scale(hl,lv)]
    terms += [scale(k,tr*kv),scale(k,tr*lv),scale(l,tr*kv),scale(l,tr*lv)]
    terms += [scale(k,dot(v,hk)),scale(k,dot(v,hl)),scale(l,dot(v,hk)),scale(l,dot(v,hl))]
    assert len(terms)==21;return terms
names=['v trH k²','v trH k.l','v trH l²','v k.Hk','v k.Hl','v l.Hl',
       'Hv k²','Hv k.l','Hv l²','Hk k.v','Hk l.v','Hl k.v','Hl l.v',
       'k trH k.v','k trH l.v','l trH k.v','l trH l.v',
       'k v.Hk','k v.Hl','l v.Hk','l v.Hl']
rows=[];targets=[];data=[];triangle_basis=[]
for vi,v in enumerate(axes):
    for wi,w in enumerate(axes):
        za=ansatz(gauge(P,v),P,Q,w);zb=ansatz(gauge(Q,w),Q,P,v)
        cols=[add(x,scale(y,-1)) for x,y in zip(za,zb)]
        df=coord(P,v,Q,w)
        for yi,Y in enumerate(axes):
            measured=triangle(Y,P,v,Q,w);target=measured-df[yi]
            components=[x[yi] for x in cols]
            keys=set(target)
            for component in components:keys.update(component)
            for mon in sorted(keys):
                rows.append([s.Rational(z.get(mon,QQ.zero)) for z in components]);targets.append(s.Rational(target.get(mon,QQ.zero)))
            data.append((vi,wi,yi,target,components,measured,df[yi]))
            triangle_basis.append(dict(v=vi,w=wi,Y=yi,triangle=str(measured)))
M=s.Matrix(rows);rhs=s.Matrix(targets);rank=M.rank();aug_rank=M.row_join(rhs).rank()
print(json.dumps(dict(rows=M.rows,columns=M.cols,rank=rank,augmented_rank=aug_rank)),flush=True)
if rank!=aug_rank:
    result=dict(statute='MEDIDA_LOCAL_GHOST_PRIMITIVE_ANSATZ_INCONSISTENT',rank=rank,augmented_rank=aug_rank,
                next='Name missing allowed primitive rather than alter measured bracket')
else:
    solution,params=M.gauss_jordan_solve(rhs);choice={z:s.S.Zero for z in params}
    coeff=[QQ(int(z.p),int(z.q)) for z in [s.cancel(x.subs(choice)) for x in solution]]
    for vi,wi,yi,target,components,measured,df in data:
        check(f'primitive_{vi}_{wi}_{yi}',target-sum((x*c for x,c in zip(components,coeff)),ZERO))
    target_nonzero=next(item[3] for item in data if item[3])
    reject('bilinear_ghost_change_without_metric_primitive',target_nonzero)
    reject('reverse_primitive_sign',2*target_nonzero)
    # Already measured independent axis example c*_0 c_0(p)c_1(r): 7/24 at a=c=1,b=0.
    entry=next(z for z in data if z[:3]==(0,1,0))
    check('original_triangle_axis_normalization',entry[5].evaluate([(a,1),(b,0),(c,1)])-QQ(7,24))
    result=dict(statute='DERIVED_LOCAL_PRIMITIVE_FOR_PRINCIPAL_GHOST_BRACKET',
        rank=rank,augmented_rank=aug_rank,rows=M.rows,columns=M.cols,
        free_parameters=len(params),choice='All Gauss-Jordan free parameters set to zero; one representative, not canonical',
        nonzero_coefficients=[dict(index=i,term=names[i],coefficient=str(x)) for i,x in enumerate(coeff) if x],
        full_coefficients=list(map(str,coeff)),checks_passed=len(checks),checks=checks,negative_controls=neg,
        triangle_basis=triangle_basis,interpretation='B1=delta_F B+Delta_Z, a local metric-dependent correction, common4kappaA0 stripped',
        full_hstar_hc_matched=False,full_Q2=False,gate_changed=False)
result.update(source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
              wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','triangle_basis')},ensure_ascii=False),flush=True)
