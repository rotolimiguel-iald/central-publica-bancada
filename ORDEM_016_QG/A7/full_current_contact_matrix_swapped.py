"""Build every h/c component for one nonconstant cutoff-jet pair."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
from functools import lru_cache
import hashlib,json,time,uuid,gc
import sympy as s
from full_loop_extension_engine import SymbolicRawLoop,loop_contact,Q
from position_metric_bubble_engine import BASIS,LABELS
from classical_current_jet_engine import current_coefficients,split_word
from metric_current_insertion_engine_v3 import CurrentInsertion
from mixed_b_h_current_engine_v3 import MixedCurrentInsertion
from ghost_current_insertion_engine import GhostCurrentInsertion
from opposite_endpoint_contact_engine import OppositeEndpointContact
from localized_source_boundary_engine import source_extension

H=Path(__file__).resolve().parent;D=H/'full_current_contact_matrix_swapped';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
lam=(1,0,0,0);eta=(1,-1,0,0);L=tuple(a+b for a,b in zip(lam,eta))
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),lambda_x=lam,eta_y=eta,
    target='All40 coefficients h_A c_r of fixed flat local-contact representative',
    diagnostic='s0 of h-c contact alone: graded formal-adjoint test with e^((lambda+eta)X)',
    caveat='Nonzero diagnostic may require remaining antifield sectors/descent; not automatically cohomological obstruction',
    weights_refitted=False,full_Q2=False,script_sha256=sha(Path(__file__))))
start=time.process_time();rows=[];A={}
def rows_for(r):
    out=[]
    for a in range(10):
        for b in range(a,10):
            data=[]
            for monomial,c in current_coefficients(a,b,r).items():
                pw,qw,kw=split_word(monomial)
                data.append(dict(pword=pw,qword=qw,kword=kw,current=list(map(str,c))))
            out.append(dict(a=a,b=b,coefficients=data))
    return out
source={r:source_extension(r,lam,eta) for r in range(4)}
current={r:rows_for(r) for r in range(4)}
for a,(i,j) in enumerate(LABELS):
    T=BASIS[a];metric=SymbolicRawLoop('metric',T,lam,eta);ghost=SymbolicRawLoop('ghost',T,lam,eta)
    for r in range(4):
        parts={}
        parts['pair']=loop_contact(ghost,r)-loop_contact(metric,r)/2
        parts['source']=(1 if i==j else 2)*source[r][i,j]
        parts['Ymetric']=CurrentInsertion(T,lam,eta,current[r]).extension_contact()/2
        parts['Ymixed']=MixedCurrentInsertion(T,r,lam,eta).extension_contact()
        parts['Yghost']=GhostCurrentInsertion(T,r,lam,eta).extension_contact()
        opposite=OppositeEndpointContact(a,r,lam,eta)
        parts['Xmetric']=opposite.extension_contact('metric');parts['Xmixed']=opposite.extension_contact('mixed')
        value=s.expand(sum(parts.values()));A[a,r]=value
        row=dict(a=a,h=[i,j],c=r,parts={k:str(v) for k,v in parts.items()},polynomial=str(value),cpu_seconds=time.process_time()-start)
        rows.append(row);put(f'component_{a}_{r}.json',row)
        print(json.dumps(dict(h=[i,j],c=r,terms=len(s.Poly(value,*Q).terms()),cpu_seconds=time.process_time()-start)),flush=True)
    gc.collect()

# Distribution A(q) is at Y, while partial_X delta acts on e^(LX)c after integration.
# Substitute q=D+L, then vary h_A by G(c)_A. No factor of two is guessed.
B=s.zeros(4)
for a,(i,j) in enumerate(LABELS):
    for r in range(4):
        f=A[a,r].subs({Q[k]:Q[k]+L[k] for k in range(4)},simultaneous=True)
        B[j,r]-=(Q[i]+L[i])*f;B[i,r]-=(Q[j]+L[j])*f
B=B.applyfunc(s.expand)
adj=B.T.applyfunc(lambda f:s.expand(f.subs({Q[k]:-Q[k]-L[k] for k in range(4)},simultaneous=True)))
defect=(B-adj).applyfunc(s.expand)
result=dict(at=datetime.now(timezone.utc).isoformat(),lambda_x=lam,eta_y=eta,rows=rows,
    cpu_seconds=time.process_time()-start,graded_adjoint_defect=[[str(defect[i,j]) for j in range(4)] for i in range(4)],
    closed_in_h_c_sector_alone=defect==s.zeros(4),full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ['rows','graded_adjoint_defect']}))
