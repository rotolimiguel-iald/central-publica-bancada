"""Probe the derivative/extension commutator in the actual current insertion.

Reuses all five current blocks. Computes only the 00 two-ghost component,
for the two already fixed cutoff orderings; no normalization is fitted.
"""
from pathlib import Path
from datetime import datetime, timezone
from functools import lru_cache
import hashlib, json, time, uuid
import sympy as s
from position_metric_bubble_engine import BASIS, LABELS
from classical_current_jet_engine import current_coefficients, split_word
from metric_current_insertion_engine_v3 import CurrentInsertion
from mixed_b_h_current_engine_v3 import MixedCurrentInsertion
from ghost_current_insertion_engine import GhostCurrentInsertion
from opposite_endpoint_current_engine import OppositeEndpointCurrent
from full_loop_extension_engine import x, z, Q, dx, contact

H=Path(__file__).resolve().parent
D=H/'current_distributional_descendant_probe'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):
    assert not p.exists(),p
    data=json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8')
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data); assert tmp.read_bytes()==data;tmp.replace(p)

@lru_cache(None)
def rows_for(r):
    rows=[]
    for a in range(10):
        for b in range(a,10):
            data=[]
            for m,c in current_coefficients(a,b,r).items():
                pw,qw,kw=split_word(m)
                data.append(dict(pword=pw,qword=qw,kword=kw,current=list(map(str,c))))
            rows.append(dict(a=a,b=b,coefficients=data))
    return rows

def expression(a,r,lam,eta):
    T=BASIS[a]
    opposite=OppositeEndpointCurrent(a,r,lam,eta)
    return s.expand(CurrentInsertion(T,lam,eta,rows_for(r)).off_diagonal()/2
        +MixedCurrentInsertion(T,r,lam,eta).off_diagonal()
        +GhostCurrentInsertion(T,r,lam,eta).off_diagonal()
        +opposite.off_diagonal('metric')+opposite.off_diagonal('mixed'))

def parse(q): return s.sympify(q,locals={str(v):v for v in Q})

def main():
    D.mkdir(exist_ok=False)
    put(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
        target='00 component of s0 of the extended complete field-current insertion',
        scope='Restricted actual two-vertex current, not full J2/Q2',
        cases=[dict(lambda_x=[1,-1,0,0],eta_y=[1,0,0,0]),
               dict(lambda_x=[1,0,0,0],eta_y=[1,-1,0,0])],
        formula='P_current=R(F_current)+A_current; s0R(F) contains R(s0F)+sum_i(1+delta_i0) C_di(F_i0,0), then delta multiplication/local conversion',
        comparison='Compare complete hc defect with actual distributional current descendant; preserve nonzero differences',
        no_fit=True,stop_on_nonzero=False,script_sha256=sha(Path(__file__))))
    start=time.process_time();raw=[];current_local=[];correction=[]
    for order,filename in enumerate(['full_current_contact_matrix/results.json',
                                    'full_current_contact_matrix_swapped/results.json']):
        data=json.loads((H/filename).read_bytes())
        lam=tuple(data['lambda_x']);eta=tuple(data['eta_y']);L=tuple(a+b for a,b in zip(lam,eta))
        f=s.Integer(0);C=s.Integer(0);local=s.Integer(0)
        for i in range(4):
            a=LABELS.index((0,i));r=0;mult=1+int(i==0)
            F=expression(a,r,lam,eta)
            f-=mult*(dx(F,i)+lam[i]*F)
            # This is the extra contact from the outer BRST derivative;
            # it is not the already stored current-contact polynomial.
            C+=mult*contact(F,(i,))
            row=next(v for v in data['rows'] if v['a']==a and v['c']==r)
            A=sum(parse(row['parts'][key])*(s.Rational(1,2) if key=='Ymetric' else 1)
                  for key in ['Ymetric','Ymixed','Yghost','Xmetric','Xmixed'])
            A=A.subs(dict(zip(Q,[Q[j]+L[j] for j in range(4)])),simultaneous=True)
            local-=mult*(Q[i]+L[i])*A
            record=dict(order=order,h=[0,i],c=0,unextended_current=str(F),
                        outer_contact=str(s.expand(mult*contact(F,(i,)))),
                        cpu_seconds=time.process_time()-start)
            put(D/f'row_{order}_{i}.json',record)
            print(json.dumps(dict(order=order,i=i,terms=len(s.Add.make_args(F)),
                                  cpu_seconds=record['cpu_seconds'])),flush=True)
        raw.append(s.expand(f));current_local.append(s.expand(local))
        # chiX*derivative(delta) moves q->q-lambda, then acts on total weight.
        correction.append(s.expand(C.subs(dict(zip(Q,[Q[j]+eta[j] for j in range(4)])),simultaneous=True)))
    # Antisymmetrize the two-ghost bilocal functional under exchanging X,Y.
    # Both cutoff orderings were computed above, rather than silently equated.
    radial=sum(v*v for v in x)
    bilocal=s.cancel((raw[0]-raw[1].subs(dict(zip(x,[-v for v in x])),simultaneous=True)).subs(z,radial))
    L=(2,-1,0,0)
    adj=lambda v:s.expand(v.subs(dict(zip(Q,[-Q[j]-L[j] for j in range(4)])),simultaneous=True))
    local_piece=s.expand((current_local[0]+current_local[1])/2)
    extra=s.expand((correction[0]+correction[1])/2)
    descent=s.expand(local_piece-adj(local_piece)+extra-adj(extra))
    original=[]
    for filename in ['full_current_contact_matrix/results.json','full_current_contact_matrix_swapped/results.json']:
        data=json.loads((H/filename).read_bytes())
        original.append(parse(data['graded_adjoint_defect'][0][0]))
    target=s.expand(sum(original)/2)
    difference=s.expand(target-descent)
    result=dict(at=datetime.now(timezone.utc).isoformat(),cpu_seconds=time.process_time()-start,
        current_bilocal_antisymmetric_remainder=str(bilocal),
        bilocal_closed_off_diagonal=bool(bilocal==0),
        current_contact_variation=str(s.expand(local_piece-adj(local_piece))),
        extra_derivative_extension_contact=str(s.expand(extra-adj(extra))),
        distributional_current_descendant_if_bilocal_zero=str(descent),
        full_hc_defect_00_polarized=str(target),difference_full_minus_current=str(difference),
        comparison_zero=bool(difference==0),
        scope='00 only at two specified cutoff orderings; if bilocal remainder nonzero, local polynomial is not the whole descendant',
        normalization_selected=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
         [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']+
         sorted(D.glob('row_*.json'))],full_Q2=False))
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
